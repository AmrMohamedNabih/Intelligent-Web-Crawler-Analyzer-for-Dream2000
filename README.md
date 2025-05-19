This project is an intelligent web crawler and analyzer tailored for the Dream2000 e-commerce website (https://dream2000.com/). 

It features:
  - Crawlability analysis based on the robots.txt file.
  - Data extraction of product details and homepage slider images.
  - A Streamlit dashboard for interacting with the crawler and downloading results.

Setup Instructions : 

- git clone https://github.com/AmrMohamedNabih/Intelligent-Web-Crawler-Analyzer-for-Dream2000.git
- pip install -r requirements.txt
- streamlit run app.py

(Usage Instructions)

- The Streamlit dashboard offers the following features:

    - Crawlability Analysis
      - Robots Summary: View crawlability rules from robots.txt (allowed/disallowed paths, crawl delays, etc.).
      - Permission Checker: Check if a specific URL can be crawled with a given user agent.
    - Site Analysis
      - Analysis Tools: Determine if the site relies heavily on JavaScript and check for RSS/API feeds.
    - Data Extraction
      - Extract Products: Retrieve product details (title, link, price, image URL) from categories and download as CSV.
      - Extract Slider: Fetch homepage slider images and download their URLs as CSV.

(Findings)

Crawlability Analysis:
  - Crawl Permission: Crawling is allowed for the user agent SmartCrawler/1.0.
  - JavaScript Usage: Most pages are crawlable with static tools (requests, BeautifulSoup), but the slider requires Playwright for       JavaScript rendering.
  - RSS/API Feeds: None detected.
  - Crawlability Score: 80/100, indicating excellent crawlability.

Extracted Data
  - Product Categories: Data extracted from:
    - Mobiles
    - Tablets
    - Laptops
    - Accessories
    - Corporate
    - Home Appliances
    - Conditioners
    - TVs
    - Fitness
  - Slider Images: Unique images extracted from the homepage slider.
  - Output: All data is downloadable as CSV files via the dashboard.
