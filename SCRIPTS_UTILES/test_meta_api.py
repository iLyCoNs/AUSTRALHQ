import requests
import json

META_TOKEN = "EAAOfxzsABmkBSMDldyZCtZAZByEZAZB1REGLFk30wgWAyHoX374xqZCcvOwkZAfZCQqsv0qxFZAIcKwtwtTo2am9WOq3v8e0mIZATBR8BVeAVZA966SG6ZCPViDYAGIuB2FBbCzXuMkfDsd0G0vdwuDZBhjp0QOmZCbdRt7gTZBUiI5cdlZBVFFicWm6lAVKxufI5iBRV4ONaduIKiw7BsZCf1l8ebZBDNsJESpy4ARQ4aMVTI7GsVQjf7rAh6JZCD5WJWWBonlsZB4NlNUWcdWCKL16tYulZAdxPSD8GyQZDZD"

def test_meta_me():
    url = "https://graph.facebook.com/v19.0/me"
    r = requests.get(url, params={"access_token": META_TOKEN})
    print("META ME:", r.json())

def test_meta_ads():
    url = "https://graph.facebook.com/v19.0/ads_archive"
    params = {
        "access_token": META_TOKEN,
        "search_terms": "parcelas osorno",
        "ad_type": "ALL",
        "ad_reached_countries": '["CL"]',
        "limit": 3
    }
    r = requests.get(url, params=params)
    print("META ADS STATUS:", r.status_code)
    print("META ADS:", json.dumps(r.json(), indent=2, ensure_ascii=False)[:500])

def test_meta_pages():
    url = "https://graph.facebook.com/v19.0/me/accounts"
    r = requests.get(url, params={"access_token": META_TOKEN})
    print("META PAGES:", r.json())

if __name__ == "__main__":
    test_meta_me()
    test_meta_pages()
