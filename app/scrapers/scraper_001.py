from playwright.async_api import async_playwright
from app.models.store import Store
from sqlalchemy.future import select

async def scrape_store_001(product_name: str, db):
    """
    Obteniendo productos desde La primera tienda usando Playwright.
    Devuelve una lista de dicts con: name, price, url, store
    """
    result = await db.execute(select(Store).filter(Store.id == 1))
    store = result.scalars().first()
    if not store:
        raise ValueError("No se encontró la tienda con id 1")

    search_url = f"{store.url}search/{product_name.replace(' ', '%20')}"
    results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print(f"Visitando: {search_url}")
        await page.goto(search_url, timeout=60000)

        # Esperar que se carguen los productos
        await page.wait_for_selector("li.item.product.product-item", timeout=20000)

        # Obtener los elementos
        items = await page.query_selector_all("li.item.product.product-item")
        print(f"Productos encontrados: {len(items)}")

        for item in items:
            try:
                name_el = await item.query_selector("a.product-item-link")
                price_el = await item.query_selector("span.price")
                link = await name_el.get_attribute("href") if name_el else None

                name = (await name_el.inner_text()) if name_el else "Sin nombre"
                price_text = (await price_el.inner_text()) if price_el else "C$0"
                price_value = float(price_text.replace("C$", "").replace(",", "").replace(",", "",1)) if price_text else 0.0

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
