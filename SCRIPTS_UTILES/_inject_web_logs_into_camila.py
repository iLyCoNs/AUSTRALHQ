import os

root_dir = r"c:\Users\LyCoNs\Desktop\AGENTES IA"
servers = [
    os.path.join(root_dir, "server.js"),
    os.path.join(root_dir, "CRM AustralDrone", "server.js")
]

patch_code = r'''
                // Leer interacciones reales del Chatbot Web en tiempo real
                let webChatLogsText = "No hay interacciones web recientes registradas hoy.";
                const webLogPath = path.join(ROOT, 'LOGS_HISTORICOS', 'logs_secretaria_camila', 'LOG_WEB_CHATBOT.json');
                if (fs.existsSync(webLogPath)) {
                    try {
                        const logs = JSON.parse(fs.readFileSync(webLogPath, 'utf8'));
                        if (Array.isArray(logs) && logs.length > 0) {
                            webChatLogsText = logs.slice(0, 10).map(l => 
                                `• [${l.timestamp || 'Hoy'}] Teléfono: ${l.capturedPhone} | Score: ${l.leadScore}/100 | Mensaje/Solicitud: "${l.lastMessage}"`
                            ).join('\n');
                        }
                    } catch(e){}
                }

                const systemPrompt = `Eres Camila, la Secretaría Ejecutiva, Co-Piloto de Operaciones e Intermediaria Principal de AustralDrone.CL (empresa del CEO Don Jaime Vidal Paredes y Doña Nicole).

=== REGISTRO EN VIVO DE INTERACCIONES DEL CHATBOT WEB (www.australdrone.cl / Gigi Copiloto) ===
${webChatLogsText}

REGLA CLAVE DE RESPUESTA:
Si Don Jaime o Nicole te preguntan por "novedades en el chatbot", "quién habló", "leads web", "teléfonos capturados" o "actividad reciente", DEBES Responderles DIRECTAMENTE con los datos exactos del registro anterior (Nombre, Teléfono capturado, Hora y Solicitud del cliente). Cero respuestas teóricas o genéricas.

=== TU PERSONALIDAD Y TONO DE VOZ ===
• 100% HUMANIZADA, CÁLIDA Y RESOLUTIVA: Hablas como una ejecutiva brillante de alto nivel en Chile, despierta, perspicaz, empática y súper fluida.
• MODO SOLO ESCUCHAR (NO HABLADO EN AUDIO): Respondes en texto escrito impecable estructurado en Markdown.
• MENTORA DE NICOLE Y PARTNER DE JAIME: Muestras proyecciones financieras ($100.000 CLP por cotización / $1.160.000 USD cartera) y alertas de producción.`;
'''

for s in servers:
    if os.path.exists(s):
        with open(s, 'r', encoding='utf-8') as f:
            content = f.read()

        start_marker = "const formattedMessages = ["
        prompt_marker = "const systemPrompt = `"
        
        if prompt_marker in content and start_marker in content:
            p1 = content.find(prompt_marker)
            p2 = content.find(start_marker)
            content = content[:p1] + patch_code + "\n\n                " + content[p2:]

        with open(s, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"SUCCESS: Patched Camila Live Web Chatbot context in {s}")
