import os
import sys
import json
import csv
import base64
import requests
from datetime import datetime
from pathlib import Path

# Configuración de Rutas
ROOT_DIR = r"c:\Users\LyCoNs\Desktop\AGENTES IA"
CSV_PATH = os.path.join(ROOT_DIR, "VENDEDORES_MACROLOTES_MASTERPLAN_360.csv")
MASTER_CSV_PATH = os.path.join(ROOT_DIR, "MASTER_LEADS_CALIFICADOS_AUSTRALDRONE.csv")
OUTPUT_DIR = os.path.join(ROOT_DIR, "REPORTES_AGENTES", "CAZADOR360")

# Meta API Token oficial del usuario
def get_tg_token():
    enc = "ODk3NzE5NjA0NzpBQUZweFFSU19fZzRwRzBIZXROazIydmdPanF1ZDVLaTlFQQ=="
    return base64.b64decode(enc).decode('utf-8')

TELEGRAM_BOT_TOKEN = get_tg_token()
TELEGRAM_CHAT_ID = "1024898120"

def sp(msg):
    try:
        print(str(msg).encode('ascii', 'ignore').decode('ascii'), flush=True)
    except Exception:
        pass

def buscar_anuncios_meta(query="parcelas"):
    sp(f"[META API] Consultando Biblioteca de Anuncios de Meta para: '{query}'...")
    url = "https://graph.facebook.com/v19.0/ads_archive"
    params = {
        "access_token": META_TOKEN,
        "search_terms": query,
        "ad_type": "ALL",
        "ad_reached_countries": '["CL"]',
        "limit": 10,
        "fields": "id,page_id,page_name,ad_creative_bodies,ad_snapshot_url"
    }
    try:
        r = requests.get(url, params=params)
        if r.status_code == 200:
            data = r.json().get('data', [])
            sp(f"[META API] Se encontraron {len(data)} anuncios activos.")
            return data
        else:
            sp(f"[-] Error en Meta API ({r.status_code}): {r.text}")
            return []
    except Exception as e:
        sp(f"[-] Error de conexión Meta API: {e}")
        return []

def procesar_y_calificar(ads):
    leads_calificados = []
    for idx, ad in enumerate(ads, 1):
        cuerpo = (ad.get('ad_creative_bodies') or [""])[0]
        page_name = ad.get('page_name', 'Inmobiliaria / Anunciante')
        page_id = ad.get('page_id', '')
        ad_id = ad.get('id', '')
        snapshot_url = ad.get('ad_snapshot_url', '')

        if not cuerpo:
            continue

        # Lógica de Scoring B2B
        score = 60  # Base para anuncios de pago activos
        ubicacion = "Chile"
        if "osorno" in cuerpo.lower() or "puerto varas" in cuerpo.lower() or "llanquihue" in cuerpo.lower() or "los lagos" in cuerpo.lower():
            score += 20
            ubicacion = "Región de Los Lagos"
        
        # Extraer teléfono si está en el cuerpo
        telefono = "Ver Anuncio"
        import re
        telefonos_encontrados = re.findall(r'\+?56\s?9\s?\d{4}\s?\d{4}|\b9\d{8}\b', cuerpo)
        if telefonos_encontrados:
            telefono = telefonos_encontrados[0]
            score += 20

        # Si califica
        if score >= 50:
            lead = {
                "rank": idx,
                "score": score,
                "nombre": page_name,
                "telefono": telefono,
                "ubicacion": ubicacion,
                "superficie": "Macrolote (Anuncio)",
                "precio": "A consultar",
                "deal_size_estimado": "Alto (>$5M CLP)",
                "nivel_urgencia": "ALTA",
                "motivo_top": f"Inmobiliaria activa pautando anuncios en {ubicacion}.",
                "accion_recomendada": "Contactar página anunciante para ofrecer videos aéreos 4K y MasterPlan.",
                "link_perfil": f"https://www.facebook.com/page/{page_id}" if page_id else snapshot_url,
                "link_post": snapshot_url
            }
            leads_calificados.append(lead)
    
    return leads_calificados

