# 像素背景

本机 ComfyUI 模板 `moss-sft-dual-lora`（MOSS SFT + 观澜 + FKEY LoRA，50 步，1536×864）生成，再用 `scripts/cast/pixelize-bg.py` 面积缩小到 480×270、48 色无抖动量化（和 `projects/kabu-quest` 同一个做法）。游戏里用 `image-rendering: pixelated` 放大显示。2026-11-03 生成；本机当时没有 Anima / Krea2 底模，所以用 MOSS。

| 文件 | 用在 | seed | 画面 |
|---|---|---|---|
| `title.png` | 开场、还没选远征的营地 | 20261103 | 夜晚山丘上的魔法学院，星星连成一棵树 |
| `lane-c.png` | 系统与网络领域（我的远征：操作系统） | 20261104 | 齿轮法塔内部，水晶处理器核心、电路符文 |
| `lane-a.png` | 人工智能领域 | 20261105 | 黄昏森林，树枝间发光的“神经网络”光线 |
| `route-cloud.png` | 推荐远征：云与运维 | 20261106 | 夜里的服务器塔城市，光桥连着中央交换枢纽 |
| `lane-f.png` | 理论领域 | 20261107 | 书架迷宫图书馆，地上发光的图、沙漏和罗盘 |
| `lane-math.png` | 三个数学领域 | 20261108 | 山顶天文台，铜望远镜，天上发光的几何图形和螺线 |
| `lane-p.png` | 程序设计领域 | 20261109 | 白天河边的工匠村，工作台上拼接彩色积木，屋顶间的绳桥 |
| `lane-d.png` | 数据领域 | 20261110 | 地下档案大厅，成排发光的水晶抽屉，卡片沿轨道滑进分拣机 |
| `lane-s.png` | 安全领域 | 20261111 | 夜里山上的要塞，刻着发光盾纹的城墙、大锁、探照灯 |
| `lane-h.png` | 硬件与嵌入式领域 | 20261112 | 建在绿色电路板上的小镇，芯片像楼房，铜线像道路 |
| `lane-v.png` | 图形与交互领域 | 20261113 | 塔楼里的光之画室，漂浮的画布和几何体，棱镜折光 |
| `lane-i.png` | 信息系统领域 | 20261114 | 黄昏的港口小镇，钟楼、贴着航线的地图板、信鸽 |
| `route-enterprise.png` | 推荐远征：企业与桌面应用 | 20261115 | 剖面的公会大楼，成排的书桌和档案柜、墙上的蓝图、气动传送管 |
| `route-mobile.png` | 推荐远征：手机应用 | 20261116 | 夜市街道，许多发光的小玻璃板像灯笼一样挂着，电车 |

**怎么选图**（`src/game/app/art.js`）：路线在 `data/routes.yaml` 里写了 `art` 就用它；否则用目标技能所在领域的图。这样“我的远征”和以后玩家自己定的任何目标都有合适的背景，不用逐个画。同一领域有两条推荐路线时（网站和企业应用、手机应用都在程序设计领域；云与运维和我的远征都在系统领域），后来的那条配一张专属图。

2026-11-03 第二批（seed 20261108 起）用同一个模板、同样的提示词格式和负面词生成。`route-mobile.png` 的电车招牌上生成出了 “FKEY” 字样（画风 LoRA 的触发词），像素化后把招牌那 17×8 像素填成招牌底色。

提示词都以 `<|artist|>fkey<|/artist|>` 开头，接英文描述：“Pixel art style … 16-bit retro game look, scenery only, no people, no text. …（场景）… flat colors, crisp blocky pixels, limited palette, readable and calm.” 负面：people, person, girl, boy, character, text, letters, watermark, logo, signature, blurry, photo, 3d render。完整原文在 ComfyUI 输出图的元数据里（`D:/agent/output/comfyui/<job>/`，节点 57 是正向提示词）。
