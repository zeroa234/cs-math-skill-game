// Creates the GitHub release v<version> for the version in package.json, after the source snapshot
// is pushed (scripts/publish-github.mjs --push), and attaches the APK. The in-app update check reads
// this release (src/game/app/update.js). See docs/android.md "发新版本".
//  - notes: docs/releases/<version>.md; APK: output/apk/点亮之路-<version>.apk; PC version: the game
//    publish-github.mjs built from HEAD (temp/publish/repo/output/web), zipped
//  - the APK must pack that same game, file for file (so it was built from the same commit, with
//    nothing uncommitted), or nothing is released
//  - the asset is uploaded as cs-math-skill-game-<version>.apk (GitHub renames non-ASCII file names)
//    with the Chinese name as its label
//  - Chinese text goes to gh as UTF-8 JSON on stdin (gh's arguments get re-encoded on Windows), and
//    the release is read back and compared; the asset's sha256 digest must equal the local file's
// usage: node scripts/release-github.mjs          (self-written glue around gh)
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const REPO = "zeroa234/cs-math-skill-game";
const version = JSON.parse(fs.readFileSync(path.join(ROOT, "package.json"), "utf8")).version;
const tag = `v${version}`;
const apk = path.join(ROOT, "output/apk", `点亮之路-${version}.apk`);
const notes = path.join(ROOT, "docs/releases", `${version}.md`);
for (const f of [apk, notes]) if (!fs.existsSync(f)) throw new Error(`missing ${path.relative(ROOT, f)}`);

const gh = (args, input) => execFileSync("gh", ["api", ...args], { input, encoding: "utf8", stdio: ["pipe", "pipe", "inherit"], maxBuffer: 1 << 26 });
const json = (args, body) => JSON.parse(gh(args, body === undefined ? undefined : Buffer.from(JSON.stringify(body), "utf8")) || "null");
const tryJson = (args) => { try { return json(args); } catch { return null; } };

// the public main must be this version's snapshot (publish-github.mjs commits as "v<version>")
const head = json([`repos/${REPO}/commits/main`]);
if (!head.commit.message.startsWith(tag)) throw new Error(`public main is "${head.commit.message.split("\n")[0]}", not ${tag}: run scripts/publish-github.mjs --push first`);

// The published game (the snapshot that is the public main), and the same game inside the APK
// (Capacitor puts it under assets/public/, next to a few files of its own, which are not compared).
const TAR = process.platform === "win32" ? "C:/Windows/System32/tar.exe" : "bsdtar"; // reads and writes zip
const snapshot = path.join(ROOT, "temp/publish/repo"), web = path.join(snapshot, "output/web");
if (!fs.existsSync(path.join(snapshot, ".git")) || execFileSync("git", ["-C", snapshot, "rev-parse", "HEAD"], { encoding: "utf8" }).trim() !== head.sha) throw new Error("temp/publish/repo is not the public main: run scripts/publish-github.mjs --push first");
const stage = path.join(ROOT, "temp/release");
fs.rmSync(stage, { recursive: true, force: true });
fs.mkdirSync(path.join(stage, "apk"), { recursive: true });
execFileSync(TAR, ["-x", "-f", apk, "-C", path.join(stage, "apk"), "assets/public"]);
const differ = fs.readdirSync(web, { recursive: true }).filter((f) => fs.statSync(path.join(web, f)).isFile())
  .filter((f) => { const inApk = path.join(stage, "apk/assets/public", f); return !fs.existsSync(inApk) || !fs.readFileSync(inApk).equals(fs.readFileSync(path.join(web, f))); });
if (differ.length) throw new Error(`the APK does not pack the published game (built from another commit, or with uncommitted changes?): ${differ.slice(0, 5).join(", ")}${differ.length > 5 ? ", …" : ""}. Rebuild it from the committed workspace: node scripts/android/build-apk.mjs`);

// The PC version: the published game alone, in one folder, zipped. Unzip and double-click index.html.
const folder = `cs-math-skill-game-${version}`;
fs.cpSync(web, path.join(stage, folder), { recursive: true });
const zip = path.join(stage, `${folder}-web.zip`);
execFileSync(TAR, ["-a", "-c", "-f", zip, "-C", stage, folder]); // -a: zip, from the file name

const want = { tag_name: tag, target_commitish: head.sha, name: `点亮之路 ${version}`, body: fs.readFileSync(notes, "utf8").trim(), draft: false, prerelease: false };
const old = tryJson([`repos/${REPO}/releases/tags/${tag}`]);
const rel = old ? json(["-X", "PATCH", `repos/${REPO}/releases/${old.id}`, "--input", "-"], { name: want.name, body: want.body }) : json(["-X", "POST", `repos/${REPO}/releases`, "--input", "-"], want);
if (rel.name !== want.name || rel.body.replace(/\r\n/g, "\n") !== want.body.replace(/\r\n/g, "\n")) throw new Error("the release's name or notes came back different (encoding?)");

console.log(rel.html_url);
for (const [file, name, label, type] of [
  [apk, `cs-math-skill-game-${version}.apk`, `点亮之路 ${version}（安卓）`, "application/vnd.android.package-archive"],
  [zip, `cs-math-skill-game-${version}-web.zip`, `点亮之路 ${version}（电脑版：解压后双击 index.html）`, "application/zip"],
]) {
  for (const a of rel.assets || []) if (a.name === name) gh(["-X", "DELETE", `repos/${REPO}/releases/assets/${a.id}`]);
  const asset = json(["-X", "POST", "-H", `Content-Type: ${type}`, `https://uploads.github.com/repos/${REPO}/releases/${rel.id}/assets?name=${name}&label=${encodeURIComponent(label)}`, "--input", file]);
  const sha = crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
  if (asset.digest && asset.digest !== `sha256:${sha}`) throw new Error(`${name}: uploaded ${asset.digest}, local sha256:${sha}`);
  console.log(`  ${asset.name} (${asset.label}) ${(asset.size / 1048576).toFixed(1)} MB, sha256 ${asset.digest ? "matches" : "not reported by GitHub"}: ${sha}`);
}
