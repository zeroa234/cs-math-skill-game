// Publishes this project to github.com/zeroa234/cs-math-skill-game as a snapshot, mentors included.
// The workspace history holds files that were never meant to be public (the replaced mentors, notes on
// where the sprites were rendered), so the public history is one commit per publish instead of a
// split of the workspace history.
//  1. exports the files committed at HEAD into temp/publish/repo (a clone of the public repository)
//  2. drops EXCLUDE (the word list itself; the extraction script, which names its source folders) and
//     builds output/web again
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
const EXCLUDE = ["assets/cast/not-public.txt", "scripts/cast/extract-sprites.py", "output/web"];
// Words that point at where the sprites came from (the list is in assets/cast/, never published).
const FORBIDDEN = notPublic(ROOT);
if (!FORBIDDEN) throw new Error("assets/cast/not-public.txt missing: publish from the author's workspace");
const DIR = path.join(ROOT, "temp/publish/repo");
const TAR_EXE = process.platform === "win32" ? "C:/Windows/System32/tar.exe" : "tar";

const run = (cmd, args, opts = {}) => execFileSync(cmd, args, { encoding: "utf8", stdio: ["ignore", "pipe", "inherit"], ...opts }).trim();
const git = (...args) => run("git", ["-C", DIR, ...args]);
const top = run("git", ["-C", ROOT, "rev-parse", "--show-toplevel"]);
const prefix = path.relative(top, ROOT).replace(/\\/g, "/");
const head = run("git", ["-C", ROOT, "rev-parse", "--short", "HEAD"]);
const version = JSON.parse(fs.readFileSync(path.join(ROOT, "package.json"), "utf8")).version;
if (run("git", ["-C", ROOT, "status", "--porcelain", "--untracked-files=no", "."])) console.warn("note: uncommitted changes are not published (HEAD only)");

// 1. a working copy of the public repository, emptied
if (!fs.existsSync(path.join(DIR, ".git"))) {
  fs.mkdirSync(path.dirname(DIR), { recursive: true });
  try { run("git", ["clone", "-q", REMOTE, DIR]); } catch { fs.mkdirSync(DIR, { recursive: true }); git("init", "-q", "-b", "main"); git("remote", "add", "origin", REMOTE); }
}
try { git("pull", "-q", "--ff-only", "origin", "main"); } catch { /* empty remote */ }
for (const e of fs.readdirSync(DIR)) if (e !== ".git") fs.rmSync(path.join(DIR, e), { recursive: true, force: true });
const tar = path.join(path.dirname(DIR), "snapshot.tar");
run("git", ["-C", top, "archive", "--format=tar", "-o", tar, `HEAD:${prefix}`]);
run(TAR_EXE, ["-xf", tar, "-C", DIR]);
fs.rmSync(tar);

// 2. drop what stays private, build the game
for (const p of EXCLUDE) fs.rmSync(path.join(DIR, p), { recursive: true, force: true });
run("node", ["scripts/build-data.mjs"], { cwd: ROOT });
run("node", ["scripts/build-web.mjs"], { cwd: ROOT, env: { ...process.env, WEB_OUT: path.join(DIR, "output/web") } });

// 3. checks, then one commit
const files = git("ls-files", "--others", "--cached", "--exclude-standard").split("\n").filter(Boolean);
const leaks = files.filter((f) => /\.(md|mjs|js|jsx|json|yaml|py|html|css)$/.test(f) && FORBIDDEN.test(fs.readFileSync(path.join(DIR, f), "utf8")));
if (leaks.length) throw new Error("these files still name where the sprites were rendered:\n" + leaks.join("\n"));
if (files.some((f) => EXCLUDE.slice(0, 2).includes(f))) throw new Error("a private file is in the snapshot");
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
git("add", "-A");
if (!git("status", "--porcelain")) { console.log("nothing new to publish"); process.exit(0); }
const env = { ...process.env, GIT_AUTHOR_NAME: ID.name, GIT_AUTHOR_EMAIL: ID.email, GIT_COMMITTER_NAME: ID.name, GIT_COMMITTER_EMAIL: ID.email };
run("git", ["-C", DIR, "commit", "-q", "-m", `v${version}`, "-m", `Snapshot of the author's workspace at ${head}.`], { env });
console.log(`${DIR}: commit ${git("rev-parse", "--short", "HEAD")} (v${version}), ${files.length} files`);
if (process.argv.includes("--push")) { git("push", "-u", "origin", "main"); console.log("pushed to", REMOTE); }
