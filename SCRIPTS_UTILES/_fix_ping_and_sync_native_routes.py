import os

root_dir = r"c:\Users\LyCoNs\Desktop\AGENTES IA"
servers = [
    os.path.join(root_dir, "server.js"),
    os.path.join(root_dir, "CRM AustralDrone", "server.js")
]

native_ping_code = r'''
    // API Route: GET /api/ping (Keep-Alive Anti-Adormecimiento para Render.com)
    if (req.method === 'GET' && req.url.startsWith('/api/ping')) {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ status: "ONLINE", timestamp: new Date().toISOString(), service: "AustralHQ Server" }));
        return;
    }

    // API Route: POST /api/secretaria/sync-absence (Sincronización Manual/Auto de Ausencia tras Despertar)
    if (req.method === 'POST' && req.url.startsWith('/api/secretaria/sync-absence')) {
        syncHistoricalAbsenceLogs();
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ status: "SUCCESS", message: "Sincronización de ausencia ejecutada por Secretaría Camila." }));
        return;
    }
'''

for s in servers:
    if os.path.exists(s):
        with open(s, 'r', encoding='utf-8') as f:
            content = f.read()

        if "req.url.startsWith('/api/ping')" not in content:
            marker = "if (req.method === 'POST' && req.url === '/api/secretaria/chat') {"
            if marker in content:
                content = content.replace(marker, native_ping_code + "\n    " + marker)

        with open(s, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"SUCCESS: Inserted native HTTP ping & sync routes into {s}")
