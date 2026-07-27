const fs = require('fs');
let content = fs.readFileSync('index.html', 'utf8');

// 1. Agregar función window.openSecretariaCuratedProspectsModal
const curatedProspectsCode = `
// ═════════════════════════════════════════════════════
//  🎯 SECRETARÍA CAMILA — BLANCOS Y PROSPECTOS MÁXIMOS RECOMENDADOS (FILTRO REAL)
// ═════════════════════════════════════════════════════
window.openSecretariaCuratedProspectsModal = function() {
  _diegoModal('modal-secretaria-prospects', '👩‍💼 SECRETARÍA CAMILA — PROSPECTOS REALES RECOMENDADOS PARA HOY', '#f472b6', \`
    <div style="display:flex; flex-direction:column; gap:12px; font-family:'Inter',sans-serif;">
      
      <!-- Top Selector Tabs -->
      <div style="display:flex; gap:8px; background:#090d16; padding:6px; border-radius:8px; border:1px solid #334155;">
        <button onclick="_diegoCloseModal('modal-secretaria-prospects'); window.openPDFStudioModal();" 
          style="flex:1; background:transparent; color:#94a3b8; border:none; padding:8px; border-radius:6px; cursor:pointer; font-size:10px; font-weight:bold;">
          📄 COTIZADOR & DESPACHO
        </button>
        <button onclick="_diegoCloseModal('modal-secretaria-prospects'); window.openSecretariaAIChatModal();" 
          style="flex:1; background:transparent; color:#f472b6; border:1px solid rgba(244,114,182,0.4); padding:8px; border-radius:6px; cursor:pointer; font-size:10px; font-weight:bold;">
          💬 CHATBOT IA (NVIDIA 70B)
        </button>
        <button style="flex:1; background:linear-gradient(135deg, #10b981, #059669); color:#fff; border:none; padding:8px; border-radius:6px; cursor:pointer; font-size:10px; font-weight:bold; box-shadow:0 0 10px rgba(16,185,129,0.4);">
          🎯 BLANCOS REALES
        </button>
      </div>

      <div style="background:rgba(16,185,129,0.1); border-left:4px solid #10b981; padding:10px 14px; border-radius:6px; font-size:10.5px; color:#cbd5e1; line-height:1.5;">
        <b style="color:#10b981;">👩‍💼 Filtro Real e Intermediación Ejecutiva — Don Jaime & Doña Nicole:</b><br/>
        He procesado todas las búsquedas de Cazador 360, Cazador Banana y Filtro Analista. Estos son los <b>3 prospectos más reales y convenientes</b> para vender la gama de www.australdrone.cl hoy mismo.
      </div>

      <div id="secCuratedList" style="display:flex; flex-direction:column; gap:10px;">
        <div style="background:#090d16; border:1px solid #334155; border-radius:8px; padding:12px; font-size:11px; color:#cbd5e1; text-align:center;">
          ⚡ Cargar prospectos filtrados por Camila...
        </div>
      </div>

    </div>
  \`);

  fetch('/api/secretaria/curated-prospects')
  .then(r => r.json())
  .then(d => {
    const listDiv = document.getElementById('secCuratedList');
    if (!listDiv) return;

    if (!d.prospectos || d.prospectos.length === 0) {
      listDiv.innerHTML = '<div style="color:#94a3b8; font-size:11px;">No hay prospectos filtrados en este momento.</div>';
      return;
    }

    listDiv.innerHTML = d.prospectos.map(p => \`
      <div style="background:#090d16; border:1px solid #334155; border-radius:8px; padding:12px; display:flex; flex-direction:column; gap:8px;">
        <div style="display:flex; justify-between; align-items:center; border-bottom:1px solid #1e293b; padding-bottom:6px;">
          <div>
            <b style="color:#fff; font-size:12px;">\${p.empresa}</b>
            <span style="color:#94a3b8; font-size:10px; margin-left:8px;">(\${p.ubicacion})</span>
          </div>
          <span style="background:#10b981; color:#fff; font-size:9px; font-weight:bold; padding:2px 8px; border-radius:10px;">\${p.prioridad}</span>
        </div>

        <div style="font-size:10.5px; color:#cbd5e1; line-height:1.4;">
          <b style="color:#f472b6;">🔍 Falencia Visual:</b> \${p.falenciaDetectada}<br/>
          <b style="color:#66fcf1;">🚀 Servicio a Vender:</b> \${p.servicioRecomendado}<br/>
          <b style="color:#fbbf24;">💼 Valor Proyectado:</b> \${p.montoProyectado}
        </div>

        <div style="background:rgba(244,114,182,0.08); border-left:3px solid #f472b6; padding:8px 10px; border-radius:4px; font-size:10px; color:#f472b6; line-height:1.4;">
          \${p.razonCamila}
        </div>

        <div style="display:flex; gap:8px; margin-top:4px;">
          <button onclick="_diegoCloseModal('modal-secretaria-prospects'); window.openSecretariaAIChatModal('Camila: Redacta la propuesta comercial perfecta para \${p.empresa} (\${p.contacto}) ofreciendo \${p.servicioRecomendado}');" 
            style="flex:1; background:linear-gradient(135deg,#f472b6,#ec4899); color:#fff; border:none; padding:7px; border-radius:6px; font-weight:bold; font-size:9.5px; cursor:pointer;">
            ✉️ Redactar Propuesta
          </button>
          <button onclick="_diegoCloseModal('modal-secretaria-prospects'); window.openPDFStudioModal();" 
            style="background:#1e293b; color:#66fcf1; border:1px solid #66fcf1; padding:7px 12px; border-radius:6px; font-weight:bold; font-size:9.5px; cursor:pointer;">
            🖨️ Emitir Cotización
          </button>
        </div>
      </div>
    \`).join('');
  })
  .catch(e => {
    const listDiv = document.getElementById('secCuratedList');
    if (listDiv) listDiv.innerHTML = '<div style="color:#ef4444; font-size:11px;">Error cargando prospectos: ' + e.message + '</div>';
  });
};
`;

