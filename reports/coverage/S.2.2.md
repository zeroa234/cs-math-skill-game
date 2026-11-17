# S.2.2 网络安全：覆盖表

**状态（2026-11-17）：已写完。** 依据 `../cs-math-skill-tree/data/outlines/S.2.2.json` 与 `../cs-math-skill-tree/output/outlines.json`，主来源为 UC Berkeley CS 161 教材网络部分（第 25–37 章，含第 28 章 WPA）；补充参考 Stanford CS155、哈工大《计算机网络》、中科大曾凡平《信息安全导论》、清华《网络空间安全导论》与 RFC 8446 / NIST SP 800-207。游戏内部章序：`1. 协议攻击面`、`2. 分段`、`3. 防火墙`、`4. 入侵检测`、`5. 传输保护与网络监测`、`6. 无线链路安全`。

必须前置为 `C.3.2 网络协议、路由与传输` 与 `C.2.1 操作系统`（及其传递前置 `P.1.1`、`P.2.2`、`F.1.1`、`C.1.1`）：可直接假设以太网帧、MAC 地址、交换机 MAC 学习与 VLAN、ARP/DHCP/NAT、IP/CIDR、BGP 自治系统、TCP 三次握手/序号/半开队列与拥塞、DNS 层级与 TTL、TLS 定位以及进程/系统调用/权限。`S.1.1` 与 `S.1.2` 仅是推荐前置，因此对称/公钥加密、数字签名、哈希与最小权限等概念在本包内从直觉讲起。

注：大纲第 13 章为 `WPA 无线安全`（`13.1`–`13.5`），虽 `omitted` 注释曾提及无线属 `S.2.3`，但大纲正表与节点简介均包含“无线链路安全”，因此本包第 6 章完整讲授 `13.1`–`13.5`。

