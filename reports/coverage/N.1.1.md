# N.1.1 大学物理：力学与热学：覆盖表

**状态（2026-11-23）：已写完（22 课，67/67 节，check-pack、check-coverage、verify.py 157 项、FULL e2e 通过）。** 依据 `../cs-math-skill-tree/data/outlines/N.1.1.json`（主来源 OpenStax *University Physics* 第一卷第 3–11 章、第二卷第 2–4 章）、`data/curation/learning-paths/N.1.1.json`（北京理工大学《大学物理—力学与热学》国家精品课与 B 站录像目录）和原技能树综合练习 7 小题。数值核对脚本 `tests/content/N.1.1.verify.py`。

前置：必须前置只有 M.1.2 一元微分学（导数、链式法则可直接用）。推荐前置 M.4.1 向量代数还没有内容包，所以矢量的分量、点乘、叉乘的方向在课里用到时现讲；推荐前置 M.1.3 一元积分学不在必须前置链上，课里需要“积分”的地方都先用“图像下的面积”讲，再说明它记作 $\int$。

## 大纲逐节

| 节 | 原文 | 课 |
|---|---|---|
| 1.1 | Position, Displacement, and Average Velocity | `position-velocity` |
| 1.2 | Instantaneous Velocity and Speed | `position-velocity` |
| 1.3 | Average and Instantaneous Acceleration | `position-velocity` |
| 1.4 | Motion with Constant Acceleration | `constant-acceleration` |
| 1.5 | Free Fall | `constant-acceleration` |
| 1.6 | Finding Velocity and Displacement from Acceleration | `constant-acceleration` |
| 2.1 | Displacement and Velocity Vectors | `vectors-projectile` |
| 2.2 | Acceleration Vector | `vectors-projectile` |
| 2.3 | Projectile Motion | `vectors-projectile` |
| 2.4 | Uniform and Nonuniform Circular Motion | `circular-relative` |
| 2.5 | Relative Motion in One and Two Dimensions | `circular-relative` |
| 3.1 | Forces | `newton-laws` |
| 3.2 | Newton's First Law | `newton-laws` |
| 3.3 | Newton's Second Law | `newton-laws` |
| 3.4 | Mass and Weight | `newton-laws` |
| 3.5 | Newton's Third Law | `newton-laws` |
| 3.6 | Common Forces | `forces-friction` |
| 3.7 | Drawing Free-Body Diagrams | `forces-friction` |
| 4.1 | Solving Problems with Newton's Laws | `forces-friction` |
| 4.2 | Friction | `forces-friction` |
| 4.3 | Centripetal Force | `centripetal-drag` |
| 4.4 | Drag Force and Terminal Speed | `centripetal-drag` |
| 5.1 | Work | `work-energy` |
| 5.2 | Kinetic Energy | `work-energy` |
| 5.3 | Work-Energy Theorem | `work-energy` |
| 5.4 | Power | `work-energy` |
| 6.1 | Potential Energy of a System | `potential-conservation` |
| 6.2 | Conservative and Non-Conservative Forces | `potential-conservation` |
| 6.3 | Conservation of Energy | `potential-conservation` |
| 6.4 | Potential Energy Diagrams and Stability | `potential-conservation` |
| 6.5 | Sources of Energy | `potential-conservation` |
| 7.1 | Linear Momentum | `momentum-impulse` |
| 7.2 | Impulse and Collisions | `momentum-impulse` |
| 7.3 | Conservation of Linear Momentum | `momentum-impulse` |
| 7.4 | Types of Collisions | `collisions` |
| 7.5 | Collisions in Multiple Dimensions | `collisions` |
| 7.6 | Center of Mass | `center-of-mass-rocket` |
| 7.7 | Rocket Propulsion | `center-of-mass-rocket` |
| 8.1 | Rotational Variables | `rotation-kinematics` |
| 8.2 | Rotation with Constant Angular Acceleration | `rotation-kinematics` |
| 8.3 | Relating Angular and Translational Quantities | `rotation-kinematics` |
| 8.4 | Moment of Inertia and Rotational Kinetic Energy | `inertia-torque` |
| 8.5 | Calculating Moments of Inertia | `inertia-torque` |
| 8.6 | Torque | `angular-momentum-particle`、`inertia-torque` |
| 8.7 | Newton's Second Law for Rotation | `inertia-torque` |
| 8.8 | Work and Power for Rotational Motion | `inertia-torque` |
| 9.1 | Rolling Motion | `rolling-gyroscope` |
| 9.2 | Angular Momentum | `angular-momentum-particle`、`rolling-gyroscope` |
| 9.3 | Conservation of Angular Momentum | `angular-momentum-particle`、`rolling-gyroscope` |
| 9.4 | Precession of a Gyroscope | `rolling-gyroscope` |
| 10.1 | Molecular Model of an Ideal Gas | `gas-molecules` |
| 10.2 | Pressure, Temperature, and RMS Speed | `gas-molecules` |
| 10.3 | Heat Capacity and Equipartition of Energy | `equipartition-distribution` |
| 10.4 | Distribution of Molecular Speeds | `equipartition-distribution` |
| 11.1 | Thermodynamic Systems | `first-law` |
| 11.2 | Work, Heat, and Internal Energy | `first-law` |
| 11.3 | First Law of Thermodynamics | `first-law` |
| 11.4 | Thermodynamic Processes | `thermo-processes` |
| 11.5 | Heat Capacities of an Ideal Gas | `thermo-processes` |
| 11.6 | Adiabatic Processes for an Ideal Gas | `thermo-processes` |
| 12.1 | Reversible and Irreversible Processes | `heat-engines` |
| 12.2 | Heat Engines | `heat-engines` |
| 12.3 | Refrigerators and Heat Pumps | `heat-engines` |
| 12.4 | Statements of the Second Law of Thermodynamics | `carnot-entropy` |
| 12.5 | The Carnot Cycle | `carnot-entropy` |
| 12.6 | Entropy | `carnot-entropy` |
| 12.7 | Entropy on a Microscopic Scale | `carnot-entropy` |

