# data_fetch.py

from bs4 import BeautifulSoup
from utils import fetch_url, logger
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from playwright.sync_api import sync_playwright
import time


def extract_products_from_page(url: str) -> list[dict]:
    """
    Fetch one page, parse the OL.products.list.items.product-items,
    and for each LI return a dict with:
      - image_url
      - title
      - link
      - price
    """
    resp = fetch_url(url)
    soup = BeautifulSoup(resp.content, "lxml")

    ol = soup.select_one("ol.products.list.items.product-items")
    if not ol:
        logger.warning(f"No product list found on {url}")
        return []

    products = []
    for li in ol.find_all("li"):
        # 1) extract the <a class="product-item-link">
        a = li.select_one("a.product-item-link")
        if not a:
            logger.debug("Missing <a class='product-item-link'>, skipping LI.")
            continue

        title = a.get_text(strip=True)
        link  = a.get("href", "").strip()

        # 2) extract price
        price_tag = li.select_one("span.price")
        price = price_tag.get_text(strip=True) if price_tag else ""

        # 3) extract nested image
        img = li.select_one(
            "div.product-item-info "
            "div.product-grid__image-wrapper "
            "a span.product-image-container "
            "span.product-image-wrapper img"
        )
        image_url = img.get("src", "").strip() if img else ""

        if not image_url:
            logger.debug(f"No image found for product '{title}'.")
        if not title or not link:
            logger.warning(f"Incomplete product entry: title={title!r}, link={link!r}")

        products.append({
            "title": title,
            "link": link,
            "price": price,
            "image_url": image_url,
        })

    return products

def extract_all_products(base_url: str, max_pages: int = 20) -> list[dict]:
    """
    Paginate through base_url?p=1..max_pages, call extract_products_from_page()
    on each, and accumulate a deduplicated list of product dicts.
    Deduplication is based on the product link.
    """
    all_products = []
    seen_links = set()

    parsed = urlparse(base_url)
    qs = parse_qs(parsed.query)

    for page in range(1, max_pages + 1):
        qs["p"] = [str(page)]
        new_query = urlencode(qs, doseq=True)
        paged = parsed._replace(query=new_query)
        page_url = urlunparse(paged)

        logger.info(f"Fetching page {page}: {page_url}")
        prods = extract_products_from_page(page_url)
        if not prods:
            logger.info("No products on this page; stopping pagination.")
            break

        # filter out already-seen links
        new_items = [p for p in prods if p["link"] not in seen_links]
        if not new_items:
            logger.info("All products on this page were duplicates; stopping.")
            break

        all_products.extend(new_items)
        for p in new_items:
            seen_links.add(p["link"])

    return all_products


def extract_slider_images(
    url: str,
    use_playwright: bool = True,
    max_clicks: int | None = None,
    slide_delay: float = 1.0
) -> list[str]:
    """
    Extract all unique slider image URLs from the homepage slider.

    - Supports Playwright for JS-driven sliders, clicking up to `max_clicks` times (if provided).
    - Extracts images from <img class="tp-rs-img"> or from <rs-sbg data-lazyload> attributes within each slide.

    Args:
        url: The page URL containing the slider.
        use_playwright: Whether to use Playwright for JS-driven navigation.
        max_clicks: Maximum number of arrow clicks to advance slides. If None, clicks until no arrow is found.
        slide_delay: Seconds to wait after each click/load.
    """
    image_urls: list[str] = []
    seen: set[str] = set()
    clicks = 0

    if use_playwright:
        logger.info(f"Launching Playwright to fetch slider from {url}")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=150000)
            time.sleep(slide_delay)

            while True:
                # collect images on current slide
                for el in page.query_selector_all("img.tp-rs-img"):
                    src = el.get_attribute("src")
                    if src and src not in seen:
                        seen.add(src)
                        image_urls.append(src)
                for bg in page.query_selector_all("rs-sbg[data-lazyload]"):
                    src = bg.get_attribute("data-lazyload")
                    if src and src not in seen:
                        seen.add(src)
                        image_urls.append(src)

                # stop if we've reached the click limit
                if max_clicks is not None and clicks >= max_clicks:
                    break

                # find and click next arrow
                arrow = page.query_selector("rs-arrow.tp-rightarrow.tparrows.hesperiden")
                logger.info(f"arrow :  {arrow}")

                if not arrow:
                    break
                try:
                    arrow.click()
                    clicks += 1
                    time.sleep(slide_delay)
                except Exception as e:
                    logger.debug(f"Arrow click failed ({e}); stopping.")
                    break

            browser.close()

    else:
        logger.info(f"Fetching static HTML for slider images from {url}")
        resp = fetch_url(url)
        soup = BeautifulSoup(resp.content, "lxml")
        for img in soup.select("img.tp-rs-img"):
            src = img.get("src", "").strip()
            if src and src not in seen:
                seen.add(src)
                image_urls.append(src)
        for bg in soup.select("rs-sbg[data-lazyload]"):
            src = bg.get("data-lazyload", "").strip()
            if src and src not in seen:
                seen.add(src)
                image_urls.append(src)

    if not image_urls:
        logger.warning("No slider images found.")
    return image_urls