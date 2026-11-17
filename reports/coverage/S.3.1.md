# S.3.1 应用、Web与API安全：覆盖表

**状态（2026-11-17）：已写完。** 依据 `../cs-math-skill-tree/data/outlines/S.3.1.json`、`../cs-math-skill-tree/output/outlines.json` 与 `../cs-math-skill-tree/data/learning-paths/S.3.1.json`，主来源为 PortSwigger *Web Security Academy* 与 Stanford *CS 253 Web Security*，并对齐 `P.5.1` 必修前置、`S.3.1` 综合练习 5 问及本地 Python 验证脚本 `tests/content/S.3.1.verify.py`。

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | What is SQL injection? | `sql-boundary` |
| 1.2 | What is the impact of SQL injection? | `sql-boundary`、`sql-signals` |
| 1.3.1 | In different parts of the query | `sql-boundary` |
| 1.3.2 | In different contexts | `sql-boundary` |
| 1.4.1 | Retrieving hidden data | `sql-signals` |
| 1.4.2 | Subverting application logic | `sql-signals` |
| 1.4.3 | Retrieving data from other tables | `sql-signals` |
| 1.4.4 | Examining the database | `sql-signals` |
| 1.4.5 | Second-order SQL injection | `sql-signals` |
| 1.5.1 | Determining the number of columns | `sql-signals` |
| 1.5.2 | Retrieving interesting data | `sql-signals` |
| 1.6.1 | What is blind SQL injection? | `sql-signals` |
| 1.6.2 | Triggering conditional responses | `sql-signals` |
| 1.7.1 | Extracting data via verbose error messages | `sql-signals` |
| 1.7.2 | Triggering time delays | `sql-signals` |
| 1.7.3 | Out-of-band (OAST) techniques | `sql-signals` |
| 1.8 | How to prevent SQL injection | `sql-boundary` |
| 2.1 | What is XSS? | `xss-paths` |
| 2.2 | How does XSS work? | `xss-paths` |
| 2.3 | Reflected XSS | `xss-paths` |
| 2.4 | Stored XSS | `xss-paths` |
| 2.5.1 | HTML sinks | `xss-paths`、`xss-output` |
| 2.5.2 | JavaScript execution sinks | `xss-paths` |
| 2.6.1 | Between HTML tags | `xss-output` |
| 2.6.2 | In HTML tag attributes | `xss-output` |
| 2.6.3 | JavaScript | `xss-output` |
| 2.7 | Content security policy (CSP) | `xss-output` |
| 2.8.1 | Encode data on output | `xss-output` |
| 2.8.2 | Validate input on arrival | `xss-output` |
| 2.8.3 | Whitelisting vs blacklisting | `xss-output` |
| 2.8.4 | Using a template engine | `xss-output` |
| 3.1 | What is authentication? | `login` |
| 3.2 | Authentication vs authorization | `login`、`policies` |
| 3.3 | How vulnerabilities arise | `login`、`mfa` |
| 3.4.1 | Brute-force attacks | `login` |
| 3.4.2 | Flaws in brute-force protection | `login` |
| 3.5.1 | Two-factor authentication tokens | `mfa` |
| 3.5.2 | Bypassing two-factor authentication | `mfa` |
| 3.6.1 | Keeping users logged in | `sessions` |
| 3.6.2 | Resetting user passwords | `recovery` |
| 3.6.3 | Changing user passwords | `recovery` |
| 3.7 | Vulnerabilities in OAuth authentication | `oauth`、`jwt` |
| 3.8 | Securing your authentication mechanisms | `login`、`mfa`、`sessions`、`recovery` |
| 4.1.1 | Vertical access controls | `policies` |
| 4.1.2 | Horizontal access controls | `policies`、`objects` |
| 4.1.3 | Context-dependent access controls | `policies`、`workflow` |
| 4.2.1 | Unprotected functionality | `workflow` |
| 4.2.2 | Parameter-based access control | `policies`、`workflow` |
| 4.2.3 | Platform misconfiguration | `workflow` |
| 4.2.4 | URL-matching discrepancies | `workflow` |
| 4.3 | Horizontal privilege escalation | `objects` |
| 4.4 | Horizontal to vertical privilege escalation | `objects` |
| 4.5.1 | Direct references to database objects | `objects` |
| 4.6 | Vulnerabilities in multi-step processes | `workflow` |
| 4.7 | Vulnerabilities in Referer-based controls | `workflow` |
| 4.8 | Preventing | `policies`、`objects`、`workflow` |
| 5.1 | API recon | `inventory` |
| 5.2.1 | Discovering API documentation | `inventory` |
| 5.2.2 | Using machine-readable API documentation | `inventory` |
| 5.3 | Identifying API endpoints | `inventory` |
| 5.4.1 | Identifying supported HTTP methods | `inventory` |
| 5.4.2 | Identifying supported content types | `inventory` |
| 5.4.3 | Finding hidden parameters | `inventory`、`api-fields` |
| 5.5.1 | Testing mass assignment vulnerabilities | `api-fields` |
| 5.5.2 | Preventing vulnerabilities in APIs | `api-fields`、`api-risk` |
| 5.6.1 | Testing the query string | `api-fields` |
| 5.6.2 | Overriding existing parameters | `api-fields` |
| 5.6.3 | Testing structured data formats | `api-fields` |
| 5.6.4 | Preventing server-side parameter pollution | `api-fields` |
| 5.7 | Alignment with the OWASP Top 10 API vulnerabilities | `api-risk` |
| 6 | Same Origin Policy | `browser-boundary` |
| 7 | Cookies and Sessions | `sessions` |
| 8 | Session attacks, Cross-Site Request Forgery | `sessions`、`csrf` |

