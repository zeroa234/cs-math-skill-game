// Section-number parsing for chapter ordering (shared by scripts/build-data.mjs and tests).
const CN_DIGITS = { 零: 0, 〇: 0, 一: 1, 二: 2, 两: 2, 三: 3, 四: 4, 五: 5, 六: 6, 七: 7, 八: 8, 九: 9 };
function cnToInt(s) {
  if (/^\d+$/.test(s)) return Number(s);
  let total = 0, cur = 0;
  for (const ch of s) {
    if (ch === "百") { total += (cur || 1) * 100; cur = 0; }
    else if (ch === "十") { total += (cur || 1) * 10; cur = 0; }
    else if (ch in CN_DIGITS) cur = CN_DIGITS[ch];
    else return NaN;
  }
  return total + cur;
}

// First section number in a free-text section reference: "2.2 The Limit…" → [2,2], "Unit 3: …" → [3],
// "第 7–10 章" → [7], "第二章" → [2], "§4.1" → [4,1]. Returns null when there is no number.
export function sectionKey(text) {
  if (!text) return null;
  const cn = text.match(/第\s*([一二两三四五六七八九十百零〇\d]+)\s*[章讲节课周部篇单元]/);
  if (cn) { const n = cnToInt(cn[1]); if (!Number.isNaN(n)) return [n]; }
  // Not section numbers: "(1)–(3)" lecture parts, "20 页" / "14 pages" / "pp. 30" page counts, years.
  const cleaned = text
    .replace(/\(\d+\)/g, " ")
    .replace(/\d+\s*(?:页|pages?\b)/gi, " ")
    .replace(/\bpp?\.\s*\d+(?:\s*[–-]\s*\d+)?/gi, " ")
    .replace(/\b(?:19|20)\d\d\b/g, " ");
  const m = cleaned.match(/(\d+(?:\.\d+)*)/);
  return m ? m[1].split(".").map(Number) : null;
}

export const cmpKey = (a, b) => {
  for (let i = 0; i < Math.max(a.length, b.length); i++) {
    const d = (a[i] ?? -1) - (b[i] ?? -1);
    if (d) return d;
  }
  return 0;
};
