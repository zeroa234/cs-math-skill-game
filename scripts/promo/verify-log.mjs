// “核对”那一拍终端里滚的字：真的把 tests/content/*.verify.py 跑一遍，记下命令、最后一行输出和用时。
// P.2.2、C.2.1 要 gcc（本机没有就用 WSL 的，见 docs/development.md“测试”）。约 1–2 分钟。
// 输出 src/promo/public/build/verify.json。用法：node scripts/promo/verify-log.mjs
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const content = JSON.parse(fs.readFileSync(path.join(ROOT, "src/gen/content.json"), "utf8"));
const tree = JSON.parse(fs.readFileSync(path.join(ROOT, "src/gen/tree.json"), "utf8"));
const name = Object.fromEntries(tree.skills.map((s) => [s.id, s.name]));
const runs = [];
for (const id of Object.keys(content)) {
  const script = `tests/content/${id}.verify.py`;
  if (!fs.existsSync(path.join(ROOT, script))) continue;
  const t = Date.now();
  const outText = execFileSync("python", ["-I", script], { cwd: ROOT, encoding: "utf8", timeout: 600000 });
  const last = outText.trim().split("\n").at(-1);
  const m = /^(\d+)\/(\d+) claims hold$/.exec(last);
  if (!m || m[1] !== m[2]) throw new Error(`${script} 没有全部通过：${last}`);
  runs.push({ id, name: name[id], cmd: `python -I ${script}`, last, claims: +m[2], sec: +((Date.now() - t) / 1000).toFixed(1), tool: /gcc/.test(fs.readFileSync(path.join(ROOT, script), "utf8").slice(0, 600)) ? "gcc" : "Python" });
  console.log(id, last, runs.at(-1).sec + " s");
}
fs.mkdirSync(path.join(ROOT, "src/promo/public/build"), { recursive: true });
fs.writeFileSync(path.join(ROOT, "src/promo/public/build/verify.json"), JSON.stringify({ at: new Date().toISOString(), runs, total: runs.reduce((n, r) => n + r.claims, 0) }, null, 1));
console.log("verify.json：共", runs.reduce((n, r) => n + r.claims, 0), "处");
