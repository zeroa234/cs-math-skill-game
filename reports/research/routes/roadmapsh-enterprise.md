# roadmap.sh — top-level topics: java / software-design-architecture / aspnet-core

Captured 2026-11-03 (server `Date: Tue, 03 Nov 2026 04:47 GMT`). All data below was read in this session; nothing is from memory.

## Sources read

| # | URL | Result |
|---|-----|--------|
| 1 | `https://roadmap.sh/api/v1-official-roadmap/java` | 200, 92,458 B |
| 2 | `https://roadmap.sh/api/v1-official-roadmap/software-design-architecture` | 200, 70,170 B |
| 3 | `https://roadmap.sh/api/v1-official-roadmap/aspnet-core` | 200, 126,741 B |
| 4 | `https://roadmap.sh/java` (headless MS Edge 142 via `playwright-core` 1.64.1) | rendered, 88 nodes |
| 5 | `https://roadmap.sh/software-design-architecture` (same) | rendered, 94 nodes |
| 6 | `https://roadmap.sh/aspnet-core` (same) | rendered, 146 nodes |
| 7 | `https://roadmap.sh/assets/index-Crg3WLyO.js` (bundle loaded by roadmaps 4–6) | colour palette, quoted below |

Re-fetched all three API records with a cache-buster: `updatedAt` and node counts identical (stable).
Rendered SVG node counts equal API node counts exactly (20+68=88, 13+81=94, 26+120=146) → nothing hidden/collapsed.

## API record metadata

| roadmap | `updatedAt` | `createdAt` | nodes |
|---|---|---|---|
| java (page title "Java Developer") | `2026-01-27T13:57:35.172Z` | 2025-05-14 | 20 topic / 68 subtopic |
| software-design-architecture | `2025-09-12T12:38:05.654Z` | 2025-06-16 | 13 topic / 81 subtopic |
| aspnet-core (page title "ASP.NET Core Developer") | `2026-09-14T11:34:19.617Z` | 2025-05-14 | 26 topic / 120 subtopic |

## How "core vs optional" is actually encoded (important caveat)

Fill colour is **not** set by core/optional; it comes from a per-node `data.style.colorType` letter mapped in the site bundle (`index-Crg3WLyO.js`, ~offset 221309) as:

`a #333333 · b #fdff00 (bright yellow = default) · c #ffe599 · d #C6F6D5 · e #a8caff · f #CBCBCB · g #FED7E2 (pink) · h #F4F4F4 (light grey)`

Default when `colorType` is absent is `b` = `#fdff00`. In the rendered SVG the topic `<rect fill>` matches this exactly.

Semantic markers are a separate system: a `legend` node plus a per-node `data.legend` tag; the rendered page draws a 9.5 px coloured dot at the node edge for tagged nodes (verified pixel-for-pixel: dot at `(772.3,502.4)` = node "Triggers" tagged *Alternative Options*; `(-281.3,590.8)` = "Razor Pages" tagged *Alternative Options*).

- java and software-design-architecture: **no** legend node, **no** legend tags, **no** dots → the only signal is fill colour (yellow vs grey), which is what the task's heuristic relies on.
- aspnet-core: legend defined, 3 categories:
  `#2b78e4` "Personal Recommendation / Opinion" · `#6d7500` "Alternative Options" · `#999999` "Optional / Learn anytime".

Where the two signals disagree (aspnet-core only), both are reported.

## 1. java — 20 top-level topics (ordered by y, x tie-break)

1. Learn the Basics
2. Exception Handling
3. Lambda Expressions
4. Annotations
5. Modules
6. Optionals
7. Cryptography
8. Dependency Injection
9. Date and Time
10. Networking
11. Regular Expressions
12. I/O Operations
13. Concurrency
14. File Operations
15. Database Access
16. Web Frameworks
17. Build Tools
18. Documentation
19. Logging Frameworks
20. Testing

Marking: **all 20 render `#fdff00` with no `colorType` and no legend** → none optional/alternative; the whole top level is core.

