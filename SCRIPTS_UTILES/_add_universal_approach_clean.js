const fs = require('fs');
let content = fs.readFileSync('index.html', 'utf8');

// 1. Agregar agentApproachCEO y agentReturnToDesk right before camilaApproachCEO
const approachCode = `
// ═════════════════════════════════════════════════════
//  🚶‍♂️ ACERCAMIENTO EN VIVO DE CUALQUIER AGENTE IA AL CEO AL PRESIONAR [E] O INTERACTUAR
// ═════════════════════════════════════════════════════
window.agentApproachCEO = function(agentId, onArrivedCallback) {
  const ag = window.AR ? window.AR[agentId] : null;
  if (!ag || !(ag instanceof DeskAgent)) {
    if (onArrivedCallback) onArrivedCallback();
    return;
  }

  const scene = window.officeScene;
  let targetX = ag.homeX;
  let targetY = ag.homeY;

  if (scene) {
    if (scene.ceo && scene.ceo.sprite) {
      const offsetX = (ag.homeX > scene.ceo.sprite.x) ? 55 : -55;
      targetX = scene.ceo.sprite.x + offsetX;
      targetY = scene.ceo.sprite.y + 10;
    } else if (scene.nicole && scene.nicole.sprite) {
      const offsetX = (ag.homeX > scene.nicole.sprite.x) ? 55 : -55;
      targetX = scene.nicole.sprite.x + offsetX;
      targetY = scene.nicole.sprite.y + 10;
    }
  }

  const agentName = ag.name || agentId.toUpperCase();
  console.log('[AGENT APPROACH] 🚶‍♂️ ' + agentName + ' caminando en vivo hacia el CEO en x:' + targetX + ' y:' + targetY);
  ag._showBubble(agentName + ': "¡Voy enseguida a su posición, Don Jaime!"');

  ag.moveTo(targetX, targetY, () => {
    if (ag.sprite) {
      ag.sprite.setFlipX(ag.homeX > targetX);
    }
    ag._setStateSilent('working');
    if (onArrivedCallback) onArrivedCallback();
  });
};

window.agentReturnToDesk = function(agentId) {
  const ag = window.AR ? window.AR[agentId] : null;
  if (!ag || !(ag instanceof DeskAgent)) return;
  setTimeout(() => {
    ag.moveTo(ag.homeX, ag.homeY, () => ag._setStateSilent('working'));
  }, 4500);
};
`;

const marker = 'window.camilaApproachCEO = function(';
if (content.includes(marker)) {
  content = content.replace(marker, approachCode + '\n' + marker);
}

// 2. Reemplazar ÚNICAMENTE el bloque DESK_AGENTS.forEach
const startIdx = content.indexOf('DESK_AGENTS.forEach(a=>{');
const endIdx = content.indexOf('});\n  }', startIdx);
const altEndIdx = content.indexOf('});\r\n  }', startIdx);
const finalEndIdx = endIdx !== -1 ? endIdx + 7 : altEndIdx + 8;

console.log('DESK_AGENTS slice:', startIdx, 'to', finalEndIdx);

const newLoop = `DESK_AGENTS.forEach(a=>{
      const promptTxt = '[E] Interactuar con ' + a.name;
      this.hm.add({id:a.id+'-hs',label:a.name,x:a.x,y:a.y,w:140,h:100,prompt:promptTxt,
        onActivate:()=>{
          const ag=window.AR[a.id];
          window.agentApproachCEO(a.id, ()=>{
            if (a.id === 'secretaria') {
              window.openSecretariaAIChatModal();
            } else {
              window.openExecModal(a, ag, this);
            }
            window.agentReturnToDesk(a.id);
          });
        }});
    });
  }`;

if (startIdx !== -1 && finalEndIdx !== -1) {
  content = content.substring(0, startIdx) + newLoop + content.substring(finalEndIdx);
  fs.writeFileSync('index.html', content, 'utf8');
  fs.copyFileSync('index.html', 'PHASER_OFFICE.html');
  console.log('SUCCESS: Clean surgical replacement complete!');
} else {
  console.error('ERROR: Could not slice DESK_AGENTS block!');
}
