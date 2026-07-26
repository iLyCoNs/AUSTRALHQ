import sys
import os
import csv
import json
import asyncio
import base64
import argparse
import re
from datetime import datetime
from pathlib import Path
import aiohttp
from pydantic import BaseModel, Field
try:
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import PydanticOutputParser
except ImportError:
    pass  # Dependencias deben estar instaladas en el entorno

def sp(msg):
    """Print seguro ignorando caracteres problemáticos en consola de Windows."""
    try:
        print(str(msg).encode('ascii', 'ignore').decode('ascii'), flush=True)
    except Exception:
        pass

# Configuraciones
CSV_PATH = r"c:\Users\LyCoNs\Desktop\AGENTES IA\VENDEDORES_MACROLOTES_MASTERPLAN_360.csv"
OUTPUT_DIR = r"c:\Users\LyCoNs\Desktop\AGENTES IA\REPORTES_AGENTES\FILTRO_ANALISTA"
LOCAL_SERVER_URL = "http://localhost:8080/api/lead-result"
REMOTE_SERVER_URL = "https://australhq.onrender.com/api/lead-result"
N8N_WEBHOOK_URL = "https://lycons.app.n8n.cloud/webhook/cazador-leads"

ZONA_SUR = [
    "osorno", "puerto montt", "puerto varas", "llanquihue", "frutillar", 
    "chiloé", "chiloe", "calbuco", "purranque", "río negro", "rio negro", 
    "los lagos", "los ríos", "los rios", "valdivia", "panguipulli"
]

ZONA_FUERA_SUR = [
    "santiago", "valparaíso", "valparaiso", "maule", "biobío", "biobio", 
    "linares", "concepción", "concepcion", "san antonio", "melipilla"
]

class LeadLLMOutput(BaseModel):
    motivo_top: str = Field(description="Por qué es un buen prospecto B2B")
    deal_size_estimado: str = Field(description="Alto (>$5M CLP), Medio ($1-5M CLP), Bajo (<$1M CLP)")
    accion_recomendada: str = Field(description="Texto corto de acción")
    nivel_urgencia: str = Field(description="ALTA, MEDIA, BAJA")

def extraer_superficie(texto):
    if not texto:
        return 0.0
    texto = texto.lower()
    # Buscar números seguidos de has, ha, hectareas, hectáreas
    match = re.search(r'([0-9.,]+)\s*(ha|has|hectarea|hectárea|hectareas|hectáreas)', texto)
    if match:
        val = match.group(1).replace(',', '.')
        try:
            return float(val)
        except:
            return 0.0
    return 0.0

def calcular_score(lead, is_duplicate, config=None):
    if not config:
        config = {}
    min_surf = float(config.get('min_surface_ha', 5.0))
    sur_pts = int(config.get('sur_bonus_points', 20))
    phone_pts = int(config.get('phone_bonus_points', 20))
    
    score = 0
    
    superficie_ha = extraer_superficie(lead.get('Superficie Has', ''))
    if superficie_ha >= min_surf:
        score += 25
        
    ubicacion = lead.get('Ubicacion', '').lower()
    if any(zona in ubicacion for zona in ZONA_SUR):
        score += sur_pts
        
    telefono = lead.get('Telefono Contacto', '').strip()
    if telefono and telefono.lower() != 'ver perfil' and ('+56' in telefono or telefono.startswith('9')):
        score += phone_pts
        
    estado_mp = lead.get('Estado MasterPlan', '').upper()
    if 'SIN MASTERPLAN' in estado_mp:
        score += 15
        
    precio = lead.get('Precio CLP UF', '').strip()
    if precio and precio.lower() != 'no especifica':
        score += 10
        
    tipo_vendedor = lead.get('Tipo Vendedor', '').strip().lower()
    if tipo_vendedor in ['dueño directo', 'dueno directo']:
        score += 10
        
    if any(zona in ubicacion for zona in ZONA_FUERA_SUR):
        score -= 30
        
    if is_duplicate:
        score -= 20
        
    nombre = lead.get('Nombre Vendedor', '').strip()
    if not nombre or nombre.lower() == 'no especifica':
        score -= 15
        
    link_perfil = lead.get('Link Perfil', '').strip()
    link_post = lead.get('Link Post Directo', '').strip()
    if not link_perfil and not link_post:
        score -= 15
        
    return score

