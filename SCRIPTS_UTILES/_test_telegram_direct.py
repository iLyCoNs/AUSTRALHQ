import requests, json

tg_token = "8977196047:AAFpxQRS__g4pG0HetNk22vgOjqud5Ki9EA"
tg_chat_id = "1024898120"
url = f"https://api.telegram.org/bot{tg_token}/sendMessage"

text = (
    "🔔 <b>PRUEBA DE NOTIFICACIÓN DE CLIENTE ACTIVO EN VIVO</b>\n\n"
    "💬 <b>Estado:</b> Cliente interactuando en tiempo real en www.australdrone.cl\n"
    "👤 <b>Cliente:</b> Jaime (Puerto Varas)\n"
    "📞 <b>Teléfono:</b> +56987491964\n"
    "📝 <b>Última interacción:</b> 'que me llame'\n\n"
    "👩‍💼 <i>Secretaría Camila: Alerta de actividad en vivo enviada a Telegram.</i>"
)

payload = {
    "chat_id": tg_chat_id,
    "text": text,
    "parse_mode": "HTML"
}

print("[TEST TELEGRAM DIRECT] Enviando mensaje a Telegram de Jaime...")
try:
    r = requests.post(url, json=payload, timeout=10)
    print("STATUS:", r.status_code)
    print("RESPONSE:", json.dumps(r.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print("ERR:", e)
