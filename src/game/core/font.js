// Font options and pure helpers (used by both app/font.js and unit tests).
export const FONTS = [
  { id: "pixel", short: "像素", name: "像素字体（默认）", desc: "全界面使用 Fusion Pixel 像素字体，最贴合像素奇幻画风。" },
  { id: "mixed", short: "混排", name: "像素标题 + 清晰正文", desc: "标题和关卡保留像素字体，课文、选项与代码改用系统清晰字体。" },
  { id: "sans", short: "清晰", name: "清晰黑体（系统字体）", desc: "全界面使用系统无衬线字体与清晰等宽代码字体，阅读更省力。" },
];

export const fontMeta = (id) => FONTS.find((f) => f.id === id) || FONTS[0];
export const fontOf = (p) => fontMeta(p?.settings?.font).id;
export const nextFont = (id) => FONTS[(FONTS.findIndex((f) => f.id === id) + 1) % FONTS.length];
