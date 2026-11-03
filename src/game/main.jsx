// Entry: mounts the app. Bundled by scripts/build-web.mjs into output/web/app.js.
import { render } from "preact";
import { App } from "./ui/App.jsx";
import { initNative } from "./app/native.js";

initNative();

const root = document.getElementById("app");
root.textContent = ""; // drop the no-JS placeholder; Preact does not remove nodes it did not create
render(<App />, root);
