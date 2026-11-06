// The Toy edition includes the skill graph and interactive packs. The separate
// self-study library (external reading, imported exercises and source evidence)
// belongs to the full edition. Keep stable IDs so local progress works in both.
export function toyTree(tree) {
  tree.meta.edition = "toy";
  for (const route of tree.routes) delete route.evidence;
  for (const skill of tree.skills) {
    skill.required = skill.required.map(({ id }) => ({ id }));
    skill.recommended = skill.recommended.map(({ id }) => ({ id }));
    skill.chapters = skill.chapters.map(({ no, title, stage }) => ({ no, title, stage }));
    skill.chapterOrder = { basis: "original", source: null };
    skill.sources = [];
    skill.courses = [];
    skill.exercise = null;
    skill.hasOutline = false;
    for (const key of ["readingSteps", "routeStatus", "prereqSummary", "kth", "extensionNote"]) delete skill[key];
  }
  return tree;
}
