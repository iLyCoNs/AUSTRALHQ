import requests, json, re, base64

good_token = '8977196047:AAFpxQRS__g4pG0HetNk22vgOjqud5Ki9EA'
bad_token_decoded = '8977196047:AAFpxQRS__g4PG0HetNk22vgOjQud5Ki9EA'

# 1. TEST N8N: Ver si realmente procesa y envia a Telegram
print("=== 1. TEST N8N WEBHOOK COMPLETO ===")
n8n_url = 'https://lycons.app.n8n.cloud/webhook/vibe-copilot'

# Enviar payload exacto como lo haría Gigi
payload_score50 = {
    "event": "telegram_lead_50",
    "businessName": "Austral Drone",
    "data": {
        "leadScore": 95,
        "capturedPhone": "+56987491964",
        "salesStage": "STAGE_5_COMMITMENT",
        "lastMessage": "DIAGNOSTICO CAMILA: grabar 30 parcelas en Puerto Varas",
        "history": [
            {"role": "user", "content": "grabar 30 parcelas"},
            {"role": "assistant", "content": "¡Prospecto de alta prioridad!"}
        ]
    }
}
try:
    r = requests.post(n8n_url, json=payload_score50, timeout=10)
    print("N8N STATUS:", r.status_code)
    print("N8N RESPONSE:", r.text[:500])
except Exception as e:
    print("N8N ERR:", e)

# 2. TEST TELEGRAM DIRECTO con el token correcto
print("\n=== 2. TELEGRAM DIRECTO TOKEN CORRECTO ===")
r2 = requests.post(f'https://api.telegram.org/bot{good_token}/sendMessage', json={
    'chat_id': '1024898120',
    'text': '🔬 DIAGNÓSTICO COMPLETO CAMILA:\n\n✅ Canal Telegram ACTIVO\n✅ Token Correcto Verificado\n\nSi ves esto, el problema estaba en el token malo del HTML de australdrone.cl',
    'parse_mode': 'HTML'
})
print("TELEGRAM DIRECTO OK:", r2.json().get('ok'))
