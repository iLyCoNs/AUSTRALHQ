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

def load_secret(key_name, default_val=""):
    cfg_file = os.path.join(ROOT_DIR, "config_secrets.json")
    if os.path.exists(cfg_file):
        try:
            with open(cfg_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get(key_name, default_val)
        except Exception:
            pass
    return default_val

META_TOKEN = load_secret("META_ACCESS_TOKEN")
TELEGRAM_BOT_TOKEN = load_secret("TELEGRAM_BOT_TOKEN", "8977196047:AAFpxQRS__g4pG0HetNk22vgOjqud5Ki9EA")
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

if __name__ == "__main__":
    ads = buscar_anuncios_meta()
    print("Meta Ads count:", len(ads))
