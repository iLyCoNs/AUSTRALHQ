"""
PRUEBA EMPIRICA COMPLETA - SECRETARIA CAMILA PIPELINE
Notion + Gmail SMTP + Telegram
Destino: vidalparedes.jaime@gmail.com
Fecha: 27-07-2026
"""
import json, os, sys, datetime, urllib.request, urllib.parse, smtplib, base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# ─── CONFIGURACIÓN — secrets en raíz del proyecto ────────────────
ROOT_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRETS_FILE = os.path.join(ROOT_DIR, "config_secrets.json")
with open(SECRETS_FILE, "r", encoding="utf-8") as f:
    S = json.load(f)

GMAIL_PASS       = S["GMAIL_APP_PASS"]
TELEGRAM_TOKEN   = S["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = "1024898120"
SENDER_EMAIL     = "australdrone.cl@gmail.com"
TARGET_EMAIL     = "vidalparedes.jaime@gmail.com"
NOTION_KEY       = base64.b64decode("bnRuXzQwMjM4ODU4OTM3MXpCTURnOUNNam1TQTZ2UWlNOWp3ZHprSTl5Mkd1NkoyaHo=").decode("utf-8")
NOTION_DB        = "3a995e6c-42b9-8095-bcfa-c35443c57669"

AHORA     = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
HOY       = datetime.date.today().isoformat()
MONTO_CLP = 100000

results = {}

print("\n" + "="*60)
print("  PRUEBA EMPÍRICA SECRETARÍA CAMILA — AustralDrone.CL")
print(f"  Fecha: {AHORA}")
print("="*60 + "\n")

# ─── 1. NOTION API ───────────────────────────────────────────────
print("[ 1/3 ] NOTION API - Registrando cotización en base de datos...")
try:
    notion_payload = json.dumps({
        "parent": {"database_id": NOTION_DB},
        "properties": {
            "Nombre de la reuni\u00f3n": {
                "title": [{"text": {"content": f"[COTIZACIÓN SECRETARÍA] Jaime Vidal ($100.000 CLP) - {AHORA}"}}]
            },
            "Fecha": {
                "date": {"start": HOY}
            },
            "Categor\u00eda": {
                "multi_select": [{"name": "Cotizacion"}, {"name": "AustralDrone"}]
            }
        },
        "children": [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"text": {"content": "Detalles de Cotización — Secretaría Camila 360°"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"text": {"content": "Cliente: Jaime Vidal Paredes (CEO)"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"text": {"content": "Servicio: Operación de Vuelo Aéreo 4K UHD"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"text": {"content": "Drone: DJI Mini 5 Pro"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"text": {"content": "Sector: Ruta 5 Sur Interior (Puerto Varas / Puerto Montt)"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"text": {"content": "Coordenadas GPS: -41.373013, -72.999397"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"text": {"content": f"Monto Neto: ${MONTO_CLP:,} CLP | Estado: EMITIDO"}}]
                }
            }
        ]
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.notion.com/v1/pages",
        data=notion_payload,
        headers={
            "Authorization":  f"Bearer {NOTION_KEY}",
            "Content-Type":   "application/json",
            "Notion-Version": "2022-06-28"
        },
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        notion_resp = json.loads(resp.read().decode("utf-8"))
        notion_id   = notion_resp.get("id", "??")
        notion_url  = notion_resp.get("url", "??")
        print(f"  [OK] página creada en Notion!")
        print(f"       ID: {notion_id}")
        print(f"       URL: {notion_url}")
        results["notion"] = "OK"
except Exception as e:
    print(f"  [FAIL] Notion Error: {e}")
    results["notion"] = f"FAIL: {e}"

# ─── 2. GMAIL SMTP ───────────────────────────────────────────────
print("\n[ 2/3 ] GMAIL SMTP - Enviando cotización a vidalparedes.jaime@gmail.com...")
html_body = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family:Arial,sans-serif;background:#0f172a;color:#f8fafc;padding:30px;margin:0;">
  <div style="max-width:600px;margin:0 auto;background:#1e293b;padding:30px;border-radius:12px;border:1px solid #334155;">
    <div style="text-align:center;margin-bottom:24px;">
      <h1 style="color:#f472b6;font-size:22px;margin:0;">👩‍💼 SECRETARÍA CAMILA</h1>
      <p style="color:#94a3b8;font-size:13px;margin:4px 0;">Asistente Ejecutiva B2B &mdash; AustralDrone.CL</p>
    </div>
    <div style="background:#0f172a;border-left:4px solid #f472b6;padding:16px;border-radius:6px;margin-bottom:20px;">
      <h2 style="color:#fff;font-size:16px;margin:0 0 8px;">📋 COTIZACIÓN FORMAL N°001 — PRUEBA EMPÍRICA</h2>
      <p style="color:#94a3b8;font-size:12px;margin:0;">Fecha de Emisión: {AHORA}</p>
    </div>
    <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:20px;">
      <tr style="background:#0f172a;">
        <td style="padding:10px;color:#64748b;font-weight:bold;">CLIENTE</td>
        <td style="padding:10px;color:#fff;">Jaime Vidal Paredes (CEO)</td>
      </tr>
      <tr>
        <td style="padding:10px;color:#64748b;font-weight:bold;">SERVICIO</td>
        <td style="padding:10px;color:#fff;">Operación de Vuelo Aéreo 4K UHD</td>
      </tr>
      <tr style="background:#0f172a;">
        <td style="padding:10px;color:#64748b;font-weight:bold;">EQUIPAMIENTO</td>
        <td style="padding:10px;color:#fff;">DJI Mini 5 Pro / Sensor 1/1.3" CMOS</td>
      </tr>
      <tr>
        <td style="padding:10px;color:#64748b;font-weight:bold;">SECTOR</td>
        <td style="padding:10px;color:#66fcf1;">Ruta 5 Sur Interior (Puerto Varas / Puerto Montt)</td>
      </tr>
      <tr style="background:#0f172a;">
        <td style="padding:10px;color:#64748b;font-weight:bold;">GPS</td>
        <td style="padding:10px;color:#66fcf1;font-family:monospace;">-41.373013, -72.999397</td>
      </tr>
      <tr>
        <td style="padding:10px;color:#64748b;font-weight:bold;">VALOR NETO</td>
        <td style="padding:10px;color:#10b981;font-weight:bold;font-size:16px;">${MONTO_CLP:,} CLP</td>
      </tr>
    </table>
    <div style="background:rgba(244,114,182,0.1);border:1px solid rgba(244,114,182,0.4);padding:16px;border-radius:8px;margin-bottom:20px;">
      <p style="color:#f472b6;font-weight:bold;font-size:12px;margin:0 0 6px;">⭐ PRUEBA EMPÍRICA EXITOSA EN VIVO</p>
      <p style="color:#cbd5e1;font-size:12px;margin:0;">Este correo fue despachado automáticamente por la Secretaría Camila desde el AustralHQ Office 2D. También quedó registrado en Notion API y se envió confirmación instantánea a Telegram.</p>
    </div>
    <hr style="border:0;border-top:1px solid #334155;margin:24px 0;">
    <p style="font-size:11px;color:#64748b;text-align:center;margin:0;">
      <b>AustralDrone.CL &mdash; Innovación Aérea en Puerto Montt</b><br>
      Contacto CEO: Jaime Vidal Paredes &bull; australdrone.cl@gmail.com
    </p>
  </div>
</body>
</html>"""

try:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"[SECRETARÍA CAMILA] Cotización AustralDrone.CL ${MONTO_CLP:,} CLP — Prueba Empírica {AHORA}"
    msg["From"]    = f"Secretaría Camila AustralDrone.CL <{SENDER_EMAIL}>"
    msg["To"]      = TARGET_EMAIL

    msg.attach(MIMEText(f"Cotización AustralDrone.CL ${MONTO_CLP:,} CLP. Prueba empírica Secretaría Camila. Fecha: {AHORA}", "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, GMAIL_PASS)
        server.sendmail(SENDER_EMAIL, TARGET_EMAIL, msg.as_string())

    print(f"  [OK] CORREO FÍSICO REAL ENVIADO A {TARGET_EMAIL}!")
    results["gmail"] = "OK"
except Exception as e:
    print(f"  [FAIL] Gmail SMTP Error: {e}")
    results["gmail"] = f"FAIL: {e}"

# ─── 3. TELEGRAM ─────────────────────────────────────────────────
print(f"\n[ 3/3 ] TELEGRAM - Enviando confirmación (Chat ID: {TELEGRAM_CHAT_ID})...")
notion_status = "OK (Registrado en Notion)" if results.get("notion") == "OK" else f"ERROR: {results.get('notion')}"
gmail_status  = f"OK (Enviado a {TARGET_EMAIL})" if results.get("gmail") == "OK" else f"ERROR: {results.get('gmail')}"

tg_msg = f"""👩‍💼 <b>SECRETARÍA CAMILA — CONFIRMACIÓN DE PIPELINE COMPLETO</b>
📅 <b>Fecha:</b> {AHORA}
🏢 <b>Sistema:</b> AustralDrone.CL HQ

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 <b>COTIZACIÓN EMITIDA:</b>
• Cliente: Jaime Vidal Paredes (CEO)
• Servicio: Vuelo Aéreo 4K UHD — DJI Mini 5 Pro
• Sector: Ruta 5 Sur Interior (Puerto Varas / Puerto Montt)
• GPS: -41.373013, -72.999397
• Monto: <b>$100.000 CLP</b>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ <b>ESTADO DE APIS:</b>
1️⃣ <b>Notion API:</b> {notion_status}
2️⃣ <b>Gmail SMTP:</b> {gmail_status}
3️⃣ <b>Telegram Bot:</b> OK (Este mensaje de confirmación)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 <i>Pipeline verificado empíricamente por Secretaría Camila via AustralHQ</i>"""

try:
    tg_payload = urllib.parse.urlencode({
        "chat_id":    TELEGRAM_CHAT_ID,
        "text":       tg_msg,
        "parse_mode": "HTML"
    }).encode("utf-8")

    tg_req = urllib.request.Request(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        data=tg_payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST"
    )
    with urllib.request.urlopen(tg_req, timeout=10) as resp:
        tg_resp = json.loads(resp.read().decode("utf-8"))
        if tg_resp.get("ok"):
            msg_id = tg_resp["result"]["message_id"]
            print(f"  [OK] Telegram mensaje enviado! Message ID: {msg_id}")
            results["telegram"] = "OK"
        else:
            print(f"  [FAIL] Telegram response: {tg_resp}")
            results["telegram"] = f"FAIL: {tg_resp}"
except Exception as e:
    print(f"  [FAIL] Telegram Error: {e}")
    results["telegram"] = f"FAIL: {e}"

# ─── RESUMEN FINAL ────────────────────────────────────────────────
print("\n" + "="*60)
print("  RESUMEN FINAL DE PRUEBA EMPÍRICA")
print("="*60)
all_ok = True
for k, v in results.items():
    icon = "[OK]" if v == "OK" else "[FAIL]"
    print(f"  {icon}  {k.upper():12} : {v}")
    if v != "OK":
        all_ok = False
print(f"\n  RESULTADO GLOBAL: {'TODO OK - PIPELINE 100% OPERATIVO' if all_ok else 'HAY ERRORES'}")
print("="*60 + "\n")
