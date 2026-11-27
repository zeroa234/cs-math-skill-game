// Commits on a shared repository's main that the workspace has not taken in yet: the ones after the last
// commit this workspace pushed there. `--accept <sha>` says that commit and everything before it were taken
// into the workspace. Used by publish-github.mjs (the public repository, where AI Studio also commits);
// how to take commits in: docs/collaboration.md.
//   git: (...args) => stdout of `git -C <clone> ...args`, after a fetch
//   isOurs: ([sha, email, author, date, subject]) => true for a commit this workspace pushed
//   accepted: the --accept value or null
export function pendingCommits(git, isOurs, accepted) {
  let log;
  try {
    log = git("log", "--format=%H%x09%ae%x09%an%x09%ad%x09%s", "--date=short", "origin/main").split("\n").filter(Boolean).map((l) => l.split("\t"));
  } catch {
    return { base: null, unseen: [] }; // empty remote
  }
  const last = log.findIndex(isOurs);
  const pending = last < 0 ? log : log.slice(0, last);
  const at = accepted ? pending.findIndex(([h]) => h.startsWith(accepted)) : -1;
  if (accepted && at < 0) throw new Error(`--accept ${accepted}: not a commit after the last one this workspace pushed`);
  return { base: last < 0 ? null : log[last][0], unseen: at < 0 ? pending : pending.slice(0, at) };
}

// Lists the commits and what they changed; returns the hint for taking them in.
export function describePending(git, { base, unseen }, what) {
  const lines = [unseen.length ? `${what} has ${unseen.length} commit(s) not taken into the workspace:` : `nothing new on ${what} since the workspace last pushed there`];
  for (const [h, , an, ad, s] of unseen) lines.push(`  ${h.slice(0, 7)} ${ad} ${an}: ${s}`);
  if (unseen.length) {
    lines.push(base ? git("diff", "--stat", base, "origin/main") : git("show", "--stat", "--format=", "origin/main"));
    lines.push(`take what is worth keeping into the workspace (docs/collaboration.md), commit, then rerun with --accept ${unseen[0][0].slice(0, 7)}`);
  }
  return lines.join("\n");
}
