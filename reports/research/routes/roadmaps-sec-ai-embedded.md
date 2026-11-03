# Roadmap top-level topic extraction — security / AI / data / embedded
Research date: 2026-11-03. Only what was actually fetched is reported.

## Sources & method
- roadmap.sh pages are client-rendered, so topic lists were taken from the site's own JSON API
  `https://roadmap.sh/api/v1-official-roadmap/<slug>` (found in the page's JS bundle
  `official-roadmap-*.js`: `queryFn: a("/v1-official-roadmap/${r}")`), and cross-checked against the
  rendered DOM (headless Edge via playwright-core, `https://roadmap.sh/<slug>`, reading each node's
  SVG box + `fill` colour).
- GitHub: `kamranahmedse/developer-roadmap` now resolves to **`nilbuild/developer-roadmap`**
  (raw.githubusercontent.com/kamranahmedse/... → 404; raw.githubusercontent.com/nilbuild/... → 200).
  `src/data/roadmaps/` **no longer exists on master**; master's `roadmaps/<slug>/` contains only
  `content/*.md`. Last commit touching `src/data/roadmaps/cyber-security/cyber-security.json`:
  `274082fd77f47874b957fd70bf19bbc0812fc13a` (2026-07-27, "feat: clean roadmap content and sync scripts
  (#10181)"). Last snapshot that still had the JSON: commit
  `deb9aaafc283f5cf88816cd79528d600878c22cc` (2025-04-04, "Migrate roadmaps"), read at
  `https://raw.githubusercontent.com/nilbuild/developer-roadmap/deb9aaafc283f5cf88816cd79528d600878c22cc/src/data/roadmaps/<slug>/<slug>.json`
  (200 for cyber-security, ai-engineer, ai-data-scientist, data-analyst; **404 for data-engineer**).
  That snapshot is stale (e.g. ai-engineer had 16 topics then vs 22 now), so the **live API is the
  source of the lists below**; the 2025-04 JSON was used only to confirm structure.
- Repo metadata (GitHub API, before rate-limiting): `nilbuild/developer-roadmap`, default branch
  `master`, 371,100 stars, pushed_at `2026-10-31T16:08:41Z`.
- Colour code in the rendered roadmap (verified from computed `fill`): bright yellow
  `rgb(253,255,0)` = core/recommended topic; beige `rgb(255,229,153)` = normal subtopic;
  light grey `rgb(244,244,244)` = alternative/optional pick. Dashed connector lines are **not** an
  optional marker (renderer draws every topic→subtopic edge dashed).

---

## 1. roadmap.sh/cyber-security
Read: `https://roadmap.sh/api/v1-official-roadmap/cyber-security`; `https://roadmap.sh/cyber-security`
(rendered); GitHub JSON at `deb9aaa…` (identical 6 topics). API record `_id 68246b4811b0d89408504880`,
`updatedAt 2026-06-15T11:47:47.372Z`, page title "Cyber Security Expert".

Top-level topic nodes (all 6 bright yellow = core; **no optional top-level node**), in order:
1. Fundamental IT Skills
2. Operating Systems
3. Networking Knowledge
4. Security Skills and Knowledge
5. Cloud Skills and Knowledge
6. Programming Skills

Side panels (label groups, not topic nodes): "CTFs (Capture the Flag)" → HackTheBox, TryHackMe,
VulnHub, picoCTF, SANS Holiday Hack Challenge; "Certifications" → Beginner Certifications (CompTIA A+,
CompTIA Linux+, CompTIA Network+, CCNA, CompTIA Security+) and Advanced Certifications (CEH, CISA,
CISM, GSEC, GPEN, GWAPT, GIAC, OSCP, CREST).
Scale: 373 nodes = 6 topics + 295 subtopics + 34 labels + sections/verticals. This roadmap is only
6 branches deep at level 1; everything else is level 2+.

## 2. roadmap.sh/ai-engineer
Read: `https://roadmap.sh/api/v1-official-roadmap/ai-engineer`; `https://roadmap.sh/ai-engineer`
(rendered); GitHub JSON at `deb9aaa…` (old 16-topic version). API `_id 68246b4711b0d89408504847`,
`updatedAt 2026-10-16T13:43:41.288Z`.

Top-level topic nodes (22, all yellow/core), in layout order (y position), split as on the canvas:
main spine: 1. Introduction; 2. How LLMs Work; 3. Prompt Engineering; 4. Context Engineering;
5. Type of Models; 6. Choosing the Right Model; 7. What are Embeddings; 8. Embedding Models;
9. Vector Databases; 10. What are RAGs?; 11. AI Agents; 12. Model Context Protocol (MCP);
13. AI Safety and Ethics; 14. LLM Observability; 15. LLM Evaluations; 16. Regression Testing;
17. Multimodal AI; 18. Development Tools.
Left "Platforms & Ecosystem" branch, sitting between "Choosing the Right Model" and
"Embeddings & Vector Databases": 19. Hugging Face; 20. Ollama; 21. LM Studio; 22. OpenRouter.
(Exact API label for 6 is "Choosing the Right Model " with a trailing space.)
Scale: 280 nodes = 22 topics + 168 subtopics.

## 3. roadmap.sh/ai-data-scientist
Read: `https://roadmap.sh/api/v1-official-roadmap/ai-data-scientist`;
`https://roadmap.sh/ai-data-scientist` (rendered); GitHub JSON at `deb9aaa…` (old 8-topic version).
API `_id 68246b4711b0d89408504850`, `updatedAt 2026-10-19T10:20:05.906Z`.

Top-level topic nodes (10, yellow/core), numbered on the canvas 1–10:
1. Mathematics
2. Statistics
3. Econometrics
4. Coding
5. Exploratory Data Analysis
6. Machine Learning
7. Deep Learning
8. MLOps
9. AI Engineering  (right-hand "Continue Learning" track, numbered 9)
10. Vibe Coding    (left-hand "Continue Learning" track, numbered 10)
Scale: 129 nodes; children are checkbox items + course boxes ("todo" type), not `subtopic` nodes.

## 4. roadmap.sh/data-analyst
Read: `https://roadmap.sh/api/v1-official-roadmap/data-analyst`; `https://roadmap.sh/data-analyst`
(rendered); GitHub JSON at `deb9aaa…` (same 14 topics, some renamed since). API
`_id 68246b4711b0d8940850484d`, `updatedAt 2026-10-08T14:57:10.940Z`.

Top-level topic nodes (14, all bright yellow/core, single column, in order):
1. Introduction
2. Types of Data Analytics
3. Excel
4. Learn a Language
5. Data Manipulation Lib's.
6. Data Viz. Libraries
7. Data Collection
8. Data Cleanup
9. Descriptive Analysis
10. Data Visualisation
11. Statistical Analysis
12. Machine Learning
13. Big Data Technologies
14. Deep Learning (Optional)  ← named "(Optional)" but rendered yellow/core
Scale: 156 nodes = 14 topics + 85 subtopics.

## 5. roadmap.sh/data-engineer (exists)
Read: `https://roadmap.sh/api/v1-official-roadmap/data-engineer`;
`https://roadmap.sh/data-engineer` (rendered). API `_id 689b4a029d7a0652aa4d5a46`,
`updatedAt 2026-10-09T08:12:57.882Z` (newer than the 2025-04 Git snapshot, where it did not exist).

Main spine (34 topic nodes, bright yellow, in vertical order):
1. Introduction
2. Data Engineering Lifecycle
3. Programming Skills
4. Data Structures & Algorithms
5. Git and GitHub
6. Linux Basics
7. Networking Fundamentals
8. Distributed Systems Basics
9. Sources of Data
10. Data Collection Ideas
11. Database Fundamentals
12. Relational Databases
13. NoSQL Databases
14. What is Data Warehouse?
15. Data Warehouse Architectures
16. Cloud Computing
17. Types of Data Ingestion
18. Data Pipelines
19. Cluster Computing Basics
20. Big Data Tools
21. Containers & Orchestration
22. CI/CD
23. Monitoring
24. Testing
25. Messaging Systems
26. Infrastructure as Code - IaC
27. Data Analytics
28. Business Intelligence
29. Reverse ETL
30. Authentication, Authorization
31. Encryption
32. Tokenization
33. Data Masking
34. Data Obfuscation

Side branch nodes (same y-band as their parent, off the spine):
- beside NoSQL Databases (grey = optional/alternative picks): Document, Column, Graph, Key-Value
- beside "What is Data Warehouse? / Data Warehouse Architectures": Data Warehouse (grey), Data Lake
  (grey), Data Mesh (beige sub-item)
Also: "Pre-requisites" panel (label) linking Python for Data Analysis and SQL Roadmap; label
"Python is recommended" over Python/Java/Scala/Go.
Scale: 258 nodes = 41 topics + 143 subtopics.

## 6. Embedded systems — m3y54m/Embedded-Engineering-Roadmap
Read: `https://api.github.com/repos/m3y54m/Embedded-Engineering-Roadmap`;
`https://raw.githubusercontent.com/m3y54m/Embedded-Engineering-Roadmap/master/README.md`.

Repo data: `stargazers_count` = **13,761**; `pushed_at` = **2026-11-01T09:14:43Z**;
forks 1,351; license CC-BY-SA-4.0; default branch `master`. (Latest commit sha not retrieved —
GitHub REST rate limit hit at the end.)

README structure: `# Embedded Systems Engineering Roadmap` → "What is an Embedded System?"
(definitions) → "The Roadmap" (interactive site https://m3y54m.github.io/Embedded-Engineering-Roadmap/,
roadmap split into three areas: SOFTWARE, HARDWARE, SOFT SKILLS) → "Don't Know Where to Start!"
(Projects; Search and Ask; Career Development; Courses and YouTube Contents; Arduino; Educational
Websites; Other Helpful Roadmaps; Development Environments) → "Learning Resources" → History/Copyright.

Main topic groups (the 25 `### ✳️` headings of "Learning Resources", in README order):
1. Soft Skills
2. Electronics
3. Using Test Equipment
4. Prototyping Skills
5. FPGA Development
6. Programming Fundamentals
7. Programming Languages
8. Microcontrollers
9. Interfaces, Protocols & Communication Technologies
10. Memory Technologies & File Systems
11. Hardware Simulation / Emulation
12. Sensors & Actuators
13. Digital Signal Processing
14. Control Theory
15. Operating Systems
16. Debugging
17. Build System
18. Software Development Life Cycle (SDLC) Models
19. Version Control Systems
20. Testing
21. Embedded Security
22. Embedded GUI
23. IoT (Internet of Things)
24. Edge AI
25. AUTOSAR Architecture
The README itself carries no required/recommended/optional flags; it says the priority highlighting
(required, recommended, optional) exists only in the interactive site.

---

## Failures / caveats (no guessing)
- GitHub REST API hit the unauthenticated rate limit after the first calls; the repo-metadata call for
  `developer-roadmap` (371,100 stars, pushed 2026-10-31) and the commit list succeeded, later calls
  (commit sha for the embedded repo) did not. `https://github.com/.../commit/<sha>.patch` returned 403.
- `https://roadmap.sh/roadmaps/<slug>.png` exports are **stale** for ai-engineer (still shows
  "OpenAI API", "OpenSource AI", "RAG & Implementation" which no longer exist) and truncated for
  ai-data-scientist; they were not used for the lists.
- Tavily MCP was not available in this sandbox; all fetches were `curl` + headless Edge
  (playwright-core 1.64.1, system msedge.exe).
- `v1-roadmap-tree-mapping/<id>` returned `[]`, so parent/child structure was derived from node type,
  canvas geometry and the rendered boxes, not from an explicit tree endpoint.
