await figma.loadAllPagesAsync();
const BLACK = [{ type: "SOLID", color: { r: 0, g: 0, b: 0 } }];
const COLS = 8;
const log = [];

function scaleConstraints(node) {
  for (const v of node.findAll(n => "constraints" in n && n.type !== "GROUP")) v.constraints = { horizontal: "SCALE", vertical: "SCALE" };
}

function toComponent(frame, label) {
  const c = figma.createComponent();
  c.resize(24, 24);
  c.fills = [];
  c.clipsContent = false;
  frame.parent.appendChild(c);
  for (const ch of [...frame.children]) c.appendChild(ch);
  frame.remove();
  c.name = "Style=" + label;
  scaleConstraints(c);
  return c;
}

function buildFilled(svg, kinds) {
  const fr = figma.createNodeFromSvg(svg);
  try { return buildFilledInner(fr, kinds); } catch (e) { fr.remove(); throw e; }
}

function buildFilledInner(fr, kinds) {
  const vecs = fr.findAll(n => n.type === "VECTOR");
  if (vecs.length !== kinds.length) throw new Error("vector count " + vecs.length + " != " + kinds.length);
  const solids = [], cuts = [], tops = [];
  vecs.forEach((v, i) => {
    const k = kinds[i];
    if (k === "S") solids.push(v);
    else if (k === "CF") cuts.push(v);
    else if (k === "SG") tops.push(v);
    else {
      const o = v.outlineStroke();
      if (o) { fr.appendChild(o); (k === "T" ? solids : k === "TG" ? tops : cuts).push(o); }
      v.remove();
    }
  });
  let shape = solids.length > 1 ? figma.union(solids, fr) : solids[0];
  fr.insertChild(0, shape);
  if (cuts.length) shape = figma.subtract([shape, ...cuts], fr, 0);
  if (tops.length) shape = figma.union([shape, ...tops], fr, 0);
  let flat = shape;
  if (shape.type !== "VECTOR") {
    const copy = shape.clone();
    fr.appendChild(copy);
    try { flat = figma.flatten([copy], fr); shape.remove(); }
    catch (e) { flat = shape; const left = fr.findOne(n => n.id === copy.id); if (left) left.remove(); }
  }
  flat.name = "Vector";
  flat.fills = BLACK;
  flat.strokes = [];
  for (const g of fr.findAll(n => n.type === "GROUP" && n.children.length === 0)) g.remove();
  return fr;
}

for (const cat of DATA) {
  let page = figma.root.children.find(p => p.name === cat.page);
  if (!page) { page = figma.createPage(); page.name = cat.page; }
  let wrap = page.children.find(n => n.name === cat.title && n.type === "FRAME");
  if (!wrap) {
    wrap = figma.createFrame();
    page.appendChild(wrap);
    wrap.name = cat.title;
    wrap.x = page.children.length > 1 ? 360 : 0;
    wrap.y = 101;
  }
  wrap.layoutMode = "HORIZONTAL";
  wrap.layoutWrap = "WRAP";
  wrap.itemSpacing = 16; wrap.counterAxisSpacing = 16;
  wrap.paddingLeft = wrap.paddingRight = wrap.paddingTop = wrap.paddingBottom = 24;
  wrap.primaryAxisSizingMode = "FIXED"; wrap.counterAxisSizingMode = "AUTO";
  wrap.resize(48 + COLS * 72 + (COLS - 1) * 16, wrap.height);
  wrap.fills = [{ type: "SOLID", color: { r: 1, g: 1, b: 1 } }];
  wrap.cornerRadius = 16;

  for (const ic of cat.icons) {
    for (const old of wrap.children.filter(n => n.name === ic.name)) old.remove();
    let f;
    try { f = buildFilled(ic.f, ic.k); } catch (e) { log.push("FAIL " + ic.name + ": " + e.message); continue; }
    let o;
    try { o = ic.ok ? buildFilled(ic.o, ic.ok) : figma.createNodeFromSvg(ic.o); } catch (e) { f.remove(); log.push("FAIL outline " + ic.name + ": " + e.message); continue; }
    page.appendChild(o);
    const oc = toComponent(o, "Outline");
    page.appendChild(f);
    const fc = toComponent(f, "Filled");
    fc.x = 32;
    const set = figma.combineAsVariants([oc, fc], wrap);
    set.name = ic.name;
    set.description = ic.desc;
    set.layoutMode = "HORIZONTAL";
    set.itemSpacing = 8;
    set.paddingLeft = set.paddingRight = set.paddingTop = set.paddingBottom = 8;
    set.primaryAxisSizingMode = "AUTO"; set.counterAxisSizingMode = "AUTO";
    log.push(ic.name);
  }
}
return { built: log.length, names: log };
