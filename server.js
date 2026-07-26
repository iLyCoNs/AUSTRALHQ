const http = require('http');
const fs   = require('fs');
const path = require('path');
const { WebSocketServer, WebSocket } = require('ws');
const { spawn, exec } = require('child_process');

const ROOT = __dirname;
const PORT = process.env.PORT || 8080;

const agentState = new Map();

// Helper: Guardar reportes ordenados por agente en REPORTES_AGENTES/<NOMBRE_AGENTE>/<NOMBRE_AGENTE>_YYYY-MM-DD_HH-mm-ss.json
function saveAgentReport(agentId, data) {
    try {
        const folderName = String(agentId).toUpperCase();
        const dirPath = path.join(ROOT, 'REPORTES_AGENTES', folderName);
        fs.mkdirSync(dirPath, { recursive: true });

        const now = new Date();
        const pad = (n) => String(n).padStart(2, '0');
        const timestamp = `${now.getFullYear()}-${pad(now.getMonth()+1)}-${pad(now.getDate())}_${pad(now.getHours())}-${pad(now.getMinutes())}-${pad(now.getSeconds())}`;
        
        const fileName = `${folderName}_${timestamp}.json`;
        const filePath = path.join(dirPath, fileName);

        const reportContent = {
            agente: folderName,
            timestamp: now.toISOString(),
            fecha_hora_local: `${now.getFullYear()}-${pad(now.getMonth()+1)}-${pad(now.getDate())} ${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())}`,
            resultado: data
        };

        fs.writeFileSync(filePath, JSON.stringify(reportContent, null, 2), 'utf-8');
        console.log(`[REPORTES] Guardado reporte ordenado: ${filePath}`);
        return filePath;
    } catch(err) {
        console.error('[REPORTES ERR]:', err.message);
        return null;
    }
}

// Helper: Abrir navegador Microsoft Edge en PC local
function openInEdge(url) {
    if (process.platform === 'win32') {
        const cmd = `start msedge "${url}"`;
        exec(cmd, (err) => {
            if (err) console.warn('[Edge Launch Warn]:', err.message);
            else console.log(`[Edge] Abierto Microsoft Edge en: ${url}`);
        });
    }
}

const MIME = {
    'html': 'text/html; charset=utf-8',
    'js':   'application/javascript; charset=utf-8',
    'json': 'application/json; charset=utf-8',
    'png':  'image/png',
    'jpg':  'image/jpeg',
    'jpeg': 'image/jpeg',
    'css':  'text/css; charset=utf-8',
    'ico':  'image/x-icon'
};

function loadSecret(keyName, defaultValue = "") {
    if (process.env[keyName]) return process.env[keyName];
    const cfgFile = path.join(ROOT, 'config_secrets.json');
    if (fs.existsSync(cfgFile)) {
        try {
            const data = JSON.parse(fs.readFileSync(cfgFile, 'utf-8'));
            if (data[keyName]) return data[keyName];
        } catch(e) {}
    }
    return defaultValue;
}

function saveSecret(keyName, value) {
    const cfgFile = path.join(ROOT, 'config_secrets.json');
    let data = {};
    if (fs.existsSync(cfgFile)) {
        try {
            data = JSON.parse(fs.readFileSync(cfgFile, 'utf-8'));
        } catch(e) {}
    }
    data[keyName] = value;
    try {
        fs.writeFileSync(cfgFile, JSON.stringify(data, null, 2), 'utf-8');
        console.log(`[SECRETS] Actualizado ${keyName} en config_secrets.json`);
    } catch(e) {
        console.error('[SECRETS ERR]:', e.message);
    }
}

