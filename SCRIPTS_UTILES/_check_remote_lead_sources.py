import requests, json

print("[DIAGNOSTIC] Checking Notion API Database 3a995e6c-42b9-8095-bcfa-c35443c57669...")
notion_url = "https://api.notion.com/v1/databases/3a995e6c-42b9-8095-bcfa-c35443c57669/query"
notion_headers = {
    "Authorization": "Bearer secret_M3t4N0t10nS3cr3tKey2026",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

try:
    r = requests.post(notion_url, headers=notion_headers, json={"page_size": 5}, timeout=8)
    print("NOTION STATUS:", r.status_code)
    if r.status_code == 200:
        results = r.json().get('results', [])
        print(f"FOUND {len(results)} PAGES IN NOTION DB:")
        for idx, p in enumerate(results):
            props = p.get('properties', {})
            print(f"  Page {idx+1}:", json.dumps(props, ensure_ascii=False)[:200])
    else:
        print("NOTION ERR:", r.text[:300])
except Exception as e:
    print("NOTION EXCEPTION:", e)

print("\n[DIAGNOSTIC] Checking Vercel Chatbot API /api/leads...")
try:
    r2 = requests.get("https://chatbot-ad-mocha.vercel.app/api/leads", timeout=8)
    print("VERCEL LEADS STATUS:", r2.status_code)
    if r2.status_code == 200:
        print("VERCEL LEADS:", r2.text)
    else:
        print("VERCEL LEADS ERR:", r2.text[:300])
except Exception as e:
    print("VERCEL EXCEPTION:", e)
