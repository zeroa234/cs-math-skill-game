# C.3.2 网络协议、路由与传输：覆盖表

**状态（2026-11-17）：已写完。** `data/content/C.3.2.yaml`（version 2）共 24 课、结业挑战 15 题。`node scripts/check-coverage.mjs C.3.2`：43 节全部有课，包含 1.2 的电路交换/分组交换与统计复用。课里的计算、CRC 模 2 除法、子网掩码、最长前缀匹配、Dijkstra、无穷计数、公平排队、拥塞窗口、Base64 与本机 TCP socket 字节流由 `tests/content/C.3.2.verify.py` 实测核对（65/65 项通过）。依据：`../cs-math-skill-tree/data/outlines/C.3.2.json`，主教材为 Larry Peterson & Bruce Davie《Computer Networks: A Systems Approach》第 6 版（2021/2024 在线版，第 1–6 章与第 9 章，略去第 7 章表示格式与第 8 章网络安全），补充参考 Stanford CS144 与小林coding《图解网络》。游戏内部章序：`1. 链路/IP/TCP/UDP`、`2. 路由`、`3. 拥塞控制`、`4. 名称系统与应用协议`。

必须前置为 `P.2.2`（及 `P.1.1`）和 `F.1.1`：可直接假设程序、函数、循环、列表、字典、字节、内存地址、十六进制、缓冲区、文件描述符、栈、队列、哈希表、树、图、邻接表与 BFS/DFS。计算机组成 `C.1.1`、操作系统 `C.2.1`、系统编程 `C.2.2` 与数据通信 `C.3.1` 仅是推荐前置，因此二进制、MAC 地址、广播、路由器查表、距离向量、链路状态、自治系统、拥塞窗口、套接字通信都在本包内从零讲起。

`node scripts/check-coverage.mjs C.3.2` 自动检查本表。

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | 1.1 Applications | `layers-perf`、`http-versions` |
| 1.2 | 1.2 Requirements | `layers-perf` |
| 1.3 | 1.3 Architecture | `layers-perf` |
| 1.4 | 1.4 Software | `layers-perf`、`sockets-echo` |
| 1.5 | 1.5 Performance | `layers-perf` |
| 2.1 | 2.1 Technology Landscape | `encoding-framing` |
| 2.2 | 2.2 Encoding | `encoding-framing` |
| 2.3 | 2.3 Framing | `encoding-framing` |
| 2.4 | 2.4 Error Detection | `error-detection` |
| 2.5 | 2.5 Reliable Transmission | `reliable-link` |
| 2.6 | 2.6 Multi-Access Networks | `shared-media` |
| 2.7 | 2.7 Wireless Networks | `shared-media` |
| 2.8 | 2.8 Access Networks | `encoding-framing` |
| 3.1 | 3.1 Switching Basics | `switching-vlan` |
| 3.2 | 3.2 Switched Ethernet | `switching-vlan` |
| 3.3 | 3.3 Internet (IP) | `ip-cidr`、`arp-dhcp-icmp` |
| 3.4.1 | 3.4.1 Network as a Graph | `link-state` |
| 3.4.2 | 3.4.2 Distance-Vector (RIP) | `distance-vector` |
| 3.4.3 | 3.4.3 Link State (OSPF) | `link-state` |
| 3.4.4 | 3.4.4 Metrics | `link-state` |
| 3.5 | 3.5 Implementation | `forwarding-lpm` |
| 4.1.1 | 4.1.1 Routing Areas | `link-state` |
| 4.1.2 | 4.1.2 Interdomain Routing (BGP) | `bgp-interdomain` |
| 4.2 | 4.2 IP Version 6 | `ipv6-multicast` |
| 4.3 | 4.3 Multicast | `ipv6-multicast` |
| 4.4 | 4.4 Multiprotocol Label Switching | `mpls-mobile` |
| 4.5 | 4.5 Routing Among Mobile Devices | `mpls-mobile` |
| 5.1 | 5.1 Simple Demultiplexor (UDP) | `udp-rpc-rtp` |
| 5.2 | 5.2 Reliable Byte Stream (TCP) | `tcp-reliable`、`sockets-echo` |
| 5.3 | 5.3 Remote Procedure Call | `udp-rpc-rtp` |
| 5.4 | 5.4 Transport for Real-Time (RTP) | `udp-rpc-rtp` |
| 6.1 | 6.1 Issues in Resource Allocation | `queues-aqm` |
| 6.2 | 6.2 Queuing Disciplines | `queues-aqm` |
| 6.3 | 6.3 TCP Congestion Control | `cwnd-aimd`、`loss-recovery-cc` |
| 6.4 | 6.4 Advanced Congestion Control | `loss-recovery-cc` |
| 6.5 | 6.5 Quality of Service | `queues-aqm` |
| 7.1.1 | 9.1.1 Electronic Mail (SMTP, MIME, IMAP) | `email-snmp` |
| 7.1.2 | 9.1.2 World Wide Web (HTTP) | `http-versions` |
| 7.1.3 | 9.1.3 Web Services | `http-versions` |
| 7.2 | 9.2 Multimedia Applications | `overlay-cdn` |
| 7.3.1 | 9.3.1 Name Service (DNS) | `dns-hierarchy` |
| 7.3.2 | 9.3.2 Network Management (SNMP, OpenConfig) | `email-snmp` |
| 7.4 | 9.4 Overlay Networks | `overlay-cdn` |

