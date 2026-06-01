
import os
import re
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

url = os.environ["STREAMLIT_APP_URL"]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto(url, wait_until="domcontentloaded", timeout=120000)

    try:
        page.get_by_role("button", name=re.compile("get this app back up|wake|despertar|app back up", re.I)).click(timeout=15000)
        page.wait_for_load_state("networkidle", timeout=120000)
    except PlaywrightTimeoutError:
        pass
    except:
        pass

    try:
        page.wait_for_selector('[data-testid="stAppViewContainer"]', timeout=120000)
    except:
        pass

    browser.close()
