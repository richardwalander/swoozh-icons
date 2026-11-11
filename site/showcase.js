// "See them in use": real Swoozh Fashion UI Kit screens (mobile + desktop) with live Swoozh icons.
// Each icon is called out in its context and shown as its component (Outline / Filled, stroke width).
(() => {
  const S = window.SWZ, M = window.Motion, HOT = window.SWZ_HOT;
  if (!S || !M || !HOT || !document.getElementById('sin')) return;
  const $ = id => document.getElementById(id);
  const stage = $('iu-stage'), sin = $('sin'), browser = $('browser'), phone = $('phone2');
  const bscreen = $('bscreen'), pscreen = $('pscreen');
  const ring = $('ring'), chip = $('chip'), lensEl = $('lens'), lline = $('lline'), ldot = $('ldot');
  const W = 760, H = 640;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  const fit = () => { const k = Math.min(1, stage.clientWidth / W); sin.style.transform = `scale(${k})`; stage.style.height = H * k + 'px'; };
  new ResizeObserver(fit).observe(stage); fit();

  // geometry: kit coordinates -> composition coordinates
  const BK = 720 / 1440, BX = 20, BY = 98, PK = 234 / 390, PX = 478, PY = 64;
  const rectOf = (key, h) => key[0] === 'm'
    ? {x: PX + h.x * PK, y: PY + h.y * PK, w: h.w * PK, h: h.h * PK}
    : {x: BX + h.x * BK, y: BY + h.y * BK, w: h.w * BK, h: h.h * BK};
  const hot = (key, name, i = 0) => HOT[key].icons.filter(h => h.n === name)[i];

  // cancellable animation helpers
  let token = 0, live = new Set(), inView = true;
  const A = (el, kf, o) => { const c = M.animate(el, kf, o); live.add(c); return c; };
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const sleep = async (ms, t) => { await wait(ms); while (!inView) await wait(300); return t === token; };
  new IntersectionObserver(e => { inView = e[0].isIntersecting; }).observe(stage);
  const reset = () => { live.forEach(c => { try { c.stop(); } catch (e) {} }); live.clear(); [ring, chip, lensEl, lline, ldot].forEach(el => { el.style.opacity = 0; }); };

  // screens + devices
  const cache = {}, current = {browser: null, phone: null};
  const imgFor = key => cache[key] || (cache[key] = Object.assign(new Image(), {src: `showcase/${key}.jpg`, alt: ''}));
  async function setScreen(key) {
    const dev = key[0] === 'm' ? 'phone' : 'browser', host = dev === 'phone' ? pscreen : bscreen;
    if (current[dev] === key) return;
    const im = imgFor(key).cloneNode(); im.style.opacity = 0; host.append(im);
    try { await im.decode(); } catch (e) {}
    const old = [...host.querySelectorAll('img')].filter(x => x !== im);
    await A(im, {opacity: [0, 1]}, {duration: .45});
    old.forEach(o => o.remove()); current[dev] = key;
  }
  let shown = null;
  async function showDevice(key) {
    const dev = key[0] === 'm' ? 'phone' : 'browser';
    if (shown === dev) return;
    const on = dev === 'phone' ? phone : browser, off = dev === 'phone' ? browser : phone;
    if (shown) A(off, {opacity: 0, y: [0, 14]}, {duration: .35});
    await A(on, {opacity: [0, 1], y: [18, 0]}, {duration: .5, ease: [.22, 1, .36, 1]}); shown = dev;
  }

  // callout: ring on the icon, leader line to the component card
  const tiles = [...lensEl.querySelectorAll('.vt')], bar = lensEl.querySelector('.sw u'), em = lensEl.querySelector('.sw em');
  const tileHost = v => lensEl.querySelector(`.vt[data-v="${v}"] .ti`);
  function ringAt(r) {
    const d = Math.max(r.w, r.h) + 12;
    Object.assign(ring.style, {width: d + 'px', height: d + 'px', left: r.x + r.w / 2 - d / 2 + 'px', top: r.y + r.h / 2 - d / 2 + 'px'});
    A(ring, {opacity: [0, 1], scale: [.5, 1]}, {duration: .28, ease: [.22, 1, .36, 1]});
  }
  async function point(key, h, t) {
    const r = rectOf(key, h); ringAt(r);
    chip.textContent = h.n; chip.style.left = Math.min(r.x + r.w / 2 + 10, W - 140) + 'px'; chip.style.top = Math.max(r.y - 28, 4) + 'px';
    A(chip, {opacity: [0, 1], y: [4, 0]}, {duration: .25, delay: .08}); return t === token;
  }
  const unpoint = () => { A(ring, {opacity: 0}, {duration: .2}); A(chip, {opacity: 0}, {duration: .2}); };

  async function callout(key, h, o, t) {
    const r = rectOf(key, h), hx = r.x + r.w / 2, hy = r.y + r.h / 2, phoneScene = key[0] === 'm';
    let variant = h.s, sw = 1.5;
    const paint = () => {
      S.draw(tileHost('outline'), h.n, 'outline', sw); S.draw(tileHost('filled'), h.n, 'filled', sw);
      tileHost('filled').style.color = h.n === 'heart' ? '#b81530' : '';
      tiles.forEach(x => x.classList.toggle('on', x.dataset.v === variant));
      bar.style.width = (variant === 'filled' ? 100 : (sw - .75) / 1.25 * 100) + '%'; em.textContent = variant === 'filled' ? '-' : sw.toFixed(2);
    };
    paint();
    lensEl.querySelector('.ln').textContent = 'Icons/' + h.n; lensEl.querySelector('.note').textContent = o.note || '';
    const cw = 270, ch = lensEl.offsetHeight || 230;
    const left = phoneScene ? 20 : (hx > 400 ? 40 : 450), top = Math.max(60, Math.min(hy + (phoneScene ? -ch / 2 : 40), H - ch - 24));
    Object.assign(lensEl.style, {left: left + 'px', top: top + 'px'});
    const cx = left + cw / 2, cy = top + ch / 2, dx = hx - cx, dy = hy - cy, horiz = Math.abs(dx) > Math.abs(dy) * .8;
    const ax = horiz ? (dx > 0 ? left + cw : left) : cx, ay = horiz ? cy : (dy > 0 ? top + ch : top);
    lline.setAttribute('x1', ax); lline.setAttribute('y1', ay); lline.setAttribute('x2', hx); lline.setAttribute('y2', hy);
    ldot.setAttribute('cx', hx); ldot.setAttribute('cy', hy);
    ringAt(r);
    A(lline, {opacity: [0, .8]}, {duration: .3, delay: .1}); A(ldot, {opacity: [0, 1]}, {duration: .3, delay: .1});
    await A(lensEl, {opacity: [0, 1], y: [12, 0]}, {duration: .45, delay: .1, ease: [.22, 1, .36, 1]});
    if (!(await sleep(900, t))) return false;
    if (o.style && o.style !== h.s) { variant = o.style; paint(); A(tileHost(variant), {scale: [1, 1.18, 1]}, {duration: .5}); if (!(await sleep(1100, t))) return false; }
    if (o.stroke) {
      variant = 'outline'; paint();
      for (const [to, d] of [[.75, .9], [2, 1.2], [1.5, .7]]) {
        const from = sw; await A(from, to, {duration: d, ease: 'easeInOut', onUpdate: v => { sw = v; paint(); }}); if (t !== token) return false; }
      if (!(await sleep(600, t))) return false;
    } else if (!(await sleep(o.hold || 900, t))) return false;
    A(lensEl, {opacity: 0, y: [0, 8]}, {duration: .3}); A(lline, {opacity: 0}, {duration: .25}); A(ldot, {opacity: 0}, {duration: .25}); A(ring, {opacity: 0}, {duration: .25});
    return sleep(350, t);
  }

  // scenes
  const scenes = [
    {key: 'm-home', steps: [{sweep: ['store', 'search', 'basket', 'heart', 'menu']}, {lens: 'basket', style: 'filled', note: 'Active tab: Style=Filled'}]},
    {key: 'm-category', steps: [{sweep: ['arrow-left', 'sort-amount-down', 'sliders-horizontal']}, {lens: 'heart', i: 1, style: 'filled', note: 'Save as favourite'}]},
    {key: 'm-product', steps: [{lens: 'share', note: 'Same icon at any size'}, {lens: 'heart', style: 'filled', note: 'Favourite on the product'}]},
    {key: 'm-cart', steps: [{lens: 'trash', note: 'Remove item'}, {lens: 'credit-card', note: 'Go to checkout'}]},
    {key: 'd-home', steps: [{sweep: ['search', 'user', 'heart', 'basket']}, {lens: 'basket', style: 'filled', note: 'Cart in the header'}]},
    {key: 'd-category', steps: [{sweep: ['sort-amount-down', 'sliders-horizontal', 'x']}, {lens: 'sliders-horizontal', note: 'Filters'}]},
    {key: 'd-product', steps: [{sweep: ['star'], all: true}, {lens: 'basket-plus', note: 'Add to cart'}]},
    {key: 'm-home', steps: [{lens: 'basket', stroke: true, note: 'Stroke width from 0.75 to 2'}]},
  ];
  const steps = [...document.querySelectorAll('#iu-steps li')];
  const setActive = i => { const k = Math.min(i, steps.length - 1); steps.forEach((l, j) => l.classList.toggle('on', j === k)); };

  async function play(i, t) {
    const sc = scenes[i]; setActive(i);
    await Promise.all([setScreen(sc.key), showDevice(sc.key)]); if (!(await sleep(600, t))) return false;
    for (const st of sc.steps) {
      if (st.sweep) {
        for (const n of st.sweep) {
          const list = HOT[sc.key].icons.filter(h => h.n === n); const items = st.all ? list : [list[0]];
          for (const h of items) { if (!h) continue; if (!(await point(sc.key, h, t))) return false; if (!(await sleep(st.all ? 220 : 520, t))) return false; }
        }
        unpoint(); if (!(await sleep(300, t))) return false;
      } else if (st.lens) {
        const h = hot(sc.key, st.lens, st.i || 0); if (!h) continue;
        if (!(await callout(sc.key, h, st, t))) return false;
      }
    }
    return true;
  }
  async function loop(from) {
    const t = ++token; reset(); let i = from;
    while (t === token) { if (!(await play(i, t))) return; i = (i + 1) % scenes.length; }
  }

  steps.forEach((li, i) => li.addEventListener('click', () => { loop(i); }));
  browser.style.opacity = 0; phone.style.opacity = 0;
  Promise.all(Object.keys(HOT).map(k => imgFor(k).decode().catch(() => {}))).then(() => {
    Promise.all([setScreen('d-home'), setScreen('m-home')]).then(() => { if (!reduce) loop(0); else { setActive(0); showDevice('m-home'); } });
  });
})();
