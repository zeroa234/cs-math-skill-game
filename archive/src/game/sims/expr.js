// Tiny whitelisted math-expression compiler for sim parameters such as f: "(x-3)^2 + 1".
// Self-written on purpose: the sims need + - * / ^, unary minus, parentheses, a few functions and
// variables. expr-eval (last published 2022) and math.js (≈9 MB unpacked) were considered; neither
// is worth a dependency for this. Never uses eval/Function.
const FUNCS = { sin: Math.sin, cos: Math.cos, tan: Math.tan, exp: Math.exp, log: Math.log, ln: Math.log, sqrt: Math.sqrt, abs: Math.abs, tanh: Math.tanh, sigmoid: (z) => 1 / (1 + Math.exp(-z)), relu: (z) => Math.max(0, z) };
const CONSTS = { pi: Math.PI, e: Math.E };

function tokenize(src) {
  const out = [];
  const re = /\s*(?:(\d+(?:\.\d+)?(?:e[+-]?\d+)?)|([A-Za-z_][A-Za-z_0-9]*)|(\*\*|[-+*/^(),]))/gy;
  let m;
  re.lastIndex = 0;
  while (re.lastIndex < src.length) {
    const at = re.lastIndex;
    m = re.exec(src);
    if (!m) { if (/^\s*$/.test(src.slice(at))) break; throw new Error(`cannot read "${src.slice(at)}"`); }
    if (m[1]) out.push({ t: "num", v: Number(m[1]) });
    else if (m[2]) out.push({ t: "id", v: m[2] });
    else if (m[3]) out.push({ t: "op", v: m[3] === "**" ? "^" : m[3] });
  }
  return out;
}

// Grammar: sum := prod (('+'|'-') prod)* ; prod := unary (('*'|'/') unary | implicit unary)* ;
// unary := '-' unary | power ; power := atom ('^' unary)? ; atom := num | id | id '(' sum ')' | '(' sum ')'
export function compile(src) {
  const toks = tokenize(String(src));
  let i = 0;
  const peek = () => toks[i];
  const eat = (v) => { const t = toks[i]; if (!t || (v && t.v !== v)) throw new Error(`expected ${v || "more input"} in "${src}"`); i++; return t; };
  const startsAtom = (t) => t && (t.t === "num" || t.t === "id" || t.v === "(");
  function sum() {
    let a = prod();
    while (peek() && (peek().v === "+" || peek().v === "-")) { const op = eat().v; const b = prod(); const l = a; a = op === "+" ? (env) => l(env) + b(env) : (env) => l(env) - b(env); }
    return a;
  }
  function prod() {
    let a = unary();
    for (;;) {
      const t = peek();
      if (t && (t.v === "*" || t.v === "/")) { eat(); const b = unary(); const l = a; a = t.v === "*" ? (env) => l(env) * b(env) : (env) => l(env) / b(env); }
      else if (startsAtom(t)) { const b = unary(); const l = a; a = (env) => l(env) * b(env); } // 2x, 3(x+1)
      else return a;
    }
  }
  function unary() {
    if (peek()?.v === "-") { eat(); const a = unary(); return (env) => -a(env); }
    if (peek()?.v === "+") { eat(); return unary(); }
    return power();
  }
  function power() {
    const base = atom();
    if (peek()?.v === "^") { eat(); const ex = unary(); return (env) => Math.pow(base(env), ex(env)); }
    return base;
  }
  function atom() {
    const t = eat();
    if (t.t === "num") return () => t.v;
    if (t.v === "(") { const a = sum(); eat(")"); return a; }
    if (t.t === "id") {
      if (peek()?.v === "(" && FUNCS[t.v]) { eat("("); const a = sum(); eat(")"); const f = FUNCS[t.v]; return (env) => f(a(env)); }
      if (t.v in CONSTS) return () => CONSTS[t.v];
      return (env) => { if (!(t.v in env)) throw new Error(`unknown variable ${t.v}`); return env[t.v]; };
    }
    throw new Error(`unexpected "${t.v}" in "${src}"`);
  }
  const fn = sum();
  if (i !== toks.length) throw new Error(`unexpected "${toks[i].v}" in "${src}"`);
  return fn;
}

// f(x) helper and a central-difference derivative good enough for plots and gradient steps.
export const fx = (src) => { const f = compile(src); return (x) => f({ x }); };
export const derivative = (f, h = 1e-5) => (x) => (f(x + h) - f(x - h)) / (2 * h);
