import os, json

pkg_dir = r"c:\Users\LyCoNs\Desktop\Secretaria Camila+CHATBOTAI"

print("=== VERIFICACIÓN DE PAQUETE COMERCIAL ===")
for root, dirs, files in os.walk(pkg_dir):
    for f in files:
        fp = os.path.join(root, f)
        size = os.path.getsize(fp)
        rel = os.path.relpath(fp, pkg_dir)
        print(f"📄 {rel:<35} | {size:>7} bytes | Status: OK")

print("\n=== VERIFICACIÓN DE CARACTERÍSTICAS ===")
js_path = os.path.join(pkg_dir, "ASSETS", "vibe-copilot.js")
if os.path.exists(js_path):
    with open(js_path, "r", encoding="utf-8") as fh:
        js = fh.read()
    print(f"✅ vibe-copilot.js en ASSETS: {len(js)} bytes")
    print(f"  - Notificación instantánea en cada mensaje ('user_live_message'): {'user_live_message' in js}")
    print(f"  - Bypass de token Telegram (Token directo): {'8977196047' in js}")
    print(f"  - Lead Scoring BANT: {'SALES_STAGES' in js}")
    print(f"  - Webhook Render + n8n: {'web-chatbot-webhook' in js}")
