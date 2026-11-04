// Markdown + KaTeX for lesson text (marked with marked-katex-extension). Content is authored in this
// repository, not by players, so rendering it as HTML is safe.
import { Marked } from "marked";
import markedKatex from "marked-katex-extension";
import { useMemo } from "preact/hooks";

const md = new Marked(markedKatex({ throwOnError: false, nonStandard: true }));
md.setOptions({ gfm: true, breaks: false });

// Glossary terms: the build turns terms into [[term|definition]] (scripts/lib/beginner.mjs, resolveTerms); here they
// become a button that shows the definition right below, so a term met again in a review weeks later
// can be looked up without leaving the question.
const esc = (t) => t.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
const TERM = /\[\[([^\]|]+)\|([^\]]+)\]\]/g;
const withTerms = (t) => t.replace(TERM, (_, term, def) => `<button type="button" class="term" aria-expanded="false">${esc(term)}</button><span class="term-def" role="note" hidden>${esc(term)}：${esc(decodeURIComponent(def))}</span>`);
// One definition open at a time; a click anywhere else (or Escape) closes it.
if (typeof document !== "undefined") {
  const closeAll = (except) => document.querySelectorAll('.term[aria-expanded="true"]').forEach((b) => { if (b !== except) { b.setAttribute("aria-expanded", "false"); if (b.nextElementSibling) b.nextElementSibling.hidden = true; } });
  document.addEventListener("click", (e) => {
    const b = e.target.closest?.(".term");
    closeAll(b);
    if (!b) return;
    const open = b.getAttribute("aria-expanded") !== "true";
    b.setAttribute("aria-expanded", String(open));
    if (b.nextElementSibling) b.nextElementSibling.hidden = !open;
  });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeAll(null); });
}

// Formulas, tables and code wider than the column scroll sideways (style.css). Phones show no scrollbar, so
// a cut-off formula looked finished: the side that has more now fades out (classes more-l / more-r, a CSS
// mask, so it works on any background) and the fade goes when that end is reached. Wide ones also get
// tabindex=0 so the keyboard can scroll them. Re-checked whenever the page changes, scrolls or resizes.
const SCROLLERS = ".md .katex-display, .md .katex-line, .md table, .md pre, pre.code";
// Inline formulas: KaTeX breaks them only after top-level relations and operators (= + − …), as TeX does. A
// piece with no such break (a list "a, b, c", a wide fraction) can be wider than the line, which widened the
// whole page; such a formula gets a line of its own (class katex-line) that scrolls and fades like a display one.
function fitInline(el) {
  if (el.classList.contains("katex-line") || el.closest(".katex-display, table")) return;
  const box = el.closest("p, li, blockquote, .md");
  if (!box) return;
  const right = box.getBoundingClientRect().right - parseFloat(getComputedStyle(box).paddingRight);
  if ([...el.getClientRects()].some((r) => r.right > right + 1)) el.classList.add("katex-line");
}
function markScroller(el) {
  const max = el.scrollWidth - el.clientWidth, wide = max > 1;
  el.classList.toggle("more-l", wide && el.scrollLeft > 1);
  el.classList.toggle("more-r", wide && el.scrollLeft < max - 1);
  if (wide) el.tabIndex = 0;
  else el.removeAttribute("tabindex");
}
if (typeof document !== "undefined" && typeof MutationObserver !== "undefined") {
  let queued = false, refit = false;
  const markAll = () => {
    queued = false;
    // the width changed: put lifted formulas back inline and measure again (fitInline lifts them if still needed)
    if (refit) { refit = false; document.querySelectorAll(".katex-line").forEach((e) => { e.classList.remove("katex-line", "more-l", "more-r"); e.removeAttribute("tabindex"); }); }
    document.querySelectorAll(".md .katex").forEach(fitInline);
    document.querySelectorAll(SCROLLERS).forEach(markScroller);
  };
  const later = () => { if (!queued) { queued = true; requestAnimationFrame(markAll); } };
  const resized = () => { refit = true; later(); };
  new MutationObserver(later).observe(document.documentElement, { childList: true, subtree: true });
  window.addEventListener("resize", resized);
  document.fonts?.ready.then(resized);
  document.addEventListener("scroll", (e) => { if (e.target instanceof Element && e.target.matches(SCROLLERS)) markScroller(e.target); }, { capture: true, passive: true });
}

export function renderMd(text, inline = false) {
  if (!text) return "";
  const t = withTerms(String(text));
  return inline ? md.parseInline(t) : md.parse(t);
}

export function Md({ text, inline, class: cls }) {
  const html = useMemo(() => renderMd(text, inline), [text, inline]);
  const Tag = inline ? "span" : "div";
  return <Tag class={"md " + (cls || "")} dangerouslySetInnerHTML={{ __html: html }} />;
}

// Plain text with newlines kept (for the original exercises, which are not Markdown-safe).
export function Pre({ text }) {
  return <div class="md">{renderMdBlocks(text)}</div>;
}
function renderMdBlocks(text) {
  return <div dangerouslySetInnerHTML={{ __html: renderMd(text) }} />;
}
