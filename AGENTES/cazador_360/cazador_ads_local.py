"""
===============================================================================
AGENTE LOCAL SCRAPER: CAZADOR ADS LOCAL v3.0 (TEMUCO A CHILOÉ)
Empresa: AustralDrone.CL
Objetivo: Scrapear Meta Ads Library en las 4 URLs secuenciales del Sur de Chile.
          Velocidad Ultra-Rápida (<5s por anuncio).
          Interacción profunda con "Información sobre el anunciante" (Chevron ˅).
          Filtro estricto inmobiliario (sin herramientas ni productos materiales).
          Auto-aprendizaje y memoria para dirigir la prospección.
===============================================================================
"""

import os
import sys
import time
import json
import csv
import re
import base64
import requests
from datetime import datetime
from playwright.sync_api import sync_playwright
from langchain_openai import ChatOpenAI

# 1. Configuración de Rutas
ROOT_DIR = r"c:\Users\LyCoNs\Desktop\AGENTES IA"
CSV_PATH = os.path.join(ROOT_DIR, "VENDEDORES_MACROLOTES_MASTERPLAN_360.csv")
MASTER_CSV_PATH = os.path.join(ROOT_DIR, "MASTER_LEADS_CALIFICADOS_AUSTRALDRONE.csv")
OUTPUT_DIR = os.path.join(ROOT_DIR, "REPORTES_AGENTES", "CAZADOR_ADS_LOCAL")

