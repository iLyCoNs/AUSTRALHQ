import requests
import json
import os

def load_secret(key_name, default=""):
    val = os.environ.get(key_name)
    if val: return val
    cfg_file = os.path.join(os.path.dirname(__file__), "config_secrets.json")
    if os.path.exists(cfg_file):
        try:
            with open(cfg_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get(key_name, default)
        except Exception:
            pass
    return default

def get_n8n_key():
    return load_secret("N8N_API_KEY")

def get_nv_key():
    return load_secret("NVIDIA_API_KEY")

def get_tg_token():
    return load_secret("TELEGRAM_BOT_TOKEN")

API_KEY = get_n8n_key()
BASE_URL = "https://lycons.app.n8n.cloud/api/v1/workflows/jAifbwHrD0MAGO5m"

headers = {
    "X-N8N-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

workflow_data = {
    "name": "SUPER AGENTE CAZADOR B2B DUAL (MasterPlan 360 + Automatizacion IA PYMEs)",
    "nodes": [
        {
            "parameters": {
                "httpMethod": "POST",
                "path": "cazador-b2b-dual",
                "responseMode": "onReceived",
                "options": {}
            },
            "id": "node-webhook",
            "name": "1. Webhook / Form Trigger",
            "type": "n8n-nodes-base.webhook",
            "typeVersion": 1,
            "position": [100, 300]
        },
        {
            "parameters": {
                "values": {
                    "string": [
                        {"name": "rubroTarget", "value": "={{ $json.body.rubro || 'Inmobiliaria' }}"},
                        {"name": "ubicacionTarget", "value": "={{ $json.body.ubicacion || 'Puerto Montt' }}"},
                        {"name": "ofertaServicio", "value": "={{ $json.body.oferta_target || 'MASTERPLAN_360' }}"},
                        {"name": "estiloEmail", "value": "={{ $json.body.estilo_email || 'Consultivo B2B High Value' }}"}
                    ]
                }
            },
            "id": "node-set-fields",
            "name": "2. Set / Normalizar Variables",
            "type": "n8n-nodes-base.set",
            "typeVersion": 1,
            "position": [320, 300]
        },
        {
            "parameters": {
                "url": "https://api.apify.com/v2/acts/compass~google-maps-scraper/run-sync-get-dataset-items",
                "sendQuery": True,
                "queryParameters": {
                    "parameters": [
                        {"name": "searchStringsArray", "value": "={{ $json.rubroTarget + ' en ' + $json.ubicacionTarget }}"},
                        {"name": "maxCrawledPlacesPerSearch", "value": "15"}
                    ]
                },
                "options": {}
            },
            "id": "node-gmaps-scraper",
            "name": "3. Scraper Google Maps / Apify",
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 3,
            "position": [540, 300]
        },
        {
            "parameters": {
                "batchSize": 1,
                "options": {}
            },
            "id": "node-split-batches",
            "name": "4. Loop Item por Item (Split Batches)",
            "type": "n8n-nodes-base.splitInBatches",
            "typeVersion": 1,
            "position": [760, 300]
        },
        {
            "parameters": {
                "conditions": {
                    "string": [
                        {
                            "value1": "={{ $json.website || '' }}",
                            "operation": "isNotEmpty"
                        }
                    ]
                }
            },
            "id": "node-if-website",
            "name": "5. IF Tiene Web Valida",
            "type": "n8n-nodes-base.if",
            "typeVersion": 1,
            "position": [980, 300]
        },
        {
            "parameters": {
                "url": "={{ $json.website }}",
                "options": {
                    "redirect": {
                        "redirect": {}
                    }
                }
            },
            "id": "node-firecrawl",
            "name": "6. Extractor Web & Firecrawl (Email Contacto)",
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 3,
            "position": [1200, 200]
        },
        {
            "parameters": {
                "method": "POST",
                "url": "https://integrate.api.nvidia.com/v1/chat/completions",
                "sendHeaders": True,
                "headerParameters": {
                    "parameters": [
                        {"name": "Authorization", "value": f"Bearer {get_nv_key()}"},
                        {"name": "Content-Type", "value": "application/json"}
                    ]
                },
                "sendBody": True,
                "bodyParameters": {
                    "parameters": [
                        {"name": "model", "value": "meta/llama-3.1-70b-instruct"},
                        {"name": "messages", "value": "=[{\"role\": \"user\", \"content\": \"Eres el Agente Comercial Senior de AustralDrone 360 en Chile.\\nGenera un correo frio B2B hiper-personalizado:\\nEMPRESA: {{$json.title}}\\nRUBRO: {{$node['2. Set / Normalizar Variables'].json.rubroTarget}}\\nOFERTA: {{$node['2. Set / Normalizar Variables'].json.ofertaServicio}}\\nUBICACION: {{$json.city || $node['2. Set / Normalizar Variables'].json.ubicacionTarget}}\\nWEB: {{$json.website}}\\n\\nDevuelve JSON: {\\\"asunto\\\":\\\"...\\\", \\\"cuerpo\\\":\\\"...\\\", \\\"email_extraido\\\":\\\"...\\\"}\"}]"}
                    ]
                },
                "options": {}
            },
            "id": "node-ai-generator",
            "name": "7. AI Generation (NVIDIA Llama 3.1 70B)",
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 3,
            "position": [1420, 200]
        },
        {
            "parameters": {
                "method": "POST",
                "url": f"https://api.telegram.org/bot{get_tg_token()}/sendMessage",
                "sendBody": True,
                "bodyParameters": {
                    "parameters": [
                        {"name": "chat_id", "value": "1024898120"},
                        {"name": "text", "value": "=🎯 [SUPER AGENTE B2B DUAL - N8N]\n\n📍 Lead: {{$json.title}}\n🗺️ Ubicación: {{$json.city || $node['2. Set / Normalizar Variables'].json.ubicacionTarget}}\n📞 Teléfono: {{$json.phone || 'Ver Web'}}\n🌐 Web: {{$json.website}}\n💡 Asunto: {{$json.choices[0].message.content}}\n"},
                        {"name": "parse_mode", "value": "HTML"}
                    ]
                },
                "options": {}
            },
            "id": "node-telegram-send",
            "name": "8. Telegram Lead Alert",
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 3,
            "position": [1640, 200]
        }
    ],
    "connections": {
        "1. Webhook / Form Trigger": {
            "main": [[{"node": "2. Set / Normalizar Variables", "type": "main", "index": 0}]]
        },
        "2. Set / Normalizar Variables": {
            "main": [[{"node": "3. Scraper Google Maps / Apify", "type": "main", "index": 0}]]
        },
        "3. Scraper Google Maps / Apify": {
            "main": [[{"node": "4. Loop Item por Item (Split Batches)", "type": "main", "index": 0}]]
        },
        "4. Loop Item por Item (Split Batches)": {
            "main": [[{"node": "5. IF Tiene Web Valida", "type": "main", "index": 0}]]
        },
        "5. IF Tiene Web Valida": {
            "main": [
                [{"node": "6. Extractor Web & Firecrawl (Email Contacto)", "type": "main", "index": 0}],
                [{"node": "7. AI Generation (NVIDIA Llama 3.1 70B)", "type": "main", "index": 0}]
            ]
        },
        "6. Extractor Web & Firecrawl (Email Contacto)": {
            "main": [[{"node": "7. AI Generation (NVIDIA Llama 3.1 70B)", "type": "main", "index": 0}]]
        },
        "7. AI Generation (NVIDIA Llama 3.1 70B)": {
            "main": [[{"node": "8. Telegram Lead Alert", "type": "main", "index": 0}]]
        }
    },
    "settings": {}
}

res = requests.put(BASE_URL, headers=headers, json=workflow_data)
print("Status Code:", res.status_code)
if res.status_code in [200, 201]:
    d = res.json()
    print("[SUCCESS] WORKFLOW CREADO EN N8N CLOUD CON EXITO!")
    print(f"ID Workflow: {d.get('id')}")
    print(f"Nombre: {d.get('name')}")
else:
    print("Error:", res.text)
