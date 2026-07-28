import asyncio
import time
import json
import os
import re
import random
import requests
from playwright.async_api import async_playwright
from langchain_openai import ChatOpenAI

# 1. URL Oficial de n8n Producción (Envío Directo JSON por Comprador)
N8N_WEBHOOK_URL = "https://lycons.app.n8n.cloud/webhook/cazador-facebook"

# 2. Rutas del Navegador Comet y Perfil 1
COMET_EXE_PATH = r"C:\Users\LyCoNs\AppData\Local\Perplexity\Comet\Application\comet.exe"
COMET_USER_DATA_PATH = r"C:\Users\LyCoNs\AppData\Local\Perplexity\Comet\User Data"

# 3. Carpeta de Respaldo Local de Logs CRM y Registro de Comentarios
LOGS_DIR = r"c:\Users\LyCoNs\Desktop\AGENTES IA\logs_cazador"
os.makedirs(LOGS_DIR, exist_ok=True)
LOG_FILE_PATH = os.path.join(LOGS_DIR, f"respaldo_leads_{time.strftime('%Y%m%d')}.jsonl")
COMMENTS_LOG_PATH = os.path.join(LOGS_DIR, f"historial_comentarios_{time.strftime('%Y%m%d')}.jsonl")

# 4. Configuración LLM NVIDIA Llama 3.1 70B
import base64
def get_nv_key():
    env_k = os.environ.get("NVIDIA_API_KEY")
    if env_k: return env_k
    enc = "bnZhcGktbGdsWlNVWGRYajhjZmMzU09GR2tObTZvWG9obmF1V3UtcUk2elhibEtMOElBZEdLRXJmdTFQVTFIS3BEczJldQ=="
    return base64.b64decode(enc).decode('utf-8')

class CustomChatOpenAI(ChatOpenAI):
    provider: str = "openai"
    model: str = "meta/llama-3.1-70b-instruct"

llm = CustomChatOpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=get_nv_key(),
    model="meta/llama-3.1-70b-instruct"
)

# 5. Lista de los 17 Grupos de Facebook
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

def safe_print(msg):
    try:
        clean_msg = str(msg).encode('ascii', 'ignore').decode('ascii')
        print(clean_msg)
    except Exception:
        pass

def extraer_telefonos(texto):
    patron = r'(\+?56\s?9?\s?\d{4}\s?\d{4}|9\s?\d{4}\s?\d{4}|\d{8,9})'
    coincidencias = re.findall(patron, texto)
    telefonos_limpios = list(set([re.sub(r'\D', '', c) for c in coincidencias if len(re.sub(r'\D', '', c)) >= 8]))
    return ", ".join(telefonos_limpios) if telefonos_limpios else "No especifica / Ver perfil"

async def realizar_tipeo_humano(element, texto):
    for char in texto:
        await element.type(char, delay=random.randint(40, 95))
    await asyncio.sleep(1)

