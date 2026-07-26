"""
CAZADOR 360 v17.0 - AustralDrone.CL
Arquitectura de procesos separados:
  - Facebook (Comet): proceso principal
  - Yapo.cl (Chromium): subprocess separado con su propio servidor Playwright
"""
import asyncio
import subprocess
import time
import json
import os
import re
import csv
import sys
from playwright.async_api import async_playwright
from langchain_openai import ChatOpenAI

# ===================== CONFIGURACION =====================
COMET_EXE_PATH = r"C:\Users\LyCoNs\AppData\Local\Perplexity\Comet\Application\comet.exe"
COMET_USER_DATA_PATH = r"C:\Users\LyCoNs\AppData\Local\Perplexity\Comet\User Data"
SINGLETON_LOCK = os.path.join(COMET_USER_DATA_PATH, "Profile 1", "SingletonLock")

TIEMPO_POR_GRUPO = 180  # 3 minutos por grupo

LOGS_DIR = r"c:\Users\LyCoNs\Desktop\AGENTES IA\logs_vendedores_360"
os.makedirs(LOGS_DIR, exist_ok=True)
LOG_FILE_PATH = os.path.join(LOGS_DIR, f"fb_{time.strftime('%Y%m%d_%H%M%S')}.jsonl")
CSV_FILE_PATH = os.path.join(r"c:\Users\LyCoNs\Desktop\AGENTES IA", "VENDEDORES_MACROLOTES_MASTERPLAN_360.csv")

HEADERS_B2B = [
    'Fecha', 'Nombre Vendedor', 'Telefono Contacto', 'Tipo Vendedor',
    'Superficie Has', 'Estado MasterPlan', 'Potencial Venta',
    'Ubicacion', 'Precio CLP UF', 'Detalles', 'Link Perfil',
    'Link Post Directo', 'Fuente', 'Estado Gestion', 'Notas Auditoria'
]

GRUPOS_FACEBOOK = [
    "https://www.facebook.com/groups/1050649785505128/",
    "https://www.facebook.com/groups/2675489595976326/",
    "https://www.facebook.com/groups/186830830292028/",
    "https://www.facebook.com/groups/970889426338010/",
    "https://www.facebook.com/groups/322475331462689/",
    "https://www.facebook.com/groups/324142478851092/",
    "https://www.facebook.com/groups/24010713181862429/",
    "https://www.facebook.com/groups/452646578868248/",
    "https://www.facebook.com/groups/557092231825478/",
    "https://www.facebook.com/groups/1718696525300596/",
    "https://www.facebook.com/groups/Comprayventadeterrenosporapuroenchile/",
    "https://www.facebook.com/groups/1103879840113888/",
    "https://www.facebook.com/groups/1868446966785535/",
    "https://www.facebook.com/groups/219104011815348/",
    "https://www.facebook.com/groups/ventadeparcelaschile/",
    "https://www.facebook.com/groups/1482352695389355/",
    "https://www.facebook.com/groups/1718059098671369/"
]
# =========================================================

import base64
def get_nv_key():
    env_k = os.environ.get("NVIDIA_API_KEY")
    if env_k: return env_k
    enc = "bnZhcGktbGdsWlNVWGRYajhjZmMzU09GR2tObTZvWG9obmF1V3UtcUk2elhibEtMOElBZEdLRXJmdTFQVTFIS3BEczJldQ=="
    return base64.b64decode(enc).decode('utf-8')

# LLM NVIDIA
class CustomChatOpenAI(ChatOpenAI):
    provider: str = "openai"
    model: str = "meta/llama-3.1-70b-instruct"

llm = CustomChatOpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=get_nv_key(),
    model="meta/llama-3.1-70b-instruct"
)

def sp(msg):
    try:
        print(str(msg).encode('ascii', 'ignore').decode('ascii'), flush=True)
    except Exception:
        pass

