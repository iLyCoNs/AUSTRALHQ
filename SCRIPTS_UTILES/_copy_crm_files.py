import os, shutil

root_dir = r'c:\Users\LyCoNs\Desktop\AGENTES IA'
target_dir = os.path.join(root_dir, 'CRM AustralDrone')

files_to_copy = [
    'server.js',
    'index.html',
    'WAR_ROOM_EXECUTIVE.html',
    'config_secrets.json',
    'SECRETARIA_CHAT_MEMORY.json'
]

for f in files_to_copy:
    src = os.path.join(root_dir, f)
    dst = os.path.join(target_dir, f)
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"SUCCESS: Copied {f} -> CRM AustralDrone/")

# Crear carpeta assets si no existe
assets_dir = os.path.join(target_dir, 'assets')
os.makedirs(assets_dir, exist_ok=True)
print("SUCCESS: Assets directory created!")
