const fs = require('fs');
let c = fs.readFileSync('index.html', 'utf8');

c = c.replace(
  "prompt:'[E] Ejecutar Python '+a.name",
  "prompt:(a.id === 'secretaria' ? '[E] Hablar con Secretaría Camila (Nube IA)' : '[E] Ejecutar Python ' + a.name)"
);

c = c.replace(
  "window.openPDFStudioModal();",
  "window.openSecretariaAIChatModal();"
);

fs.writeFileSync('index.html', c, 'utf8');
fs.copyFileSync('index.html', 'PHASER_OFFICE.html');
console.log('SUCCESS: Updated Secretaria prompt label to Nube IA and default click to openSecretariaAIChatModal!');
