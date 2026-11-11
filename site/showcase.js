// "See them in use": real Swoozh Fashion UI Kit screens (mobile + desktop) with live Swoozh icons.
// Each icon is followed from the screen into its component card, where style and stroke width change.
(() => {
  const S = window.SWZ, M = window.Motion, HOT = window.SWZ_HOT;
  if (!S || !M || !HOT || !document.getElementById('sin')) return;
  const $ = id => document.getElementById(id);
  const stage = $('iu-stage'), sin = $('sin'), browser = $('browser'), phone = $('phone2');
  const bscreen = $('bscreen'), pscreen = $('pscreen');
  const dim = $('dim'), ring = $('ring'), chip = $('chip'), lensEl = $('lens'), fly = $('fly');
  const W = 760, H = 620;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // fit the 760 x 620 composition to the available width
  const fit = () => { const k = Math.min(1, stage.clientWidth / W); sin.style.transform = `scale(${k})`; stage.style.height = H * k + 'px'; };
  new ResizeObserver(fit).observe(stage); fit();

  // geometry: where a hotspot (in kit coordinates) lands in the composition
  const BK = 600 / 1440, BX = 0, BY = 56, PK = 200 / 390, PX = 532, PY = 158;
  const rectOf = (key, h) => key[0] === 'm'
    ? {x: PX + h.x * PK, y: PY + h.y * PK, w: h.w * PK, h: h.h * PK}
    : {x: BX + h.x * BK, y: BY + h.y * BK, w: h.w * BK, h: h.h * BK};
  const hot = (key, name, i = 0) => HOT[key].icons.filter(h => h.n === name)[i];
  const SLOT = {x: 340, y: 190};

  // animation helpers with cancellation
  let token = 0, live = new Set();
  const A = (el, kf, o) => { const c = M.animate(el, kf, o); live.add(c); return c; };
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const sleep = async (ms, t) => { await wait(ms); while (!inView) await wait(300); return t === token; };
  let inView = true; new IntersectionObserver(e => { inView = e[0].isIntersecting; }).observe(stage);
  const hide = el => { el.style.opacity = 0; };
  const reset = () => { live.forEach(c => { try { c.stop(); } catch (e) {} }); live.clear(); [dim, ring, chip, lensEl, fly].forEach(hide); };

  // screens
  const cache = {};
  const imgFor = key => cache[key] || (cache[key] = Object.assign(new Image(), {src: `showcase/${key}.jpg`, alt: ''}));
  const current = {browser: null, phone: null};
  async function setScreen(key) {
    const dev = key[0] === 'm' ? 'phone' : 'browser', host = dev === 'phone' ? pscreen : bscreen;
    if (current[dev] === key) return;
    const im = imgFor(key).cloneNode(); im.style.opacity = 0; host.append(im);
    try { await im.decode(); } catch (e) {}
    const old = [...host.querySelectorAll('img')].filter(x => x !== im);
    await A(im, {opacity: [0, 1]}, {duration: .5});
    old.forEach(o => o.remove()); current[dev] = key;
  }
  async function focus(key) {
    const onPhone = key[0] === 'm';
    A(phone, {opacity: onPhone ? 1 : .5, scale: onPhone ? 1 : .94}, {duration: .6});
    A(browser, {opacity: onPhone ? .5 : 1, scale: onPhone ? .96 : 1}, {duration: .6});
    phone.style.zIndex = onPhone ? 3 : 1;
  }

  // ring + label on one icon
  async function point(key, h, t) {
    const r = rectOf(key, h), d = Math.max(r.w, r.h) + 12;
    Object.assign(ring.style, {width: d + 'px', height: d + 'px', left: r.x + r.w / 2 - d / 2 + 'px', top: r.y + r.h / 2 - d / 2 + 'px'});
    chip.textContent = h.n; chip.style.left = Math.min(r.x + r.w / 2 + 10, W - 130) + 'px'; chip.style.top = r.y - 26 + 'px';
    A(ring, {opacity: [0, 1], scale: [.5, 1]}, {duration: .28, ease: [.22, 1, .36, 1]});
    A(chip, {opacity: [0, 1], y: [4, 0]}, {duration: .25, delay: .08});
    return t === token;
  }
  const unpoint = () => { A(ring, {opacity: 0}, {duration: .2}); A(chip, {opacity: 0}, {duration: .2}); };

  // lift an icon out of the screen into its component card
  async function lens(key, h, o, t) {
    const r = rectOf(key, h), cx = r.x + r.w / 2, cy = r.y + r.h / 2, s0 = Math.max(r.w, r.h) / 24, SC = 4.5;
    let variant = h.s, sw = 1.5;
    const seg = [...lensEl.querySelectorAll('.seg span')], bar = lensEl.querySelector('.sw u'), em = lensEl.querySelector('.sw em');
    const paint = () => { S.draw(fly, h.n, variant, sw); fly.style.color = variant === 'filled' && h.n === 'heart' ? '#b81530' : ''; seg.forEach(x => x.classList.toggle('on', x.dataset.v === variant));
      bar.style.width = (variant === 'filled' ? 100 : (sw - .75) / 1.25 * 100) + '%'; em.textContent = variant === 'filled' ? '-' : sw.toFixed(2); };
    lensEl.querySelector('.ln').textContent = 'Icons/' + h.n; lensEl.querySelector('.note').textContent = o.note || '';
    paint();
    Object.assign(fly.style, {left: SLOT.x - 12 + 'px', top: SLOT.y - 12 + 'px'});
    A(dim, {opacity: 1}, {duration: .35});
    A(lensEl, {opacity: [0, 1], y: [14, 0]}, {duration: .4, delay: .2});
    fly.style.opacity = 1;
    await A(fly, {x: [cx - SLOT.x, 0], y: [cy - SLOT.y, 0], scale: [s0, SC]}, {duration: .8, ease: [.22, 1, .36, 1]});
    if (t !== token || !(await sleep(500, t))) return false;
    if (o.style && o.style !== variant) { variant = o.style; paint(); A(fly, {scale: [SC, SC * 1.18, SC]}, {duration: .5}); if (!(await sleep(900, t))) return false; }
    if (o.stroke) {
      for (const [to, d] of [[.75, .9], [2, 1.2], [1.5, .7]]) {
        const from = sw; await A(from, to, {duration: d, ease: 'easeInOut', onUpdate: v => { sw = v; paint(); }}); if (t !== token) return false; }
      if (!(await sleep(500, t))) return false;
    } else if (!(await sleep(o.hold || 700, t))) return false;
    A(lensEl, {opacity: 0, y: [0, 8]}, {duration: .3}); A(dim, {opacity: 0}, {duration: .4, delay: .1});
    await A(fly, {x: [0, cx - SLOT.x], y: [0, cy - SLOT.y], scale: [SC, s0], opacity: [1, 1, 0]}, {duration: .6, ease: [.65, 0, .35, 1]});
    return t === token;
  }

  // scenes
  const scenes = [
    {key: 'm-home', steps: [{sweep: ['store', 'search', 'basket', 'heart', 'menu']}, {lens: 'basket', style: 'filled', note: 'Active tab: Style=Filled'}]},
    {key: 'm-category', steps: [{sweep: ['arrow-left', 'sort-amount-down', 'sliders-horizontal']}, {lens: 'heart', i: 1, style: 'filled', note: 'Save as favourite'}]},
    {key: 'm-product', steps: [{lens: 'share', note: 'Same icon, any size'}, {lens: 'heart', style: 'filled', note: 'Favourite on the product'}]},
    {key: 'm-cart', steps: [{lens: 'trash', note: 'Remove item'}, {lens: 'credit-card', note: 'Checkout'}]},
    {key: 'd-home', steps: [{sweep: ['search', 'user', 'heart', 'basket']}, {lens: 'truck-fast', note: 'Delivery promise'}]},
    {key: 'd-category', steps: [{sweep: ['sort-amount-down', 'sliders-horizontal', 'x']}, {lens: 'sliders-horizontal', note: 'Filters'}]},
    {key: 'd-product', steps: [{sweep: ['star'], all: true}, {lens: 'basket-plus', note: 'Add to cart'}]},
    {key: 'm-home', steps: [{lens: 'basket', stroke: true, note: 'Stroke width 0.75 to 2'}]},
  ];
  const steps = [...document.querySelectorAll('#iu-steps li')];
  const setActive = i => { const k = Math.min(i, steps.length - 1); steps.forEach((l, j) => l.classList.toggle('on', j === k)); };

  async function play(i, t) {
    const sc = scenes[i]; setActive(i);
    await Promise.all([setScreen(sc.key), focus(sc.key)]); if (t !== token || !(await sleep(500, t))) return false;
    for (const st of sc.steps) {
      if (st.sweep) {
        for (const n of st.sweep) {
          const list = HOT[sc.key].icons.filter(h => h.n === n); const items = st.all ? list : [list[0]];
          for (const h of items) { if (!(await point(sc.key, h, t))) return false; if (!(await sleep(st.all ? 220 : 480, t))) return false; }
        }
        unpoint(); if (!(await sleep(300, t))) return false;
      } else if (st.lens) {
        const h = hot(sc.key, st.lens, st.i || 0); if (!h) continue;
        if (!(await lens(sc.key, h, st, t))) return false; if (!(await sleep(350, t))) return false;
      }
    }
    return true;
  }
  async function loop(from) {
    const t = ++token; reset();
    let i = from;
    while (t === token) { if (!(await play(i, t))) return; i = (i + 1) % scenes.length; }
  }

  steps.forEach((li, i) => li.addEventListener('click', () => { loop(i); }));
  Promise.all(Object.keys(HOT).map(k => imgFor(k).decode().catch(() => {}))).then(() => {
    Promise.all([setScreen('d-home'), setScreen('m-home')]).then(() => { focus('m-home'); if (!reduce) loop(0); else setActive(0); });
  });
})();
