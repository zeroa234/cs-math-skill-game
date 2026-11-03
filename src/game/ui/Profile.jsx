// 我的: level, achievements, stats, settings, export / import / reset.
import { useState } from "preact/hooks";
import { g, store, useProgress, stateOf } from "../app/state.js";
import { levelOf, streak } from "../core/progress.js";
import { mastery } from "../core/rules.js";
import { ACHIEVEMENTS } from "../app/actions.js";
import { STYLES, PACKS, DEFAULT_VOLUME } from "../app/music.js";
import { VERSION, RELEASES_PAGE, checkUpdate } from "../app/update.js";
import { Bar, toast } from "./common.jsx";
import { Icon } from "./icons.jsx";
import { CAST, HAS_CAST } from "./cast.jsx";
import { NATIVE } from "../app/native.js";
import { saveTextFile, saveName } from "../app/files.js";
import { ImportSave } from "./SaveProblem.jsx";

export function Profile() {
  const p = useProgress();
  const [confirmReset, setConfirmReset] = useState(false);
  const lv = levelOf(p.xp);
  const lit = Object.keys(p.skills).filter((id) => g.byId.has(id) && stateOf(p, id).status === "lit");
  const tiers = { lit: 0, solid: 0, mastered: 0 };
  for (const id of lit) tiers[mastery(p, id)]++;
  const exportFile = () => saveTextFile(saveName(), store.exportJson()).catch((err) => toast({ title: "导出失败", body: err?.message || String(err) }));
  const set = (k, v) => store.update((d) => { d.settings[k] = v; });
  return (
    <div class="page profile">
      <h1>我的</h1>
      <section class="grid2">
        <div class="card">
          <h2>学徒 Lv.{lv.level}</h2>
          <Bar value={lv.into / lv.span} label="到下一级" />
          <p class="small muted">总经验 {p.xp} · 连续 {streak(p)} 天</p>
          <ul class="stats">
            <li><b>{lit.length}</b> 个技能已点亮（熟练 {tiers.solid}，精通 {tiers.mastered}）</li>
            <li><b>{Object.values(p.lessons).filter((l) => l.done).length}</b> 课已完成</li>
            <li><b>{Object.keys(p.cards).length}</b> 道题在复习卡组里</li>
          </ul>
        </div>
        <div class="card">
          <h2>成就</h2>
          <ul class="achievements">
            {ACHIEVEMENTS.map((a) => <li class={p.achievements[a.id] ? "got" : ""}><b><Icon name="trophy" class={p.achievements[a.id] ? "got" : "not-yet"} /> {a.name}</b><span class="small">{a.desc}</span></li>)}
          </ul>
        </div>
      </section>
      <section class="card">
        <h2>设置</h2>
        <label class="select">“去哪深入”显示 <select value={p.settings.sourceLang} onChange={(e) => set("sourceLang", e.currentTarget.value)}><option value="zh">中文资料优先</option><option value="en">英文资料优先</option><option value="both">中英文都显示</option></select></label>
        <label class="check"><input type="checkbox" checked={!!p.settings.reduceMotion} onChange={(e) => set("reduceMotion", e.currentTarget.checked)} /> 减少动画（角色不动、不放彩带、开场文字直接显示）</label>
        <label class="check"><input type="checkbox" checked={p.settings.sound !== false} onChange={(e) => set("sound", e.currentTarget.checked)} /> 声音（音效和音乐一起开关；顶栏右边的喇叭按钮也能切换）</label>
        <label class="check"><input type="checkbox" checked={p.settings.music !== false} disabled={p.settings.sound === false} onChange={(e) => set("music", e.currentTarget.checked)} /> 背景音乐</label>
        <div class="music-settings">
          <label class="select">音乐风格 <select value={p.settings.musicStyle || STYLES[0].id} disabled={p.settings.sound === false || p.settings.music === false} onChange={(e) => set("musicStyle", e.currentTarget.value)}>{STYLES.map((s) => <option value={s.id}>{s.name}</option>)}</select></label>
          <span class="small muted">{(STYLES.find((s) => s.id === p.settings.musicStyle) || STYLES[0]).desc}</span>
          <label class="select">音乐音量 <input type="range" min="0" max="100" step="5" value={Math.round((p.settings.musicVolume ?? DEFAULT_VOLUME) * 100)} disabled={p.settings.sound === false || p.settings.music === false} onInput={(e) => set("musicVolume", Number(e.currentTarget.value) / 100)} /></label>
        </div>
        <details class="credits small">
          <summary>音乐来源</summary>
          <p class="muted">全部是 CC0（公有领域）的作品，可以自由使用，这里仍然列出作者以示感谢。开场、营地和路线、上课和复习、结业挑战各放不同的曲子。</p>
          <ul>{PACKS.map((k) => <li><a href={k.page} target="_blank" rel="noopener">{k.name}</a> · {k.author} · {k.license}</li>)}</ul>
        </details>
        {HAS_CAST && <details class="credits small">
          <summary>角色来源</summary>
          <p class="muted">两位导师{CAST.blue.name}和{CAST.black.name}是鲸鱼娘，角色设计作者 ZipZipPipe，采用 <a href="https://creativecommons.org/licenses/by-nc/4.0/" target="_blank" rel="noopener">CC BY-NC 4.0</a>（署名-非商业性使用）。游戏里的改动：姐姐的立绘去掉了背景；妹妹是在原设计上衍生的黑色女仆版；两人的像素小人是照设定重做的方块小人，眼睛放大了一些，长裙改成了短裙。</p>
        </details>}
      </section>
      <section class="card">
        <h2>存档</h2>
        <p class="small muted">{NATIVE ? "进度只存在这个 App 里。卸载或换手机前，先导出（会弹出分享，可以发到微信、QQ 或存到文件）。" : "进度只存在这个浏览器里。换电脑或清理浏览器数据前，先导出。"}</p>
        <div class="row">
          <button type="button" class="btn" onClick={exportFile}>导出存档</button>
          <ImportSave />
          {!confirmReset ? <button type="button" class="btn ghost danger" onClick={() => setConfirmReset(true)}>清空进度…</button> : <>
            <span>确定清空全部进度？</span>
            <button type="button" class="btn danger" onClick={() => { store.replace({ v: 1 }); setConfirmReset(false); toast({ title: "进度已清空" }); }}>清空</button>
            <button type="button" class="btn ghost" onClick={() => setConfirmReset(false)}>取消</button>
          </>}
        </div>
      </section>
      <section class="small muted">
        <p>数据来自 cs-math-skill-tree（{g.tree.meta.builtFrom}）：游戏保留 {g.tree.meta.skills} 个技能、{g.tree.meta.requiredEdges} 条“要先学”的连线，包含“数据中心与高性能网络”；筛去了“交叉应用与前沿专题”。</p>
      </section>
      <UpdateCheck />
    </div>
  );
}

