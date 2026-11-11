await figma.loadAllPagesAsync();
const START = __START__, END = __END__;
const all = [];
for (const p of figma.root.children) for (const s of p.findAll(n => n.type === 'COMPONENT_SET')) all.push([p.name, s]);
const hasStroke = n => n.visible !== false && n.strokes && n.strokes.some(s => s.visible !== false) && n.strokeWeight > 0;
const hasFill = n => n.fills && n.fills !== figma.mixed && n.fills.some(f => f.visible !== false);
function outlineIn(parent) {
  for (const c of [...parent.children]) {
    if (c.type === 'BOOLEAN_OPERATION' || !('children' in c)) {
      if (hasStroke(c)) {
        const o = c.outlineStroke();
        if (o) { const i = parent.children.indexOf(c); parent.insertChild(i + 1, o); if (!hasFill(c)) c.remove(); }
      }
    } else outlineIn(c);
  }
}
const out = [], errs = [];
for (const [page, s] of all.slice(START, END)) {
  const rec = {name: s.name};
  for (const v of s.children) {
    const key = v.name.includes('Filled') ? 'filled' : 'outline';
    const f = figma.createFrame(); f.resize(24, 24); f.fills = []; f.x = -20000; f.y = 0; f.clipsContent = true;
    try {
      for (const c of v.children) { const cl = c.clone(); f.appendChild(cl); cl.x = c.x; cl.y = c.y; }
      outlineIn(f);
      const kids = [...f.children];
      const u = kids.length > 1 ? figma.union(kids, f) : kids[0];
      figma.flatten([u], f);
      rec[key + 'Font'] = await f.exportAsync({format: 'SVG_STRING'});
    } catch (e) { errs.push(s.name + '/' + key + ': ' + e); }
    f.remove();
  }
  out.push(rec);
}
return {total: all.length, out, errs};
