# S.3.1 课程覆盖表

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | What is SQL injection? | `sql-boundary` |
| 1.2 | What is the impact of SQL injection? | `sql-boundary`, `sql-signals` |
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
| 2.5.1 | HTML sinks | `xss-paths`, `xss-output` |
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
| 3.2 | Authentication vs authorization | `login`, `policies` |
| 3.3 | How vulnerabilities arise | `login`, `mfa` |
| 3.4.1 | Brute-force attacks | `login` |
| 3.4.2 | Flaws in brute-force protection | `login` |
| 3.5.1 | Two-factor authentication tokens | `mfa` |
| 3.5.2 | Bypassing two-factor authentication | `mfa` |
| 3.6.1 | Keeping users logged in | `sessions` |
| 3.6.2 | Resetting user passwords | `recovery` |
| 3.6.3 | Changing user passwords | `recovery` |
| 3.7 | Vulnerabilities in OAuth authentication | `oauth`, `jwt` |
| 3.8 | Securing your authentication mechanisms | `login`, `mfa`, `sessions`, `recovery` |
| 4.1.1 | Vertical access controls | `policies` |
| 4.1.2 | Horizontal access controls | `policies`, `objects` |
| 4.1.3 | Context-dependent access controls | `policies`, `workflow` |
| 4.2.1 | Unprotected functionality | `workflow` |
| 4.2.2 | Parameter-based access control | `policies`, `workflow` |
| 4.2.3 | Platform misconfiguration | `workflow` |
| 4.2.4 | URL-matching discrepancies | `workflow` |
| 4.3 | Horizontal privilege escalation | `objects` |
| 4.4 | Horizontal to vertical privilege escalation | `objects` |
| 4.5.1 | Direct references to database objects | `objects` |
| 4.6 | Vulnerabilities in multi-step processes | `workflow` |
| 4.7 | Vulnerabilities in Referer-based controls | `workflow` |
| 4.8 | Preventing | `policies`, `objects`, `workflow` |
| 5.1 | API recon | `inventory` |
| 5.2.1 | Discovering API documentation | `inventory` |
| 5.2.2 | Using machine-readable API documentation | `inventory` |
| 5.3 | Identifying API endpoints | `inventory` |
| 5.4.1 | Identifying supported HTTP methods | `inventory` |
| 5.4.2 | Identifying supported content types | `inventory` |
| 5.4.3 | Finding hidden parameters | `inventory`, `api-fields` |
| 5.5.1 | Testing mass assignment vulnerabilities | `api-fields` |
| 5.5.2 | Preventing vulnerabilities in APIs | `api-fields`, `api-risk` |
| 5.6.1 | Testing the query string | `api-fields` |
| 5.6.2 | Overriding existing parameters | `api-fields` |
| 5.6.3 | Testing structured data formats | `api-fields` |
| 5.6.4 | Preventing server-side parameter pollution | `api-fields` |
| 5.7 | Alignment with the OWASP Top 10 API vulnerabilities | `api-risk` |
| 6 | Same Origin Policy | `browser-boundary` |
| 7 | Cookies and Sessions | `sessions` |
| 8 | Session attacks, Cross-Site Request Forgery | `sessions`, `csrf` |

## CS2023、双语材料与综合练习

- SEC-Coding 的输入验证和净化见 `sql-boundary`、`xss-output`、`files-parsers`、`api-fields`，XSS 机制和缓解见 `xss-paths`、`xss-output`。SEC-Foundations 的身份核验和授权概念、访问控制模型分别见 `login`、`mfa`、`sessions`、`policies` 和 `objects`。必修前置 P.5.1 的 HTTP、会话、CORS 与 OIDC 知识可直接承接。[PortSwigger Web Security Academy](https://portswigger.net/web-security) · [Stanford CS253](https://web.stanford.edu/class/cs253/)
- 原题 1 的 SQL 注入、三类 XSS、CSRF 见 `sql-boundary`、`sql-signals`、`xss-paths`、`xss-output`、`csrf`。原题 2 见 `sessions`、`recovery`，区分 Lax 的顶层安全方法导航例外与令牌检查。原题 3 的对象权限以当前主体和对象共同过滤，并用双用户测试核对。[OWASP SQL 注入](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html) · [OWASP XSS](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html) · [OWASP CSRF](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html) · [OWASP 会话管理](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- 原题 4 的 PKCE 与 JWT 见 `oauth`、`jwt`，原题 5 的云元数据、解析与真实目标绑定见 `ssrf`。这几节属于技能学习路径和综合练习的补充。`files-parsers` 和 `interfaces` 将路径、上传、SSTI、XXE、GraphQL、SOAP、WebSocket、请求走私和缓存风险放进同一信任边界视角。[OAuth 安全最佳实践](https://www.rfc-editor.org/rfc/rfc9700) · [JWT 最佳实践](https://www.rfc-editor.org/rfc/rfc8725) · [OWASP SSRF](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html) · [OWASP API 安全十大风险](https://owasp.org/API-Security/)