def extraer_telefonos(texto):
    hits = re.findall(r'(\+?56\s?9?\s?\d{4}\s?\d{4}|\b9\s?\d{4}\s?\d{4}\b|\b9\d{8}\b)', texto)
    limpios = list(set([re.sub(r'\D', '', c) for c in hits if len(re.sub(r'\D', '', c)) >= 8]))
    formateados = []
    for t in limpios:
        if t.startswith("569") and len(t) == 11:
            formateados.append(f"+{t}")
        elif t.startswith("9") and len(t) == 9:
            formateados.append(f"+56{t}")
        else:
            formateados.append(t)
    return ", ".join(formateados) if formateados else "Ver perfil"

def guardar_reporte_agente(agente_nombre, datos):
    if not datos: return
    now_str = time.strftime('%Y-%m-%d_%H-%M-%S')
    base_dir = os.path.join(r"c:\Users\LyCoNs\Desktop\AGENTES IA", "REPORTES_AGENTES", agente_nombre.upper())
    os.makedirs(base_dir, exist_ok=True)
    filename = os.path.join(base_dir, f"{agente_nombre.upper()}_{now_str}.json")
    try:
        reporte = {
            "agente": agente_nombre.upper(),
            "fecha_hora_local": time.strftime('%Y-%m-%d %H:%M:%S'),
            "total_registros": len(datos) if isinstance(datos, list) else 1,
            "datos": datos
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(reporte, f, indent=2, ensure_ascii=False)
        sp(f"  >> [REPORTES] Guardado en carpeta {agente_nombre.upper()}: {filename}")
    except Exception as e:
        sp(f"  >> [REPORTES ERROR] {e}")

def guardar_csv(leads, fuente="Facebook"):
    if not leads:
        return
    guardar_reporte_agente("CAZADOR360", leads)
    existe = os.path.exists(CSV_FILE_PATH)
    try:
        with open(CSV_FILE_PATH, 'a', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=HEADERS_B2B)
            if not existe:
                writer.writeheader()
            for v in leads:
                writer.writerow({
                    'Fecha': v.get('Fecha', time.strftime('%Y-%m-%d %H:%M')),
                    'Nombre Vendedor': v.get('Nombre Vendedor', ''),
                    'Telefono Contacto': v.get('Telefono Contacto', 'Ver perfil'),
                    'Tipo Vendedor': v.get('Tipo Vendedor', 'Dueno Directo'),
                    'Superficie Has': v.get('Superficie Has', ''),
                    'Estado MasterPlan': v.get('Estado MasterPlan', 'SIN MASTERPLAN - Target Perfecto'),
                    'Potencial Venta': v.get('Potencial Venta', 'ALTO - Ofrecer 360'),
                    'Ubicacion': v.get('Ubicacion', ''),
                    'Precio CLP UF': v.get('Precio CLP UF', ''),
                    'Detalles': v.get('Detalles', ''),
                    'Link Perfil': v.get('Link Perfil', ''),
                    'Link Post Directo': v.get('Link Post Directo', ''),
                    'Fuente': fuente,
                    'Estado Gestion': 'Nuevo Prospecto B2B',
                    'Notas Auditoria': v.get('Notas Auditoria', 'Requiere MasterPlan 360 AustralDrone.CL')
                })
        sp(f"  >> [CSV] {len(leads)} leads de {fuente} guardados")
    except PermissionError:
        sp(f"  >> [CSV BLOQUEADO] Cierra el archivo CSV de Excel/Sheets y vuelve a intentar")
    except Exception as e:
        sp(f"  >> [CSV ERROR] {e}")

async def analizar_con_ia(texto, telefonos, fuente_url, num):
    if len(texto.strip()) < 500:
        sp(f"  >> [IA FB #{num}] Texto muy corto ({len(texto)} chars), saltando")
        return
    prompt = f"""Eres el AUDITOR B2B experto de AustralDrone.CL.
Analiza estas publicaciones de Facebook y extrae SOLO vendedores de terrenos o macrolotes de mas de 5 hectareas
en el SUR DE CHILE: Osorno, Puerto Varas, Llanquihue, Frutillar, Puerto Montt, Calbuco, Chiloe, Purranque o cercanos.

TEXTO DEL FEED:
{texto[:12000]}

TELEFONOS DETECTADOS: {telefonos}

CRITERIOS:
- Solo vendedores, NO compradores, NO arriendos
- Solo terrenos >5 hectareas
- Foto sin render 360 ni video drone = SIN MASTERPLAN
- EXCLUIR zonas fuera del sur de Chile

JSON sin markdown o [] si no hay nada:
[{{"Fecha":"{time.strftime('%Y-%m-%d %H:%M')}","Nombre Vendedor":"","Telefono Contacto":"{telefonos}","Tipo Vendedor":"Dueno Directo","Superficie Has":"","Estado MasterPlan":"SIN MASTERPLAN - Target Perfecto","Potencial Venta":"ALTO - Ofrecer 360","Ubicacion":"","Precio CLP UF":"","Detalles":"","Link Perfil":"","Link Post Directo":"{fuente_url}","Notas Auditoria":""}}]"""

    try:
        resp = await asyncio.wait_for(llm.ainvoke(prompt), timeout=40)
        res = (resp.content if hasattr(resp, 'content') else str(resp)).strip()
        if not res or (not res.startswith('[') and not res.startswith('{')):
            sp(f"  >> [IA FB #{num}] Respuesta no valida: '{res[:60]}'")
            return
        res = res.lstrip("```json").lstrip("```").rstrip("```").strip()
        leads = json.loads(res)
        if isinstance(leads, list) and leads:
            guardar_csv(leads, "Facebook")
            with open(LOG_FILE_PATH, 'a', encoding='utf-8') as f:
                f.write(json.dumps({"ts": time.strftime('%H:%M:%S'), "grupo": num, "leads": leads}, ensure_ascii=False) + "\n")
            sp(f"  >> [IA FB #{num}] {len(leads)} prospectos detectados!")
        else:
            sp(f"  >> [IA FB #{num}] Sin vendedores relevantes")
    except asyncio.TimeoutError:
        sp(f"  >> [IA FB #{num}] Timeout 40s")
    except json.JSONDecodeError:
        sp(f"  >> [IA FB #{num}] JSON invalido en respuesta")
    except Exception as e:
        sp(f"  >> [IA FB #{num}] Error: {str(e)[:80]}")

async def escanear_facebook():
    tareas_ia = []
    sp("[FB] Iniciando con Comet...")
    async with async_playwright() as p:
        try:
            # Fallback inteligente: Comet (Tu PC) -> Microsoft Edge (PC Nicole) -> Chromium genérico
            launch_kwargs = {
                "headless": False,
                "viewport": None,
                "args": ["--start-maximized"]
            }
            if os.path.exists(COMET_EXE_PATH):
                launch_kwargs["executable_path"] = COMET_EXE_PATH
                launch_kwargs["user_data_dir"] = COMET_USER_DATA_PATH
                launch_kwargs["args"].append("--profile-directory=Profile 1")
                sp("[FB] Usando navegador Comet (PC Principal)...")
            else:
                edge_user_data = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Microsoft", "Edge", "User Data")
                if os.path.exists(edge_user_data):
                    launch_kwargs["channel"] = "msedge"
                    launch_kwargs["user_data_dir"] = edge_user_data
                    sp("[FB] Usando Microsoft Edge (PC Nicole)...")
                else:
                    launch_kwargs["user_data_dir"] = os.path.join(os.path.expanduser("~"), ".australdrone_profile")
                    sp("[FB] Usando Chromium Estándar...")

            context = await p.chromium.launch_persistent_context(**launch_kwargs)
            page = await context.new_page()
            sp("[FB] Navegador listo. Iniciando recorrido de 17 grupos...")

            for idx, grupo_url in enumerate(GRUPOS_FACEBOOK, 1):
                sp(f"\n[FB {idx}/17] {grupo_url}")
                try:
                    await page.goto(grupo_url, wait_until="domcontentloaded", timeout=25000)
                    # Esperar feed real de Facebook
                    try:
                        await page.wait_for_selector('div[role="feed"]', timeout=12000)
                        sp(f"  Feed detectado OK.")
                    except Exception:
                        sp(f"  Feed no aparecio en 12s, continuando...")
                    await asyncio.sleep(2)

                    titulo = await page.title()
                    sp(f"  Cargado: {titulo[:50]}")

                    texto_acumulado = ""
                    t_inicio = time.time()
                    s = 0

                    while (time.time() - t_inicio) < TIEMPO_POR_GRUPO:
                        s += 1
                        seg_rest = int(TIEMPO_POR_GRUPO - (time.time() - t_inicio))
                        await page.evaluate("window.scrollBy(0, 1500);")
                        await asyncio.sleep(1.5)

                        # Capturar texto del feed real
                        texto_feed = await page.evaluate("""
                            () => {
                                const feed = document.querySelector('div[role="feed"]');
                                if (feed && feed.innerText.length > 100) return feed.innerText;
                                return document.body.innerText;
                            }
                        """)
                        if texto_feed and len(texto_feed) > len(texto_acumulado):
                            texto_acumulado = texto_feed

                        if s % 10 == 0 or seg_rest < 5:
                            sp(f"  [FB {idx}] Scroll #{s} | {len(texto_acumulado)} chars | {seg_rest}s")

                    telefonos = extraer_telefonos(texto_acumulado)
                    sp(f"  [FB {idx}] Scan OK: {len(texto_acumulado)} chars | Tel: {telefonos} | -> IA background")
                    tarea = asyncio.create_task(analizar_con_ia(texto_acumulado, telefonos, grupo_url, idx))
                    tareas_ia.append(tarea)

                except Exception as e:
                    sp(f"  [FB {idx}] Error: {str(e)[:80]}")

            sp(f"\n[FB] Recorrido completo. Esperando {len(tareas_ia)} tareas IA...")
            await asyncio.gather(*tareas_ia, return_exceptions=True)
            await context.close()
            sp("[FB] Modulo Facebook completado.")
        except Exception as e:
            sp(f"[FB ERROR CRITICO] {str(e)[:120]}")

def limpiar_locks_comet():
    """Elimina archivos de bloqueo de Comet para evitar conflicto de sesion"""
    for lock_name in ["SingletonLock", "SingletonSocket", "lockfile"]:
        lock_path = os.path.join(COMET_USER_DATA_PATH, "Profile 1", lock_name)
        if os.path.exists(lock_path):
            try:
                os.remove(lock_path)
                sp(f"[INIT] Lock eliminado: {lock_name}")
            except Exception as e:
                sp(f"[INIT] No se pudo eliminar {lock_name}: {e}")

if __name__ == "__main__":
    sp("=" * 60)
    sp("CAZADOR 360 v17.0 - Facebook + Yapo.cl (Procesos Separados)")
    sp(f"Facebook: {len(GRUPOS_FACEBOOK)} grupos x {TIEMPO_POR_GRUPO}s")
    sp(f"CSV: {CSV_FILE_PATH}")
    sp("=" * 60)

    # Inicializar CSV
    if not os.path.exists(CSV_FILE_PATH):
        with open(CSV_FILE_PATH, 'w', newline='', encoding='utf-8-sig') as f:
            csv.DictWriter(f, fieldnames=HEADERS_B2B).writeheader()

    # 1. Cerrar Comet y limpiar locks
    sp("[INIT] Cerrando Comet...")
    subprocess.run(["taskkill", "/IM", "comet.exe", "/F"], capture_output=True)
    time.sleep(4)
    limpiar_locks_comet()
    time.sleep(2)

    # 2. Lanzar Yapo como PROCESO SEPARADO (completamente independiente)
    sp("[INIT] Lanzando Yapo.cl como proceso independiente...")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    proc_yapo = subprocess.Popen(
        [sys.executable, os.path.join(script_dir, "yapo_scanner.py")],
        cwd=script_dir
    )
    sp(f"[INIT] Yapo PID: {proc_yapo.pid}")

    # 3. Facebook en proceso principal
    asyncio.run(escanear_facebook())

    # 4. Esperar que Yapo termine si aun no ha terminado
    sp("[INIT] Esperando que el proceso de Yapo.cl finalice...")
    proc_yapo.wait()
    sp("[INIT] Yapo.cl proceso finalizado.")

    sp(f"\n{'='*60}")
    sp(f"[FIN] Cazador 360 v17.0 completado.")
    sp(f"[CSV] {CSV_FILE_PATH}")
    sp(f"{'='*60}")
