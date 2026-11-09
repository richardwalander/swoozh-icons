// tools/export/raw.json (Figma export) -> icons/{outline,filled}/*.svg, icons/icons.json, icons/codepoints.json
import { readFileSync, writeFileSync, mkdirSync, rmSync, existsSync } from 'node:fs';
import { fixSvg } from './pathfix.mjs';
const R = new URL('..', import.meta.url).pathname;
const raw = JSON.parse(readFileSync(R + 'tools/export/raw.json', 'utf8')).icons;
const svg = d => `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="${d}"/></svg>\n`;
const cat = p => p.replace(/^[^A-Za-z]+/, '').replace('Paymen &', 'Payment &').trim();
for (const v of ['outline', 'filled']) { rmSync(R + 'icons/' + v, {recursive: true, force: true}); mkdirSync(R + 'icons/' + v, {recursive: true}); }
const cpFile = R + 'icons/codepoints.json';
const cps = existsSync(cpFile) ? JSON.parse(readFileSync(cpFile, 'utf8')) : {};
let next = Math.max(0xe000 - 1, ...Object.values(cps)) + 1;
const meta = [];
for (const i of raw) {
  writeFileSync(R + `icons/outline/${i.name}.svg`, svg(fixSvg(i.outlineFont)));
  writeFileSync(R + `icons/filled/${i.name}.svg`, svg(fixSvg(i.filledFont)));
  if (!(i.name in cps)) cps[i.name] = next++;
  meta.push({name: i.name, category: cat(i.page), tags: (i.desc || '').split(',').map(t => t.trim()).filter(t => t && t !== i.name)});
}
writeFileSync(R + 'icons/icons.json', JSON.stringify(meta, null, 1) + '\n');
writeFileSync(cpFile, JSON.stringify(cps, null, 1) + '\n');
console.log('icons', meta.length, 'categories', new Set(meta.map(m => m.category)).size);
