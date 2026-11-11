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
const out = [];
for (const [page, s] of all.slice(START, END)) {
  const rec = {page, name: s.name, desc: s.description};
  for (const v of s.children) rec[v.name.includes('Filled') ? 'filled' : 'outline'] = await v.exportAsync({format: 'SVG_STRING'});
  out.push(rec);
}
return {total: all.length, out};
