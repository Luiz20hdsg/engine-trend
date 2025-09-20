
from playwright.sync_api import sync_playwright

url = "https://us.shein.com/trends/SHEIN-Trends-sc-00679470.html"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url, wait_until='domcontentloaded', timeout=60000)
    for _ in range(5):
        page.keyboard.press('PageDown')
        page.wait_for_timeout(1000)
    content = page.content()
    browser.close()

with open("/Users/mymac/trend-engine/app/services/collectors/manual_html/shein_us.html", "w", encoding="utf-8") as f:
    f.write(content)

print("HTML content saved to shein_us.html")
