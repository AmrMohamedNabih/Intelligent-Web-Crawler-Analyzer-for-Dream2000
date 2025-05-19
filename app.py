import streamlit as st
import pandas as pd
from utils import (
    get_robots_summary,
    can_crawl,
    is_javascript_heavy,
    check_rss_feeds,
    show_crawlability_report
)
from data_fetch import (
    extract_all_products,
    extract_slider_images
)

st.set_page_config(page_title="🕷️ Dream2000 Crawler", layout="wide")

# Sidebar menu
pages = [
    "Robots Summary",
    "Permission Checker",
    "Site Analysis",
    "Extract Mobiles",
    "Extract Slider",
    "Extract Tablets",
    "Extract Laptops",
    "Extract accessories",
    "Extract corporate",
    "Extract appliances",
    "Extract conditioners",
    "Extract tvs",
    "Extract fitness",

]
choice = st.sidebar.selectbox("Navigation", pages)

if choice == "Robots Summary":
    st.title("Summary of Crawlability Rules")
    summary = get_robots_summary()
    st.text(summary)
    show_crawlability_report("https://dream2000.com/")
    st.download_button(
        "Download robots.txt summary",
        summary,
        "robots_summary.txt",
        "text/plain"
    )

elif choice == "Permission Checker":
    st.title("Check If Crawling Is Allowed")
    ua = st.text_input("User-Agent", "SmartCrawler/1.0")
    url = st.text_input("URL to check", "https://dream2000.com/")
    if st.button("Check Permission"):
        if can_crawl(url, ua):
            st.success("✅ Crawling ALLOWED.")
        else:
            st.error("❌ Crawling NOT ALLOWED.")

elif choice == "Site Analysis":
    st.title("Site Analysis Tools")
    url = st.text_input("Enter URL to analyze", "https://dream2000.com/")
    if st.button("Analyze"):
        if is_javascript_heavy(url):
            st.warning("⚠️ JS-heavy site detected.")
        else:
            st.success("✅ Static site.")
        feeds = check_rss_feeds(url)
        if feeds:
            st.info("📡 Feeds / APIs found:")
            for f in feeds:
                st.write(f)
        else:
            st.info("ℹ️ No feeds/APIs detected.")

elif choice == "Extract Mobiles":
    st.title("📦 Preview Products from Mobile List")
    base_url = st.text_input(
        "Product list base URL",
        value="https://dream2000.com/mobiles.html",
    )
    max_pages = st.number_input(
        "Max pages to crawl", 1, 100, 10, 1
    )
    if st.button("Fetch & Preview Mobiles"):
        if not can_crawl(base_url):
            st.error("❌ Crawling disallowed by robots.txt.")
        else:
            with st.spinner("Crawling pages…"):
                products = extract_all_products(base_url, max_pages)
            if not products:
                st.warning("No products found.")
            else:
                st.success(f"Collected {len(products)} unique products.")
                per_row = 3
                for i in range(0, len(products), per_row):
                    cols = st.columns(per_row)
                    for col, prod in zip(cols, products[i : i + per_row]):
                        with col:
                            if prod["image_url"]:
                                st.image(prod["image_url"], use_container_width=True)
                            st.markdown(f"**[{prod['title']}]({prod['link']})**")
                            st.markdown(f"*{prod['price']}*")
                df = pd.DataFrame(products)
                st.download_button(
                    "Download products as CSV",
                    df.to_csv(index=False),
                    "products.csv",
                    "text/csv",
                )

elif choice == "Extract Tablets":
    st.title("📦 Preview Products from Tablet List")
    base_url = st.text_input(
        "Product list base URL",
        value="https://dream2000.com/tablets.html",
    )
    max_pages = st.number_input(
        "Max pages to crawl", 1, 100, 10, 1
    )
    if st.button("Fetch & Preview Tablets"):
        if not can_crawl(base_url):
            st.error("❌ Crawling disallowed by robots.txt.")
        else:
            with st.spinner("Crawling pages…"):
                products = extract_all_products(base_url, max_pages)
            if not products:
                st.warning("No tablets found.")
            else:
                st.success(f"Collected {len(products)} unique tablets.")
                per_row = 3
                for i in range(0, len(products), per_row):
                    cols = st.columns(per_row)
                    for col, prod in zip(cols, products[i : i + per_row]):
                        with col:
                            if prod["image_url"]:
                                st.image(prod["image_url"], use_container_width=True)
                            st.markdown(f"**[{prod['title']}]({prod['link']})**")
                            st.markdown(f"*{prod['price']}*")
                df = pd.DataFrame(products)
                st.download_button(
                    "Download tablets as CSV",
                    df.to_csv(index=False),
                    "tablets.csv",
                    "text/csv",
                )

