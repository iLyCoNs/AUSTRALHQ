const fs = require('fs');
let c = fs.readFileSync('index.html', 'utf8');

// Find index of window.saveCurrentTVEditorConfig
const idx = c.indexOf('window.saveCurrentTVEditorConfig');
console.log('saveCurrentTVEditorConfig at:', idx);

// Look backwards from saveCurrentTVEditorConfig to find where _setupHotspots ended
const beforeStr = c.substring(idx - 200, idx);
console.log('Before saveCurrentTVEditorConfig:', JSON.stringify(beforeStr));

const fixPart = `    DESK_AGENTS.forEach(a=>{
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
    });
  }

  _connectWebhooks(){
    window.changePhaserState=(ev)=>{
      const who=ev.target||'ceo',dir=who==='nicole'?this.nicole:this.ceo;
      if(dir&&(who==='ceo'||who==='nicole')){
        switch(ev.action){
          case 'moving':{const p=(ev.destination||'900,500').split(',');const dx=parseFloat(p[0]),dy=parseFloat(p[1]);if(!isNaN(dx))dir.moveTo(dx,dy);break;}
          case 'scraping_active':dir.startWork(ev.duration||10000);break;
          case 'lead_qualified':dir.startCelebrate();this._particles(dir.x,dir.y,who==='nicole'?'#ec4899':'#fbbf24');break;
          case 'idle':dir.goIdle();break;
        }return;
      }
      const da=window.AR[who];
      if(da instanceof DeskAgent){const s=ev.action==='lead_qualified'?'lead':ev.action==='scraping_active'?'working':'idle';da.setState(s);}
    };
    window.ceoGo    =(a,e)=>_dispatch(Object.assign({action:a,target:'ceo'},e||{}),'API');
    window.nicoleGo =(a,e)=>_dispatch(Object.assign({action:a,target:'nicole'},e||{}),'API');
    window.agentGo  =(id,a,e)=>_dispatch(Object.assign({action:a,target:id},e||{}),'API');
    window.triggerWorkflow=wfTrigger;
  }
}

window.saveCurrentTVEditorConfig`;

// Perform replacement from DESK_AGENTS.forEach to window.saveCurrentTVEditorConfig
const deskIdx = c.indexOf('DESK_AGENTS.forEach(a=>{');
console.log('DESK_AGENTS at:', deskIdx);

if (deskIdx !== -1 && idx !== -1) {
  const beforeDesk = c.substring(0, deskIdx);
  const afterSave = c.substring(idx);
  const fixed = beforeDesk + fixPart + '\n\n' + afterSave;
  fs.writeFileSync('index.html', fixed, 'utf8');
  fs.copyFileSync('index.html', 'PHASER_OFFICE.html');
  console.log('SUCCESS: Completely repaired index.html and PHASER_OFFICE.html!');
}
