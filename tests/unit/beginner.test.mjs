// The beginner standard's checks (scripts/lib/beginner.mjs): each rule must fire on a pack that breaks
// it and stay quiet on one that follows it; look-up links must land only where they are allowed.
import test from "node:test";
import assert from "node:assert/strict";
import { beginnerIssues, resolveTerms } from "../../scripts/lib/beginner.mjs";
import { coverageIssues } from "../../scripts/lib/coverage.mjs";
import { normalizeLesson } from "../../src/game/core/lesson.js";

const q = (id, prompt = "1 + 1？", extra = {}) => ({ id, type: "number", prompt, answer: 2, explain: "因为 1 + 1 = 2。", ...extra });
const lesson = (flow) => normalizeLesson({ id: "l", chapter: "c", title: "t", flow });
const boss = { items: [1, 2, 3, 4, 5].map((i) => q("b" + i)) };
// The fixtures are tiny lessons, so B8 (a lesson's worth of explanation) is left out except in its own test.
const allRules = (pack, lessons, opts) => beginnerIssues({ boss, ...pack }, lessons, opts).map((m) => m.split(" ")[0]);
const rules = (pack, lessons, opts) => allRules(pack, lessons, opts).filter((r) => r !== "B8");

test("B1: jargon before its definition is caught; defined, inherited or assumed jargon is fine", () => {
  const early = lesson([{ item: q("a", "这个变量是多少？") }, { card: { body: "**变量（variable）**是名字。" } }, { item: q("b") }]);
  assert.deepEqual(rules({ terms: [{ term: "变量", def: "名字" }] }, [early]), ["B1"]);
  const ok = lesson([{ card: { body: "**变量（variable）**是名字。" } }, { item: q("a", "这个变量是多少？") }, { item: q("b") }]);
  assert.deepEqual(rules({ terms: [{ term: "变量", def: "名字" }] }, [ok]), []);
  assert.deepEqual(rules({}, [early], { inherited: new Set(["变量"]) }), [], "taught by a prerequisite's pack");
  assert.deepEqual(rules({ assumes: ["变量"] }, [early]), [], "listed under assumes");
  assert.deepEqual(rules({}, [ok]), ["B1"], "defined in a card but missing from terms");
});

test("B1 in code: a program using a keyword from a later lesson is caught; the teaching lesson, strings, comments and inline code are not", () => {
  const terms = { terms: [{ term: "循环", def: "重复" }] };
  const loopCode = "counts = {}\nfor w in 'aba':\n    counts[w] = 1\n";
  const looped = (extra = {}) => ({ item: q("a", "显示什么？", { code: loopCode, lang: "python", ...extra }) });
  const teachLoop = lesson([{ card: { body: "**循环（loop）**：重复做。" } }, { item: q("c") }, { item: q("d") }]);
  // P.1.1, 2026-11-04: the dictionary lesson counted with a for loop two lessons before for was taught
  assert.deepEqual(rules(terms, [lesson([looped(), { item: q("b") }]), teachLoop]), ["B1"]);
  assert.deepEqual(rules(terms, [teachLoop, lesson([looped(), { item: q("b") }])]), [], "after the lesson that teaches it");
  const guessFirst = lesson([{ guess: q("g", "猜一猜？", { code: "for i in range(3):\n    print(i)", lang: "python" }) }, { card: { body: "**循环（loop）**：重复做。" } }, { item: q("c") }, { item: q("d") }]);
  assert.deepEqual(rules(terms, [guessFirst]), [], "the lesson that teaches it may show it first");
  assert.deepEqual(rules({}, [lesson([{ item: q("a", "显示什么？", { code: 'print("for while")  # for each', lang: "python" }) }, { item: q("b") }])]), [], "strings and comments");
  assert.deepEqual(rules({}, [lesson([{ card: { body: "不能用 `for` 当名字。" } }, { item: q("a") }, { item: q("b") }])]), [], "inline code names a keyword");
  assert.deepEqual(rules({}, [lesson([{ card: { body: "看：\n\n```c\n// look for it\nint format = 1;\n```" } }, { item: q("a") }, { item: q("b") }])]), [], "C comments, words containing a keyword");
  assert.deepEqual(rules({}, [lesson([{ card: { body: "看：\n\n```python\nwhile True:\n    pass\n```" } }, { item: q("a") }, { item: q("b") }])]), ["B1"], "fenced blocks in cards");
  assert.deepEqual(rules({}, [lesson([{ card: { body: "**第三方库（third-party library）**要先导入：\n\n```python\nimport pandas as pd\n```" } }, { item: q("a") }, { item: q("b") }])]).filter((r) => r === "B1").length, 1, "import is fine once any of its terms is taught (the remaining B1 is the missing terms entry)");
});

test("B2, B3, B4: three cards in a row, an overlong card, a graded sim before any demo", () => {
  const card = { card: { body: "一句话。" } };
  assert.deepEqual(rules({}, [lesson([card, card, card, { item: q("a") }, { item: q("b") }])]), ["B2"]);
  assert.deepEqual(rules({}, [lesson([{ card: { body: "字".repeat(241) } }, { item: q("a") }, { item: q("b") }])]), ["B3"]);
  assert.deepEqual(rules({}, [lesson([{ card: { body: "字".repeat(240) + "\n\n```python\n" + "x = 1\n".repeat(80) + "```" } }, { item: q("a") }, { item: q("b") }])]), [], "code is not counted");
  const sim = { id: "s", type: "sim", sim: "trace", prompt: "走一遍", explain: "这样。", params: { code: "x = 1" }, goal: { ask: [] } };
  assert.deepEqual(rules({}, [lesson([card, { item: sim }, { item: q("b") }])]), ["B4"]);
  assert.deepEqual(rules({}, [lesson([{ card: { body: "看。", sim: { name: "trace", params: { code: "x = 1" } } } }, { item: sim }, { item: q("b") }])]), []);
});

