// Syncs this project to the private collaboration repository github.com/zeroa234/remote, where a cloud
// Gemini also writes lessons (how the two sides work together: docs/collaboration.md).
//  1. fetches the remote and refuses to go on while it has commits after the last "sync:" commit that have
//     not been taken into the workspace yet (it lists them; --status only lists them). Take their content
//     into the workspace and commit it first, then pass --accept <sha of the remote commit you took in>.
//  2. runs publish-github.mjs --game-only (no push) for the public snapshot of HEAD: private files dropped,
//     output/web built from HEAD; copies its files, plus the skill tree's data as vendor/cs-math-skill-tree
//     so the cloud side can build and check without the sibling project
//  3. keeps what the remote added for its own environment (Google AI Studio): the KEEP files, extra
//     package.json scripts and dependencies, extra .gitignore lines; leaves out the Pages workflow
//  4. commits "sync: workspace at <sha>" as the author's GitHub identity; --push pushes main.
// usage: node scripts/sync-remote.mjs [--status] [--accept <sha>] [--push]          (self-written glue)
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { ROOT } from "./lib/edge.mjs";
import { githubEnv } from "./lib/github-id.mjs";

const REMOTE = "https://github.com/zeroa234/remote.git";
const DIR = path.join(ROOT, "temp/remote/repo");
const SNAP = path.join(ROOT, "temp/publish/repo");
const TREE = path.join(ROOT, "temp/publish/tree");
const KEEP = ["server.mjs", "metadata.json", ".env.example", "src/App.tsx", "src/main.tsx", "src/index.css"];
const DROP = [".github/workflows/pages.yml"]; // Pages deploys the public repository, not this one
const SYNC = /^sync: workspace at /;

const arg = (name) => { const i = process.argv.indexOf(name); return i > 0 ? process.argv[i + 1] : null; };
const run = (cmd, args, opts = {}) => execFileSync(cmd, args, { encoding: "utf8", stdio: ["ignore", "pipe", "inherit"], ...opts }).trim();
const git = (...args) => run("git", ["-C", DIR, "-c", "core.autocrlf=false", ...args]);

// 1. what the remote has that the workspace has not taken in yet
if (!fs.existsSync(path.join(DIR, ".git"))) { fs.mkdirSync(path.dirname(DIR), { recursive: true }); run("git", ["clone", "-q", REMOTE, DIR]); }
git("fetch", "-q", "origin");
const log = git("log", "--format=%H%x09%an%x09%ad%x09%s", "--date=short", "origin/main").split("\n").filter(Boolean).map((l) => l.split("\t"));
const lastSync = log.findIndex(([, , , s]) => SYNC.test(s));
const pending = lastSync < 0 ? log : log.slice(0, lastSync);
const accepted = arg("--accept");
const acceptedAt = accepted ? pending.findIndex(([h]) => h.startsWith(accepted)) : -1;
if (accepted && acceptedAt < 0) throw new Error(`--accept ${accepted}: not a remote commit after the last sync`);
const unseen = acceptedAt < 0 ? pending : pending.slice(0, acceptedAt);
if (unseen.length || process.argv.includes("--status")) {
  console.log(unseen.length ? `the remote has ${unseen.length} commit(s) not taken into the workspace:` : "nothing new on the remote since the last sync");
  for (const [h, an, ad, s] of unseen) console.log(`  ${h.slice(0, 7)} ${ad} ${an}: ${s}`);
  if (unseen.length) {
    const base = lastSync < 0 ? null : log[lastSync][0];
    console.log(base ? git("diff", "--stat", base, "origin/main") : git("show", "--stat", "--format=", "origin/main"));
    console.log("take what is worth keeping into the workspace (docs/collaboration.md), commit, then rerun with --accept " + unseen[0][0].slice(0, 7));
    process.exit(process.argv.includes("--status") ? 0 : 1);
  }
  if (process.argv.includes("--status")) process.exit(0);
}

