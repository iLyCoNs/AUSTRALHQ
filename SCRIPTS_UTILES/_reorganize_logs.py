import os, shutil, glob

root_dir = r"c:\Users\LyCoNs\Desktop\AGENTES IA"
logs_dir = os.path.join(root_dir, "LOGS_HISTORICOS")

agent_folders = [
    "logs_cazador_meta",
    "logs_cazador_360",
    "logs_secretaria_camila",
    "logs_filtro_analista",
    "logs_vendedores_360",
    "prospectos_dormidos"
]

for folder in agent_folders:
    os.makedirs(os.path.join(logs_dir, folder), exist_ok=True)

# Mover reportes viejos desordenados a prospectos_dormidos
reports_dir = os.path.join(root_dir, "REPORTES_AGENTES")
if os.path.exists(reports_dir):
    for root, dirs, files in os.walk(reports_dir):
        for file in files:
            if file.endswith('.json') or file.endswith('.csv'):
                src = os.path.join(root, file)
                dst = os.path.join(logs_dir, "prospectos_dormidos", file)
                try:
                    shutil.move(src, dst)
                    print(f"MOVED: {file} -> prospectos_dormidos/")
                except Exception:
                    pass

print("SUCCESS: Log directory structure cleaned and reorganized!")
