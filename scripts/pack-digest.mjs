// Prints a compact, reviewable digest of content packs: cards, every item with its answer.
// usage: node scripts/pack-digest.mjs data/content/C.2.1.yaml [--cards]
import { loadPack } from "./lib/packs.mjs";
import { normalizeLesson } from "../src/game/core/lesson.js";

const showCards = process.argv.includes("--cards");
const ans = (it) => {
  switch (it.type) {
    case "choice": return it.options.map((o, i) => `${o.correct ? "✔" : "·"}${o.text}${o.why ? ` (${o.why})` : ""}`).join(" | ");
    case "number": return `= ${it.answer}${it.tolerance !== undefined ? " ±" + it.tolerance : ""}${it.unit ? " " + it.unit : ""}`;
    case "text": return `= ${it.answers.join(" / ")}`;
    case "order": return it.steps.join(" → ");
    case "match": return it.pairs.map((p) => p.join("→")).join("; ");
    case "sim": return `${it.sim} params=${JSON.stringify(it.params)} goal=${JSON.stringify(it.goal)} solution=${JSON.stringify(it.solution)}`;
  }
};
const one = (s) => String(s ?? "").replace(/\s+/g, " ").trim();
for (const f of process.argv.slice(2).filter((a) => !a.startsWith("--"))) {
  const p = loadPack(f);
  console.log(`\n######## ${p.skill}\nWHY: ${one(p.brief.why)}\nOUT: ${p.brief.outcomes.join(" / ")}`);
  for (const l of p.lessons) {
    console.log(`\n=== [${l.chapter}] ${l.id}: ${l.title}`);
    for (const st of normalizeLesson(l).flow) {
      if (st.card) { const c = st.card; console.log(`  CARD ${c.title || ""}${c.sim ? ` [sim ${c.sim.name} ${JSON.stringify(c.sim.params).slice(0, 120)}]` : ""}${showCards ? "\n    " + one(c.body) + (c.reveal || []).map((r) => `\n    > ${r.title || ""} ${one(r.body)}`).join("") : ""}`); continue; }
      const it = st.item;
      console.log(`  - ${st.kind === "guess" ? "GUESS " : ""}${it.id} (${it.type}) ${one(it.prompt)}${it.code ? "\n      CODE: " + one(it.code) : ""}\n      ANS: ${one(ans(it))}\n      EXP: ${one(it.explain)}`);
    }
  }
  for (const it of p.boss?.items || []) console.log(`  BOSS ${it.id} (${it.type}) ${one(it.prompt)}\n      ANS: ${one(ans(it))}\n      EXP: ${one(it.explain)}`);
}
