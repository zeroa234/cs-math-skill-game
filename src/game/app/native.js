// Android app (Capacitor) glue. In a browser, including file://, NATIVE is false and nothing here runs.
// See docs/android.md.
import { Capacitor } from "@capacitor/core";
import { App } from "@capacitor/app";
import { setAppBackground } from "./music.js";
import { checkInBackground } from "./update.js";

export const NATIVE = Capacitor.isNativePlatform();

// The phone's back button goes back one screen (every screen is a #/ address in the history) and
// leaves the app only from the first screen, like a browser tab would.
export function initNative() {
  if (!NATIVE) return;
  App.addListener("backButton", ({ canGoBack }) => (canGoBack ? history.back() : App.exitApp()));
  // Music stops while the app is in the background (home button, a call, another app).
  App.addListener("appStateChange", ({ isActive }) => setAppBackground(!isActive));
  // Once a day: is there a newer release? Shows a banner on the camp (src/game/app/update.js).
  checkInBackground();
  // No page zoom inside the app (MainActivity.java also turns WebView zoom off): a pinch otherwise
  // blows the whole UI up. The browser version stays zoomable for people who need larger text.
  document.querySelector('meta[name="viewport"]')?.setAttribute("content", "width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no");
}
