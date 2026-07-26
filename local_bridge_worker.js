const WebSocket = require('ws');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const https = require('https');

// URL del servidor WebSockets público en Render (o localhost)
const RENDER_WS_URL = process.env.HQ_SERVER_URL || 'wss://australhq.onrender.com';
// URL del webhook n8n cloud para el pipeline de leads
const N8N_WEBHOOK_URL = process.env.N8N_WEBHOOK_URL || 'https://lycons.app.n8n.cloud/webhook/cazador-leads';
const ROOT = __dirname;

// Keep-alive ping a n8n Render para evitar que se duerma la instancia Free
setInterval(() => {
    try {
        https.get('https://n8n-australdrone.onrender.com/', () => {}).on('error', () => {});
    } catch(e) {}
}, 10 * 60 * 1000);

console.log('╔══════════════════════════════════════════════════════════╗');
console.log('║  AustralDrone.CL — Agente Puente de Ejecución Local PC  ║');
console.log('║  Conectando al HQ en la Nube: ' + RENDER_WS_URL.padEnd(25) + '║');
console.log('╚══════════════════════════════════════════════════════════╝');

let ws = null;
let pingInterval = null;

function connectBridge() {
    ws = new WebSocket(RENDER_WS_URL);

    ws.on('open', () => {
        console.log('✅ Conectado al HQ en la nube. Esperando órdenes de Jaime, Nicole o Diego...');
        ws.send(JSON.stringify({ type: 'local_worker_register', status: 'ready', pc: 'PC-LOCAL-JAIME' }));

        // Keepalive Heartbeat cada 20s para mantener el WebSocket activo sin desconexiones
        clearInterval(pingInterval);
        pingInterval = setInterval(() => {
            if (ws && ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({ type: 'ping' }));
            }
        }, 20000);
    });

    ws.on('message', (message) => {
        try {
            const data = JSON.parse(message.toString());
            if (data.type === 'trigger_local_agent') {
                const agentId = data.agent || 'cazador360';
                console.log(`⚡ Orden recibida desde la web HQ: Ejecutar Agente ${agentId}`);
                runLocalScript(agentId);
            } else if (data.type === 'trigger_filter') {
                console.log('⚡ Orden recibida: Ejecutar Filtro Analista');
                runLocalScript('filtro_analista');
            }
        } catch (e) {
            console.warn('Err mensaje WS:', e.message);
        }
    });

    ws.on('close', () => {
        clearInterval(pingInterval);
        console.log('⚠️ Conexión perdida con el HQ. Reintentando en 5s...');
        setTimeout(connectBridge, 5000);
    });

    ws.on('error', (e) => {
        console.warn('WS Err:', e.message);
    });
}

function runLocalScript(agentId) {
    const scriptMap = {
        'cazador360': 'cazador_360_vendedores.py',
        'cazadorventas': 'cazador_facebook.py',
        'yapo': 'yapo_scanner.py',
        'troya': 'core/agente_14_caballo_troya.py',
        'filtro_analista': 'agente_filtro_leads.py'
    };

    const script = scriptMap[agentId] || 'cazador_360_vendedores.py';
    const scriptPath = path.join(ROOT, script);
    const isCazador = agentId === 'cazador360';

    console.log(`🚀 Ejecutando en tu PC: py ${script}`);

    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: 'agent_status', agent: agentId, state: 'working', msg: `Ejecutando ${script} en PC local...` }));
    }

    let pyProc = spawn('py', [scriptPath], { cwd: ROOT });

    pyProc.on('error', (err) => {
        console.warn('⚠️ Falló py launcher, reintentando con python...', err.message);
        pyProc = spawn('python', [scriptPath], { cwd: ROOT });
        bindProcEvents(pyProc, agentId, isCazador);
    });

    bindProcEvents(pyProc, agentId, isCazador);
}

function bindProcEvents(pyProc, agentId, autoTriggerFilter=false) {
    pyProc.stdout.on('data', (d) => {
        const line = d.toString().trim();
        console.log(`[Py Log]: ${line}`);
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({ type: 'agent_log', agent: agentId, msg: line.substring(0, 90) }));
        }
    });

    pyProc.stderr.on('data', (d) => {
        console.warn(`[Py Err]:`, d.toString().trim());
    });

    pyProc.on('close', (code) => {
        console.log(`✅ Agente ${agentId} finalizado (código: ${code}).`);
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({ type: 'agent_status', agent: agentId, state: 'lead', msg: `¡${agentId} completado! Código: ${code}` }));
        }
        // ══ CICLO AUTÓNOMO: Si termina el Cazador 360, lanza automáticamente el Filtro Analista
        if (autoTriggerFilter && code === 0) {
            console.log('🔄 Ciclo Autónomo: Cazador completado → lanzando Filtro Analista...');
            setTimeout(() => {
                if (ws && ws.readyState === WebSocket.OPEN) {
                    ws.send(JSON.stringify({ type: 'agent_status', agent: 'filtro_analista', state: 'working', msg: '🔄 Ciclo autónomo: analizando CSV del Cazador...' }));
                }
                runLocalScript('filtro_analista');
            }, 3000); // Esperar 3s para que se guarden todos los archivos
        }
        // Si es el filtro analista, intentar enviar resultados a n8n cloud
        if (agentId === 'filtro_analista') {
            setTimeout(() => sendLeadsToN8N(), 2000);
        }
    });
}

// ══ Enviar TOP leads a n8n cloud después del filtro
function sendLeadsToN8N() {
    const reportDir = path.join(ROOT, 'REPORTES_AGENTES', 'FILTRO_ANALISTA');
    if (!fs.existsSync(reportDir)) return;
    // Leer el reporte más reciente
    const files = fs.readdirSync(reportDir).filter(f => f.endsWith('.json')).sort().reverse();
    if (!files.length) { console.warn('[N8N] No hay reporte del Filtro para enviar.'); return; }
    const latestFile = path.join(reportDir, files[0]);
    let report;
    try {
        report = JSON.parse(fs.readFileSync(latestFile, 'utf-8'));
    } catch(e) { console.warn('[N8N] Error leyendo reporte:', e.message); return; }

    const payload = JSON.stringify(report.resultado || report);
    const url = new URL(N8N_WEBHOOK_URL);
    const options = {
        hostname: url.hostname,
        port: url.port || 443,
        path: url.pathname,
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(payload)
        }
    };
    console.log(`[N8N] Enviando ${report.resultado?.total_calificados || '?'} leads a n8n cloud...`);
    const req = https.request(options, (res) => {
        let body = '';
        res.on('data', d => body += d);
        res.on('end', () => console.log(`[N8N] Respuesta: ${res.statusCode} — ${body.substring(0, 100)}`));
    });
    req.on('error', (e) => console.warn('[N8N] Error enviando a n8n:', e.message));
    req.setTimeout(10000, () => { req.destroy(); console.warn('[N8N] Timeout enviando a n8n.'); });
    req.write(payload);
    req.end();
}

connectBridge();
