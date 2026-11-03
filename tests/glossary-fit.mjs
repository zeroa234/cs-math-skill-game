// Focused regression for clipped glossary definitions; no full lesson or layout sweep.
// usage: node tests/glossary-fit.mjs [web-directory]
// GLOSSARY_CASES=integer-phone runs just the screenshot's reproduction.
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { ROOT, launchEdge } from "../scripts/lib/edge.mjs";
import { answerCorrectly } from "./lib/play.mjs";

const web = path.resolve(process.argv[2] || path.join(ROOT, "output/web"));
const url = pathToFileURL(path.join(web, "index.html")).href;
const out = path.join(ROOT, "temp/glossary-fit");
fs.mkdirSync(out, { recursive: true });
const packs = JSON.parse(fs.readFileSync(path.join(ROOT, "src/gen/content.json"), "utf8"));
const cases = [
  { name: "integer-phone", width: 390, height: 844, skill: "P.1.1", lesson: "tuples-sets", step: 4, term: "整数" },
  { name: "integer-short-phone", width: 360, height: 640, skill: "P.1.1", lesson: "tuples-sets", step: 4, term: "整数" },
  { name: "long-definition", width: 320, height: 640, skill: "P.2.2", lesson: "multi-file", step: 1, term: "声明" },
  { name: "answer-feedback", width: 360, height: 640, skill: "P.2.2", lesson: "multi-file", step: 2, term: "声明", feedback: true },
  { name: "integer-desktop", width: 1366, height: 860, skill: "P.1.1", lesson: "tuples-sets", step: 4, term: "整数" },
];
const selected = process.env.GLOSSARY_CASES?.split(",");
const browser = await launchEdge(path.join(out, "browser"));
const errors = [];

try {
  for (const c of cases.filter((c) => !selected || selected.includes(c.name))) {
    const ctx = await browser.newContext({ viewport: { width: c.width, height: c.height }, isMobile: c.width < 760, hasTouch: c.width < 760, colorScheme: "dark", reducedMotion: "reduce" });
    const p = await ctx.newPage();
    p.setDefaultTimeout(6000);
    p.on("pageerror", (e) => errors.push(`${c.name}: ${e.message}`));
    try {
      const lesson = packs[c.skill].lessons.find((l) => l.id === c.lesson);
      await p.goto(url + `#/lesson/${c.skill}/${c.lesson}`);
      await p.waitForSelector(".player .lcard");
      await p.evaluate(() => document.fonts.ready);
      const next = p.locator(".answer-bar .inner > .btn");
      for (let i = 0; i < c.step; i++) {
        const s = lesson.flow[i];
        if (s.item) {
          assert(await answerCorrectly(p, s.item), `cannot answer ${s.item.id}`);
          await next.click();
          await p.waitForFunction(() => document.querySelector(".answer-bar .inner > .btn")?.textContent.trim() === "继续");
        }
        await next.click();
        await p.waitForFunction((n) => document.querySelector(".pcount")?.textContent.trim().startsWith(n + " /"), i + 2);
      }
      if (c.feedback) {
        assert(await answerCorrectly(p, lesson.flow[c.step].item));
        await next.click();
        await p.waitForSelector(".answer-bar.is-good");
        await p.waitForTimeout(250);
      }

      const host = c.feedback ? ".answer-bar .verdict" : ".lcard";
      const term = p.locator(`${host} .term`).filter({ hasText: new RegExp(`^${c.term}$`) }).first();
      await term.click();
      const definition = p.locator(".term-def:not([hidden])");
      assert.equal(await definition.count(), 1, "exactly one definition opens");
      if (!c.feedback) {
        const contained = await definition.evaluate((el) => {
          const d = el.getBoundingClientRect(), card = el.closest(".lcard").getBoundingClientRect();
          return d.top >= card.top && d.bottom <= card.bottom && d.left >= card.left && d.right <= card.right;
        });
        assert(contained, "definition extends beyond the clipped lesson card");
      }
      await definition.evaluate((el) => el.scrollIntoView({ block: "center" }));
      const reachable = await definition.evaluate((el) => {
        const text = el.firstChild, range = document.createRange();
        range.setStart(text, text.length - 1);
        range.setEnd(text, text.length);
        const last = range.getBoundingClientRect();
        const hit = document.elementFromPoint(last.x + last.width / 2, last.y + last.height / 2);
        return { visible: !!hit && el.contains(hit), horizontalFit: document.documentElement.scrollWidth <= document.documentElement.clientWidth };
      });
      assert(reachable.visible, "the final characters cannot be scrolled into view (clipped or covered)");
      assert(reachable.horizontalFit, "opening the definition causes horizontal overflow");
      await p.screenshot({ path: path.join(out, `${c.name}.png`) });

      await p.keyboard.press("Escape");
      assert.equal(await p.locator(".term-def:not([hidden])").count(), 0, "Escape closes the definition");
      await term.click();
      const other = p.locator(`${host} .term`).filter({ hasNotText: new RegExp(`^${c.term}$`) }).first();
      await other.click();
      assert.equal(await p.locator('.term[aria-expanded="true"]').count(), 1, "switching terms closes the previous definition");
      await other.click();
      assert.equal(await p.locator(".term-def:not([hidden])").count(), 0, "tapping the same term closes it");
      await next.click();
      assert.equal(await p.locator(".term-def:not([hidden])").count(), 0, "continuing does not leave a definition behind");
      console.log(`ok — ${c.name}: complete definition reachable, no overflow, open/close/switch/continue work`);
    } catch (e) {
      errors.push(`${c.name}: ${e.message}`);
      await p.screenshot({ path: path.join(out, `${c.name}-fail.png`) });
    } finally {
      await ctx.close();
    }
  }
} finally {
  await browser.close();
}
if (errors.length) { console.error(errors.join("\n")); process.exitCode = 1; }
