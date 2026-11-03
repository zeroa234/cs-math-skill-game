// Banner art for a route (pictures and prompts: assets/bg/README.md). A route with a picture of its
// own (routes.yaml `art`) shows it; any other route shows the picture of the lane its headline goal
// sits in, so a goal a player picks gets a fitting scene without anyone drawing it a banner.
import { g } from "./state.js";

const BG = "assets/bg/";
const LANE_ART = { M1: "lane-math", M2: "lane-math", M3: "lane-math", F: "lane-f", P: "lane-p", C: "lane-c", D: "lane-d", A: "lane-a", S: "lane-s", H: "lane-h", V: "lane-v", I: "lane-i" };
export const TITLE_ART = BG + "title.png";

export function artFor(route) {
  if (!route) return TITLE_ART;
  if (route.art) return `${BG}${route.art}.png`;
  const lane = g.byId.get(route.goal)?.lane;
  return LANE_ART[lane] ? `${BG}${LANE_ART[lane]}.png` : TITLE_ART;
}