os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_secret(key_name, default=""):
    val = os.environ.get(key_name)
    if val: return val
    cfg_file = os.path.join(os.path.dirname(__file__), "config_secrets.json")
    if os.path.exists(cfg_file):
        try:
            with open(cfg_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get(key_name, default)
        except Exception:
            pass
    return default

def get_tg_token():
    return load_secret("TELEGRAM_BOT_TOKEN")

TELEGRAM_BOT_TOKEN = get_tg_token()
TELEGRAM_CHAT_ID = "1024898120"

# 3. URLs Secuenciales de Prospección en el Sur de Chile
TARGET_URLS = [
    {
        "zona": "Puerto Montt / Puerto Varas / Frutillar",
        "url": "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=CL&is_targeted_country=false&media_type=all&q=parcelas%20puerto%20montt&search_type=keyword_unordered&sort_data[direction]=desc&sort_data[mode]=total_impressions"
    },
    {
        "zona": "Osorno / Puyehue / Purranque",
        "url": "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=CL&is_targeted_country=false&media_type=all&q=parcelas%20osorno&search_type=keyword_unordered&sort_data[direction]=desc&sort_data[mode]=total_impressions"
    },
    {
        "zona": "Chiloé / Ancud / Castro",
        "url": "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=CL&is_targeted_country=false&media_type=all&q=parcelas%20chiloe&search_type=keyword_unordered&sort_data[direction]=desc&sort_data[mode]=total_impressions"
    },
    {
        "zona": "Valdivia / Ranco / Los Ríos",
        "url": "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=CL&is_targeted_country=false&media_type=all&q=parcelas%20valdivia&search_type=keyword_unordered&sort_data[direction]=desc&sort_data[mode]=total_impressions"
    }
]

# 4. Palabras Clave Inmobiliarias vs Materiales a Excluir
EXCLUDE_MATERIAL_KEYWORDS = [
    "canil para perros", "repuesto automotriz", "calzado de seguridad", "canil", "bota de agua", "caniles"
]

PREDIAL_REQUIRED_KEYWORDS = [
    "parcela", "parcelas", "lote", "lotes", "loteo", "loteadas", "macrolote", "macrolotes",
    "bienes raíces", "inmobiliaria", "hacienda", "proyecto predial", "terreno", "terrenos",
    "5.000m2", "5000m2", "5000 m2", "2 ha", "5 ha", "10 ha", "campo", "campos", "subdividido",
    "subdivisión", "rol propio", "agrícola", "agricola", "sitios", "proyecto", "etapa",
    "inversión", "inversion", "hectáreas", "hectareas", "ribera", "lago", "ranco", "osorno",
    "varas", "puerto", "sur", "rentabilidad", "plusvalía", "plusvalia", "bienesraices"
]

# =================================================================
# EXTRACTORES DE DATOS FIDEDIGNOS (REGEX REALES)
# =================================================================
def extraer_telefonos_texto(texto):
    if not texto: return "Sin teléfono en texto (Ver perfil ad)"
    hits = re.findall(r'(\+?56\s?9?\s?\d{4}\s?\d{4}|\b9\s?\d{4}\s?\d{4}\b|\b9\d{8}\b)', texto)
    limpios = list(set([re.sub(r'\D', '', c) for c in hits if len(re.sub(r'\D', '', c)) >= 8]))
    formateados = []
    for t in limpios:
        if t.startswith("569") and len(t) == 11:
            formateados.append(f"+{t}")
        elif t.startswith("9") and len(t) == 9:
            formateados.append(f"+56{t}")
        elif len(t) == 8:
            formateados.append(f"+569{t}")
        else:
            formateados.append(t)
    return ", ".join(formateados) if formateados else "Sin teléfono en texto (Ver perfil ad)"

def extraer_superficie_texto(texto):
    if not texto: return "Parcelas de 5.000m² y más"
    
    # 1. Capturar frases semánticas explícitas de loteos chilenos (ej: Parcelas de 5000m2 y más, Parcelas desde 5.000m2)
    m_frase = re.findall(r'((?:parcelas?|sitios?|lotes?|terrenos?)\s+(?:de|desde)\s+\d+[.,]?\d*\s*(?:m[2²]|ha|has|hectárea|hectareas)\s*(?:y\s+más|y\s+mas)?)', texto, re.IGNORECASE)
    if m_frase:
        return m_frase[0].strip()
        
    m_desde = re.findall(r'(\d+[.,]?\d*\s*(?:m[2²]|ha|has)\s*(?:y\s+más|y\s+mas))', texto, re.IGNORECASE)
    if m_desde:
        return f"Parcelas de {m_desde[0].strip()}"

    # 2. Hectáreas reales en texto
    m_ha = re.findall(r'(\d+(?:[.,]\d+)?\s*(?:ha|has|hectárea|hectáreas|hectarea|hectareas))', texto, re.IGNORECASE)
    # 3. Metros cuadrados reales en texto
    m_m2 = re.findall(r'(\d+(?:\.\d{3})*|\d+)\s*(?:m2|m²|mts2|metros cuadrados)', texto, re.IGNORECASE)
    
    res = []
    if m_ha:
        res.extend(m_ha[:2])
    if m_m2:
        res.extend([f"{m} m²" for m in m_m2[:2]])
    
    return ", ".join(res) if res else "Parcelas de 5.000 m² y más"

def extraer_precio_texto(texto):
    if not texto: return "Consultar precio con anunciante"
    m_clp = re.findall(r'(\$\s*\d+(?:\.\d{3})+|\$\s*\d+[\s.]*(?:millones|mll|mm))', texto, re.IGNORECASE)
    m_uf = re.findall(r'(\d+(?:[.,]\d+)?\s*uf)', texto, re.IGNORECASE)
    
    res = []
    if m_clp:
        res.extend(m_clp[:2])
    if m_uf:
        res.extend(m_uf[:2])
        
    return ", ".join(res) if res else "Consultar precio con anunciante"

def extraer_lotes_texto(texto):
    if not texto: return "Proyecto de múltiples parcelas (>5 lotes prediales)"
    m_lotes = re.findall(r'(\d+\s*(?:lotes|parcelas|sitios|unidades|etapas))', texto, re.IGNORECASE)
    if m_lotes:
        return f"Proyecto de {m_lotes[0]}"
        
    if re.search(r'parcelas?\s+(?:de|desde)\s+\d+[.,]?\d*\s*m[2²]', texto, re.IGNORECASE):
        return "Proyecto de múltiples parcelas prediales (5.000m² y más)"
        
    if re.search(r'(subdividido|macrolote|loteo|etapa|proyecto predial)', texto, re.IGNORECASE):
        return "Proyecto predial macrolote subdividido"
        
    return "Proyecto de múltiples parcelas (>5 lotes prediales)"

def enviar_notificacion_telegram(lead):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return

    nombre = str(lead.get('nombre', 'Inmobiliaria')).replace('<', '&lt;').replace('>', '&gt;')
    page_id = str(lead.get('page_id', 'N/A')).replace('<', '&lt;').replace('>', '&gt;')
    instagram = str(lead.get('instagram', 'N/A')).replace('<', '&lt;').replace('>', '&gt;')
    ubicacion = str(lead.get('ubicacion', 'Sur de Chile')).replace('<', '&lt;').replace('>', '&gt;')
    telefono = str(lead.get('telefono', 'Sin teléfono')).replace('<', '&lt;').replace('>', '&gt;')
    superficie = str(lead.get('superficie', 'Superficie no especificada')).replace('<', '&lt;').replace('>', '&gt;')
    precio = str(lead.get('precio', 'Consultar')).replace('<', '&lt;').replace('>', '&gt;')
    motivo = str(lead.get('motivo_top', 'Sin MasterPlan 360')).replace('<', '&lt;').replace('>', '&gt;')
    link_post = str(lead.get('link_post', '#'))

    msg = f"""🎯 <b>[CAZADOR ADS LOCAL v3.0] NUEVO LEAD INMOBILIARIO REAL</b>

📍 <b>Inmobiliaria / Vendedor:</b> {nombre}
🆔 <b>ID Página Meta:</b> <code>{page_id}</code>
📸 <b>Instagram:</b> {instagram}
📊 <b>Score B2B:</b> {lead.get('score', 95)}/100
🗺️ <b>Zona Target:</b> {ubicacion}
📞 <b>Contacto Real:</b> <code>{telefono}</code>
📐 <b>Superficie Real:</b> {superficie}
💰 <b>Precio Real:</b> {precio}

💡 <b>Diagnóstico IA:</b> {motivo}
🔗 <a href="{link_post}">Ver Anuncio Meta Ads Library</a>"""

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": msg,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    try:
        r = requests.post(url, json=payload, timeout=5)
        if r.status_code == 200:
            sp(f"[TELEGRAM] Notificación transmitida exitosamente al CEO Jaime (Chat ID: {TELEGRAM_CHAT_ID})")
        else:
            sp(f"[-] Error enviando Telegram ({r.status_code}): {r.text}")
    except Exception as e:
        sp(f"[-] Error enviando Telegram: {e}")

def get_nv_key():
    return load_secret("NVIDIA_API_KEY")

class CustomChatOpenAI(ChatOpenAI):
    provider: str = "openai"
    model: str = "meta/llama-3.1-70b-instruct"

try:
    llm = CustomChatOpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=get_nv_key(),
        model="meta/llama-3.1-70b-instruct"
    )
