import os, re, base64

# Token correcto
good_token = '8977196047:AAFpxQRS__g4pG0HetNk22vgOjqud5Ki9EA'
good_token_b64 = base64.b64encode(good_token.encode()).decode()
bad_token_b64 = 'ODk3NzE5NjA0NzpBQUZweFFSU19fZzRQRzBIZXROazIydmdPalF1ZDVLaTlFQQ=='
good_webhook = 'https://australhq.onrender.com/api/secretaria/web-chatbot-webhook'
n8n_webhook = 'https://lycons.app.n8n.cloud/webhook/vibe-copilot'

# Archivo que ESTÁ en Vercel desplegado
target_file = r"c:\Users\LyCoNs\Desktop\AI CHABOT\vibe-copilot.js"

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Corregir el token base64 dentro del archivo 
content = content.replace(bad_token_b64, good_token_b64)

# Asegurar que la función de Telegram en _triggerN8nActionEvent usa el token correcto
content = content.replace(
    '"8977196047:AAFpxQRS__g4PG0HetNk22vgOjQud5Ki9EA"',
    f'"{good_token}"'
)

with open(target_file, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"FIXED vibe-copilot.js")
print(f"Good token B64: {good_token_b64}")

# Ahora el problema PRINCIPAL: La web de australdrone.cl tiene VibeCopilotConfig con el token malo
# Tenemos que buscar donde esta el HTML fuente de australdrone.cl
# Revisar 27-06 (posible folder del sitio web)
folder_27 = r"c:\Users\LyCoNs\Desktop\27-06"
if os.path.exists(folder_27):
    for root, dirs, files in os.walk(folder_27):
        dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', 'dist']]
        for f in files:
            if f.endswith(('.html', '.js', '.json')):
                fp = os.path.join(root, f)
                try:
                    with open(fp, 'r', encoding='utf-8', errors='ignore') as fh:
                        c = fh.read()
                        if 'VibeCopilotConfig' in c or bad_token_b64 in c or 'ODk3NzE5' in c:
                            print(f"FOUND IN 27-06: {fp}")
                except:
                    pass
else:
    print("27-06 no existe")
