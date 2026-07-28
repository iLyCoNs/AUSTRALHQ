import requests, json

url = "https://integrate.api.nvidia.com/v1/chat/completions"
headers = {
    "Authorization": "Bearer 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",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Content-Type": "application/json"
}

prompt_camila = (
    "Eres Camila, la Secretaría Ejecutiva, Co-Piloto de Operaciones e Intermediaria Principal de AustralDrone.CL (empresa del CEO Don Jaime Vidal Paredes).\n"
    "Hablas como una ejecutiva brillante de alto nivel en Chile, cálida, despierta, perspicaz, empática y súper resuelta. Cero plantillas robóticas. Te diriges siempre con afecto y respeto ejecutivo ('Don Jaime')."
)

payload = {
    "model": "meta/llama-3.1-70b-instruct",
    "messages": [
        {"role": "system", "content": prompt_camila},
        {"role": "user", "content": "Hola Camila, ¿cuál es nuestra estrategia para las parcelaciones de Frutillar y Puerto Varas hoy?"}
    ],
    "max_tokens": 350,
    "temperature": 0.65
}

r = requests.post(url, headers=headers, json=payload)
if r.status_code == 200:
    reply = r.json()['choices'][0]['message']['content']
    print("STATUS 200 OK!\n")
    print("RESPUESTA HUMANIZADA DE CAMILA:\n" + reply)
else:
    print("ERR:", r.status_code, r.text)
