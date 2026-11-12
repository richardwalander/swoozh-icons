// Builds the Figma plugin into figma-plugin/dist from the site data written by scripts/build.mjs.
import { readFileSync, writeFileSync, mkdirSync, copyFileSync } from 'node:fs';

const R = new URL('..', import.meta.url).pathname;
const P = R + 'figma-plugin/';
const json = (file) => readFileSync(R + file, 'utf8').replace(/^[^=]*=\s*/, '').trim().replace(/;$/, '');

const data = JSON.parse(json('site/data/icons.js'));
const stroke = JSON.parse(json('site/data/stroke.js'));
// Keep only what the plugin uses: [name, category, tags, outline, filled].
const slim = { categories: data.categories, icons: data.icons.map(([n, c, t, o, f]) => [n, c, t, o, f]) };
const safe = (o) => JSON.stringify(o).replace(/</g, '\\u003c');

mkdirSync(P + 'dist', { recursive: true });
const ui = readFileSync(P + 'src/ui.html', 'utf8')
  .replace('/*DATA*/null', () => safe(slim))
  .replace('/*STROKE*/null', () => safe(stroke));
writeFileSync(P + 'dist/ui.html', ui);
copyFileSync(P + 'src/code.js', P + 'dist/code.js');
console.log(`figma-plugin/dist: ${slim.icons.length} icons, ui.html ${(ui.length / 1024 / 1024).toFixed(2)} MB`);
