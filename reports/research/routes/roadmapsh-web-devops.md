# roadmap.sh role roadmaps — top-level topic lists

Research date: 2026-11-03 (UTC). Read-only research; no project files touched except this report.

## Source & method (read this first)

The task's suggested GitHub path **no longer exists on master**:

- `https://raw.githubusercontent.com/kamranahmedse/developer-roadmap/master/src/data/roadmaps/backend/backend.json` → **404**
- `https://api.github.com/repos/.../contents/src/data/roadmaps/backend` → **404**; the repo root has no `src/` any more, only `roadmaps/`, and `roadmaps/backend/` contains **only `content/`** (markdown, one file per node, e.g. `roadmaps/backend/content/caching@uPjCrDGA2MHylWXbZvMBM.md`). Per-node markdown has **no hierarchy / no front-matter**, so the graph cannot be rebuilt from the repo any more.
- Note: `kamranahmedse/developer-roadmap` now **301-redirects** via the API to `nilbuild/developer-roadmap` (same repo id 85077558). The old JSON layout is still reachable at the last pre-restructure commit `6f745dc1eaa9d6a9841fe964be33835263f0fd92` (restructure commit = `274082fd77f4`, 2026-07-27, "clean roadmap content and sync scripts").

What I actually used (per roadmap): **the JSON the site itself renders**, at `https://roadmap.sh/<slug>.json` (HTTP 200, e.g. 155 KB for backend), plus the GitHub **atom** feeds for commit ids (the commits API was rate-limited):

- `https://github.com/nilbuild/developer-roadmap/commits/master/roadmaps/<slug>/content.atom`
- repo HEAD at read time: `491a0e3314b0` (2026-10-31T16:08:41Z), branch `master`

Structure of the site JSON: `nodes[]` with `type` = `title | topic | subtopic | paragraph | label | button | section | legend | linksgroup | vertical | horizontal`; `edges[]` with `data.edgeStyle` = `solid | dashed` (in practice `dashed` = parent→child grouping links, **not** "optional": 37 dashed vs 23 solid in backend, all dashed ones topic→subtopic apart from 2 that point from a subtopic up to a topic); each roadmap also has Mongo `_id`, `slug`, `title{card,page}`, `updatedAt`.

**Top-level topics below = the `topic`-type nodes** (the boxes that carry a content page); `subtopic` nodes are the leaves and were dropped. Order = node `y` coordinate (top→bottom, x as tie-break), cross-checked against the solid edge chains; where the two disagree I say so.

**Recommended vs optional/alternative**: only three roadmaps carry a legend (`legend` node + a `data.legend` object on individual nodes):

| marker | colour | label (backend / frontend / devops) |
|---|---|---|
| rec | `#874efe` | "Personal Recommendation / Opinion" |
| alt | `#4f7a28` (devops `#667113`) | "Alternative Option (Pick this or purple)" |
| loose | `#929292` (devops `#949494`) | "Order not strict / Learn anytime" |

Applied as `[rec] [alt] [loose]` below. **`full-stack` and `android` have no legend node and no `data.legend` on any node** → nothing to mark. In the other three, the legend is applied mostly to *sub*-nodes; at topic level only `frontend` has marked topics (listed). Examples at sub-node level: backend "Frontend Basics" → HTML, CSS [rec]; frontend "Learn a Framework" → React [rec] vs Angular/Vue.js/SvelteKit [alt].

---

## 1. Backend — `https://roadmap.sh/backend.json`

- URLs read: `https://roadmap.sh/backend.json`; `https://github.com/nilbuild/developer-roadmap/commits/master/roadmaps/backend/content.atom`
- JSON `title`: Backend / "Backend Developer", `slug: backend`, `updatedAt: 2026-02-07T16:58:57Z`
- latest commit on `roadmaps/backend/content`: `9cdd2e13da21`, 2026-10-26T07:34:24Z ("docs: fix moved resource links and drop dead ones (#10486)")
- 225 nodes: 23 `topic`, 132 `subtopic`. No topic-level legend marks (legend colours are used on sub-nodes only).

1. Introduction
2. Frontend Basics
3. Pick a Backend Language
4. Version Control Systems
5. Repo Hosting Services
6. Relational Databases
7. Learn about APIs
8. Caching
9. Learn about Web Servers
10. Learn the Basics  *(AI sub-branch, left column: "How LLMs work", "AI vs Traditional Coding", "Embeddings", "Vectors")*
11. Applications  *(AI sub-branch: "Code Reviews", …)*
12. AI Assisted Coding
13. Integration Patterns
14. CI / CD
15. More about Databases
16. Testing
17. Message Brokers
18. Architectural Patterns
19. Search Engines
20. Real-Time Data
21. Scaling Databases
22. NoSQL Databases
23. Building For Scale

