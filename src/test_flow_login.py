#!/usr/bin/env python3
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

COOKIES_PATH = Path("/root/.agy-avisii/.gemini/flow-manju-pipeline/config/flow_cookies.json")
SCREENSHOT_PATH = Path("/root/.agy-gabor/.gemini/antigravity-cli/brain/aba683fa-a376-46a0-93b9-3717daeb52a2/flow_account_check.png")

with open(COOKIES_PATH, "r", encoding="utf-8") as f:
    raw_cookies = json.load(f)

playwright_cookies = []
for c in raw_cookies:
    s = c.get("sameSite", "")
    s_val = "None" if str(s).lower() in ["no_restriction", "none"] else ("Strict" if str(s).lower() == "strict" else "Lax")
    playwright_cookies.append({
        "name": c.get("name"),
        "value": c.get("value"),
        "domain": c.get("domain"),
        "path": c.get("path", "/"),
        "secure": c.get("secure", True),
        "httpOnly": c.get("httpOnly", False),
        "sameSite": s_val
    })

print(f"Loaded {len(playwright_cookies)} cookies.")

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-blink-features=AutomationControlled"]
    )
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        accept_downloads=True
    )
    context.add_cookies(playwright_cookies)
    page = context.new_page()

    print("Navigating to https://flow.google.com/ ...")
    try:
        response = page.goto("https://flow.google.com/", wait_until="networkidle", timeout=60000)
        print(f"Response status: {response.status if response else 'None'}")
    except Exception as e:
        print(f"Goto error: {e}")

    time.sleep(5)
    print(f"Current URL: {page.url}")
    print(f"Title: {page.title()}")

    # Take screenshot
    page.screenshot(path=str(SCREENSHOT_PATH), full_page=True)
    print(f"Saved screenshot to {SCREENSHOT_PATH}")

    # Check for text elements indicating credits / user profile / projects
    content = page.content()
    print("Page text snippet (first 1000 chars):")
    text_content = page.locator("body").inner_text()
    print(text_content[:1500])

    browser.close()
