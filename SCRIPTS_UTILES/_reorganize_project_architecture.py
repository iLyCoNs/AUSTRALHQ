import os, shutil, re

root_dir = r"c:\Users\LyCoNs\Desktop\AGENTES IA"

# 1. Crear carpetas destino
agentes_dir = os.path.join(root_dir, "AGENTES")
data_dir = os.path.join(root_dir, "DATA")
scripts_dir = os.path.join(root_dir, "SCRIPTS_UTILES")

agent_subdirs = {
    "cazador_meta": os.path.join(agentes_dir, "cazador_meta"),
    "cazador_360": os.path.join(agentes_dir, "cazador_360"),
    "vendedores_360": os.path.join(agentes_dir, "vendedores_360"),
    "filtro_analista": os.path.join(agentes_dir, "filtro_analista"),
    "secretaria_camila": os.path.join(agentes_dir, "secretaria_camila")
}

for d in list(agent_subdirs.values()) + [data_dir, scripts_dir]:
    os.makedirs(d, exist_ok=True)

# 2. Mapeo de archivos a mover
moves = [
    # Agente Meta
    ("cazador_meta_api.py", agent_subdirs["cazador_meta"]),
    
    # Agente Cazador 360
    ("cazador_ads_local.py", agent_subdirs["cazador_360"]),
    ("cazador_facebook.py", agent_subdirs["cazador_360"]),
    ("scrapling_agent_engine.py", agent_subdirs["cazador_360"]),
    
    # Agente Vendedores 360
    ("cazador_360_vendedores.py", agent_subdirs["vendedores_360"]),
    
    # Agente Filtro Analista
    ("agente_filtro_leads.py", agent_subdirs["filtro_analista"]),
    
    # Secretaría Camila
    ("SECRETARIA_CHAT_MEMORY.json", agent_subdirs["secretaria_camila"]),
    
    # Scripts Útiles
    ("simular_email_360.py", scripts_dir),
    ("scan_real_prospects.py", scripts_dir),
    ("crear_workflow_n8n.py", scripts_dir),
    ("local_bridge_worker.js", scripts_dir),
    ("CREAR_ACCESO_DIRECTO.ps1", scripts_dir),
    
    # Data & JSON de Estado
    ("BACKUP_CORE_INITIAL.json", data_dir),
    ("CAZADOR_BANANA_MEMORY.json", data_dir),
    ("DIEGO_CHANGES_LOG.json", data_dir),
    ("MAP_CONFIG_PERMANENT.json", data_dir),
    ("deep_search_out.json", data_dir),
    ("australdrone.ico", os.path.join(root_dir, "assets"))
]

for src_name, target_folder in moves:
    src_path = os.path.join(root_dir, src_name)
    if os.path.exists(src_path):
        dst_path = os.path.join(target_folder, src_name)
        shutil.move(src_path, dst_path)
        print(f"MOVED: {src_name} -> {os.path.relpath(target_folder, root_dir)}")

# Mover carpetas de logs antiguas si existen en la raíz
old_logs_dir = os.path.join(root_dir, "logs_cazador")
if os.path.exists(old_logs_dir):
    try:
        shutil.move(old_logs_dir, os.path.join(root_dir, "LOGS_HISTORICOS", "logs_cazador"))
        print("MOVED: logs_cazador -> LOGS_HISTORICOS/logs_cazador")
    except Exception as e:
        print("INFO logs_cazador:", e)

print("\nSUCCESS: All files reorganized into clean AGENTES/, DATA/, and SCRIPTS_UTILES/ folders!")
