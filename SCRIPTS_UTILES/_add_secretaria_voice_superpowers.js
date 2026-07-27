const fs = require('fs');
let content = fs.readFileSync('index.html', 'utf8');

// 1. Agregar funciones de reconocimiento y síntesis de voz en index.html
const voiceSuperpowersCode = `
// ═════════════════════════════════════════════════════
//  🎙️ SUPERPODER DE VOZ DE SECRETARÍA CAMILA (WEB SPEECH API)
// ═════════════════════════════════════════════════════
window._isListeningCamila = false;

window.toggleSecretariaVoiceDictation = function() {
  const btn = document.getElementById('btnVoiceDictation');
  const inp = document.getElementById('secChatInput');

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    alert('⚠️ Tu navegador no soporta reconocimiento de voz nativo. Te recomendamos Google Chrome o Microsoft Edge.');
    return;
  }

  if (window._isListeningCamila) {
    window._camilaRecognizer?.stop();
    window._isListeningCamila = false;
    if (btn) {
      btn.style.background = '#1e293b';
      btn.style.color = '#f472b6';
      btn.innerHTML = '🎙️ Dictar por Voz';
    }
    return;
  }

  try {
    const rec = new SpeechRecognition();
    rec.lang = 'es-CL';
    rec.continuous = false;
    rec.interimResults = false;

    rec.onstart = function() {
      window._isListeningCamila = true;
      if (btn) {
        btn.style.background = '#ef4444';
        btn.style.color = '#fff';
        btn.innerHTML = '🔴 Escuchando a Don Jaime...';
      }
    };

    rec.onresult = function(event) {
      const transcript = event.results[0][0].transcript;
      if (inp) {
        inp.value = transcript;
      }
      window._isListeningCamila = false;
      if (btn) {
        btn.style.background = '#10b981';
        btn.style.color = '#fff';
        btn.innerHTML = '✅ Voz Capturada';
        setTimeout(() => {
          btn.style.background = '#1e293b';
          btn.style.color = '#f472b6';
          btn.innerHTML = '🎙️ Dictar por Voz';
        }, 2000);
      }
      // Enviar automáticamente la instrucción dictada por el CEO
      window.submitSecretariaAIChat();
    };

    rec.onerror = function(err) {
      console.warn('Error reconocimiento voz:', err.error);
      window._isListeningCamila = false;
      if (btn) {
        btn.style.background = '#1e293b';
        btn.style.color = '#f472b6';
        btn.innerHTML = '🎙️ Dictar por Voz';
      }
    };

    window._camilaRecognizer = rec;
    rec.start();
  } catch(e) {
    alert('Error iniciando voz: ' + e.message);
  }
};

window.speakCamilaResponse = function(text) {
  if (!('speechSynthesis' in window)) return;
  window.speechSynthesis.cancel();

  const cleanText = text.replace(/\\*/g, '').replace(/#/g, '').substring(0, 250);
  const utter = new SpeechSynthesisUtterance(cleanText);
  utter.lang = 'es-CL';
  utter.rate = 1.05;
  utter.pitch = 1.1;

  const voices = window.speechSynthesis.getVoices();
  const esVoice = voices.find(v => v.lang && v.lang.includes('es'));
  if (esVoice) utter.voice = esVoice;

  window.speechSynthesis.speak(utter);
};
`;

// Insert voiceSuperpowersCode before openSecretariaCuratedProspectsModal definition
const marker = 'window.openSecretariaCuratedProspectsModal = function() {';
if (!content.includes(marker)) {
  console.error('ERROR: openSecretariaCuratedProspectsModal marker not found!');
  process.exit(1);
}

content = content.replace(marker, voiceSuperpowersCode + '\n' + marker);

// Update Quick Action Chips in openSecretariaAIChatModal to include the 🎙️ Dictar por Voz button
const oldInputBar = `<div style="display:flex; gap:8px;">
        <textarea id="secChatInput" placeholder="Escribe aquí tu orden o instrucción para Camila..."`;

const newInputBar = `<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
        <span style="font-size:9px; color:#64748b; font-weight:bold;">💬 DICTADO DIRECTO DE DON JAIME & DOÑA NICOLE:</span>
        <button id="btnVoiceDictation" onclick="window.toggleSecretariaVoiceDictation()" 
          style="background:#1e293b; color:#f472b6; border:1px solid #f472b6; padding:4px 10px; border-radius:14px; font-size:9px; font-weight:bold; cursor:pointer; display:flex; align-items:center; gap:4px;">
          🎙️ Dictar por Voz
        </button>
      </div>
      <div style="display:flex; gap:8px;">
        <textarea id="secChatInput" placeholder="Escribe o dicta aquí tu orden o instrucción para Camila..."`;

if (content.includes(oldInputBar)) {
  content = content.replace(oldInputBar, newInputBar);
}

// Update submitSecretariaAIChat response rendering to trigger speakCamilaResponse
const oldReplyHandling = `botDiv.innerHTML = \`
      <div style="background:#f472b6; color:#000; font-weight:bold; font-size:10px; width:22px; height:22px; border-radius:50%; display:flex; align-items:center; justify-content:center;">C</div>`;

const newReplyHandling = `window.speakCamilaResponse(reply);
    botDiv.innerHTML = \`
      <div style="background:#f472b6; color:#000; font-weight:bold; font-size:10px; width:22px; height:22px; border-radius:50%; display:flex; align-items:center; justify-content:center;">C</div>`;

if (content.includes(oldReplyHandling)) {
  content = content.replace(oldReplyHandling, newReplyHandling);
}

fs.writeFileSync('index.html', content, 'utf8');
fs.copyFileSync('index.html', 'PHASER_OFFICE.html');
console.log('SUCCESS: Voice dictation & audio synthesis added to Secretaría Camila!');
