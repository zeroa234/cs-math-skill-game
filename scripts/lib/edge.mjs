// The system Edge for the tests and scripts that drive a page (playwright-core, no browser download).
// Edge and Playwright write temporary files to TEMP; they go under the project's temp/, not to C:.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { chromium } from "playwright-core";

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
// The built game (npm run build), opened from disk like a player double-clicking it.
export const GAME_URL = pathToFileURL(path.join(ROOT, "output/web/index.html")).href;

const EDGE = ["C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe", "C:/Program Files/Microsoft/Edge/Application/msedge.exe"].find((p) => fs.existsSync(p));

export function launchEdge(tmp = path.join(ROOT, "temp/browser")) {
  if (!EDGE) throw new Error("Microsoft Edge not found in Program Files");
  fs.mkdirSync(tmp, { recursive: true });
  process.env.TEMP = process.env.TMP = tmp;
  return chromium.launch({ executablePath: EDGE, headless: true });
}
