// Bundles the game into output/web/ as plain files that open with a double click (file://):
// one IIFE script (no ES modules, which browsers block on file://), the stylesheet, KaTeX's CSS and
// fonts, and the lazily loaded knowledge-map outlines.
// usage: node scripts/build-web.mjs [--watch] [--toy]
// CAST=none (or no assets/cast/ at all, e.g. after replacing the characters) builds without the
// mentor characters; the game then simply shows no mentors. WEB_OUT=<dir> writes somewhere other than output/web.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";
import * as esbuild from "esbuild";
import { toyTree } from "./lib/toy-content.mjs";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const TOY = process.argv.includes("--toy");
const OUT = path.resolve(process.env.WEB_OUT || path.join(ROOT, TOY ? "output/toy/web" : "output/web"));
const VERSION = JSON.parse(fs.readFileSync(path.join(ROOT, "package.json"), "utf8")).version;
const CAST = process.env.CAST !== "none" && fs.existsSync(path.join(ROOT, "assets/cast/sprites.json"));
fs.mkdirSync(path.join(OUT, "fonts"), { recursive: true });

const options = {
  entryPoints: [path.join(ROOT, "src/game/main.jsx")],
  bundle: true,
  format: "iife",
  target: ["es2020"],
  outfile: path.join(OUT, "app.js"),
  jsx: "automatic",
  jsxImportSource: "preact",
  minify: !process.argv.includes("--dev"),
  sourcemap: process.argv.includes("--dev") ? "inline" : false,
  legalComments: "eof",
  loader: { ".json": "json", ".svg": "text" },
  define: { __APP_VERSION__: JSON.stringify(VERSION) },
  // without the characters, src/game/ui/cast.jsx gets an empty sprite list and draws nobody
  plugins: CAST ? [] : [{ name: "no-cast", setup: (b) => b.onResolve({ filter: /assets\/cast\/sprites\.json$/ }, () => ({ path: path.join(ROOT, "src/game/ui/no-cast.json") })) }],
  logLevel: "info",
};

if (TOY) options.plugins.push({
  name: "toy-content",
  setup(build) {
    build.onLoad({ filter: /[\\/]gen[\\/]tree\.json$/ }, ({ path: file }) => ({
      contents: JSON.stringify(toyTree(JSON.parse(fs.readFileSync(file, "utf8")))),
      loader: "json",
    }));
  },
});

function copyStatic() {
  for (const f of ["index.html", "style.css"]) fs.copyFileSync(path.join(ROOT, "src/web", f), path.join(OUT, f));
  const outlineFile = path.join(OUT, "outlines.js");
  if (TOY) fs.rmSync(outlineFile, { force: true });
  else fs.copyFileSync(path.join(ROOT, "src/web/outlines.js"), outlineFile);
  // resolved like an import, so a copy of the project inside it (scripts/publish-github.mjs builds
  // the published snapshot in temp/publish/repo) finds the project's node_modules too
  const katexDist = path.join(path.dirname(createRequire(import.meta.url).resolve("katex/package.json")), "dist");
  fs.copyFileSync(path.join(katexDist, "katex.min.css"), path.join(OUT, "katex.min.css"));
  for (const f of fs.readdirSync(path.join(katexDist, "fonts")).filter((f) => f.endsWith(".woff2"))) fs.copyFileSync(path.join(katexDist, "fonts", f), path.join(OUT, "fonts", f));
  // KaTeX's CSS lists woff2, woff and ttf; keep only woff2 so missing files never 404.
  const css = fs.readFileSync(path.join(OUT, "katex.min.css"), "utf8").replace(/,url\(fonts\/[^)]+\.woff\) format\("woff"\)|,url\(fonts\/[^)]+\.ttf\) format\("truetype"\)/g, "");
  fs.writeFileSync(path.join(OUT, "katex.min.css"), css);
  // Art and the pixel font: only the published folders (assets/cast/source holds the originals).
  // Emptied first, so files removed or renamed in assets/ (or the cast, with CAST=none) do not linger.
  fs.rmSync(path.join(OUT, "assets"), { recursive: true, force: true });
  for (const dir of [...(CAST ? ["cast/sprites", "cast/portraits"] : []), "bg", "fonts", "music"]) {
    const from = path.join(ROOT, "assets", dir);
    // the folders' README.md (sources, licences) are for the repository, not the game
    if (fs.existsSync(from)) fs.cpSync(from, path.join(OUT, "assets", dir), { recursive: true, filter: (f) => !f.endsWith(".md") });
  }
  // Tab icon = the app icon (scripts/android/make-icon-sources.mjs); also stops the WebView asking for /favicon.ico.
  fs.copyFileSync(path.join(ROOT, "assets/app-icon/icon-only.png"), path.join(OUT, "assets/icon.png"));
}

if (process.argv.includes("--watch")) {
  const ctx = await esbuild.context({ ...options, plugins: [...options.plugins, { name: "static", setup: (b) => b.onEnd(copyStatic) }] });
  await ctx.watch();
} else {
  await esbuild.build(options);
  copyStatic();
  const size = (f) => (fs.statSync(path.join(OUT, f)).size / 1024).toFixed(0) + " KB";
  console.log(`${path.relative(ROOT, OUT).split(path.sep).join("/")}: app.js ${size("app.js")}${TOY ? "" : ", outlines.js " + size("outlines.js")}${CAST ? "" : ", without the cast"}`);
}
