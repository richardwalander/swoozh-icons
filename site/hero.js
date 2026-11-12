// Hero: Swoozh Icons in use. Tilted cards and floating icon tiles drift at different depths and follow the
// pointer; hovering straightens a card, every control works. When left alone it plays a short demo.
(() => {
  const play = document.getElementById('play'); if (!play || !window.SWZ) return;
  const {byName, draw} = window.SWZ;
  const $ = id => document.getElementById(id);
  const stage = $('play-in');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const W = 600;

  // icons
  const icon = (el, name, v = 'outline') => { el.dataset.i = name; draw(el, name, v); };
  play.querySelectorAll('.ii[data-i]').forEach(el => icon(el, el.dataset.i));

  // scale the 600×600 canvas to the column
  let s = 1;
  new ResizeObserver(([e]) => { s = e.contentRect.width / W; play.style.setProperty('--s', s); }).observe(play);

  // floating icon tiles in the background (depth: far = small, soft, faint)
  const pat = $('pat');
  const names = 'heart hanger shopping-bag dress high-heel perfume-bottle lipstick sneaker handbag jewelry-ring tag gift wash-30 truck star trench-coat diamond scissors'.split(' ').filter(n => byName[n]);
  const rnd = (k, a, b) => { const x = Math.sin(k * 12.9898 + 4.1) * 43758.5453; return a + (x - Math.floor(x)) * (b - a); };
  const SPOTS = [[-30, 40], [110, -20], [330, -40], [560, 10], [620, 220], [570, 400], [600, 600], [380, 620], [190, 600], [-40, 560], [-60, 260], [250, 300], [520, 250], [80, 420], [300, 520], [470, 560]];
  const floats = SPOTS.map(([x, y], k) => {
    const z = rnd(k, .25, .75), size = Math.round(40 + z * 36);
    const el = document.createElement('button'); el.type = 'button'; el.className = 'fl'; el.tabIndex = -1; el.setAttribute('aria-hidden', 'true');
    el.style.cssText = `left:${x - size / 2}px;top:${y - size / 2}px;width:${size}px;height:${size}px;filter:blur(${((1 - z) * 2.4).toFixed(1)}px);opacity:${(.35 + z * .6).toFixed(2)}`;
    const ic = document.createElement('span'); ic.className = 'ii'; el.append(ic); icon(ic, names[k % names.length]); pat.append(el);
    const f = {el, d: z * .9, r0: rnd(k + 7, -28, 28), ph: rnd(k + 3, 0, 6.28), sp: rnd(k + 9, .7, 1.3), amp: 6 + z * 10, rot: 0, k: 1, hover: false};
    el.onmouseenter = () => { f.hover = true; el.classList.add('hot'); }; el.onmouseleave = () => { f.hover = false; el.classList.remove('hot'); };
    el.onclick = () => { const v = ic.dataset.v === 'filled' ? 'outline' : 'filled'; ic.dataset.v = v; icon(ic, ic.dataset.i, v); f.spin = (f.spin || 0) + 360; };
    return f;
  });

  // cards: tilted like pinned swatches, straighten and lift on hover
  const TILT = {'c-toast': 3, 'c-atc': -6, 'c-qty': 5, 'c-prod': -3, 'c-rate': 6, 'c-size': 4, 'c-ship': -5, 'c-nav': -7};
  const cards = [...stage.querySelectorAll('.pc')].map((el, k) => {
    const c = {el, d: +el.dataset.d || .5, ph: k * 1.3, sp: .8 + (k % 3) * .15, amp: 4, r0: TILT[[...el.classList].find(x => TILT[x] !== undefined)] || 0, rot: 0, k: 1, hover: false};
    el.addEventListener('mouseenter', () => c.hover = true); el.addEventListener('mouseleave', () => c.hover = false);
    return c;
  });
  const all = [...floats, ...cards];
  all.forEach(c => { c.rot = c.r0; c.spinNow = 0; });

  // pointer
  const cur = {x: 0, y: 0}, tgt = {x: 0, y: 0};
  let lastUser = performance.now() - 2500, visible = true;
  const onMove = e => {
    const r = play.getBoundingClientRect();
    tgt.x = Math.max(-1, Math.min(1, (e.clientX - r.left - r.width / 2) / (r.width / 2)));
    tgt.y = Math.max(-1, Math.min(1, (e.clientY - r.top - r.height / 2) / (r.height / 2)));
    lastUser = performance.now();
  };
  const hero = play.closest('section') || play;
  hero.addEventListener('pointermove', onMove);
  hero.addEventListener('pointerleave', () => { tgt.x = tgt.y = 0; });
  play.addEventListener('pointerdown', () => { lastUser = performance.now(); });

  const idle = t => t - lastUser > 5000;
  const frame = t => {
    if (visible) {
      if (idle(t) && !reduce) { tgt.x = Math.sin(t / 3200) * .5; tgt.y = Math.cos(t / 4100) * .4; }
      cur.x += (tgt.x - cur.x) * .06; cur.y += (tgt.y - cur.y) * .06;
      stage.style.setProperty('--tx', (-cur.y * 5).toFixed(2) + 'deg'); stage.style.setProperty('--ty', (cur.x * 7).toFixed(2) + 'deg');
      for (const c of all) {
        const w = reduce ? 0 : t / 1000 * c.sp + c.ph;
        const dx = Math.sin(w * .9) * c.amp * c.d, dy = Math.cos(w * .7) * c.amp * c.d;
        const tr = c.hover ? 0 : c.r0 + (reduce ? 0 : Math.sin(w * .5) * 3) + cur.x * 4 * c.d;
        c.rot += (tr - c.rot) * .1;
        if (c.spin) { c.spinNow += (c.spin - c.spinNow) * .12; }
        c.k += ((c.hover ? 1.06 : 1) - c.k) * .15;
        const st = c.el.style;
        st.setProperty('--x', (cur.x * c.d * 34 + dx).toFixed(2) + 'px');
        st.setProperty('--y', (cur.y * c.d * 34 + dy).toFixed(2) + 'px');
        st.setProperty('--r', (c.rot + c.spinNow).toFixed(2) + 'deg');
        st.setProperty('--k', c.k.toFixed(3));
      }
    }
    requestAnimationFrame(frame);
  };
  new IntersectionObserver(([e]) => { visible = e.isIntersecting; }).observe(play);
  requestAnimationFrame(frame);

  // controls --------------------------------------------------------------------------------------
  const pop = (el, cls = 'pop') => { el.classList.remove(cls); void el.offsetWidth; el.classList.add(cls); };
  // favourite
  const fav = $('p-fav'), navFav = $('p-navfav');
  const setFav = on => {
    fav.classList.toggle('on', on); fav.setAttribute('aria-pressed', on); icon(fav.querySelector('.ii'), 'heart', on ? 'filled' : 'outline'); pop(fav);
    navFav.classList.toggle('on', on); icon(navFav.querySelector('.ii'), 'heart', on ? 'filled' : 'outline');
  };
  fav.onclick = () => setFav(!fav.classList.contains('on'));
  navFav.onclick = fav.onclick;

  // add to cart
  const atc = $('p-atc'), toast = $('p-toast'), badge = $('p-badge');
  let cart = 1, atcT;
  atc.onclick = () => {
    clearTimeout(atcT);
    atc.classList.add('done'); icon(atc.querySelector('.ii'), 'check'); atc.querySelector('.t').textContent = 'Added';
    cart += +$('p-q').value || 1; badge.textContent = cart > 9 ? '9+' : cart; pop(badge, 'bump');
    toast.classList.add('show');
    atcT = setTimeout(() => { atc.classList.remove('done'); icon(atc.querySelector('.ii'), 'basket'); atc.querySelector('.t').textContent = 'Add to cart'; toast.classList.remove('show'); }, 2200);
  };

  // quantity
  const q = $('p-q');
  $('p-minus').onclick = () => { q.value = q.textContent = Math.max(1, +q.textContent - 1); };
  $('p-plus').onclick = () => { q.value = q.textContent = Math.min(9, +q.textContent + 1); };
  q.value = q.textContent;

  // rating
  const rate = $('p-rate'), starsHost = rate.querySelector('.stars');
  let rating = 4;
  const stars = [1, 2, 3, 4, 5].map(n => { const b = document.createElement('button'); b.type = 'button'; b.setAttribute('aria-label', n + ' stars');
    const ii = document.createElement('span'); ii.className = 'ii'; b.append(ii); starsHost.append(b);
    b.onmouseenter = () => paintStars(n); b.onclick = () => { rating = n; paintStars(n); pop(b, 'pop'); }; return ii; });
  const paintStars = n => { stars.forEach((ii, k) => icon(ii, 'star', k < n ? 'filled' : 'outline')); $('p-rv').textContent = n.toFixed(1); };
  starsHost.onmouseleave = () => paintStars(rating);
  paintStars(rating);

  // size
  const sizes = [...$('p-size').children];
  const setSize = b => sizes.forEach(x => { x.classList.toggle('on', x === b); x.setAttribute('aria-checked', x === b); });
  sizes.forEach(b => { b.setAttribute('role', 'radio'); b.onclick = () => setSize(b); });
  setSize(sizes.find(b => b.classList.contains('on')));

  // demo when left alone ----------------------------------------------------------------------------
  if (!reduce) {
    const steps = [
      () => setFav(true), () => { rating = 5; paintStars(5); }, () => setSize(sizes[3]), () => atc.onclick(),
      () => $('p-plus').onclick(), () => { rating = 4; paintStars(4); }, () => setFav(false), () => setSize(sizes[2]), () => $('p-minus').onclick(),
    ];
    let k = 0;
    setInterval(() => { if (visible && idle(performance.now()) && !document.hidden) { steps[k % steps.length](); k++; } }, 2200);
  }
})();
