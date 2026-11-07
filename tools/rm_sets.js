await figma.loadAllPagesAsync();
const kill = {"Nature": ["clover"], "Beauty & care": ["compact"]};
let removed = [];
for (const p of figma.root.children) for (const w of p.children) if (kill[w.name]) for (const s of w.children.filter(c => c.type === "COMPONENT_SET" && kill[w.name].includes(c.name))) { removed.push(s.name); s.remove(); }
return removed;
