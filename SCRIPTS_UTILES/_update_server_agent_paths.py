import os

root_dir = r"c:\Users\LyCoNs\Desktop\AGENTES IA"
servers = [
    os.path.join(root_dir, "server.js"),
    os.path.join(root_dir, "CRM AustralDrone", "server.js")
]

path_replacements = [
    ("cazador_meta_api.py", "AGENTES/cazador_meta/cazador_meta_api.py"),
    ("cazador_ads_local.py", "AGENTES/cazador_360/cazador_ads_local.py"),
    ("cazador_360_vendedores.py", "AGENTES/vendedores_360/cazador_360_vendedores.py"),
    ("agente_filtro_leads.py", "AGENTES/filtro_analista/agente_filtro_leads.py"),
    ("SECRETARIA_CHAT_MEMORY.json", "AGENTES/secretaria_camila/SECRETARIA_CHAT_MEMORY.json")
]

for s in servers:
    if os.path.exists(s):
        with open(s, 'r', encoding='utf-8') as f:
            content = f.read()
        
        for old_path, new_path in path_replacements:
            content = content.replace(old_path, new_path)
            # Evitar duplicaciones como AGENTES/.../AGENTES/...
            content = content.replace(f"AGENTES/{new_path}", new_path)
        
        with open(s, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"SUCCESS: Updated execution paths in {s}")
