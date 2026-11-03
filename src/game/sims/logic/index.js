// Registry of sim logic (pure, runs in node and the page). The UI views live in src/game/sims/views/.
// Only the sims today's lessons use; the rest are in archive/src/game/sims/ (see archive/README.md).
import os from "./os.js";
import trace from "./trace.js";
import algo from "./algo.js";
import { registerSimChecker } from "../../core/check.js";

export const SIMS = Object.fromEntries([...os, ...trace, ...algo].map((s) => [s.name, s]));
for (const s of Object.values(SIMS)) registerSimChecker(s.name, (p, g, r) => s.check(p, g, r));
