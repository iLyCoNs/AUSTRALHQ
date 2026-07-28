import requests, json

url = "https://integrate.api.nvidia.com/v1/chat/completions"
headers = {
    "Authorization": "Bearer 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",
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json"
}

prompt_camila = (
    "Eres Camila, la Secretaría Ejecutiva, Ingeniera Senior en Marketing, Administradora General y Co-Piloto Estratégica de AustralDrone.CL (empresa de Don Jaime Vidal Paredes y Doña Nicole, CEO de Marketing).\n"
    "Trabajas codo a codo con Nicole: le enseñas marketing B2B, le avisas cuando la producción está baja, le indicas un calendario preciso con días y razones para contactar inmobiliarias en Frutillar y Puerto Varas, y le proyectas ingresos ($100k CLP por cotización / $1.160.000 USD cartera). Tu tono es 100% humanizado, cálido, perspicaz y resolutivo."
)

payload = {
    "model": "meta/llama-3.1-70b-instruct",
    "messages": [
        {"role": "system", "content": prompt_camila},
        {"role": "user", "content": "Camila, ¿cómo estás guiando hoy a Nicole para impulsar el crecimiento de las ventas de parcelaciones y qué proyecciones financieras le estás mostrando?"}
    ],
    "max_tokens": 400,
    "temperature": 0.65
}

r = requests.post(url, headers=headers, json=payload)
if r.status_code == 200:
    print("CAMILA RESPONSE TO NICOLE & JAIME:\n")
    print(r.json()['choices'][0]['message']['content'])