// Version and a manual "is there a newer one?" (the app also checks by itself once a day).
function UpdateCheck() {
  const [st, setSt] = useState({});
  // aria-disabled rather than disabled while busy: a disabled button drops the keyboard and
  // screen-reader focus, and the result below would be announced with the reader lost on the page.
  const check = async () => {
    if (st.busy) return;
    setSt({ busy: true });
    try { setSt({ result: await checkUpdate() }); } catch (e) { setSt({ error: e.message }); }
  };
  const r = st.result;
  return (
    <section class="card update-check">
      <h2>版本</h2>
      <p>当前版本 <b>{VERSION}</b>{NATIVE ? "" : "（网页版）"}</p>
      <div class="row">
        <button type="button" class="btn" aria-disabled={st.busy ? "true" : undefined} onClick={check}>{st.busy ? "正在检查…" : "检查更新"}</button>
        <a class="small" href={RELEASES_PAGE} target="_blank" rel="noopener">所有版本和更新说明</a>
      </div>
      <div role="status" aria-live="polite">
        {st.error && <p class="small">{st.error}</p>}
        {r && !r.newer && <p class="small">已经是最新版本（GitHub 上最新的是 {r.latest}）。</p>}
        {r?.newer && <>
          <p><b>有新版本 {r.latest}</b>{NATIVE ? "：下载后点开安装，进度不会丢。" : "。"}</p>
          {r.notes && <pre class="release-notes small">{r.notes}</pre>}
          <a class="btn primary" href={NATIVE ? r.download : r.page} target="_blank" rel="noopener">{NATIVE ? "下载新版本" : "去发布页"}</a>
        </>}
      </div>
    </section>
  );
}
