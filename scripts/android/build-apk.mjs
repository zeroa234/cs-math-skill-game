// Builds the Android app: web build -> `cap sync` (copies output/web into src/android) -> Gradle release
// build signed with config/android/ -> output/apk/点亮之路-<versionName>.apk. See docs/android.md.
// Tool locations default to this machine's D: drive installs and can be overridden by the usual env vars.
// usage: node scripts/android/build-apk.mjs [--skip-web]
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { notPublic } from "../lib/not-public.mjs";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const tmp = path.join(ROOT, "temp/android-tmp");
fs.mkdirSync(tmp, { recursive: true });
const env = {
  ...process.env,
  JAVA_HOME: process.env.JAVA_HOME || "D:/java/jdk-21.0.12.1+1",
  ANDROID_HOME: process.env.ANDROID_HOME || "D:/tools/android-sdk",
  // Gradle's caches and Android's per-user files default to C:\Users\…; keep them on D:.
  GRADLE_USER_HOME: process.env.GRADLE_USER_HOME || "D:/tools/gradle-home",
  ANDROID_USER_HOME: process.env.ANDROID_USER_HOME || "D:/tools/android-user-home",
  TEMP: tmp,
  TMP: tmp,
};
for (const k of ["JAVA_HOME", "ANDROID_HOME"]) if (!fs.existsSync(env[k])) throw new Error(`${k} not found: ${env[k]}`);
if (!fs.existsSync(path.join(ROOT, "config/android/keystore.properties"))) throw new Error("config/android/keystore.properties missing: the release build would be unsigned (docs/android.md)");

const run = (cmd, args, cwd = ROOT) => execFileSync(cmd, args, { cwd, env, stdio: "inherit", shell: process.platform === "win32" });
if (!process.argv.includes("--skip-web")) run("npm", ["run", "build"]);
// The APK is public too (GitHub releases): the words the public repository must not contain must not
// be in the web files it packs either.
const re = notPublic(ROOT);
if (re) {
  const web = path.join(ROOT, "output/web");
  const hits = fs.readdirSync(web, { recursive: true }).filter((f) => /\.(js|css|html|json)$/.test(f) && re.test(fs.readFileSync(path.join(web, f), "utf8")));
  if (hits.length) throw new Error(`output/web mentions a not-public word (assets/cast/not-public.txt): ${hits.join(", ")}`);
}
run("npx", ["cap", "sync", "android"]);
const androidDir = path.join(ROOT, "src/android");
run(path.join(androidDir, process.platform === "win32" ? "gradlew.bat" : "gradlew"), ["assembleRelease", "--console=plain"], androidDir);

const versionName = JSON.parse(fs.readFileSync(path.join(ROOT, "package.json"), "utf8")).version; // build.gradle reads it too
const built = path.join(androidDir, "app/build/outputs/apk/release/app-release.apk");
const out = path.join(ROOT, "output/apk", `点亮之路-${versionName}.apk`);
fs.mkdirSync(path.dirname(out), { recursive: true });
fs.copyFileSync(built, out);
console.log(`${path.relative(ROOT, out)}  ${(fs.statSync(out).size / 1048576).toFixed(1)} MB`);