Caveats: 10–14 ("Learn the Basics", "Applications", "AI Assisted Coding", "Integration Patterns", "CI / CD") sit in side columns of the layout — the AI branch hangs off "Learn about Web Servers" via the label "AI in Development". One edge contradicts the layout ("More about Databases → CI / CD"), so the exact sequence of the late sections (14–19) is approximate; the *set* is exact.
Non-topic top-level items (excluded): title "Backend", buttons "Visit Beginner Friendly Version", "Beginner/Intermediate Project Ideas", "Docker", "Kubernetes", "System Design", "Design & Architecture", "DevOps", "Full Stack", "Basic Operations Skills", "Prompt Engineering Roadmap", "AI Agents Roadmap", paragraphs ("Learn one language and build lots of projects before moving on", "You may never need most of these…"), labels ("API Styles", "Server Side", "AI in Development", "Advanced Backend", "Containerization", "Hashing Algorithms").

## 2. Full Stack — `https://roadmap.sh/full-stack.json`

- URLs read: `https://roadmap.sh/full-stack.json`; `https://github.com/nilbuild/developer-roadmap/commits/master/roadmaps/full-stack/content.atom`
- JSON `title`: Full Stack / "Full Stack Developer", `updatedAt: 2026-01-06T16:31:50Z`
- latest commit on `roadmaps/full-stack/content`: `621b8478da5f`, 2026-08-14T16:59:55Z ("fix: correct typos and improve clarity…")
- 79 nodes: 19 `topic`, 18 `subtopic`. **No legend** in this roadmap.

Order below = the solid edge chain from the title node (authoritative; it matches the layout except for one tie row):

1. HTML
2. CSS
3. JavaScript
4. npm
5. Git
6. GitHub
7. Tailwind CSS
8. React
9. Node.js  *(after the paragraph "Start Backend Development")*
10. PostgreSQL
11. RESTful APIs
12. JWT Auth
13. Redis
14. Linux Basics
15. Basic AWS Services
16. Monit
17. GitHub Actions
18. Ansible
19. Terraform

Excluded non-topics: buttons "Frontend / Backend / DevOps / AWS", 13 `subtopic` "Checkpoint …" nodes ("Static Webpages", "Interactivity", "Collaborative Work", "External Packages", "Frontend Apps", "CLI Apps", "Simple CRUD Apps", "Complete App", "Deployment", "Automation", "CI / CD", "Monitoring", "Infrastructure" — the source stores a separator glyph before the name that renders as mojibake in the JSON), paragraphs/labels ("Backend Starts here", "DevOps starts here").

## 3. Frontend — `https://roadmap.sh/frontend.json`

- URLs read: `https://roadmap.sh/frontend.json`; `https://github.com/nilbuild/developer-roadmap/commits/master/roadmaps/frontend/content.atom`
- JSON `title`: Frontend / "Frontend Developer", `updatedAt: 2026-07-15T11:43:37Z`
- latest commit on `roadmaps/frontend/content`: `a02b7d34156f`, 2026-10-31T16:08:22Z ("chore: sync content to repo (#10515)")
- 156 nodes: 37 `topic`, 83 `subtopic`. Legend marks at topic level: `[rec]` React, GraphQL; `[alt]` Vue.js, SvelteKit; `[loose]` PWAs, Mobile Apps.

Main spine (order cross-checked with solid edges where they exist):

1. Internet
2. HTML
3. CSS
4. JavaScript
5. Version Control  *(sic — trailing space in source)*
6. VCS Hosting
7. Package Managers
8. CSS Frameworks
9. Learn a Framework — framework choice nodes under it: **React [rec]**, **Vue.js [alt]**, **SvelteKit [alt]** (they have their own children: Next.js / Tanstack Start, Nuxt.js, …)
10. Learn the Basics  *(AI sub-branch, right column under label "AI in Development": "How LLMs work", "AI vs Traditional Coding", "Applications" → Code Reviews, Refactoring, Docs Generation)*
11. AI Assisted Coding
12. Prompting Techniques
13. Agents
14. MCP
15. Skills
16. Implementing AI
17. Linters & Formatters  *(label "Advanced Frontend" links here from Implementing AI)*
18. Module Bundlers
19. Auth Strategies
20. Testing
21. Web APIs
22. Web Security
23. SSR
24. SSG
25. Type Checkers
26. Deployment
27. Design Systems
28. Performance
29. Web Components
30. GraphQL [rec]
31. Accessibility
32. PWAs [loose]
33. Desktop Apps
34. Mobile Apps [loose]

