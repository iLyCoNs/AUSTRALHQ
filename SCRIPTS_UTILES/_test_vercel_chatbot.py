import requests, json

url = "https://chatbot-ad-mocha.vercel.app/api/chat"
headers = {"Content-Type": "application/json"}
payload = {
    "businessName": "Austral Drone",
    "messages": [
        {"role": "user", "content": "Hola, necesito información sobre cotizar un MasterPlan 360 y fotos drone para parcelas en Puerto Varas."}
    ]
}

print("[TEST VERCEL CHATBOT] Probando conectividad con chatbot-ad-mocha.vercel.app...")
try:
    r = requests.post(url, headers=headers, json=payload, timeout=10)
    print("STATUS:", r.status_code)
    print("RESPONSE:", r.json())
except Exception as e:
    print("ERR:", e)
