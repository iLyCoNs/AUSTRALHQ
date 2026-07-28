import os, sys, subprocess

def build_windows_app():
    crm_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"=== COMPILADOR NATIVO CRM AUSTRALDRONE ===")
    print(f"Directorio de trabajo: {crm_dir}")

    # 1. Instalar npm packages
    print("\n[1/3] Instalando dependencias de Node.js / Electron...")
    subprocess.run("npm install", shell=True, cwd=crm_dir)

    # 2. Compilar ejecutable con electron-builder
    print("\n[2/3] Compilando binarios de Windows (.exe)...")
    result = subprocess.run("npx electron-builder --win nsis portable", shell=True, cwd=crm_dir)

    dist_dir = os.path.join(crm_dir, 'dist')
    if os.path.exists(dist_dir):
        print(f"\n[3/3] ¡ÉXITO! Los archivos ejecutables de Windows se generaron en:")
        print(f"👉 {dist_dir}")
        for item in os.listdir(dist_dir):
            if item.endswith('.exe'):
                print(f"   📦 {item}")
    else:
        print("\n⚠️ No se encontró la carpeta dist/. Revisa los logs de compilación.")

if __name__ == '__main__':
    build_windows_app()
