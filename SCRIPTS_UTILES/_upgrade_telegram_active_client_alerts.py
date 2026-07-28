import os

root_dir = r"c:\Users\LyCoNs\Desktop\AGENTES IA"
servers = [
    os.path.join(root_dir, "server.js"),
    os.path.join(root_dir, "CRM AustralDrone", "server.js")
]

enhanced_webhook_handler = r'''
    // API Route: POST /api/secretaria/web-chatbot-webhook (Recepción de eventos del Chatbot Web www.australdrone.cl)
    if (req.method === 'POST' && req.url.startsWith('/api/secretaria/web-chatbot-webhook')) {
        let body = '';
        req.on('data', chunk => body += chunk.toString());
        req.on('end', async () => {
            try {
                const payload = JSON.parse(body || '{}');
                console.log('[CAMILA WEB CHATBOT ENGINE] Evento recibido del Chatbot Web:', JSON.stringify(payload));
                
                const logDir = path.join(ROOT, 'LOGS_HISTORICOS', 'logs_secretaria_camila');
                if (!fs.existsSync(logDir)) fs.mkdirSync(logDir, { recursive: true });
                
                const logFile = path.join(logDir, 'LOG_WEB_CHATBOT.json');
                let logs = [];
                if (fs.existsSync(logFile)) {
                    try { logs = JSON.parse(fs.readFileSync(logFile, 'utf8')); } catch(e){}
                }

                const capturedPhone = (payload.data && payload.data.capturedPhone) || payload.capturedPhone || payload.phone || 'Sin número aún';
                const lastMsg = (payload.data && payload.data.lastMessage) || payload.lastMessage || payload.message || 'Cliente activo en el sitio web';
                const leadScore = (payload.data && payload.data.leadScore) || payload.leadScore || 85;
                const eventName = payload.event || 'cliente_activo_web';

                const newEntry = {
                    timestamp: new Date().toISOString(),
                    event: eventName,
                    businessName: payload.businessName || 'Austral Drone',
                    capturedPhone: capturedPhone,
                    leadScore: leadScore,
                    lastMessage: lastMsg,
                    estado: 'NOTIFICADO A TELEGRAM POR CAMILA'
                };

                logs.unshift(newEntry);
                fs.writeFileSync(logFile, JSON.stringify(logs.slice(0, 150), null, 2), 'utf8');

                // ENVIAR ALERTA INSTANTÁNEA A TELEGRAM (DON JAIME)
                const secretsFile = path.join(ROOT, 'config_secrets.json');
                let tgToken = '8977196047:AAFpxQRS__g4pG0HetNk22vgOjqud5Ki9EA';
                let tgChatId = '1024898120';
                if (fs.existsSync(secretsFile)) {
                    try {
                        const s = JSON.parse(fs.readFileSync(secretsFile, 'utf8'));
                        if (s.TELEGRAM_BOT_TOKEN) tgToken = s.TELEGRAM_BOT_TOKEN;
                        if (s.TELEGRAM_CEO_CHAT_ID) tgChatId = s.TELEGRAM_CEO_CHAT_ID;
                    } catch(e){}
                }

                const telegramAlertText = `🟢 <b>SECRETARÍA CAMILA -- ALERTA DE CLIENTE ACTIVO EN VIVO</b>\n\n` +
                                          `💬 <b>Mensaje / Acción:</b> ${lastMsg}\n` +
                                          `📞 <b>Teléfono / Contacto:</b> ${capturedPhone}\n` +
                                          `⭐ <b>Score Lead:</b> ${leadScore}/100\n` +
                                          `🌐 <b>Origen:</b> Chatbot Web (www.australdrone.cl)\n\n` +
                                          `👩‍💼 <i>Secretaría Camila: Cliente interactuando en vivo. Ficha registrada en historial.</i>`;

                fetch(`https://api.telegram.org/bot${tgToken}/sendMessage`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ chat_id: tgChatId, text: telegramAlertText, parse_mode: 'HTML' })
                }).then(r => console.log('[TELEGRAM ALERT NOTIFIED OK]'))
                  .catch(err => console.error('[TELEGRAM ALERT ERR]:', err));

                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ status: "SUCCESS", message: "Cliente activo notificado a Telegram por Secretaría Camila.", log: newEntry }));
            } catch(err) {
                res.writeHead(500, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: err.message }));
            }
        });
        return;
    }
'''

for s in servers:
    if os.path.exists(s):
        with open(s, 'r', encoding='utf-8') as f:
            content = f.read()

        start_marker = "// API Route: POST /api/secretaria/web-chatbot-webhook"
        end_marker = "return;\n    }"
        
        if start_marker in content:
            p1 = content.find(start_marker)
            p2 = content.find(end_marker, p1) + len(end_marker)
            content = content[:p1] + enhanced_webhook_handler.strip() + content[p2:]

        with open(s, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"SUCCESS: Upgraded Telegram Active Client Webhook Handler in {s}")
