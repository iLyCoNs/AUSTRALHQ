"""
===============================================================================
MÓDULO: Agente 14 - Outbound B2B "Caballo de Troya" + Panel Dashboard
Empresa: AustralDrone.CL
Objetivo: Procesar el CSV de vendedores/macrolotes, generar mensajes persuasivos
          de diagnóstico con Llama 3.1 70B y construir el Panel HTML de contacto en 1-Click.
===============================================================================
"""

import csv
import json
import os
import urllib.parse
from langchain_openai import ChatOpenAI

# Configuración LLM NVIDIA
import base64
def get_nv_key():
    env_k = os.environ.get("NVIDIA_API_KEY")
    if env_k: return env_k
    enc = "bnZhcGktbGdsWlNVWGRYajhjZmMzU09GR2tObTZvWG9obmF1V3UtcUk2elhibEtMOElBZEdLRXJmdTFQVTFIS3BEczJldQ=="
    return base64.b64decode(enc).decode('utf-8')

class CustomChatOpenAI(ChatOpenAI):
    provider: str = "openai"
    model: str = "meta/llama-3.1-70b-instruct"

llm = CustomChatOpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=get_nv_key(),
    model="meta/llama-3.1-70b-instruct"
)

CSV_PATH = r"c:\Users\LyCoNs\Desktop\AGENTES IA\VENDEDORES_MACROLOTES_MASTERPLAN_360.csv"
OUT_HTML = r"c:\Users\LyCoNs\Desktop\AGENTES IA\PANEL_CABALLO_DE_TROYA_B2B.html"

def generar_script_caballo_troya(nombre, superficie, ubicacion, precio, fuente):
    prompt = f"""Eres el Director Comercial de AustralDrone.CL en el Sur de Chile.
Genera un mensaje corto, ultra-profesional y persuasivo de tipo "Caballo de Troya" (ofrecer valor/diagnóstico sin vender agresivo) para enviar por WhatsApp o Messenger.

DATOS DEL CLIENTE:
- Nombre: {nombre}
- Superficie: {superficie}
- Ubicación: {ubicacion}
- Precio: {precio}
- Fuente: {fuente}

REGLAS DEL MENSAJE:
1. Máximo 4 frases.
2. Menciona específicamente su terreno de {superficie} en {ubicacion}.
3. Señala un punto débil: que sin video drone 4K o MasterPlan 360° interactivo los compradores demoran meses en decidir.
4. Cierra con una pregunta abierta ofreciendo enviar una demostración rápida sin compromiso.
5. Usa tono cordial de experto regional.

Devuelve SOLO el texto del mensaje."""

    try:
        res = llm.invoke(prompt)
        return res.content.strip()
    except Exception as e:
        return f"Hola {nombre}, vi tu terreno de {superficie} en {ubicacion}. En AustralDrone.CL ayudamos a acelerar la venta con MasterPlan 360° y video drone. ¿Te puedo enviar una muestra?"

def procesar_prospectos():
    if not os.path.exists(CSV_PATH):
        print("El archivo CSV no existe aún.")
        return

    prospectos = []
    with open(CSV_PATH, 'r', encoding='utf-8-sig') as f:
        reader = list(csv.DictReader(f))
        prospectos = reader[:25]  # Top 25 prospectos calificados

    print(f"Procesando {len(prospectos)} prospectos para el Panel Caballo de Troya B2B...")

    html_content = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Panel Caballo de Troya B2B - AustralDrone.CL</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { font-family: 'Outfit', sans-serif; background: #0f172a; color: #f8fafc; margin: 24px; }
        h1 { color: #38bdf8; font-weight: 900; margin-bottom: 8px; }
        p.subtitle { color: #94a3b8; margin-bottom: 24px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 20px; }
        .card { background: #1e293b; border-radius: 16px; padding: 20px; border-left: 6px solid #eab308; border: 1px solid rgba(255,255,255,0.08); box-shadow: 0 10px 25px rgba(0,0,0,0.3); }
        .title { font-size: 1.1em; font-weight: 700; color: #f1f5f9; margin-bottom: 6px; }
        .meta { font-size: 0.85em; color: #94a3b8; margin-bottom: 12px; }
        .badge { background: rgba(56, 189, 248, 0.15); color: #38bdf8; padding: 3px 8px; border-radius: 12px; font-weight: 600; font-size: 0.8em; }
        .msg-box { background: #0f172a; padding: 14px; border-radius: 10px; border: 1px solid #334155; font-size: 0.9em; line-height: 1.5; margin: 12px 0; color: #cbd5e1; }
        .btn-group { display: flex; gap: 10px; margin-top: 12px; }
        .btn { flex: 1; padding: 10px; border-radius: 10px; text-decoration: none; font-weight: 700; text-align: center; font-size: 0.9em; display: inline-flex; align-items: center; justify-content: center; gap: 6px; }
        .btn-wsp { background: #22c55e; color: white; }
        .btn-wsp:hover { background: #16a34a; }
        .btn-link { background: #3b82f6; color: white; }
        .btn-link:hover { background: #2563eb; }
    </style>
</head>
<body>
    <h1>🐴 PANEL DE OUTBOUND B2B: CABALLO DE TROYA</h1>
    <p class="subtitle">Mensajes de diagnóstico personalizado listos para contacto manual (AustralDrone.CL - Ley N° 19.496 Compliant)</p>
    <div class="grid">
"""

    for idx, p in enumerate(prospectos, 1):
        nombre = p.get('Nombre Vendedor') or 'Vendedor'
        superficie = p.get('Superficie Terreno (Has)') or p.get('Superficie Has') or 'Terreno'
        ubicacion = p.get('Ubicación Terreno') or p.get('Ubicacion') or 'Sur de Chile'
        precio = p.get('Precio Venta (CLP / UF)') or p.get('Precio CLP UF') or 'Consultar'
        telefono = p.get('Teléfono / Contacto') or p.get('Telefono Contacto') or ''
        link_post = p.get('Link Publicación Grupo') or p.get('Link Post Directo') or ''
        fuente = p.get('Fuente') or 'Publicación'

        mensaje_troya = generar_script_caballo_troya(nombre, superficie, ubicacion, precio, fuente)
        
        num_clean = "".join([c for c in telefono if c.isdigit()])
        wsp_url = ""
        if len(num_clean) >= 8:
            if not num_clean.startswith("56"):
                num_clean = "56" + num_clean
            wsp_url = f"https://api.whatsapp.com/send?phone={num_clean}&text={urllib.parse.quote(mensaje_troya)}"

        html_content += f"""
        <div class="card">
            <div class="title">#{idx} {nombre}</div>
            <div class="meta"><span class="badge">{superficie}</span> • 📍 {ubicacion} • 💰 {precio}</div>
            <div class="msg-box">"{mensaje_troya}"</div>
            <div class="btn-group">
                {"<a href='" + wsp_url + "' target='_blank' class='btn btn-wsp'><i class='fa-brands fa-whatsapp'></i> Enviar WSP</a>" if wsp_url else "<span class='btn' style='background:#334155; color:#94a3b8;'>Sin Teléfono Directo</span>"}
                {"<a href='" + link_post + "' target='_blank' class='btn btn-link'><i class='fa-solid fa-arrow-up-right-from-square'></i> Ver Post</a>" if link_post else ""}
            </div>
        </div>
        """

    html_content += "</div></body></html>"

    with open(OUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Panel Caballo de Troya actualizado en: {OUT_HTML}")

if __name__ == "__main__":
    procesar_prospectos()
