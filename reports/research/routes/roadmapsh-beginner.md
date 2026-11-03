# roadmap.sh "beginner" roadmap variants — research report

Read on the live site (no memory used). Everything below is from HTTP responses / rendered DOM I actually fetched.

## Method (what worked)

1. JSON API per slug: `https://roadmap.sh/api/v1-official-roadmap/<slug>` (200 = exists, 404 = no such slug).
   Top-level topics = nodes `type:"topic"`, leaves = `type:"subtopic"`; order taken from node `position.y` (x as tie-break).
2. Rendered pages in headless Edge (`msedge.exe` via `playwright-core` from `projects/cs-math-skill-game/node_modules`), then read the SVG:
   every node is `<g data-node-id data-type data-title>`, its box is the child `<rect fill=...>`; legend badges are `<circle id="icon-link" fill=...>` at the node's left edge.
   This was necessary because **the JSON contains no colour/optional data at all** (node `data.style` has only fontSize/justifyContent/textAlign).
3. Link discovery on the role pages' HTML: `https://roadmap.sh/<role>` embeds a button whose label + href point at the beginner variant.
4. Cross-check of the complete slug list: `https://api.github.com/repos/kamranahmedse/developer-roadmap/contents/roadmaps?ref=master` (97 roadmap dirs) and the site index `https://roadmap.sh/roadmaps/`.

Measured fills (rendered): topic boxes `#fdff00` (bright yellow, core), subtopic boxes `#ffe599` (pale yellow), badge purple `#874efe`, badge green `#4f7a28`. Grey `#929292` exists **only as the third legend swatch** ("Order not strict / Learn anytime") and does **not** occur on any node of any beginner roadmap — so "light grey = optional" is not how these pages are marked.

## Existence summary

| role | beginner variant | slug |
|---|---|---|
| backend | yes | backend-beginner |
| frontend | yes | frontend-beginner |
| devops | yes | devops-beginner |
| full-stack | **no** | – |
| android | **no** | – |
| cyber-security | **no** | – |
| ai-data-scientist | **no** | – |
| java | **no** | – |

There is also a 4th beginner roadmap site-wide that was not in the question: `git-github-beginner` (`/api/v1-official-roadmap/git-github-beginner` → 200, `/git-github-beginner` → 200).

## 1. Backend Beginner — YES

URLs read:
- `https://roadmap.sh/api/v1-official-roadmap/backend-beginner` (200, slug `backend-beginner`, title.card "Backend Beginner", type `skill`)
- `https://roadmap.sh/backend?r=backend-beginner` (rendered)
- `https://roadmap.sh/backend-beginner` (rendered; canonical `<link rel=canonical href="https://roadmap.sh/backend-beginner"/>`; identical 8 topics / 18 subtopics as the `?r=` view)
- `https://roadmap.sh/backend` (the link lives there: button **"Visit Beginner Friendly Version"** → `/backend?r=backend-beginner`)

updatedAt: `2026-03-04T16:32:38.311Z` (createdAt `2025-05-14T10:07:04.691Z`)

8 top-level topics in order (y), subtopics as named, badge = optional mark:

1. **Pick a Language** — JavaScript *(purple)*, Go *(green)*, Python *(green)*
2. **Version Control Systems** — Git *(purple)*
3. **Repo hosting services** — Github *(purple)*
4. **Relational Databases** — PostgreSQL *(purple)*
5. **Learn about APIs** — REST *(purple)*, JSON APIs *(purple)*, Authentication *(none)*, JWT *(none)*
6. **Caching** — Redis *(none)*
7. **More about Databases** — ORMs, ACID, Transactions, N+1 Problem *(all none)*
8. **Testing** — Integration Testing, Unit Testing, Functional Testing *(all none)*

Badge census: 8 of 18 subtopics carry a badge (6× purple = "Personal Recommendation / Opinion", 2× green = "Alternative Option / Pick this or purple"); no topic box has a badge. Legend box is shown on this page with all three colours.
Data anomaly: in the API JSON, JWT is the only subtopic with **no edge** to any parent; in the rendered roadmap it is drawn nested under Authentication (same column, directly below it), so it is listed there.
Footer of the roadmap: paragraph "Have a look at the detailed version" + button "Backend Developer Roadmap" → `/backend`.

## 2. Frontend Beginner — YES

URLs read:
- `https://roadmap.sh/api/v1-official-roadmap/frontend-beginner` (200, title.card "Frontend Beginner", type `skill`)
- `https://roadmap.sh/frontend?r=frontend-beginner` (rendered)
- `https://roadmap.sh/frontend` (button **"Visit Beginner Friendly Version"** → `/frontend?r=frontend-beginner`)
- canonical on `/frontend-beginner`: `https://roadmap.sh/frontend-beginner`

