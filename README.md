# Multi-Source Job Scraper

A web application that scrapes software engineering job listings from multiple sources including LinkedIn Jobs, Indeed, and company career pages.

## Features

- Web-based interface for easy job searching
- Asynchronous scraping for better performance
- Multiple job sources
- Automatic rate limiting and user agent rotation
- CSV export of results
- Error handling and logging

## Local Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/job-search-app.git
cd job-search-app
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python server.py
```

5. Open your browser and go to: http://localhost:10000

## Deployment

### Option 1: Render.com (Recommended)

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure the build command: `pip install -r requirements.txt`
4. Set the start command: `python server.py`
5. Deploy!

### Option 2: PythonAnywhere

1. Create a new Web App on PythonAnywhere
2. Upload your code via GitHub
3. Set up a virtual environment and install requirements
4. Configure the WSGI file to point to your application
5. Reload the web app

## Environment Variables

- `PORT`: Port to run the server on (default: 10000)

## Note

- Some websites may block automated scraping
- Company career pages may change their structure
- You may need to add proxies for production use
- Consider rate limiting for production use
