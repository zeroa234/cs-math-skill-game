# C.3.2 课程覆盖表

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | Applications | `layers` |
| 1.2 | Requirements | `layers` |
| 1.3 | Architecture | `layers` |
| 1.4 | Software | `layers` |
| 1.5 | Performance | `layers` |
| 2.1 | Technology Landscape | `layers` |
| 2.2 | Encoding | `layers` |
| 2.3 | Framing | `ethernet` |
| 2.4 | Error Detection | `ethernet` |
| 2.5 | Reliable Transmission | `ethernet` |
| 2.6 | Multi-Access Networks | `ethernet` |
| 2.7 | Wireless Networks | `ethernet` |
| 2.8 | Access Networks | `ethernet` |
| 3.1 | Switching Basics | `ethernet` |
| 3.2 | Switched Ethernet | `ethernet` |
| 3.3 | Internet (IP) | `ip` |
| 3.4.1 | Network as a Graph | `routing` |
| 3.4.2 | Distance-Vector (RIP) | `routing` |
| 3.4.3 | Link State (OSPF) | `routing` |
| 3.4.4 | Metrics | `routing` |
| 3.5 | Implementation | `forwarding` |
| 4.1.1 | Routing Areas | `bgp` |
| 4.1.2 | Interdomain Routing (BGP) | `bgp` |
| 4.2 | IP Version 6 | `ip` |
| 4.3 | Multicast | `ip` |
| 4.4 | Multiprotocol Label Switching | `forwarding` |
| 4.5 | Routing Among Mobile Devices | `forwarding` |
| 5.1 | Simple Demultiplexor (UDP) | `transport` |
| 5.2 | Reliable Byte Stream (TCP) | `transport` |
| 5.3 | Remote Procedure Call | `http` |
| 5.4 | Transport for Real-Time (RTP) | `transport` |
| 6.1 | Issues in Resource Allocation | `queues` |
| 6.2 | Queuing Disciplines | `queues` |
| 6.3 | TCP Congestion Control | `cwnd` |
| 6.4 | Advanced Congestion Control | `cwnd` |
| 6.5 | Quality of Service | `queues` |
| 7.1.1 | Electronic Mail (SMTP, MIME, IMAP) | `http` |
| 7.1.2 | World Wide Web (HTTP) | `http` |
| 7.1.3 | Web Services | `http` |
| 7.2 | Multimedia Applications | `http` |
| 7.3.1 | Name Service (DNS) | `dns` |
| 7.3.2 | Network Management (SNMP, OpenConfig) | `dns` |
| 7.4 | Overlay Networks | `http` |

## 核心主题、综合练习与后继技能

CS2023 分层、路由、拥塞、命名分别见 `layers`、`forwarding` / `routing` / `bgp`、`queues` / `cwnd`、`dns`。原综合练习的封装、子网、握手和窗口、最短路径、回显分别见 `layers`、`ip`、`transport` / `cwnd`、`routing`、`http`。为 S.2.2 等后继技能准备了 ARP、DHCP、VLAN、BGP、TCP 序号与 DNS 缓存。主资料为 [Peterson 与 Davie 教材](https://github.com/SystemsApproach/book) 和 [Stanford CS144](https://cs144.github.io/)。物理信号推导留给 C.3.1，移动网络与高性能转发的实现留给 C.3.3、C.3.5。
