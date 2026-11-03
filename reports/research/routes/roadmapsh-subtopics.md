# roadmap.sh subtopics — cyber-security & android

Snapshot read 2026-11-03. API `updatedAt`: cyber-security 2026-06-15, android 2026-07-24.

## URLs read

Primary (all names below come from these):
- https://roadmap.sh/api/v1-official-roadmap/cyber-security — 373 nodes, 18 edges, 295 subtopics
- https://roadmap.sh/api/v1-official-roadmap/android — 157 nodes, 36 edges, 98 subtopics

Layout check only (not used for names):
- https://roadmap.sh/roadmaps/cyber-security.png
- https://roadmap.sh/roadmaps/android.png

The PNGs are older than the JSON: the CS PNG has "SANS Holiday Hack Challenge" where the JSON has "pwn.college"; the Android PNG has an older node set (Frame/Linear/…, Toast/ListView, no Security) and no Jetpack Compose-era nodes. Edge-count corroboration: the old repo snapshot `raw.githubusercontent.com/nilbuild/developer-roadmap/deb9aaafc283f5cf88816cd79528d600878c22cc/src/data/roadmaps/cyber-security/cyber-security.json` also has exactly 18 edges.

## How subtopics were assigned

- **Edges first.** Used every topic→subtopic edge, and subtopic→subtopic edges by following the source subtopic’s topic.
  - cyber-security: “Connection Types and their function” → NFC, WiFi; “Understand Basics of Popular Suites” → MS Office Suite, iCloud, Google Suite; “Security Skills and Knowledge” → Blue / Red / Purple Teams; “Programming Skills” → Python, Go, JavaScript, C++, Bash, Power Shell. Also section→Networking (the DHCP/DNS/NTP/IPAM box) and Cloud→section (the left cloud box). 12 subtopics are edge-covered; Bluetooth/Infrared have no edge.
  - android: Storage → Shared Preferences, DataStore, Room Database, File System. Design & Architecture’s only edge goes to the paragraph node “Architectural Patterns”, which is not a subtopic. No other requested topic has a child edge.
- **Position fallback.** Remaining cyber-security subtopics (283) and remaining android target subtopics were assigned by position. I did not use plain Euclidean nearest-topic: topic headers sit at branch points, so plain nearest misassigns e.g. MS Office Suite/iCloud/Google Suite (x≈427) to Operating Systems (x≈370) instead of Fundamental IT Skills, and flips lower certification rows. I reconstructed the visual branch/column structure (topic headers, horizontal/vertical connector lines, stacked label boxes, sections) and assigned each subtopic to the topic whose branch/column contains it.
- **Grouping** only where a topic has >~40 subtopics (Security 157, Networking 61). Group titles are the roadmap’s `label` nodes (bold). “No label” groups have no label node. Paragraph nodes (Beginner/Advanced Certifications, Keep Learning, Architectural Patterns, Design Patterns) are not subtopics and are excluded.
- All 295 CS subtopics are covered exactly once: 32 + 19 + 61 + 157 + 20 + 6 = 295.

## 1) cyber-security

### Fundamental IT Skills — 32 (flat)
HackTheBox, TryHackMe, VulnHub, picoCTF, pwn.college; CompTIA A+, CompTIA Linux+, CompTIA Network+, CCNA, CompTIA Security+, CEH, CISA, CISM, GSEC, GPEN, GWAPT, GIAC, OSCP, CREST, CISSP; Computer Hardware Components, Connection Types and their function, OS-Independent Troubleshooting, Understand Basics of Popular Suites, Basics of Computer Networking, NFC, Bluetooth, WiFi, Infrared, MS Office Suite, iCloud, Google Suite.

### Operating Systems — 19 (flat)
Windows, Linux, MacOS; Installation and Configuration, Different Versions and Differences, Navigating using GUI and CLI, Understand Permissions, Installing Software and Applications, Performing CRUD on Files, Troubleshooting, Common Commands; VMWare, VirtualBox, esxi, proxmox, Hypervisor, GuestOS, HostOS, VM.