Notes: 37 `topic` nodes total = the 34 above + React + Vue.js + SvelteKit (listed inline at #9; they are `topic` nodes because they have children, but they belong to the "Learn a Framework" branch). Items 17–19 share one layout row and 21–22 share one row; their internal order comes from the edges (Linters & Formatters → Module Bundlers → Auth Strategies; Testing → Web APIs → Web Security → SSR). Excluded non-topics: buttons ("Advanced Project Ideas", "TypeScript", "Prompt Engineering", "AI Agents Roadmap"), labels ("AI in Development", "Advanced Frontend"), paragraphs.

## 4. DevOps — `https://roadmap.sh/devops.json`

- URLs read: `https://roadmap.sh/devops.json`; `https://github.com/nilbuild/developer-roadmap/commits/master/roadmaps/devops/content.atom`
- JSON `title`: DevOps / "DevOps Roadmap", `updatedAt: 2026-10-27T10:48:40Z`
- latest commit on `roadmaps/devops/content`: `317e25b44a0c`, 2026-10-27T10:26:48Z ("docs(docker): add hands-on prepare.sh tutorials…")
- 171 nodes: 22 `topic`, 117 `subtopic`. No topic-level legend marks (colours used on sub-nodes only, e.g. under "Learn a Programming Language": Go [rec], Python [rec] vs Ruby [alt], Rust [alt], JavaScript / Node.js [alt]).

1. Learn a Programming Language
2. Operating System
3. Terminal Knowledge
4. Version Control Systems
5. VCS Hosting
6. Containers
7. What is and how to setup X ?  *(sic, trailing space before "?")*
8. Networking & Protocols
9. Cloud Providers
10. Serverless
11. Configuration Management
12. Provisioning
13. CI / CD Tools
14. Logs Management
15. Infrastructure Monitoring
16. Secret Management
17. Container Orchestration
18. Observability
19. Artifact Management
20. GitOps
21. Service Mesh
22. Cloud Design Patterns

Caveat: 14–16 and 17–20 are **parallel columns** in the layout (y ties at 2195 and 2475), so their relative order is not strict; edges show Secret Management → Infrastructure Monitoring → Logs Management (i.e. the reverse of the y order for 14/15). 11 vs 12 also tie (Configuration Management / Provisioning). Excluded non-topics: title "DevOps", buttons ("Visit the Beginner Version", "Network Engineer", "Cloud Computing", "Docker", "Kubernetes", "Linux"), labels ("Scripting", "Linux", "Unix", "Editors", "Web Server", "Email Protocols").

## 5. Android (= mobile) — `https://roadmap.sh/android.json`

- URLs read: `https://roadmap.sh/android.json`; `https://github.com/nilbuild/developer-roadmap/commits/master/roadmaps/android/content.atom`
- JSON `title`: Android / "Android Developer", `updatedAt: 2026-07-24T08:58:13Z`
- latest commit on `roadmaps/android/content`: `ab591ce0e9d2`, 2026-10-02T07:19:32Z ("docs: remove duplicate resource lines (#10411)")
- 157 nodes: 15 `topic`, 98 `subtopic`. **No legend** in this roadmap.

Order = solid edge chain (title → Pick a Language → The Fundamentals → Version Control → App Components → Interface & Navigation → Design & Architecture … Network → Asynchronism → Common Services → Linting → Testing → Debugging → Distribution), with Storage/Security placed by layout (no edge into them):

1. Pick a Language
2. The Fundamentals
3. Version Control
4. App Components
5. Interface & Navigation
6. Design & Architecture
7. Storage
8. Security
9. Network
10. Asynchronism
11. Common Services
12. Linting
13. Testing
14. Debugging
15. Distribution

Note: the layout puts "Asynchronism" (x 541) slightly above/before "Network" (x 860) on the same row, but the edge is Network → Asynchronism; I followed the edge. Excluded non-topics: title "Android", linksgroup "Related Roadmaps", buttons ("iOS", "React Native", "Flutter"), labels ("VCS Hosting", "Layouts", "Elements", "UI Patterns", "Navigation & State", "Legacy : XML Views", "Firebase", "Ways to distribute"), paragraphs ("Architectural Patterns" / "Design Patterns" / "Visit the following relevant roadmaps").

---

## Things I could not verify

- No rendered page/screenshot was obtained (roadmap.sh serves a client-rendered app; `/backend.png`, `/og-images/...` → 404), so "order" is derived from node coordinates + edges, not from the visual diagram.
- GitHub commits REST API hit rate limits (`403 API rate limit exceeded`) after ~10 calls; commit ids/dates above come from `commits/...atom` feeds instead (same repo, same data).
- The pre-restructure JSONs (e.g. `https://raw.githubusercontent.com/nilbuild/developer-roadmap/6f745dc1eaa9d6a9841fe964be33835263f0fd92/src/data/roadmaps/frontend/frontend.json`, HTTP 200) were downloaded but **not** used for the lists above; they differ from live data (frontend had 25 `topic` nodes then vs 37 now) and are stale.
