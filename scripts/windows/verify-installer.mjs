// Unpacks a Windows installer built by build-installer.mjs and compares the game inside, file by file,
// with a game folder (the published one, temp/publish/repo/output/web). Used by build-installer.mjs and
// release-github.mjs, so an installer that packs another build is never released.
// The NSIS installer holds $PLUGINSDIR/app-64.7z, which holds resources/app.asar, which holds game/.
// 7-Zip is the one electron-builder downloaded into its cache; asar is electron-builder's @electron/asar.
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { pathToFileURL, fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
export const STAGE = path.join(ROOT, "temp/windows-package");

function sevenZip() {
  const cache = path.join(STAGE, "builder-cache");
  const hit = fs.existsSync(cache) && fs.readdirSync(cache, { recursive: true }).find((f) => /(^|[\\/])bin[\\/]7za\.exe$/.test(f));
  if (!hit) throw new Error("7-Zip not found in temp/windows-package/builder-cache: run node scripts/windows/build-installer.mjs once");
  return path.join(cache, hit);
}

export async function verifyInstaller(exe, web) {
  const out = path.join(STAGE, "installer-check");
  fs.rmSync(out, { recursive: true, force: true });
  const z = sevenZip();
  // 7-Zip exit code 1 is a warning: the standalone 7za opens the installer as the 7z archive inside it
  // and warns about the data after it (it does not read the NSIS wrapper, so there is no $PLUGINSDIR).
  const x = (archive, dest) => { try { execFileSync(z, ["x", archive, `-o${dest}`, "-y"], { stdio: "ignore" }); } catch (e) { if (e.status !== 1) throw e; } };
  x(exe, out);
  let app = out;
  if (!fs.existsSync(path.join(out, "resources/app.asar"))) { app = path.join(out, "app"); x(path.join(out, "$PLUGINSDIR", "app-64.7z"), app); }
  const asar = await import(pathToFileURL(path.join(STAGE, "node_modules/@electron/asar/lib/asar.js")).href);
  const unpacked = path.join(out, "asar");
  (asar.extractAll || asar.default.extractAll)(path.join(app, "resources/app.asar"), unpacked);
  const files = fs.readdirSync(web, { recursive: true }).filter((f) => fs.statSync(path.join(web, f)).isFile());
  const differ = files.filter((f) => { const p = path.join(unpacked, "game", f); return !fs.existsSync(p) || !fs.readFileSync(p).equals(fs.readFileSync(path.join(web, f))); });
  if (differ.length) throw new Error(`${path.basename(exe)} does not pack the published game: ${differ.slice(0, 5).join(", ")}${differ.length > 5 ? ", …" : ""}. Rebuild it: node scripts/windows/build-installer.mjs`);
  return files.length;
}