class CustomChatOpenAI(ChatOpenAI):
    @property
    def _llm_type(self):
        return "custom-chat-openai"

async def enriquecer_lead_con_llm(lead, llm):
    parser = PydanticOutputParser(pydantic_object=LeadLLMOutput)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Eres un analista B2B experto en calificar leads inmobiliarios. Analiza la información del lead y extrae la información solicitada en el formato exacto.\n{format_instructions}"),
        ("user", "Información del Lead:\nNombre: {nombre}\nUbicación: {ubicacion}\nSuperficie: {superficie}\nPrecio: {precio}\nEstado MasterPlan: {estado_mp}\nNotas: {notas}\nFuente: {fuente}")
    ])
    
    prompt = prompt.partial(format_instructions=parser.get_format_instructions())
    
    try:
        # Timeout de 30s
        async with asyncio.timeout(30):
            chain = prompt | llm | parser
            result = await chain.ainvoke({
                "nombre": lead.get("Nombre Vendedor", ""),
                "ubicacion": lead.get("Ubicacion", ""),
                "superficie": lead.get("Superficie Has", ""),
                "precio": lead.get("Precio CLP UF", ""),
                "estado_mp": lead.get("Estado MasterPlan", ""),
                "notas": lead.get("Detalles", ""),
                "fuente": lead.get("Fuente", "")
            })
            return result
    except Exception as e:
        sp(f"Error enriqueciendo lead {lead.get('Nombre Vendedor')}: {e}")
        return LeadLLMOutput(
            motivo_top="No se pudo analizar (Timeout o Error)",
            deal_size_estimado="Desconocido",
            accion_recomendada="Revisar manualmente",
            nivel_urgencia="MEDIA"
        )

