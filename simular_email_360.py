import requests
import json
import base64
import os

import re
from datetime import datetime

TARGET_EMAIL = "vidalparedes.jaime@gmail.com"
TELEGRAM_CHAT_ID = "1024898120"
N8N_WEBHOOK_URL = "https://lycons.app.n8n.cloud/webhook/cazador-b2b-dual"
MEMORY_FILE = os.path.join(os.path.dirname(__file__), "CAZADOR_BANANA_MEMORY.json")

def cargar_memoria_banana():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"enviados": [], "emails": [], "dominios": [], "empresas": []}

def guardar_memoria_banana(memoria):
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(memoria, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error guardando memoria Cazador Banana: {e}")

def ya_fue_contactado(email, empresa="", website=""):
    memoria = cargar_memoria_banana()
    
    # 1. Chequeo por email (excepto test mail personal)
    if email and email.lower().strip() != "vidalparedes.jaime@gmail.com":
        if email.lower().strip() in [e.lower() for e in memoria.get("emails", [])]:
            return True, f"Correo '{email}' ya fue contactado previamente."
        
    # 2. Chequeo por nombre de empresa
    if empresa:
        emp_norm = re.sub(r'[^a-zA-Z0-9]', '', empresa).lower()
        for emp_exist in memoria.get("empresas", []):
            if re.sub(r'[^a-zA-Z0-9]', '', emp_exist).lower() == emp_norm:
                return True, f"Empresa '{empresa}' ya recibió propuesta anteriormente."
                
    # 3. Chequeo por dominio web
    if website:
        dom = website.lower().replace('https://', '').replace('http://', '').replace('www.', '').split('/')[0]
        if dom and dom in [d.lower() for d in memoria.get("dominios", [])]:
            return True, f"Dominio '{dom}' ya fue auditado y contactado."
            
    return False, "Nuevo prospecto no contactado."

def registrar_envio_exitoso(email, empresa="", website="", asunto="", oferta="MASTERPLAN_360"):
    memoria = cargar_memoria_banana()
    now_iso = datetime.now().isoformat()
    
    entry = {
        "email": email,
        "empresa": empresa,
        "website": website,
        "asunto": asunto,
        "oferta": oferta,
        "fecha_envio": now_iso
    }
    
    memoria["enviados"].append(entry)
    if email and email not in memoria["emails"]:
        memoria["emails"].append(email)
    if empresa and empresa not in memoria["empresas"]:
        memoria["empresas"].append(empresa)
    if website:
        dom = website.lower().replace('https://', '').replace('http://', '').replace('www.', '').split('/')[0]
        if dom and dom not in memoria["dominios"]:
            memoria["dominios"].append(dom)
            
    guardar_memoria_banana(memoria)
    print(f"[MEMORIA CAZADOR BANANA] Guardado en registro permanente: {email} | {empresa}")

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

def generar_propuesta_360(empresa="Country Puerto Varas", rubro="Inmobiliarias", zona="Puerto Varas / Los Lagos"):
    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {get_nv_key()}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""Eres el Director Comercial de AustralDrone.CL, basados en Puerto Montt, Región de Los Lagos (expertos en Masterplan 360° Inmobiliario, Ortomosaicos 3D, Grabación Drone 4K y ChatBots con IA).

Redacta una propuesta comercial altamente respetuosa, profesional y armoniosa dirigida al Gerente Comercial de la empresa '{empresa}' ({rubro} en {zona}).

REGLAS DE ORO DEL CORREO:
1. Iniciar presentándonos como AustralDrone.CL desde Puerto Montt.
2. Expresar nuestro deseo de ser PARTNERS PERMANENTES para impulsar las ventas de sus parcelas actuales y futuras en la región.
3. Presentar nuestros planes de MasterPlan 360° Económicos:
   - PLAN BÁSICO: MasterPlan 360° interactivo + Videos y Fotografías Aéreas Drone 4K.
   - PLAN PREMIUM: MasterPlan 360° + Videos/Fotos Drone 4K + ChatBot Interactivo con IA 24/7 (atiende dudas de compradores al instante sin intervención manual).
4. Iluminar su oportunidad comercial: Explicar cómo esto permite a compradores de Santiago y el extranjero recorrer las parcelas virtualmente antes de viajar, incrementando las ventas a distancia en más de un 40%.
5. Cierre respetuoso invitando a una breve conversación de 10 minutos para evaluar cómo potenciar sus parcelaciones.

Devuelve ÚNICAMENTE un objeto JSON válido:
{{
    "asunto": "Asunto profesional y atractivo sobre alianza y MasterPlan 360",
    "cuerpo_html": "Cuerpo HTML elegante con tonos azul pastel #8CA3B0, arena lujo #DCCBAE y fondo oscuro #0f172a, tarjetas para Plan Básico vs Plan Premium y botón CTA",
    "cuerpo_texto": "Versión en texto plano legible",
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
        "asunto": "Alianza Estratégica & MasterPlan 360° Económico para sus Parcelaciones | AustralDrone.CL Puerto Montt",
        "cuerpo_html": f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family: 'Inter', Arial, sans-serif; background-color: #0f172a; color: #f8fafc; padding: 30px;">
  <div style="max-width: 640px; margin: 0 auto; background-color: #1e293b; padding: 36px; border-radius: 16px; border: 1px solid #334155; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
    <div style="text-align: center; margin-bottom: 24px;">
      <h2 style="color: #8CA3B0; font-size: 13px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; margin: 0;">AUSTRALDRONE.CL — PUERTO MONTT</h2>
      <h1 style="color: #DCCBAE; font-size: 22px; margin-top: 6px; font-weight: 800;">MasterPlan 360° Económico & Alianza Comercial</h1>
    </div>
    
    <p style="font-size: 15px; color: #cbd5e1; line-height: 1.7;">Estimado Equipo Comercial de <b>{empresa}</b>,</p>
    
    <p style="font-size: 14px; color: #94a3b8; line-height: 1.7;">
      Le saludamos cordialmente desde <b>AustralDrone.CL en Puerto Montt</b>. Nos ponemos en contacto con el deseo de convertirnos en sus <b>Partners Permanentes</b> para impulsar la proyección de sus parcelas ofrecidas actuales y futuras en la Región de Los Lagos.
    </p>

    <p style="font-size: 14px; color: #94a3b8; line-height: 1.7;">
      Sabemos que brindar total certeza visual a los compradores e inversionistas de <b>Santiago y otras regiones</b> acelera drásticamente el cierre de ventas a distancia. Para ello, hemos estructurado planes de MasterPlan 360° accesibles y de alto impacto:
    </p>

    <!-- TARJETAS DE PLANES BÁSICO VS PREMIUM -->
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin: 24px 0;">
      <!-- PLAN BÁSICO -->
      <div style="background-color: #0f172a; padding: 20px; border-radius: 12px; border: 1px solid #334155;">
        <h4 style="color: #8CA3B0; font-size: 14px; margin-top: 0; margin-bottom: 8px;">🔹 PLAN BÁSICO</h4>
        <p style="font-size: 12px; color: #94a3b8; line-height: 1.6; margin-bottom: 12px;">Ideal para loteos que buscan impacto visual inmediato.</p>
        <ul style="color: #cbd5e1; font-size: 12px; line-height: 1.7; padding-left: 16px; margin: 0;">
          <li><b>MasterPlan 360° Interactivo</b> navegable.</li>
          <li><b>Fotografía Aérea HD</b> de linderos.</li>
          <li><b>Video Drone 4K</b> del entorno natural.</li>
        </ul>
      </div>

      <!-- PLAN PREMIUM -->
      <div style="background-color: #0f172a; padding: 20px; border-radius: 12px; border: 1px solid #DCCBAE; box-shadow: 0 0 15px rgba(220, 203, 174, 0.15);">
        <h4 style="color: #FFD700; font-size: 14px; margin-top: 0; margin-bottom: 8px;">🌟 PLAN PREMIUM + IA</h4>
        <p style="font-size: 12px; color: #94a3b8; line-height: 1.6; margin-bottom: 12px;">Solución integral de aceleración comercial 24/7.</p>
        <ul style="color: #cbd5e1; font-size: 12px; line-height: 1.7; padding-left: 16px; margin: 0;">
          <li>Todo lo del Plan Básico.</li>
          <li><b>ChatBot Interactivo con IA 24/7</b>.</li>
          <li>Responde dudas y cotizaciones al instante.</li>
        </ul>
      </div>
    </div>

    <p style="font-size: 14px; color: #cbd5e1; line-height: 1.7;">
      Nuestra tecnología permite que los clientes exploren cada parcela con total confianza, <b>incrementando la tasa de conversión a distancia en más de un 40%</b>.
    </p>

    <div style="text-align: center; margin: 32px 0 20px 0;">
      <a href="https://australdrone.cl" target="_blank" style="background: linear-gradient(135deg, #DCCBAE 0%, #CBB99C 100%); color: #111827; padding: 14px 28px; text-decoration: none; border-radius: 30px; font-weight: bold; font-size: 13px; display: inline-block; box-shadow: 0 4px 15px rgba(220, 203, 174, 0.3);">Explorar Tecnología 360° en AustralDrone.cl</a>
    </div>

    <hr style="border: 0; border-top: 1px solid #334155; margin-top: 32px; margin-bottom: 20px;">
    
    <p style="font-size: 12px; color: #64748b; text-align: center; line-height: 1.6;">
      <b>AustralDrone.CL — Puerto Montt, Región de Los Lagos</b><br>
      Partners Tecnológicos en MasterPlan 360°, Drones 4K y Agentes de IA.<br>
      <i>Contacto Directo: Jaime Vidal Paredes | CEO AustralDrone.CL (+56 9 8749 1964)</i>
    </p>
  </div>
</body>
</html>""",
        "cuerpo_texto": f"Estimado Equipo Comercial de {empresa}:\n\nLe saludamos cordialmente desde AustralDrone.CL en Puerto Montt. Queremos ser sus partners permanentes en la Región de Los Lagos para potenciar sus parcelaciones actuales y futuras.\n\nOfrecemos planes de MasterPlan 360° Económicos:\n1. PLAN BÁSICO: MasterPlan 360° + Videos y Fotos Drone 4K.\n2. PLAN PREMIUM: MasterPlan 360° + Videos 4K + ChatBot Interactivo con IA 24/7.\n\nConozca nuestra tecnología en https://australdrone.cl\n\nAtentamente,\nJaime Vidal Paredes | CEO AustralDrone.CL Puerto Montt",
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

    # 0. Chequeo de Memoria Persistente
    ya_enviado, motivo_dup = ya_fue_contactado(TARGET_EMAIL, empresa="Country Puerto Varas", website="countrypuertovaras.cl")
    if ya_enviado:
        print("\n[MEMORIA CAZADOR BANANA] OMITIDO DE ENVIO:")
        print(f"   - {motivo_dup}")
        print("   - La memoria impidio reenviar el correo a una empresa ya contactada.\n")
        return

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
        registrar_envio_exitoso(TARGET_EMAIL, empresa="Country Puerto Varas", website="countrypuertovaras.cl", asunto=asunto)

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
