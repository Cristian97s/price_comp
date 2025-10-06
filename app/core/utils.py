from playwright.async_api import async_playwright

async def scrape_price(url: str) -> float:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        price = await page.locator(".price").inner_text()
        await browser.close()
        return float(price.replace("$", "").strip())
