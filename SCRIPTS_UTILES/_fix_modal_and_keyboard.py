import re, os

# Leemos index.html
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Actualizar _diegoModal y _diegoCloseModal para desactivar/activar teclado del juego
old_modal_def = """window._diegoModal = function(id, title, colorHex, bodyHtml) {
  let modal = document.getElementById(id);
  if (!modal) {
    modal = document.createElement('div');
    modal.id = id;
    modal.style.cssText = `
      position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
      background: rgba(15, 23, 42, 0.8); backdrop-filter: blur(8px);
      z-index: 10000; display: flex; align-items: center; justify-content: center;
      padding: 16px; box-sizing: border-box;
    `;
    document.body.appendChild(modal);
  }

  modal.innerHTML = `
    <div style="width: 540px; max-width: 94vw; max-height: 88vh; overflow-y: auto; background: #090d16; border: 2px solid ${colorHex || '#f472b6'}; border-radius: 12px; padding: 20px; color: #fff; font-family: 'Inter', sans-serif; box-shadow: 0 0 30px ${colorHex || '#f472b6'}44;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; border-bottom:1px solid #1e293b; padding-bottom:10px;">
        <h3 style="margin:0; font-size:13px; color:${colorHex || '#f472b6'}; font-weight:bold; letter-spacing:0.02em;">${title}</h3>
        <button onclick="window._diegoCloseModal('${id}')" style="background:transparent; border:none; color:#94a3b8; font-size:18px; cursor:pointer; font-weight:bold; padding:0 4px;" onmouseover="this.style.color='#fff'" onmouseout="this.style.color='#94a3b8'">✕</button>
      </div>
      <div>${bodyHtml}</div>
    </div>
  `;

  modal.style.display = 'flex';
};

window._diegoCloseModal = function(id) {
  const modal = document.getElementById(id);
  if (modal) {
    modal.style.display = 'none';
  }
};"""

new_modal_def = """window._diegoModal = function(id, title, colorHex, bodyHtml) {
  let modal = document.getElementById(id);
  if (!modal) {
    modal = document.createElement('div');
    modal.id = id;
    modal.style.cssText = `
      position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
      background: rgba(15, 23, 42, 0.75); backdrop-filter: blur(8px);
      z-index: 10000; display: flex; align-items: center; justify-content: center;
      padding: 16px; box-sizing: border-box;
    `;
    document.body.appendChild(modal);
  }

  modal.innerHTML = `
    <div style="width: 540px; max-width: 94vw; max-height: 88vh; overflow-y: auto; background: #090d16; border: 2px solid ${colorHex || '#f472b6'}; border-radius: 12px; padding: 20px; color: #fff; font-family: 'Inter', sans-serif; box-shadow: 0 0 30px ${colorHex || '#f472b6'}44;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; border-bottom:1px solid #1e293b; padding-bottom:10px;">
        <h3 style="margin:0; font-size:13px; color:${colorHex || '#f472b6'}; font-weight:bold; letter-spacing:0.02em;">${title}</h3>
        <button onclick="window._diegoCloseModal('${id}')" style="background:transparent; border:none; color:#94a3b8; font-size:18px; cursor:pointer; font-weight:bold; padding:0 4px;" onmouseover="this.style.color='#fff'" onmouseout="this.style.color='#94a3b8'">✕</button>
      </div>
      <div>${bodyHtml}</div>
    </div>
  `;

  modal.style.display = 'flex';
  if (typeof disableGameKeyboard === 'function') disableGameKeyboard();
};

window._diegoCloseModal = function(id) {
  const modal = document.getElementById(id);
  if (modal) {
    modal.style.display = 'none';
  }
  if (typeof enableGameKeyboard === 'function') enableGameKeyboard();
};"""

if old_modal_def in content:
    content = content.replace(old_modal_def, new_modal_def)
    print("SUCCESS: Updated _diegoModal with keyboard disable/enable!")

# 2. Actualizar DESK_AGENTS loop para abrir modal instantáneamente sin esperar el callback de la caminata
old_desk_loop = """DESK_AGENTS.forEach(a=>{
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
    });"""

new_desk_loop = """DESK_AGENTS.forEach(a=>{
      const promptTxt = '[E] Hablar con ' + a.name;
      this.hm.add({id:a.id+'-hs',label:a.name,x:a.x,y:a.y,w:140,h:100,prompt:promptTxt,
        onActivate:()=>{
          const ag=window.AR[a.id];
          // 1. Iniciar caminata fluida hacia Don Jaime
          window.agentApproachCEO(a.id);

          // 2. Abrir modal inmediatamente sin congelamientos ni esperas
          if (a.id === 'secretaria') {
            window.openSecretariaAIChatModal();
          } else {
            window.openExecModal(a, ag, this);
          }

          // 3. Programar retorno a escritorio
          window.agentReturnToDesk(a.id);
        }});
    });"""

if old_desk_loop in content:
    content = content.replace(old_desk_loop, new_desk_loop)
    print("SUCCESS: Updated DESK_AGENTS loop to open modal instantly!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('PHASER_OFFICE.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: Saved changes to index.html and PHASER_OFFICE.html!")
