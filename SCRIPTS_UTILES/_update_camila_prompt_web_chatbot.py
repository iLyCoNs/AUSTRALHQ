import os

root_dir = r"c:\Users\LyCoNs\Desktop\AGENTES IA"
servers = [
    os.path.join(root_dir, "server.js"),
    os.path.join(root_dir, "CRM AustralDrone", "server.js")
]

prompt_web_chatbot_extension = r'''
5. CONTROL Y SEGUIMIENTO DEL CHATBOT WEB (www.australdrone.cl / chatbot-ad-mocha.vercel.app):
   • Conectada 100% en tiempo real con el Chatbot Web de la empresa (chatbot-ad-mocha.vercel.app/api/chat).
   • Monitoreas todas las interacciones de los clientes en la página web.
   • Cuando un cliente interactúa con el Chatbot y entrega su teléfono (+56 9 ...) o es derivado para agendar una cita con Don Jaime o Nicole, registras la captura en LOGS_HISTORICOS/logs_secretaria_camila/LOG_WEB_CHATBOT.json, le asignas un Lead Score (ej: 75/100 o 95/100) y notificas de inmediato a Telegram.
   • Puedes consultar al Chatbot Web en cualquier momento a través de la función consultarChatbotDesdeSecretaria(mensaje).'''

for s in servers:
    if os.path.exists(s):
        with open(s, 'r', encoding='utf-8') as f:
            content = f.read()

        if "5. CONTROL Y SEGUIMIENTO DEL CHATBOT WEB" not in content:
            marker = "4. SUITE DE PLATAFORMAS & HERRAMIENTAS:"
            if marker in content:
                content = content.replace(marker, prompt_web_chatbot_extension + "\n" + marker)

        with open(s, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"SUCCESS: Updated Camila System Prompt with Web Chatbot awareness in {s}")
