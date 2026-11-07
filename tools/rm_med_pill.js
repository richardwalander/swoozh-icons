await figma.loadAllPagesAsync();
const page = figma.root.children.find(p => p.name === "💊 Medical");
const wrap = page.children.find(n => n.name === "Medical");
const hits = wrap.children.filter(n => n.type === "COMPONENT_SET" && n.name === "pill");
for (const h of hits) h.remove();
return {removed: hits.length, shapesPill: figma.root.findAll(n => n.type === "COMPONENT_SET" && n.name === "pill").map(n => n.parent.name)};
