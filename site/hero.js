// Hero: Swoozh Icons in use. The headline sits in the middle; tilted UI cards and floating icon tiles orbit it
// at different depths, sway on their own and follow the pointer. Hover straightens a card; every control works.
(() => {
  const play = document.getElementById('play'); if (!play || !window.SWZ) return;
  const {byName, draw} = window.SWZ;
  const $ = id => document.getElementById(id);
  const hero = $('hero'), stage = $('play-in');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const icon = (el, name, v = 'outline') => { el.dataset.i = name; draw(el, name, v); };
  play.querySelectorAll('.ii[data-i]').forEach(el => icon(el, el.dataset.i));

  // layouts: [left, top, rotation] on a design canvas around the centred headline.
  const L = {
    desk: {w: 1280, h: 780, cards: {
      'c-pay': [56, 46, -4], 'c-nav': [252, 132, -7], 'c-search': [392, 34, -2], 'c-notif': [716, 40, 3], 'c-toast': [744, 118, 2], 'c-qty': [1050, 56, 6],
      'c-prod2': [74, 182, -6], 'c-prod': [1000, 164, 5], 'c-care': [30, 520, 4], 'c-ship': [96, 626, -5], 'c-return': [36, 700, 3],
      'c-atc': [372, 640, -4], 'c-size': [612, 664, 3], 'c-swatch': [800, 636, -3], 'c-rate': [968, 478, 6], 'c-promo': [1066, 568, -5], 'c-track': [968, 676, 2]},
      floats: [[330, 300], [318, 560], [960, 130], [1236, 470], [1240, 110], [16, 360], [684, 748], [560, 600], [940, 590], [1200, 740], [240, 470], [610, 140]]},
    // mobile: the headline stays centred, cards hug the top and bottom edges and bleed off screen.
    // A negative top is measured from the bottom of the canvas (its height follows the viewport).
    mob: {w: 560, h: 1100, cards: {
      'c-atc': [-34, 44, -7], 'c-nav': [372, 18, 7], 'c-notif': [236, 138, -3],
      'c-rate': [-26, -300, 5], 'c-size': [352, -270, -5], 'c-prod': [176, -178, 4], 'c-swatch': [-44, -150, -6], 'c-care': [404, -142, 7]},
      floats: [[34, 300], [530, 330], [22, -380], [540, -400], [300, 236], [120, -40], [470, -20]]},
  };
  let mode = '', lay;

  // floating icon tiles: far = small, soft, faint
  const pat = $('pat');
  const names = 'heart hanger shopping-bag dress high-heel perfume-bottle lipstick sneaker handbag jewelry-ring gift wash-30 star trench-coat diamond scissors'.split(' ').filter(n => byName[n]);
  const rnd = (k, a, b) => { const x = Math.sin(k * 12.9898 + 4.1) * 43758.5453; return a + (x - Math.floor(x)) * (b - a); };
  const floats = L.desk.floats.map((_, k) => {
    const z = rnd(k, .25, .75), size = Math.round(40 + z * 36);
    const el = document.createElement('button'); el.type = 'button'; el.className = 'fl'; el.tabIndex = -1; el.setAttribute('aria-hidden', 'true');
    el.style.cssText = `width:${size}px;height:${size}px;filter:blur(${((1 - z) * 2.4).toFixed(1)}px);opacity:${(.35 + z * .6).toFixed(2)}`;
    const ic = document.createElement('span'); ic.className = 'ii'; el.append(ic); icon(ic, names[k % names.length]); pat.append(el);
    const f = {el, size, d: z * .9, r0: rnd(k + 7, -28, 28), ph: rnd(k + 3, 0, 6.28), sp: rnd(k + 9, .7, 1.3), amp: 6 + z * 10, hover: false, spin: 0};
    el.onmouseenter = () => { f.hover = true; el.classList.add('hot'); }; el.onmouseleave = () => { f.hover = false; el.classList.remove('hot'); };
    el.onclick = () => { const v = ic.dataset.v === 'filled' ? 'outline' : 'filled'; ic.dataset.v = v; icon(ic, ic.dataset.i, v); f.spin += 360; };
    return f;
  });
  const cards = [...stage.querySelectorAll('.pc')].map((el, k) => {
    const key = el.classList.contains('c-prod2') ? 'c-prod2' : [...el.classList].find(x => L.desk.cards[x]);
    const c = {el, key, d: +el.dataset.d || .5, ph: k * 1.3, sp: .8 + (k % 3) * .15, amp: 4, r0: 0, hover: false, spin: 0};
    el.addEventListener('mouseenter', () => c.hover = true); el.addEventListener('mouseleave', () => c.hover = false);
    return c;
  });
  const all = [...floats, ...cards];
  all.forEach(c => { c.rot = 0; c.spinNow = 0; c.k = 1; });

  let lastW = 0;
  const place = (el, x, y, size = 0) => { el.style.left = x - size / 2 + 'px'; el.style.top = (y < 0 ? lay.h + y : y) - size / 2 + 'px'; };
  const layout = () => {
    const w = hero.clientWidth, m = w < 1024 ? 'mob' : 'desk';
    if (m === mode && w === lastW) return;
    lastW = w; mode = m; lay = {...L[m]}; hero.classList.toggle('mob', m === 'mob');
    const s = m === 'mob' ? Math.min(w / lay.w, 1.3) : Math.min(w / lay.w, 1.15);
    if (m === 'mob') { const vh = Math.max(640, Math.min(document.documentElement.clientHeight - 64, 920)); lay.h = vh / s; }
    stage.style.width = lay.w + 'px'; stage.style.height = lay.h + 'px';
    cards.forEach(c => { const p = lay.cards[c.key]; c.el.hidden = !p; if (p) { place(c.el, p[0], p[1]); c.r0 = c.rot = p[2]; } });
    floats.forEach((f, k) => { const p = lay.floats[k]; f.el.hidden = !p; if (p) { place(f.el, p[0], p[1], f.size); f.rot = f.r0; } });
    play.style.setProperty('--s', s); hero.style.setProperty('--s', s);
    play.style.setProperty('--ox', ((w - lay.w * s) / 2 + lay.w / 2 * (s - 1)) + 'px'); play.style.setProperty('--oy', (lay.h / 2 * (s - 1)) + 'px');
    hero.style.setProperty('--h', lay.h * s + 'px');
  };
  new ResizeObserver(layout).observe(hero); layout();

  // pointer
  const cur = {x: 0, y: 0}, tgt = {x: 0, y: 0};
  let lastUser = performance.now() - 2500, visible = true;
  hero.addEventListener('pointermove', e => {
    const r = play.getBoundingClientRect();
    tgt.x = Math.max(-1, Math.min(1, (e.clientX - r.left - r.width / 2) / (r.width / 2)));
    tgt.y = Math.max(-1, Math.min(1, (e.clientY - r.top - r.height / 2) / (r.height / 2)));
    lastUser = performance.now();
  });
  hero.addEventListener('pointerleave', () => { tgt.x = tgt.y = 0; });
  hero.addEventListener('pointerdown', () => { lastUser = performance.now(); });
  const idle = t => t - lastUser > 5000;

  const frame = t => {
    if (visible) {
      if (idle(t) && !reduce) { tgt.x = Math.sin(t / 3200) * .5; tgt.y = Math.cos(t / 4100) * .4; }
      cur.x += (tgt.x - cur.x) * .06; cur.y += (tgt.y - cur.y) * .06;
      stage.style.setProperty('--tx', (-cur.y * 4).toFixed(2) + 'deg'); stage.style.setProperty('--ty', (cur.x * 5).toFixed(2) + 'deg');
      for (const c of all) {
        if (c.el.hidden) continue;
        const w = reduce ? 0 : t / 1000 * c.sp + c.ph;
        const dx = Math.sin(w * .9) * c.amp * c.d, dy = Math.cos(w * .7) * c.amp * c.d;
        const tr = c.hover ? 0 : c.r0 + (reduce ? 0 : Math.sin(w * .5) * 3) + cur.x * 4 * c.d;
        c.rot += (tr - c.rot) * .1; c.spinNow += (c.spin - c.spinNow) * .12; c.k += ((c.hover ? 1.05 : 1) - c.k) * .15;
        const st = c.el.style;
        st.setProperty('--x', (cur.x * c.d * 34 + dx).toFixed(2) + 'px');
        st.setProperty('--y', (cur.y * c.d * 34 + dy).toFixed(2) + 'px');
        st.setProperty('--r', (c.rot + c.spinNow).toFixed(2) + 'deg');
        st.setProperty('--k', c.k.toFixed(3));
      }
    }
    requestAnimationFrame(frame);
  };
  new IntersectionObserver(([e]) => { visible = e.isIntersecting; }).observe(hero);
  requestAnimationFrame(frame);

  // controls --------------------------------------------------------------------------------------
  const pop = (el, cls = 'pop') => { el.classList.remove(cls); void el.offsetWidth; el.classList.add(cls); };
  // favourites
  const navFav = $('p-navfav');
  const favs = [$('p-fav'), $('p-fav2')];
  const paintNav = () => { const on = favs.some(f => f.classList.contains('on')); navFav.classList.toggle('on', on); icon(navFav.querySelector('.ii'), 'heart', on ? 'filled' : 'outline'); };
  const setFav = (fav, on) => { fav.classList.toggle('on', on); fav.setAttribute('aria-pressed', on); icon(fav.querySelector('.ii'), 'heart', on ? 'filled' : 'outline'); pop(fav); paintNav(); };
  favs.forEach(f => f.onclick = () => setFav(f, !f.classList.contains('on')));
  navFav.onclick = () => favs[0].onclick();

  // add to cart
  const atc = $('p-atc'), toast = $('p-toast'), badge = $('p-badge');
  let cart = 1, atcT;
  atc.onclick = () => {
    clearTimeout(atcT);
    atc.classList.add('done'); icon(atc.querySelector('.ii'), 'check'); atc.querySelector('.t').textContent = 'Added';
    cart += +$('p-q').textContent || 1; badge.textContent = cart > 9 ? '9+' : cart; pop(badge, 'bump');
    toast.classList.add('show');
    atcT = setTimeout(() => { atc.classList.remove('done'); icon(atc.querySelector('.ii'), 'basket'); atc.querySelector('.t').textContent = 'Add to cart'; toast.classList.remove('show'); }, 2200);
  };

  // quantity
  const q = $('p-q');
  $('p-minus').onclick = () => { q.textContent = Math.max(1, +q.textContent - 1); };
  $('p-plus').onclick = () => { q.textContent = Math.min(9, +q.textContent + 1); };

  // rating
  const starsHost = $('p-rate').querySelector('.stars');
  let rating = 4;
  const paintStars = n => { stars.forEach((ii, k) => icon(ii, 'star', k < n ? 'filled' : 'outline')); $('p-rv').textContent = n.toFixed(1); };
  const stars = [1, 2, 3, 4, 5].map(n => { const b = document.createElement('button'); b.type = 'button'; b.setAttribute('aria-label', n + ' stars');
    const ii = document.createElement('span'); ii.className = 'ii'; b.append(ii); starsHost.append(b);
    b.onmouseenter = () => paintStars(n); b.onclick = () => { rating = n; paintStars(n); pop(b); }; return ii; });
  starsHost.onmouseleave = () => paintStars(rating);
  paintStars(rating);

  // size
  const sizes = [...$('p-size').children];
  const setSize = b => sizes.forEach(x => { x.classList.toggle('on', x === b); x.setAttribute('aria-checked', x === b); });
  sizes.forEach(b => { b.setAttribute('role', 'radio'); b.onclick = () => setSize(b); });
  setSize(sizes[2]);

  // colour
  const dots = [...$('p-sw').children];
  const setDot = b => { dots.forEach(x => x.classList.toggle('on', x === b)); $('p-sw-l').textContent = b.getAttribute('aria-label'); };
  dots.forEach(b => b.onclick = () => setDot(b));

  // care label: name on hover
  const CARE = [['wash-30', 'Wash at 30°'], ['do-not-bleach', 'Do not bleach'], ['tumble-dry-low', 'Tumble dry low'], ['iron-low', 'Iron on low'], ['dry-clean', 'Dry clean']];
  CARE.filter(([n]) => byName[n]).forEach(([n, label]) => { const b = document.createElement('span'); b.className = 'ii'; b.title = label; icon(b, n);
    b.onmouseenter = () => { $('p-care-l').textContent = label; $('p-care').querySelectorAll('.ii').forEach(x => x.classList.toggle('on', x === b)); };
    $('p-care').append(b); });
  $('p-care').onmouseleave = () => { $('p-care-l').textContent = CARE[0][1]; $('p-care').querySelectorAll('.ii').forEach(x => x.classList.remove('on')); };

  // promo code
  const promo = $('p-promo');
  promo.onclick = () => { try { navigator.clipboard.writeText('SWOOZH20'); } catch (e) {} icon(promo.querySelector('.ii'), 'check'); promo.classList.add('on');
    setTimeout(() => { icon(promo.querySelector('.ii'), 'copy'); promo.classList.remove('on'); }, 1600); };

  // delivery tracking
  const TRACK = ['Order packed', 'Out for delivery', 'Delivered'];
  let step = 1;
  const paintTrack = () => { const parts = [...$('p-track').querySelectorAll('.steps > *')];
    parts.forEach((p, k) => p.classList.toggle('on', k <= step * 2)); $('p-track-l').textContent = TRACK[step]; };
  $('p-track').onclick = () => { step = (step + 1) % 3; paintTrack(); };
  paintTrack();

  // search: types a few queries
  const sq = $('p-search'), QUERIES = ['linen blazer', 'silk scarf', 'white sneakers', 'gold hoops'];
  if (!reduce) { let qi = 0, ch = sq.textContent.length, dir = -1, hold = 30;
    setInterval(() => { if (!visible) return; if (hold > 0) { hold--; return; }
      ch += dir; sq.textContent = QUERIES[qi].slice(0, ch);
      if (dir < 0 && ch <= 0) { qi = (qi + 1) % QUERIES.length; dir = 1; }
      else if (dir > 0 && ch >= QUERIES[qi].length) { dir = -1; hold = 30; } }, 70); }

  // demo when left alone
  if (!reduce) {
    const steps = [
      () => setFav(favs[0], true), () => { rating = 5; paintStars(5); }, () => setSize(sizes[3]), () => atc.onclick(), () => $('p-track').onclick(),
      () => setDot(dots[1]), () => setFav(favs[1], true), () => $('p-plus').onclick(), () => { rating = 4; paintStars(4); }, () => setFav(favs[0], false),
      () => setSize(sizes[2]), () => setDot(dots[0]), () => $('p-minus').onclick(), () => setFav(favs[1], false),
    ];
    let k = 0;
    setInterval(() => { if (visible && idle(performance.now()) && !document.hidden) { steps[k % steps.length](); k++; } }, 2000);
  }
})();
