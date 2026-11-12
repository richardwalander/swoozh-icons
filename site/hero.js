// Hero: Swoozh Icons in use. Cards drift with the pointer (parallax by depth), the faint icon pattern
// lights up around the cursor, and every control works. When left alone it plays a short demo.
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

  // pattern
  const pat = $('pat');
  const names = 'heart search wash-30 basket user hanger store star iron tag shopping-bag gift percent package bell truck calendar dress sneaker lipstick ruler credit-card high-heel perfume-bottle'.split(' ').filter(n => byName[n]);
  for (let k = 0; k < 100; k++) { const sp = document.createElement('span'); draw(sp, names[(k * 7) % names.length]); pat.append(sp); }
  const patIcons = [...pat.children].map((el, k) => ({el: el.firstChild, x: -60 + (k % 10) * 72 + 36, y: -60 + Math.floor(k / 10) * 72 + 36}));
  const light = (px, py) => patIcons.forEach(p => { const d = Math.hypot(p.x - px, p.y - py);
    p.el.style.setProperty('--o', (0.06 + 0.42 * Math.max(0, 1 - d / 170)).toFixed(3)); });

  // parallax
  const cards = [...stage.querySelectorAll('.pc')].map((el, k) => ({el, d: +el.dataset.d || .5, ph: k * 1.3}));
  const cur = {x: 0, y: 0}, tgt = {x: 0, y: 0};
  let lastUser = performance.now() - 2500, visible = true;
  const onMove = e => {
    const r = play.getBoundingClientRect();
    tgt.x = Math.max(-1, Math.min(1, (e.clientX - r.left - r.width / 2) / (r.width / 2)));
    tgt.y = Math.max(-1, Math.min(1, (e.clientY - r.top - r.height / 2) / (r.height / 2)));
    light((e.clientX - r.left) / s, (e.clientY - r.top) / s);
    lastUser = performance.now();
  };
  const hero = play.closest('section') || play;
  hero.addEventListener('pointermove', onMove);
  hero.addEventListener('pointerleave', () => { tgt.x = tgt.y = 0; light(-999, -999); });
  play.addEventListener('pointerdown', () => { lastUser = performance.now(); });

  const idle = t => t - lastUser > 5000;
  const frame = t => {
    if (visible) {
      if (idle(t) && !reduce) { // slow drift so the scene breathes on its own
        tgt.x = Math.sin(t / 2600) * .55; tgt.y = Math.cos(t / 3400) * .45;
        light(W / 2 + tgt.x * 220, W / 2 + tgt.y * 220);
      }
      cur.x += (tgt.x - cur.x) * .07; cur.y += (tgt.y - cur.y) * .07;
      for (const c of cards) {
        const f = reduce ? 0 : Math.sin(t / 1600 + c.ph) * 4;
        c.el.style.setProperty('--x', (cur.x * c.d * 26).toFixed(2) + 'px');
        c.el.style.setProperty('--y', (cur.y * c.d * 26 + f * c.d).toFixed(2) + 'px');
      }
      pat.style.transform = `translate(${(-cur.x * 10).toFixed(2)}px, ${(-cur.y * 10).toFixed(2)}px)`;
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
