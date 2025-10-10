from playwright.async_api import async_playwright
from app.models.store import Store
from sqlalchemy.future import select

async def scrape_store_002(product_name: str, db):
    """
    Obteniendo productos desde la segunda tienda usando Playwright.
    Devuelve una list de dicts con: name, price, url, store
    """
    result = await db.execute(select(Store).filter(Store.id == 2))
    store = result.scalars().first()
    if not store:
        raise ValueError("No se encontro la tienda con id 2")
    
    search_url = f"{store.url}catalogsearch/result/?q={product_name.replace(' ', '%20')}"
    results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print(f"visitando: {search_url}")
        await page.goto(search_url, timeout=60000)

        await page.wait_for_selector(".ais-Hits-list", timeout=30000)
        await page.wait_for_timeout(2000) # 2 segundos extras por que usa Algolia

        items = await page.query_selector_all(".ais-Hits-item")
        print(f"Productos encontrados: {len(items)}")

        for item in items:
            try:
                name_el = await item.query_selector("h3.result-title")
                price_el = await item.query_selector("div.price-wrapper span.after_special")
                link_el = await item.query_selector("a.result") 

                name = (await name_el.inner_text()) if name_el else "Sin nombre"
                price_text = (await price_el.inner_text()) if price_el else "C$0"
                price_value = float(price_text.replace("C$", "").replace(",", "").replace(" ", "",).strip()) if price_text else 0.0
                link = await link_el.get_attribute("href") if link_el else None

                results.append({
                    "name": name.strip(),
                    "price": price_value,
                    "url": link,
                    "store_id": store.id,
                })

            except Exception as e:
                print(f"Error procesando un producto: {e}")

        await browser.close()

    print(f"Scraping finalizado. Productos encontrados: {len(results)}")
    return results