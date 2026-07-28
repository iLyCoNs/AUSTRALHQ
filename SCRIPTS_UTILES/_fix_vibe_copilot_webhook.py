import os

fp = r"c:\Users\LyCoNs\Desktop\AI CHABOT\vibe-copilot.js"

with open(fp, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Reemplazar webhookUrl por defecto por la URL real de Render
content = content.replace("webhookUrl: '',", "webhookUrl: 'https://australhq.onrender.com/api/secretaria/web-chatbot-webhook',")
content = content.replace("webhookUrl: \"\",", "webhookUrl: 'https://australhq.onrender.com/api/secretaria/web-chatbot-webhook',")

# 2. Asegurar que si telegramToken está desfasado se use el token válido
token_old = "ODk3NzE5NjA0NzpBQUZweFFSU19fZzRQRzBIZXROazIydmdPalF1ZDVLaTlFQQ=="
token_new_clean = "8977196047:AAFpxQRS__g4pG0HetNk22vgOjqud5Ki9EA"

# Reemplazar cualquier token antiguo de Telegram por el token verificado
content = content.replace(token_old, token_new_clean)

# 3. Asegurar que _triggerN8nActionEvent SIEMPRE dispare a https://australhq.onrender.com/api/secretaria/web-chatbot-webhook si no hay otra URL
target_func = "async function _triggerN8nActionEvent(eventType, payloadData) {"
if target_func in content:
    replacement = target_func + "\n    const targetUrl = _config.webhookUrl || 'https://australhq.onrender.com/api/secretaria/web-chatbot-webhook';\n    try {\n        fetch(targetUrl, {\n            method: 'POST',\n            headers: { 'Content-Type': 'application/json' },\n            body: JSON.stringify({ event: eventType, businessName: _config.businessName || 'Austral Drone', data: payloadData })\n        }).catch(e=>{});\n    } catch(e){}"
    content = content.replace(target_func, replacement)

with open(fp, 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: Patched vibe-copilot.js in AI CHABOT repo with default Render Webhook URL and clean Telegram Token!")
