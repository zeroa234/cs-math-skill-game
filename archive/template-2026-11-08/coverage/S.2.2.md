# S.2.2 课程覆盖表

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | Local Area Networks | `adversaries` |
| 1.2 | Internet layering | `adversaries` |
| 1.3 | Protocols and Headers | `adversaries` |
| 1.4 | Addressing: MAC, IP, Ports | `adversaries` |
| 1.5 | Packets vs. Connections | `adversaries` |
| 1.6 | Network Adversaries | `adversaries` |
| 2.1 | Cheat sheet | `adversaries` |
| 2.2 | Networking background: Ethernet | `adversaries` |
| 2.3 | Protocol: ARP | `adversaries` |
| 2.4 | Attack: ARP Spoofing | `local-spoof` |
| 2.5 | Defenses: Switches | `local-spoof` |
| 3.1 | Cheat sheet | `local-spoof` |
| 3.2 | Protocol: DHCP | `local-spoof` |
| 3.3 | Networking background: NAT | `segments` |
| 3.4 | Attack | `local-spoof` |
| 3.5 | Defenses | `local-spoof` |
| 4.1 | Cheat sheet | `routing-attacks` |
| 4.2 | Networking background: Subnets | `segments` |
| 4.3 | Protocol: BGP | `routing-attacks` |
| 4.4 | Attack: Malicious ASs | `routing-attacks` |
| 4.5 | Defenses | `routing-attacks` |
| 5.1 | Cheat sheet | `transport-attacks` |
| 5.2 | Networking background: Ports | `transport-attacks` |
| 5.3 | Protocol: UDP | `transport-attacks` |
| 5.4 | Protocol: TCP | `transport-attacks` |
| 5.5 | Tradeoffs between TCP and UDP | `transport-attacks` |
| 5.6 | Attack: TCP Packet Injection | `transport-attacks` |
| 5.7 | Defenses: TLS, random initial sequence numbers | `tls` |
| 6.1 | TLS Handshake | `tls` |
| 6.2 | Replay attacks | `tls` |
| 6.3 | TLS in practice | `tls` |
| 7.1 | Name servers | `dns-poison` |
| 7.2 | Name server hierarchy | `dns-poison` |
| 7.3 | DNS Message Format | `dns-poison` |
| 7.4 | DNS Lookup | `dns-poison` |
| 7.5 | DNS Security: Bailiwick | `dns-poison` |
| 7.6 | DNS Security: On-path attackers and off-path attackers | `dns-poison` |
| 7.7 | DNS Security: Kaminsky attack | `dns-poison` |
| 8.1 | Signing records | `dnssec` |
| 8.2 | Delegating trust | `dnssec` |
| 8.3 | DNSSEC Intuition | `dnssec` |
| 8.4 | New DNSSEC record types | `dnssec` |
| 8.5 | Key Signing Keys and Zone Signing Keys | `dnssec` |
| 8.6 | DNSSEC query walkthrough | `dnssec` |
| 8.7 | Nonexistent domains | `dnssec` |
| 9.1 | Introduction | `transport-attacks` |
| 9.2 | Application Level DoS | `transport-attacks` |
| 9.3 | SYN Flood Attacks | `transport-attacks` |
| 9.4 | Distributed Denial of Service (DDoS) | `transport-attacks` |
| 10.1 | Introduction to Controlling Network Access | `segments` |
| 10.2 | Security Policy | `firewall` |
| 10.3 | Enforcement: Stateful Packet Filters | `firewall` |
| 10.4 | Enforcement: Other Firewalls | `firewall` |
| 10.5 | Firewall Principles | `firewall` |
| 10.6 | Firewall Advantages | `firewall` |
| 10.7 | Firewall Disadvantages | `firewall` |
| 11.1 | Types of detectors | `detection` |
| 11.2 | Types of detectors: Network Intrusion Detection System (NIDS) | `detection` |
| 11.3 | Types of detectors: Host-based Intrusion Detection System (HIDS) | `detection` |
| 11.4 | Types of detectors: Logging | `monitoring` |
| 11.5 | False Positives and False Negatives | `detection` |
| 11.6 | Detection strategies | `detection` |
| 11.7 | Detection strategies: Signature-based detection | `detection` |
| 11.8 | Detection strategies: Anomaly-based detection | `detection` |
| 11.9 | Detection strategies: Specification-based detection | `detection` |
| 12 | Abusing Intrusion Detection | `monitoring` |
| 13.1 | Cheat sheet | `wifi` |
| 13.2 | Networking background: WiFi | `wifi` |
| 13.3 | Protocol | `wifi` |
| 13.4 | Attacks | `wifi` |
| 13.5 | Defenses: WPA2-Enterprise | `wifi` |

## 核心主题、综合练习与后继技能

CS2023 的网络威胁、访问控制、检测和监测分别见 `adversaries` 至 `dnssec`、`segments` / `firewall`、`detection`、`monitoring`。综合练习的分层攻击、防火墙规则、TLS、告警基率、分段与零信任分别由 `local-spoof` 至 `dnssec`、`firewall`、`tls`、`detection`、`segments` 准备。S.4.4 用到的证据保全、告警分诊和检测度量由 `detection` / `monitoring` 打底。参考 [Berkeley CS161](https://textbook.cs161.org/)、[Stanford CS155](https://cs155.stanford.edu/)、[TLS 1.3 RFC](https://www.rfc-editor.org/rfc/rfc8446) 和 [NIST 零信任架构](https://csrc.nist.gov/pubs/sp/800/207/final)。