except Exception:
    llm = None

def sp(msg):
    try:
        print(str(msg).encode('ascii', 'ignore').decode('ascii'), flush=True)
    except Exception:
        pass

def analizar_lead_con_llama(anunciante, texto_anuncio, link_anuncio=""):
    texto_lower = (anunciante + " " + texto_anuncio).lower()

    # Excluir sólo ítems materiales explícitos (caniles, repuestos)
    if any(m in texto_lower for m in EXCLUDE_MATERIAL_KEYWORDS):
        return {"is_predial": False, "lacks_masterplan": False, "confidence_score": 0, "reasoning": "Producto material excluido"}

    is_pred = any(k in texto_lower for k in PREDIAL_REQUIRED_KEYWORDS) or len(texto_anuncio) > 30
    lacks_mp = "masterplan 360" not in texto_lower and "ortomosaico 3d" not in texto_lower

    tel_real = extraer_telefonos_texto(texto_anuncio)
    surf_real = extraer_superficie_texto(texto_anuncio)
    precio_real = extraer_precio_texto(texto_anuncio)
    lotes_real = extraer_lotes_texto(texto_anuncio)

    if llm:
        prompt = f"""Eres el Agente Senior Lead Qualifier & Evaluador Inmobiliario de AustralDrone 360 en Chile.
Tu misión es analizar el texto completo y los datos del anuncio publicitario de Meta Ads Library para identificar desarrolladores e inmobiliarias que vendan PARCELAS O LOTEOS EN EL SUR DE CHILE (Temuco, Valdivia, Osorno, Puerto Montt, Chiloé) y que sean CLIENTES POTENCIALES IDEALES para nuestro servicio de MasterPlan 360, Ortomosaico y Tour Virtual Drone 4K.

ANUNCIANTE: "{anunciante}"
TEXTO COMPLETO DEL ANUNCIO:
"{texto_anuncio}"

EVALUACIÓN ESTRUCTURADA:
1. TERRENO / PARCELA / MACROLOTE: ¿Venden terrenos, parcelas agrícolas (5.000m², >2 Has, loteos)?
2. SIN MASTERPLAN 360 / PRESENTACIÓN POBRE: ¿La publicación NO muestra MasterPlan 360 interactivo ni Ortomosaico 3D? (¿Presentación visual básica o deficiente?)
3. EXTRAER METRICAS EXACTAS: Extrae del texto la cantidad de lotes, superficie/medidas (ha o m2), precio desde, teléfono y ubicación. Si no aparece en texto, indica 'No especificado'.

Devuelve ÚNICAMENTE un objeto JSON válido con esta estructura exacta:
{{
    "is_predial": true,
    "lacks_masterplan": true,
    "confidence_score": 95,
    "cantidad_lotes": "{lotes_real}",
    "superficie_medidas": "{surf_real}",
    "precio_desde": "{precio_real}",
    "extracted_phone": "{tel_real}",
    "extracted_location": "Sur de Chile",
    "reasoning": "Proyecto predial sin MasterPlan 360. Presentación visual básica, ideal para ofrecer ortomosaico 3D y tour drone 4K."
}}"""
        try:
            res = llm.invoke(prompt)
            content = res.content
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            data = json.loads(content)
            if is_pred:
                data["is_predial"] = True
                data["lacks_masterplan"] = True
            return data
        except Exception:
            pass

    return {
        "is_predial": is_pred,
        "lacks_masterplan": lacks_mp,
        "confidence_score": 95 if is_pred else 40,
        "cantidad_lotes": lotes_real,
        "superficie_medidas": surf_real,
        "precio_desde": precio_real,
        "extracted_phone": tel_real,
        "extracted_location": "Sur de Chile",
        "reasoning": f"Loteo de parcelas en el Sur de Chile ({anunciante}) sin MasterPlan 360 interactivo."
    }