## CS2023 核心主题（C2）

`scope.json` 在 `S.3.1` 的 4 个知识点中 4/4 全匹配 CS2023 核心主题：

| 知识点 | KA / 要求 | 课 |
|---|---|---|
| 输入输出边界 | SEC-Coding · CS Core（Input validation and data sanitization） | `sql-boundary`、`xss-output`、`files-parsers`、`api-fields` |
| 认证会话 | SEC-Foundations · CS Core（Basic concepts of authentication and authorization/access control） | `login`、`mfa`、`sessions`、`recovery`、`csrf`、`oauth`、`jwt` |
| 访问控制 | SEC-Foundations · KA Core（Access control models） | `policies`、`objects`、`workflow` |
| 服务端/客户端与接口安全 | SEC-Coding · CS Core（Cross-site scripting techniques and mitigations） | `xss-paths`、`xss-output`、`inventory`、`browser-boundary`、`interfaces`、`api-risk` |

## 综合练习、补充专题与后继状态（C3 / C4 / C5）

- **综合练习 5 问映射**：(1) SQL 注入、三类 XSS（反射型/存储型/DOM 型）及 CSRF 原理与标准防御 → `sql-boundary`、`sql-signals`、`xss-paths`、`xss-output`、`csrf`；(2) 会话 Cookie `HttpOnly` / `Secure` / `SameSite=Lax|Strict` 与常见找回漏洞（令牌可测/不失效/复用、账号枚举、Host 头注入、改密不踢旧会话）→ `sessions`、`recovery`；(3) `GET /api/orders/123` 仅验登录属 IDOR/BOLA 越权，须结合当前主体属主共同过滤 `WHERE id = ? AND user_id = ?` 并做双用户隔离验证 → `objects`、`policies`；(4) OAuth 2.0 授权码 + PKCE（RFC 7636 `code_verifier` / `code_challenge` 防截获重放）及 JWT 常见陷阱（`alg=none`、算法混淆、漏验 `exp`/`aud`/`iss`、payload 明文非加密、`localStorage` + XSS）→ `oauth`、`jwt`；(5) SSRF（未列入大纲但属 C4 必考题）利用 `169.254.169.254` 云元数据窃取临时凭证及五重防御（白名单、DNS 解析后校验阻断回环/私网/链路本地、禁用重定向、独立受限出口网、IMDSv2）→ `ssrf`。
- **大纲外但随学习路径补充的课**：除 `ssrf` 外，`files-parsers` 与 `interfaces` 补充路径穿越、上传校验、模板/XXE 解析及 GraphQL/WebSocket/请求走私/缓存边界，不虚增表格行。
- **后继与前置状态（C3 / C5）**：承接必修前置 `P.5.1`（HTTP、Cookie、CORS、同源与 JWT 基础）；`S.3.1` 无强依赖下游（`unlocks: []`），作为推荐前置服务 `S.4.1`（渗透测试）及 `A.4.3`（LLM 应用安全边界）。
