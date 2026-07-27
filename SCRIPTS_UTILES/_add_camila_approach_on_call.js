const fs = require('fs');
let content = fs.readFileSync('index.html', 'utf8');

// 1. Definir función window.camilaApproachCEO
const camilaApproachCode = `
// ═════════════════════════════════════════════════════
//  🚶‍♀️ ACERCAMIENTO EN VIVO DE SECRETARÍA CAMILA AL CEO AL LLAMARLA POR CHAT O VOZ
// ═════════════════════════════════════════════════════
window.camilaApproachCEO = function(onArrivedCallback) {
  const sec = window.AR ? window.AR['secretaria'] : null;
  if (!sec || !(sec instanceof DeskAgent)) {
    if (onArrivedCallback) onArrivedCallback();
    return;
  }

  // Buscar posición del CEO activo (Jaime o Nicole) en la escena Phaser
  const scene = window.officeScene;
  let targetX = 450;
  let targetY = 320;

  if (scene) {
    const ceo = scene.ceo;
    const nicole = scene.nicole;
    if (ceo && ceo.active) {
      targetX = ceo.x + 45;
      targetY = ceo.y + 10;
    } else if (nicole && nicole.active) {
      targetX = nicole.x + 45;
      targetY = nicole.y + 10;
    }
  }

  // Camila camina en vivo hacia la posición del CEO
  sec._showBubble('👩‍💼 ¡Voy enseguida Don Jaime!');
  sec.moveTo(targetX, targetY, () => {
    sec._setStateSilent('working');
    if (onArrivedCallback) onArrivedCallback();
  });
};

window.camilaReturnToDesk = function() {
  const sec = window.AR ? window.AR['secretaria'] : null;
  if (!sec || !(sec instanceof DeskAgent)) return;
  setTimeout(() => {
    sec.moveTo(sec.homeX, sec.homeY, () => sec._setStateSilent('working'));
  }, 4000);
};
`;

// Insert camilaApproachCode before window.toggleSecretariaVoiceDictation definition
const marker = 'window.toggleSecretariaVoiceDictation = function() {';
if (!content.includes(marker)) {
  console.error('ERROR: toggleSecretariaVoiceDictation marker not found!');
  process.exit(1);
}

content = content.replace(marker, camilaApproachCode + '\n' + marker);

// Update toggleSecretariaVoiceDictation to trigger approach on voice start
const oldVoiceStart = `rec.onstart = function() {
      window._isListeningCamila = true;`;

const newVoiceStart = `rec.onstart = function() {
      window._isListeningCamila = true;
      window.camilaApproachCEO();`;

if (content.includes(oldVoiceStart)) {
  content = content.replace(oldVoiceStart, newVoiceStart);
}

// Update submitSecretariaAIChat to trigger approach when CEO submits a message
const oldSubmitStart = `window.submitSecretariaAIChat = function() {
  const inp = document.getElementById('secChatInput');`;

const newSubmitStart = `window.submitSecretariaAIChat = function() {
  const inp = document.getElementById('secChatInput');
  window.camilaApproachCEO();`;

if (content.includes(oldSubmitStart)) {
  content = content.replace(oldSubmitStart, newSubmitStart);
}

// Update submitSecretariaAIChat response handler to schedule return to desk
const oldSubmitSuccess = `window.speakCamilaResponse(reply);`;
const newSubmitSuccess = `window.speakCamilaResponse(reply);
    window.camilaReturnToDesk();`;

if (content.includes(oldSubmitSuccess)) {
  content = content.replace(oldSubmitSuccess, newSubmitSuccess);
}

fs.writeFileSync('index.html', content, 'utf8');
fs.copyFileSync('index.html', 'PHASER_OFFICE.html');
console.log('SUCCESS: Dynamic walk and approach loop on call added to Secretaría Camila!');
