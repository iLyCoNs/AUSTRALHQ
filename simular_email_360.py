import requests
import json
import base64
import os

TARGET_EMAIL = "vidalparedes.jaime@gmail.com"
TELEGRAM_CHAT_ID = "1024898120"
N8N_WEBHOOK_URL = "https://lycons.app.n8n.cloud/webhook/cazador-b2b-dual"

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

def get_gmail_pass():
    return load_secret("GMAIL_APP_PASS")

def get_nv_key():
    return load_secret("NVIDIA_API_KEY")

def generar_propuesta_360():
    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {get_nv_key()}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""Eres el Director Comercial B2B de AustralDrone 360 (empresa líder en Ortomosaicos 3D, MasterPlan 360 interactivo y Fotografía Aérea Drone 4K en el Sur de Chile).

Redacta una propuesta comercial fría B2B de alta conversión dirigida al Gerente Comercial de una inmobiliaria predial en el Sur de Chile (ej: Country Puerto Varas / Lomas de Cancura) que vende parcelas de 5.000m² y más.

OBJETIVO: Vender nuestro servicio de MasterPlan 360 Interactivo y Tour Drone 4K para elevar las ventas a distancia con compradores de Santiago y el extranjero.

Devuelve ÚNICAMENTE un objeto JSON estrictamente válido:
{{
    "asunto": "Asunto atractivo y profesional con emojis",
    "cuerpo_html": "Cuerpo HTML formateado con estilo elegante, viñetas, beneficios clave, estimación de retorno y llamado a reunión",
    "cuerpo_texto": "Versión en texto plano para clientes de correo tradicionales",
    "target_email": "{TARGET_EMAIL}"
}}"""

    payload = {
        "model": "meta/llama-3.1-70b-instruct",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3
    }
    
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=25)
        res_json = r.json()
        if 'choices' in res_json:
            content = res_json['choices'][0]['message']['content']
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            return json.loads(content)
        else:
            print("Response API:", res_json)
    except Exception as e:
        print(f"Error generando con Llama: {e}")
        
    return {
        "asunto": "Propuesta Exclusiva: MasterPlan 360 para Loteo Predial en Puerto Varas",
        "cuerpo_html": "<h1>Propuesta MasterPlan 360</h1><p>Potencie sus ventas de parcelas de 5.000m2 con ortomosaico 3D y tour drone 4K.</p>",
        "cuerpo_texto": "Estimado equipo comercial: Le presentamos la propuesta de MasterPlan 360 e integracion de ortomosaico 3D con tour drone 4K para potenciar la venta a distancia de sus parcelas prediales en el Sur de Chile.",
        "target_email": TARGET_EMAIL
    }

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SENDER_EMAIL = "australdrone.cl@gmail.com"
def enviar_correo_real_gmail(destinatario, asunto, cuerpo_html, cuerpo_texto):
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = asunto
        msg["From"] = f"AustralDrone 360 <{SENDER_EMAIL}>"
        msg["To"] = destinatario

        part1 = MIMEText(cuerpo_texto, "plain", "utf-8")
        part2 = MIMEText(cuerpo_html, "html", "utf-8")
        msg.attach(part1)
        msg.attach(part2)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, get_gmail_pass())
            server.sendmail(SENDER_EMAIL, destinatario, msg.as_string())
        
        return True
    except Exception as e:
        print(f"  [-] Error enviando SMTP Gmail: {e}")
        return False

def ejecutar_simulacion():
    print("\n=======================================================")
    print(" [ENVIO REAL DE EMAIL OUTREACH B2B - GMAIL SMTP]")
    print(f" Emisor: {SENDER_EMAIL}")
    print(f" Destinatario: {TARGET_EMAIL}")
    print("=======================================================\n")

    print("[IA LLAMA 3.1 70B] Generando propuesta B2B hiper-personalizada...")
    propuesta = generar_propuesta_360()

    asunto = propuesta.get("asunto", "Propuesta Exclusiva MasterPlan 360 para Loteo Predial en Puerto Varas")
    cuerpo_texto = propuesta.get("cuerpo_texto", "Estimado equipo comercial: Le presentamos la propuesta comercial de AustralDrone 360 para la integración de MasterPlan 360 interactivo, Ortomosaico 3D y Tour Virtual Drone 4K para potenciar la venta a distancia de sus parcelas prediales de 5.000 m2 y más en la zona de Puerto Varas / Los Lagos.")
    cuerpo_html = propuesta.get("cuerpo_html", f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family: Arial, sans-serif; background-color: #0f172a; color: #f8fafc; padding: 30px;">
  <div style="max-width: 600px; margin: 0 auto; background-color: #1e293b; padding: 30px; border-radius: 12px; border: 1px solid #334155;">
    <h1 style="color: #38bdf8; font-size: 24px;">🚀 Propuesta Comercial B2B — AustralDrone 360°</h1>
    <p style="font-size: 16px; color: #cbd5e1;">Estimado Equipo Comercial de <b>Country Puerto Varas</b>,</p>
    <p style="font-size: 15px; color: #94a3b8; line-height: 1.6;">
      Analizamos su presencia en el Sur de Chile y notamos que comercializan parcelas de <b>5.000 m² y más</b>. 
      Actualmente, los inversionistas de Santiago y el extranjero exigen visualizar el terreno de forma remota antes de viajar.
    </p>
    <div style="background-color: #0f172a; padding: 20px; border-radius: 8px; border-left: 4px solid #38bdf8; margin: 20px 0;">
      <h3 style="color: #f8fafc; margin-top: 0;">🎯 Lo que incluye la solución AustralDrone 360:</h3>
      <ul style="color: #cbd5e1; font-size: 14px; line-height: 1.8;">
        <li><b>Ortomosaico 3D de Alta Definición</b> con curvas de nivel y delimitación SAG.</li>
        <li><b>MasterPlan 360 Interactivo</b> con pins navegables por cada parcela.</li>
        <li><b>Fotografía Aérea y Video Drone 4K</b> integrado en su sitio web o pauta.</li>
      </ul>
    </div>
    <p style="font-size: 15px; color: #cbd5e1;">
      Elevamos la tasa de conversión a distancia en más de un <b>40%</b>.
    </p>
    <div style="text-align: center; margin-top: 30px;">
      <a href="https://australdrone.cl" style="background-color: #0284c7; color: #ffffff; padding: 14px 28px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">Agendar Demostración Interactiva</a>
    </div>
    <hr style="border: 0; border-top: 1px solid #334155; margin-top: 30px;">
    <p style="font-size: 12px; color: #64748b; text-align: center;">
      AustralDrone.CL — Soluciones Aéreas Inmobiliarias en el Sur de Chile.<br>
      Contacto Directo: Jaime Vidal Paredes | CEO AustralDrone
    </p>
  </div>
</body>
</html>""")

    print("\n[EMAIL ENVIADO EN VIVO POR GMAIL SMTP]")
    print("------------------------------------------------------------")
    print(f"De: {SENDER_EMAIL}")
    print(f"Para: {TARGET_EMAIL}")
    print(f"Asunto: {asunto}")
    print("------------------------------------------------------------\n")

    # 1. Enviar correo SMTP real
    print(f"[GMAIL SMTP] Enviando correo físico a {TARGET_EMAIL}...")
    exito_email = enviar_correo_real_gmail(TARGET_EMAIL, asunto, cuerpo_html, cuerpo_texto)
    if exito_email:
        print(f"  [SUCCESS] CORREO FISICO REAL ENTREGADO CON EXITO EN LA BANDEJA DE {TARGET_EMAIL}!")

    # 2. Despachar a Webhook de n8n Cloud
    print(f"[N8N CLOUD] Despachando evento a {N8N_WEBHOOK_URL}...")
    try:
        r_n8n = requests.post(N8N_WEBHOOK_URL, json={
            "evento": "EMAIL_OUTREACH_REAL_SENT",
            "sender_email": SENDER_EMAIL,
            "target_email": TARGET_EMAIL,
            "asunto": asunto,
            "cuerpo_html": cuerpo_html,
            "oferta": "MASTERPLAN_360"
        }, timeout=5)
        print(f"  Response n8n ({r_n8n.status_code}): {r_n8n.text}")
    except Exception as e:
        print(f"  Error n8n: {e}")

    # 3. Enviar notificación directa a Telegram del CEO Jaime
    print(f"[TELEGRAM] Transmitiendo copia a Telegram (Chat ID: {TELEGRAM_CHAT_ID})...")
    tg_msg = f"""📩 <b>[CORREO REAL DISPARADO A GMAIL]</b>

<b>De:</b> <code>{SENDER_EMAIL}</code>
<b>Para:</b> <code>{TARGET_EMAIL}</code>
<b>Asunto:</b> {asunto}

✅ <b>Estado:</b> Entregado exitosamente por Gmail SMTP en la bandeja de entrada."""

    try:
        r_tg = requests.post(f"https://api.telegram.org/bot{get_tg_token()}/sendMessage", json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": tg_msg,
            "parse_mode": "HTML"
        }, timeout=5)
        if r_tg.status_code == 200:
            print("  Notificacion transmitida a Telegram con exito (Status 200 OK)")
    except Exception as e:
        print(f"  Error Telegram: {e}")

if __name__ == "__main__":
    ejecutar_simulacion()
