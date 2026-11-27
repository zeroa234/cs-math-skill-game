// Unit tests for scripts/lib/pending-commits.mjs: which commits on a shared repository the workspace has not
// taken in (publish-github.mjs refuses to push over them). Run: npm test.
import test from "node:test";
import assert from "node:assert/strict";
import { pendingCommits } from "../../scripts/lib/pending-commits.mjs";

const OURS = "208007470+zeroa234@users.noreply.github.com";
// newest first, as `git log` prints them: sha, author email, author, date, subject
const LOG = [
  ["c3", "gemini@example.com", "ANONONE", "2026-11-28", "feat: lesson draft"],
  ["c2", "gemini@example.com", "ANONONE", "2026-11-28", "chore: dev server"],
  ["b1", OURS, "zeroa234", "2026-11-27", "v2.6.0"],
  ["a0", "gemini@example.com", "ANONONE", "2026-11-27", "older, before our last snapshot"],
];
const fakeGit = (log) => (...args) => {
  if (args[0] !== "log") throw new Error("unexpected git call " + args.join(" "));
  return log.map((c) => c.join("\t")).join("\n");
};
const isOurs = ([, email, , , s]) => email === OURS && /^v\d+\.\d+\.\d+$/.test(s);

test("commits after the workspace's last snapshot are pending, older ones are not", () => {
  const { base, unseen } = pendingCommits(fakeGit(LOG), isOurs, null);
  assert.equal(base, "b1");
  assert.deepEqual(unseen.map(([h]) => h), ["c3", "c2"]);
});

test("--accept takes in that commit and everything before it", () => {
  assert.deepEqual(pendingCommits(fakeGit(LOG), isOurs, "c2").unseen.map(([h]) => h), ["c3"]);
  assert.deepEqual(pendingCommits(fakeGit(LOG), isOurs, "c3").unseen, []);
});

test("--accept of a commit that is not pending is an error", () => {
  assert.throws(() => pendingCommits(fakeGit(LOG), isOurs, "a0"), /not a commit after/);
});

test("nothing pending right after our own push; an empty remote has nothing pending", () => {
  assert.deepEqual(pendingCommits(fakeGit(LOG.slice(2)), isOurs, null).unseen, []);
  assert.deepEqual(pendingCommits(() => { throw new Error("unknown revision origin/main"); }, isOurs, null), { base: null, unseen: [] });
});

test("a snapshot subject from someone else is not ours", () => {
  const log = [["d1", "gemini@example.com", "ANONONE", "2026-11-28", "v2.6.1"], ...LOG.slice(2)];
  assert.deepEqual(pendingCommits(fakeGit(log), isOurs, null).unseen.map(([h]) => h), ["d1"]);
});
