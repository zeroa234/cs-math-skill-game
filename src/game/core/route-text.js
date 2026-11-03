// What a route says about itself when nobody wrote its story by hand: a goal the player picked, or
// the author's own goal (我的远征). Everything comes from the tree, so any of the skills gets a
// name, a one-line tagline and a short introduction in the same voice as the curated routes.
// Pure: takes the indexed tree (graph.js indexTree) and a planned route (planRoute).

const join = (xs) => xs.join("、");

// Stops grouped by the lane they belong to, in the order the lanes first appear on the route.
export function stopsByLane(g, stops) {
  const groups = new Map();
  for (const id of stops) {
    const s = g.byId.get(id);
    if (!groups.has(s.lane)) groups.set(s.lane, { lane: g.lanes.get(s.lane), skills: [] });
    groups.get(s.lane).skills.push(s);
  }
  return [...groups.values()];
}

// Which shelf a route sits on, as the player reads it.
export const KIND_LABEL = { own: "我的远征", recommended: "推荐远征", custom: "自定目标" };

export function goalRouteText(g, route) {
  const goal = g.byId.get(route.goal);
  const first = g.byId.get(route.stops[0]);
  const before = route.stops.filter((id) => id !== goal.id);
  const core = goal.chapters.filter((c) => c.stage !== "extension").map((c) => c.title);
  const story = [`终点“${goal.name}”要学：${join(core)}。`];
  if (before.length) {
    const parts = stopsByLane(g, before).map((x) => `${x.lane.short}（${join(x.skills.map((s) => s.name))}）`);
    story.push(`在那之前要先学 ${before.length} 个技能：${join(parts)}。它们是“${goal.name}”要求先学的技能，加上这些技能自己要求先学的，由技能树按先后排好。`);
  } else {
    story.push(`“${goal.name}”不要求先学别的技能，可以直接开始。`);
  }
  const code = (course) => course.match(/^([A-Za-z]+\s*)?\d[\w./-]*/)?.[0] || course;
  const courses = (goal.courses || []).map((c) => `${c.school} ${code(c.course)}`);
  if (courses.length) story.push(`要先学什么，依据是大学课程的先修要求：${join(courses)}（原文在技能详情里）。`);
  return {
    name: goal.name,
    tagline: before.length ? `从“${first.name}”走到“${goal.name}”，共 ${route.stops.length} 站` : `目标：点亮“${goal.name}”`,
    story,
  };
}
