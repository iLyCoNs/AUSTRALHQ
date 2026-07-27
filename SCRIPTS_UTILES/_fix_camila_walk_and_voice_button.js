const fs = require('fs');
let content = fs.readFileSync('index.html', 'utf8');

// 1. Corregir camilaApproachCEO para usar scene.ceo.sprite.x y scene.ceo.sprite.y
const oldApproachFunc = `window.camilaApproachCEO = function(onArrivedCallback) {
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
};`;

const newApproachFunc = `window.camilaApproachCEO = function(onArrivedCallback) {
  const sec = window.AR ? window.AR['secretaria'] : null;
  if (!sec || !(sec instanceof DeskAgent)) {
    if (onArrivedCallback) onArrivedCallback();
    return;
  }

  const scene = window.officeScene;
  let targetX = 450;
  let targetY = 320;

  if (scene) {
    if (scene.ceo && scene.ceo.sprite) {
      targetX = scene.ceo.sprite.x + 50;
      targetY = scene.ceo.sprite.y + 10;
    } else if (scene.nicole && scene.nicole.sprite) {
      targetX = scene.nicole.sprite.x + 50;
      targetY = scene.nicole.sprite.y + 10;
    }
  }

  console.log('[CAMILA] 🚶‍♀️ Caminando en vivo hacia Don Jaime/CEO en x:' + targetX + ' y:' + targetY);
  sec._showBubble('👩‍💼 ¡Voy enseguida a su posición, Don Jaime!');
  sec.moveTo(targetX, targetY, () => {
    if (sec.sprite) sec.sprite.setFlipX(true);
    sec._setStateSilent('working');
    if (onArrivedCallback) onArrivedCallback();
  });
};`;

if (content.includes(oldApproachFunc)) {
  content = content.replace(oldApproachFunc, newApproachFunc);
} else {
  console.warn('WARNING: oldApproachFunc exact match not found, replacing via regex...');
  content = content.replace(/window\.camilaApproachCEO = function[\s\S]*?};/, newApproachFunc);
}

// 2. Agregar botón brillante de CHAT DE VOZ en el Top Navbar
const oldNavButtons = `<button onclick="window.openPDFStudioModal()" style="background:rgba(244,114,182,0.2); color:#f472b6; border:1px solid rgba(244,114,182,0.5); padding:4px 10px; border-radius:16px; font-size:8.5px; font-weight:bold; cursor:pointer; display:flex; align-items:center; gap:4px; transition:transform 0.15s;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='none'">
    👩‍💼 SECRETARÍA CAMILA
  </button>`;

const newNavButtons = `<button onclick="window.openSecretariaAIChatModal()" style="background:linear-gradient(135deg, rgba(244,114,182,0.3), rgba(236,72,153,0.3)); color:#f472b6; border:1px solid #f472b6; padding:4px 12px; border-radius:16px; font-size:8.5px; font-weight:bold; cursor:pointer; display:flex; align-items:center; gap:4px; transition:transform 0.15s; box-shadow:0 0 10px rgba(244,114,182,0.3);" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='none'">
    👩‍💼 SECRETARÍA CAMILA
  </button>
  <button onclick="window.openSecretariaAIChatModal(); setTimeout(window.toggleSecretariaVoiceDictation, 400);" style="background:linear-gradient(135deg, #10b981, #059669); color:#fff; border:none; padding:4px 12px; border-radius:16px; font-size:8.5px; font-weight:bold; cursor:pointer; display:flex; align-items:center; gap:4px; transition:transform 0.15s; box-shadow:0 0 12px rgba(16,185,129,0.5);" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='none'">
    🎙️ CHAT DE VOZ EN VIVO
  </button>`;

if (content.includes(oldNavButtons)) {
  content = content.replace(oldNavButtons, newNavButtons);
}

fs.writeFileSync('index.html', content, 'utf8');
fs.copyFileSync('index.html', 'PHASER_OFFICE.html');
console.log('SUCCESS: Fixed Jaime sprite position detection and added top navbar Voice Chat button!');