elif choice == "Extract Laptops":
    st.title("📦 Preview Products from Laptop/Notebook List")
    base_url = st.text_input(
        "Product list base URL",
        value="https://dream2000.com/laptop-notebook.html",
    )
    max_pages = st.number_input(
        "Max pages to crawl", 1, 100, 10, 1
    )
    if st.button("Fetch & Preview Laptops"):
        if not can_crawl(base_url):
            st.error("❌ Crawling disallowed by robots.txt.")
        else:
            with st.spinner("Crawling pages…"):
                products = extract_all_products(base_url, max_pages)
            if not products:
                st.warning("No laptops found.")
            else:
                st.success(f"Collected {len(products)} unique laptops.")
                per_row = 3
                for i in range(0, len(products), per_row):
                    cols = st.columns(per_row)
                    for col, prod in zip(cols, products[i : i + per_row]):
                        with col:
                            if prod["image_url"]:
                                st.image(prod["image_url"], use_container_width=True)
                            st.markdown(f"**[{prod['title']}]({prod['link']})**")
                            st.markdown(f"*{prod['price']}*")
                df = pd.DataFrame(products)
                st.download_button(
                    "Download laptops as CSV",
                    df.to_csv(index=False),
                    "laptops.csv",
                    "text/csv",
                )

elif choice == "Extract accessories":
    st.title("📦 Preview Products from Computer List")
    base_url = st.text_input(
        "Product list base URL",
        value="https://dream2000.com/accessories.html",
    )
    max_pages = st.number_input(
        "Max pages to crawl", 1, 100, 10, 1
    )
    if st.button("Fetch & Preview accessories"):
        if not can_crawl(base_url):
            st.error("❌ Crawling disallowed by robots.txt.")
        else:
            with st.spinner("Crawling pages…"):
                products = extract_all_products(base_url, max_pages)
            if not products:
                st.warning("No accessories found.")
            else:
                st.success(f"Collected {len(products)} unique accessories.")
                per_row = 3
                for i in range(0, len(products), per_row):
                    cols = st.columns(per_row)
                    for col, prod in zip(cols, products[i : i + per_row]):
                        with col:
                            if prod["image_url"]:
                                st.image(prod["image_url"], use_container_width=True)
                            st.markdown(f"**[{prod['title']}]({prod['link']})**")
                            st.markdown(f"*{prod['price']}*")
                df = pd.DataFrame(products)
                st.download_button(
                    "Download accessories as CSV",
                    df.to_csv(index=False),
                    "accessories.csv",
                    "text/csv",
                )
elif choice == "Extract corporate":
    st.title("📦 Preview Products from Computer List")
    base_url = st.text_input(
        "Product list base URL",
        value="https://dream2000.com/corporate.html",
    )
    max_pages = st.number_input(
        "Max pages to crawl", 1, 100, 10, 1
    )
    if st.button("Fetch & Preview corporate"):
        if not can_crawl(base_url):
            st.error("❌ Crawling disallowed by robots.txt.")
        else:
            with st.spinner("Crawling pages…"):
                products = extract_all_products(base_url, max_pages)
            if not products:
                st.warning("No corporate found.")
            else:
                st.success(f"Collected {len(products)} unique corporate.")
                per_row = 3
                for i in range(0, len(products), per_row):
                    cols = st.columns(per_row)
                    for col, prod in zip(cols, products[i : i + per_row]):
                        with col:
                            if prod["image_url"]:
                                st.image(prod["image_url"], use_container_width=True)
                            st.markdown(f"**[{prod['title']}]({prod['link']})**")
                            st.markdown(f"*{prod['price']}*")
                df = pd.DataFrame(products)
                st.download_button(
                    "Download corporate as CSV",
                    df.to_csv(index=False),
                    "corporate.csv",
                    "text/csv",
                )
elif choice == "Extract appliances":
    st.title("📦 Preview Products from Computer List")
    base_url = st.text_input(
        "Product list base URL",
        value="https://dream2000.com/home-appliances.html",
    )
    max_pages = st.number_input(
        "Max pages to crawl", 1, 100, 10, 1
    )
    if st.button("Fetch & Preview appliances"):
        if not can_crawl(base_url):
            st.error("❌ Crawling disallowed by robots.txt.")
        else:
            with st.spinner("Crawling pages…"):
                products = extract_all_products(base_url, max_pages)
            if not products:
                st.warning("No appliances found.")
            else:
                st.success(f"Collected {len(products)} unique appliances.")
                per_row = 3
                for i in range(0, len(products), per_row):
                    cols = st.columns(per_row)
                    for col, prod in zip(cols, products[i : i + per_row]):
                        with col:
                            if prod["image_url"]:
                                st.image(prod["image_url"], use_container_width=True)
                            st.markdown(f"**[{prod['title']}]({prod['link']})**")
                            st.markdown(f"*{prod['price']}*")
                df = pd.DataFrame(products)
                st.download_button(
                    "Download appliances as CSV",
                    df.to_csv(index=False),
                    "appliances.csv",
                    "text/csv",
                )
