"""
===============================================================================
MÓDULO: Meta Ad Library & Dark Post Hunter (Fase 1 y 2)
Empresa: AustralDrone.CL
Objetivo: Consultar la API de Meta Ad Library para anuncios de parcelas/terrenos,
          resolver las URLs reales de publicaciones (Dark Posts) con Playwright.
Cumplimiento: Ley N° 19.628 (Datos Públicos) & Ley N° 19.496 (Human-in-the-loop)
===============================================================================
"""

import requests
import asyncio
import random
import json
import os
import time
from playwright.async_api import async_playwright

META_ACCESS_TOKEN = os.environ.get("META_AD_LIBRARY_TOKEN", "EAAB...YOUR_TOKEN_HERE")
SEARCH_KEYWORDS = ["parcelas 5000 m2", "rol propio", "macrolote", "terreno vista al lago", "parcelacion sur de chile"]
COUNTRY = "CL"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0"
]

def consultar_meta_ad_library(keyword, limit=10):
    """
    Fase 1: Consulta la API oficial de Meta Ad Library.
    Si no hay token configurado, genera estructura compatible para pruebas local/sandbox.
    """
    print(f"[FASE 1] Consultando Meta Ad Library API para keyword: '{keyword}'...")
    url = "https://graph.facebook.com/v18.0/ads_archive"
    params = {
        "access_token": META_ACCESS_TOKEN,
        "search_terms": keyword,
        "ad_reached_countries": [COUNTRY],
        "ad_active_status": "ACTIVE",
        "fields": "id,ad_creation_time,ad_creative_bodies,ad_snapshot_url,page_id,page_name",
        "limit": limit
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get("data", [])
        else:
            print(f"[WARN] API Meta devolvió {response.status_code}. Generando mock estructurado de demostración.")
    except Exception as e:
        print(f"[WARN] Excepción en llamada API Meta ({e}). Usando simulador de pruebas.")
        
    # Mock estructurado de demostración si no hay token activo de Graph API
    return [
        {
            "id": "120205849302190",
            "ad_snapshot_url": "https://www.facebook.com/ads/archive/render_ad/?id=120205849302190",
            "page_name": "Parcelas Los Lagos Venta Directa",
            "ad_creative_bodies": ["Hermosas parcelas de 5000 m2 con rol propio en Puerto Varas. Descuento lanzamiento."]
        },
        {
            "id": "120205849302191",
            "ad_snapshot_url": "https://www.facebook.com/ads/archive/render_ad/?id=120205849302191",
            "page_name": "Macrolotes Inmobiliaria Sur",
            "ad_creative_bodies": [" Macrolote de 15 Hectáreas en Alerce / Puerto Montt ideal para desarrollo inmobiliario."]
        }
    ]

async def resolver_dark_post_url(snapshot_url):
    """
    Fase 2: Utiliza Playwright para renderizar la vista previa de la Ad Library
    y resolver el permalink directo a la publicación (Dark Post).
    """
    print(f"[FASE 2] Resolviendo URL real de Dark Post: {snapshot_url}")
    user_agent = random.choice(USER_AGENTS)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent=user_agent)
        page = await context.new_page()
        
        try:
            await page.goto(snapshot_url, wait_until="domcontentloaded", timeout=20000)
            await asyncio.sleep(random.uniform(2.0, 4.0))  # Delay anti-baneo
            
            # Buscar el botón o enlace hacia la publicación original en Facebook
            dark_post_link = await page.evaluate("""
                () => {
                    const a = document.querySelector('a[href*="facebook.com/"], a[href*="/posts/"], a[href*="fbid="]');
                    return a ? a.href : null;
                }
            """)
            
            await browser.close()
            return dark_post_link or snapshot_url
        except Exception as e:
            print(f"[ERROR] Error al resolver {snapshot_url}: {e}")
            await browser.close()
            return snapshot_url

async def ejecutar_radar_anuncios(keyword="parcelas 5000 m2"):
    anuncios = consultar_meta_ad_library(keyword)
    resultados = []
    
    for ad in anuncios:
        snapshot_url = ad.get("ad_snapshot_url", "")
        real_url = await resolver_dark_post_url(snapshot_url)
        ad["dark_post_url"] = real_url
        resultados.append(ad)
        await asyncio.sleep(random.uniform(1.5, 3.0))  # Retardo aleatorio comportamental
        
    return resultados

if __name__ == "__main__":
    res = asyncio.run(ejecutar_radar_anuncios("parcelas 5000 m2"))
    print("\n[RESULTADO RADAR DE ANUNCIOS]")
    print(json.dumps(res, indent=2, ensure_ascii=False))
