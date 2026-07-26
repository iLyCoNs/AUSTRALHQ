import asyncio
from playwright.async_api import async_playwright

COMET_EXE_PATH = r"C:\Users\LyCoNs\AppData\Local\Perplexity\Comet\Application\comet.exe"
COMET_USER_DATA_PATH = r"C:\Users\LyCoNs\AppData\Local\Perplexity\Comet\User Data"

async def test():
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=COMET_USER_DATA_PATH,
            executable_path=COMET_EXE_PATH,
            headless=False,
            viewport=None,
            args=["--profile-directory=Profile 1", "--start-maximized"]
        )
        page = await context.new_page()
        await page.goto("https://www.facebook.com/groups/ventadeparcelaschile/", wait_until="domcontentloaded", timeout=30000)
        
        # Esperar mas tiempo para que el muro cargue completamente
        print("Esperando que el muro de Facebook cargue completamente (5 segundos)...")
        await asyncio.sleep(5)
        
        # Hacer un primer scroll para activar mas contenido
        await page.evaluate("window.scrollBy(0, 500);")
        await asyncio.sleep(2)
        
        titulo = await page.title()
        print(f"Titulo: {titulo}")
        
        # Intentar diferentes selectores para capturar el contenido
        texto_body = await page.inner_text("body")
        lineas = [l.strip() for l in texto_body.split("\n") if len(l.strip()) > 30]
        print(f"\nLineas de texto encontradas en el muro (primeras 20):")
        for i, linea in enumerate(lineas[:20], 1):
            print(f"  {i}. {linea[:100]}")
        
        print(f"\nTotal lineas utiles: {len(lineas)}")
        
        # Buscar numeros de telefono en el texto
        import re
        telefonos = re.findall(r'(\+?56\s?9?\s?\d{4}\s?\d{4}|\b9\s?\d{4}\s?\d{4}\b)', texto_body)
        if telefonos:
            print(f"\nTelefonos encontrados: {telefonos}")
        
        await context.close()

asyncio.run(test())
