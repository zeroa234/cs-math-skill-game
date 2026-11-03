// Validates content packs without writing anything (safe to run while others build).
// usage: node scripts/check-pack.mjs data/content/C.2.1.yaml [more.yaml…]
// Needs src/gen/tree.json (run `npm run data` once). Exit code 1 when any pack has errors.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { loadPack, validatePack } from "./lib/packs.mjs";
import { normalizeLesson } from "../src/game/core/lesson.js";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const tree = JSON.parse(fs.readFileSync(path.join(ROOT, "src/gen/tree.json"), "utf8"));
const byId = Object.fromEntries(tree.skills.map((s) => [s.id, s]));
// Every pack on disk, so a pack may use terms its prerequisites' packs define (beginner standard).
const dir = path.join(ROOT, "data/content");
const packsBySkill = {};
for (const f of fs.readdirSync(dir).filter((f) => f.endsWith(".yaml"))) { try { const p = loadPack(path.join(dir, f)); packsBySkill[p.skill] = p; } catch {} }
let bad = 0;
for (const f of process.argv.slice(2)) {
  let errs;
  try {
    const pack = loadPack(f);
    errs = validatePack(pack, byId[pack?.skill], path.basename(f), { byId, packsBySkill });
    if (!errs.length) {
      const items = pack.lessons.reduce((n, l) => n + normalizeLesson(l).items.length, 0);
      console.log(`ok  ${f}: ${pack.lessons.length} lessons, ${items} items, chapters ${byId[pack.skill].chapters.map((c) => c.no + "." + c.title).join(" / ")}`);
    }
  } catch (err) {
    errs = [`${f}: ${err.message}`];
  }
  if (errs.length) { bad++; console.log(`ERR ${f}\n  - ` + errs.join("\n  - ")); }
}
process.exit(bad ? 1 : 0);