`node scripts/check-coverage.mjs S.2.2` 自动检查本表。

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | 25.1 Local Area Networks | `network-adversaries` |
| 1.2 | 25.2 Internet layering | `network-adversaries` |
| 1.3 | 25.3 Protocols and Headers | `network-adversaries` |
| 1.4 | 25.4 Addressing: MAC, IP, Ports | `network-adversaries` |
| 1.5 | 25.5 Packets vs. Connections | `network-adversaries` |
| 1.6 | 25.6 Network Adversaries | `network-adversaries` |
| 2.1 | 26.1 Cheat sheet (ARP) | `arp-dhcp-spoofing` |
| 2.2 | 26.2 Networking background: Ethernet | `arp-dhcp-spoofing` |
| 2.3 | 26.3 Protocol: ARP | `arp-dhcp-spoofing` |
| 2.4 | 26.4 Attack: ARP Spoofing | `arp-dhcp-spoofing` |
| 2.5 | 26.5 Defenses: Switches | `arp-dhcp-spoofing` |
| 3.1 | 27.1 Cheat sheet (DHCP) | `arp-dhcp-spoofing` |
| 3.2 | 27.2 Protocol: DHCP | `arp-dhcp-spoofing` |
| 3.3 | 27.3 Networking background: NAT | `network-segmentation` |
| 3.4 | 27.4 Attack (DHCP) | `arp-dhcp-spoofing` |
| 3.5 | 27.5 Defenses (DHCP) | `arp-dhcp-spoofing` |
| 4.1 | 29.1 Cheat sheet (BGP) | `bgp-hijacking` |
| 4.2 | 29.2 Networking background: Subnets | `network-segmentation` |
| 4.3 | 29.3 Protocol: BGP | `bgp-hijacking` |
| 4.4 | 29.4 Attack: Malicious ASs | `bgp-hijacking` |
| 4.5 | 29.5 Defenses (BGP) | `bgp-hijacking` |
| 5.1 | 30.1 Cheat sheet (TCP/UDP) | `tcp-injection-dos` |
| 5.2 | 30.2 Networking background: Ports | `tcp-injection-dos` |
| 5.3 | 30.3 Protocol: UDP | `tcp-injection-dos` |
| 5.4 | 30.4 Protocol: TCP | `tcp-injection-dos` |
| 5.5 | 30.5 Tradeoffs between TCP and UDP | `tcp-injection-dos` |
| 5.6 | 30.6 Attack: TCP Packet Injection | `tcp-injection-dos` |
| 5.7 | 30.7 Defenses: TLS, random initial sequence numbers | `tcp-injection-dos`、`tls-handshake-pfs` |
| 6.1 | 31.1 TLS Handshake | `tls-handshake-pfs` |
| 6.2 | 31.2 Replay attacks | `tls-handshake-pfs` |
| 6.3 | 31.3 TLS in practice | `tls-handshake-pfs` |
| 7.1 | 32.1 Name servers | `dns-poisoning` |
| 7.2 | 32.2 Name server hierarchy | `dns-poisoning` |
| 7.3 | 32.3 DNS Message Format | `dns-poisoning` |
| 7.4 | 32.4 DNS Lookup | `dns-poisoning` |
| 7.5 | 32.5 DNS Security: Bailiwick | `dns-poisoning` |
| 7.6 | 32.6 DNS Security: On-path vs off-path attackers | `dns-poisoning` |
| 7.7 | 32.7 DNS Security: Kaminsky attack | `dns-poisoning` |
| 8.1 | 33.1 Signing records | `dnssec-trust` |
| 8.2 | 33.2 Delegating trust | `dnssec-trust` |
| 8.3 | 33.3 DNSSEC Intuition | `dnssec-trust` |
| 8.4 | 33.4 New DNSSEC record types | `dnssec-trust` |
| 8.5 | 33.5 Key Signing Keys and Zone Signing Keys | `dnssec-trust` |
| 8.6 | 33.6 DNSSEC query walkthrough | `dnssec-trust` |
| 8.7 | 33.7 Nonexistent domains | `dnssec-trust` |
| 9.1 | 34.1 Introduction (DoS) | `tcp-injection-dos` |
| 9.2 | 34.2 Application Level DoS | `tcp-injection-dos` |
| 9.3 | 34.3 SYN Flood Attacks | `tcp-injection-dos` |
| 9.4 | 34.4 Distributed Denial of Service (DDoS) | `tcp-injection-dos` |
| 10.1 | 35.1 Introduction to Controlling Network Access | `network-segmentation`、`zero-trust` |
| 10.2 | 35.2 Security Policy | `stateless-stateful-fw`、`firewall-rules-tradeoffs` |
| 10.3 | 35.3 Enforcement: Stateful Packet Filters | `stateless-stateful-fw` |
| 10.4 | 35.4 Enforcement: Other Firewalls | `firewall-rules-tradeoffs` |
| 10.5 | 35.5 Firewall Principles | `firewall-rules-tradeoffs` |
| 10.6 | 35.6 Firewall Advantages | `firewall-rules-tradeoffs` |
| 10.7 | 35.7 Firewall Disadvantages | `firewall-rules-tradeoffs` |
| 11.1 | 36.1 Types of detectors | `ids-nids-hids` |
| 11.2 | 36.2 Network Intrusion Detection System (NIDS) | `ids-nids-hids`、`network-monitoring` |
| 11.3 | 36.3 Host-based Intrusion Detection System (HIDS) | `ids-nids-hids` |
| 11.4 | 36.4 Logging | `ids-baserate-evasion`、`network-monitoring` |
| 11.5 | 36.5 False Positives and False Negatives | `ids-baserate-evasion` |
| 11.6 | 36.6 Detection strategies | `ids-nids-hids` |
| 11.7 | 36.7 Signature-based | `ids-nids-hids` |
| 11.8 | 36.8 Anomaly-based | `ids-nids-hids` |
| 11.9 | 36.9 Specification-based | `ids-nids-hids` |
| 12 | 37 Abusing Intrusion Detection | `ids-baserate-evasion` |
| 13.1 | 28.1 Cheat sheet (WPA) | `wifi-wpa-security` |
| 13.2 | 28.2 Networking background: WiFi | `wifi-wpa-security` |
| 13.3 | 28.3 Protocol (WPA) | `wifi-wpa-security` |
| 13.4 | 28.4 Attacks (WPA) | `wifi-wpa-security` |
| 13.5 | 28.5 Defenses: WPA2-Enterprise | `wifi-wpa-security` |

## CS2023 核心主题（C2）

依据 `../cs-math-skill-tree/data/curation/scope.json`（均属 `NC-Security · KA Core`）：

