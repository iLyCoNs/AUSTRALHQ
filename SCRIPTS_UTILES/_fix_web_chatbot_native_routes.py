import os

root_dir = r"c:\Users\LyCoNs\Desktop\AGENTES IA"
servers = [
    os.path.join(root_dir, "server.js"),
    os.path.join(root_dir, "CRM AustralDrone", "server.js")
]

native_webhook_route = r'''
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

                const newEntry = {
                    timestamp: new Date().toISOString(),
                    event: payload.event || 'web_chat_interaction',
                    businessName: payload.businessName || 'Austral Drone',
                    capturedPhone: (payload.data && payload.data.capturedPhone) || payload.capturedPhone || 'N/A',
                    leadScore: (payload.data && payload.data.leadScore) || payload.leadScore || 75,
                    lastMessage: (payload.data && payload.data.lastMessage) || payload.lastMessage || 'Interacción en sitio web',
                    estado: 'REGISTRADO POR SECRETARIA CAMILA'
                };

                logs.unshift(newEntry);
                fs.writeFileSync(logFile, JSON.stringify(logs.slice(0, 100), null, 2), 'utf8');

                // Notificar a Telegram
                const secretsFile = path.join(ROOT, 'config_secrets.json');
                let tgToken = '8977196047:AAFpxQRS__g4pG0HetNk22vgOjqud5Ki9EA';
                let tgChatId = '1024898120';
                if (fs.existsSync(secretsFile)) {
                    try {
                        const s = JSON.parse(fs.readFileSync(secretsFile, 'utf8'));
                        if (s.TELEGRAM_BOT_TOKEN) tgToken = s.TELEGRAM_BOT_TOKEN;
                    } catch(e){}
                }

                const msgText = `🌐 <b>SECRETARÍA CAMILA -- CAPTURA CHATBOT WEB</b>\n\n` +
                                `📞 <b>Teléfono Capturado:</b> ${newEntry.capturedPhone}\n` +
                                `⭐ <b>Score Lead:</b> ${newEntry.leadScore}/100\n` +
                                `💬 <b>Detalle:</b> ${newEntry.lastMessage}\n\n` +
                                `👩‍💼 <i>Secretaría Camila: Registrado en historial y derivado a CEO Jaime & Nicole.</i>`;

                fetch(`https://api.telegram.org/bot${tgToken}/sendMessage`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ chat_id: tgChatId, text: msgText, parse_mode: 'HTML' })
                }).catch(err => console.error('[TELEGRAM ERR]:', err));

                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ status: "SUCCESS", message: "Evento registrado exitosamente por Secretaría Camila.", log: newEntry }));
            } catch(err) {
                res.writeHead(500, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: err.message }));
            }
        });
        return;
    }

    // API Route: POST /api/secretaria/consult-web-chatbot (Consulta directa al Chatbot de Vercel)
    if (req.method === 'POST' && req.url.startsWith('/api/secretaria/consult-web-chatbot')) {
        let body = '';
        req.on('data', chunk => body += chunk.toString());
        req.on('end', async () => {
            try {
                const payload = JSON.parse(body || '{}');
                const mensaje = payload.mensaje || 'Hola';
                const response = await fetch('https://chatbot-ad-mocha.vercel.app/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        businessName: 'Austral Drone',
                        messages: [ { role: 'user', content: mensaje } ]
                    })
                });
                const data = await response.json();
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ status: "OK", text: data.text || '' }));
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

        if '/api/secretaria/web-chatbot-webhook' not in content:
            marker = "if (req.method === 'POST' && req.url === '/api/secretaria/chat') {"
            if marker in content:
                content = content.replace(marker, native_webhook_route + "\n    " + marker)

        with open(s, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"SUCCESS: Inserted native HTTP Web Chatbot routes into {s}")
