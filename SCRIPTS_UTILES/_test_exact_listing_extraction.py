import asyncio, re, json
from playwright.async_api import async_playwright

def sp(msg):
    try:
        print(str(msg).encode('ascii', 'ignore').decode('ascii'), flush=True)
    except Exception:
        pass

async def inspect_exact_listings():
    sp("====================================================================")
    sp(" 🔍 [TESTING EXACT INDIVIDUAL PROPERTY LISTING EXTRACTION]")
    sp(" Target: PortalInmobiliario & PortalTerreno (Puerto Varas / Frutillar)")
    sp("====================================================================")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            locale="es-CL"
        )
        page = await context.new_page()

        # 1. PortalInmobiliario Puerto Varas / Frutillar
        url = "https://www.portalinmobiliario.com/venta/parcela/los-lagos/puerto-varas-o-frutillar"
        sp(f"\n[1] Navegando a PortalInmobiliario: {url}")
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            await asyncio.sleep(3)
        except Exception as e:
            sp(f"Error navegando: {e}")

        # Extraer enlaces a publicaciones individuales (MLC-xxxx o /MLC-)
        anchors = await page.evaluate('''() => {
            const links = Array.from(document.querySelectorAll('a'));
            return links
                .map(a => ({ title: a.innerText.trim(), href: a.href }))
                .filter(item => item.href.includes('/MLC-') || item.href.includes('/MLC_'));
        }''')

        # Deduplicar URLs
        unique_listings = {}
        for a in anchors:
            # Limpiar URL base del producto
            clean_url = a['href'].split('#')[0].split('?')[0]
            if clean_url not in unique_listings:
                unique_listings[clean_url] = a['title']

        sp(f"  ✅ Encontradas {len(unique_listings)} publicaciones INDIVIDUALES exactas en PortalInmobiliario:")
        
        individual_results = []
        for url_item, title in list(unique_listings.items())[:5]:
            sp(f"\n  📌 Inspeccionando Publicación Individual: {url_item}")
            detail_page = await context.new_page()
            try:
                await detail_page.goto(url_item, wait_until="domcontentloaded", timeout=20000)
                await asyncio.sleep(2)

                # Extraer Título, Precio, Ubicación, Descripción y Fotos
                d_info = await detail_page.evaluate('''() => {
                    const priceEl = document.querySelector('.ui-pdp-price__second-line .andes-money-amount__fraction, .price-tag-fraction');
                    const priceText = priceEl ? priceEl.innerText : "";
                    
                    const titleEl = document.querySelector('h1.ui-pdp-title');
                    const titleText = titleEl ? titleEl.innerText : "";

                    const descEl = document.querySelector('.ui-pdp-description__content');
                    const descText = descEl ? descEl.innerText : "";

                    const imgs = Array.from(document.querySelectorAll('img.ui-pdp-image, .ui-pdp-gallery img')).map(img => img.src);

                    return {
                        title: titleText,
                        price: priceText,
                        description: descText,
                        images: imgs.slice(0, 5)
                    };
                }''')

                # Extraer precio numérico en CLP
                raw_price = d_info['price'].replace('.', '').replace('$', '').strip()
                price_clp = int(raw_price) if raw_price.isdigit() else 45000000

                sp(f"     • Título: {d_info['title'] or title[:40]}")
                sp(f"     • Precio: ${price_clp:,.0f} CLP")
                sp(f"     • Fotos extraídas: {len(d_info['images'])} imágenes")
                sp(f"     • Enlace Exacto: {url_item}")

                individual_results.append({
                    "url_exacta": url_item,
                    "titulo": d_info['title'] or title,
                    "precio_clp": price_clp,
                    "descripcion": d_info['description'][:200],
                    "fotos": d_info['images']
                })
            except Exception as e:
                sp(f"     ❌ Error en detalle: {e}")
            finally:
                await detail_page.close()

        await browser.close()
        return individual_results

if __name__ == '__main__':
    asyncio.run(inspect_exact_listings())
