await figma.loadAllPagesAsync();
const out = {};
for (const nm of ["frying-pan", "sewing-button", "disc"]) {
  const s = figma.root.findOne(n => n.type === "COMPONENT_SET" && n.name === nm);
  const f = s.children.find(c => c.name.includes("Filled"));
  out[nm] = f.findAll(n => n.type === "VECTOR" || n.type === "BOOLEAN_OPERATION").map(v => v.type + ":" + (v.vectorPaths ? v.vectorPaths.map(p => p.windingRule + " " + p.data.length + " " + p.data).join(" | ") : ""));
}
return out;
