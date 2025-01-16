import time
from tqdm import tqdm
import os
import requests
from playwright.sync_api import sync_playwright
import json
import random
import asyncio

SBR_WSC_CDP1 = "wss://brd-customer-hl_0bc9c3ef-zone-scraping_browser3:43vx0yl5zj8i@brd.superproxy.io:9222"
SBR_WSC_CDP2 = {"server": "http://51.254.78.223:80/"}

GPTproxies = [
    "http://45.152.188.248:3128",
    "http://103.231.78.36:80",
    "http://154.236.189.54:8080",
    "http://45.158.186.253:8080",
    "http://103.159.46.4:83",
    "http://47.254.20.82:80",
    "http://206.81.27.58:1080",
    "http://103.214.113.232:80",
    "http://139.5.29.97:39241",
    "http://198.8.92.143:3128}",
]

randomIdx = int(random.random() * len(GPTproxies))


# look for for some other proxy (check wss)

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
    "Accept-Language": "fr-Fr q=0.9",
}

URL = "https://amazon.fr/"
SEARCH_PARAM = "s?k=applewatchse2"


def scrape_urls(page):
    try:
        print(f"Scraping URLs")
        urls = page.eval_on_selector_all(
            ".a-size-mini.a-spacing-none.a-color-base.s-line-clamp-4 > a",
            " ele => ele.map(e=> e.href)",
        )

        print(f"Found {len(urls)} URLs")
        page.close()
        return urls

    except Exception as e:
        print(f"Exception occured scraping urls: {str(e)[:50]}")
        return {}


def scrape_url(url_number, url):
    try:
        title = url.eval_on_selector("#productTitle", "el => el.textContent")
        imgSrc = url.eval_on_selector("#imgTagWrapperId > img", "el => el.src")
        rating = url.eval_on_selector(
            "#acrPopover .a-size-base.a-color-base", "el => el.textContent"
        )
        price = url.eval_on_selector(".a-price-whole", "el => el.textContent")
        decimalPrice = url.eval_on_selector(".a-price-fraction", "el => el.textContent")

        scraped_data = {
            "title": str(title).strip(),
            "imgSrc": imgSrc,
            "rating": rating,
            "price": price + decimalPrice,
        }

        return scraped_data

    except Exception as e:
        print(f"Exception occured scraping url {url_number}: {str(e)[:50]}")
        return {}


def main():
    with sync_playwright() as pw:
        # browser = pw.chromium.connect(SBR_WSC_CDP2, headers=header)

        browser = pw.chromium.launch(
            devtools=True, headless=True, proxy=GPTproxies[randomIdx]
        )

        page = browser.new_page()

        try:
            print(f"Navigating to {URL + SEARCH_PARAM}")
            page.goto(
                URL + SEARCH_PARAM, timeout=15000
            )  # Increase the timeout value to 30 seconds

            urls = scrape_urls(page)
            data = []

            for url_number, link in tqdm(enumerate(urls), total=len(urls)):
                # session_browser = pw.chromium.connect_over_cdp(SBR_WSC_CDP2)
                session_browser = pw.chromium.launch(
                    devtools=True, headless=True, proxy=GPTproxies[randomIdx]
                )
                session_page = session_browser.new_page()
                session_page.goto(link)

                page_data = scrape_url(url_number, session_page)
                data.append(page_data)

                session_page.close()

            format_data(data)

        except Exception as e:
            print(f"Exception occurued: {str(e)}")


def format_data(data):
    try:
        with open(f"AppleWatchSE2.json {time.asctime()}", "w") as file:
            json.dump(data, file)
            # file.write(",\n")
            print(f"Successfully wrote data to json file.")

    except Exception as e:
        print(f"Exception occured while writing json to file: {str(e)[:50]}")


main()
# use AsyncAPI for syncronised calls : https://www.asyncapi.com/docs