async def ejecutar_cazador_produccion_directa():
    safe_print("[INIT] Abriendo Comet con Cazador de Transmisión Directa a Google Sheets...")
    
    async with async_playwright() as p:
        launch_kwargs = {
            "headless": False,
            "viewport": None,
            "args": ["--start-maximized"]
        }
        if os.path.exists(COMET_EXE_PATH):
            launch_kwargs["executable_path"] = COMET_EXE_PATH
            launch_kwargs["user_data_dir"] = COMET_USER_DATA_PATH
            launch_kwargs["args"].append("--profile-directory=Profile 1")
            safe_print("[INIT] Usando navegador Comet (PC Principal)...")
        else:
            edge_user_data = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Microsoft", "Edge", "User Data")
            if os.path.exists(edge_user_data):
                launch_kwargs["channel"] = "msedge"
                launch_kwargs["user_data_dir"] = edge_user_data
                safe_print("[INIT] Usando Microsoft Edge (PC Nicole)...")
            else:
                launch_kwargs["user_data_dir"] = os.path.join(os.path.expanduser("~"), ".australdrone_profile")
                safe_print("[INIT] Usando Chromium Estándar...")

        context = await p.chromium.launch_persistent_context(**launch_kwargs)
        page = await context.new_page()

        for index, grupo_url in enumerate(GRUPOS_FACEBOOK, 1):
            safe_print(f"\n[GRUPO {index}/17] Navegando a: {grupo_url}")
            
            try:
                await page.goto(grupo_url, wait_until="domcontentloaded", timeout=45000)
                await asyncio.sleep(2.5)
                
                tiempo_inicio = time.time()
                duracion_grupo = 1.0 * 60
                scroll_count = 0
                
                datos_extraidos = []

                while (time.time() - tiempo_inicio) < duracion_grupo:
                    if page.is_closed():
                        safe_print("[ALERTA] Se cerró la pestaña del navegador.")
                        break

                    scroll_count += 1
                    safe_print(f"  -> [Grupo {index}] Scroll #{scroll_count}...")
                    
                    try:
                        await page.keyboard.press("Escape")
                    except Exception:
                        pass

                    links_perfiles = await page.evaluate("""
                        () => {
                            const links = Array.from(document.querySelectorAll('a[href*="facebook.com/user"], a[href*="facebook.com/profile.php"], a[href*="/user/"]'));
                            return links.map(l => ({ name: l.innerText, href: l.href })).filter(l => l.name.length > 2);
                        }
                    """)
                    
                    texto_pantalla = await page.inner_text("body")
                    if texto_pantalla and len(texto_pantalla) > 150:
                        datos_extraidos.append({
                            "texto": texto_pantalla,
                            "perfiles": links_perfiles[:5]
                        })

                    await page.evaluate("window.scrollBy(0, 1500);")
                    await asyncio.sleep(1.5)

                safe_print(f"[OK] [GRUPO {index}/17 REALIZADO] Evaluando estricto con IA en Python...")

                if datos_extraidos:
                    textos_unidos = "\n--- SECCION MURO Y COMENTARIOS --- \n".join([d["texto"] for d in datos_extraidos[-5:]])
                    telefonos_detectados = extraer_telefonos(textos_unidos)
                    
                    perfiles_encontrados = []
                    for d in datos_extraidos:
                        perfiles_encontrados.extend(d["perfiles"])
                    
                    perfiles_str = "\n".join([f"- Nombre: {p['name']}, Link: {p['href']}" for p in perfiles_encontrados[:8]])
                    
                    prompt = f"""
                    Eres el Cazador Psicográfico e Ingeniero Social de Compradores de AustralDrone.CL (Los Ríos y Los Lagos).

                    PATRONES DE INGENIERÍA SOCIAL DE MIGRACIÓN NORTE -> SUR:
                    1. DETECTAR ORIGEN NORTE / SANTIAGO: Identifica compradores que mencionan expresamente vivir en el Norte (Antofagasta, Calama, Iquique, Copiapó, Coquimbo, La Serena) o Santiago/RM y que expresen deseos de comprar/trasladarse/invertir en el SUR (Puerto Varas, Frutillar, Valdivia, Chiloé).
                       - Frases típicas: 'nos queremos ir al sur', 'soy de antofagasta y busco parcela', 'para irnos de santiago', 'busco en el sur para cambio de vida', 'trabajo en la mineria y busco terreno'.
                       - Registra este hallazgo en la Columna 'Origen Residencia'.
                    2. AUDITORÍA COMPRADOR VS VENDEDOR: DESCARTA VENDEDORES Y ARRIENDOS. Selecciona únicamente compradores.
                    3. TEMPERATURA LEAD: 'HOT 🔥 (Migración Norte/RM)' si busca comprar en el sur, 'WARM 🟡' si evalúa.

                    LINKS DE PERFILES DETECTADOS:
                    {perfiles_str}

                    TEXTO EXTRAÍDO DEL MURO:
                    {textos_unidos[:14000]}

                    Devuelve ÚNICAMENTE un arreglo JSON válido (sin Markdown) alineado a las columnas exactas de Google Sheets:
                    [
                      {{
                        "Fecha": "Fecha u hora del post o {time.strftime('%Y-%m-%d %H:%M')}",
                        "Nombre Comprador": "Nombre completo de la persona",
                        "Teléfono / Contacto": "{telefonos_detectados}",
                        "Origen Residencia": "Norte (Antofagasta/Calama/Iquique) / Santiago-RM / Local Sur",
                        "Tipo de Propiedad": "Parcela/Terreno / Casa / Departamento / Sitio Urbano",
                        "Origen Lead": "Comentario de Publicación / Publicación Principal",
                        "Temperatura Lead": "HOT 🔥 (Migración Norte/RM) / WARM 🟡",
                        "Zona Deseada": "Zona exacta del Sur",
                        "Presupuesto (CLP)": "Monto si figura o 'No especifica'",
                        "Requisitos Clave": "Detalles solicitados",
                        "Link Perfil Facebook": "Link al perfil",
                        "Link Publicación Grupo": "{grupo_url}",
                        "Estado Gestión": "Nuevo"
                      }}
                    ]

                    Si no hay compradores reales, responde estrictamente: []
                    """

                    respuesta_ia = await llm.ainvoke(prompt)
                    res_text = respuesta_ia.content if hasattr(respuesta_ia, 'content') else str(respuesta_ia)

                    res_text_clean = res_text.strip()
                    if res_text_clean.startswith("```json"):
                        res_text_clean = res_text_clean[7:]
                    if res_text_clean.startswith("```"):
                        res_text_clean = res_text_clean[3:]
                    if res_text_clean.endswith("```"):
                        res_text_clean = res_text_clean[:-3]
                    res_text_clean = res_text_clean.strip()

                    try:
                        json_parsed = json.loads(res_text_clean)
                    except Exception:
                        json_parsed = []

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
                            print(f"[REPORTES] Guardado en carpeta {agente_nombre.upper()}: {filename}")
                        except Exception as e:
                            print(f"[REPORTES ERROR] {e}")

                    if json_parsed and isinstance(json_parsed, list) and len(json_parsed) > 0:
                        guardar_reporte_agente("CAZADORVENTAS", json_parsed)
                        # Respaldo Local
                        with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
                            log_entry = {
                                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
                                "grupo": grupo_url,
                                "resultado_ia": json_parsed
                            }
                            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
                        
                        # Envío directo en tiempo real por cada comprador a n8n
                        for lead in json_parsed:
                            res_post = requests.post(N8N_WEBHOOK_URL, json=lead)
                            safe_print(f"  └─► 📥 [SHEETS INYECTADO] {lead.get('Nombre Comprador')} en Google Sheets. Status: {res_post.status_code}")

            except Exception as e:
                err_clean = str(e).encode('ascii', 'ignore').decode('ascii')
                safe_print(f"[ERROR EN GRUPO {index}] {err_clean}")

        safe_print("\n[FIN] Recorrido completado con inyección directa a Sheets.")
        await context.close()

if __name__ == "__main__":
    # Cargar configuración dinámica desde el servidor HQ si está disponible
    try:
        r = requests.get("http://localhost:8080/api/agent-config?agent=cazadorventas", timeout=2)
        if r.status_code == 200 and r.json().get('success'):
            cfg = r.json().get('config', {})
            safe_print(f"[CAZADOR FB] Configuración dinámica HQ cargada: {cfg}")
    except Exception:
        pass

    asyncio.run(ejecutar_cazador_produccion_directa())