### Networking Knowledge — 61 (grouped)
- **IP Terminology** — Basics of Subnetting, Public vs Private IP Addresses, localhost, loopback, CIDR, subnet mask, default gateway
- **Understand the Terminology** — VLAN, DMZ, ARP, VM, DHCP, DNS, NAT, IP, Router, Switch, VPN
- **Understand these** — MAN, LAN, WAN, WLAN
- **Functions of each** — DHCP, DNS, NTP, IPAM
- **Network Topologies** — Star, Ring, Mesh, Bus
- **Network Protocols** — SSH, RDP, FTP, SFTP, HTTP / HTTPS, SSL / TLS
- **Authentication Methodologies** — Kerberos, RADIUS, LDAP, SSO, Certificates, Local Auth
- **Troubleshooting Tools** — ipconfig, ping, dig, netstat, route, nmap, tcpdump, arp, tracert, nslookup, iptables, Packet Sniffers, Port Scanners, Protocol Analyzers
- **No label (right-hand column)** — Understand the OSI Model, Common Protocols and their Uses, Common Ports and their Uses, SSL and TLS Basics, Basics of NAS and SAN

### Security Skills and Knowledge — 157 (grouped)
- **No label, left column (10)** — Understand Common Hacking Tools, Understand Common Exploit Frameworks, Understand Concept of Defense in Depth, Understand Concept of Runbooks, Understand Basics of Forensics, Basics and Concepts of Threat Hunting, Basics of Vulnerability Management, Basics of Reverse Engineering, Penetration Testing Rules of Engagement, Perimiter vs DMZ vs Segmentation
- **No label, center column (11)** — Core Concepts of Zero Trust, Roles of Compliance and Auditors, Understand the Definition of Risk, Understand Backups and Resiliency, Cyber Kill Chain, MFA & 2FA, Honeypots, Operating System Hardening, Understand Concept of Isolation, Basics of IDS and IPS, Authentication vs Authorization
- **No label, right column (9)** — Blue / Red / Purple Teams, False Negative / False Positive, True Negative / True Positive, Basics of Threat Intel, OSINT, Understand Handshakes, Understand CIA Triad, Privilege Escalation, Web Based Attacks and OWASP10, Learn how Malware works and Types
- **Tools for Incident Response and Discovery** — dig, nmap, ping, arp, cat, dd, tail, hping, head, grep, nslookup, tracert, winhex, autopsy, ipconfig, curl, wireshark, memdump, FTK Imager
- **Basics of Cryptography** — Salting, Hashing, Key Exchange, Private vs Public Keys, PKI, Obfuscation
- **Attack Types and Differences** — Phishing, Whishing, Whaling, Smishing, Spam vs Spim, Shoulder Surfing, Tailgating, Dumpster Diving, Zero day, Social Engineering, Reconnaissance, Impersonation, Watering Hole Attack, Drive by Attack, Typo Squatting, Brute Force vs Password Spray
- **Common Attacks** — DoS vs DDoS, MITM, CSRF, Spoofing, SQL Injection, XSS, Evil Twin, VLAN Hopping, DNS Poisoning, Deauth Attack, Replay Attack, Rogue Access Point, Buffer Overflow, Memory Leak, Pass the Hash, Directory Traversal
- **Understand Frameworks** — Diamond Model, Kill Chain, ATT&CK
- **Understand Common Standards** — ISO, RMF, NIST, CIS, CSF
- **Common Distros for hacking** — ParrotOS, Kali Linux
- **Understand the following** — SIEM, SOAR
- **Using tools for Unintended Purposes** — LOLBAS, GTFOBINS, WADCOMS
- **Secure vs Unsecure Protocols** — FTP vs SFTP, SSL vs TLS, IPSEC, DNSSEC, LDAPS, SRTP, S/MIME
- **Learn how to find and use these logs** — Event Logs, syslogs, netflow, Packet Captures, Firewall Logs
- **Understand Hardening Concepts** — MAC-based, NAC-based, Port Blocking, Group Policy, Sinkholes, ACLs, Patching, Jump Server, Endpoint Security
- **Understand the following Terms** — Antivirus, Antimalware, EDR, DLP, Firewall & Nextgen Firewall, HIPS, NIDS, NIPS, Host Based Firewall, Sandboxing, EAP vs PEAP, WPS, ACL, WPA vs WPA2 vs WPA3 vs WEP
- **Understand the Incident Response Process** — Preparation, Identification, Containment, Eradication, Recovery, Lessons Learned
- **Understand Common Tools** — VirusTotal, urlscan, any.run, Joe Sandbox, urlvoid, WHOIS
- **Understand Audience** — Stakeholders, HR, Legal, Compliance, Management
- **Understand Threat Classification** — Zero Day, Known vs Unknown, APT

