import requests, json

url = "http://localhost:8080/api/secretaria/chat"
headers = {"Content-Type": "application/json"}
payload = {"prompt": "novedades en el chatbot?"}

r = requests.post(url, headers=headers, json=payload)
if r.status_code == 200:
    print("STATUS 200 OK!\n")
    print("RESPUESTA REAL EN VIVO DE CAMILA:\n" + (r.json().get('response') or r.json().get('reply')))
else:
    print("ERR:", r.status_code, r.text)
