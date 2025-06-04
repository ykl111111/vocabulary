// generateIndex.js
const fs = require('fs');
const path = require('path');

const files = fs.readdirSync('./html').filter(f => f.endsWith('.html'));
const list = JSON.stringify(files, null, 2);

const indexHTML = fs.readFileSync('index.html', 'utf-8');
const newHTML = indexHTML.replace(/const files = \[.*?\];/s, `const files = ${list};`);
fs.writeFileSync('index.html', newHTML);
console.log("✅ index.html updated with file list");
