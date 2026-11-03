// Shell: top navigation and the hash-routed views. The first visit opens with the intro scene.
// A save that cannot be read replaces all of it until the player decides (SaveProblem.jsx).
import { useEffect } from "preact/hooks";
import { useRoute, href } from "../app/router.js";
import { useProgress, dueCards, store, activeRoute, packs } from "../app/state.js";
import { play } from "../app/sound.js";
import { setMusicScene } from "../app/music.js";
import { Home } from "./Home.jsx";
import { Intro } from "./Intro.jsx";
import { PickGoal } from "./PickGoal.jsx";
import { RouteView } from "./RouteView.jsx";
import { MapView } from "./MapView.jsx";
import { SkillView } from "./SkillView.jsx";
import { LessonPlayer } from "./LessonPlayer.jsx";
import { BossView } from "./BossView.jsx";
import { ReviewView } from "./ReviewView.jsx";
import { Profile } from "./Profile.jsx";
import { Lab } from "./Lab.jsx";
import { Toasts } from "./common.jsx";
import { Icon } from "./icons.jsx";
import { useSaveHealth, UnreadableSave, UnsavedWarning } from "./SaveProblem.jsx";

export function App() {
  const health = useSaveHealth();
  if (health.unreadable) return <><main id="main"><UnreadableSave problem={health.unreadable} /></main><Toasts /></>;
  return <Game unsaved={health.unsaved} />;
}

function Game({ unsaved }) {
  const r = useRoute();
  const p = useProgress();
  const due = dueCards(p).length;
  const intro = r.name === "intro" || (r.name === "home" && !p.settings.introSeen);
  const immersive = intro || r.name === "lesson" || (r.name === "review" && due > 0);
  let view;
  switch (r.name) {
    case "intro": view = <Intro />; break;
    case "pick": view = <PickGoal />; break;
    case "route": view = <RouteView id={r.args[0]} />; break;
    case "map": view = <MapView />; break;
    case "skill": view = <SkillView id={r.args[0]} />; break;
    case "lesson": view = <LessonPlayer skillId={r.args[0]} lessonId={r.args[1]} />; break;
    case "boss": view = <BossView id={r.args[0]} mode={r.args[1]} />; break;
    case "review": view = <ReviewView />; break;
    case "me": view = <Profile />; break;
    case "lab": view = <Lab />; break;
    default: view = intro ? <Intro /> : <Home />;
  }
  const onRoute = activeRoute(p);
  const routeHref = onRoute ? href("route", onRoute.id) : href("pick");
  const nav = [["home", "营地", href()], ["route", "远征", routeHref], ["map", "地图", href("map")], ["review", `复习${due ? " " + due : ""}`, href("review")], ["me", "我的", href("me")]];
  const active = (k) => r.name === k || (k === "route" && r.name === "pick");
  const sound = p.settings.sound !== false;
  const toggleSound = () => { store.update((d) => { d.settings.sound = !sound; }); if (!sound) setTimeout(() => play("select"), 0); };
  // Music by what the player is doing; a final challenge without lessons is only reading, so calm.
  const scene = intro ? "title" : r.name === "lesson" || r.name === "review" ? "focus" : r.name === "boss" && packs[r.args[0]] ? "challenge" : "explore";
  useEffect(() => setMusicScene(scene), [scene]);
  return (
    <>
      {!immersive && (
        <header class="topbar">
          <a class="brand" href={href()} aria-label="点亮之路，回营地"><span class="logo"><Icon name="sparkle" size={24} /></span><span class="brand-text">点亮之路</span></a>
          <nav aria-label="主导航">{nav.map(([k, label, h]) => <a href={h} class={active(k) ? "active" : ""} aria-current={active(k) ? "page" : undefined}>{label}</a>)}</nav>
          <button type="button" class="icon-btn" aria-pressed={sound} aria-label={sound ? "声音：开（点一下关闭音效和音乐）" : "声音：关（点一下打开）"} title={sound ? "关闭声音" : "打开声音"} onClick={toggleSound}><Icon name={sound ? "volume" : "mute"} size={24} /></button>
        </header>
      )}
      {unsaved && <UnsavedWarning />}
      <main id="main" class={"view-" + r.name}>{view}</main>
      <Toasts />
    </>
  );
}
