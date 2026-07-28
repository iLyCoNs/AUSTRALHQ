import os

root_dir = r"c:\Users\LyCoNs\Desktop\AGENTES IA"
servers = [
    os.path.join(root_dir, "server.js"),
    os.path.join(root_dir, "CRM AustralDrone", "server.js")
]

webhook_code = '''
// API Webhook: Recepción de Eventos y Captura de Leads del Chatbot Web www.australdrone.cl (Vercel)
app.post('/api/secretaria/web-chatbot-webhook', async (req, res) => {
    try {
        const payload = req.body || {};
        console.log('[CAMILA WEB CHATBOT ENGINE] Evento recibido del Chatbot Web:', JSON.stringify(payload));
        
        const logDir = path.join(__dirname, 'LOGS_HISTORICOS', 'logs_secretaria_camila');
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
            estado: 'REGISTRADO POR CAMILA'
        };

        logs.unshift(newEntry);
        fs.writeFileSync(logFile, JSON.stringify(logs.slice(0, 100), null, 2), 'utf8');

        // Notificar a Telegram si es derivación o captura de contacto
        const secretsFile = path.join(__dirname, 'config_secrets.json');
        let tgToken = '8977196047:AAFpxQRS__g4pG0HetNk22vgOjqud5Ki9EA';
        let tgChatId = '1024898120';
        if (fs.existsSync(secretsFile)) {
            try {
                const s = JSON.parse(fs.readFileSync(secretsFile, 'utf8'));
                if (s.TELEGRAM_BOT_TOKEN) tgToken = s.TELEGRAM_BOT_TOKEN;
            } catch(e){}
        }

        const msgText = `🌐 <b>SECRETARÍA CAMILA -- CAPTURA CHATBOT WEB</b>\\n\\n` +
                        `📞 <b>Teléfono Capturado:</b> ${newEntry.capturedPhone}\\n` +
                        `⭐ <b>Score Lead:</b> ${newEntry.leadScore}/100\\n` +
                        `💬 <b>Último Mensaje:</b> ${newEntry.lastMessage}\\n\\n` +
                        `👩‍💼 <i>Secretaría Camila: Prospecto registrado en historial y derivado a CEO / Nicole.</i>`;

        fetch(`https://api.telegram.org/bot${tgToken}/sendMessage`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ chat_id: tgChatId, text: msgText, parse_mode: 'HTML' })
        }).catch(err => console.error('[TELEGRAM ERR]:', err));

        return res.json({ status: "SUCCESS", message: "Evento registrado exitosamente por Secretaría Camila.", log: newEntry });
    } catch(err) {
        console.error('[CAMILA WEB CHATBOT ERR]:', err);
        return res.status(500).json({ error: err.message });
    }
});

// API Función: Consultar directamente el Chatbot de Vercel (https://chatbot-ad-mocha.vercel.app/api/chat)
app.post('/api/secretaria/consult-web-chatbot', async (req, res) => {
    try {
        const { mensaje } = req.body || {};
        const response = await fetch('https://chatbot-ad-mocha.vercel.app/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                businessName: 'Austral Drone',
                messages: [ { role: 'user', content: mensaje || 'Hola' } ]
            })
        });
        const data = await response.json();
        return res.json({ status: "OK", text: data.text || '' });
    } catch(err) {
        return res.status(500).json({ error: err.message });
    }
});
'''

for s in servers:
    if os.path.exists(s):
        with open(s, 'r', encoding='utf-8') as f:
            content = f.read()

        if '/api/secretaria/web-chatbot-webhook' not in content:
            content = content.replace("app.listen(", webhook_code + "\napp.listen(")

        with open(s, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"SUCCESS: Integrated Vercel Web Chatbot API into {s}")
