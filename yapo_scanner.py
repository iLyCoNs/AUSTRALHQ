"""
MÓDULO INDEPENDIENTE: Escaneo de Yapo.cl
Se ejecuta como proceso separado - completamente aislado de Facebook/Comet
"""
import asyncio
import time
import re
import csv
import os
import sys
from playwright.async_api import async_playwright

CSV_FILE_PATH = r"c:\Users\LyCoNs\Desktop\AGENTES IA\VENDEDORES_MACROLOTES_MASTERPLAN_360.csv"
YAPO_BASE_URL = "https://www.yapo.cl/bienes-raices-venta-de-propiedades-lotes-y-terrenos/los-lagos.{page}?sort=f_added&dir=desc"
YAPO_PAGINAS = 5

HEADERS_B2B = [
    'Fecha', 'Nombre Vendedor', 'Telefono Contacto', 'Tipo Vendedor',
    'Superficie Has', 'Estado MasterPlan', 'Potencial Venta',
    'Ubicacion', 'Precio CLP UF', 'Detalles', 'Link Perfil',
    'Link Post Directo', 'Fuente', 'Estado Gestion', 'Notas Auditoria'
]

def sp(msg):
    try:
        print(f"[YAPO] {str(msg).encode('ascii','ignore').decode('ascii')}", flush=True)
    except Exception:
        pass

def es_mayor_5has(superficie_str, titulo):
    patron_ha = r'(\d+[,.]?\d*)\s*(ha|hect)'
    match = re.search(patron_ha, titulo.lower())
    if match:
        valor = float(match.group(1).replace(',', '.'))
        if valor >= 5:
            return True, valor
    if superficie_str:
        m2 = int(re.sub(r'\D', '', str(superficie_str)) or 0)
        if m2 >= 50000:
            return True, round(m2 / 10000, 1)
    return False, 0

def guardar_reporte_agente(agente_nombre, datos):
    if not datos: return
    now_str = time.strftime('%Y-%m-%d_%H-%M-%S')
    base_dir = os.path.join(r"c:\Users\LyCoNs\Desktop\AGENTES IA", "REPORTES_AGENTES", agente_nombre.upper())
    os.makedirs(base_dir, exist_ok=True)
    filename = os.path.join(base_dir, f"{agente_nombre.upper()}_{now_str}.json")
    try:
        reporte = {
            "agente": agente_nombre.upper(),
            "fecha_hora_local": time.strftime('%Y-%m-%d %H:%M:%S'),
            "total_registros": len(datos) if isinstance(datos, list) else 1,
            "datos": datos
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(reporte, f, indent=2, ensure_ascii=False)
        sp(f"[REPORTES] Guardado en carpeta {agente_nombre.upper()}: {filename}")
    except Exception as e:
        sp(f"[REPORTES ERROR] {e}")

def guardar_csv(leads):
    if not leads:
        return
    guardar_reporte_agente("YAPOCL", leads)
    existe = os.path.exists(CSV_FILE_PATH)
    try:
        with open(CSV_FILE_PATH, 'a', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=HEADERS_B2B)
            if not existe:
                writer.writeheader()
            for v in leads:
                writer.writerow(v)
        sp(f"{len(leads)} leads guardados en CSV")
    except Exception as e:
        sp(f"CSV ERROR: {e}")

async def main():
    sp(f"Iniciando - {YAPO_PAGINAS} paginas de Los Lagos (mas recientes)")
    total_leads = []

    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(channel="msedge", headless=False)
        except Exception:
            browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        for num_pag in range(1, YAPO_PAGINAS + 1):
            url = YAPO_BASE_URL.format(page=num_pag)
            sp(f"Pagina {num_pag}/{YAPO_PAGINAS} -> {url}")
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                await asyncio.sleep(3)
                sp(f"Pagina {num_pag} cargada: {(await page.title())[:40]}")

                # Scrolls para cargar lazy images
                for _ in range(6):
                    await page.evaluate("window.scrollBy(0, 1000);")
                    await asyncio.sleep(0.8)

                # Extractor especializado para estructura d3-ad-tile de Yapo
                avisos = await page.evaluate("""
                    () => {
                        const tiles = Array.from(document.querySelectorAll('.d3-ad-tile'));
                        return tiles.map(tile => {
                            const linkElem = tile.querySelector('a.d3-ad-tile__description, a[href*="/bienes-raices"]');
                            const link = linkElem ? 'https://www.yapo.cl' + (linkElem.getAttribute('href') || '') : '';
                            const titulo = ((tile.querySelector('.d3-ad-tile__title') || {}).innerText || '').trim();
                            const desc = ((tile.querySelector('.d3-ad-tile__short-description') || {}).innerText || '').trim();
                            const vendedor = ((tile.querySelector('.d3-ad-tile__seller span') || {}).innerText || '').trim();
                            const ubicacion = ((tile.querySelector('.d3-ad-tile__location span') || {}).innerText || '').trim();
                            const precio = ((tile.querySelector('.d3-ad-tile__price') || {}).innerText || '').trim();
                            const superficie = ((tile.querySelector('.d3-ad-tile__details-item') || {}).innerText || '').trim();
                            return { link, titulo, desc, vendedor, ubicacion, precio, superficie };
                        }).filter(a => a.link && a.titulo.length > 3);
                    }
                """)

                sp(f"Pagina {num_pag}: {len(avisos)} avisos extraidos del HTML")

                filtrados = []
                for av in avisos:
                    es_grande, has_calc = es_mayor_5has(av.get('superficie', ''), av.get('titulo', ''))
                    if es_grande:
                        av['has_calc'] = has_calc
                        filtrados.append(av)
                        sp(f"  TARGET: {av['titulo'][:55]} | {has_calc} Has | {av['precio']} | {av['ubicacion']}")
                        sp(f"          {av['link']}")

                sp(f"Pagina {num_pag}: {len(filtrados)} avisos >5 Has")
                total_leads.extend(filtrados)

            except Exception as e:
                sp(f"Pagina {num_pag} Error: {str(e)[:80]}")

        await browser.close()

    if total_leads:
        leads_csv = [{
            'Fecha': time.strftime('%Y-%m-%d %H:%M'),
            'Nombre Vendedor': av.get('vendedor', ''),
            'Telefono Contacto': 'Ver aviso en Yapo.cl',
            'Tipo Vendedor': 'Dueno Directo / Particular',
            'Superficie Has': f"{av.get('has_calc','?')} Has ({av.get('superficie','')})",
            'Estado MasterPlan': 'SIN MASTERPLAN - Target Perfecto',
            'Potencial Venta': 'ALTO - Ofrecer Servicio 360',
            'Ubicacion': av.get('ubicacion', ''),
            'Precio CLP UF': av.get('precio', ''),
            'Detalles': av.get('desc', '')[:200],
            'Link Perfil': '',
            'Link Post Directo': av.get('link', ''),
            'Fuente': 'Yapo.cl',
            'Estado Gestion': 'Nuevo Prospecto B2B',
            'Notas Auditoria': f"Yapo.cl: {av.get('titulo','')[:100]}"
        } for av in total_leads]
        guardar_csv(leads_csv)
        sp(f"COMPLETADO: {len(leads_csv)} avisos >5 Has guardados en CSV")
    else:
        sp("Sin avisos >5 Has encontrados")

if __name__ == "__main__":
    asyncio.run(main())
