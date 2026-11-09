// Parse absolute SVG path data (M L H V C Z), merge subpaths, and orient contours so that
// the even-odd look is preserved under the nonzero rule (needed for fonts and plain <path>).
const NUM = /[MLHVCZmlhvcz]|-?(?:\d+\.?\d*|\.\d+)(?:e[-+]?\d+)?/g;

export function parse(d) {
  const tok = d.match(NUM) || [];
  const subs = []; let cur = null, cmd = null, i = 0, x = 0, y = 0;
  const num = () => parseFloat(tok[i++]);
  while (i < tok.length) {
    if (/^[a-zA-Z]$/.test(tok[i])) { cmd = tok[i++]; if (cmd !== cmd.toUpperCase()) throw new Error('relative path command ' + cmd); }
    if (cmd === 'Z') { if (cur) { cur.closed = true; x = cur.start[0]; y = cur.start[1]; } cur = null; continue; }
    if (cmd === 'M') { x = num(); y = num(); cur = {start: [x, y], segs: [], closed: false}; subs.push(cur); cmd = 'L'; continue; }
    if (!cur) { cur = {start: [x, y], segs: [], closed: false}; subs.push(cur); }
    if (cmd === 'L') { x = num(); y = num(); cur.segs.push({t: 'L', p: [x, y]}); }
    else if (cmd === 'H') { x = num(); cur.segs.push({t: 'L', p: [x, y]}); }
    else if (cmd === 'V') { y = num(); cur.segs.push({t: 'L', p: [x, y]}); }
    else if (cmd === 'C') { const c1 = [num(), num()], c2 = [num(), num()]; x = num(); y = num(); cur.segs.push({t: 'C', c1, c2, p: [x, y]}); }
    else throw new Error('unsupported command ' + cmd);
  }
  return subs.filter(s => s.segs.length);
}

function poly(s) {
  const pts = [s.start]; let p0 = s.start;
  for (const g of s.segs) {
    if (g.t === 'L') pts.push(g.p);
    else for (let k = 1; k <= 8; k++) {
      const t = k / 8, u = 1 - t;
      pts.push([0, 1].map(j => u*u*u*p0[j] + 3*u*u*t*g.c1[j] + 3*u*t*t*g.c2[j] + t*t*t*g.p[j]));
    }
    p0 = g.p;
  }
  return pts;
}
const area = P => { let a = 0; for (let i = 0; i < P.length; i++) { const [x1, y1] = P[i], [x2, y2] = P[(i + 1) % P.length]; a += x1*y2 - x2*y1; } return a / 2; };
function inside(pt, P) {
  let c = false;
  for (let i = 0, j = P.length - 1; i < P.length; j = i++) {
    const [xi, yi] = P[i], [xj, yj] = P[j];
    if ((yi > pt[1]) !== (yj > pt[1]) && pt[0] < (xj - xi) * (pt[1] - yi) / (yj - yi) + xi) c = !c;
  }
  return c;
}
function reverse(s) {
  const pts = [s.start, ...s.segs.map(g => g.p)];
  const segs = [];
  for (let k = s.segs.length - 1; k >= 0; k--) {
    const g = s.segs[k], to = pts[k];
    segs.push(g.t === 'L' ? {t: 'L', p: to} : {t: 'C', c1: g.c2, c2: g.c1, p: to});
  }
  return {start: pts[pts.length - 1], segs, closed: s.closed};
}

export function orient(subs) {
  const P = subs.map(poly), A = P.map(area);
  return subs.map((s, i) => {
    if (Math.abs(A[i]) < 1e-9) return s;
    const probes = [0.17, 0.5, 0.83].map(f => P[i][Math.floor(f * (P[i].length - 1))]);
    let depth = 0;
    P.forEach((Q, j) => { if (j !== i && Math.abs(A[j]) > Math.abs(A[i]) * 0.999 && probes.filter(pt => inside(pt, Q)).length >= 2) depth++; });
    const wantPos = depth % 2 === 0;
    return (A[i] > 0) === wantPos ? s : reverse(s);
  });
}

const f = v => { let s = (Math.round(v * 1000) / 1000).toString(); if (s === '-0') s = '0'; return s; };
const pair = p => f(p[0]) + ' ' + f(p[1]);
export function serialize(subs) {
  return subs.map(s => {
    let d = 'M' + pair(s.start), prev = s.start;
    for (const g of s.segs) {
      if (g.t === 'L') {
        if (f(g.p[1]) === f(prev[1]) && f(g.p[0]) !== f(prev[0])) d += 'H' + f(g.p[0]);
        else if (f(g.p[0]) === f(prev[0]) && f(g.p[1]) !== f(prev[1])) d += 'V' + f(g.p[1]);
        else if (f(g.p[0]) !== f(prev[0]) || f(g.p[1]) !== f(prev[1])) d += 'L' + pair(g.p);
      } else d += 'C' + pair(g.c1) + ' ' + pair(g.c2) + ' ' + pair(g.p);
      prev = g.p;
    }
    return d + (s.closed ? 'Z' : '');
  }).join('').replace(/ -/g, '-');
}

export function fixSvg(svg) {
  // each <path> keeps its own even-odd holes; separate paths overlap as union (nonzero)
  const vb = svg.match(/viewBox="0 0 24 24"/);
  if (!vb) throw new Error('unexpected viewBox ' + svg.slice(0, 120));
  return [...svg.matchAll(/ d="([^"]*)"/g)].map(m => serialize(orient(parse(m[1])))).join('');
}
