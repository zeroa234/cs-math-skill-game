# P.5.1 课程覆盖表

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | How the web works | `web-trip` |
| 1.2 | The web standards model | `web-trip` |
| 1.3 | How browsers load websites | `web-trip`, `render` |
| 2.1 | Basic HTML syntax | `html` |
| 2.2 | Structuring documents | `html` |
| 2.3 | Creating links | `html` |
| 2.4 | Images | `html`, `accessible-media` |
| 2.5 | Forms and buttons | `forms` |
| 3.1 | What is CSS? | `style` |
| 3.2 | CSS getting started | `style` |
| 3.3 | Basic selectors | `style` |
| 3.4 | Box model | `style` |
| 3.5 | Handling conflicts | `style` |
| 3.6 | Values and units | `style` |
| 4.1 | Introduction | `layout` |
| 4.2 | Flexbox | `layout` |
| 4.3 | CSS grid layout | `layout` |
| 4.4.1 | Media queries | `layout` |
| 5.1 | What is JavaScript? | `javascript` |
| 5.2 | JavaScript walkthrough | `javascript`, `dom` |
| 5.3 | Variables | `javascript` |
| 5.4 | Functions | `javascript` |
| 5.5 | Events | `javascript`, `dom` |
| 5.6 | Objects | `javascript` |
| 5.7 | DOM scripting | `dom` |
| 5.8 | Network requests | `fetch` |
| 5.9 | JSON | `rest`, `fetch` |
| 5.10 | Debugging and error handling | `javascript`, `fetch` |
| 6.1 | Introduction | `react` |
| 6.2 | Framework features | `react` |
| 6.3 | React getting started | `react`, `toolchain` |
| 6.4 | React components | `react` |
| 6.5 | React events and state | `react` |
| 7.1 | What is accessibility? | `accessibility` |
| 7.2 | Accessibility tools | `accessibility` |
| 7.3 | Accessible HTML | `accessibility`, `forms` |
| 7.4 | Accessible CSS and JS | `accessibility` |
| 7.5 | WAI-ARIA | `accessibility` |
| 7.6 | Mobile accessibility | `accessible-media` |
| 8.1 | Introduction | `fetch`, `dom` |
| 8.2 | Client-side storage | `storage` |
| 8.3 | Third-party APIs | `origins` |
| 9.1 | Introduction | `async` |
| 9.2 | Using promises | `async`, `fetch` |
| 9.3 | Implementing promise-based APIs | `async` |
| 9.4 | Introducing workers | `async`, `storage` |
| 10.1 | Your first form | `forms` |
| 10.2 | Sending form data | `forms`, `greet-server` |
| 10.3 | Client-side form validation | `forms`, `server-data` |
| 11.1 | Overview | `toolchain` |
| 11.2 | Package management | `toolchain` |
| 11.3 | Sample toolchain | `toolchain` |
| 11.4 | Deploying our app | `toolchain`, `server-data` |
| 12.1.1 | Introduction | `greet-server` |
| 12.1.2 | Client-server overview | `web-trip`, `greet-server` |
| 12.1.3 | Server-side frameworks | `server-data` |
| 12.1.4 | Website security | `server-data`, `sessions` |
| 12.2.1 | Django introduction | `server-data` |
| 12.2.2 | Sessions framework | `server-data`, `sessions` |
| 12.2.3 | Authentication and permissions | `server-data`, `sessions` |
| 12.2.4 | Django security | `server-data` |
| 12.2.5 | Deploying | `server-data` |
| 12.3.1 | Express/Node introduction | `server-data` |
| 12.3.2 | Routes and controllers | `server-data`, `greet-server` |
| 12.3.3 | Deploying | `server-data` |
| 13.1 | The general HTTP authentication framework | `sessions` |
| 13.2 | Authentication schemes | `sessions`, `oidc` |
| 13.3 | Basic authentication scheme | `sessions` |
| 14.1 | What cookies are used for | `sessions` |
| 14.2 | Creating, removing, and updating cookies | `sessions` |
| 14.3 | Security | `sessions`, `oidc` |
| 14.4 | Privacy and tracking | `sessions` |
| 15.1 | What requests use CORS? | `origins` |
| 15.2 | Functional overview | `origins` |
| 15.3 | The HTTP response headers | `origins` |

## CS2023、学习资源与综合练习

- CS2023 的 NC-Applications 应用层协议对应 `web-trip`、`messages`、`cache`。SPD-Web 的平台和框架见 `react`、`toolchain`，API 见 `rest`、`fetch`，DOM 与 Web Components 见 `dom`，SaaS 见 `server-data`，安全和隐私见 `origins`、`sessions`、`oidc`。原综合练习 1 和 3 由 HTTP 三课及 `render` 衔接。[MDN HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP) · [MDN Web Components](https://developer.mozilla.org/en-US/docs/Web/API/Web_components)
- 原综合练习 2 的完整问好页面由 `html`、`forms`、`fetch`、`dom` 和 `greet-server` 拼成一套同源示例。包含 URL 查询编码、JSON 响应和安全的文本插入。React 负责同一类界面状态练习；Tailwind、Express 和 Django 在工具链或服务端课中讲清各自负责的层，深入框架项目留给读者按原教材实践。[MDN 学习 Web 开发](https://developer.mozilla.org/zh-CN/docs/Learn_web_development) · [Flask 快速入门](https://flask.palletsprojects.com/en/stable/quickstart/)
- 原综合练习 4 的 Cookie、会话、JWT、同源和 CORS 在 `sessions`、`oidc`、`origins`。OAuth 授权和 OIDC 身份核验分开讲，加入 PKCE 和令牌核验，供 S.3.1 的 PKCE、JWT 与对象权限练习承接。Cookie 属性与服务端权限也为该技能的安全问题打基础。[OWASP 认证指南](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html) · [OpenID Connect Core](https://openid.net/specs/openid-connect-core-1_0.html) · [MDN CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS)
- 原综合练习 5 的首屏优化由 `cache`、`render` 覆盖。键盘、语义结构、动态状态提示、对比度、字幕和触屏测试见 `accessibility`、`accessible-media`。HTML 基础先给原生控件，ARIA 留在原生语义和焦点之后。[MDN 可访问性](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility)