updatedAt: `2026-03-04T16:31:44.654Z` (createdAt `2025-05-14T10:07:04.668Z`)

9 top-level topics, **no subtopics at all** (the 19 `type:"label"` nodes are free-floating side notes / tips, e.g. "Important Tip", "You should be able to find an intern or Junior…"; they are not attached to topics):

1. HTML
2. CSS
3. JavaScript
4. Git *(same row as GitHub; x −304.7)*
5. GitHub *(x −104.7)*
6. npm
7. React
8. Tailwind
9. Vitest

Optional marks: none — 0 badges, no legend box rendered, all 9 topic boxes `#fdff00`.
Page also shows a box "This is the beginner friendly version of the Frontend roadmap…" with buttons "Visit the Detailed Version" (`/frontend`) and "Visit Detailed Frontend Roadmap" (`https://roadmap.sh/frontend`).

## 3. DevOps Beginner — YES

URLs read:
- `https://roadmap.sh/api/v1-official-roadmap/devops-beginner` (200, title.card "DevOps Beginner", type `skill`)
- `https://roadmap.sh/devops?r=devops-beginner` (rendered)
- `https://roadmap.sh/devops` (button label differs: **"Visit the Beginner Version"** → `/devops?r=devops-beginner`)
- canonical on `/devops-beginner`: `https://roadmap.sh/devops-beginner`

updatedAt: `2026-03-04T16:32:50.218Z` (createdAt `2025-05-14T10:07:04.747Z`)

11 top-level topics in order:

1. **Programming Language** — Python, Go *(no badges)*
2. Operating System
3. Networking & Protocols
4. Docker
5. Git *(same row as GitHub; x −270.2)*
6. GitHub *(x −139.2)*
7. AWS
8. Terraform
9. Ansible
10. GitHub Actions
11. Nginx

Optional marks: none — 0 badges, no legend box, all 11 topic boxes `#fdff00`, both subtopics `#ffe599`.
Extra (non-topic) node: a dark-purple **button** "Linux" → `https://roadmap.sh/linux`, attached to Operating System. Footer: "Visit the Detailed Version" (`/devops`) and "Visit Detailed DevOps Roadmap" (`https://roadmap.sh/devops`).

## Roles with no beginner version

All five: **full-stack, android, cyber-security, ai-data-scientist, java** — no beginner roadmap exists.

How checked (all returned negative):
- `https://roadmap.sh/api/v1-official-roadmap/<role>-beginner` → **404** for `full-stack-beginner`, `android-beginner`, `cyber-security-beginner`, `ai-data-scientist-beginner`, `java-beginner` (also `fullstack-beginner`, `cybersecurity-beginner`, `ai-beginner` → 404).
- `https://roadmap.sh/<role>-beginner` page route → **404** (all five).
- Base slugs verified valid first: `…/full-stack`, `…/android`, `…/cyber-security`, `…/ai-data-scientist`, `…/java` all return 200 (titles Full Stack / Android / Cyber Security / AI and Data Scientist / Java).
- Role page HTML (`https://roadmap.sh/full-stack`, `/android`, `/cyber-security`, `/ai-data-scientist`, `/java`) contains **no** `?r=` variant link of any kind and no beginner slug; the few "Beginner" strings found are unrelated (course titles like "SQL and Python for Beginners", "OpenClaw for Beginners", and a topic label "Beginner Certifications" on cyber-security).
- Site index `https://roadmap.sh/roadmaps/` links only `/backend-beginner`, `/devops-beginner`, `/frontend-beginner`, `/git-github-beginner`.
- GitHub `developer-roadmap` repo, `roadmaps/` directory (97 entries) contains only `backend-beginner`, `devops-beginner`, `frontend-beginner`, `git-github-beginner`.

## Caveats / failures

- No fetch failed outright; the only timeouts were `waitUntil:"networkidle"` on roadmap.sh (ads/analytics keep sockets open) — fixed by using `domcontentloaded` + waiting for `g[data-type="topic"]`.
- `https://roadmap.sh/roadmaps` is a 301 to `/roadmaps/`; `https://roadmap.sh/sitemap.xml` is 404.
- The API JSON carries no colours and no "optional" flag; badge/colour claims above come from the rendered SVG only. Badge count was stable when scrolling the whole page (11 `#icon-link` circles on backend = 8 node badges + 3 legend swatches), so absent badges are real, not lazy-loading artefacts.
- Server-side draft/unpublished beginner roadmaps cannot be ruled out (unknown slugs and drafts both yield 404); the GitHub content dir is the strongest available enumeration.
- `updatedAt` values are quoted exactly as returned (they read as 2026 dates).
