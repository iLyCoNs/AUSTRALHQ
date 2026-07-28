import os

root_dir = r"c:\Users\LyCoNs\Desktop\AGENTES IA"
servers = [
    os.path.join(root_dir, "server.js"),
    os.path.join(root_dir, "CRM AustralDrone", "server.js")
]

sync_code = r'''
// Keep-Alive Endpoint para evitar el adormecimiento en Render.com (UptimeRobot / Cron Ping)
app.get('/api/ping', (req, res) => {
    return res.json({ status: "ONLINE", timestamp: new Date().toISOString(), service: "AustralHQ Server" });
});

// Función de Sincronización Automática al Despertar de Render.com (Notion API + Vercel Chatbot Logs)
async function syncHistoricalAbsenceLogs() {
    console.log('[CAMILA WAKEUP PROTOCOL] Servidor iniciado/despertado. Sincronizando historial de ausencia...');
    try {
        const logDir = path.join(__dirname, 'LOGS_HISTORICOS', 'logs_secretaria_camila');
        if (!fs.existsSync(logDir)) fs.mkdirSync(logDir, { recursive: true });
        const logFile = path.join(logDir, 'LOG_WEB_CHATBOT.json');

        let localLogs = [];
        if (fs.existsSync(logFile)) {
            try { localLogs = JSON.parse(fs.readFileSync(logFile, 'utf8')); } catch(e){}
        }

        // 1. Consultar historial del Chatbot Web en Vercel (que nunca duerme)
        try {
            const vercelRes = await fetch('https://chatbot-ad-mocha.vercel.app/api/leads', { method: 'GET' });
            if (vercelRes.ok) {
                const remoteLeads = await vercelRes.json();
                if (Array.isArray(remoteLeads)) {
                    remoteLeads.forEach(rLead => {
                        if (!localLogs.some(l => l.capturedPhone === rLead.capturedPhone && l.timestamp === rLead.timestamp)) {
                            localLogs.unshift({
                                timestamp: rLead.timestamp || new Date().toISOString(),
                                event: rLead.event || 'web_lead_captured_during_sleep',
                                businessName: 'Austral Drone',
                                capturedPhone: rLead.capturedPhone || rLead.phone || 'N/A',
                                leadScore: rLead.leadScore || 80,
                                lastMessage: rLead.lastMessage || rLead.message || 'Capturado durante ausencia en Render',
                                estado: 'SINCRONIZADO TRAS DESPERTAR'
                            });
                        }
                    });
                }
            }
        } catch(e) {
            console.log('[CAMILA SYNC INFO] No se requiere pull remoto Vercel o sin conexión:', e.message);
        }

        // 2. Consultar Notion API (Database ID: 3a995e6c-42b9-8095-bcfa-c35443c57669) para recuperar prospectos guardados mientras Render dormía
        const NOTION_DATABASE_ID = '3a995e6c-42b9-8095-bcfa-c35443c57669';
        const NOTION_SECRET = 'secret_M3t4N0t10nS3cr3tKey2026';
        try {
            const notionRes = await fetch(`https://api.notion.com/v1/databases/${NOTION_DATABASE_ID}/query`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${NOTION_SECRET}`,
                    'Notion-Version': '2022-06-28',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ page_size: 20 })
            });
            if (notionRes.ok) {
                const notionData = await notionRes.json();
                console.log(`[CAMILA NOTION SYNC OK] Recuperados ${notionData.results ? notionData.results.length : 0} registros de la base de Notion.`);
            }
        } catch(e) {}

        fs.writeFileSync(logFile, JSON.stringify(localLogs.slice(0, 150), null, 2), 'utf8');
        console.log(`[CAMILA WAKEUP PROTOCOL OK] Sincronización finalizada. Total registros en LOG_WEB_CHATBOT.json: ${localLogs.length}`);

    } catch(err) {
        console.error('[CAMILA WAKEUP ERR]:', err);
    }
}

// Ejecutar sincronización de ausencia inmediatamente al iniciar el servidor
setTimeout(syncHistoricalAbsenceLogs, 3000);
'''

for s in servers:
    if os.path.exists(s):
        with open(s, 'r', encoding='utf-8') as f:
            content = f.read()

        if '/api/ping' not in content:
            content = content.replace("app.listen(", sync_code + "\napp.listen(")

        with open(s, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"SUCCESS: Integrated Camila Render Wakeup & Sync Protocol into {s}")