## CS2023 核心主题（C2）

`../cs-math-skill-tree/data/curation/scope.json` 中 `C.3.2` 条目为空（`{}`），主大纲 8 个知识点（链路、IP、TCP、UDP、路由、拥塞控制、名称系统、应用协议）已全部对应到上述课程。

## 学习资源的章节（C3）

| 来源 | 章节与概念 | 课 / 说明 |
|---|---|---|
| `en1` Peterson & Davie 第 6 版 | 第 1–6 章与第 9 章 43 节 | 全收；第 7 章表示与第 8 章安全按大纲 `omitted` 分别留给其他节点 |
| `zh1` 哈工大《计算机网络》 | 三单元：分层与 Socket、可靠传输与滑动窗口、UDP/TCP、数据报与虚电路、IP/CIDR/聚合、ICMP/DHCP/NAT/IPv6、路由算法与协议、差错编码、MAC/ARP/以太网/VLAN/PPP/无线 | 全部讲到（`layers-perf` 到 `sockets-echo`）；无线与安全攻防的深度留给 `S.2.2` |
| `en2` Stanford CS144 | week-1 可靠性、week-2 TCP、week-3 分组交换、week-4 拥塞控制、routing-intro | 对应 `reliable-link`、`tcp-reliable`、`forwarding-lpm`、`cwnd-aimd`、`loss-recovery-cc`、`link-state` |
| `r7-zh1` 小林coding《图解网络》 | 4.2 拥塞控制（慢启动、拥塞避免、超时与快重传/快恢复）、2.2 DNS 域名树与解析、03 应用层（HTTP/HTTPS/HTTP2/HTTP3/RPC/WebSocket） | 对应 `cwnd-aimd`、`loss-recovery-cc`、`dns-hierarchy`、`http-versions`、`udp-rpc-rtp`（HTTPS 握手细节在 `S.2.2` 展开） |

## 综合练习（C4）

| 小题 | 要用到的 | 课 |
|---|---|---|
| (1) TCP/IP 分层各层功能与代表协议；HTTP 请求从应用层往下加哪些头部 | 分层封装、HTTP/DNS、TCP/UDP、IP/ICMP、以太网帧头帧尾（MAC 与 FCS） | `layers-perf`、`shared-media`、`ip-cidr`、`http-versions` |
| (2) 192.168.10.77/26 求网络地址、广播地址、可用主机数和范围 | 32 位地址、掩码按位与、块大小、首尾地址含义 | `ip-cidr` |
| (3) TCP 三次握手；为什么不能两次；初始 cwnd=1、ssthresh=8 前 6 个 RTT | SYN/SYN-ACK/ACK、滞留旧 SYN 问题、慢启动倍增到 ssthresh 后每轮 +1 | `tcp-reliable`、`cwnd-aimd` |
| (4) 距离向量与链路状态区别；A–B 1, A–C 4, B–C 2, B–D 5, C–D 1 求 Dijkstra 与 A 的转发表 | Bellman–Ford 与泛洪+Dijkstra、无穷计数、转发表只写下一跳 | `link-state`、`distance-vector` |
| (5) Python socket 写 TCP 回显服务器和客户端，为什么一次 recv 不保证收齐 | `create_server`、`accept`、`create_connection`、`recv`/`sendall` 循环、字节流无边界 | `sockets-echo` |

## 后继技能（C5）

必须后继为 `S.2.2` 网络安全、`S.2.4` 云安全与容器安全、`S.4.1` 渗透测试、`C.3.4` SDN 与可编程网络、`C.3.5` 数据中心与高性能网络、`H.4.4` 边缘计算。其中最直接衔接、且本包需铺垫的概念：
- `S.2.2`：以太网帧与交换机 MAC 学习、VLAN 分段（`switching-vlan`）；ARP 请求/应答为何无认证、DHCP 广播与中继、NAT 地址端口映射（`arp-dhcp-icmp`）；TCP 序列号/随机 ISN 与半开连接队列（`tcp-reliable`）；BGP AS_PATH 与邻接通告为何缺源验证（`bgp-interdomain`）；DNS 层级、事务 ID/源端口与缓存 TTL（`dns-hierarchy`）；HTTPS 与 TLS 的定位（`http-versions`）。
- `C.3.4`：控制面与数据面分离、交换机 MAC 自学习表、IP 最长前缀匹配查表、SNMP 轮询与声明式配置演进（`switching-vlan`、`forwarding-lpm`、`email-snmp`）。
- `C.3.5`：带宽与延迟乘积、队列尾丢弃与 ECN 显式拥塞通知、内核 socket 与数据路径开销（`layers-perf`、`queues-aqm`、`loss-recovery-cc`、`sockets-echo`）。
- `S.2.4` / `S.4.1` / `H.4.4`：CIDR 网段表达（`ip-cidr`）、HTTP/REST 与 RPC 服务边界（`http-versions`、`udp-rpc-rtp`）。
