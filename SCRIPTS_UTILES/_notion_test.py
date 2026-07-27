import json, urllib.request, base64, datetime

NOTION_KEY = base64.b64decode("bnRuXzQwMjM4ODU4OTM3MXpCTURnOUNNam1TQTZ2UWlNOWp3ZHprSTl5Mkd1NkoyaHo=").decode("utf-8")
NOTION_DB  = "3a995e6c-42b9-8095-bcfa-c35443c57669"

AHORA = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
HOY   = datetime.date.today().isoformat()

# Payload adaptado al schema real de la DB (Notas de Reunion)
# Campos disponibles: 'Nombre de la reunión' (title), 'Fecha' (date), 'Categoria' (multi_select)
payload = json.dumps({
    "parent": {"database_id": NOTION_DB},
    "properties": {
        "Nombre de la reuni\u00f3n": {
            "title": [{"text": {"content": f"[SECRETARIA CAMILA] Cotizacion $100.000 CLP - Ruta 5 Sur Interior ({AHORA})"}}]
        },
        "Fecha": {
            "date": {"start": HOY}
        },
        "Categor\u00eda": {
            "multi_select": [{"name": "Cotizacion"}, {"name": "AustralDrone"}]
        }
    },
    "children": [
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"text": {"content": "Cotizacion Emitida por Secretaria Camila"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"text": {"content": f"Servicio: Operacion de Vuelo Aereo 4K UHD"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"text": {"content": "Equipamiento: DJI Mini 5 Pro"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"text": {"content": "Sector: Ruta 5 Sur Interior - Puerto Varas / Puerto Montt"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"text": {"content": "GPS: -41.373013, -72.999397"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"text": {"content": "Monto: $100.000 CLP | Estado: EMITIDO"}}]
            }
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"text": {"content": f"Email despachado a: vidalparedes.jaime@gmail.com | {AHORA}"}}]
            }
        }
    ]
}).encode("utf-8")

req = urllib.request.Request(
    "https://api.notion.com/v1/pages",
    data=payload,
    headers={
        "Authorization":  f"Bearer {NOTION_KEY}",
        "Content-Type":   "application/json",
        "Notion-Version": "2022-06-28"
    },
    method="POST"
)

try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        print("[OK] Notion page creada!")
        print("  ID:", result.get("id"))
        print("  URL:", result.get("url"))
except Exception as e:
    print("[FAIL] Error:", e)
    # Get the response body for more details
    try:
        body = e.read().decode("utf-8")
        print("  Response body:", body)
    except:
        pass
