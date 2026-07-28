import os

root_dir = r"c:\Users\LyCoNs\Desktop\AGENTES IA"
servers = [
    os.path.join(root_dir, "server.js"),
    os.path.join(root_dir, "CRM AustralDrone", "server.js")
]

prompt_render_extension = r'''
6. PROTOCOLO DE RECUPERACIÓN Y SINCRONIZACIÓN AL DESPERTAR DE RENDER.COM:
   • Comprendes perfectamente la infraestructura: Vercel (chatbot-ad-mocha.vercel.app) y Telegram están activos 24/7 en la nube y NUNCA duermen, mientras que Render.com entra en modo de reposo tras inactividad.
   • Cada vez que el servidor de Render se despierta o inicias una sesión con Don Jaime/Nicole, ejecutas tu "Protocolo de Auto-Despertar": consultas la Base de Datos de Notion y el historial de Vercel, consolidas todos los chats y teléfonos capturados durante tu periodo de reposo en LOGS_HISTORICOS/logs_secretaria_camila/LOG_WEB_CHATBOT.json y le entregas al CEO un reporte de sincronización de ausencia impecable.'''

for s in servers:
    if os.path.exists(s):
        with open(s, 'r', encoding='utf-8') as f:
            content = f.read()

        if "6. PROTOCOLO DE RECUPERACIÓN Y SINCRONIZACIÓN" not in content:
            marker = "=== TU OBJETIVO Y ESTILO DE INTERACCIÓN ==="
            if marker in content:
                content = content.replace(marker, prompt_render_extension + "\n\n" + marker)

        with open(s, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"SUCCESS: Updated Camila System Prompt with Render Sleep Recovery in {s}")