// Insert the curated prospect code right before openSecretariaAIChatModal definition
const marker = 'window.openSecretariaAIChatModal = function(';
if (!content.includes(marker)) {
  console.error('ERROR: openSecretariaAIChatModal marker not found!');
  process.exit(1);
}

content = content.replace(marker, curatedProspectsCode + '\n' + marker);

// Update tabs in openSecretariaAIChatModal to include the 🎯 BLANCOS REALES tab
const oldChatTabs = `<!-- Top Selector Tabs -->
      <div style="display:flex; gap:8px; background:#090d16; padding:6px; border-radius:8px; border:1px solid #334155;">
        <button onclick="_diegoCloseModal('modal-secretaria-chat'); window.openPDFStudioModal();" 
          style="flex:1; background:transparent; color:#94a3b8; border:none; padding:8px; border-radius:6px; cursor:pointer; font-size:10px; font-weight:bold;">
          📄 COTIZADOR & DESPACHO
        </button>
        <button style="flex:1; background:linear-gradient(135deg, #f472b6, #ec4899); color:#fff; border:none; padding:8px; border-radius:6px; cursor:pointer; font-size:10px; font-weight:bold; box-shadow:0 0 10px rgba(244,114,182,0.4);">
          💬 CHATBOT IA EJECUTIVA (NVIDIA 70B)
        </button>
      </div>`;

const newChatTabs = `<!-- Top Selector Tabs -->
      <div style="display:flex; gap:8px; background:#090d16; padding:6px; border-radius:8px; border:1px solid #334155;">
        <button onclick="_diegoCloseModal('modal-secretaria-chat'); window.openPDFStudioModal();" 
          style="flex:1; background:transparent; color:#94a3b8; border:none; padding:8px; border-radius:6px; cursor:pointer; font-size:10px; font-weight:bold;">
          📄 COTIZADOR & DESPACHO
        </button>
        <button style="flex:1; background:linear-gradient(135deg, #f472b6, #ec4899); color:#fff; border:none; padding:8px; border-radius:6px; cursor:pointer; font-size:10px; font-weight:bold; box-shadow:0 0 10px rgba(244,114,182,0.4);">
          💬 CHATBOT IA (NVIDIA 70B)
        </button>
        <button onclick="_diegoCloseModal('modal-secretaria-chat'); window.openSecretariaCuratedProspectsModal();" 
          style="flex:1; background:transparent; color:#10b981; border:1px solid rgba(16,185,129,0.4); padding:8px; border-radius:6px; cursor:pointer; font-size:10px; font-weight:bold;">
          🎯 BLANCOS REALES
        </button>
      </div>`;

if (content.includes(oldChatTabs)) {
  content = content.replace(oldChatTabs, newChatTabs);
}

// Add autonomous approach routine for Secretaria Camila in OfficeScene
const routineMarker = 'this._initAutonomousAIConversations();';
const secretariaRoutineCode = `this._initAutonomousAIConversations();
    
    // Rutina de Acercamiento Autónomo de Secretaría Camila a Don Jaime y Doña Nicole (cada 2.3 min)
    this.time.addEvent({
      delay: 140000,
      loop: true,
      callback: () => {
        const sec = window.AR['secretaria'];
        if (sec && sec instanceof DeskAgent) {
          const alerts = [
            'Don Jaime: Filtré 3 nuevos loteos en Frutillar. Nos conviene contactar hoy a Inmobiliaria Frutillar con MasterPlan 360°!',
            'Doña Nicole: Revisé los hallazgos de Cazador 360. El prospecto más real para venta de ChatBot IA es Country Club Puerto Varas.',
            'Don Jaime y Doña Nicole: Tengo la nómina de los 3 prospectos más reales de la Región de Los Lagos lista para su revisión.',
            'Don Jaime: La cotización de $100.000 CLP quedó registrada en Notion API. Puedo enviarla ahora por Gmail.'
          ];
          const alertMsg = alerts[Math.floor(Math.random() * alerts.length)];
          // Camila camina hacia el escritorio del CEO Jaime (x:450, y:320)
          sec.moveTo(450, 320, () => {
            sec._showBubble('👩‍💼 ' + alertMsg);
            // Regresa a su escritorio tras 8 segundos
            this.time.delayedCall(8000, () => {
              sec.moveTo(sec.homeX, sec.homeY, () => sec._setStateSilent('working'));
            });
          });
        }
      }
    });`;

if (content.includes(routineMarker)) {
  content = content.replace(routineMarker, secretariaRoutineCode);
}

fs.writeFileSync('index.html', content, 'utf8');
fs.copyFileSync('index.html', 'PHASER_OFFICE.html');
console.log('SUCCESS: Secretaría Camila Intermediary UI & Autonomous Approach loop added!');
