// When the save is in trouble (core/progress.js health()): a save that cannot be read stops the
// game on one page until the player decides what happens to it; a save that did not reach storage
// gets a warning on every screen until one does.
import { useState } from "preact/hooks";
import { useSyncExternalStore } from "preact/compat";
import { store } from "../app/state.js";
import { href } from "../app/router.js";
import { saveTextFile, saveName } from "../app/files.js";
import { toast } from "./common.jsx";

export const useSaveHealth = () => useSyncExternalStore(store.subscribe, store.health);

export function ImportSave({ label = "导入存档", class: cls = "btn ghost" }) {
  const pick = async (e) => {
    const input = e.currentTarget;
    const f = input.files[0];
    if (!f) return;
    try { store.importJson(await f.text()); toast({ title: "存档已导入" }); } catch (err) { toast({ title: "导入失败", body: err.message }); }
    input.value = "";
  };
  return <label class={cls}>{label}<input type="file" accept="application/json,.json" hidden onChange={pick} /></label>;
}

export function UnreadableSave({ problem }) {
  const [sure, setSure] = useState(false);
  const download = () => saveTextFile(saveName("读不出的存档"), problem.raw).catch((err) => toast({ title: "下载失败", body: err?.message || String(err) }));
  return (
    <div class="page"><section class="card save-problem" role="alert">
      <h1>存档读不出来</h1>
      <p>原因：{problem.message}。</p>
      <p>原来的存档还在，没有被改动。可以先把它原样存下来；如果是新版游戏的存档，更新游戏后再导入就行。</p>
      <div class="row">
        <button type="button" class="btn primary" onClick={download}>下载原来的存档</button>
        <ImportSave label="导入另一个存档" class="btn" />
        {!sure ? <button type="button" class="btn ghost danger" onClick={() => setSure(true)}>从头开始…</button> : <>
          <span>原来的存档会被清掉。确定？</span>
          <button type="button" class="btn danger" onClick={() => store.replace({ v: 1 })}>清掉，从头开始</button>
          <button type="button" class="btn ghost" onClick={() => setSure(false)}>取消</button>
        </>}
      </div>
    </section></div>
  );
}

export const UnsavedWarning = () => (
  <div class="save-warning" role="alert">
    <b>进度没能存到本机</b>（存储空间可能满了，或浏览器不允许保存）。先别关掉游戏，去 <a href={href("me")}>我的 → 导出存档</a>。
  </div>
);