## CS2023 核心主题（C2）

`scope.json` 对 N.1.1 只给了国标物理学类的两条（0806-1.1.1 牛顿力学、热学），没有 CS2023 主题。两条分别由第 1–5 章的课和第 6–7 章的课负责。

## 学习资源的章节（C3）

- en1/en2（OpenStax 第一卷第 3–11 章、第二卷第 2–4 章）：就是上面的大纲，逐节落课。
- zh2（北京理工大学录像目录）里比 OpenStax 多出的点：惯性力与潮汐、玻尔兹曼分布、平均碰撞频率。惯性力在 `centripetal-drag` 讲（非惯性系里的离心惯性力）；平均自由程和平均碰撞频率在 `equipartition-distribution` 讲；玻尔兹曼分布只在 `equipartition-distribution` 用一句话说明“高度越高分子越稀”的指数规律，不展开推导（超出入门层）；潮汐不教（属于万有引力，大纲说明本技能不收第 13 章）。
- 万有引力定律（zh2 的 2.2.6）：大纲不收第 13 章，`newton-laws` 只把重力写成 $mg$，并在“常见力”里说明 $g$ 来自地球的引力。

## 原技能树综合练习（C4）

| 小题 | 内容 | 由哪一课教到 |
|---|---|---|
| (1) | 抛体的飞行时间、射程、最大高度 | `vectors-projectile` |
| (2) | 斜面上有摩擦的下滑加速度 | `forces-friction` |
| (3) | 完全非弹性碰撞的末速度和动能损失 | `collisions` |
| (4) | 圆盘 + 绳 + 物块的加速度、角加速度、拉力 | `inertia-torque` |
| (5) | 滑冰运动员收臂后的转速 | `rolling-gyroscope` |
| (6) | 等温膨胀做功与吸热、卡诺效率 | `thermo-processes`、`carnot-entropy` |
| (7) | 氮气的方均根速率 | `gas-molecules` |

## 后继技能用到的写法（C5）

必须后继：N.1.2 大学物理：电磁学（还没有内容包），E.1.8 卫星导航与定位（还没有内容包）。N.1.2 的大纲直接用到：矢量和分量、力与牛顿第二定律、功、势能与保守力、动能、圆周运动的向心加速度、动量。这些都在本包讲到，并写进 `terms`，后面的包可以直接继承查词。
