# S.2.3 移动应用与设备安全：覆盖表

**状态（2026-11-18）：已写完（v2 重写，按零基础与知识覆盖面标准重写）。** 依据 `../cs-math-skill-tree/data/outlines/S.2.3.json`、`output/outlines.json`、`../cs-math-skill-tree/data/curation/learning-paths/S.2.3.json`，主来源为 OWASP Mobile Application Security（MASVS v2 / MASTG），辅以 AOSP 官方中文文档（应用沙盒、硬件支持密钥库 Keystore、文件级加密 FBE、网络安全配置 `networkSecurityConfig`）、Android 开发者安全指南（`android:exported`）及 Apple 开发者文档（App Sandbox / Keychain Services / ATS）以及微软中文威胁建模指南，对齐 `S.2.3` 综合练习 3 问，本地核对脚本 `tests/content/S.2.3.verify.py`（Python 3 + XML 校验 + 本地 OpenSSL 真实 X.509 信任来源与主机名校验实测）。

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | Storage | `storage` |
| 1.2 | Cryptography | `crypto` |
| 1.3 | Authentication and Authorization | `identity`、`permissions` |
| 1.4 | Network Communication | `tls` |
| 1.5 | Platform Interaction | `ipc` |
| 1.6 | Code Quality | `build` |
| 1.7 | Resilience Against Reverse Engineering and Tampering | `resilience` |
| 1.8 | Privacy | `privacy` |
| 2.1 | Mobile Application Taxonomy | `sandbox` |
| 2.2 | Mobile Application Security Testing | `test` |
| 2.3 | Mobile App Tampering and Reverse Engineering | `resilience` |
| 2.4 | Mobile App Authentication Architectures | `identity`、`permissions` |
| 2.5 | Mobile App Network Communication | `tls` |
| 2.6 | Mobile App Cryptography | `crypto` |
| 2.7 | Mobile App Code Quality | `build` |
| 2.8 | Mobile App User Privacy Protection | `privacy` |
| 3.1 | Android Platform Overview | `sandbox` |
| 3.2 | Android Security Testing | `test` |
| 3.3 | Android Data Storage | `storage` |
| 3.4 | Android Cryptographic APIs | `crypto` |
| 3.5 | Android Local Authentication | `identity`、`permissions` |
| 3.6 | Android Network Communication | `tls` |
| 3.7 | Android Platform APIs | `ipc` |
| 3.8 | Android Code Quality and Build Settings | `build` |
| 3.9 | Android Anti-Reversing Defenses | `resilience` |
| 4.1 | iOS Platform Overview | `sandbox` |
| 4.2 | iOS Security Testing | `test` |
| 4.3 | iOS Data Storage | `storage` |
| 4.4 | iOS Cryptographic APIs | `crypto` |
| 4.5 | iOS Local Authentication | `identity`、`permissions` |
| 4.6 | iOS Network Communication | `tls` |
| 4.7 | iOS Platform APIs | `ipc` |
| 4.8 | iOS Code Quality and Build Settings | `build` |
| 4.9 | iOS Anti-Reversing Defenses | `resilience` |

## CS2023 核心主题（C2）

`../cs-math-skill-tree/data/curation/scope.json` 为 `S.2.3` 匹配的 2 项 CS2023 核心主题全部落课（其余“设备身份”与“数据通信保护”结合 OWASP MASVS 一并完整覆盖）：

| 知识点 | KA / 要求 | 课 |
|---|---|---|
| 移动平台与沙箱 | SPD-Mobile / KA Core：Mobile platform constraints | `sandbox`、`ipc`、`permissions` |
| 移动应用威胁建模与测试 | SEC-Foundations / KA Core：web, cloud, and mobile devices | `test`、`build`、`resilience` |

## 综合练习与前置/后继映射（C3 / C4 / C5）

- **综合练习 3 问映射（C4）**：
  - 第 (1) 问比较 Android 与 iOS 的应用安全模型（沙箱、运行时权限、代码签名、商店审核与侧载差异） → `sandbox`、`permissions`。
  - 第 (2) 问参照 OWASP MASVS 举例并修复“不安全的本地数据存储”、“缺少证书校验”与“客户端硬编码密钥” → `storage`、`tls`、`crypto`。
  - 第 (3) 问导出 Intent 组件按外部传入路径读本地文件为何属于权限边界问题（混淆代理）及两项具体修复（关闭导出 `android:exported="false"`；必须导出时校验调用者身份/签名权限并用业务资源允许表映射，不靠路径字符串拼接或隐藏入口名字） → `ipc`。
- **前后继状态（C3 / C5）**：
  - `S.2.3` 在技能树中无必须前置（推荐前置 `S.2.2`、`P.5.2`、`S.1.1`、`C.3.2` 仅作背景衔接；本包对沙箱、进程/内核、混淆代理、Intent、TLS 证书链/证书固定与代码签名等全部术语均按零基础随文定义、不预设已完成推荐前置）。
  - `S.2.3` 无下游后继技能依赖（`unlocks` / `related` 均为空）；同时在 `reports/coverage/S.2.2.md:119` 中承接作为网络安全的移动平台专项推荐延伸（C5 无未覆盖缺口）。
