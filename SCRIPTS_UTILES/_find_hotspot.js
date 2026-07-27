const fs = require('fs');
const c = fs.readFileSync('index.html', 'utf8');
const allOccs = [];
let pos = 0;
const needle = "cazador360' ||";
while((pos = c.indexOf(needle, pos)) !== -1) {
  allOccs.push(pos);
  pos++;
}
console.log('All positions of needle:', allOccs);
if (allOccs.length > 0) {
  console.log('Context:');
  console.log(JSON.stringify(c.substring(allOccs[0]-80, allOccs[0]+200)));
}
