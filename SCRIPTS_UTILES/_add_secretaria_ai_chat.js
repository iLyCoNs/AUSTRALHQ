const fs = require('fs');
let content = fs.readFileSync('index.html', 'utf8');

// 1. Agregar openSecretariaAIChatModal y submitSecretariaAIChat
const secretariaAIChatCode = `
// ═════════════════════════════════════════════════════
//  🤖 CHATBOT IA EJECUTIVA SECRETARÍA CAMILA (NVIDIA LLAMA 3.1 70B)
// ═════════════════════════════════════════════════════
window.openSecretariaAIChatModal = function(initialPrompt = '') {
  _diegoModal('modal-secretaria-chat', '👩‍💼 SECRETARÍA CAMILA — CHATBOT IA EJECUTIVA (NVIDIA LLAMA 3.1 70B)', '#f472b6', \`
    <div style="display:flex; flex-direction:column; gap:12px; font-family:'Inter',sans-serif;">
      
      <!-- Top Selector Tabs -->
      <div style="display:flex; gap:8px; background:#090d16; padding:6px; border-radius:8px; border:1px solid #334155;">
        <button onclick="_diegoCloseModal('modal-secretaria-chat'); window.openPDFStudioModal();" 
          style="flex:1; background:transparent; color:#94a3b8; border:none; padding:8px; border-radius:6px; cursor:pointer; font-size:10px; font-weight:bold;">
          📄 COTIZADOR & DESPACHO
        </button>
        <button style="flex:1; background:linear-gradient(135deg, #f472b6, #ec4899); color:#fff; border:none; padding:8px; border-radius:6px; cursor:pointer; font-size:10px; font-weight:bold; box-shadow:0 0 10px rgba(244,114,182,0.4);">
          💬 CHATBOT IA EJECUTIVA (NVIDIA 70B)
        </button>
      </div>

      <div style="background:rgba(244,114,182,0.1); border-left:4px solid #f472b6; padding:10px 14px; border-radius:6px; font-size:10.5px; color:#cbd5e1; line-height:1.5;">
        <b style="color:#f472b6;">👩‍💼 Asistente Virtual Inteligente — Don Jaime & Doña Nicole:</b><br/>
        Procesaré cualquier orden real: optimización de correos B2B, revisión de propuestas, proyecciones comerciales, redacción de minutas o instrucciones personalizadas.
      </div>

      <!-- Quick Action Prompt Chips -->
      <div style="display:flex; flex-wrap:wrap; gap:6px;">
        <button onclick="window.setSecretariaPrompt('Don Jaime: Por favor optimiza el texto del correo B2B para una inmobiliaria en Puerto Varas que comercializa parcelas de 5.000m2.')"
          style="background:#1e293b; color:#66fcf1; border:1px solid #334155; padding:5px 9px; border-radius:14px; font-size:9px; cursor:pointer;">
          ✉️ Optimizar Correo B2B
        </button>
        <button onclick="window.setSecretariaPrompt('Camila, genera una propuesta comercial con foco en ROI y MasterPlan 360° para parcelaciones.')"
          style="background:#1e293b; color:#fbbf24; border:1px solid #334155; padding:5px 9px; border-radius:14px; font-size:9px; cursor:pointer;">
          📈 Propuesta MasterPlan 360°
        </button>
        <button onclick="window.setSecretariaPrompt('Dame una proyección de cartera y resultados para el próximo trimestre de AustralDrone.CL.')"
          style="background:#1e293b; color:#10b981; border:1px solid #334155; padding:5px 9px; border-radius:14px; font-size:9px; cursor:pointer;">
          📊 Proyección de Cartera
        </button>
        <button onclick="window.setSecretariaPrompt('Prepara el resumen ejecutivo listo para Telegram del avance de hoy.')"
          style="background:#1e293b; color:#f472b6; border:1px solid #334155; padding:5px 9px; border-radius:14px; font-size:9px; cursor:pointer;">
          📱 Resumen Telegram 19:00 hrs
        </button>
      </div>

      <!-- Chat History Box -->
      <div id="secChatHistory" style="height:260px; overflow-y:auto; background:#090d16; border:1px solid #334155; border-radius:8px; padding:12px; display:flex; flex-direction:column; gap:10px;">
        <div style="display:flex; gap:8px;">
          <div style="background:#f472b6; color:#000; font-weight:bold; font-size:10px; width:22px; height:22px; border-radius:50%; display:flex; align-items:center; justify-content:center;">C</div>
          <div style="background:#1e293b; color:#cbd5e1; padding:10px 12px; border-radius:8px; font-size:11px; max-width:85%; line-height:1.5;">
            ¡Buenos días Don Jaime y Doña Nicole! Soy <b>Camila</b>, su Secretaría Ejecutiva operada por <b>NVIDIA Llama 3.1 70B</b>. ¿En qué propuesta, correo o análisis de negocios trabajaremos hoy?
          </div>
        </div>
      </div>

      <!-- Input Bar -->
      <div style="display:flex; gap:8px;">
        <textarea id="secChatInput" placeholder="Escribe aquí tu orden o instrucción para Camila..." 
          style="flex:1; height:45px; background:#0f172a; border:1px solid #f472b6; color:#fff; padding:8px; border-radius:6px; font-size:11px; outline:none; resize:none;"
          onkeydown="if(event.key==='Enter' && !event.shiftKey){ event.preventDefault(); window.submitSecretariaAIChat(); }"></textarea>
        <button onclick="window.submitSecretariaAIChat()" 
          style="background:linear-gradient(135deg, #f472b6, #ec4899); color:#fff; font-weight:bold; border:none; padding:0 18px; border-radius:6px; cursor:pointer; font-size:11px; box-shadow:0 0 12px rgba(244,114,182,0.4);">
          ⚡ ENVIAR
        </button>
      </div>

    </div>
  \`);

  if (initialPrompt) {
    window.setSecretariaPrompt(initialPrompt);
    window.submitSecretariaAIChat();
  }
};

window.setSecretariaPrompt = function(txt) {
  const inp = document.getElementById('secChatInput');
  if (inp) inp.value = txt;
};

window.submitSecretariaAIChat = function() {
  const inp = document.getElementById('secChatInput');
  const txt = inp?.value?.trim();
  if (!txt) return;

  const history = document.getElementById('secChatHistory');
  if (!history) return;

  // Render User Message
  const userDiv = document.createElement('div');
  userDiv.style.cssText = 'display:flex; justify-content:flex-end; gap:8px;';
  userDiv.innerHTML = \`
    <div style="background:#0284c7; color:#fff; padding:10px 12px; border-radius:8px; font-size:11px; max-width:85%; line-height:1.5;">
      \${txt.replace(/</g,'&lt;').replace(/>/g,'&gt;')}
    </div>
    <div style="background:#0284c7; color:#fff; font-weight:bold; font-size:10px; width:22px; height:22px; border-radius:50%; display:flex; align-items:center; justify-content:center;">CEO</div>
  \`;
  history.appendChild(userDiv);
  inp.value = '';

  // Render Loading Indicator
  const loadDiv = document.createElement('div');
  loadDiv.id = 'secLoadingBubble';
  loadDiv.style.cssText = 'display:flex; gap:8px;';
  loadDiv.innerHTML = \`
    <div style="background:#f472b6; color:#000; font-weight:bold; font-size:10px; width:22px; height:22px; border-radius:50%; display:flex; align-items:center; justify-content:center;">C</div>
    <div style="background:#1e293b; color:#f472b6; padding:10px 12px; border-radius:8px; font-size:11px; max-width:85%; line-height:1.5; font-style:italic;">
      ⚡ Camila procesando instrucción con NVIDIA Llama 3.1 70B...
    </div>
  \`;
  history.appendChild(loadDiv);
  history.scrollTop = history.scrollHeight;

  fetch('/api/secretaria/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ prompt: txt })
  })
  .then(r => r.json())
  .then(d => {
    document.getElementById('secLoadingBubble')?.remove();
    const reply = d.reply || 'Don Jaime, he procesado su instrucción.';

    const botDiv = document.createElement('div');
    botDiv.style.cssText = 'display:flex; gap:8px;';
    botDiv.innerHTML = \`
      <div style="background:#f472b6; color:#000; font-weight:bold; font-size:10px; width:22px; height:22px; border-radius:50%; display:flex; align-items:center; justify-content:center;">C</div>
      <div style="background:#1e293b; color:#fff; padding:10px 12px; border-radius:8px; font-size:11px; max-width:85%; line-height:1.6; white-space:pre-wrap; border-left:3px solid #f472b6;">
\${reply.replace(/</g,'&lt;').replace(/>/g,'&gt;')}
        <div style="margin-top:8px; display:flex; gap:6px;">
          <button onclick="navigator.clipboard.writeText(\\\`\${reply.replace(/"/g,'&quot;')}\\\`); alert('📋 Texto copiado al portapapeles!');" style="background:#090d16; color:#66fcf1; border:1px solid #66fcf1; padding:3px 8px; border-radius:4px; font-size:8.5px; cursor:pointer;">📋 Copiar</button>
          <button onclick="_diegoCloseModal('modal-secretaria-chat'); window.openPDFStudioModal();" style="background:#090d16; color:#f472b6; border:1px solid #f472b6; padding:3px 8px; border-radius:4px; font-size:8.5px; cursor:pointer;">📥 Ir a Cotizador</button>
        </div>
      </div>
    \`;
    history.appendChild(botDiv);
    history.scrollTop = history.scrollHeight;
  })
  .catch(e => {
    document.getElementById('secLoadingBubble')?.remove();
    const errDiv = document.createElement('div');
    errDiv.style.cssText = 'display:flex; gap:8px;';
    errDiv.innerHTML = \`
      <div style="background:#ef4444; color:#fff; font-size:11px; padding:8px 12px; border-radius:6px;">Error procesando chat: \${e.message}</div>
    \`;
    history.appendChild(errDiv);
  });
};
`;

