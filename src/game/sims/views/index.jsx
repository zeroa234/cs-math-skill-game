// Registry of sim views by name (logic lives in ../logic, shared with the node-side checks).
import os from "./os.jsx";
import trace from "./trace.jsx";
import algo from "./algo.jsx";

export const SIM_VIEWS = { ...os, ...trace, ...algo };
