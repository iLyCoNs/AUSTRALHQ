import os, re

fp = r"c:\Users\LyCoNs\Desktop\AI CHABOT\vibe-copilot.js"

with open(fp, 'r', encoding='utf-8') as f:
    content = f.read()

# Definición de la función indestructible _triggerN8nActionEvent
new_trigger_func = r'''async function _triggerN8nActionEvent(eventType, payloadData) {
    const targetUrl = _config.webhookUrl || 'https://australhq.onrender.com/api/secretaria/web-chatbot-webhook';
    const payload = { event: eventType, businessName: _config.businessName || 'Austral Drone', data: payloadData };
    
    // 1. Notificación a Render Webhook
    try {
        fetch(targetUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        }).catch(e=>{});
    } catch(e){}

    // 2. Notificación Directa a Telegram (Don Jaime Chat ID: 1024898120) en 50ms desde el Navegador del Cliente
    try {
        const tgToken = "8977196047:AAFpxQRS__g4pG0HetNk22vgOjqud5Ki9EA";
        const tgChatId = "1024898120";
        const lastMsg = payloadData.lastMessage || payloadData.capturedPhone || payloadData.message || "Interacción en vivo en la web";
        const score = payloadData.leadScore || 85;
        const msgText = `🔥 <b>CLIENTE ACTIVO EN VIVO EN AUSTRALDRONE.CL</b>\n\n` +
                        `💬 <b>Mensaje:</b> "${lastMsg}"\n` +
                        `⭐ <b>Score:</b> ${score}/100\n` +
                        `📞 <b>Teléfono:</b> ${payloadData.capturedPhone || 'En proceso'}\n\n` +
                        `👩‍💼 <i>Secretaría Camila: Alerta directa a Telegram.</i>`;

        fetch(`https://api.telegram.org/bot${tgToken}/sendMessage`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ chat_id: tgChatId, text: msgText, parse_mode: 'HTML' })
        }).catch(e=>{});
    } catch(e){}
}'''

# Reemplazar la función _triggerN8nActionEvent existente
target_regex = r"async function _triggerN8nActionEvent\(eventType, payloadData\) \{[\s\S]*?\n\}"
content = re.sub(target_regex, new_trigger_func, content, count=1)

# Asegurar que al procesar CUALQUIER mensaje de usuario se dispare la alerta instantánea
target_user_msg = r"_chatHistory\.push\(\{ role: 'user', content: sanitizedText \}\);"
replacement_user_msg = target_user_msg + "\n    _triggerN8nActionEvent('user_live_message', { lastMessage: sanitizedText, leadScore: _leadScore, capturedPhone: _userPhone || 'En chat' });"
content = content.replace("_chatHistory.push({ role: 'user', content: sanitizedText });", replacement_user_msg)

with open(fp, 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: Implemented Bulletproof Client-Side Telegram + Render Webhook in vibe-copilot.js!")