// Insert the code right before openPDFStudioModal definition
const marker = 'window.openPDFStudioModal = function() {';
if (!content.includes(marker)) {
  console.error('ERROR: openPDFStudioModal marker not found!');
  process.exit(1);
}

content = content.replace(marker, secretariaAIChatCode + '\n' + marker);

// Update openPDFStudioModal header to add tab navigation buttons
const oldHeader = `<div style="display:flex;flex-direction:column;gap:14px;font-family:'Inter',sans-serif;">`;
const newHeader = `<div style="display:flex;flex-direction:column;gap:14px;font-family:'Inter',sans-serif;">
      
      <!-- Top Selector Tabs -->
      <div style="display:flex; gap:8px; background:#090d16; padding:6px; border-radius:8px; border:1px solid #334155;">
        <button style="flex:1; background:linear-gradient(135deg, #0284c7, #0369a1); color:#fff; border:none; padding:8px; border-radius:6px; cursor:pointer; font-size:10px; font-weight:bold; box-shadow:0 0 10px rgba(2,132,199,0.4);">
          📄 COTIZADOR & DESPACHO
        </button>
        <button onclick="_diegoCloseModal('modal-pdf-studio'); window.openSecretariaAIChatModal();" 
          style="flex:1; background:transparent; color:#f472b6; border:1px solid rgba(244,114,182,0.4); padding:8px; border-radius:6px; cursor:pointer; font-size:10px; font-weight:bold;">
          💬 CHATBOT IA EJECUTIVA (NVIDIA 70B)
        </button>
      </div>`;

if (content.includes(oldHeader)) {
  content = content.replace(oldHeader, newHeader);
}

fs.writeFileSync('index.html', content, 'utf8');
fs.copyFileSync('index.html', 'PHASER_OFFICE.html');
console.log('SUCCESS: Secretaría Camila AI Chatbot (NVIDIA 70B) added to index.html and synced to PHASER_OFFICE.html!');
