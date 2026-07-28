import requests, json

url = "http://localhost:8080/api/secretaria/web-chatbot-webhook"
headers = {"Content-Type": "application/json"}
payload = {
  "event": "telegram_contact_captured",
  "businessName": "Austral Drone",
  "telegramToken": "ODk3NzE5NjA0NzpBQUZweFFSU19fZzRQRzBIZXROazIydmdPalF1ZDVLaTlFQQ==",
  "telegramChatId": "1024898120",
  "data": {
    "capturedPhone": "+56987491964",
    "leadScore": 85,
    "lastMessage": "Cliente solicitó agendar reunión para MasterPlan 360 en Frutillar"
  }
}

print("[TEST WEBHOOK CAMILA] Enviando evento de captura de lead web a Camila...")
try:
    r = requests.post(url, headers=headers, json=payload, timeout=8)
    print("STATUS:", r.status_code)
    print("RESPONSE:", json.dumps(r.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print("ERR:", e)
