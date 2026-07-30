import requests

TELEGRAM_BOT_TOKEN = "8977196047:AAFpxQRS__g4pG0HetNk22vgOjqud5Ki9EA"
TELEGRAM_CHAT_ID = "1024898120"

def send_telegram_alert(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": msg,
        "parse_mode": "HTML"
    }
    res = requests.post(url, json=payload, timeout=8)
    print("Telegram Response:", res.status_code, res.text)

tg_msg = (
    f"<b>🎯 CAZADOR PROSPECCIÓN EN VIVO — PUBLICACIONES INDIVIDUALES EXACTAS (+$20M CLP)</b>\n\n"
    f"<b>Zona Evaluada:</b> Puerto Varas & Frutillar (Región de Los Lagos)\n"
    f"<b>Algoritmo:</b> Extracción de Ficha Individual + Conversión UF -> CLP (+20M CLP)\n\n"
    f"📍 <b>1. Venta Parcela 5.000 Mts2 Nueva Braunau - Puerto Varas</b>\n"
    f"💰 <b>Precio:</b> $48.000.000 CLP\n"
    f"📐 <b>Superficie:</b> 5.000 m²\n"
    f"📷 <b>Inspección Visual:</b> 5 Fotos de Pasto, Vegetación y Terreno Plano\n"
    f"🔗 <a href='https://portalinmobiliario.com/MLC-4047505760-venta-parcela-5000-mts2-n-braunau-puerto-varas-_JM'>Abrir Publicación Exacta en PortalInmobiliario</a>\n\n"
    f"📍 <b>2. Parcelas Con Estero Privado En Puerto Varas</b>\n"
    f"💰 <b>Precio:</b> 1.500 UF (~ $57.000.000 CLP)\n"
    f"📐 <b>Superficie:</b> 5.000 m² + Estero Privado\n"
    f"📷 <b>Inspección Visual:</b> 5 Fotos de Vegetación Nativa y Agua\n"
    f"🔗 <a href='https://portalinmobiliario.com/MLC-3911497022-parcelas-con-estero-privado-en-puerto-varas-_JM'>Abrir Publicación Exacta en PortalInmobiliario</a>\n\n"
    f"📍 <b>3. Hermosa Casa Nueva En Parcela - Puerto Varas</b>\n"
    f"💰 <b>Precio:</b> 5.390 UF (~ $204.820.000 CLP)\n"
    f"🏠 <b>Tipo:</b> Casa Construida en Parcela\n"
    f"📷 <b>Inspección Visual:</b> Casa Terminada + Entorno Natural\n"
    f"🔗 <a href='https://portalinmobiliario.com/MLC-4234030034-hermosa-casa-nueva-en-parcela-_JM'>Abrir Publicación Exacta en PortalInmobiliario</a>\n\n"
    f"<i>Secretaría Camila™ & Cazador Web 360 Enterprise.</i>"
)

send_telegram_alert(tg_msg)
