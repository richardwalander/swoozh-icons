await figma.loadAllPagesAsync();
let count = 0;
for (const s of figma.root.findAllWithCriteria({types: ["COMPONENT_SET"]})) {
  if (!s.description) { s.description = s.name.split("-").join(", "); count++; }
}
return {count, missing: figma.root.findAllWithCriteria({types: ["COMPONENT_SET"]}).filter(s => !s.description).length};
