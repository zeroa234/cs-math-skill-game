// Words that must not appear in anything published (the public repository and the APK): they point at
// where the mentor sprites came from. The list sits in assets/cast/not-public.txt, which is never
// published itself. Returns a case-insensitive RegExp, or null where that folder is absent (a clone of
// the public repository, which has no characters to protect).
import fs from "node:fs";
import path from "node:path";

export function notPublic(root) {
  const file = path.join(root, "assets/cast/not-public.txt");
  if (!fs.existsSync(file)) return null;
  const words = fs.readFileSync(file, "utf8").split(/\r?\n/).map((l) => l.trim()).filter((l) => l && !l.startsWith("#"));
  return new RegExp(words.map((w) => w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).join("|"), "i");
}
