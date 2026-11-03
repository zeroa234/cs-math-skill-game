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
