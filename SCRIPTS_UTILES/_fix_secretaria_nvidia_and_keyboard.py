import os

# 1. ACTUALIZAR SERVER.JS — Agregar User-Agent a la llamada a NVIDIA API
with open('server.js', 'r', encoding='utf-8') as f:
    server_code = f.read()

old_headers = """headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${nvKey}`,
                        'Content-Length': Buffer.byteLength(postData)
                    }"""

new_headers = """headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${nvKey}`,
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                        'Content-Length': Buffer.byteLength(postData)
                    }"""

if old_headers in server_code:
    server_code = server_code.replace(old_headers, new_headers)
    print("SUCCESS: Added User-Agent header to NVIDIA API call in server.js!")

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(server_code)

# 2. ACTUALIZAR INDEX.HTML — Agregar event.stopPropagation(), focus/blur y auto-focus a secChatInput
with open('index.html', 'r', encoding='utf-8') as f:
    html_code = f.read()

old_textarea = """<textarea id="secChatInput" placeholder="Escribe o dicta aquí tu orden o instrucción para Camila..." 
          style="flex:1; height:45px; background:#0f172a; border:1px solid #f472b6; color:#fff; padding:8px; border-radius:6px; font-size:11px; outline:none; resize:none;"
          onkeydown="if(event.key==='Enter' && !event.shiftKey){ event.preventDefault(); window.submitSecretariaAIChat(); }"></textarea>"""

new_textarea = """<textarea id="secChatInput" placeholder="Escribe o dicta aquí tu orden o instrucción para Camila..." 
          style="flex:1; height:45px; background:#0f172a; border:1px solid #f472b6; color:#fff; padding:8px; border-radius:6px; font-size:11px; outline:none; resize:none;"
          onfocus="disableGameKeyboard()"
          onblur="enableGameKeyboard()"
          onkeydown="event.stopPropagation(); if(event.key==='Enter' && !event.shiftKey){ event.preventDefault(); window.submitSecretariaAIChat(); }"></textarea>"""

if old_textarea in html_code:
    html_code = html_code.replace(old_textarea, new_textarea)
    print("SUCCESS: Added event.stopPropagation() and focus handlers to secChatInput!")

# Auto-focus al abrir el modal de chat de Camila
old_open_chat = """if (initialPrompt) {
    window.setSecretariaPrompt(initialPrompt);
    window.submitSecretariaAIChat();
  }
};"""

new_open_chat = """setTimeout(() => {
    const inp = document.getElementById('secChatInput');
    if (inp) { inp.focus(); disableGameKeyboard(); }
  }, 100);

  if (initialPrompt) {
    window.setSecretariaPrompt(initialPrompt);
    window.submitSecretariaAIChat();
  }
};"""

if old_open_chat in html_code:
    html_code = html_code.replace(old_open_chat, new_open_chat)
    print("SUCCESS: Added auto-focus to secChatInput!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_code)

with open('PHASER_OFFICE.html', 'w', encoding='utf-8') as f:
    f.write(html_code)

print("SUCCESS: Updated index.html and PHASER_OFFICE.html!")
