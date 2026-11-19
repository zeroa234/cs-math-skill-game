// The author's GitHub identity for commits to the public and collaboration repositories (no AI attribution).
export const GITHUB_ID = { name: "zeroa234", email: "208007470+zeroa234@users.noreply.github.com" }; // as on zeroa234/cs-math-skill-tree
export const githubEnv = () => ({ ...process.env, GIT_AUTHOR_NAME: GITHUB_ID.name, GIT_AUTHOR_EMAIL: GITHUB_ID.email, GIT_COMMITTER_NAME: GITHUB_ID.name, GIT_COMMITTER_EMAIL: GITHUB_ID.email });
