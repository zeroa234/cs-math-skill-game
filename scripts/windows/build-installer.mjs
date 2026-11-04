// Builds the Windows x64 installer of the version in package.json: the game publish-github.mjs built from
// HEAD (temp/publish/repo/output/web, the same files as the release's PC zip) inside an Electron app
// (main.cjs here), as a one-click NSIS installer made by electron-builder (electron-builder.json here).
// Electron 45.2.2 and electron-builder 26.18.0 are pinned by package-lock.json here and installed into
// temp/windows-package (npm ci the first time); Electron, NSIS and 7-Zip downloads are cached there too,
// never on C:. Afterwards the installer is unpacked again and its game compared file by file with the
// published one (verify-installer.mjs), and the unpacked app is started once, headless, to see the
// game's first screen. See docs/android.md, "Windows 安装版".
// usage: node scripts/windows/build-installer.mjs     → output/windows/cs-math-skill-game-<version>-windows-x64-setup.exe
// (self-written glue around npm and electron-builder)
import fs from "node:fs";
import path from "node:path";
import { execFileSync, spawn } from "node:child_process";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright-core";
import { STAGE, verifyInstaller } from "./verify-installer.mjs";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "../..");
const version = JSON.parse(fs.readFileSync(path.join(ROOT, "package.json"), "utf8")).version;
const snapshot = path.join(ROOT, "temp/publish/repo");
const web = path.join(snapshot, "output/web");
if (!fs.existsSync(path.join(web, "index.html"))) throw new Error("temp/publish/repo/output/web missing: run node scripts/publish-github.mjs first");
const snapVersion = JSON.parse(fs.readFileSync(path.join(snapshot, "package.json"), "utf8")).version;
if (snapVersion !== version) throw new Error(`the published snapshot is ${snapVersion}, package.json is ${version}: run node scripts/publish-github.mjs first`);

// 1. stage: the packaging files, package.json carrying this version, and the published game as game/
fs.mkdirSync(STAGE, { recursive: true });
for (const f of ["main.cjs", "game.ico", "electron-builder.json", "package-lock.json"]) fs.copyFileSync(path.join(HERE, f), path.join(STAGE, f));
const pkg = JSON.parse(fs.readFileSync(path.join(HERE, "package.json"), "utf8"));
fs.writeFileSync(path.join(STAGE, "package.json"), JSON.stringify({ ...pkg, version }, null, 2) + "\n");
for (const d of ["game", "dist"]) fs.rmSync(path.join(STAGE, d), { recursive: true, force: true });
fs.cpSync(web, path.join(STAGE, "game"), { recursive: true });

const tmp = path.join(STAGE, "runtime-tmp");
fs.mkdirSync(tmp, { recursive: true });
const env = {
  ...process.env,
  ELECTRON_CACHE: path.join(STAGE, "builder-cache"),
  ELECTRON_BUILDER_CACHE: path.join(STAGE, "builder-cache"),
  npm_config_cache: path.join(STAGE, "npm-cache"),
  TEMP: tmp,
  TMP: tmp,
};
const run = (cmd, args) => execFileSync(cmd, args, { cwd: STAGE, env, stdio: "inherit", shell: process.platform === "win32" });

// 2. tools, then the installer
if (!fs.existsSync(path.join(STAGE, "node_modules/electron-builder"))) run("npm", ["ci", "--no-audit", "--no-fund"]);
execFileSync(process.execPath, ["--check", path.join(STAGE, "main.cjs")]);
run("npx", ["electron-builder", "--win", "--config", "electron-builder.json"]);
const name = `cs-math-skill-game-${version}-windows-x64-setup.exe`;
const exe = path.join(STAGE, "dist", name);
if (!fs.existsSync(exe)) throw new Error(`electron-builder did not write dist/${name}`);

// 3. the game inside is the published one
const n = await verifyInstaller(exe, web);
console.log(`the installer packs the published game (${n} files)`);

// 4. the unpacked app starts and shows the game's first screen (headless, its own profile, DevTools port)
const app = path.join(STAGE, "dist/win-unpacked", fs.readdirSync(path.join(STAGE, "dist/win-unpacked")).find((f) => f.endsWith(".exe") && !/uninstall/i.test(f)));
const profile = path.join(STAGE, "smoke-profile");
fs.rmSync(profile, { recursive: true, force: true });
const port = 9333;
const child = spawn(app, ["--headless", `--user-data-dir=${profile}`, `--remote-debugging-port=${port}`], { env, stdio: "ignore" });
try {
  let browser;
  for (let i = 0; i < 40 && !browser; i++) {
    try { browser = await chromium.connectOverCDP(`http://127.0.0.1:${port}`); } catch { await new Promise((r) => setTimeout(r, 500)); }
  }
  if (!browser) throw new Error("the packed app did not open its DevTools port");
  const page = browser.contexts()[0].pages()[0];
  await page.waitForSelector(".intro, .topbar", { timeout: 15000 });
  console.log(`the packed app shows the game: ${await page.title()} (${page.url()})`);
  await browser.close();
} finally {
  child.kill();
}

fs.mkdirSync(path.join(ROOT, "output/windows"), { recursive: true });
fs.copyFileSync(exe, path.join(ROOT, "output/windows", name));
console.log(`output/windows/${name}  ${(fs.statSync(exe).size / 1048576).toFixed(1)} MB`);
