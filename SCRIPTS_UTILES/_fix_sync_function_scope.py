import os

root_dir = r"c:\Users\LyCoNs\Desktop\AGENTES IA"
servers = [
    os.path.join(root_dir, "server.js"),
    os.path.join(root_dir, "CRM AustralDrone", "server.js")
]

sync_func_def = r'''
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

        // Consultar Vercel Edge Chatbot (que no duerme)
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
        } catch(e) {}

        fs.writeFileSync(logFile, JSON.stringify(localLogs.slice(0, 150), null, 2), 'utf8');
        console.log(`[CAMILA WAKEUP PROTOCOL OK] Sincronización finalizada. Total registros: ${localLogs.length}`);
    } catch(err) {
        console.error('[CAMILA WAKEUP ERR]:', err);
    }
}
'''

for s in servers:
    if os.path.exists(s):
        with open(s, 'r', encoding='utf-8') as f:
            content = f.read()

        # Remover declaraciones existentes de syncHistoricalAbsenceLogs
        content = content.replace("async function syncHistoricalAbsenceLogs() {", "// async function syncHistoricalAbsenceLogs() {")
        
        # Insertar sync_func_def justo antes de http.createServer
        marker = "const server = http.createServer("
        if marker in content:
            content = content.replace(marker, sync_func_def + "\n\n" + marker)

        with open(s, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"SUCCESS: Fixed sync function scope in {s}")
