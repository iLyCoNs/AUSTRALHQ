import os, re

root_dir = r"c:\Users\LyCoNs\Desktop\AGENTES IA"
server_files = [
    os.path.join(root_dir, "server.js"),
    os.path.join(root_dir, "CRM AustralDrone", "server.js")
]

meta_config_code = '''
// API Configuración del Agente Meta independiente desde el War Room
app.get('/api/config/meta-agent', (req, res) => {
    const cfgPath = path.join(__dirname, 'config_meta_agent.json');
    if (fs.existsSync(cfgPath)) {
        try { return res.json(JSON.parse(fs.readFileSync(cfgPath, 'utf8'))); } catch(e) {}
    }
    return res.json({
        geographic_scope: "Temuco a Chiloé (Sur de Chile)",
        keywords: ["parcelas", "loteo", "frutillar", "puerto varas", "osorno", "temuco", "valdivia", "villarrica", "pucon", "chiloe"],
        forbidden_languages: ["portugués", "pt", "br"],
        min_score_threshold: 85,
        status: "ACTIVO EXCLUSIVO"
    });
});

app.post('/api/config/meta-agent', (req, res) => {
    const cfgPath = path.join(__dirname, 'config_meta_agent.json');
    fs.writeFileSync(cfgPath, JSON.stringify(req.body, null, 2), 'utf8');
    return res.json({ status: "OK", message: "Configuración del Agente Meta actualizada desde War Room." });
});
'''

for sf in server_files:
    if os.path.exists(sf):
        with open(sf, 'r', encoding='utf-8') as f:
            content = f.read()

        if '/api/config/meta-agent' not in content:
            content = content.replace("app.listen(", meta_config_code + "\napp.listen(")

        with open(sf, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"SUCCESS: Updated {sf} with War Room Meta Agent Configuration endpoints!")
