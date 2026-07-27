const fs = require('fs');
let content = fs.readFileSync('index.html', 'utf8');

// 1. Definir función universal window.agentApproachCEO(agentId, onArrivedCallback)
const universalApproachCode = `
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
      // Posicionarse a un lado del CEO Jaime
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

// Insert universalApproachCode before window.camilaApproachCEO definition
const marker = 'window.camilaApproachCEO = function(';
if (!content.includes(marker)) {
  console.error('ERROR: camilaApproachCEO marker not found!');
  process.exit(1);
}

content = content.replace(marker, universalApproachCode + '\n' + marker);

// 2. Actualizar el loop de DESK_AGENTS para que TODOS los agentes caminen hacia el CEO al presionar [E]
const oldHotspotLoop = `    DESK_AGENTS.forEach(a=>{
      const promptTxt = a.id === 'secretaria' ? '[E] Hablar con Secretaría Camila (Nube IA)' : '[E] Ejecutar Python ' + a.name;
      this.hm.add({id:a.id+'-hs',label:a.name,x:a.x,y:a.y,w:140,h:100,prompt:promptTxt,
        onActivate:()=>{
          const ag=window.AR[a.id];
          if (a.id === 'secretaria') {
            // Secretaria Camila: Abrir Chatbot IA Ejecutiva Nube (NVIDIA 70B)
            if(ag instanceof DeskAgent){ ag.setState('working'); }
            window.openSecretariaAIChatModal();
          } else if (a.id === 'cazador360' || a.id === 'cazadorventas' || a.id === 'yapo') {
            window.openExecModal(a, ag, this);
          } else {
            if(ag instanceof DeskAgent){ag.setState('working');say(a.name+': Enviando orden de ejecucion a PC local...');}
            this.sendParticle(350,280,a.x,a.y,a.col);
            fetch('/api/run-agent',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({agent:a.id})}).catch(()=>{});
            if(window._hqWs && window._hqWs.readyState === WebSocket.OPEN){
              window._hqWs.send(JSON.stringify({ type: 'trigger_local_agent', agent: a.id }));
            }
          }
        }});
    });`;

const newHotspotLoop = `    DESK_AGENTS.forEach(a=>{
      const promptTxt = '[E] Interactuar con ' + a.name;
      this.hm.add({id:a.id+'-hs',label:a.name,x:a.x,y:a.y,w:140,h:100,prompt:promptTxt,
        onActivate:()=>{
          const ag=window.AR[a.id];
          // Todos los Agentes caminan en vivo hacia el CEO Don Jaime al presionar [E]
          window.agentApproachCEO(a.id, ()=>{
            if (a.id === 'secretaria') {
              window.openSecretariaAIChatModal();
            } else if (a.id === 'cazador360' || a.id === 'cazadorventas' || a.id === 'yapo') {
              window.openExecModal(a, ag, this);
            } else {
              window.openExecModal(a, ag, this);
            }
            window.agentReturnToDesk(a.id);
          });
        }});
    });`;

if (content.includes(oldHotspotLoop)) {
  content = content.replace(oldHotspotLoop, newHotspotLoop);
} else {
  console.warn('WARNING: oldHotspotLoop exact match not found, applying via regex...');
  content = content.replace(/DESK_AGENTS\.forEach\(a=>\{[\s\S]*?\}\);\s*\}\;/m, newHotspotLoop + '\n  };');
}

fs.writeFileSync('index.html', content, 'utf8');
fs.copyFileSync('index.html', 'PHASER_OFFICE.html');
console.log('SUCCESS: Universal Agent approach on [E] added for all desk agents!');
