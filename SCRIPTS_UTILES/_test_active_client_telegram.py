import requests, json

url = "http://localhost:8080/api/secretaria/web-chatbot-webhook"
headers = {"Content-Type": "application/json"}
payload = {
  "event": "cliente_activo_web",
  "businessName": "Austral Drone",
  "data": {
    "capturedPhone": "+56987491964",
    "leadScore": 95,
    "lastMessage": "Jaime interactuando en vivo en www.australdrone.cl: 'que me llame'"
  }
}

print("[TEST ACTIVE CLIENT TELEGRAM] Enviando evento a Camila...")
try:
    r = requests.post(url, headers=headers, json=payload, timeout=8)
    print("STATUS:", r.status_code)
    print("RESPONSE:", json.dumps(r.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print("ERR:", e)
