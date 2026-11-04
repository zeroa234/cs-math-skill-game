// Windows desktop app (Electron): shows the game from the folder `game/` packed next to this file.
// Files are served through a private skill-game:// scheme (secure, so the game's storage and fetch work
// as on the web); anything outside `game/` is refused. Links to textbooks and courses open in the
// system browser. Saves live in %APPDATA%\cs-math-skill-game. --user-data-dir and --headless are for
// smoke tests. Built by scripts/windows/build-installer.mjs (docs/android.md, "Windows 安装版").
const { app, BrowserWindow, net, protocol, shell } = require("electron");
const path = require("node:path");
const { pathToFileURL } = require("node:url");

const home = "skill-game://local/index.html";
const web = path.join(__dirname, "game");
const testProfile = app.commandLine.getSwitchValue("user-data-dir");
app.setPath("userData", testProfile || path.join(app.getPath("appData"), "cs-math-skill-game"));
app.setAppUserModelId("local.csmathskillgame.desktop");

protocol.registerSchemesAsPrivileged([
  { scheme: "skill-game", privileges: { standard: true, secure: true, supportFetchAPI: true, stream: true } },
]);

function openReference(url) {
  if (/^https?:\/\//i.test(url)) void shell.openExternal(url).catch(console.error);
}

app.whenReady().then(() => {
  protocol.handle("skill-game", (request) => {
    const url = new URL(request.url);
    let pathname;
    try { pathname = decodeURIComponent(url.pathname); } catch { return new Response(null, { status: 400 }); }
    const file = path.resolve(web, "." + pathname);
    const relative = path.relative(web, file);
    if (url.host !== "local" || /[\\:\0]/.test(pathname) || !relative ||
        relative === ".." || relative.startsWith(".." + path.sep) || path.isAbsolute(relative)) {
      return new Response(null, { status: 404 });
    }
    return net.fetch(pathToFileURL(file).href, { headers: request.headers });
  });

  const win = new BrowserWindow({
    width: 1280,
    height: 850,
    autoHideMenuBar: true,
    show: !app.commandLine.hasSwitch("headless"),
    webPreferences: { sandbox: true, contextIsolation: true, nodeIntegration: false },
  });
  win.webContents.setWindowOpenHandler(({ url }) => {
    openReference(url);
    return { action: "deny" };
  });
  win.webContents.on("will-navigate", (event, url) => {
    if (new URL(url).protocol === "skill-game:") return;
    event.preventDefault();
    openReference(url);
  });
  void win.loadURL(home);
});

app.on("window-all-closed", () => app.quit());
