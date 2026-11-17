# P.5.1 互联网与 Web 开发：覆盖表

**状态（2026-11-17）：已写完。** 依据 `../cs-math-skill-tree/data/outlines/P.5.1.json` 与 `../cs-math-skill-tree/output/outlines.json`，主来源为 MDN *Learn web development (2025)* 与 MDN HTTP 指南（Authentication、Cookies、CORS）；补充参考 OWASP Authentication Cheat Sheet 与阮一峰 OAuth 2.0 教程。游戏内部章序：`1. HTTP应用`、`2. 前后端`、`3. API`、`4. 浏览器`、`5. 服务端`、`6. 认证集成与可访问性`。

必须前置仅为 `P.1.1 程序设计基础`：可直接假设 Python 基础、字符串、字典、列表、函数、JSON 读写与异常，其余 DNS/HTTP/URL、HTML/CSS/JS、DOM/浏览器渲染、React、Fetch/Promise、同源策略、CORS、Cookie/Session、JWT/OAuth2 PKCE 与可访问性均在本包从零讲清。

`node scripts/check-coverage.mjs P.5.1` 自动检查本表。

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | A How the web works | `web-trip` |
| 1.2 | A The web standards model | `web-trip` |
| 1.3 | A How browsers load websites | `web-trip`、`perf-render` |
| 2.1 | A Basic HTML syntax | `html-forms` |
| 2.2 | A Structuring documents | `html-forms` |
| 2.3 | A Creating links | `html-forms` |
| 2.4 | A Images | `html-forms`、`accessible-media` |
| 2.5 | A Forms and buttons | `html-forms`、`forms-validation` |
| 3.1 | A What is CSS? | `css-box` |
| 3.2 | A CSS getting started | `css-box` |
| 3.3 | A Basic selectors | `css-box` |
| 3.4 | A Box model | `css-box` |
| 3.5 | A Handling conflicts | `css-box` |
| 3.6 | A Values and units | `css-box` |
| 4.1 | A Introduction (CSS layout) | `css-layout` |
| 4.2 | A Flexbox | `css-layout` |
| 4.3 | A CSS grid layout | `css-layout` |
| 4.4.1 | A Media queries | `css-layout` |
| 5.1 | A What is JavaScript? | `js-dom` |
| 5.2 | A JavaScript walkthrough | `js-dom` |
| 5.3 | A Variables | `js-dom` |
| 5.4 | A Functions | `js-dom` |
| 5.5 | A Events | `js-dom` |
| 5.6 | A Objects | `js-dom` |
| 5.7 | A DOM scripting | `js-dom` |
| 5.8 | A Network requests | `async-fetch` |
| 5.9 | A JSON | `rest-http`、`async-fetch` |
| 5.10 | A Debugging and error handling | `async-fetch` |
| 6.1 | A Introduction (Frameworks) | `react-components` |
| 6.2 | A Framework features | `react-components` |
| 6.3 | A React getting started | `react-components` |
| 6.4 | A React components | `react-components` |
| 6.5 | A React events and state | `react-components` |
| 7.1 | A What is accessibility? | `a11y-basics` |
| 7.2 | A Accessibility tools | `a11y-basics` |
| 7.3 | A Accessible HTML | `a11y-basics` |
| 7.4 | A Accessible CSS and JS | `a11y-basics` |
| 7.5 | A WAI-ARIA | `accessible-media` |
| 7.6 | A Mobile accessibility | `accessible-media` |
| 8.1 | A Introduction (Client-side web APIs) | `storage-origins` |
| 8.2 | A Client-side storage | `storage-origins` |
| 8.3 | A Third-party APIs | `storage-origins` |
| 9.1 | A Introduction (Async JS) | `async-fetch` |
| 9.2 | A Using promises | `async-fetch` |
| 9.3 | A Implementing promise-based APIs | `async-fetch` |
| 9.4 | A Introducing workers | `perf-render` |
| 10.1 | A Your first form | `forms-validation` |
| 10.2 | A Sending form data | `forms-validation` |
| 10.3 | A Client-side form validation | `forms-validation` |
| 11.1 | A Overview (Client-side tools) | `frontend-toolchain` |
| 11.2 | A Package management | `frontend-toolchain` |
| 11.3 | A Sample toolchain | `frontend-toolchain` |
| 11.4 | A Deploying our app | `frontend-toolchain` |
| 12.1.1 | A Introduction (Server-side) | `server-basics` |
| 12.1.2 | A Client-server overview | `server-basics` |
| 12.1.3 | A Server-side frameworks | `server-basics` |
| 12.1.4 | A Website security | `server-security` |
| 12.2.1 | A Django introduction | `server-basics` |
| 12.2.2 | A Sessions framework | `sessions-cookies` |
| 12.2.3 | A Authentication and permissions | `sessions-cookies`、`oauth-jwt` |
| 12.2.4 | A Django security | `server-security` |
| 12.2.5 | A Deploying | `frontend-toolchain` |
| 12.3.1 | A Express/Node introduction | `server-basics` |
| 12.3.2 | A Routes and controllers | `server-basics` |
| 12.3.3 | A Deploying | `frontend-toolchain` |
| 13.1 | B General HTTP authentication framework | `http-auth-cors` |
| 13.2 | B Authentication schemes | `http-auth-cors` |
| 13.3 | B Basic authentication scheme | `http-auth-cors` |
| 14.1 | B What cookies are used for | `sessions-cookies` |
| 14.2 | B Creating, removing, and updating cookies | `sessions-cookies` |
| 14.3 | B Cookie Security | `sessions-cookies` |
| 14.4 | B Cookie Privacy and tracking | `sessions-cookies` |
| 15.1 | B What requests use CORS? | `http-auth-cors` |
| 15.2 | B Functional overview | `http-auth-cors` |
| 15.3 | B The HTTP response headers | `http-auth-cors` |

