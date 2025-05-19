import requests
import urllib.robotparser
import logging
from bs4 import BeautifulSoup
import time
from playwright.sync_api import sync_playwright
import streamlit as st

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Robots.txt parser
rp = urllib.robotparser.RobotFileParser()
rp.set_url("https://dream2000.com/robots.txt")
rp.read()

# Fetch URL helper

def fetch_url(url: str) -> requests.Response:
    headers = {"User-Agent": "SmartCrawler/1.0"}
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp

# Robots summary
def get_robots_summary() -> str:
    text = fetch_url(rp.url).text
    allowed, disallowed, sitemaps = [], [], []
    crawl_delay = None
    for line in text.splitlines():
        l = line.strip().lower()
        if l.startswith('allow:'):    allowed.append(line.split(':',1)[1].strip())
        elif l.startswith('disallow:'): disallowed.append(line.split(':',1)[1].strip())
        elif l.startswith('crawl-delay:'): crawl_delay = line.split(':',1)[1].strip()
        elif l.startswith('sitemap:'):    sitemaps.append(line.split(':',1)[1].strip())
    return (
        f"Allowed paths: {allowed}\n"
        f"Disallowed paths: {disallowed}\n"
        f"Crawl-delay: {crawl_delay}\n"
        f"Sitemap links: {sitemaps}\n"
    )

# Permission checker
def can_crawl(url: str, user_agent: str = "SmartCrawler/1.0") -> bool:
    return rp.can_fetch(user_agent, url)

# JS-heavy check

def fetch_url_with_retries(url: str, retries: int = 3, backoff: float = 2.0) -> requests.Response:
    headers = {"User-Agent": "SmartCrawler/1.0"}
    for attempt in range(1, retries+1):
        try:
            return requests.get(url, headers=headers, timeout=10)
        except requests.exceptions.RequestException as e:
            logger.warning(f"Fetch attempt {attempt} failed: {e}")
            if attempt < retries:
                time.sleep(backoff * attempt)
            else:
                raise

def is_javascript_heavy(url: str) -> bool:
    try:
        resp = fetch_url_with_retries(url)
        soup = BeautifulSoup(resp.text, "html.parser")
        visible_text = soup.get_text(strip=True)
        return len(visible_text) < 100
    except Exception as e:
        logger.error(f"JS-heavy check failed after retries: {e}")
        return True


# RSS/API feeders check
def check_rss_feeds(domain: str) -> list[str]:
    candidates = ["/feed", "/rss", "/feeds/posts/default", "/api"]
    found = []
    for path in candidates:
        u = domain.rstrip("/") + path
        try:
            r = requests.get(u, timeout=5)
            ct = r.headers.get("Content-Type","")
            if "xml" in ct or "json" in ct:
                found.append(u)
        except:
            continue
    return found

# Playwright renderer
def get_rendered_html_with_playwright(url: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=15000)
        time.sleep(3)
        html = page.content()
        browser.close()
        return html
def show_crawlability_report(url: str):
    """Compute and render a crawlability score + recommendations."""
    allowed    = can_crawl(url)
    logger.info(allowed)
    js_heavy   = is_javascript_heavy(url)
    logger.info(js_heavy)
    feeds      = check_rss_feeds(url)
    logger.info(feeds)
    has_feeds  = bool(feeds)
    logger.info(has_feeds)

    # Score calculation
    score = 100
    if not allowed:  score -= 50
    if js_heavy:     score -= 30
    if not has_feeds: score -= 20
    score = max(0, score)

    # Recommendations list
    tools = []
    if not allowed:
        tools.append("• Respect robots.txt: use `requests` + `robotsparser`")
    if js_heavy:
        tools.append("• Use a headless browser (Playwright or Selenium)")
    else:
        tools.append("• Static fetcher: `requests` + `BeautifulSoup`")
    if has_feeds:
        tools.append("• You can also fetch RSS/API endpoints directly")

    # Render
    st.markdown("---")
    st.subheader("📊 Crawlability Report")
    st.metric("Crawlability Score", f"{score}/100")
    st.write("**Recommendations:**")
    for rec in tools:
        st.write(rec)
