const fs = require('fs');
let content = fs.readFileSync('index.html', 'utf8');

// Definición global de _diegoModal y _diegoCloseModal
const modalDefCode = `
// ═════════════════════════════════════════════════════
//  🪟 HELPER GLOBAL DE MODALES (DIEGO / SECRETARÍA CAMILA / LAYOUTS)
// ═════════════════════════════════════════════════════
window._diegoModal = function(id, title, colorHex, bodyHtml) {
  let modal = document.getElementById(id);
  if (!modal) {
    modal = document.createElement('div');
    modal.id = id;
    modal.style.cssText = \`
      position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
      background: rgba(15, 23, 42, 0.8); backdrop-filter: blur(8px);
      z-index: 10000; display: flex; align-items: center; justify-content: center;
      padding: 16px; box-sizing: border-box;
    \`;
    document.body.appendChild(modal);
  }

  modal.innerHTML = \`
    <div style="width: 540px; max-width: 94vw; max-height: 88vh; overflow-y: auto; background: #090d16; border: 2px solid \${colorHex || '#f472b6'}; border-radius: 12px; padding: 20px; color: #fff; font-family: 'Inter', sans-serif; box-shadow: 0 0 30px \${colorHex || '#f472b6'}44;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; border-bottom:1px solid #1e293b; padding-bottom:10px;">
        <h3 style="margin:0; font-size:13px; color:\${colorHex || '#f472b6'}; font-weight:bold; letter-spacing:0.02em;">\${title}</h3>
        <button onclick="window._diegoCloseModal('\${id}')" style="background:transparent; border:none; color:#94a3b8; font-size:18px; cursor:pointer; font-weight:bold; padding:0 4px;" onmouseover="this.style.color='#fff'" onmouseout="this.style.color='#94a3b8'">✕</button>
      </div>
      <div>\${bodyHtml}</div>
    </div>
  \`;

  modal.style.display = 'flex';
};

window._diegoCloseModal = function(id) {
  const modal = document.getElementById(id);
  if (modal) {
    modal.style.display = 'none';
  }
};
`;

const marker = 'window.openZonePainter = function() {';
if (content.includes(marker)) {
  content = content.replace(marker, modalDefCode + '\n' + marker);
  fs.writeFileSync('index.html', content, 'utf8');
  fs.copyFileSync('index.html', 'PHASER_OFFICE.html');
  console.log('SUCCESS: Added _diegoModal and _diegoCloseModal to index.html and PHASER_OFFICE.html!');
} else {
  console.error('ERROR: openZonePainter marker not found!');
  process.exit(1);
}