async def enviar_resultados_servidor(data):
    async with aiohttp.ClientSession() as session:
        # Local
        try:
            async with session.post(LOCAL_SERVER_URL, json=data) as response:
                if response.status == 200:
                    sp(f"[+] Enviado correctamente al servidor local WS.")
        except Exception as e:
            sp(f"[-] Error enviando a servidor local: {e}")
            
        # Remote
        try:
            async with session.post(REMOTE_SERVER_URL, json=data) as response:
                if response.status == 200:
                    sp(f"[+] Enviado correctamente al servidor remoto.")
        except Exception as e:
            sp(f"[-] Error enviando a servidor remoto: {e}")

        # n8n Cloud Webhook
        try:
            async with session.post(N8N_WEBHOOK_URL, json=data) as response:
                if response.status in (200, 201):
                    sp(f"[+] Enviado correctamente a n8n Cloud pipeline.")
        except Exception as e:
            sp(f"[-] Error enviando a n8n Cloud: {e}")

        # Telegram Alerta Directa (Garantizado)
        try:
            cfg_f = os.path.join(os.path.dirname(__file__), "config_secrets.json")
            bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
            if not bot_token and os.path.exists(cfg_f):
                try:
                    with open(cfg_f, 'r', encoding='utf-8') as f:
                        bot_token = json.load(f).get("TELEGRAM_BOT_TOKEN")
                except Exception: pass
            chat_id = "1024898120"
            top_leads = data.get("top_leads", [])
            for lead in top_leads:
                if lead.get("score", 0) >= 60:
                    nombre = lead.get('nombre', '—')
                    tel = lead.get('telefono', 'Ver perfil')
                    ubic = lead.get('ubicacion', '—')
                    sup = lead.get('superficie', '—')
                    precio = lead.get('precio') or 'No especificado'
                    score = lead.get('score', 0)
                    deal = lead.get('deal_size_estimado', 'Desconocido')
                    urgencia = lead.get('nivel_urgencia', 'MEDIA')
                    motivo = lead.get('motivo_top', '')
                    accion = lead.get('accion_recomendada', '')
                    l_perfil = lead.get('link_perfil', '')
                    l_post = lead.get('link_post', '')

                    tg_msg = (
                        f"🚨 <b>PROSPECTO CALIFICADO — AustralDrone.CL</b>\n\n"
                        f"👤 <b>{nombre}</b>\n"
                        f"📞 <code>{tel}</code>\n"
                        f"📍 {ubic}\n"
                        f"🌾 {sup}\n"
                        f"💰 {precio}\n\n"
                        f"🎯 <b>Score B2B: {score}/100</b>\n"
                        f"💼 Deal: {deal}\n"
                        f"⚡ Urgencia: {urgencia}\n\n"
                        f"💡 <b>Diagnóstico IA:</b>\n{motivo}\n\n"
                        f"✅ <b>Acción:</b> {accion}\n\n"
                    )
                    if l_perfil: tg_msg += f"🔗 <a href='{l_perfil}'>Ver Perfil Facebook</a> "
                    if l_post: tg_msg += f"| <a href='{l_post}'>Ver Publicación</a>"

                    tg_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                    async with session.post(tg_url, json={"chat_id": chat_id, "text": tg_msg, "parse_mode": "HTML", "disable_web_page_preview": True}) as response:
                        if response.status == 200:
                            sp(f"[+] Alerta Telegram enviada a Celedonio para lead: {nombre}")
                        else:
                            resp_txt = await response.text()
                            sp(f"[-] Telegram API Status {response.status}: {resp_txt}")
        except Exception as e:
            sp(f"[-] Error notificando Telegram directo: {e}")

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--top", type=int, default=20, help="Cantidad de leads a entregar y analizar")
    args = parser.parse_args()
    
    top_n = args.top

    sp(f"[FILTRO] Leyendo CSV y archivos de respaldo históricos...")
    leads = []
    
    # 1. Leer CSV principal
    if os.path.exists(CSV_PATH):
        try:
            with open(CSV_PATH, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    leads.append(row)
            sp(f"[FILTRO] Cargar CSV principal: {len(leads)} filas.")
        except Exception as e:
            sp(f"[-] Error leyendo CSV: {e}")

    # 2. Leer respaldos históricos JSONL y CSV en LOGS_HISTORICOS/ y raíz
    base_dir = r"c:\Users\LyCoNs\Desktop\AGENTES IA"
    log_dirs = [
        os.path.join(base_dir, "LOGS_HISTORICOS", "logs_vendedores_360"),
        os.path.join(base_dir, "LOGS_HISTORICOS", "logs_vendedores_360", "archivos"),
        os.path.join(base_dir, "LOGS_HISTORICOS", "logs_cazador"),
        os.path.join(base_dir, "LOGS_HISTORICOS", "logs_cazador", "ARCHIVOS"),
        os.path.join(base_dir, "logs_vendedores_360"),
        os.path.join(base_dir, "logs_cazador"),
        base_dir
    ]
    
    count_historico = 0
    for ldir in log_dirs:
        if os.path.exists(ldir):
            for file in os.listdir(ldir):
                fpath = os.path.join(ldir, file)
                if os.path.isdir(fpath): continue
                
                # Cargar archivos JSONL
                if file.endswith('.jsonl'):
                    try:
                        with open(fpath, 'r', encoding='utf-8') as f:
                            for line in f:
                                line = line.strip()
                                if not line: continue
                                data = json.loads(line)
                                items = data.get('resultado_ia', []) if isinstance(data, dict) else []
                                if isinstance(items, list):
                                    for item in items:
                                        normalized = {
                                            'Nombre Vendedor': item.get('Nombre Vendedor') or item.get('Nombre Comprador') or item.get('nombre') or '',
                                            'Telefono Contacto': item.get('Teléfono / Contacto') or item.get('telefono') or item.get('Telefono Contacto') or '',
                                            'Ubicacion': item.get('Ubicación Terreno') or item.get('Zona Deseada') or item.get('ubicacion') or item.get('Ubicacion') or '',
                                            'Superficie Has': item.get('Superficie Terreno (Has)') or item.get('Requisitos Clave') or item.get('superficie') or item.get('Superficie Has') or '',
                                            'Precio CLP UF': item.get('Precio Venta (CLP / UF)') or item.get('Presupuesto (CLP)') or item.get('precio') or item.get('Precio CLP UF') or '',
                                            'Estado MasterPlan': item.get('Estado MasterPlan Actual') or item.get('estado_masterplan') or '',
                                            'Link Perfil': item.get('Link Perfil Facebook') or item.get('link_perfil') or '',
                                            'Link Post Directo': item.get('Link Publicación Grupo') or item.get('link_post') or '',
                                            'Detalles': item.get('Detalles Terreno') or item.get('Requisitos Clave') or '',
                                            'Fuente': 'Histórico JSONL'
                                        }
                                        leads.append(normalized)
                                        count_historico += 1
                    except Exception:
                        pass
                # Cargar archivos CSV adicionales (ej: COMPRADORES_PARCELAS_SUR_CHILE_OFICIAL.csv)
                elif file.endswith('.csv') and file not in ['MASTER_LEADS_CALIFICADOS_AUSTRALDRONE.csv']:
                    try:
                        with open(fpath, 'r', encoding='utf-8-sig') as f:
                            reader = csv.DictReader(f)
                            for row in reader:
                                normalized = {
                                    'Nombre Vendedor': row.get('Nombre Vendedor') or row.get('Nombre Comprador') or row.get('nombre') or '',
                                    'Telefono Contacto': row.get('Telefono Contacto') or row.get('Teléfono / Contacto') or row.get('telefono') or '',
                                    'Ubicacion': row.get('Ubicacion') or row.get('Ubicación Terreno') or row.get('Zona Deseada') or row.get('ubicacion') or '',
                                    'Superficie Has': row.get('Superficie Has') or row.get('Superficie Terreno (Has)') or row.get('Requisitos Clave') or row.get('superficie') or '',
                                    'Precio CLP UF': row.get('Precio CLP UF') or row.get('Precio Venta (CLP / UF)') or row.get('Presupuesto (CLP)') or row.get('precio') or '',
                                    'Estado MasterPlan': row.get('Estado MasterPlan') or row.get('Estado MasterPlan Actual') or '',
                                    'Link Perfil': row.get('Link Perfil') or row.get('Link Perfil Facebook') or '',
                                    'Link Post Directo': row.get('Link Post Directo') or row.get('Link Publicación Grupo') or '',
                                    'Detalles': row.get('Detalles') or row.get('Requisitos Clave') or '',
                                    'Fuente': f"CSV Histórico ({file})"
                                }
                                leads.append(normalized)
                                count_historico += 1
                    except Exception:
                        pass

    sp(f"[FILTRO] Total cargado: {len(leads)} prospectos ({count_historico} extraídos del historial JSONL).")
            
    total_leidos = len(leads)
    sp(f"[FILTRO] Total leídos: {total_leidos}")

    # 1. Filtros Duros
    leads_filtrados = []
    eliminados_duros = 0
    for lead in leads:
        nombre = lead.get('Nombre Vendedor', '').strip()
        if not nombre or nombre.lower() == 'no especifica':
            eliminados_duros += 1
            continue
            
        sup_val = extraer_superficie(lead.get('Superficie Has', ''))
        # Solo aplicar filtro si hay una superficie válida detectada, si es 0 (no detectada) lo dejamos pasar
        if sup_val > 0 and sup_val < 0.5:
            eliminados_duros += 1
            continue
            
        leads_filtrados.append(lead)

    sp(f"[FILTRO] Eliminados por filtros duros: {eliminados_duros}")

    # 2. Deduplicación
    seen = set()
    duplicados_count = 0
    
    leads_scoring = []
    for lead in leads_filtrados:
        nombre = lead.get('Nombre Vendedor', '').strip().lower()
        ubicacion = lead.get('Ubicacion', '').strip().lower()
        key = f"{nombre}_{ubicacion}"
        
        is_duplicate = False
        if key in seen:
            is_duplicate = True
            duplicados_count += 1
        else:
            if nombre and ubicacion: # No marcar como unico si estan vacios
                seen.add(key)
                
        # Calculamos score
        score = calcular_score(lead, is_duplicate)
        lead['Score'] = score
        leads_scoring.append(lead)

    sp(f"[FILTRO] Duplicados detectados (penalizados): {duplicados_count}")
    
    total_calificados = len(leads_scoring)
    score_prom = sum(l['Score'] for l in leads_scoring) / total_calificados if total_calificados > 0 else 0
    
    # 3. Ordenar por score
    leads_scoring.sort(key=lambda x: x['Score'], reverse=True)
    
    # Seleccionar Top N
    top_leads_raw = leads_scoring[:top_n]
    
    # Enriquecimiento LLM
    api_key_b64 = "bnZhcGktbGdsWlNVWGRYajhjZmMzU09GR2tObTZvWG9obmF1V3UtcUk2elhibEtMOElBZEdLRXJmdTFQVTFIS3BEczJldQ=="
    api_key = base64.b64decode(api_key_b64).decode('utf-8')
    
    llm = CustomChatOpenAI(
        model="meta/llama-3.1-70b-instruct",
        api_key=api_key,
        base_url="https://integrate.api.nvidia.com/v1",
        temperature=0.3
    )

    sp(f"[FILTRO] Enriqueciendo TOP {len(top_leads_raw)} con Llama 3.1 70B (NVIDIA)...")
    
    tasks = [enriquecer_lead_con_llm(lead, llm) for lead in top_leads_raw]
    llm_results = await asyncio.gather(*tasks)
    
    top_leads_final = []
    for i, (lead, enrichment) in enumerate(zip(top_leads_raw, llm_results), 1):
        top_leads_final.append({
            "rank": i,
            "score": lead.get("Score", 0),
            "nombre": lead.get("Nombre Vendedor", ""),
            "telefono": lead.get("Telefono Contacto", ""),
            "ubicacion": lead.get("Ubicacion", ""),
            "superficie": lead.get("Superficie Has", ""),
            "precio": lead.get("Precio CLP UF", ""),
            "estado_masterplan": lead.get("Estado MasterPlan", ""),
            "link_perfil": lead.get("Link Perfil", ""),
            "link_post": lead.get("Link Post Directo", ""),
            "fuente": lead.get("Fuente", ""),
            "motivo_top": enrichment.motivo_top,
            "deal_size_estimado": enrichment.deal_size_estimado,
            "accion_recomendada": enrichment.accion_recomendada,
            "nivel_urgencia": enrichment.nivel_urgencia
        })

    # Guardar reporte JSON
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"REPORTE_FILTRO_LEADS_{timestamp}.json"
    report_path = os.path.join(OUTPUT_DIR, report_filename)

    # Guardar CSV Maestro Enriquecido
    master_csv_path = r"c:\Users\LyCoNs\Desktop\AGENTES IA\MASTER_LEADS_CALIFICADOS_AUSTRALDRONE.csv"
    csv_headers = [
        "Fecha Procesamiento", "Rank", "Score B2B", "Nombre Vendedor", "Telefono Contacto", 
        "Ubicacion", "Superficie Has", "Precio CLP UF", "Deal Size Estimado", 
        "Nivel Urgencia", "Diagnostico IA", "Accion Recomendada", 
        "Link Perfil Facebook", "Link Publicacion Grupo"
    ]
    file_exists = os.path.exists(master_csv_path)
    try:
        with open(master_csv_path, 'a', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(csv_headers)
            for lead in top_leads_final:
                writer.writerow([
                    datetime.now().strftime("%Y-%m-%d %H:%M"),
                    lead.get("rank"),
                    lead.get("score"),
                    lead.get("nombre"),
                    lead.get("telefono"),
                    lead.get("ubicacion"),
                    lead.get("superficie"),
                    lead.get("precio"),
                    lead.get("deal_size_estimado"),
                    lead.get("nivel_urgencia"),
                    lead.get("motivo_top"),
                    lead.get("accion_recomendada"),
                    lead.get("link_perfil"),
                    lead.get("link_post")
                ])
        sp(f"[FILTRO] CSV Maestro actualizado: {master_csv_path}")
    except Exception as e:
        sp(f"[-] Error guardando CSV Maestro: {e}")
    
    final_json = {
        "agente": "FILTRO_ANALISTA",
        "fecha_hora_local": datetime.now().isoformat(),
        "total_analizados": total_leidos,
        "total_filtrados_duros": eliminados_duros,
        "total_duplicados": duplicados_count,
        "total_calificados": total_calificados,
        "score_promedio": round(score_prom, 2),
        "top_leads": top_leads_final
    }
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(final_json, f, ensure_ascii=False, indent=2)
        
    sp(f"[FILTRO] Reporte JSON guardado en: {report_path}")
    
    # Resumen en consola
    sp("\n" + "="*50)
    sp(f"🏆 TOP 5 LEADS RANKING 🏆")
    sp("="*50)
    for lead in top_leads_final[:5]:
        sp(f"#{lead['rank']} - {lead['nombre']} (Score: {lead['score']})")
        sp(f"📍 {lead['ubicacion']} | 📏 {lead['superficie']} | 📞 {lead['telefono']}")
        sp(f"💡 {lead['motivo_top']}")
        sp(f"💰 Deal: {lead['deal_size_estimado']} | ⚡ Urgencia: {lead['nivel_urgencia']}")
        sp("-" * 50)
        
    sp("[FILTRO] Enviando resultados a servidores WebSocket (Local y Render)...")
    await enviar_resultados_servidor(final_json)
    sp("[FILTRO] Proceso finalizado con éxito.")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
