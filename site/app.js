(() => {
  const D = window.SWOOZH;
  const NS = 'http://www.w3.org/2000/svg';
  const icons = D.icons.map(([name, category, tags, o, f, cp]) => ({name, category, tags: tags ? tags.split(',') : [], o, f, cp,
    hay: (name.replace(/-/g, ' ') + ' ' + tags.replace(/,/g, ' ') + ' ' + category).toLowerCase()}));
  const byName = Object.fromEntries(icons.map(i => [i.name, i]));
  const $ = id => document.getElementById(id);
  const pascal = n => n.split('-').map(s => s[0].toUpperCase() + s.slice(1)).join('');
  const store = {
    get(k, d) { try { const v = localStorage.getItem('swz-' + k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem('swz-' + k, JSON.stringify(v)); } catch (e) {} },
  };
  const svgEl = (d, size) => {
    const s = document.createElementNS(NS, 'svg');
    s.setAttribute('viewBox', '0 0 24 24'); s.setAttribute('width', size); s.setAttribute('height', size);
    s.setAttribute('fill', 'currentColor'); s.setAttribute('aria-hidden', 'true');
    const p = document.createElementNS(NS, 'path'); p.setAttribute('d', d); s.append(p); return s;
  };
  const svgText = (i, v, size = 24) => `<svg xmlns="${NS}" width="${size}" height="${size}" viewBox="0 0 24 24" fill="currentColor"><path d="${v === 'filled' ? i.f : i.o}"/></svg>`;
  const fillIcons = (root = document) => root.querySelectorAll('[data-icon]').forEach(el => {
    const i = byName[el.dataset.icon]; if (!i) return; el.replaceChildren(svgEl(i.o, el.dataset.size || 20)); el.style.display = 'inline-flex';
  });

  // state ----------------------------------------------------------------------------------------
  const params = new URLSearchParams(location.search);
  const st = {q: params.get('q') || '', cat: params.get('cat') || '', variant: store.get('variant', 'outline'), size: store.get('size', 24),
    color: store.get('color', ''), review: store.get('review', false), flags: store.get('flags', {}), onlyFlagged: false, sel: null, tab: store.get('tab', 'svg')};

  const toast = msg => { const t = $('toast'); t.textContent = msg; t.classList.add('show'); clearTimeout(toast.t); toast.t = setTimeout(() => t.classList.remove('show'), 1400); };
  const copy = async (text, msg = 'Copied') => { try { await navigator.clipboard.writeText(text); } catch (e) {
    const ta = document.createElement('textarea'); ta.value = text; document.body.append(ta); ta.select(); document.execCommand('copy'); ta.remove(); } toast(msg); };

  // hero ------------------------------------------------------------------------------------------
  $('s-icons').textContent = icons.length.toLocaleString('en');
  $('s-cats').textContent = D.categories.length;
  $('ver').textContent = 'v' + D.version;
  ['hanger', 'shopping-bag', 'dress', 'high-heel', 't-shirt', 'wash-30', 'tag', 'truck-fast', 'credit-card', 'heart', 'lipstick', 'sweater', 'package-return', 'ruler']
    .filter(n => byName[n]).forEach((n, k) => $('marquee').append(svgEl(k % 2 ? byName[n].f : byName[n].o, 28)));

  // sidebar ---------------------------------------------------------------------------------------
  const counts = {}; icons.forEach(i => counts[i.category] = (counts[i.category] || 0) + 1);
  const side = $('side');
  side.innerHTML = '<h4>Categories</h4>';
  const catBtn = (label, value, n) => { const b = document.createElement('button'); b.className = 'cat'; b.dataset.cat = value;
    b.innerHTML = `<span></span><small>${n}</small>`; b.firstChild.textContent = label; b.onclick = () => { st.cat = st.cat === value ? '' : value; st.onlyFlagged = false; render(); }; side.append(b); };
  catBtn('All icons', '', icons.length);
  D.categories.forEach(c => catBtn(c, c, counts[c]));

  // grid ------------------------------------------------------------------------------------------
  const grid = $('grid');
  const tiles = new Map();
  const frag = document.createDocumentFragment();
  for (const i of icons) {
    const t = document.createElement('button'); t.className = 'tile'; t.title = i.name; t.dataset.name = i.name;
    t.append(svgEl(i.o, 24)); const s = document.createElement('span'); s.textContent = i.name; t.append(s);
    const fl = document.createElement('i'); fl.className = 'flag'; t.append(fl);
    t.onclick = () => open(i.name); tiles.set(i.name, t); frag.append(t);
  }
  grid.append(frag);

  function score(i, words) {
    let s = 0;
    for (const w of words) {
      if (!i.hay.includes(w)) return -1;
      if (i.name === w) s += 100; else if (i.name.startsWith(w)) s += 40; else if (i.name.includes(w)) s += 20;
      else if (i.tags.some(t => t === w)) s += 12; else if (i.tags.some(t => t.includes(w))) s += 6; else s += 1;
    }
    return s;
  }
  function render() {
    const words = st.q.toLowerCase().trim().split(/\s+/).filter(Boolean);
    let list = icons.filter(i => (!st.cat || i.category === st.cat) && (!st.onlyFlagged || st.flags[i.name]));
    if (words.length) list = list.map(i => [i, score(i, words)]).filter(x => x[1] >= 0).sort((a, b) => b[1] - a[1]).map(x => x[0]);
    const show = new Set(list.map(i => i.name));
    for (const t of tiles.values()) t.hidden = !show.has(t.dataset.name);
    if (words.length) list.forEach(i => grid.append(tiles.get(i.name))); else if (render.sorted) { icons.forEach(i => grid.append(tiles.get(i.name))); }
    render.sorted = words.length > 0;
    $('empty').hidden = list.length > 0;
    $('count').textContent = `${list.length.toLocaleString('en')} ${list.length === 1 ? 'icon' : 'icons'}${st.cat ? ' in ' + st.cat : ''}${st.onlyFlagged ? ' flagged' : ''}`;
    side.querySelectorAll('.cat').forEach(b => b.classList.toggle('on', b.dataset.cat === st.cat && !st.onlyFlagged));
    const u = new URLSearchParams(); if (st.q) u.set('q', st.q); if (st.cat) u.set('cat', st.cat);
    history.replaceState(null, '', u.toString() ? '?' + u : location.pathname);
  }
  function paint() {
    for (const i of icons) tiles.get(i.name).firstChild.firstChild.setAttribute('d', st.variant === 'filled' ? i.f : i.o);
    grid.querySelectorAll('svg').forEach(s => { s.setAttribute('width', st.size); s.setAttribute('height', st.size); });
    grid.style.setProperty('--cell', Math.max(96, st.size * 2 + 48) + 'px');
    document.body.style.setProperty('--icon', st.color || '');
    $('v-outline').classList.toggle('on', st.variant === 'outline'); $('v-filled').classList.toggle('on', st.variant === 'filled');
    $('size').value = st.size; $('size-v').textContent = st.size;
    $('color').value = st.color || (getComputedStyle(document.body).color.match(/\d+/g) || [23, 22, 26]).slice(0, 3).reduce((s, n) => s + (+n).toString(16).padStart(2, '0'), '#');
  }
  function paintFlags() {
    for (const [n, t] of tiles) t.classList.toggle('flagged', !!st.flags[n]);
    const n = Object.keys(st.flags).length;
    $('review').classList.toggle('on', st.review);
    $('reviewbar').classList.toggle('show', st.review);
    $('rb-count').textContent = `${n} flagged`;
    $('d-review').hidden = !st.review;
  }

  // drawer ----------------------------------------------------------------------------------------
  const TABS = {
    svg: i => svgText(i, st.variant),
    react: i => `import { ${pascal(i.name)} } from '@swoozh/icons-react';\n\n<${pascal(i.name)}${st.variant === 'filled' ? ' variant="filled"' : ''} size={24} />`,
    vue: i => `<script setup>\nimport { ${pascal(i.name)} } from '@swoozh/icons-vue';\n</script>\n\n<template>\n  <${pascal(i.name)}${st.variant === 'filled' ? ' variant="filled"' : ''} :size="24" />\n</template>`,
    svelte: i => `<script>\n  import { Icon, ${pascal(i.name)} } from '@swoozh/icons-svelte';\n</script>\n\n<Icon icon={${pascal(i.name)}}${st.variant === 'filled' ? ' variant="filled"' : ''} size={24} />`,
    element: i => `<script type="module" src="https://unpkg.com/@swoozh/icons-element"></script>\n\n<swoozh-icon name="${i.name}"${st.variant === 'filled' ? ' variant="filled"' : ''}></swoozh-icon>`,
    font: i => `<link rel="stylesheet" href="swoozh-icons.css">\n\n<i class="swz swz-${i.name}${st.variant === 'filled' ? ' swz-filled' : ''}"></i>`,
    elm: i => { const c = pascal(i.name); return `import SwoozhIcons exposing (Variant(..))\n\nSwoozhIcons.${c[0].toLowerCase() + c.slice(1)} ${st.variant === 'filled' ? 'Filled' : 'Outline'} []`; },
    sprite: i => `<svg width="24" height="24"><use href="sprite-${st.variant}.svg#${i.name}"/></svg>`,
  };
  const LABEL = {svg: 'SVG', react: 'React', vue: 'Vue', svelte: 'Svelte', element: 'Web component', font: 'Font', elm: 'Elm', sprite: 'Sprite'};
  Object.keys(TABS).forEach(k => { const b = document.createElement('button'); b.textContent = LABEL[k]; b.dataset.tab = k; b.onclick = () => { st.tab = k; store.set('tab', k); fillDrawer(); }; $('d-tabs').append(b); });
  function fillDrawer() {
    const i = byName[st.sel]; if (!i) return;
    $('d-name').textContent = i.name;
    $('d-head').replaceChildren(svgEl(st.variant === 'filled' ? i.f : i.o, 20));
    $('d-o').firstChild.setAttribute('d', i.o); $('d-f').firstChild.setAttribute('d', i.f);
    $('d-cat').textContent = i.category;
    $('d-tags').replaceChildren(...i.tags.map(t => { const b = document.createElement('button'); b.textContent = t; b.onclick = () => { $('q').value = st.q = t; st.cat = ''; render(); }; return b; }));
    $('d-tabs').querySelectorAll('button').forEach(b => b.classList.toggle('on', b.dataset.tab === st.tab));
    $('d-code').textContent = TABS[st.tab](i);
    $('d-font-o').className = 'swz swz-' + i.name; $('d-font-f').className = 'swz swz-filled swz-' + i.name;
    $('d-flag').classList.toggle('on', !!st.flags[i.name]); $('d-flag').textContent = st.flags[i.name] ? 'Flagged · unflag' : 'Flag for redraw';
    $('d-note').value = (st.flags[i.name] && st.flags[i.name].note) || '';
  }
  function open(name) { st.sel = name; fillDrawer(); $('drawer').classList.add('open'); }
  $('d-close').onclick = () => $('drawer').classList.remove('open');
  $('d-copy-svg').onclick = () => copy(svgText(byName[st.sel], st.variant), 'SVG copied');
  $('d-copy-name').onclick = () => copy(st.sel, 'Name copied');
  $('d-copy-code').onclick = () => copy($('d-code').textContent, 'Snippet copied');
  $('d-dl').onclick = () => { const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([svgText(byName[st.sel], st.variant)], {type: 'image/svg+xml'}));
    a.download = `${st.sel}${st.variant === 'filled' ? '-filled' : ''}.svg`; a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 1000); };

  // review ----------------------------------------------------------------------------------------
  const saveFlags = () => { store.set('flags', st.flags); paintFlags(); };
  $('d-flag').onclick = () => { if (st.flags[st.sel]) delete st.flags[st.sel]; else st.flags[st.sel] = {note: $('d-note').value}; saveFlags(); fillDrawer(); };
  $('d-note').oninput = e => { st.flags[st.sel] = {note: e.target.value}; saveFlags(); $('d-flag').classList.add('on'); $('d-flag').textContent = 'Flagged · unflag'; };
  $('review').onclick = () => { st.review = !st.review; store.set('review', st.review); if (!st.review) st.onlyFlagged = false; paintFlags(); render(); };
  $('rb-show').onclick = () => { st.onlyFlagged = !st.onlyFlagged; st.cat = ''; $('rb-show').textContent = st.onlyFlagged ? 'Show all' : 'Show flagged'; render(); };
  $('rb-copy').onclick = () => copy(Object.entries(st.flags).map(([n, f]) => f.note ? `${n}: ${f.note}` : n).join('\n') || '(none)', 'Flag list copied');
  $('rb-clear').onclick = () => { if (confirm('Clear all flags?')) { st.flags = {}; saveFlags(); render(); } };

  // controls --------------------------------------------------------------------------------------
  let qt; $('q').value = st.q;
  $('q').oninput = e => { clearTimeout(qt); qt = setTimeout(() => { st.q = e.target.value; render(); }, 60); };
  $('v-outline').onclick = () => { st.variant = 'outline'; store.set('variant', 'outline'); paint(); fillDrawer(); };
  $('v-filled').onclick = () => { st.variant = 'filled'; store.set('variant', 'filled'); paint(); fillDrawer(); };
  $('size').oninput = e => { st.size = +e.target.value; store.set('size', st.size); paint(); };
  $('color').oninput = e => { st.color = e.target.value; store.set('color', st.color); paint(); };
  $('theme').onclick = () => { const dark = matchMedia('(prefers-color-scheme: dark)').matches;
    const cur = document.documentElement.dataset.theme || (dark ? 'dark' : 'light'); const next = cur === 'dark' ? 'light' : 'dark';
    document.documentElement.dataset.theme = next; try { localStorage.setItem('swz-theme', next); } catch (e) {} st.color = ''; store.set('color', ''); paint(); };
  document.querySelectorAll('[data-copy]').forEach(b => b.onclick = () => copy(b.dataset.copy));
  document.addEventListener('keydown', e => {
    if (e.key === '/' && document.activeElement !== $('q') && !/TEXTAREA|INPUT/.test(document.activeElement.tagName)) { e.preventDefault(); $('q').focus(); }
    if (e.key === 'Escape') $('drawer').classList.remove('open');
  });

  fillIcons(); paint(); paintFlags(); render();
})();