### Cloud Skills and Knowledge — 20 (flat)
Understand the Concept of Security in the Cloud, Understand the differences between cloud and on-premises, Understand the concept of Infrastructure as Code, Understand the Concept of Serverless, Understand the basics and general flow of deploying in the cloud; SaaS, PaaS, IaaS, Private, Public, Hybrid, AWS, GCP, Azure, S3, Dropbox, iCloud, Box, OneDrive, Google Drive.

### Programming Skills — 6 (flat)
Python, Go, JavaScript, C++, Bash, Power Shell.

## 2) android

- **Asynchronism (5)** — Coroutines, RxJava, WorkManager, Threads, RxKotlin.
- **Storage (4)** — Shared Preferences, DataStore, Room Database, File System. (All four are topic→subtopic edges.)
- **Network (3)** — Retro, OkHttp, Apollo-Android.
- **Design & Architecture (16)** — MVI, MVVM, MVP, MVC, Repository Pattern, Builder Pattern, Factory Pattern, Observer Pattern, Flow, RxKotlin, RxJava, LiveData, Dependency Injection, Dagger, Hilt, Koin.
- **Security (0)** — no subtopic node exists in the JSON for this topic. (It is absent from the older PNG too.)

## Ambiguous / notes

- **Cyber-security has almost no parent edges:** only 12 subtopics are covered by edges; 283 are positional. The old repo snapshot has the same 18 edges, so this is not an API truncation.
- **Most uncertain positional calls** (left-hand stacked blocks):
  - Common Virtualization Technologies + Basics of Virtualization → **Operating Systems**. No connector in the PNG; OS is the nearest header and the block sits at OS height. Plain Euclidean nearest would put “Basics of Virtualization” nearer Networking.
  - Troubleshooting Tools → **Networking Knowledge**. The PNG shows a dotted connector from Networking Knowledge into the Troubleshooting Tools box (and into “Functions of each”), and it is nearest to Networking’s label.
  - Authentication Methodologies → **Networking Knowledge**. No connector; it sits just above the Security Skills branch line and next to Network Protocols. A plain nearest-topic test would award it to Security Skills and Knowledge, so this is the weakest attribution.
  - CTFs (Capture the Flag) and Certifications → **Fundamental IT Skills**. No edge; they form the top-left block and Fundamental is the only plausible top-level topic.
- **Security’s top 30 subtopics have no label node.** I split them by their three visual columns; no invented group names.
- **Duplicate names are distinct nodes** and are not deduplicated: `VM` (Understand the Terminology / Basics of Virtualization), `DHCP` and `DNS` (Understand the Terminology / Functions of each), `iCloud` (Fundamental / Cloud storage), `ping`, `dig`, `arp`, `nmap`, `tracert`, `nslookup`, `ipconfig` (Networking / Security tools). `ACL` and `ACLs` are two different subtopics.
- **Android Security has zero subtopics.** Its nearest nodes are Network/Design & Architecture items, but there is no edge or column containment; listing any would be guessing.
- **Android “Dependency Injection”** is typed `subtopic` (not a paragraph) although it visually acts as a heading, so it is included; “Architectural Patterns” and “Design Patterns” are paragraphs and excluded. No android target topic exceeds 40 subtopics, so no grouping was applied there.
- The Android PNG is stale relative to the JSON (older UI/navigation nodes, no Security), so it was used only to understand column layout, never for names.