| 主题 | 对应知识点 | 课 |
|---|---|---|
| Network specific threats and attack types | 协议攻击面 | `network-adversaries`、`arp-dhcp-spoofing`、`bgp-hijacking`、`tcp-injection-dos`、`dns-poisoning`、`dnssec-trust` |
| intrusion detection, firewall | 防火墙、入侵检测 | `stateless-stateful-fw`、`firewall-rules-tradeoffs`、`ids-nids-hids`、`ids-baserate-evasion` |
| Network monitoring | 传输保护与网络监测 | `tls-handshake-pfs`、`network-monitoring` |

## 学习资源的章节（C3）

| 来源 | 章节与概念 | 课 / 说明 |
|---|---|---|
| `en2` Berkeley CS 161 | 第 25–37 章（含第 28 章 WPA） | 全部 71 个叶子节逐一教到 |
| `en1` Stanford CS155 | L12 HTTPS、L14 协议攻击、L15 BGP/DNS/DNSSEC/防火墙/Bro IDS、L16 DoS | 对应 `tls-handshake-pfs`、`arp-dhcp-spoofing`、`bgp-hijacking`、`dns-poisoning`、`dnssec-trust`、`firewall-rules-tradeoffs`、`network-monitoring`、`tcp-injection-dos` |
| `zh1` 哈工大《计算机网络》 | 第二单元 CIDR/VLAN、第三单元安全威胁/防火墙/入侵检测/SSL/IPsec/VPN/无线局域网 | 对应 `network-segmentation`、`firewall-rules-tradeoffs`、`ids-nids-hids`、`tls-handshake-pfs`、`wifi-wpa-security` |
| `zh2` 中科大《信息安全导论》 | 第 7 章扫描/DoS/僵尸网络、第 8 章防火墙/IDS/蜜罐/审计、第 10 章 IPsec/SSL/WEP/WPA | 对应 `tcp-injection-dos`、`firewall-rules-tradeoffs`、`ids-nids-hids`、`network-monitoring`、`tls-handshake-pfs`、`wifi-wpa-security` |
| `r7-zh1` 清华《网络空间安全导论》 | 第 8–11 章 TCP/IP 栈安全、BGP 路由安全与 MANRS/BGPsec、DNS 缓存投毒与 DNSSEC、源地址验证 | 对应 `bgp-hijacking`、`tcp-injection-dos`、`dns-poisoning`、`dnssec-trust` |

## 综合练习（C4）

| 小题 | 要用到的 | 课 |
|---|---|---|
| (1) ARP 欺骗、IP 伪造、TCP SYN 洪泛、DNS 缓存投毒的原理与防御 | 分层攻击面、DAI/静态绑定、BCP 38 入口过滤、SYN Cookie、随机端口与查询 ID + DNSSEC | `arp-dhcp-spoofing`、`network-segmentation`、`tcp-injection-dos`、`dns-poisoning`、`dnssec-trust` |
| (2) 内网/DMZ/外网三区有状态防火墙规则设计，为什么默认拒绝 | 五元组与规则首条匹配、ESTABLISHED 状态化回包、DMZ 对外仅放 443、默认拒绝白名单原则 | `network-segmentation`、`stateless-stateful-fw`、`firewall-rules-tradeoffs` |
| (3) TLS 1.3 握手主要步骤、服务器证书验证要素、前向保密定义 | ClientHello/ServerHello/Certificate/CertificateVerify/Finished、CA 链/有效期/域名/吊销、临时 (EC)DHE | `tls-handshake-pfs` |
| (4) 签名 vs 异常检测区别，10^6 事件 / 10 真攻击 / 99% 检测率 / 0.1% 误报率的基率谬误计算 | 误报率与真攻击率相差数个数量级导致约 99% 告警为误报 | `ids-nids-hids`、`ids-baserate-evasion` |
| (5) 什么是网络分段与零信任核心思想 | VLAN/子网/DMZ 限制横向移动、永不信任始终验证、最小权限与持续监测 | `network-segmentation`、`zero-trust` |

## 后继技能（C5）

必须后继为 `S.4.4 安全运营、检测与攻防评估`（其综合练习要求运用 NIDS/HIDS、签名与异常检测、误报/漏报与基率计算、网络/代理/DNS/认证日志分诊、从单纯封 IP 升级到多源日志关联）。本包在 `ids-nids-hids`、`ids-baserate-evasion` 与 `network-monitoring` 已将上述概念、计算与“告警/日志/分诊”术语全部打通。推荐后继 `S.2.3`、`S.2.4`、`S.4.1` 亦可直接衔接无线安全、分段隔离与协议攻击面。
