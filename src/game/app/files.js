// Handing the player a text file (a save): a download in the browser; in the Android app, whose
// WebView ignores <a download>, the file goes to the app cache and the share sheet opens.
import { Filesystem, Directory, Encoding } from "@capacitor/filesystem";
import { Share } from "@capacitor/share";
import { NATIVE } from "./native.js";

// Resolves when handed over; a share sheet the player closes is not an error.
export async function saveTextFile(name, text) {
  if (NATIVE) {
    try {
      const { uri } = await Filesystem.writeFile({ path: name, data: text, directory: Directory.Cache, encoding: Encoding.UTF8 });
      await Share.share({ title: name, files: [uri] });
    } catch (err) {
      if (!/cancel/i.test(err?.message || "")) throw err;
    }
    return;
  }
  const a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([text], { type: "application/json" }));
  a.download = name;
  a.click();
  setTimeout(() => URL.revokeObjectURL(a.href), 1000);
}

export const saveName = (what = "存档") => `计算机大学习-${what}-${new Date().toISOString().slice(0, 10)}.json`;
