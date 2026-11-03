// 实验室: the experiments met in lessons so far (app/lab.js), to play with freely, not graded.
import { useState } from "preact/hooks";
import { SimDemo } from "./items.jsx";
import { href } from "../app/router.js";
import { packs, useProgress } from "../app/state.js";
import { labGroups, metKeys, programs } from "../app/lab.js";
import { Icon } from "./icons.jsx";

// Python 单步执行: pick one of the programs met on lesson cards.
function TraceLab({ list }) {
  const [i, setI] = useState(0);
  return (
    <>
      <label class="select">程序 <select value={i} onChange={(e) => setI(Number(e.currentTarget.value))}>{list.map((x, k) => <option value={k}>{x.label}</option>)}</select></label>
      <SimDemo key={i} sim={{ name: "trace", params: list[i].params }} />
    </>
  );
}

export function Lab() {
  const p = useProgress();
  const groups = labGroups(metKeys(packs, p));
  const progs = programs(packs, p);
  return (
    <div class="page lab">
      <a class="back" href={href()}><Icon name="back" /> 营地</a>
      <h1>实验室</h1>
      <p class="lead">课里出现过的实验都在这里，随便玩，不计分。课里每出现一个新的实验，这里就多一个。</p>
      {!groups.length && <p class="card lab-empty">还没有实验。学完一课，课里能动手操作的部分（比如一步一步执行一段程序）就会出现在这里。</p>}
      {groups.map((g) => (
        <section>
          <h2>{g.group}</h2>
          {g.items.map((it) => (
            <article class="card lab-item">
              <h3>{it.title}</h3>
              <p class="small muted">{it.try}</p>
              {it.name === "trace" ? (progs.length ? <TraceLab list={progs} /> : <p class="small">学完的课里还没有可以单步执行的程序（课里的练习题不算）。</p>) : <SimDemo sim={{ name: it.name, params: it.params }} />}
            </article>
          ))}
        </section>
      ))}
    </div>
  );
}
