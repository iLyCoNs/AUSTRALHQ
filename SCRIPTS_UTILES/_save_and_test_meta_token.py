import os, json, requests

token = "EAAOUrF35xC4BSG1uhXGs4ZCOZALk2LV7bCEIDairIZAL4FQwD2BGtpi5XDPzfc6rxUcq1h4OeXxmC5Iy2DbEmQGz2wsudrn5mCtIv1OBLJ1zfQiXmnIpGkDAoZBw4PwYDl3sNLmnTcKYQ2mmkjqNZB5TbLZAIjZBCumf8NocDHKShBVjiHf0R6TH5H9uYLy6wpF9QZDZD"

root_dir = r"c:\Users\LyCoNs\Desktop\AGENTES IA"
cfg_files = [
    os.path.join(root_dir, "config_secrets.json"),
    os.path.join(root_dir, "CRM AustralDrone", "config_secrets.json")
]

for cfg_path in cfg_files:
    os.makedirs(os.path.dirname(cfg_path), exist_ok=True)
    data = {}
    if os.path.exists(cfg_path):
        try:
            with open(cfg_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception:
            pass
    data["META_ACCESS_TOKEN"] = token
    with open(cfg_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"SUCCESS: Saved META_ACCESS_TOKEN to {cfg_path}")

# Probar API de Meta en vivo
print("\n[META API TEST] Probando conectividad en vivo con graph.facebook.com...")
url_me = "https://graph.facebook.com/v19.0/me"
r_me = requests.get(url_me, params={"access_token": token})
print("STATUS ME:", r_me.status_code)
print("RESPONSE ME:", r_me.json())

url_ads = "https://graph.facebook.com/v19.0/ads_archive"
params_ads = {
    "access_token": token,
    "search_terms": "parcelas",
    "ad_type": "ALL",
    "ad_reached_countries": '["CL"]',
    "limit": 3,
    "fields": "id,page_name,ad_snapshot_url"
}
r_ads = requests.get(url_ads, params=params_ads)
print("\nSTATUS ADS:", r_ads.status_code)
if r_ads.status_code == 200:
    data = r_ads.json().get('data', [])
    print(f"SUCCESS! Encontrados {len(data)} anuncios de parcelas en Chile:")
    for ad in data:
        print(f" - Anuncio ID {ad.get('id')}: {ad.get('page_name')}")
else:
    print("RESPONSE ADS:", r_ads.text)
