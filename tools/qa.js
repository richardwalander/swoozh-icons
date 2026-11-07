await figma.loadAllPagesAsync();
const sets = figma.root.findAllWithCriteria({types: ["COMPONENT_SET"]});
const names = {}, bad = [], noDesc = [], wrongSize = [], same = [];
for (const s of sets) {
  names[s.name] = (names[s.name] || 0) + 1;
  const v = s.children.map(c => c.name).sort().join("|");
  if (v !== "Style=Filled|Style=Outline") bad.push(s.name + ":" + v);
  if (!s.description) noDesc.push(s.name);
  for (const c of s.children) {
    if (c.width !== 24 || c.height !== 24) wrongSize.push(s.name);
    const vis = c.findAll(n => n.type !== "GROUP" && n.type !== "FRAME");
    if (!vis.length) bad.push(s.name + " EMPTY " + c.name);
    const b = c.absoluteRenderBounds;
    if (!b || b.width < 2 || b.height < 2) bad.push(s.name + " NORENDER " + c.name);
  }
}
const dups = Object.entries(names).filter(([k, v]) => v > 1).map(([k, v]) => k + " x" + v);
return {sets: sets.length, pages: figma.root.children.length, dups, bad, wrongSize: [...new Set(wrongSize)], noDescCount: noDesc.length, noDescSample: noDesc.slice(0, 5),
  stray: figma.root.children.flatMap(p => p.children.filter(c => c.type !== "FRAME").map(c => p.name + ": " + c.name))};
