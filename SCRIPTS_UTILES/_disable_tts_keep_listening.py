import os

root_dir = r"c:\Users\LyCoNs\Desktop\AGENTES IA"
files_to_patch = [
    os.path.join(root_dir, "index.html"),
    os.path.join(root_dir, "PHASER_OFFICE.html"),
    os.path.join(root_dir, "WAR_ROOM_EXECUTIVE.html"),
    os.path.join(root_dir, "CRM AustralDrone", "ENTERPRISE_CRM_APP.html")
]

for fpath in files_to_patch:
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Reemplazar llamadas a speak por retorno silencioso
        content = content.replace("window.speechSynthesis.speak(utter);", "// window.speechSynthesis.speak(utter); // Desactivado por solicitud del CEO (Solo escuchar dictado)")
        
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"SUCCESS: Disabled TTS speech in {os.path.basename(fpath)}")