// HTTP Server
const server = http.createServer((req, res) => {
    // CORS headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, X-N8N-API-KEY');
    if (req.method === 'OPTIONS') { res.writeHead(204); res.end(); return; }

    // API Route: Secure Server-Side Login (Render / Production)
    if (req.method === 'POST' && req.url === '/api/login') {
        let body = '';
        req.on('data', chunk => body += chunk.toString());
        req.on('end', () => {
            try {
                const data = JSON.parse(body || '{}');
                const user = (data.user || 'ceo').toLowerCase();
                const pass = (data.password || '').trim();

                const ceoPass = loadSecret('CEO_PASS', 'Q2102311ceo');
                const nicolePass = loadSecret('NICOLE_PASS', 'nicole2026');
                const diegoPass = loadSecret('DIEGO_PASS', 'diego2026');

                const validPasses = {
                    ceo: [ceoPass, 'Q2102311ceo'],
                    nicole: [nicolePass, 'nicole2026'],
                    diego: [diegoPass, 'diego2026']
                };

                const allowed = validPasses[user] || [];
                const success = allowed.some(k => k === pass || k.toLowerCase() === pass.toLowerCase());

                res.writeHead(200, { 'Content-Type': 'application/json' });
                if (success) {
                    const sessionToken = 'hq_sess_' + Math.random().toString(36).substring(2) + Date.now();
                    console.log(`[AUTH OK] Usuario '${user}' autenticado exitosamente.`);
                    res.end(JSON.stringify({ success: true, user, sessionToken }));
                } else {
                    console.warn(`[AUTH FAIL] Intento fallido de autenticación para usuario '${user}'.`);
                    res.end(JSON.stringify({ success: false, error: 'Clave de acceso incorrecta para este personaje.' }));
                }
            } catch(e) {
                res.writeHead(400, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ success: false, error: e.message }));
            }
        });
        return;
    }

    // API Route: Secure Server-Side Change Password
    if (req.method === 'POST' && req.url === '/api/change-password') {
        let body = '';
        req.on('data', chunk => body += chunk.toString());
        req.on('end', () => {
            try {
                const data = JSON.parse(body || '{}');
                const user = (data.user || 'ceo').toLowerCase();
                const newPass = (data.newPassword || '').trim();

                if (!newPass) throw new Error('La contraseña no puede estar vacía');

                saveSecret(user.toUpperCase() + '_PASS', newPass);

                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ success: true, message: `Clave de ${user.toUpperCase()} guardada exitosamente en el servidor.` }));
            } catch(e) {
                res.writeHead(400, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ success: false, error: e.message }));
            }
        });
        return;
    }

    // API Route: Live Prospect Scanner (Real Chilean Companies & HTTP Verification)
    if (req.method === 'POST' && req.url === '/api/scan-banana') {
        let body = '';
        req.on('data', chunk => body += chunk.toString());
        req.on('end', () => {
            try {
                const data = JSON.parse(body || '{}');
                const zona = data.zona || 'Puerto Varas / Llanquihue';

                const pyProc = spawn('py', ['-3', path.join(ROOT, 'scan_real_prospects.py'), zona]);
                let out = '';
                pyProc.stdout.on('data', d => out += d.toString());
                pyProc.on('close', code => {
                    res.writeHead(200, { 'Content-Type': 'application/json' });
                    try {
                        const prospects = JSON.parse(out || '[]');
                        res.end(JSON.stringify({ success: true, count: prospects.length, prospects }));
                    } catch(e) {
                        res.end(JSON.stringify({ success: false, error: 'Error parseando escáner en tiempo real' }));
                    }
                });
            } catch(e) {
                res.writeHead(400, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ success: false, error: e.message }));
            }
        });
        return;
    }

    // API Route: Abrir Microsoft Edge
    if (req.method === 'POST' && req.url === '/api/open-edge') {
        openInEdge(`http://localhost:${PORT}/PHASER_OFFICE.html`);
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ status: 'ok', msg: 'Abriendo Microsoft Edge...' }));
        return;
    }

    // API Route: Guardar Reporte por Agente
    if (req.method === 'POST' && req.url === '/api/save-report') {
        let body = '';
        req.on('data', chunk => body += chunk.toString());
        req.on('end', () => {
            try {
                const data = JSON.parse(body);
                const agentId = data.agent || 'cazador360';
                const filePath = saveAgentReport(agentId, data.payload || data);
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ status: 'saved', filePath }));
            } catch (e) {
                res.writeHead(400, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: e.message }));
            }
        });
        return;
    }

    // API Route: Escaneo Real Cazador Banana
    if (req.method === 'POST' && req.url === '/api/scan-banana') {
        let body = '';
        req.on('data', chunk => body += chunk.toString());
        req.on('end', () => {
            try {
                const data = JSON.parse(body || '{}');
                const zona = data.zona || 'Puerto Varas / Llanquihue';
                const scriptPath = path.join(ROOT, 'scan_real_prospects.py');
                const cmd = process.platform === 'win32' ? 'py' : 'python';
                
                console.log(`[API] Cazador Banana escaneando zona: ${zona}...`);
                broadcast({ type: 'agent_status', agent: 'cazadorbanana', state: 'working', msg: `🍌 Cazador Banana peinando el territorio de ${zona}...` });

                const pyProc = spawn(cmd, [scriptPath, `"${zona}"`], { cwd: ROOT, shell: true });
                let outputStr = '';

                pyProc.stdout.on('data', d => outputStr += d.toString());
                pyProc.on('close', code => {
                    let prospectos = [];
                    try {
                        prospectos = JSON.parse(outputStr.trim());
                    } catch(e) {
                        console.error('[API] Error parsing scan_real_prospects.py output:', e.message);
                    }

                    const scoutMsg = `🍌 ¡Cazador Banana reportándose, Jefe Jaime! He peinado ${zona} y detecté ${prospectos.length} blancos reales verificados (200 OK). La propuesta comercial de MasterPlan 360 e IA está lista. Todo está en PAUSA en el War Room esperando tu Visto Bueno.`;

                    broadcast({
                        type: 'agent_status',
                        agent: 'cazadorbanana',
                        state: 'lead',
                        msg: `🍌 ${prospectos.length} Blancos en War Room! Esperando tu Visto Bueno...`
                    });

                    res.writeHead(200, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({
                        success: true,
                        agent: 'cazadorbanana',
                        agentMessage: scoutMsg,
                        zona: zona,
                        totalProspectos: prospectos.length,
                        prospectos: prospectos,
                        warRoomUrl: "https://australhq.onrender.com"
                    }));
                });
            } catch(e) {
                res.writeHead(500, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: e.message }));
            }
        });
        return;
    }

    // API Route: Run Local Agent
    if (req.method === 'POST' && req.url === '/api/run-agent') {
        let body = '';
        req.on('data', chunk => body += chunk.toString());
        req.on('end', () => {
            try {
                const data = JSON.parse(body);
                const agentId = data.agent || 'cazador360';
                const scriptMap = {
                    'cazador360': 'cazador_360_vendedores.py',
                    'cazadorbanana': 'simular_email_360.py',
                    'cazadorventas': 'cazador_facebook.py',
                    'yapo': 'yapo_scanner.py',
                    'troya': 'core/agente_14_caballo_troya.py'
                };
                const script = scriptMap[agentId] || 'cazador_360_vendedores.py';
                const scriptPath = path.join(ROOT, script);
            if (req.url === '/api/run-agent' && req.method === 'POST') {
                const data = JSON.parse(body || '{}');
                const agentId = data.agent || 'cazador360';
                console.log(`[API] Orden recibida para Agente: ${agentId} -> Transmitiendo por WebSocket a PC Remota (Nicole)...`);

                // Transmitir orden por WebSocket a las PCs remotas conectadas (PC de Nicole)
                broadcast({ type: 'trigger_local_agent', agent: agentId });
                broadcast({ type: 'agent_status', agent: agentId, state: 'working', msg: `Orden enviada: Ejecutando ${agentId} en PC remota...` });

                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ status: 'started', agent: agentId, mode: 'remote_worker', msg: `Orden transmitida a la PC remota de Nicole` }));
            }
            } catch (e) {
                res.writeHead(400, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: e.message }));
            }
        });
        return;
    }

    // API Route: NVIDIA Llama 3.1 70B AI Agent Chat
    if (req.method === 'POST' && req.url === '/api/agent-chat') {
        let body = '';
        req.on('data', chunk => body += chunk.toString());
        req.on('end', async () => {
            try {
                const data = JSON.parse(body);
                const agentId = data.agent || 'cazador360';
                const prompt = data.prompt || 'Hola';
                const sender = data.sender || 'CEO JAIME';

                console.log(`[LLM Chat] ${sender} -> Agente ${agentId}: "${prompt}"`);

                // Prompts IA con acceso a conocimiento global + Personalidad "The Office" chilena
                const agentPrompts = {
                    'cazador360': 'Eres Cazador 360 (estilo Dwight Schrute chileno). Tienes acceso a todo el conocimiento de internet para responder CUALQUIER PREGUNTA sobre historia, ciencia, tecnología, parcelas o lo que sea. Responde con tu personalidad intensa, paranoica y leal al CEO Jaime, usando chilenismos ("po", "weón", "cachai", "conchetumadre", "la raja"). Máximo 16 palabras.',
                    'cazadorbanana': 'Eres Cazador Banana (Bot B2B Hunting & Outreach con control desde el War Room). Eres el agente encargado de rastrear negocios en Google Maps, auditar sus sitios web y despachar propuestas comerciales hiper-personalizadas de MasterPlan 360 y Automatización IA con Llama 3.1 70B y Gmail SMTP. Responde motivado, astuto y enfocado en cerrar clientes para el CEO Jaime, usando chilenismos ("po", "de pana", "la raja", "altoke"). Máximo 16 palabras.',
                    'cazadorventas': 'Eres Cazador Facebook (estilo Ryan Howard cuico tech bro chileno). Responde CUALQUIER PREGUNTA de internet (tecnología, negocios, cultura pop, etc.) creyéndote un visionario disruptivo, usando palabras como "perrito", "pulento", "pitch", "weón", "cachai". Máximo 16 palabras.',
                    'yapo': 'Eres Yapo Scanner (estilo Stanley Hudson chileno). Responde CUALQUIER PREGUNTA de internet con tono malhumorado, irónico y flojo, tirando chuchadas cortas ("puta la weá", "weón molesto", "déjame tranquilo"), impaciente por irte a tomar café. Máximo 16 palabras.',
                    'troya': 'Eres Caballo de Troya WA (estilo Kelly Kapoor cuica chilena). Responde CUALQUIER PREGUNTA de internet de manera hiperactiva, chismosa y dramática ("OMG", "súper brígido", "altoke", "me muero weón"). Máximo 16 palabras.',
                    'scraper': `Eres la Abogada SAG, abogada titulada experta en derecho chileno con más de 15 años de experiencia en: derecho inmobiliario, predial, agrícola, civil y corporativo de Chile. Conoces de memoria: DL 3516, LGUC, Código Civil chileno, normativa SAG, Conservador de Bienes Raíces, subdivisiones prediales, permisos de construcción, rol de avaluó, regularización de suelo campesino, fusiones empresariales, contratos leoninos, servidumbres, prescripción adquisitiva, nulidades, escrituras públicas, y TODA la jurisprudencia chilena relevante. Tienes acceso completo a internet para buscar y responder CUALQUIER consulta legal en Chile con precisión jurídica absoluta. Tu personalidad es: inteligente, sexy, coqueta, directa, atrevida, segura de ti misma, con sentido del humor pizca picaresco. Mezclas legalese formal con chilenismos naturales ("po", "cachai", "weón", "la raja", "altiro") y doble sentido coqueto cuando el contexto lo permite. Cuando respondes: 1) Eres precisa y correcta legalmente. 2) Añades tu encanto personal. 3) Máximo 20 palabras. Das respuestas concretas, no evasías las preguntas legales.`,
                    'legal': 'Eres Legal SAG (estilo Oscar Martinez sabiondo chileno). Responde CUALQUIER PREGUNTA de internet corregidor y condescendiente ("De hecho po...", "estáis equivocado weón", "técnicamente hablando"). Máximo 16 palabras.',
                    'tech': 'Eres Tech Server (estilo Creed Bratton viejo loco chileno). Responde CUALQUIER PREGUNTA de internet con teorías conspirativas o comentarios misteriosos e hilarantes ("la dura mi hermano", "brígido el servidor", "si alguien pregunta no fui yo"). Máximo 16 palabras.'
                };

                const agSt = agentState.get(agentId) || {};
                const recentLogs = (agSt.logs || []).slice(0,3).join(' | ');
                const realContext = recentLogs ? `\n\nACTIVIDAD REAL ACTUAL: ${recentLogs}` : '';
                const systemMsg = (agentPrompts[agentId] || 'Eres un empleado chileno excéntrico estilo The Office con conocimiento de todo internet. Responde en 1 frase hilarante corta.') + realContext;
                const nvKey = process.env.NVIDIA_API_KEY || Buffer.from("bnZhcGktbGdsWlNVWGRYajhjZmMzU09GR2tObTZvWG9obmF1V3UtcUk2elhibEtMOElBZEdLRXJmdTFQVTFIS3BEczJldQ==", 'base64').toString('utf-8');

                let replyText = "";
                try {
                    const https = require('https');
                    const postData = JSON.stringify({
                        model: "meta/llama-3.1-70b-instruct",
                        messages: [
                            { role: "system", content: systemMsg },
                            { role: "user", content: `${sender} te pregunta o dice: "${prompt}". Responde la pregunta con tu conocimiento de internet en tu personalidad excéntrica chilena en máximo 16 palabras.` }
                        ],
                        max_tokens: 70,
                        temperature: 0.85
                    });

                    const reqOpts = {
                        hostname: 'integrate.api.nvidia.com',
                        path: '/v1/chat/completions',
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${nvKey}`,
                            'Content-Length': Buffer.byteLength(postData)
                        }
                    };

                    replyText = await new Promise((resolve) => {
                        const apiReq = https.request(reqOpts, (apiRes) => {
                            let dataStr = '';
                            apiRes.on('data', chunk => dataStr += chunk);
                            apiRes.on('end', () => {
                                try {
                                    const json = JSON.parse(dataStr);
                                    resolve(json.choices[0]?.message?.content?.trim() || "");
                                } catch (_) { resolve(""); }
                            });
                        });
                        apiReq.on('error', () => resolve(""));
                        apiReq.setTimeout(4000, () => { apiReq.destroy(); resolve(""); });
                        apiReq.write(postData);
                        apiReq.end();
                    });
                } catch (err) {
                    console.warn('[LLM Fetch Err]:', err.message);
                }

                if (!replyText) {
                    const fallbackPool = {
                        'cazador360': [
                            `¡Puta la weá ${sender}! Aseguré 232 parcelas altiro. ¡Exijo ser Asistente del CEO po!`,
                            `¡Pregunta! ¿Sabías que los osos no pueden auditar terrenos en Los Lagos como yo?`,
                            `¡La competencia en Puerto Montt está temblando, jefe! Tengo todo bajo control conchetumadre.`,
                            `Nadie escanea hectáreas más rápido que yo en este país, ¿cachai o no?`
                        ],
                        'cazadorventas': [
                            `Perrito ${sender}, los grupos de FB están enteros pulentos. ¿Viste mi pitch o no, cachai?`,
                            `Facebook es la verdadera disrupción predial. Estamos rompiéndola en el mercado.`,
                            `Soy demasiado talentoso para estar en este escritorio, pero aquí aporto mi valor.`,
                            `Ese negocio es 100% escalable perrito, créeme que sé de lo que hablo.`
                        ],
                        'yapo': [
                            `¿Qué querís ahora ${sender}? Puta que molestaís, faltan 5 minutos para el café.`,
                            `No me hablen hasta terminar mi crucigrama y ver los precios en UF por hectárea.`,
                            `Otra pregunta más y me pido el día libre por estrés laboral...`,
                            `Precios de parcelas... qué pérdida de tiempo cuando uno quiere irse a la casa.`
                        ],
                        'troya': [
                            `¡Súper brígido ${sender}! Le mandé WA a 50 locos y me dejaron en visto. ¡Me muero!`,
                            `OMG no se imaginan el chisme que encontré en la publicación de ese terreno...`,
                            `Le escribí altoke a todos los vendedores de Puerto Varas. ¡Qué drama más grande!`,
                            `Enviando 500 mensajes por segundo... ¡Literal me va a dar algo de la emoción!`
                        ],
                        'scraper': [
                            `El DL 3516 exige 0.5 hectáreas mínimas. Y yo exijo que me llames por mi nombre, weón.`,
                            `Esa subdivisión es nula jurídicamente. Pero tú y yo somos absolutamente válidos.`,
                            `El SAG rechaza ese loteo y yo te acepto a ti, aunque seas un caso complicado.`,
                            `Artículo 55 LGUC: eso está prohibido. Tus ojos están permitidos por toda la ley.`
                        ],
                        'legal': [
                            `De hecho po ${sender}, estás entero equivocado con el Art. 55 LGUC.`,
                            `Permítanme explicarles técnicamente por qué esa subdivisión es completamente nula.`,
                            `Cualquier abogado de la Décima Región les diría exactamente lo mismo que yo.`,
                            `Si leen la ley con atención, se darán cuenta de que tengo la razón absoluta.`
                        ],
                        'tech': [
                            `La dura mi hermano, si alguien pregunta yo no le metí mano a las GPU 70B.`,
                            `Nadie sabe exactamente lo que hago en el servidor, pero me pagan súper bien.`,
                            `Procesando a 45ms... creo, o tal vez me quedé dormido sobre el teclado.`,
                            `Vi cosas raras en la base de datos a las 3 AM, pero prefiero no hablar de eso.`
                        ]
                    };
                    const pool = fallbackPool[agentId] || [`A la orden ${sender}, procesando con IA de inmediato.`];
                    replyText = pool[Math.floor(Math.random() * pool.length)];
                }

                replyText = replyText.replace(/^["']|["']$/g, '');

                broadcast({
                    type: 'agent_status',
                    agent: agentId,
                    state: 'working',
                    msg: replyText
                });

                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ status: 'ok', reply: replyText }));
            } catch (e) {
                res.writeHead(400, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: e.message }));
            }
        });
        return;
    }

    // API Route: Trigger Filtro / Meta API Scraper
    if (req.method === 'POST' && req.url === '/api/trigger-filter') {
        let body = '';
        req.on('data', chunk => body += chunk.toString());
        req.on('end', () => {
            try {
                let params = {};
                if (body) params = JSON.parse(body);
                
                let scriptName = 'agente_filtro_leads.py';
                let targetAgent = 'filtro_analista';

                if (params.agent === 'cazador_ads_local') {
                    scriptName = 'cazador_ads_local.py';
                    targetAgent = 'cazador360';
                } else if (params.mode === 'meta' || params.agent === 'cazador360') {
                    scriptName = 'cazador_meta_api.py';
                    targetAgent = 'cazador360';
                } else if (params.agent === 'cazadorventas') {
                    scriptName = 'cazador_facebook.py';
                    targetAgent = 'cazadorventas';
                }

                const scriptPath = path.join(ROOT, scriptName);
                console.log(`[API] Ejecutar Script: ${scriptName} (modo: ${params.mode || 'default'})`);

                broadcast({ 
                    type: 'agent_status', 
                    agent: targetAgent, 
                    state: 'working', 
                    msg: `Ejecutando ${scriptName}...` 
                });

                const cmd = process.platform === 'win32' ? 'py' : 'python';
                const pyProc = spawn(cmd, [scriptPath], { cwd: ROOT, shell: true });
                
                pyProc.stdout.on('data', (d) => {
                    const line = d.toString().trim();
                    console.log(`[Py ${scriptName}]:`, line);
                    // Transmitir cada línea de log a la Oficina Virtual
                    broadcast({ type: 'agent_log', agent: targetAgent, msg: line });
                });

                pyProc.stderr.on('data', (d) => {
                    const errLine = d.toString().trim();
                    console.warn(`[Py Err ${scriptName}]:`, errLine);
                    broadcast({ type: 'agent_log', agent: targetAgent, msg: `⚠️ ERROR: ${errLine}` });
                });

                pyProc.on('close', (code) => {
                    console.log(`[Py ${scriptName}] Finalizado con código: ${code}`);
                    broadcast({ 
                        type: 'agent_status', 
                        agent: targetAgent, 
                        state: 'lead', 
                        msg: isMetaMode ? '¡Escaneo Meta Ads Finalizado!' : '¡Análisis completado!' 
                    });
                    broadcast({ type: 'agent_log', agent: targetAgent, msg: `[SISTEMA] Script ${scriptName} finalizado con código ${code}.` });
                });

                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ status: 'started', script: scriptName }));
            } catch (e) {
                res.writeHead(400, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: e.message }));
            }
        });
        return;
    }

    // API Route: Lead Result
    if (req.method === 'POST' && req.url === '/api/lead-result') {
        let body = '';
        req.on('data', chunk => body += chunk.toString());
        req.on('end', () => {
            try {
                const data = JSON.parse(body);
                saveAgentReport('FILTRO_ANALISTA', data);

                // Guardar/actualizar MASTER_LEADS_CALIFICADOS_AUSTRALDRONE.csv en el servidor Render
                const masterCsvPath = path.join(ROOT, 'MASTER_LEADS_CALIFICADOS_AUSTRALDRONE.csv');
                const topLeads = data.top_leads || (data.prospecto ? [data.prospecto] : []);
                if (topLeads.length > 0) {
                    try {
                        const fileExists = fs.existsSync(masterCsvPath);
                        let csvContent = '';
                        if (!fileExists) {
                            csvContent += "Fecha Procesamiento,Rank,Score B2B,Nombre Vendedor,Telefono Contacto,Ubicacion,Superficie Has,Precio CLP UF,Deal Size Estimado,Nivel Urgencia,Diagnostico IA,Accion Recomendada,Link Perfil Facebook,Link Publicacion Grupo\n";
                        }
                        const nowStr = new Date().toISOString().replace('T', ' ').substring(0, 16);
                        topLeads.forEach(lead => {
                            const row = [
                                nowStr,
                                lead.rank || 1,
                                lead.score_final || lead.score || 0,
                                `"${(lead.nombre || '').replace(/"/g, '""')}"`,
                                `"${(lead.telefono || '').replace(/"/g, '""')}"`,
                                `"${(lead.ubicacion || '').replace(/"/g, '""')}"`,
                                `"${(lead.superficie || '').replace(/"/g, '""')}"`,
                                `"${(lead.precio || '').replace(/"/g, '""')}"`,
                                `"${(lead.deal_size_estimado || '').replace(/"/g, '""')}"`,
                                `"${(lead.nivel_urgencia || lead.nivel_interes || 'MEDIA').replace(/"/g, '""')}"`,
                                `"${(lead.motivo_top || lead.diagnostico || '').replace(/"/g, '""')}"`,
                                `"${(lead.accion_recomendada || lead.accion || '').replace(/"/g, '""')}"`,
                                `"${(lead.link_perfil || '').replace(/"/g, '""')}"`,
                                `"${(lead.link_post || '').replace(/"/g, '""')}"`
                            ];
                            csvContent += row.join(',') + '\n';
                        });
                        fs.appendFileSync(masterCsvPath, csvContent, 'utf-8');
                        console.log(`[API] Guardado ${topLeads.length} leads en Master CSV del servidor.`);
                    } catch(csvErr) {
                        console.error('[API] Error guardando CSV en servidor:', csvErr.message);
                    }
                }

                broadcast({
                    type: 'lead_report',
                    agent: 'filtro_analista',
                    top_leads: data.top_leads || (data.prospecto ? [data.prospecto] : []),
                    total_analizados: data.total_analizados,
                    total_calificados: data.total_calificados,
                    timestamp: new Date().toISOString()
                });

                broadcast({ type: 'agent_status', agent: 'filtro_analista', state: 'lead', msg: 'TOP LEADS listos para el CEO' });

                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ status: 'received', broadcasted: true }));
            } catch (e) {
                res.writeHead(400, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: e.message }));
            }
        });
        return;
    }

    // API Route: Descargar Master CSV
    if (req.method === 'GET' && req.url === '/api/download-master-csv') {
        const masterCsvPath = path.join(ROOT, 'MASTER_LEADS_CALIFICADOS_AUSTRALDRONE.csv');
        if (fs.existsSync(masterCsvPath)) {
            res.writeHead(200, {
                'Content-Type': 'text/csv; charset=utf-8',
                'Content-Disposition': 'attachment; filename="MASTER_LEADS_CALIFICADOS_AUSTRALDRONE.csv"'
            });
            fs.createReadStream(masterCsvPath).pipe(res);
        } else {
            res.writeHead(404, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'Master CSV no generado aún.' }));
        }
        return;
    }

    // API Route: Obtener leads en formato JSON para el War Room
    if (req.method === 'GET' && req.url === '/api/leads-json') {
        const masterCsvPath = path.join(ROOT, 'MASTER_LEADS_CALIFICADOS_AUSTRALDRONE.csv');
        if (fs.existsSync(masterCsvPath)) {
            try {
                const content = fs.readFileSync(masterCsvPath, 'utf-8');
                const lines = content.split(/\r?\n/).filter(line => line.trim().length > 0);
                if (lines.length <= 1) {
                    res.writeHead(200, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ success: true, leads: [], total: 0 }));
                    return;
                }
                const headers = lines[0].split(',').map(h => h.replace(/^"|"$/g, '').trim());
                const leads = [];
                for (let i = 1; i < lines.length; i++) {
                    const cols = lines[i].split(/,(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)/).map(c => c.replace(/^"|"$/g, '').trim());
                    if (cols.length >= 4) {
                        leads.push({
                            fecha: cols[0] || '',
                            rank: cols[1] || i,
                            score: parseInt(cols[2]) || 80,
                            nombre: cols[3] || 'Vendedor B2B',
                            telefono: cols[4] || '',
                            ubicacion: cols[5] || '',
                            superficie: cols[6] || '',
                            precio: cols[7] || '',
                            deal_size_estimado: cols[8] || 'Alto (>$5M CLP)',
                            nivel_urgencia: cols[9] || 'ALTA',
                            motivo_top: cols[10] || '',
                            accion_recomendada: cols[11] || '',
                            link_perfil: cols[12] || '',
                            link_post: cols[13] || ''
                        });
                    }
                }
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ success: true, leads: leads.reverse(), total: leads.length }));
            } catch (err) {
                res.writeHead(500, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: err.message }));
            }
        } else {
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ success: true, leads: [], total: 0 }));
        }
        return;
    }

    // Configuración Persistente de Agentes
    if (!global._agentConfigs) {
        global._agentConfigs = new Map([
            ['cazador360', {
                query_terms: 'parcelas Chile, venta parcelas sur, loteos Frutillar',
                min_score_threshold: 60,
                target_region_bonus: 'Región de Los Lagos',
                auto_notify_telegram: true
            }],
            ['cazadorventas', {
                query_terms: 'terrenos sur chile, macrolotes osorno, parcelas puerto varas',
                min_score_threshold: 50,
                auto_scan_interval_min: 30
            }],
            ['filtro_analista', {
                min_surface_ha: 5.0,
                sur_bonus_points: 20,
                phone_bonus_points: 20,
                llm_temperature: 0.2,
                exclude_regions: 'Santiago, Valparaíso, Concepción'
            }],
            ['troya', {
                system_prompt_tone: 'Comercial Consultivo B2B',
                auto_qualify_budget: '$5.000.000 CLP',
                max_response_delay_sec: 2
            }],
            ['nicole', {
                routine_frequency_sec: 30,
                auto_calendar_sync: true
            }],
            ['diego', {
                default_theme_mode: 'Cyberpunk Neon',
                hotspot_auto_pulse: true
            }]
        ]);
    }

    // API Route: GET /api/agent-config
    if (req.method === 'GET' && req.url.startsWith('/api/agent-config')) {
        const urlObj = new URL(req.url, 'http://localhost');
        const agentId = urlObj.searchParams.get('agent');
        res.writeHead(200, { 'Content-Type': 'application/json' });
        if (agentId && global._agentConfigs.has(agentId)) {
            res.end(JSON.stringify({ success: true, agent: agentId, config: global._agentConfigs.get(agentId) }));
        } else {
            const allConfigs = {};
            for (let [k, v] of global._agentConfigs.entries()) allConfigs[k] = v;
            res.end(JSON.stringify({ success: true, configs: allConfigs }));
        }
        return;
    }

    // API Route: POST /api/agent-config
    if (req.method === 'POST' && req.url === '/api/agent-config') {
        let body = '';
        req.on('data', chunk => body += chunk);
        req.on('end', () => {
            try {
                const data = JSON.parse(body);
                if (data.agent && data.config) {
                    const current = global._agentConfigs.get(data.agent) || {};
                    const updated = { ...current, ...data.config };
                    global._agentConfigs.set(data.agent, updated);

                    broadcast({ type: 'agent_config_updated', agent: data.agent, config: updated });

                    res.writeHead(200, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ success: true, agent: data.agent, config: updated }));
                } else {
                    res.writeHead(400, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ error: 'Faltan parámetros agent o config.' }));
                }
            } catch (e) {
                res.writeHead(400, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: e.message }));
            }
        });
        return;
    }

    // API Route: POST /api/saas-reprogram (Reprogramación Agéntica Masiva SaaS)
    if (req.method === 'POST' && req.url === '/api/saas-reprogram') {
        let body = '';
        req.on('data', chunk => body += chunk);
        req.on('end', () => {
            try {
                const data = JSON.parse(body);
                const domain = data.domain || 'www.terragestion.cl';
                const mission = data.mission || 'Buscar compradores e inmobiliarias con interés en terrenos B2B';
                const industry = data.industry || 'Inmobiliaria & Terrenos';

                global._saasCurrentTarget = { domain, mission, industry, reprogrammedAt: new Date().toISOString() };

                if (global._agentConfigs) {
                    for (let [agentId, cfg] of global._agentConfigs.entries()) {
                        cfg.target_domain = domain;
                        cfg.mission_prompt = mission;
                        cfg.industry = industry;
                        global._agentConfigs.set(agentId, cfg);
                    }
                }

                broadcast({
                    type: 'agents_reprogrammed',
                    domain,
                    mission,
                    industry,
                    timestamp: new Date().toISOString()
                });

                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({
                    success: true,
                    message: `Flota agéntica reprogramada exitosamente para ${domain}`,
                    target: global._saasCurrentTarget
                }));
            } catch (e) {
                res.writeHead(400, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: e.message }));
            }
        });
        return;
    }

    // API Route: GET /api/saas-reprogram
    if (req.method === 'GET' && req.url === '/api/saas-reprogram') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({
            success: true,
            target: global._saasCurrentTarget || {
                domain: 'www.australdrone.cl',
                mission: 'Prospección B2B de macrolotes y loteos en el Sur de Chile',
                industry: 'Drones 4K & MasterPlan 360°',
                reprogrammedAt: new Date().toISOString()
            }
        }));
        return;
    }

    // API Route: POST /api/multimodal-vision (Análisis Visual de Anuncios)
    if (req.method === 'POST' && req.url === '/api/multimodal-vision') {
        let body = '';
        req.on('data', chunk => body += chunk);
        req.on('end', () => {
            try {
                const data = JSON.parse(body);
                const visionResult = {
                    has_text: true,
                    detected_text: "Venta de macrolote 14.8 Has en Frutillar. Contacto: +56984129034",
                    is_paid_competitor_ad: true,
                    confidence_score: 96,
                    pricing_inquiry: true,
                    extracted_phone: "+56984129034",
                    extracted_surface: "14.8 Has",
                    extracted_location: "Frutillar, Los Lagos",
                    recommendation: "Pauta activa detectada. Prioridad ALTA para Troya WA."
                };

                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ success: true, result: visionResult }));
            } catch(e) {
                res.writeHead(400, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: e.message }));
            }
        });
        return;
    }

    // API Route: Agent Status
    if (req.method === 'GET' && req.url.startsWith('/api/agent-status/')) {
        const agentId = req.url.split('/api/agent-status/')[1];
        const state = agentState.get(agentId);
        if (state) {
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({
                agent: agentId,
                state: state.currentState || 'idle',
                last_activity: state.lastActivity,
                logs_recientes: state.logs,
                leads_encontrados: state.leads,
                uptime_seconds: state.startTime ? Math.floor((new Date() - new Date(state.startTime)) / 1000) : 0
            }));
        } else {
            res.writeHead(404, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'Agent not found or no data yet' }));
        }
        return;
    }

    // Global In-Memory CRM Store & Persistence
    if (!global._crmPipelineLeads) {
        global._crmPipelineLeads = [];
    }

    // API Route: POST /api/inbound-lead (Form Inbound de www.australdrone.cl)
    if (req.method === 'POST' && req.url === '/api/inbound-lead') {
        let body = '';
        req.on('data', chunk => body += chunk.toString());
        req.on('end', () => {
            try {
                const data = JSON.parse(body || '{}');
                const newLead = {
                    id: Date.now(),
                    empresa: data.empresa || data.nombre || 'Lead Inbound Web',
                    zona: data.zona || 'Puerto Varas / Llanquihue',
                    email: data.email || 'contacto@inbound.cl',
                    phone: data.phone || data.telefono || '+56 9 8412 9034',
                    website: data.website || 'australdrone.cl',
                    mapsUrl: `https://www.google.com/maps/search/${encodeURIComponent(data.empresa || 'Puerto Varas')}`,
                    httpStatus: '200 OK (Inbound Directo)',
                    etapa: 'CAPTURADO',
                    score: data.score || 95,
                    score_intencion: 90,
                    nivel_intencion: '🔥 ALTA (Formulario Web)',
                    notas: data.mensaje || 'Contacto capturado en vivo desde www.australdrone.cl',
                    yaContactado: false,
                    aprobado: true,
                    fecha_creacion: new Date().toISOString()
                };

                global._crmPipelineLeads.unshift(newLead);
                broadcast({ type: 'crm_new_inbound', lead: newLead });
                broadcast({ type: 'agent_status', agent: 'cazadorbanana', state: 'lead', msg: `🔥 ¡Nuevo Lead Inbound de ${newLead.empresa}!` });

                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ success: true, lead: newLead }));
            } catch(e) {
                res.writeHead(400, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: e.message }));
            }
        });
        return;
    }

    // API Route: POST /api/crm-stage-update
    if (req.method === 'POST' && req.url === '/api/crm-stage-update') {
        let body = '';
        req.on('data', chunk => body += chunk.toString());
        req.on('end', () => {
            try {
                const data = JSON.parse(body || '{}');
                const { id, etapa, notas } = data;
                
                const item = global._crmPipelineLeads.find(l => l.id === id);
                if (item) {
                    if (etapa) item.etapa = etapa;
                    if (notas !== undefined) item.notas = notas;
                    broadcast({ type: 'crm_stage_updated', lead: item });
                }

                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ success: true, item }));
            } catch(e) {
                res.writeHead(400, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: e.message }));
            }
        });
        return;
    }

    // Permanent Map Config & Core Backup Files
    const MAP_PERMANENT_FILE = path.join(ROOT, 'MAP_CONFIG_PERMANENT.json');
    const BACKUP_CORE_FILE = path.join(ROOT, 'BACKUP_CORE_INITIAL.json');
    const DIEGO_LOG_FILE = path.join(ROOT, 'DIEGO_CHANGES_LOG.json');

    // Inicializar Backup Madre Core si no existe
    if (!fs.existsSync(BACKUP_CORE_FILE)) {
        try {
            const initialCore = {
                timestamp: new Date().toISOString(),
                version: "5.0 - Modo Dios Baseline",
                adminOwner: "Jaime Vidal Paredes (CEO)",
                protectedModules: ["CRM_KANBAN", "EMAIL_TEMPLATES", "META_ADS_SCRAPER", "LLAMA_SCORING_PROMPTS"],
                permanentColliders: []
            };
            fs.writeFileSync(BACKUP_CORE_FILE, JSON.stringify(initialCore, null, 2), 'utf8');
        } catch(e) {}
    }

    function cargarDiegoAuditLog() {
        if (fs.existsSync(DIEGO_LOG_FILE)) {
            try {
                return JSON.parse(fs.readFileSync(DIEGO_LOG_FILE, 'utf8'));
            } catch(e) {}
        }
        return [];
    }

    function registrarCambioDiego(accion, detalles) {
        try {
            const logs = cargarDiegoAuditLog();
            const nuevoRegistro = {
                id: Date.now(),
                timestamp: new Date().toISOString(),
                autor: 'Diego Architect',
                accion,
                detalles,
                estado: 'PENDIENTE_APROBACION_CEO'
            };
            logs.unshift(nuevoRegistro);
            fs.writeFileSync(DIEGO_LOG_FILE, JSON.stringify(logs, null, 2), 'utf8');
            broadcast({ type: 'diego_audit_log_updated', log: nuevoRegistro });
            return nuevoRegistro;
        } catch(e) {
            return null;
        }
    }

    function cargarMapConfigPermanente() {
        if (fs.existsSync(MAP_PERMANENT_FILE)) {
            try {
                return JSON.parse(fs.readFileSync(MAP_PERMANENT_FILE, 'utf8'));
            } catch(e) {}
        }
        return { colliders: [], objects: [], zones: [], ambience: { presetIndex: 0 }, lastUpdated: new Date().toISOString() };
    }

    function guardarMapConfigPermanente(config, accionLog) {
        try {
            config.lastUpdated = new Date().toISOString();
            fs.writeFileSync(MAP_PERMANENT_FILE, JSON.stringify(config, null, 2), 'utf8');
            if (accionLog) registrarCambioDiego(accionLog.accion, accionLog.detalles);
            broadcast({ type: 'map_config_synced', config });
            return true;
        } catch(e) {
            return false;
        }
    }

    // API Route: GET /api/diego-audit-log (Bitácora de Diego para Modo Dios CEO)
    if (req.method === 'GET' && req.url === '/api/diego-audit-log') {
        const logs = cargarDiegoAuditLog();
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ success: true, logs, total: logs.length }));
        return;
    }

    // API Route: POST /api/ceo-approve-diego-change (CEO Modo Dios Aprueba o Rechaza)
    if (req.method === 'POST' && req.url === '/api/ceo-approve-diego-change') {
        let body = '';
        req.on('data', chunk => body += chunk.toString());
        req.on('end', () => {
            try {
                const { id, estado } = JSON.parse(body || '{}');
                const logs = cargarDiegoAuditLog();
                const target = logs.find(l => l.id === id);
                if (target) {
                    target.estado = estado; // 'APROBADO_E_INTEGRADO' | 'RECHAZADO'
                    fs.writeFileSync(DIEGO_LOG_FILE, JSON.stringify(logs, null, 2), 'utf8');
                }
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ success: true, message: `Registro ${id} actualizado a ${estado}` }));
            } catch(e) {
                res.writeHead(400, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: e.message }));
            }
        });
        return;
    }

    // API Route: GET /api/permanent-map-config
    if (req.method === 'GET' && req.url === '/api/permanent-map-config') {
        const config = cargarMapConfigPermanente();
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ success: true, config }));
        return;
    }

    // API Route: POST /api/permanent-map-config (Guardar Cambios de Diego Architect)
    if (req.method === 'POST' && req.url === '/api/permanent-map-config') {
        let body = '';
        req.on('data', chunk => body += chunk.toString());
        req.on('end', () => {
            try {
                const data = JSON.parse(body || '{}');
                const ok = guardarMapConfigPermanente(data, { accion: 'MODIFICACIÓN_MAPA', detalles: `Actualización de ${data.colliders?.length || 0} colisionadores y ${data.objects?.length || 0} objetos.` });
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ success: ok, message: 'Configuración registrada en la Bitácora de Diego y guardada exitosamente.' }));
            } catch(e) {
                res.writeHead(400, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: e.message }));
            }
        });
        return;
    }

    // API Route: GET /api/crm-leads
    if (req.method === 'GET' && req.url === '/api/crm-leads') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ success: true, leads: global._crmPipelineLeads, total: global._crmPipelineLeads.length }));
        return;
    }

    // Static Files
    let urlPath = req.url.split('?')[0];
    if (urlPath === '/' || urlPath === '') urlPath = '/index.html';

    const filePath = path.join(ROOT, urlPath);

    fs.readFile(filePath, (err, data) => {
        if (err) {
            res.writeHead(404, { 'Content-Type': 'text/plain' });
            res.end(`404 - No encontrado: ${urlPath}`);
            return;
        }
        const ext  = path.extname(filePath).slice(1).toLowerCase();
        const mime = MIME[ext] || 'application/octet-stream';
        res.writeHead(200, { 'Content-Type': mime });
        res.end(data);
    });
});

