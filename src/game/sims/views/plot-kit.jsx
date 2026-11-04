// Small SVG plotting kit for the sims: linear scales, recessive axes/grid, a function path, and a
// hover readout. Sized by viewBox so it stays sharp at any width.
import { useState } from "preact/hooks";

export function scales(xd, yd, W = 480, H = 300, pad = { l: 40, r: 12, t: 12, b: 28 }) {
  const sx = (x) => pad.l + ((x - xd[0]) / (xd[1] - xd[0])) * (W - pad.l - pad.r);
  const sy = (y) => H - pad.b - ((y - yd[0]) / (yd[1] - yd[0])) * (H - pad.t - pad.b);
  const ix = (px) => xd[0] + ((px - pad.l) / (W - pad.l - pad.r)) * (xd[1] - xd[0]);
  return { sx, sy, ix, W, H, pad, xd, yd };
}

export function niceTicks(lo, hi, n = 5) {
  const span = hi - lo;
  const step0 = span / n;
  const mag = 10 ** Math.floor(Math.log10(step0));
  const step = [1, 2, 5, 10].map((m) => m * mag).find((s) => s >= step0) || step0;
  const out = [];
  for (let v = Math.ceil(lo / step) * step; v <= hi + 1e-9; v += step) out.push(Math.abs(v) < 1e-12 ? 0 : +v.toPrecision(10));
  return out;
}

export function fmt(v, d = 4) {
  if (!Number.isFinite(v)) return String(v);
  if (Math.abs(v) >= 1e5 || (Math.abs(v) < 1e-4 && v !== 0)) return v.toExponential(2);
  return String(+v.toFixed(d));
}

export function Axes({ s }) {
  const xt = niceTicks(s.xd[0], s.xd[1]), yt = niceTicks(s.yd[0], s.yd[1]);
  return (
    <g class="axes">
      {xt.map((v) => <line class="grid" x1={s.sx(v)} x2={s.sx(v)} y1={s.pad.t} y2={s.H - s.pad.b} />)}
      {yt.map((v) => <line class="grid" y1={s.sy(v)} y2={s.sy(v)} x1={s.pad.l} x2={s.W - s.pad.r} />)}
      {s.yd[0] <= 0 && s.yd[1] >= 0 && <line class="axis" x1={s.pad.l} x2={s.W - s.pad.r} y1={s.sy(0)} y2={s.sy(0)} />}
      {s.xd[0] <= 0 && s.xd[1] >= 0 && <line class="axis" y1={s.pad.t} y2={s.H - s.pad.b} x1={s.sx(0)} x2={s.sx(0)} />}
      {xt.map((v) => <text class="tick" x={s.sx(v)} y={s.H - 8} text-anchor="middle">{fmt(v, 2)}</text>)}
      {yt.map((v) => <text class="tick" x={s.pad.l - 6} y={s.sy(v) + 4} text-anchor="end">{fmt(v, 2)}</text>)}
    </g>
  );
}

export function fnPath(f, s, n = 240) {
  let d = "", pen = false;
  for (let i = 0; i <= n; i++) {
    const x = s.xd[0] + ((s.xd[1] - s.xd[0]) * i) / n;
    let y;
    try { y = f(x); } catch { y = NaN; }
    const ok = Number.isFinite(y) && y > s.yd[0] - (s.yd[1] - s.yd[0]) && y < s.yd[1] + (s.yd[1] - s.yd[0]);
    if (!ok) { pen = false; continue; }
    d += (pen ? "L" : "M") + s.sx(x).toFixed(2) + "," + s.sy(y).toFixed(2);
    pen = true;
  }
  return d;
}

// Range of f over the domain, padded, for auto-scaling the y axis.
export function autoRange(fs, xd, pad = 0.1) {
  let lo = Infinity, hi = -Infinity;
  for (const f of fs) for (let i = 0; i <= 200; i++) {
    const x = xd[0] + ((xd[1] - xd[0]) * i) / 200;
    let y; try { y = f(x); } catch { continue; }
    if (Number.isFinite(y)) { lo = Math.min(lo, y); hi = Math.max(hi, y); }
  }
  if (!Number.isFinite(lo)) return [-1, 1];
  if (hi - lo < 1e-9) { lo -= 1; hi += 1; }
  const m = (hi - lo) * pad;
  return [lo - m, hi + m];
}

// SVG frame with a hover crosshair that reports x and the given readout functions.
export function Frame({ s, children, readout, label }) {
  const [hx, setHx] = useState(null);
  const onMove = (e) => {
    const svg = e.currentTarget;
    const pt = svg.createSVGPoint();
    pt.x = e.clientX; pt.y = e.clientY;
    const p = pt.matrixTransform(svg.getScreenCTM().inverse());
    if (p.x < s.pad.l || p.x > s.W - s.pad.r) { setHx(null); return; }
    setHx(s.ix(p.x));
  };
  return (
    <div class="plot">
      <svg viewBox={`0 0 ${s.W} ${s.H}`} role="img" aria-label={label} onPointerMove={onMove} onPointerLeave={() => setHx(null)}>
        <Axes s={s} />
        {children}
        {hx !== null && readout && <line class="crosshair" x1={s.sx(hx)} x2={s.sx(hx)} y1={s.pad.t} y2={s.H - s.pad.b} />}
      </svg>
      {hx !== null && readout && <div class="readout">x = {fmt(hx, 3)}{readout(hx).map(([name, v]) => <span> · {name} = {fmt(v, 4)}</span>)}</div>}
    </div>
  );
}