// 2. the public snapshot of HEAD
execFileSync("node", [path.join(ROOT, "scripts/publish-github.mjs"), "--game-only"], { stdio: ["ignore", "inherit", "inherit"] });
const head = run("git", ["-C", ROOT, "rev-parse", "--short", "HEAD"]);
git("checkout", "-q", "-B", "main", "origin/main");
const readRemote = (p) => { const f = path.join(DIR, p); return fs.existsSync(f) ? fs.readFileSync(f) : null; };
const kept = Object.fromEntries(KEEP.map((p) => [p, readRemote(p)]).filter(([, b]) => b));
const remotePkg = readRemote("package.json") && JSON.parse(readRemote("package.json"));
const remoteIgnore = (readRemote(".gitignore") || "").toString().split(/\r?\n/);
for (const e of fs.readdirSync(DIR)) if (e !== ".git") fs.rmSync(path.join(DIR, e), { recursive: true, force: true });
const files = run("git", ["-C", SNAP, "ls-files", "-z"]).split("\0").filter((f) => f && !DROP.includes(f));
for (const f of files) { fs.mkdirSync(path.dirname(path.join(DIR, f)), { recursive: true }); fs.copyFileSync(path.join(SNAP, f), path.join(DIR, f)); }
for (const f of ["output/skilltree.json", "output/outlines.json"]) {
  const to = path.join(DIR, "vendor/cs-math-skill-tree", f);
  fs.mkdirSync(path.dirname(to), { recursive: true });
  fs.copyFileSync(path.join(TREE, f), to);
}

// 3. the remote's own environment
for (const [p, b] of Object.entries(kept)) { fs.mkdirSync(path.dirname(path.join(DIR, p)), { recursive: true }); fs.writeFileSync(path.join(DIR, p), b); }
if (remotePkg) {
  const pkgPath = path.join(DIR, "package.json");
  const pkg = JSON.parse(fs.readFileSync(pkgPath, "utf8"));
  for (const key of ["scripts", "dependencies", "devDependencies"]) {
    for (const [k, v] of Object.entries(remotePkg[key] || {})) if (!(k in (pkg[key] || {}))) (pkg[key] ||= {})[k] = v;
  }
  fs.writeFileSync(pkgPath, JSON.stringify(pkg, null, 2) + "\n");
}
// The remote's extra ignore lines, minus any that would hide project files (its "coverage/" hid reports/coverage/).
const ignorePath = path.join(DIR, ".gitignore");
const ignore = fs.readFileSync(ignorePath, "utf8").replace(/\n?$/, "\n");
const hides = (line) => {
  fs.writeFileSync(ignorePath, line + "\n");
  try { return !!run("git", ["-C", DIR, "check-ignore", "--no-index", "--stdin"], { input: files.join("\n"), stdio: ["pipe", "pipe", "ignore"] }); } catch { return false; } // exit 1: nothing ignored
};
const extra = remoteIgnore.filter((l) => l.trim() && !l.startsWith("#") && !ignore.split("\n").includes(l) && !hides(l));
fs.writeFileSync(ignorePath, ignore + (extra.length ? "\n# the collaboration repository's own environment\n" + extra.join("\n") + "\n" : ""));

// 4. one commit, holding every file of the snapshot
git("add", "-A");
const tracked = new Set(git("ls-files", "-z").split("\0"));
const missing = files.filter((f) => !tracked.has(f));
if (missing.length) throw new Error(`${missing.length} snapshot files are not tracked in the remote, e.g. ${missing.slice(0, 3).join(", ")}`);
if (git("status", "--porcelain")) {
  const msg = ["-m", `sync: workspace at ${head}`, ...(accepted ? ["-m", `Remote commits up to ${accepted} were taken into the workspace first.`] : [])];
  run("git", ["-C", DIR, "-c", "core.autocrlf=false", "commit", "-q", ...msg], { env: githubEnv() });
}
console.log(`${DIR}: ${git("log", "-1", "--format=%h %s")}`);
console.log(git("diff", "--stat", "origin/main", "HEAD").split("\n").slice(-1)[0] || "no changes");
if (process.argv.includes("--push")) { git("push", "-q", "origin", "main"); console.log("pushed to", REMOTE); }