## 2. software-design-architecture — 13 top-level topics

1. Clean Code Principles
2. Programming Paradigms
3. Object Oriented Programming
4. Design Principles
5. Design Patterns
6. Model-Driven Design
7. Messaging
8. Distributed
9. Architectural Styles
10. Architectural Principles
11. Structural
12. Architectural Patterns
13. Enterprise Patterns

Marking:
- Core (yellow `#fdff00`, no `colorType`): 1–5, 9, 10, 12, 13.
- Non-core, `colorType: "h"` → rendered `#F4F4F4` light grey (per the site convention: alternative/optional), **no legend in this roadmap to name it**: **Model-Driven Design, Messaging, Distributed, Structural**.

## 3. aspnet-core — 26 top-level topics

| # | topic | fill (`colorType`) | legend tag |
|---|---|---|---|
| 1 | Learn the Basics of C# | `#fdff00` (–) | – |
| 2 | General Development Skills | `#fdff00` (–) | – |
| 3 | ASP.NET Core Basics | `#fdff00` (–) | – |
| 4 | Database Fundamentals | `#fdff00` (–) | Personal Recommendation / Opinion |
| 5 | Object Relational Mapping | `#fdff00` (–) | – |
| 6 | Caching | `#fdff00` (–) | – |
| 7 | Dependency Injection | `#fdff00` (–) | – |
| 8 | Life Cycles | `#FED7E2` (g) | Personal Recommendation / Opinion |
| 9 | DI Containers | `#F4F4F4` (h) | Personal Recommendation / Opinion |
| 10 | Search Engines | `#fdff00` (–) | **Alternative Options** |
| 11 | Cloud | `#fdff00` (–) | **Alternative Options** |
| 12 | Databases | `#fdff00` (–) | – |
| 13 | Relational | `#fdff00` (–) | Personal Recommendation / Opinion |
| 14 | NoSQL | `#fdff00` (–) | **Alternative Options** |
| 15 | Log Frameworks | `#fdff00` (–) | – |
| 16 | GraphQL | `#FED7E2` (g) | **Alternative Options** |
| 17 | REST | `#FED7E2` (g) | Personal Recommendation / Opinion |
| 18 | API Clients and Communication | `#fdff00` (–) | – |
| 19 | Real-Time Communication | `#fdff00` (–) | – |
| 20 | Object Mapping | `#fdff00` (–) | – |
| 21 | Task Scheduling | `#fdff00` (–) | – |
| 22 | Testing | `#fdff00` (–) | – |
| 23 | Microservices | `#fdff00` (–) | – |
| 24 | CI / CD | `#fdff00` (–) | – |
| 25 | Template Engines | `#fdff00` (–) | – |
| 26 | Frameworks | `#fdff00` (–) | – |

Marked optional/alternative (by legend tag, the roadmap's own wording):
- **Alternative Options (4):** Search Engines, Cloud, NoSQL, GraphQL.
- **Optional / Learn anytime (0 at top level).**
- Top-level tags "Personal Recommendation / Opinion" (5): Database Fundamentals, Life Cycles, DI Containers, Relational, REST.

Marked non-core **by colour only** (differs from the tag list): `#F4F4F4` grey = **DI Containers**; pink `#FED7E2` = Life Cycles, REST, GraphQL. Note the contradictions: Search Engines / Cloud / NoSQL are tagged *Alternative Options* yet render core-yellow, and DI Containers renders grey yet is tagged *Personal Recommendation / Opinion*. For this roadmap the dot tag, not the fill, is the author's semantic marker.

## Failures / not verified
- GitHub API was rate-limited (HTTP 403 `API rate limit exceeded`) and raw-path guesses under `nilbuild/developer-roadmap` returned 404, so the repo content was **not** consulted; all findings come from the live API + rendered pages + the site's JS bundle.
- `updatedAt` is the API's DB field; no independent git commit cross-check was possible.
- Headless render used `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`; `waitUntil:'networkidle'` times out on these pages (ads), so `domcontentloaded` + explicit selector wait was used.
