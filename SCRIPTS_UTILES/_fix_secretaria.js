const fs = require('fs');
let content = fs.readFileSync('index.html', 'utf8');

// Add secretaria to validFramesMap (after abogada entry)
const oldFrames = `      abogada: {\r\n        idle: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],\r\n        walk: [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],\r\n        working: [24, 25, 26, 28, 29, 31, 35],\r\n        lead: [37, 38, 39, 41, 42, 43, 44, 45]\r\n      }`;

const newFrames = `      abogada: {\r\n        idle: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],\r\n        walk: [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],\r\n        working: [24, 25, 26, 28, 29, 31, 35],\r\n        lead: [37, 38, 39, 41, 42, 43, 44, 45]\r\n      },\r\n      secretaria: {\r\n        idle: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],\r\n        walk: [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],\r\n        working: [24, 25, 26, 27, 28, 29, 30, 31],\r\n        lead: [36, 37, 38, 39, 40, 41, 42, 43]\r\n      }`;

if (content.includes(oldFrames)) {
  content = content.replace(oldFrames, newFrames);
  fs.writeFileSync('index.html', content, 'utf8');
  console.log('SUCCESS: secretaria validFramesMap entry added!');
} else {
  console.log('WARNING: abogada frames not found with CRLF, trying LF...');
  const oldFramesLF = oldFrames.replace(/\r\n/g, '\n');
  const newFramesLF = newFrames.replace(/\r\n/g, '\n');
  if (content.includes(oldFramesLF)) {
    content = content.replace(oldFramesLF, newFramesLF);
    fs.writeFileSync('index.html', content, 'utf8');
    console.log('SUCCESS: secretaria validFramesMap entry added (LF)!');
  } else {
    console.log('WARNING: Could not add frames map, skipping (optional). Continuing...');
  }
}

// Sync to PHASER_OFFICE.html
fs.copyFileSync('index.html', 'PHASER_OFFICE.html');
console.log('SUCCESS: Synced to PHASER_OFFICE.html!');
