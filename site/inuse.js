// Animated ecommerce flow built from Swoozh icons (layout follows the Swoozh Fashion UI Kit).
(() => {
  const S = window.SWZ; if (!S) return;
  const phone = document.getElementById('phone'); if (!phone) return;
  const ic = (n, s = 22, v = '') => `<span data-icon="${n}" data-size="${s}"${v ? ` data-variant="${v}"` : ''}></span>`;
  const status = `<div class="st"><b>9:41</b><span>${ic('signal', 14)}${ic('wifi', 14)}${ic('battery', 16)}</span></div>`;
  const tabs = on => `<div class="tabs"><span class="${on === 0 ? 'on' : ''}">${ic('store')}</span><span>${ic('search')}</span><span class="tbasket ${on === 2 ? 'on' : ''}" id="tbasket">${ic('basket')}<i id="badge">1</i></span><span>${ic('heart')}</span><span>${ic('menu')}</span></div>`;
  const img = (icon, cls = '') => `<div class="pimg ${cls}">${ic(icon, 120)}</div>`;
  const screens = [
    // 0 home
    `<div class="scr" data-s="0">${status}<h3 class="ttl">Apartments</h3>
      <div class="cat-tabs"><span>Kids</span><span class="on">Women</span><span>Men</span><span>Beauty</span><span>Home</span></div>
      <div class="blk" id="jackets">${img('jacket', 'tall')}<h4>Jackets</h4></div>
      <div class="blk">${img('dress', 'tall alt')}<h4>Dresses</h4></div>
      <div class="chipgrid"><span>Trending</span><span>Shoes</span><span>Handbags</span><span>Accessories</span></div>${tabs(0)}</div>`,
    // 1 item
    `<div class="scr" data-s="1">${status}<div class="bar">${ic('arrow-left')}${ic('share')}</div>
      <div class="hero-img">${ic('t-shirt', 150, 'filled')}<button class="fav" id="fav">${ic('heart', 22)}</button></div>
      <div class="pad"><h4 class="pn">Sweater</h4><small>Casual t-shirt · T-Shirts &amp; Sweaters</small><b class="pr">$ 39</b>
      <div class="rule"></div><div class="lbl">Color <small>Black</small></div><div class="sw"><i></i><i class="sel"></i><i class="b"></i><i class="g"></i></div>
      <div class="rule"></div><button class="btn-o" id="selsize">${ic('chevron-down', 16)} Select size</button>
      <button class="btn-d" id="add1">${ic('basket', 20)} Add to cart</button>
      <ul class="care"><li>${ic('wash-30', 18)}Machine wash 30°</li><li>${ic('iron', 18)}Iron on low heat</li><li>${ic('tumble-dry', 18)}Tumble dry gentle</li></ul></div>${tabs(0)}</div>`,
    // 2 size sheet
    `<div class="scr sheet" data-s="2">${status}<div class="bar">${ic('arrow-left')}${ic('share')}</div>
      <div class="hero-img dim">${ic('t-shirt', 120, 'filled')}</div>
      <div class="pad c"><h4 class="pn ctr">Pick size</h4><div class="sizes"><span>XS</span><span>S</span><span id="szm">M</span><span>L</span><span>XL</span></div>
      <div class="guide">${ic('ruler', 20)}Size guide<span class="push">${ic('chevron-right', 18)}</span></div>
      <button class="btn-d" id="add2">${ic('basket', 20)} Add to cart</button></div></div>`,
    // 3 added
    `<div class="scr" data-s="3">${status}<div class="bar">${ic('arrow-left')}${ic('share')}</div>
      <div class="hero-img">${ic('t-shirt', 150, 'filled')}<span class="fav on">${ic('heart', 22, 'filled')}</span></div>
      <div class="toast2">${ic('check-circle', 22)}<span>Added to cart</span></div>
      <div class="pad"><h4 class="pn">Sweater</h4><small>Casual t-shirt · M · Black</small><b class="pr">$ 39</b></div>${tabs(2)}</div>`,
    // 4 cart
    `<div class="scr" data-s="4">${status}<h3 class="ttl">Shopping cart</h3>
      <div class="row"><div class="th">${ic('t-shirt', 44, 'filled')}</div><div class="rm"><b>Sweater</b><small>Casual t-shirt · M · Black</small><span class="q">1 ${ic('chevron-down', 14)}</span><b class="pr2">$39</b></div><div class="rb"><span>${ic('trash', 18)}</span><span id="rheart">${ic('heart', 18)}</span></div></div>
      <div class="disc"><b>Discount code</b><div><span class="inp">Enter code</span><span class="usec">Use code</span></div></div>
      <div class="sum"><p><span>Price</span><span>$39</span></p><p><span>Shipping</span><span class="free">Free</span></p><p class="tot"><span>Total price (inc. vat)</span><b>$39</b></p></div>
      <div class="checkout"><div><small>Total:</small><b>$39</b></div><button class="btn-d" id="chk">${ic('credit-card', 20)} Go to checkout</button></div>${tabs(2)}</div>`,
  ];
  phone.innerHTML = '<div class="notch"></div><div class="vp">' + screens.join('') + '<div class="tap" id="tap"></div></div>';
  S.fillIcons(phone);
  const $ = id => document.getElementById(id), scr = n => phone.querySelector(`.scr[data-s="${n}"]`);
  const steps = [...document.querySelectorAll('#iu-steps li')];
  const show = n => { phone.querySelectorAll('.scr').forEach(s => s.classList.toggle('show', +s.dataset.s === n)); steps.forEach((l, i) => l.classList.toggle('on', i === n)); };
  const tap = el => { const t = $('tap'), vp = phone.querySelector('.vp'); if (!el) return; const r = el.getBoundingClientRect(), v = vp.getBoundingClientRect(), k = v.width / 390;
    t.style.left = ((r.left + r.width / 2 - v.left) / k) + 'px'; t.style.top = ((r.top + r.height / 2 - v.top) / k) + 'px'; t.classList.remove('go'); void t.offsetWidth; t.classList.add('go'); };
  const wait = ms => new Promise(r => setTimeout(r, ms));
  let run = 0, alive = true;
  const io = new IntersectionObserver(e => { alive = e[0].isIntersecting; }); io.observe(phone);
  async function loop() {
    const me = ++run;
    const ok = async ms => { await wait(ms); while (!alive && me === run) await wait(300); return me === run; };
    while (me === run) {
      show(0); $('fav').innerHTML = ic('heart', 22); S.fillIcons($('fav'));
      phone.querySelectorAll('.sizes span').forEach(s => s.classList.remove('sel')); phone.querySelectorAll('.tbasket').forEach(b => b.classList.remove('has', 'pop'));
      if (!await ok(1400)) return; tap($('jackets')); if (!await ok(700)) return;
      show(1); if (!await ok(1200)) return; tap($('fav')); await wait(250);
      $('fav').classList.add('on'); $('fav').innerHTML = ic('heart', 22, 'filled'); S.fillIcons($('fav')); if (!await ok(1000)) return;
      tap($('selsize')); if (!await ok(600)) return; show(2); if (!await ok(900)) return;
      tap($('szm')); await wait(250); $('szm').classList.add('sel'); if (!await ok(900)) return;
      tap($('add2')); if (!await ok(600)) return; show(3); phone.querySelectorAll('.tbasket').forEach(b => b.classList.add('has', 'pop')); if (!await ok(1700)) return;
      tap(scr(3).querySelector('.tbasket')); if (!await ok(600)) return; show(4); if (!await ok(3200)) return;
    }
  }
  steps.forEach(l => l.onclick = () => { run++; const n = +l.dataset.i; show(n); if (n >= 3) phone.querySelectorAll('.tbasket').forEach(b => b.classList.add('has')); setTimeout(loop, 6000); });
  loop();
})();
