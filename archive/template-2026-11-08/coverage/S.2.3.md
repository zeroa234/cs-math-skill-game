# S.2.3 课程覆盖表

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | Storage | `storage` |
| 1.2 | Cryptography | `crypto` |
| 1.3 | Authentication and Authorization | `identity`, `permissions` |
| 1.4 | Network Communication | `tls` |
| 1.5 | Platform Interaction | `ipc` |
| 1.6 | Code Quality | `build` |
| 1.7 | Resilience Against Reverse Engineering and Tampering | `resilience` |
| 1.8 | Privacy | `privacy` |
| 2.1 | Mobile Application Taxonomy | `sandbox` |
| 2.2 | Mobile Application Security Testing | `test` |
| 2.3 | Mobile App Tampering and Reverse Engineering | `resilience` |
| 2.4 | Mobile App Authentication Architectures | `identity`, `permissions` |
| 2.5 | Mobile App Network Communication | `tls` |
| 2.6 | Mobile App Cryptography | `crypto` |
| 2.7 | Mobile App Code Quality | `build` |
| 2.8 | Mobile App User Privacy Protection | `privacy` |
| 3.1 | Android Platform Overview | `sandbox` |
| 3.2 | Android Security Testing | `test` |
| 3.3 | Android Data Storage | `storage` |
| 3.4 | Android Cryptographic APIs | `crypto` |
| 3.5 | Android Local Authentication | `identity`, `permissions` |
| 3.6 | Android Network Communication | `tls` |
| 3.7 | Android Platform APIs | `ipc` |
| 3.8 | Android Code Quality and Build Settings | `build` |
| 3.9 | Android Anti-Reversing Defenses | `resilience` |
| 4.1 | iOS Platform Overview | `sandbox` |
| 4.2 | iOS Security Testing | `test` |
| 4.3 | iOS Data Storage | `storage` |
| 4.4 | iOS Cryptographic APIs | `crypto` |
| 4.5 | iOS Local Authentication | `identity`, `permissions` |
| 4.6 | iOS Network Communication | `tls` |
| 4.7 | iOS Platform APIs | `ipc` |
| 4.8 | iOS Code Quality and Build Settings | `build` |
| 4.9 | iOS Anti-Reversing Defenses | `resilience` |

## CS2023 与原综合练习

- SPD-Mobile KA Core 的平台限制见 `sandbox`、`ipc`、`permissions`；SEC-Foundations KA Core 的移动设备安全见威胁建模和测试章节。OWASP MASVS 的八个控制域、MASTG 验证流程和 Android/iOS 的对应问题均按表覆盖。 [OWASP MASVS](https://mas.owasp.org/MASVS/) · [OWASP MASTG](https://mas.owasp.org/MASTG/)
- 原题 1 用 `sandbox` 比较隔离、权限、签名和分发。原题 2 的私有数据、TLS 验证和客户端硬编码秘密见 `storage`、`crypto`、`tls`。原题 3 的导出组件与路径读取见 `ipc`，明确默认关闭、调用者授权和资源允许表。 [Android 应用沙箱](https://source.android.com/docs/security/app-sandbox) · [android:exported](https://developer.android.com/privacy-and-security/risks/android-exported)
- 本地验证检查 Android 清单和网络策略的构建产物、受限资源访问用例以及 TLS 配置的验证行为。平台特定的动态检查在课中说明设备、权限与版本条件。 [Android Keystore](https://developer.android.com/privacy-and-security/keystore) · [Android 网络安全配置](https://developer.android.com/privacy-and-security/security-config) · [Apple Keychain](https://developer.apple.com/documentation/security/keychain-services)
