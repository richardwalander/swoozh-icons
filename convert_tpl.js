await figma.loadAllPagesAsync();
const BLACK = [{ type: "SOLID", color: { r: 0, g: 0, b: 0 } }];
const COLS = 8;
const log = [];
const isKey = n => n.type === "GROUP" && n.findAll(k => "strokeWeight" in k && k.strokeWeight > 0.2).length === 0;
const closed = n => ["ELLIPSE", "RECTANGLE", "POLYGON", "STAR", "BOOLEAN_OPERATION"].includes(n.type) ||
  (n.type === "VECTOR" && (n.vectorPaths.some(p => /z/i.test(p.data)) || (n.strokeAlign && n.strokeAlign !== "CENTER") ||
    (n.vectorNetwork.regions && n.vectorNetwork.regions.length > 0)));
const hasStroke = n => "strokes" in n && n.strokes.some(s => s.visible !== false) && n.strokeWeight > 0;
const hasFill = n => "fills" in n && Array.isArray(n.fills) && n.fills.some(f => f.visible !== false);

function flattenSafe(shape, parent) {
  if (shape.type === "VECTOR") return shape;
  const copy = shape.clone(); parent.appendChild(copy);
  try { const f = figma.flatten([copy], parent); shape.remove(); return f; }
  catch (e) { const left = parent.findOne(n => n.id === copy.id); if (left) left.remove(); return shape; }
}

async function textToVector(n) {
  try { if (n.fontName !== figma.mixed) await figma.loadFontAsync(n.fontName); return figma.flatten([n], n.parent); } catch (e) { return n; }
}

async function cloneInto(cell, target) {
  for (const k of cell.children) {
    if (isKey(k)) continue;
    const c = k.clone(); target.appendChild(c); c.x = k.x; c.y = k.y;
  }
  for (const t of target.findAll(n => n.type === "TEXT")) await textToVector(t);
  for (const g of target.findAll(n => n.type === "GROUP")) { if (!g.removed) figma.ungroup(g); }
}

function makeComponent(label) {
  const c = figma.createComponent();
  c.resize(24, 24); c.fills = []; c.clipsContent = false; c.name = "Style=" + label;
  return c;
}

const SAME = ["rotate-cw", "refresh", "toggle-off", "check-circle-alt", "check-square-alt"];
function fillVariant(comp, name) {
  if (SAME.includes(name)) return false;
  const kids = [...comp.children];
  const ab = n => n.absoluteBoundingBox;
  const cands = kids.filter(n => closed(n) && Math.max(ab(n).width, ab(n).height) >= 12 && Math.min(ab(n).width, ab(n).height) >= 3);
  if (!cands.length) return false;
  const box = cands.reduce((a, b) => (ab(a).width * ab(a).height >= ab(b).width * ab(b).height ? a : b));
  const B = ab(box), bx = B.x - 0.5, by = B.y - 0.5, bw = B.width + 1, bh = B.height + 1;
  const inside = n => { const r = ab(n); return r.x >= bx && r.y >= by && r.x + r.width <= bx + bw && r.y + r.height <= by + bh; };
  const solids = [], cuts = [];
  for (const n of kids) {
    const dest = n === box || !inside(n) ? solids : cuts;
    if (closed(n) || hasFill(n)) {
      const f = n.clone(); comp.appendChild(f);
      if ("strokes" in f) f.strokes = [];
      f.fills = BLACK; dest.push(f);
    }
    if (hasStroke(n)) { const o = n.outlineStroke(); if (o) { comp.appendChild(o); dest.push(o); } }
    n.remove();
  }
  let shape = solids.length > 1 ? figma.union(solids, comp) : solids[0];
  comp.insertChild(0, shape);
  if (cuts.length) shape = figma.subtract([shape, ...cuts], comp, 0);
  const flat = flattenSafe(shape, comp);
  flat.name = "Vector"; flat.fills = BLACK;
  return true;
}

for (const job of JOBS) {
  const page = await figma.getNodeByIdAsync(job.page);
  const grid = page.children.find(n => n.name === job.src).children[0];
  let wrap = page.children.find(n => n.name === job.title && n.type === "FRAME");
  if (wrap) for (const c of [...wrap.children]) c.remove();
  else { wrap = figma.createFrame(); page.appendChild(wrap); wrap.name = job.title; wrap.x = 360; wrap.y = 101; }
  wrap.layoutMode = "HORIZONTAL"; wrap.layoutWrap = "WRAP";
  wrap.itemSpacing = 16; wrap.counterAxisSpacing = 16;
  wrap.paddingLeft = wrap.paddingRight = wrap.paddingTop = wrap.paddingBottom = 24;
  wrap.primaryAxisSizingMode = "FIXED"; wrap.counterAxisSizingMode = "AUTO";
  wrap.resize(48 + COLS * 72 + (COLS - 1) * 16, wrap.height);
  wrap.fills = [{ type: "SOLID", color: { r: 1, g: 1, b: 1 } }]; wrap.cornerRadius = 16;

  const cells = grid.children.flatMap(r => r.children).filter(c => c.children.some(k => !isKey(k)));
  if (cells.length !== job.names.length) return { error: job.title + " cells " + cells.length + " != names " + job.names.length };
  let same = [];
  for (let i = 0; i < cells.length; i++) {
    const oc = makeComponent("Outline"); page.appendChild(oc);
    await cloneInto(cells[i], oc);
    const fc = makeComponent("Filled"); page.appendChild(fc);
    await cloneInto(cells[i], fc);
    let ok = false;
    try { ok = fillVariant(fc, job.names[i]); } catch (e) { log.push("FAIL " + job.names[i] + ": " + e.message); }
    if (!ok) { same.push(job.names[i]); fc.remove(); const c2 = makeComponent("Filled"); page.appendChild(c2); await cloneInto(cells[i], c2); var fcc = c2; } else var fcc = fc;
    for (const c of [oc, fcc]) for (const v of c.findAll(n => "constraints" in n)) v.constraints = { horizontal: "SCALE", vertical: "SCALE" };
    fcc.x = 32;
    const set = figma.combineAsVariants([oc, fcc], wrap);
    set.name = job.names[i];
    set.layoutMode = "HORIZONTAL"; set.itemSpacing = 8;
    set.paddingLeft = set.paddingRight = set.paddingTop = set.paddingBottom = 8;
    set.primaryAxisSizingMode = "AUTO"; set.counterAxisSizingMode = "AUTO";
  }
  log.push(job.title + ": " + cells.length + " sets, filled same as outline: " + same.join(", "));
}
return log;
