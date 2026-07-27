import json, urllib.request, base64

NOTION_KEY = base64.b64decode("bnRuXzQwMjM4ODU4OTM3MXpCTURnOUNNam1TQTZ2UWlNOWp3ZHprSTl5Mkd1NkoyaHo=").decode("utf-8")
NOTION_DB  = "3a995e6c-42b9-8095-bcfa-c35443c57669"

req = urllib.request.Request(
    f"https://api.notion.com/v1/databases/{NOTION_DB}",
    headers={
        "Authorization":  f"Bearer {NOTION_KEY}",
        "Notion-Version": "2022-06-28"
    }
)
with urllib.request.urlopen(req, timeout=10) as resp:
    db = json.loads(resp.read().decode("utf-8"))
    props = db.get("properties", {})
    print("Propiedades de la DB Notion:")
    for name, info in props.items():
        print(f"  '{name}' -> type: {info.get('type')}")
    print("\nTitle field:", db.get("title", [{}])[0].get("plain_text", "N/A"))
