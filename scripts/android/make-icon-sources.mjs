// Draws the app icon and splash sources for `@capacitor/assets` into assets/app-icon/: the game's pixel
// lightbulb (pixelarticons, MIT) in gold on the dark theme's night blue, scaled by whole pixels so the
// pixel grid stays crisp. Run from the project root: node scripts/android/make-icon-sources.mjs
import fs from "node:fs";
import path from "node:path";
import { ROOT, launchEdge } from "../lib/edge.mjs";

const OUT = path.join(ROOT, "assets/app-icon");
fs.mkdirSync(OUT, { recursive: true });

const BG = "#14142b"; // --bg in the dark theme
const GOLD = "#f2b82e"; // a step lighter than --gold (#e0a210) so it reads on the dark blue
const GLOW = "#fff0b3"; // the lit inside of the bulb (the glyph itself is only an outline)
const INSIDE = "M9 6h6v2H9zM7 8h10v6H7zm2 6h6v2H9z";
const bulb = fs.readFileSync(path.join(ROOT, "node_modules/pixelarticons/svg/lightbulb.svg"), "utf8").match(/<path d="([^"]+)"/)[1];

// One square image: `cell` px per icon pixel, glyph centred; the glyph is 24×24 icon pixels.
function svg(size, cell, bg) {
  const off = (size - 24 * cell) / 2;
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" shape-rendering="crispEdges">` +
    (bg ? `<rect width="${size}" height="${size}" fill="${bg}"/>` : "") +
    `<g transform="translate(${off} ${off}) scale(${cell})"><path d="${INSIDE}" fill="${GLOW}"/><path d="${bulb}" fill="${GOLD}"/></g></svg>`;
}

// @capacitor/assets insets the adaptive foreground by 16.7 % per side, so this image becomes the visible
// 72 dp area, which launchers usually crop to a circle: the glyph's outermost pixels (the corner rays,
// 14.9 icon pixels from the centre) must stay inside radius 512, so 30 px per icon pixel (447 px).
const jobs = [
  ["icon-only.png", 1024, svg(1024, 32, BG)],
  ["icon-foreground.png", 1024, svg(1024, 30, null)],
  ["icon-background.png", 1024, `<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024"><rect width="1024" height="1024" fill="${BG}"/></svg>`],
  ["splash.png", 2732, svg(2732, 24, BG)],
  ["splash-dark.png", 2732, svg(2732, 24, BG)],
];

const browser = await launchEdge();
for (const [name, size, markup] of jobs) {
  const page = await browser.newPage({ viewport: { width: size, height: size }, deviceScaleFactor: 1 });
  await page.setContent(`<html><body style="margin:0;background:transparent">${markup}</body></html>`);
  await page.locator("svg").screenshot({ path: path.join(OUT, name), omitBackground: true });
  await page.close();
}
await browser.close();
console.log("wrote", jobs.map((j) => j[0]).join(", "), "to assets/app-icon/");