test("B5, B6, B7: skipped steps, self-assessment, too few final checks", () => {
  assert.deepEqual(rules({}, [lesson([{ card: { body: "显然成立。" } }, { item: q("a") }, { item: q("b") }])]), ["B5"]);
  assert.deepEqual(rules({}, [lesson([{ card: { body: "做完请自评。" } }, { item: q("a") }, { item: q("b") }])]), ["B6"]);
  assert.deepEqual(beginnerIssues({ boss: { items: [q("x")] } }, [lesson([{ card: { body: "一句。" } }, { item: q("a") }, { item: q("b") }])], { coreChapters: 6 }).map((m) => m.split(" ")[0]).filter((r) => r !== "B8"), ["B7"]);
});

// 2026-11-08: 35 packs of "guess, 2 cards, 2 two-option questions" passed B1–B7 (reports/quality-audit-2026-11-08.md).
test("B8, B9, B10: a lesson's worth of explanation and questions, a final challenge guessing cannot pass, definitions that stand alone", () => {
  const card = (n) => ({ card: { body: "例".repeat(n) } });
  const template = lesson([card(100), { item: q("a") }, card(100), { item: q("b") }]);
  assert.deepEqual([...new Set(allRules({}, [template]))], ["B8"], "200 characters and 2 questions");
  const full = lesson([card(210), { item: q("a") }, { item: q("b") }, card(210), { item: q("c") }, { item: q("d") }]);
  assert.deepEqual(allRules({}, [full]), [], "420 characters and 4 questions");
  const two = (id) => ({ id, type: "choice", prompt: "哪个？", options: [{ text: "甲", correct: true }, { text: "乙", why: "不是乙。" }], explain: "甲。" });
  assert.deepEqual(rules({ boss: { items: [1, 2, 3, 4, 5].map((i) => two("b" + i)) } }, [full]), ["B9"], "five two-option choices: 4 of 5 by chance is 19 %");
  assert.deepEqual(rules({}, [full]), [], "typed answers cannot be guessed");
  assert.deepEqual(rules({ terms: [{ term: "自旋锁", def: "，忙等直到锁可用" }] }, [full]).filter((r) => r === "B10"), ["B10"], "cut out of a card's sentence");
  assert.deepEqual(rules({ terms: [{ term: "静态库", def: ".a 文件：链接时复制进程序" }] }, [full]).filter((r) => r === "B10"), [], "a file extension may lead");
});

test("C1 depth: a coverage table may not hand more sections to a pack than its explanation can teach", () => {
  const outline = { outline: [{ number: "1", title: "c", items: [1, 2, 3, 4].map((i) => ({ number: "1." + i, title: "s" + i })) }] };
  const pack = (n) => ({ lessons: [{ id: "l", flow: [{ card: { body: "例".repeat(n) } }] }] });
  const table = "| 节 | 原文 | 课 |\n|---|---|---|\n" + [1, 2, 3, 4].map((i) => `| 1.${i} | s${i} | \`l\` |`).join("\n");
  assert.deepEqual(coverageIssues("X", outline, pack(400), table).issues.map((m) => m.split(":")[0]), ["C1 depth"], "4 sections from 400 characters");
  assert.deepEqual(coverageIssues("X", outline, pack(800), table).issues, [], "4 sections from 800 characters");
});

test("look-up links: first use in questions, not in the defining lesson's cards, not in code or options", () => {
  const pack = { terms: [{ term: "变量", def: "指向值的名字 [如 x]" }, { term: "局部变量", def: "函数里的名字" }, { term: "值", def: "数据" }] };
  const l1 = lesson([{ card: { body: "**变量**是名字，变量很常用。" } }, { item: q("a", "变量 `变量` 和局部变量，还有变量和值", { options: undefined }) }]);
  const l2 = lesson([{ card: { body: "上一课的变量。" } }, { item: { id: "c", type: "choice", prompt: "选", explain: "因为变量。", options: [{ text: "[[变量]]", correct: true, why: "变量" }, { text: "否" }] } }]);
  const [r1, r2] = resolveTerms(pack, [l1, l2]).lessons;
  assert.equal(r1.flow[0].card.body, "**变量**是名字，变量很常用。", "the lesson that defines a term does not link it in its cards");
  const p = r1.flow[1].item.prompt;
  assert.match(p, /^\[\[变量\|/, "first use in a question is linked");
  assert.equal((p.match(/\[\[变量\|/g) || []).length, 1, "only the first use");
  assert.match(p, /`变量`/, "code is left alone");
  assert.match(p, /\[\[局部变量\|/, "longer terms win over the terms inside them");
  assert.ok(!/\[\[值\|/.test(p), "single-character terms are not auto-linked");
  assert.ok(decodeURIComponent(p).includes("[如 x]"), "definitions survive brackets");
  assert.match(r2.flow[0].card.body, /\[\[变量\|/, "a later lesson's card links an earlier term");
  assert.equal(r2.flow[1].item.options[0].text, "变量", "no links inside option buttons");
  assert.equal(r2.flow[1].item.options[0].why, "变量");
});