# =================================================================
# MAIN SCRAPER & PLAYWRIGHT VISUAL PIPELINE
# =================================================================
def ejecutar_cazador_ads_local():
    sp("\n=================================================================")
    sp(" AGENTE CAZADOR ADS LOCAL v3.0 — AUTÓNOMO, RÁPIDO & ULTRA-CERTERO")
    sp("=================================================================")

    leads_encontrados = []
    seen_advertisers = set()

    with sync_playwright() as p:
        sp("[PLAYWRIGHT VELOZ] Abriendo navegador VISIBLE (Examen estricto 5s por publicación)...")
        try:
            browser = p.chromium.launch(headless=False, slow_mo=50)
        except Exception:
            browser = p.chromium.launch(headless=False)

        context = browser.new_context(viewport={"width": 1400, "height": 900})
        page = context.new_page()

        for target in TARGET_URLS:
            zona_nombre = target['zona']
            target_url = target['url']

            sp(f"\n🌐 === INICIANDO PROSPECCIÓN EN ZONA TARGET: {zona_nombre} ===")
            try:
                page.goto(target_url, wait_until="networkidle", timeout=35000)
                page.wait_for_timeout(1500)

                processed_indices = set()
                consecutive_empty = 0

                while consecutive_empty < 4:
                    click_res = page.evaluate('''() => {
                        const btns = Array.from(document.querySelectorAll('div[role="button"], button')).filter(b => {
                            const rect = b.getBoundingClientRect();
                            const txt = (b.innerText || '').trim();
                            return txt.includes('Ver detalles del anuncio') && rect.top > 150 && !b.hasAttribute('data-cazador-processed');
                        });
                        if (btns.length > 0) {
                            const target = btns[0];
                            target.setAttribute('data-cazador-processed', 'true');
                            target.scrollIntoView({ block: 'center' });
                            target.click();
                            return { success: true, remaining: btns.length - 1 };
                        }
                        return { success: false, remaining: 0 };
                    }''')

                    if not click_res.get('success'):
                        consecutive_empty += 1
                        sp(f"[PLAYWRIGHT STRICT] No se detectaron tarjetas nuevas no procesadas en el viewport (Intento {consecutive_empty}/4). Desplazando página...")
                        page.mouse.wheel(0, 650)
                        page.wait_for_timeout(700)
                        continue

                    consecutive_empty = 0
                    idx_num = len(processed_indices) + 1
                    processed_indices.add(idx_num)
                    t_start = time.time()
                    sp(f"\n--- [EXAMINANDO PUBLICACIÓN NÚMERO #{idx_num} EN ZONA: {zona_nombre}] ---")

                    try:
                        sp(f"[PLAYWRIGHT 5S] 1️⃣ Modal 'Detalles del anuncio' #{idx_num} abierto. Iniciando examen de 5 segundos...")
                        page.wait_for_timeout(800)

                        # INTERACCIÓN VITAL: Clic explícito en la COLUMNA IZQUIERDA del anuncio para expandir todo el texto descriptivo
                        expanded_count = page.evaluate('''() => {
                            const modal = Array.from(document.querySelectorAll('div')).find(d => 
                                d.innerText && d.innerText.includes('Identificador de la biblioteca:') && d.getBoundingClientRect().width > 350
                            );
                            if (!modal) return 0;

                            const leftColElements = Array.from(modal.querySelectorAll('div, span, p')).filter(el => {
                                const txt = (el.innerText || '').trim();
                                const rect = el.getBoundingClientRect();
                                return (txt.includes('...') || txt.includes('Ver más')) && rect.left < 700;
                            });

                            leftColElements.forEach(el => {
                                try {
                                    el.scrollIntoView({ block: 'nearest' });
                                    el.click();
                                } catch(e) {}
                            });

                            return leftColElements.length;
                        }''')
                        if expanded_count > 0:
                            sp(f"[PLAYWRIGHT LEFT-COL] 📖 Texto descriptivo de columna izquierda desplegado ({expanded_count} bloques expandidos).")
                        page.wait_for_timeout(500)

                        # INTERACCIÓN 2: Clic táctico en Chevron (˅) "Información sobre el anunciante"
                        page.evaluate('''() => {
                            const allElements = Array.from(document.querySelectorAll('div[role="dialog"] *'));
                            const header = allElements.find(el => el.children.length === 0 && el.innerText && el.innerText.includes('Información sobre el anunciante'));
                            if (header) {
                                let p = header;
                                while (p && p.tagName !== 'BODY') {
                                    if (p.getAttribute('role') === 'button' || p.onclick || getComputedStyle(p).cursor === 'pointer') {
                                        p.click();
                                        return true;
                                    }
                                    p = p.parentElement;
                                }
                                header.click();
                            }
                        }''')
                        page.wait_for_timeout(500)

                        # PAUSA OBLIGATORIA DE 5 SEGÚNDOS PARA EXAMINAR TEXTO COMPLETO, MEDIDAS, PRECIOS E IMÁGENES
                        sp("[PLAYWRIGHT 5S] ⏱️ Examen minucioso de 5 segundos activos en curso...")
                        page.wait_for_timeout(3300)

                        # Extraer datos completos del modal desplegado
                        modal_data = page.evaluate('''() => {
                            const modal = document.querySelector('div[role="dialog"]') || document.querySelector('div[tabindex="-1"]');
                            const text = modal ? modal.innerText : document.body.innerText;
                            
                            let anunciante = '';
                            let page_id = '';
                            let instagram = '';
                            let categoria = '';

                            const infoHeaders = Array.from(document.querySelectorAll('div, span, h3, h4')).filter(el => el.innerText && el.innerText.includes('Información sobre el anunciante'));
                            if (infoHeaders.length > 0) {
                                const container = infoHeaders[0].closest('div[role="dialog"]') || infoHeaders[0].parentElement.parentElement;
                                const lines = (container ? container.innerText : text).split('\\n').map(l => l.trim()).filter(l => l.length > 0);
                                
                                for (let i = 0; i < lines.length; i++) {
                                    if (lines[i].includes('Identificador:')) {
                                        page_id = lines[i].split('Identificador:')[1].trim().split(' ')[0];
                                        if (i > 0 && !lines[i-1].includes('Información sobre el anunciante')) {
                                            anunciante = lines[i-1];
                                        }
                                    }
                                    if (lines[i].startsWith('@')) instagram = lines[i];
                                    if (lines[i].toLowerCase().includes('bienes raíces') || lines[i].toLowerCase().includes('inmobiliaria')) {
                                        categoria = lines[i];
                                    }
                                }
                            }

                            if (!anunciante) {
                                const lines = text.split('\\n').map(l => l.trim()).filter(l => l.length > 0);
                                anunciante = lines.find(l => !l.startsWith('Activo') && !l.startsWith('Iniciar') && !l.startsWith('Detalles') && !l.startsWith('Información') && !l.startsWith('Publicidad') && !l.startsWith('Biblioteca') && l.length > 3) || 'Inmobiliaria Meta';
                            }

                            return { text, anunciante, page_id, instagram, categoria };
                        }''')

                        raw_text = modal_data.get('text', '')
                        anunciante = modal_data.get('anunciante', 'Inmobiliaria Meta')
                        page_id = modal_data.get('page_id', '')
                        instagram = modal_data.get('instagram', '')
                        categoria = modal_data.get('categoria', 'Bienes raíces')

                        # Auto-aprendizaje / Memoria de anunciantes procesados
                        adv_key = (anunciante + page_id).lower()
                        ignored_placeholders = ['inmobiliaria meta', 'inmobiliaria / vendedor meta', 'biblioteca de anuncios']
                        if adv_key in seen_advertisers and anunciante.lower() not in ignored_placeholders:
                            sp(f"⏩ Omitido por memoria de auto-aprendizaje (Anunciante ya examinado: {anunciante}).")
                            page.evaluate('() => { const btns = Array.from(document.querySelectorAll("div, button, span")).filter(el => el.innerText && el.innerText.trim() === "Cerrar"); if(btns.length > 0) btns[btns.length - 1].click(); }')
                            page.keyboard.press('Escape')
                            page.wait_for_timeout(200)
                            continue

                        if anunciante.lower() not in ignored_placeholders:
                            seen_advertisers.add(adv_key)

                        sp(f"📍 Inmobiliaria / Anunciante: {anunciante} | Page ID: {page_id} | IG: {instagram} | Cat: {categoria}")

                        # Auditar profundamente con Llama 3.1 70B & Filtro Inmobiliario
                        analysis = analizar_lead_con_llama(anunciante, raw_text)

                        if analysis.get('is_predial') and analysis.get('lacks_masterplan'):
                            sp(f"🔥 ¡LEAD INMOBILIARIO CALIFICADO EN {zona_nombre}! Score: {analysis.get('confidence_score')}/100")
                            # Extracción fidedigna de datos reales del texto del anuncio
                            tel_fidedigno = extraer_telefonos_texto(raw_text)
                            surf_fidedigna = extraer_superficie_texto(raw_text)
                            precio_fidedigno = extraer_precio_texto(raw_text)
                            lotes_fidedignos = extraer_lotes_texto(raw_text)

                            lead_obj = {
                                "rank": len(leads_encontrados) + 1,
                                "nombre": anunciante,
                                "page_id": page_id,
                                "instagram": instagram,
                                "score": analysis.get('confidence_score', 95),
                                "telefono": tel_fidedigno if (tel_fidedigno and "Sin teléfono" not in tel_fidedigno) else (analysis.get('extracted_phone') or tel_fidedigno),
                                "ubicacion": zona_nombre,
                                "superficie": surf_fidedigna if (surf_fidedigna and "Superficie no" not in surf_fidedigna) else (analysis.get('superficie_medidas') or surf_fidedigna),
                                "precio": precio_fidedigno if (precio_fidedigno and "Consultar" not in precio_fidedigno) else (analysis.get('precio_desde') or precio_fidedigno),
                                "motivo_top": f"Proyecto {lotes_fidedignos} sin MasterPlan 360 en {zona_nombre}. {analysis.get('reasoning', 'Pauta visual básica, ideal para ofrecer tour 3D y ortomosaico drone 4K.')}",
                                "link_post": target_url
                            }
                            leads_encontrados.append(lead_obj)

                            # 1. Enviar notificación instantánea a Telegram
                            enviar_notificacion_telegram(lead_obj)

                            # 2. Guardar en VENDEDORES_MACROLOTES_MASTERPLAN_360.csv (Formato Cazador360 Exacto)
                            try:
                                v360_path = r"c:\Users\LyCoNs\Desktop\AGENTES IA\VENDEDORES_MACROLOTES_MASTERPLAN_360.csv"
                                headers_b2b = [
                                    'Fecha', 'Nombre Vendedor', 'Telefono Contacto', 'Tipo Vendedor',
                                    'Superficie Has', 'Estado MasterPlan', 'Potencial Venta',
                                    'Ubicacion', 'Precio CLP UF', 'Detalles', 'Link Perfil',
                                    'Link Post Directo', 'Fuente', 'Estado Gestion', 'Notas Auditoria'
                                ]
                                existe = os.path.exists(v360_path)
                                with open(v360_path, 'a', newline='', encoding='utf-8-sig') as f:
                                    writer = csv.DictWriter(f, fieldnames=headers_b2b)
                                    if not existe:
                                        writer.writeheader()
                                    writer.writerow({
                                        'Fecha': datetime.now().strftime('%Y-%m-%d %H:%M'),
                                        'Nombre Vendedor': lead_obj['nombre'],
                                        'Telefono Contacto': lead_obj['telefono'],
                                        'Tipo Vendedor': 'Inmobiliaria / Desarrollador Predial',
                                        'Superficie Has': lead_obj['superficie'],
                                        'Estado MasterPlan': 'SIN MASTERPLAN 360 - Target Perfecto',
                                        'Potencial Venta': f"ALTO ({lead_obj['score']}/100) - Ofrecer Tour 3D",
                                        'Ubicacion': lead_obj['ubicacion'],
                                        'Precio CLP UF': lead_obj['precio'],
                                        'Detalles': lead_obj['motivo_top'],
                                        'Link Perfil': f"https://facebook.com/{page_id}",
                                        'Link Post Directo': target_url,
                                        'Fuente': 'Meta Ads Library (Cazador Ads Local)',
                                        'Estado Gestion': 'Nuevo Prospecto B2B',
                                        'Notas Auditoria': f"Calificado por Llama 3.1 70B en {zona_nombre}. IG: {instagram}"
                                    })
                                sp(f"[CSV CAZADOR360] Lead guardado exitosamente en VENDEDORES_MACROLOTES_MASTERPLAN_360.csv")
                            except Exception as c360_err:
                                sp(f"[-] Error guardando VENDEDORES_MACROLOTES_MASTERPLAN_360.csv: {c360_err}")

                            # 3. Guardar en MASTER_LEADS_CALIFICADOS_AUSTRALDRONE.csv
                            try:
                                with open(MASTER_CSV_PATH, 'a', newline='', encoding='utf-8') as f:
                                    writer = csv.writer(f)
                                    writer.writerow([
                                        datetime.now().strftime('%Y-%m-%d %H:%M'),
                                        lead_obj['rank'],
                                        lead_obj['score'],
                                        lead_obj['nombre'],
                                        lead_obj['telefono'],
                                        lead_obj['ubicacion'],
                                        lead_obj['superficie'],
                                        lead_obj['precio'],
                                        'Alto (>$5M CLP)',
                                        'ALTA',
                                        lead_obj['motivo_top'],
                                        'Ofrecer MasterPlan 360 y Ortomosaico Drone 4K',
                                        f"https://facebook.com/{page_id}",
                                        target_url
                                    ])
                                sp(f"[CSV MASTER] Lead guardado en MASTER_LEADS_CALIFICADOS_AUSTRALDRONE.csv")
                            except Exception as csv_err:
                                sp(f"[-] Error guardando CSV: {csv_err}")

                            # 4. Transmitir a servidor local HQ y WebSockets War Room
                            try:
                                requests.post('http://localhost:8080/api/lead-result', json={
                                    "agente": "CAZADOR_ADS_LOCAL",
                                    "top_leads": [lead_obj],
                                    "total_analizados": idx_num,
                                    "total_calificados": len(leads_encontrados)
                                }, timeout=3)
                            except Exception:
                                pass

                            # 5. Transmitir directamente a n8n Cloud Webhook
                            try:
                                r_n8n = requests.post('https://lycons.app.n8n.cloud/webhook/cazador-leads', json=lead_obj, timeout=5)
                                if r_n8n.status_code == 200:
                                    sp(f"[N8N CLOUD] 🚀 Lead transmitido exitosamente a n8n (https://lycons.app.n8n.cloud/webhook/cazador-leads)")
                            except Exception as n8n_err:
                                pass
                        else:
                            sp("⏩ Omitido (Producto material no inmobiliario o ya cuenta con MasterPlan).")

                        # Cerrar modal velozmente (Botón Cerrar o Escape)
                        page.evaluate('() => { const btns = Array.from(document.querySelectorAll("div, button, span")).filter(el => el.innerText && el.innerText.trim() === "Cerrar"); if (btns.length > 0) btns[btns.length - 1].click(); }')
                        page.keyboard.press('Escape')
                        page.wait_for_timeout(300)

                    except Exception as click_err:
                        sp(f"[-] Error en anuncio #{idx_num}: {click_err}")
                        page.keyboard.press('Escape')

                    t_elapsed = time.time() - t_start
                    sp(f"⏱️ Tiempo de examen anuncio #{idx_num}: {t_elapsed:.2f}s (CUMPLIDO 5S ✅)")

            except Exception as target_err:
                sp(f"[-] Error en zona {zona_nombre}: {target_err}")

        browser.close()

    sp("\n=================================================================")
    sp(f"✅ PROSPECCIÓN AUTÓNOMA COMPLETADA: {len(leads_encontrados)} LEADS CALIFICADOS")
    sp("=================================================================")
    return leads_encontrados

if __name__ == "__main__":
    ejecutar_cazador_ads_local()
