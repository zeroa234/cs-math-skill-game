// Where the skill tree's built data is read from: the sibling ../cs-math-skill-tree in the author's
// workspace, or vendor/cs-math-skill-tree (only output/skilltree.json and output/outlines.json) in a
// clone that has no sibling, such as the cloud collaboration repository (docs/collaboration.md).
import fs from "node:fs";
import path from "node:path";

export function treeDir(root) {
  const sibling = path.join(root, "../cs-math-skill-tree");
  return fs.existsSync(path.join(sibling, "output/skilltree.json")) ? sibling : path.join(root, "vendor/cs-math-skill-tree");
}
