import requests, json

url = "http://localhost:8080/api/secretaria/web-chatbot-webhook"
headers = {"Content-Type": "application/json"}
payload = {
  "event": "telegram_contact_captured",
  "businessName": "Austral Drone",
  "telegramToken": "8977196047:AAFpxQRS__g4pG0HetNk22vgOjqud5Ki9EA",
  "telegramChatId": "1024898120",
  "data": {
    "capturedPhone": "+56987491964",
    "leadScore": 100,
    "lastMessage": "Jaime solicitó llamada directa del CEO sobre su proyecto en Puerto Varas ('que me llame')"
  }
}

print("[SIMULATING JAIME MYSTERY SHOPPER WEB LEAD] Enviando a Camila...")
try:
    r = requests.post(url, headers=headers, json=payload, timeout=8)
    print("STATUS:", r.status_code)
    print("RESPONSE:", json.dumps(r.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print("ERR:", e)
