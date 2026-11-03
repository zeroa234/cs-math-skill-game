# KTH 先修交叉核对（自动生成）

由 `scripts/build-data.mjs` 依据 `data/kth-evidence.yaml` 生成，请勿手改。KTH 课程页 “Specific prerequisites” 原文读取于 2026-11-03。

“一致”表示 KTH 要求的先修课对应的技能，落在技能树为该技能要求的必须前置链里（含它自己）。

| KTH 课程 | 对应技能 | KTH 要求的先修 → 技能 | 一致 |
|---|---|---|---|
| [DD1337 Programming](https://www.kth.se/student/kurser/kurs/DD1337?l=en) | P.1.1 程序设计基础 | 无（No information inserted） | ✓ |
| [DD1338 Algorithms and Data Structures](https://www.kth.se/student/kurser/kurs/DD1338?l=en) | F.1.1 数据结构 | DD1337 → P.1.1 程序设计基础 | ✓ |
| [ID1021 Algorithms and Data Structures](https://www.kth.se/student/kurser/kurs/ID1021?l=en) | F.1.1 数据结构 | ID1022/ID1018 → P.1.1 程序设计基础 | ✓ |
| [IS1500 Computer Organization and Components](https://www.kth.se/student/kurser/kurs/IS1500?l=en) | C.1.1 计算机组成原理 | DD1337/… → P.1.1 程序设计基础 | ✓ |
| [IS1200 Computer Hardware Engineering](https://www.kth.se/student/kurser/kurs/IS1200?l=en) | C.1.1 计算机组成原理 | 无（No information inserted） | ✓ |
| [ID1206 Operating Systems](https://www.kth.se/student/kurser/kurs/ID1206?l=en) | C.2.1 操作系统 | DD1337/… → P.1.1 程序设计基础；DD1338/…/ID1021 → F.1.1 数据结构；IS1200/IS1500/EP1200 → C.1.1 计算机组成原理 | ✓ |
| [SF1625 Calculus in One Variable](https://www.kth.se/student/kurser/kurs/SF1625?l=en) | M.1.1 极限与连续 | 无（Basic requirements.） | ✓ |
| [SF1672 Linear Algebra](https://www.kth.se/student/kurser/kurs/SF1672?l=en) | M.3.1 线性代数 | 无（Basic requirements.） | ✓ |
| [SF1624 Algebra and Geometry](https://www.kth.se/student/kurser/kurs/SF1624?l=en) | M.3.1 线性代数 | 无（Basic requirements.） | ✓ |
| [SF1626 Calculus in Several Variables](https://www.kth.se/student/kurser/kurs/SF1626?l=en) | M.1.4.1 多元微分学 | SF1625 → M.1.2 一元微分学 | ✓ |
| [SF1922 Probability Theory and Statistics](https://www.kth.se/student/kurser/kurs/SF1922?l=en) | M.6.1 概率论 | SF1673/SF1625 → M.1.3 一元积分学 | ✓ |
| [DD2421 Machine Learning](https://www.kth.se/student/kurser/kurs/DD2421?l=en) | A.2.1 监督、无监督与半监督学习 | DD1337/… → P.1.1 程序设计基础；SF1624/SF1672/SF1684 → M.3.1 线性代数；SF1626/SF1674 → M.1.4.1 多元微分学；SF1910-SF1924/SF1935 → M.6.1 概率论 | ✓ |
| [DD2424 Deep Learning in Data Science](https://www.kth.se/student/kurser/kurs/DD2424?l=en) | A.2.3 深度学习 | DD1337/… → P.1.1 程序设计基础；SF1624/SF1672/SF1684 → M.3.1 线性代数；SF1626/SF1674 → M.1.4.1 多元微分学；SF1910-SF1924/SF1935 → M.6.1 概率论；DD1420/DD2421/DD2380/ID1214 → A.2.1 监督、无监督与半监督学习 | ✓ |
| [IK2215 Advanced Internetworking](https://www.kth.se/student/kurser/kurs/IK2215?l=en) | C.3.2 网络协议、路由与传输 | 无（Knowledge in Internet technique, 6 higher education credits, equivalent completed course IK1552.） | ✓ |
| [FIK3221 Networked Systems for Machine Learning](https://www.kth.se/student/kurser/kurs/FIK3221?l=en) | C.3.5 数据中心与高性能网络 | IK2215 → C.3.2 网络协议、路由与传输；DD1310-…/DD1337 → P.1.1 程序设计基础 | ✓ |

不一致：无。
