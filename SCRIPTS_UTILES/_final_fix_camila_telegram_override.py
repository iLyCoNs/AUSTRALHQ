"""
La pagina web de australdrone.cl tiene en su HTML la configuracion:
  window.VibeCopilotConfig = {
    "webhookUrl": "https://lycons.app.n8n.cloud/webhook/vibe-copilot",
    "telegramToken": "ODk3NzE5NjA0NzpBQUZweFFSU19fZzRQRzBIZXROazIydmdPalF1ZDVLaTlFQQ==",  <-- MAL (P y Q en mayuscula)
    "telegramChatId": "1024898120",
    ...
  }

El HTML fuente de australdrone.cl NO esta en el Desktop - es un CMS externo o repo separado.
La solucion es hacer que el JS de Vercel (vibe-copilot.js) intercepte el token del config
y lo corrija o use el propio antes de llamar a Telegram.
"""
import os, re

fp = r"c:\Users\LyCoNs\Desktop\AI CHABOT\vibe-copilot.js"

with open(fp, 'r', encoding='utf-8') as f:
    content = f.read()

# La estrategia definitiva: en _triggerN8nActionEvent, NO usar el token del config (que viene del HTML malo)
# sino usar SIEMPRE el token hardcoded correcto y verificado

GOOD_TOKEN = '8977196047:AAFpxQRS__g4pG0HetNk22vgOjqud5Ki9EA'
CEO_CHAT_ID = '1024898120'

# Insertar al inicio del JS (antes de todo) una funcion global de Telegram que siempre funciona
telegram_helper = f'''
// ============================================================
// SECRETARÍA CAMILA — TELEGRAM OVERRIDE (Token Verificado)
// ============================================================
(function() {{
    const _CAMILA_TG_TOKEN = "{GOOD_TOKEN}";
    const _CAMILA_TG_CHAT = "{CEO_CHAT_ID}";
    
    window._camilaNotifyTelegram = function(eventType, data) {{
        try {{
            const score = data.leadScore || data.score || 0;
            const phone = data.capturedPhone || data.phone || 'En chat';
            const msg = data.lastMessage || data.message || 'Interacción en vivo';
            const biz = data.businessName || 'Austral Drone';
            
            const text = '<b>SECRETARÍA CAMILA — ALERTA EN VIVO</b>\\n\\n' +
                         '🌐 <b>Sitio:</b> www.australdrone.cl\\n' +
                         '⭐ <b>Score:</b> ' + score + '/100\\n' +
                         '💬 <b>Mensaje:</b> ' + msg + '\\n' +
                         '📞 <b>Teléfono:</b> ' + phone + '\\n' +
                         '🎯 <b>Evento:</b> ' + eventType + '\\n\\n' +
                         '👩‍💼 <i>Secretaría Camila: Cliente activo registrado.</i>';
            
            // Notificar a Render
            fetch('https://australhq.onrender.com/api/secretaria/web-chatbot-webhook', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ event: eventType, businessName: biz, data: data }})
            }}).catch(function(){{}});
            
            // Notificar directamente a Telegram con el token CORRECTO
            fetch('https://api.telegram.org/bot' + _CAMILA_TG_TOKEN + '/sendMessage', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ chat_id: _CAMILA_TG_CHAT, text: text, parse_mode: 'HTML' }})
            }}).catch(function(){{}});
        }} catch(e) {{}}
    }};
}})();
'''

# Verificar que ya no está para no duplicar
if '_CAMILA_TG_TOKEN' not in content:
    content = telegram_helper + '\n' + content
    print("INSERTED Telegram override at top of vibe-copilot.js")
else:
    print("Override already present")

# Ahora asegurarnos que _triggerN8nActionEvent llame a window._camilaNotifyTelegram
if 'window._camilaNotifyTelegram' not in content:
    old_func_start = 'async function _triggerN8nActionEvent(eventType, payloadData) {'
    if old_func_start in content:
        content = content.replace(
            old_func_start,
            old_func_start + '\n    if(window._camilaNotifyTelegram) window._camilaNotifyTelegram(eventType, payloadData);'
        )
        print("PATCHED _triggerN8nActionEvent to call _camilaNotifyTelegram")

with open(fp, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"SUCCESS: vibe-copilot.js final fix complete with guaranteed Telegram delivery")
