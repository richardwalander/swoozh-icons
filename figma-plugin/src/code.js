// Swoozh Icons for Figma: main thread. The UI sends ready-made SVG markup; this side turns it into vectors.
figma.showUI(__html__, { width: 368, height: 600, themeColors: true });

const CONTAINERS = ['FRAME', 'COMPONENT', 'COMPONENT_SET', 'SECTION', 'GROUP'];

function makeIcon(name, svg) {
  const node = figma.createNodeFromSvg(svg);
  node.name = name;
  return node;
}

function place(node) {
  const sel = figma.currentPage.selection;
  const target = sel.length === 1 ? sel[0] : null;
  if (target && CONTAINERS.includes(target.type) && target.type !== 'GROUP') {
    target.appendChild(node);
    if (!('layoutMode' in target) || target.layoutMode === 'NONE') {
      node.x = Math.round((target.width - node.width) / 2);
      node.y = Math.round((target.height - node.height) / 2);
    }
  } else if (target && target.parent) {
    // Drop next to the selected layer, in the same parent.
    const p = target.parent;
    p.appendChild(node);
    node.x = Math.round(target.x + target.width + 16);
    node.y = Math.round(target.y);
  } else {
    const c = figma.viewport.center;
    node.x = Math.round(c.x - node.width / 2);
    node.y = Math.round(c.y - node.height / 2);
  }
  figma.currentPage.selection = [node];
}

figma.ui.onmessage = async (msg) => {
  if (msg.type === 'insert') {
    const node = makeIcon(msg.name, msg.svg);
    place(node);
    figma.notify(`Inserted ${msg.name}`, { timeout: 1200 });
  } else if (msg.type === 'save') {
    await figma.clientStorage.setAsync('prefs', msg.prefs);
  } else if (msg.type === 'resize') {
    figma.ui.resize(msg.w, msg.h);
  }
};

figma.on('drop', (e) => {
  const item = e.items.find((i) => i.type === 'image/svg+xml');
  if (!item) return false;
  const meta = e.dropMetadata || {};
  const node = makeIcon(meta.name || 'icon', item.data);
  const parent = e.node && e.node.type !== 'DOCUMENT' && 'appendChild' in e.node ? e.node : figma.currentPage;
  parent.appendChild(node);
  node.x = Math.round(e.x - node.width / 2);
  node.y = Math.round(e.y - node.height / 2);
  figma.currentPage.selection = [node];
  return false;
});

figma.clientStorage.getAsync('prefs').then((prefs) => figma.ui.postMessage({ type: 'prefs', prefs: prefs || null }));
