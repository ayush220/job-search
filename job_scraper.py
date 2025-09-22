import asyncio
import aiohttp
import pandas as pd
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from datetime import datetime
import json
import logging
import argparse
import sys

# Import company lists
from companies import greenhouse_companies

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_user_inputs():
    """Get filtering parameters from command line arguments"""
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Job Search Script')
    parser.add_argument('--title', type=str, default='software,backend',
                      help='Job title filter (comma-separated for multiple)')
    parser.add_argument('--location', type=str, default='all',
                      help='Location filter (comma-separated for multiple)')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Process command line arguments
    titles = [t.strip().lower() for t in args.title.split(',')] if args.title.lower() != 'all' else []
    locations = [l.strip().lower() for l in args.location.split(',')] if args.location.lower() != 'all' else []
    
    return {
        'titles': titles,
        'locations': locations
    }

class JobScraper:
    def __init__(self, filters=None):
        self.jobs = []
        self.ua = UserAgent()
        self.session = None
        self.filters = filters or {'titles': [], 'locations': []}

    async def setup_session(self):
        self.session = aiohttp.ClientSession(headers={
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        })

    async def close_session(self):
        if self.session:
            await self.session.close()

    async def fetch_page(self, url):
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    logger.error(f"Error fetching {url}: Status {response.status}")
                    return None
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return None

    def _matches_filters(self, title, location):
        """Check if job matches the filters"""
        # If no filters, include all
        if not self.filters['titles'] and not self.filters['locations']:
            return True
        
        # Check title match
        title_match = not self.filters['titles'] or any(t in title.lower() for t in self.filters['titles'])
        
        # Check location match
        location_match = not self.filters['locations'] or any(l in location.lower() for l in self.filters['locations'])
        
        return title_match and location_match

    async def scrape_greenhouse_jobs(self, companies):
        """Scrape jobs from Greenhouse ATS"""
        for company in companies:
            url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"
            try:
                async with self.session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        for job in data.get('jobs', []):
                            title = job.get('title', '')
                            location = job.get('location', {}).get('name', 'Remote/Various')
                            
                            if 'software' in title.lower() or 'engineer' in title.lower():
                                if self._matches_filters(title, location):
                                    self.jobs.append({
                                        'title': title,
                                        'company': company,
                                        'location': location,
                                        'link': job.get('absolute_url', ''),
                                        'source': f"{company} (Greenhouse)"
                                    })
                    else:
                        logger.warning(f"Failed to fetch jobs from {company}: {response.status}")
            except Exception as e:
                logger.error(f"Error scraping {company} on Greenhouse: {e}")

    def save_jobs(self, filename='jobs.csv'):
        if not self.jobs:
            logger.warning("No jobs found to save")
            return
        
        df = pd.DataFrame(self.jobs)
        df['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        df.to_csv(filename, index=False)
        logger.info(f"Saved {len(self.jobs)} jobs to {filename}")

async def main():
    # Get user inputs for filtering
    filters = get_user_inputs()
    
    # Print selected filters
    print("\nApplying filters:")
    if filters['titles']:
        print(f"Title filters: {', '.join(filters['titles'])}")
    else:
        print("Title filters: None (showing all titles)")
        
    if filters['locations']:
        print(f"Location filters: {', '.join(filters['locations'])}")
    else:
        print("Location filters: None (showing all locations)")

    scraper = JobScraper(filters)
    await scraper.setup_session()
    
    try:
        # Run scraping task
        await scraper.scrape_greenhouse_jobs(greenhouse_companies)
    except Exception as e:
        logger.error(f"Error during scraping: {e}")
    finally:
        await scraper.close_session()
    
    # Save results
    scraper.save_jobs()
    
    # Print summary
    if scraper.jobs:
        print(f"\nFound {len(scraper.jobs)} total jobs:")
        df = pd.DataFrame(scraper.jobs)
        if not df.empty and 'source' in df.columns:
            sources = df['source'].value_counts()
            for source, count in sources.items():
                print(f"{source}: {count} jobs")
        else:
            print("No job source information available")
    else:
        print("No jobs found")

if __name__ == "__main__":
    asyncio.run(main())
