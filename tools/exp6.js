await figma.loadAllPagesAsync();
const out = {};
for (const p of figma.root.children) for (const c of p.children)
  if (["Devices", "File icons", "Finance", "Charts", "Home", "Food & beverage", "Transportation"].includes(c.name) && c.type === "FRAME")
    out[c.name] = figma.base64Encode(await c.exportAsync({ format: "PNG", constraint: { type: "SCALE", value: 3 } }));
return out;