## CS2023 核心主题（C2）

| 主题 | KA / 要求 | 课 |
|---|---|---|
| application-layer protocols (e.g., HTTP) | NC-Applications · CS Core | `web-trip`、`rest-http`、`http-auth-cors` |
| Web platforms, frameworks, or meta-frameworks | SPD-Web · KA Core | `react-components`、`frontend-toolchain`、`server-basics` |
| API, Web Components | SPD-Web · KA Core | `rest-http`、`async-fetch`、`storage-origins` |
| Web standards such as document object model | SPD-Web · KA Core | `html-forms`、`css-box`、`css-layout`、`js-dom` |
| Software as a Service (SaaS) | SPD-Web · KA Core | `server-basics`、`sessions-cookies` |
| Security and Privacy Considerations | SPD-Web · KA Core | `server-security`、`sessions-cookies`、`http-auth-cors`、`oauth-jwt`、`a11y-basics` |

## 学习资源的章节（C3）

| 来源 | 章节与概念 | 课 / 说明 |
|---|---|---|
| `en1` / `zh1` MDN Learn Web Development | Web 标准、HTML/表单、CSS 盒模型/Flex/Grid/媒体查询、JS/DOM/事件/Promise/Worker、React、工具链、Django/Express 服务端 | 对应 `web-trip` 到 `server-security`、`a11y-basics`、`accessible-media` |
| `r7-zh1` / `r7-en1` MDN Client-side Web APIs | DOM、Fetch、Web Storage（localStorage/sessionStorage）与第三方 API | `js-dom`、`async-fetch`、`storage-origins` |
| `r7-zh2` / `r7-en2` MDN Accessibility | 语义化 HTML、键盘聚焦、颜色对比度、WAI-ARIA 与移动端无障碍 | `a11y-basics`、`accessible-media` |
| MDN HTTP Guides / `r7-zh3` / `r7-en3` | HTTP Basic/Bearer 认证、Cookie 属性与隐私、CORS 预检、OAuth 2.0 PKCE、OWASP 认证校验 | `http-auth-cors`、`sessions-cookies`、`oauth-jwt` |

## 综合练习（C4）

| 小题 | 要用到的 | 课 |
|---|---|---|
| (1) 从输入 URL 到浏览器显示页面的完整流程 | DNS 解析 → TCP/TLS 建连 → HTTP 请求/响应 → HTML/CSSOM/DOM/JS 解析与渲染 | `web-trip`、`perf-render` |
| (2) 最小 HTML+JS fetch `GET /api/greet?name=` 与 Flask 后端实现 | 表单与 `URLSearchParams`、`textContent` 防 XSS、Flask 路由与参数校验返回 200/400 JSON | `html-forms`、`js-dom`、`async-fetch`、`server-basics`、`server-security` |
| (3) GET vs POST、状态码 `200/201/301/304/400/401/403/404/500`、REST 删除 | 方法语义与幂等性、条件缓存 304、`DELETE /api/items/5` | `rest-http` |
| (4) Cookie+Session vs JWT、同源策略、CORS | 服务端状态与无状态签名令牌对比、协议+域名+端口三元组、`Access-Control-Allow-Origin` 与预检 | `storage-origins`、`sessions-cookies`、`http-auth-cors`、`oauth-jwt` |
| (5) 三种首屏渲染与性能加载优化 | 脚本 `defer`/`async` 防阻塞、强缓存与 ETag `304`、资源压缩/图片懒加载/Web Worker 拆重活 | `perf-render` |

## 后继技能（C5）

必须后继为 `S.3.1 应用、Web 与 API 安全`。本包在 `server-security`、`sessions-cookies`、`http-auth-cors` 与 `oauth-jwt` 中提前讲透：`HttpOnly` / `Secure` / `SameSite=Lax|Strict` 会话 Cookie 属性、参数化查询与 `textContent` 防注入/XSS、对象级归属权（IDOR/BOLA）校验直觉、OAuth 2.0 授权码 + PKCE（`code_verifier`/`code_challenge`）、以及 JWT 常见陷阱（`alg=none`、校验 `exp`/`iss`/`aud`、不放敏感到 payload、警惕 `localStorage` 遇 XSS 失窃），保证 `S.3.1` 无缝衔接。
