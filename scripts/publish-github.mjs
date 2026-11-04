// Publishes this project to github.com/zeroa234/cs-math-skill-game as a snapshot, mentors included.
// The workspace history holds files that were never meant to be public (the replaced mentors, notes on
// where the sprites were rendered), so the public history is one commit per publish instead of a
// split of the workspace history.
//  1. exports the files committed at HEAD into temp/publish/repo (a clone of the public repository),
//     and the skill tree's data at HEAD (../cs-math-skill-tree/output) into temp/publish/tree
//  2. drops EXCLUDE (the word list itself; the extraction script, which names its source folders) and
//     builds output/web inside the snapshot, with the snapshot's own scripts: the published game is
//     built from HEAD alone, never from uncommitted or untracked files in the workspace
//  3. refuses if any text still names where the sprites were rendered, or if the built game does not
//     load its mentors; commits as the author's GitHub identity (no AI attribution). --push pushes main.
// usage: node scripts/publish-github.mjs [--push]          (self-written glue)
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { pathToFileURL } from "node:url";
import { ROOT, launchEdge } from "./lib/edge.mjs";
import { notPublic } from "./lib/not-public.mjs";

const REMOTE = "https://github.com/zeroa234/cs-math-skill-game.git";
const ID = { name: "zeroa234", email: "208007470+zeroa234@users.noreply.github.com" }; // as on zeroa234/cs-math-skill-tree
const EXCLUDE = ["assets/cast/not-public.txt", "scripts/cast/extract-sprites.py", "output/web", "output/apk", "output/windows"];
// Words that point at where the sprites came from (the list is in assets/cast/, never published).
const FORBIDDEN = notPublic(ROOT);
if (!FORBIDDEN) throw new Error("assets/cast/not-public.txt missing: publish from the author's workspace");
const DIR = path.join(ROOT, "temp/publish/repo");
const TAR_EXE = process.platform === "win32" ? "C:/Windows/System32/tar.exe" : "tar";

const run = (cmd, args, opts = {}) => execFileSync(cmd, args, { encoding: "utf8", stdio: ["ignore", "pipe", "inherit"], ...opts }).trim();
const git = (...args) => run("git", ["-C", DIR, "-c", "core.autocrlf=false", ...args]);
const top = run("git", ["-C", ROOT, "rev-parse", "--show-toplevel"]);
const prefix = path.relative(top, ROOT).replace(/\\/g, "/");
const head = run("git", ["-C", ROOT, "rev-parse", "--short", "HEAD"]);
const version = JSON.parse(fs.readFileSync(path.join(ROOT, "package.json"), "utf8")).version;
if (run("git", ["-C", ROOT, "status", "--porcelain", "--untracked-files=no", "."])) console.warn("note: uncommitted changes are not published (HEAD only, the built game too)");

// 1. a working copy of the public repository, emptied
if (!fs.existsSync(path.join(DIR, ".git"))) {
  fs.mkdirSync(path.dirname(DIR), { recursive: true });
  try { run("git", ["clone", "-q", REMOTE, DIR]); } catch { fs.mkdirSync(DIR, { recursive: true }); git("init", "-q", "-b", "main"); git("remote", "add", "origin", REMOTE); }
}
try { git("pull", "-q", "--ff-only", "origin", "main"); } catch { /* empty remote */ }
for (const e of fs.readdirSync(DIR)) if (e !== ".git") fs.rmSync(path.join(DIR, e), { recursive: true, force: true });
const tar = path.join(path.dirname(DIR), "snapshot.tar");
run("git", ["-C", top, "-c", "core.autocrlf=false", "archive", "--format=tar", "-o", tar, `HEAD:${prefix}`]);
run(TAR_EXE, ["-xf", tar, "-C", DIR]);
const TREE = path.join(path.dirname(DIR), "tree");
fs.rmSync(TREE, { recursive: true, force: true });
fs.mkdirSync(TREE);
run("git", ["-C", top, "-c", "core.autocrlf=false", "archive", "--format=tar", "-o", tar, `HEAD:${path.posix.join(path.posix.dirname(prefix), "cs-math-skill-tree")}`, "output/skilltree.json", "output/outlines.json"]);
run(TAR_EXE, ["-xf", tar, "-C", TREE]);
fs.rmSync(tar);

// 2. drop what stays private, build the game in the snapshot (node_modules: this project's, found
//    by walking up from temp/publish/repo, as for any import)
for (const p of EXCLUDE) fs.rmSync(path.join(DIR, p), { recursive: true, force: true });
run("node", ["scripts/build-data.mjs", "--tree", TREE], { cwd: DIR });
run("node", ["scripts/build-web.mjs"], { cwd: DIR, env: { ...process.env, WEB_OUT: "", CAST: "" } });

// 3. checks, then one commit
git("add", "-A");
const files = git("ls-files", "-z").split("\0").filter(Boolean);
if (files.some((f) => EXCLUDE.slice(0, 2).includes(f) || f.startsWith("config/android/"))) {
  throw new Error("a private file is in the snapshot");
}
const leakCount = files.filter((f) => {
  if (FORBIDDEN.test(f)) return true;
  const contents = fs.readFileSync(path.join(DIR, f), "utf8");
  // Compressed media can contain coincidental byte sequences; check actual text files.
  return !contents.includes("\uFFFD") && !contents.includes("\0") && FORBIDDEN.test(contents);
}).length;
if (leakCount) throw new Error(`the snapshot contains ${leakCount} files with private terms`);
// The built game must show its mentors: the intro's two portraits load and nothing fails to load.
{
  const browser = await launchEdge();
  const p = await browser.newPage();
  const failed = [];
  p.on("requestfailed", (r) => failed.push(r.url()));
  p.on("pageerror", (e) => failed.push(String(e)));
  await p.goto(pathToFileURL(path.join(DIR, "output/web/index.html")).href);
  await p.click(".intro .title-card .btn");
  await p.waitForTimeout(1500);
  const shown = await p.$$eval(".intro img.portrait", (imgs) => imgs.filter((i) => i.complete && i.naturalWidth > 0).length);
  await browser.close();
  if (shown !== 2 || failed.length) throw new Error(`the published game does not show its mentors (portraits shown: ${shown}; failed: ${failed.join(", ")})`);
}
if (git("status", "--porcelain")) {
  const env = { ...process.env, GIT_AUTHOR_NAME: ID.name, GIT_AUTHOR_EMAIL: ID.email, GIT_COMMITTER_NAME: ID.name, GIT_COMMITTER_EMAIL: ID.email };
  run("git", ["-C", DIR, "commit", "-q", "-m", `v${version}`, "-m", `Snapshot of the author's workspace at ${head}.`], { env });
}
console.log(`${DIR}: commit ${git("rev-parse", "--short", "HEAD")} (v${version}), ${files.length} files checked`);
if (process.argv.includes("--push")) { git("push", "-u", "origin", "main"); console.log("pushed to", REMOTE); }