elif choice == "Extract conditioners":
    st.title("📦 Preview Products from Computer List")
    base_url = st.text_input(
        "Product list base URL",
        value="https://dream2000.com/conditioners.html",
    )
    max_pages = st.number_input(
        "Max pages to crawl", 1, 100, 10, 1
    )
    if st.button("Fetch & Preview conditioners"):
        if not can_crawl(base_url):
            st.error("❌ Crawling disallowed by robots.txt.")
        else:
            with st.spinner("Crawling pages…"):
                products = extract_all_products(base_url, max_pages)
            if not products:
                st.warning("No conditioners found.")
            else:
                st.success(f"Collected {len(products)} unique conditioners.")
                per_row = 3
                for i in range(0, len(products), per_row):
                    cols = st.columns(per_row)
                    for col, prod in zip(cols, products[i : i + per_row]):
                        with col:
                            if prod["image_url"]:
                                st.image(prod["image_url"], use_container_width=True)
                            st.markdown(f"**[{prod['title']}]({prod['link']})**")
                            st.markdown(f"*{prod['price']}*")
                df = pd.DataFrame(products)
                st.download_button(
                    "Download conditioners as CSV",
                    df.to_csv(index=False),
                    "conditioners.csv",
                    "text/csv",
                )
elif choice == "Extract tvs":
    st.title("📦 Preview Products from Computer List")
    base_url = st.text_input(
        "Product list base URL",
        value="https://dream2000.com/tvs/brands.html",
    )
    max_pages = st.number_input(
        "Max pages to crawl", 1, 100, 10, 1
    )
    if st.button("Fetch & Preview tvs"):
        if not can_crawl(base_url):
            st.error("❌ Crawling disallowed by robots.txt.")
        else:
            with st.spinner("Crawling pages…"):
                products = extract_all_products(base_url, max_pages)
            if not products:
                st.warning("No tvs found.")
            else:
                st.success(f"Collected {len(products)} unique tvs.")
                per_row = 3
                for i in range(0, len(products), per_row):
                    cols = st.columns(per_row)
                    for col, prod in zip(cols, products[i : i + per_row]):
                        with col:
                            if prod["image_url"]:
                                st.image(prod["image_url"], use_container_width=True)
                            st.markdown(f"**[{prod['title']}]({prod['link']})**")
                            st.markdown(f"*{prod['price']}*")
                df = pd.DataFrame(products)
                st.download_button(
                    "Download tvs as CSV",
                    df.to_csv(index=False),
                    "tvs.csv",
                    "text/csv",
                )
elif choice == "Extract fitness":
    st.title("📦 Preview Products from Computer List")
    base_url = st.text_input(
        "Product list base URL",
        value="https://dream2000.com/fitness.html",
    )
    max_pages = st.number_input(
        "Max pages to crawl", 1, 100, 10, 1
    )
    if st.button("Fetch & Preview fitness"):
        if not can_crawl(base_url):
            st.error("❌ Crawling disallowed by robots.txt.")
        else:
            with st.spinner("Crawling pages…"):
                products = extract_all_products(base_url, max_pages)
            if not products:
                st.warning("No fitness found.")
            else:
                st.success(f"Collected {len(products)} unique fitness.")
                per_row = 3
                for i in range(0, len(products), per_row):
                    cols = st.columns(per_row)
                    for col, prod in zip(cols, products[i : i + per_row]):
                        with col:
                            if prod["image_url"]:
                                st.image(prod["image_url"], use_container_width=True)
                            st.markdown(f"**[{prod['title']}]({prod['link']})**")
                            st.markdown(f"*{prod['price']}*")
                df = pd.DataFrame(products)
                st.download_button(
                    "Download fitness as CSV",
                    df.to_csv(index=False),
                    "fitness.csv",
                    "text/csv",
                )
elif choice == "Extract Slider":
    st.title("🎞️ Preview Homepage Slider Images")
    slider_url = st.text_input(
        "Page URL",
        value="https://dream2000.com/"
    )
    use_playwright = st.checkbox(
        "Use Playwright to advance slides (JS)", 
        value=True
    )
    max_clicks = st.number_input(
        "Max slider clicks (leave 0 for unlimited)",
        min_value=0,
        value=0,
        step=1
    )

    if st.button("Fetch & Preview Slider Images"):
        if not can_crawl(slider_url):
            st.error("❌ Crawling disallowed by robots.txt.")
        else:
            with st.spinner("Extracting slider images…"):
                limit = max_clicks or None
                imgs = extract_slider_images(
                    slider_url,
                    use_playwright=use_playwright,
                    max_clicks=limit,
                    slide_delay=1.0
                )

            if not imgs:
                st.warning("No slider images found.")
            else:
                st.success(f"Found {len(imgs)} unique slider images.")

                # --- display in a grid: 4 columns per row, images 200px wide ---
                cols_per_row = 4
                for row_start in range(0, len(imgs), cols_per_row):
                    row_imgs = imgs[row_start : row_start + cols_per_row]
                    cols = st.columns(len(row_imgs))
                    for col, img_url in zip(cols, row_imgs):
                        with col:
                            st.image(img_url, width=200)

                # Download CSV of URLs
                df = pd.DataFrame({"slider_image_url": imgs})
                st.download_button(
                    "Download slider image URLs as CSV",
                    df.to_csv(index=False),
                    "slider_images.csv",
                    "text/csv"
                )