def guardar_y_notificar(leads):
    if not leads:
        sp("[META API] No hay leads con puntuación calificada (>=60) en este ciclo.")
        return

    # Guardar en CSV Maestro
    file_exists = os.path.exists(MASTER_CSV_PATH)
    try:
        with open(MASTER_CSV_PATH, 'a', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow([
                    "Fecha Procesamiento", "Rank", "Score B2B", "Nombre Vendedor", "Telefono Contacto", 
                    "Ubicacion", "Superficie Has", "Precio CLP UF", "Deal Size Estimado", 
                    "Nivel Urgencia", "Diagnostico IA", "Accion Recomendada", 
                    "Link Perfil Facebook", "Link Publicacion Grupo"
                ])
            for lead in leads:
                writer.writerow([
                    datetime.now().strftime("%Y-%m-%d %H:%M"),
                    lead.get("rank"),
                    lead.get("score"),
                    lead.get("nombre"),
                    lead.get("telefono"),
                    lead.get("ubicacion"),
                    lead.get("superficie"),
                    lead.get("precio"),
                    lead.get("deal_size_estimado"),
                    lead.get("nivel_urgencia"),
                    lead.get("motivo_top"),
                    lead.get("accion_recomendada"),
                    lead.get("link_perfil"),
                    lead.get("link_post")
                ])
        sp(f"[+] CSV Maestro actualizado con {len(leads)} leads de Meta API.")
    except Exception as e:
        sp(f"[-] Error guardando en CSV Maestro: {e}")

    # Notificar a Telegram
    for lead in leads:
        tg_msg = (
            f"🚨 <b>NUEVO ANUNCIO CALIFICADO (META API)</b>\n\n"
            f"🏢 <b>{lead['nombre']}</b>\n"
            f"📞 <code>{lead['telefono']}</code>\n"
            f"📍 {lead['ubicacion']}\n"
            f"🌾 {lead['superficie']}\n\n"
            f"🎯 <b>Score B2B: {lead['score']}/100</b>\n"
            f"⚡ Urgencia: {lead['nivel_urgencia']}\n\n"
            f"💡 <b>Diagnóstico:</b> {lead['motivo_top']}\n"
            f"✅ <b>Recomendación B2B:</b> {lead['accion_recomendada']}\n\n"
            f"🔗 <a href='{lead['link_post']}'>Ver Anuncio en Facebook</a>"
        )
        tg_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        try:
            requests.post(tg_url, json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": tg_msg,
                "parse_mode": "HTML",
                "disable_web_page_preview": True
            })
            sp(f"[+] Alerta enviada a Telegram para: {lead['nombre']}")
        except Exception as e:
            sp(f"[-] Error enviando Telegram: {e}")

    # Mandar a la Oficina Virtual (WebSockets de Render / Local)
    try:
        requests.post("http://localhost:8080/api/lead-result", json={
            "agente": "CAZADOR360",
            "top_leads": leads,
            "total_analizados": len(leads),
            "total_calificados": len(leads)
        }, timeout=5)
    except Exception:
        pass

    try:
        requests.post("https://australhq.onrender.com/api/lead-result", json={
            "agente": "CAZADOR360",
            "top_leads": leads,
            "total_analizados": len(leads),
            "total_calificados": len(leads)
        }, timeout=5)
    except Exception:
        pass

def main():
    queries = ["parcelas Chile", "venta parcelas sur", "terrenos sur chile", "loteos Frutillar"]
    min_score = 60
    
    # Obtener configuración dinámica desde el servidor HQ
    try:
        r = requests.get("http://localhost:8080/api/agent-config?agent=cazador360", timeout=2)
        if r.status_code == 200 and r.json().get('success'):
            cfg = r.json().get('config', {})
            if cfg.get('query_terms'):
                queries = [q.strip() for q in cfg['query_terms'].split(',') if q.strip()]
            if cfg.get('min_score_threshold'):
                min_score = int(cfg['min_score_threshold'])
            sp(f"[META API] Configuración dinámica cargada desde HQ: Queries={queries} | Score Mínimo={min_score}")
    except Exception as e:
        sp(f"[META API] Usando parámetros por defecto. ({e})")

    all_leads = []
    for q in queries:
        ads = buscar_anuncios_meta(q)
        leads = procesar_y_calificar(ads)
        filtered = [l for l in leads if (l.get('score') or 0) >= min_score]
        all_leads.extend(filtered)
    
    guardar_y_notificar(all_leads)
    sp("[META API] Escaneo finalizado correctamente.")

if __name__ == "__main__":
    main()
