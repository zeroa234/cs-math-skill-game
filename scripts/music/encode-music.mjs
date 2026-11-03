// Builds assets/music/<track>.ogg from data/music.yaml. Each pack is downloaded once into
// temp/music-src/<pack>/ (zips unpacked there). Every track is measured (EBU R128 loudness and true
// peak, ffmpeg's ebur128 filter) and given one fixed gain so all of them sit at the same level; a
// plain gain keeps the seamless loops seamless, where a dynamic normaliser would not. Then Opus
// 64 kbit/s, which every Chromium (Android WebView, Edge, Chrome) and Firefox plays.
// Needs ffmpeg on PATH. usage: node scripts/music/encode-music.mjs [--force]   (self-written glue)
import fs from "node:fs";
import path from "node:path";
import { execFileSync, spawnSync } from "node:child_process";
import * as yaml from "js-yaml";
import { ROOT } from "../lib/edge.mjs";

const SRC = path.join(ROOT, "temp/music-src");
const OUT = path.join(ROOT, "assets/music");
const TARGET_LUFS = -18; // a little under typical game music, so the sound effects stay on top
const MAX_TRUE_PEAK = -1; // dBTP
const force = process.argv.includes("--force");
const doc = yaml.load(fs.readFileSync(path.join(ROOT, "data/music.yaml"), "utf8"));

async function packDir(id) {
  const dir = path.join(SRC, id);
  if (fs.existsSync(dir) && fs.readdirSync(dir).length) return dir;
  const { url } = doc.packs[id];
  const name = decodeURIComponent(path.basename(new URL(url).pathname));
  console.log("downloading", name);
  const res = await fetch(url);
  if (!res.ok) throw new Error(`${url}: HTTP ${res.status}`);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, name), Buffer.from(await res.arrayBuffer()));
  // Windows' own tar (bsdtar) reads zips; Git Bash's GNU tar earlier on PATH does not.
  if (name.endsWith(".zip")) execFileSync(process.platform === "win32" ? "C:/Windows/System32/tar.exe" : "unzip", process.platform === "win32" ? ["-xf", name] : ["-o", name], { cwd: dir });
  return dir;
}

function loudness(file) {
  const r = spawnSync("ffmpeg", ["-hide_banner", "-nostats", "-i", file, "-af", "ebur128=peak=true", "-f", "null", "-"], { encoding: "utf8" });
  const log = r.stderr;
  const last = (re) => { const all = [...log.matchAll(re)]; return all.length ? Number(all.at(-1)[1]) : NaN; };
  return { lufs: last(/I:\s+(-?[\d.]+) LUFS/g), peak: last(/Peak:\s+(-?[\d.]+) dBFS/g) };
}

fs.mkdirSync(OUT, { recursive: true });
for (const [id, t] of Object.entries(doc.tracks)) {
  const out = path.join(OUT, `${id}.ogg`);
  if (fs.existsSync(out) && !force) continue;
  const dir = await packDir(t.pack);
  const file = t.file ? path.join(dir, t.file) : path.join(dir, decodeURIComponent(path.basename(new URL(doc.packs[t.pack].url).pathname)));
  const { lufs, peak } = loudness(file);
  const gain = Math.min(TARGET_LUFS - lufs, MAX_TRUE_PEAK - peak);
  execFileSync("ffmpeg", ["-hide_banner", "-loglevel", "error", "-y", "-i", file, "-af", `volume=${gain.toFixed(2)}dB`, "-c:a", "libopus", "-b:a", "64k", "-vbr", "on", "-ar", "48000", "-ac", "2", "-map_metadata", "-1", out]);
  console.log(`${id.padEnd(28)} ${lufs.toFixed(1)} LUFS, peak ${peak.toFixed(1)} dBTP → gain ${gain.toFixed(1)} dB, ${(fs.statSync(out).size / 1024).toFixed(0)} KB`);
}