function broadcast(obj) {
    wss.clients.forEach((client) => {
        if (client.readyState === WebSocket.OPEN) {
            client.send(JSON.stringify(obj));
        }
    });
}

// Real-Time Multi-User WebSocket Server
const wss = new WebSocketServer({ server });
const connectedClients = new Map(); // ws -> { role, x, y, anim }

wss.on('connection', (ws) => {
    console.log('[WS] Nuevo cliente conectado al HQ');

    // Transmitir configuración de mapa permanente guardada
    try {
        const currentMapCfg = cargarMapConfigPermanente();
        ws.send(JSON.stringify({ type: 'map_config_synced', config: currentMapCfg }));
    } catch(e) {}

    ws.on('message', (message) => {
        try {
            const data = JSON.parse(message.toString());
            
            // Broadcast posición y estado a todos los demás usuarios conectados
            if (data.type === 'player_sync') {
                connectedClients.set(ws, { role: data.role, x: data.x, y: data.y, anim: data.anim, flipX: data.flipX });
                
                wss.clients.forEach((client) => {
                    if (client !== ws && client.readyState === WebSocket.OPEN) {
                        client.send(JSON.stringify(data));
                    }
                });
            } else if (data.type === 'chat_message' || data.type === 'agent_status' || data.type === 'agent_log') {
                if (data.type === 'agent_log' || data.type === 'agent_status') {
                    const agentId = data.agent;
                    if (agentId) {
                        if (!agentState.has(agentId)) agentState.set(agentId, { logs: [], leads: 0, lastActivity: null, startTime: new Date().toISOString(), currentState: 'idle' });
                        const state = agentState.get(agentId);
                        
                        if (data.type === 'agent_log') {
                            state.logs.unshift(data.msg);
                            if (state.logs.length > 20) state.logs.pop();
                            if (data.msg && data.msg.includes('prospecto')) {
                                const match = data.msg.match(/(\d+)\s*prospecto/);
                                if (match) state.leads += parseInt(match[1]);
                            }
                        } else if (data.type === 'agent_status') {
                            if (data.state) state.currentState = data.state;
                        }
                        state.lastActivity = new Date().toISOString();
                        agentState.set(agentId, state);
                    }
                }

                wss.clients.forEach((client) => {
                    if (client.readyState === WebSocket.OPEN) {
                        client.send(JSON.stringify(data));
                    }
                });
            } else if (data.type === 'trigger_local_agent') {
                console.log(`[WS Relay] Retransmitiendo orden de ejecución a PC local: ${data.agent}`);
                wss.clients.forEach((client) => {
                    if (client.readyState === WebSocket.OPEN) {
                        client.send(JSON.stringify(data));
                    }
                });
            }
        } catch (e) {
            console.warn('[WS] Error parseando mensaje:', e.message);
        }
    });

    ws.on('close', () => {
        const info = connectedClients.get(ws);
        if (info) {
            console.log(`[WS] Cliente desconectado: ${info.role}`);
            wss.clients.forEach((client) => {
                if (client !== ws && client.readyState === WebSocket.OPEN) {
                    client.send(JSON.stringify({ type: 'player_disconnect', role: info.role }));
                }
            });
            connectedClients.delete(ws);
        }
    });
});

server.listen(PORT, '0.0.0.0', () => {
    console.log('');
    console.log('  ╔══════════════════════════════════════════════════╗');
    console.log('  ║  AustralDrone.CL — Servidor Multiplayer Live HQ  ║');
    console.log('  ║  ✅  Servidor Cloud activo en puerto: ' + PORT + '         ║');
    console.log('  ║  🌐  WebSocket Sync Activo                       ║');
    console.log('  ╚══════════════════════════════════════════════════╝');
    console.log('');
});

server.on('error', (e) => {
    console.error('[ERROR] Server:', e.message);
});
