const fs = require('fs');
let content = fs.readFileSync('index.html', 'utf8');

// The corrupt merge starts at this exact string (the comment jammed into a function)
// "scene// ══════ ... HERRAMIENTA SECRETARIA"
// And ends after the last submitPDFGeneration definition closing "};"
// then initWebhooks follows

// Step 1: Find where the corruption starts (inside setAmbiencePreset function)
// The clean text before the corruption ends at: "const W = scene.scale.width * 4, H = scene"
// Then immediately the corrupt Secretaria comment block was jammed in

const corruptionStart = content.indexOf('scene.scale.width * 4, H = scene// ');
if (corruptionStart === -1) {
  console.error('Corruption start marker not found!');
  process.exit(1);
}
// The corruption starts right after "H = scene"
const realCutStart = corruptionStart + 'scene.scale.width * 4, H = scene'.length;
console.log('Corruption starts at char:', realCutStart);
console.log('Context:', JSON.stringify(content.substring(realCutStart-20, realCutStart+80)));

// Step 2: Find the end of the corrupt block — the last }; before initWebhooks
const initHooksPos = content.lastIndexOf('initWebhooks();');
const corruptionEnd = content.lastIndexOf('};', initHooksPos);
const realCutEnd = corruptionEnd + 2; // include the };
console.log('Corruption ends at char:', realCutEnd);
console.log('Context:', JSON.stringify(content.substring(realCutEnd - 30, realCutEnd + 60)));

// Step 3: Replace the corrupt block with clean closing code
// The original clean text that should follow "H = scene" is:
// .scale.width * 4;  ... setAmbiencePreset continuation

// Actually the problem is different - the comment was inserted in the middle of:
// const W = scene.scale.width * 4, H = scene.scale.height * 4;

// We need to:
// A) Fix the broken setAmbiencePreset line (restore `. scale.height * 4;`) 
// B) Insert proper Secretaria modal code at end before initWebhooks

// Find the original setAmbiencePreset context to understand clean state
const beforeCorrupt = content.substring(corruptionStart - 200, realCutStart);
console.log('\nContent just before corruption (200 chars):');
console.log(JSON.stringify(beforeCorrupt));
