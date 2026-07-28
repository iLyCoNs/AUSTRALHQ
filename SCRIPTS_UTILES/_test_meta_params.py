import requests, json

token = "EAAOUrF35xC4BSG1uhXGs4ZCOZALk2LV7bCEIDairIZAL4FQwD2BGtpi5XDPzfc6rxUcq1h4OeXxmC5Iy2DbEmQGz2wsudrn5mCtIv1OBLJ1zfQiXmnIpGkDAoZBw4PwYDl3sNLmnTcKYQ2mmkjqNZB5TbLZAIjZBCumf8NocDHKShBVjiHf0R6TH5H9uYLy6wpF9QZDZD"

# Test 1: Me
r1 = requests.get("https://graph.facebook.com/v19.0/me", params={"access_token": token})
print("TEST 1 (/me):", r1.status_code, r1.json())

# Test 2: Accounts / Pages
r2 = requests.get("https://graph.facebook.com/v19.0/me/accounts", params={"access_token": token})
print("TEST 2 (/me/accounts):", r2.status_code, r2.json())

# Test 3: Business Management
r3 = requests.get("https://graph.facebook.com/v19.0/me/businesses", params={"access_token": token})
print("TEST 3 (/me/businesses):", r3.status_code, r3.json())

# Test 4: Ads Archive with different param formats
params_list = [
    {"search_terms": "parcelas", "ad_type": "ALL", "ad_reached_countries": '["CL"]'},
    {"search_terms": "parcelas", "ad_type": "POLITICAL_AND_ISSUE_ADS", "ad_reached_countries": '["CL"]'},
    {"search_terms": "loteo", "ad_type": "ALL", "ad_reached_countries": '["CL"]'}
]

for idx, p in enumerate(params_list, 1):
    p["access_token"] = token
    r = requests.get("https://graph.facebook.com/v19.0/ads_archive", params=p)
    print(f"\nTEST 4.{idx} (/ads_archive):", r.status_code)
    print("RESPONSE:", r.text[:300])
