# 宣传片：我把计算机专业做成了一款游戏

约 1 分 48 秒（107.7 s），1920×1080 / 30 fps，H.264 + AAC，响度 -16 LUFS。鲸鱼娘旁白 + 像素字幕 + 游戏自己的背景音乐和 8-bit 音效。
成片 `output/promo/cs-math-game-promo.mp4`，封面 `output/promo/cover-{16x9,4x3,3x4,9x16}.png` 和 `cover.jpg`（像素塔 + 大标题 + 鲸鱼娘姐妹半身），
混音前的画面 `cs-math-game-promo.raw.mp4`（只换 BGM 时从它重混，不用重渲）。都不入库，按下面的步骤重新生成。还没有发布。

技术栈照搬 cs-math-skill-tree 的宣传片（那边 `docs/promo-video.md`）：Remotion 画面、Blender 3D 镜头、os-review-bilingual 的 Breeze 旁白管线，画面只按“旁白说到哪个词”取帧。
这一部换成游戏自己的东西：

| | 技能树那部 | 这部 |
|---|---|---|
| 3D 镜头 | 201 个技能的发光树（Eevee 1080p） | “我的远征”的 129 个关卡（124 课 + 5 个结业挑战）沿星图学院的塔盘旋而上；**像素 3D**：640×360 不抗锯齿渲染，一套 48 色调色板无抖动量化，最近邻放大 3 倍（和 `assets/bg` 像素背景同一个做法） |
| 字 | Noto Sans SC | 游戏的像素字体 Fusion Pixel（字号取 12 px 的整数倍） |
| 框、鼠标、转场 | 圆角玻璃窗、矢量鼠标、淡入 | 游戏的像素切角边框（四道硬阴影）、像素箭头鼠标、方格有序抖动的像素溶解转场、一格一格的动画 |
| 角色 | 封面上的 deepseek 娘 | 游戏里的两位导师：截图里藏起精灵、在原位按帧播放 `assets/cast/sprites` 的动画条，所以画面里导师照样会动（施法、跳舞、害羞）；开场对白像游戏一样逐字打出 |
| 声音 | os-review 合成的 whoosh / pop | 游戏自己的 ZzFX 音效（从 `src/game/app/sound.js` 读参数离线合成）；BGM 是游戏开场曲 Grasslands（CC0） |
| 数字 | 从 skilltree.json 数 | 从 `src/gen/` 和游戏代码算：路线用游戏的 `planRoute`，复习曲线用游戏的 `review.js`（ts-fsrs），结业挑战线用 `PASS_SHARE`；“核对”那拍的终端输出是真把 `tests/content/*.verify.py` 跑一遍记下的 |

## 段落

| 拍 | 画面 | 素材 |
|---|---|---|
| cold / hook / title | 塔脚第 1 课亮起，关卡一课课往上亮；左边逐字打出提问和“上一集”（技能树宣传片封面）；说到“点亮之路”塔顶水晶亮，像素大标题 + 两位导师 | Blender（`--shot intro`） |
| cast | 游戏开场：标题卡 → 点“开始” → 妹妹的两句对白逐字打出；立绘上标出姐妹 | 截图 `intro-*` |
| route | 选远征点“继续这条” → 远征横幅“共 5 站” → 往下扫第 1 站的关卡；下方 5 站牌子和每站课数，合计 124 课 | 截图 `pick`、`route`；`facts.json` |
| lesson | 先猜 / 再看 / 再做三张快切；再演一遍先猜：选错 → 检查 → 红色反馈栏、正确项标绿、“答错不扣任何东西”，导师害羞 | 截图 `lesson-*` |
| race | 你来当调度器：按标准答案 T1 T2 T1 T1 T2 T2 一步步点，共享 x = 1；检查 → 答对了 | 截图 `race-*`（每点一下拍一张） |
| replace | 你来当 FIFO：7 次缺页各点一次要换出的页 | 截图 `replace-*` |
| lab | 九宫格：9 种交互组件在实验室里的样子 | 实验室各实验的截图 |
| boss | 结业挑战说明（第一次答对 80%）→ 点开始 → 点亮页（导师施法、跳舞，像素彩带，号角音）→ “我学会了”勾选框被打叉 | 截图 `boss-*`（真的在页面里答完 15 题） |
| review | 左：一道题每次到期都答对时的回忆概率曲线（复习日 0 / 5 / 31 / 123 / 416 天，降到 90% 回来复习）；右：游戏的复习页 | `facts.json` 的 `fsrs`；截图 `review` |
| tree | 地图 + “183 个技能”；技能页展开“换出谁”一章的“去哪深入”；必须先学（理由）和课程证据（官网先修原文） | 截图 `map`、`skill-*` |
| check | 终端里 5 条 `python -I tests/content/<技能>.verify.py` 和真实的最后一行（共 957 处） | `verify.json` |
| outro | 三台手机（营地、远征、上课）+ “安卓 App / 电脑版 / 离线 / 不用注册”；说到“一路点亮”整条路变金，落版标题、GitHub、署名 | Blender（`--shot outro`）、截图 `phone-*` |

片尾署名：导师角色设计 ZipZipPipe（CC BY-NC 4.0，许可要求署名）、背景音乐 Juhani Junkala《Grasslands》（CC0）、像素字体 Fusion Pixel（OFL）。

## 生成步骤（项目根目录，Git Bash）

```bash
npm run build                               # 截图拍的是 output/web（构建好的游戏）
# 1. 旁白：复用 os-review-bilingual 的 Breeze 管线（鲸鱼娘参考音频 + 讲解语气，配置在那边的 config/tts-breeze.json）
wsl -e bash -lc "bash /mnt/d/agent/projects/os-review-bilingual/scripts/start-breeze.sh"     # 起服务，等 http://127.0.0.1:7861/health 返回 ok
python -X utf8 ../os-review-bilingual/scripts/narrate.py data/promo/script.json --lang zh --out output/promo/narration
N=/mnt/d/agent/projects/cs-math-skill-game/output/promo/narration
wsl -e bash -lc "cd /mnt/d/agent/projects/os-review-bilingual && ~/vd/venv-qfa/bin/python scripts/align-narration.py $N && ~/vd/venv-asr/bin/python scripts/qc-narration.py $N"
wsl -e bash -lc "systemctl --user stop vd-breeze-api"                                           # 合成完释放显存
python -X utf8 ../os-review-bilingual/scripts/timeline.py data/promo/script.json --lang zh --nar output/promo/narration --out src/promo/public/build
node scripts/promo/word-times.mjs           # → src/promo/public/build/words.json（逐字帧号）
# 2. 数据、截图、音效、素材副本
node scripts/promo/build-facts.mjs          # → build/facts.json；和旁白念的数对不上就报错
node scripts/promo/verify-log.mjs           # → build/verify.json（真跑 5 个内容核对脚本，P.2.2、C.2.1 用 WSL 的 gcc，约 1 分钟）
node scripts/promo/capture-game.mjs         # → src/promo/public/shots/*.png + shots.json（约 3.5 分钟）
node scripts/promo/sfx.mjs                  # → src/promo/public/sfx/*.wav（游戏的 ZzFX 音效）
node scripts/promo/assets.mjs               # 字体、导师素材、背景、技能树宣传片封面、两个过渡音的副本
(cd src/promo && npm install)
# 3. Blender 两段（读 timeline.json / words.json / facts.json，旁白改了要重渲）
bash scripts/promo/render-blender.sh        # → src/promo/public/blender/intro.mp4、outro.mp4
# 4. 先抽帧看版面，再出成片
(cd src/promo && TEMP=D:/agent/projects/cs-math-skill-game/temp/promo/tmp node stills.mjs --every 2.5)   # → temp/promo/stills/sheet.jpg
bash scripts/promo/render.sh                # Remotion 渲染 + 混 BGM + -16 LUFS → output/promo/cs-math-game-promo.mp4
# 5. 封面（Remotion 静帧，背景是 Blender 片尾第 300 帧的原始 PNG）
node scripts/promo/cover.mjs                # → output/promo/cover-*.png、cover.jpg
rm -rf temp/promo/blender/intro temp/promo/blender/outro/0[0-2]* # Blender 的 PNG 帧编成 mp4 后可删（留 outro/0300.png 给封面）
```

文稿 `data/promo/script.json` 只有中文，数字写汉字（送 TTS 的就是原文）。改了文稿：重跑第 1 步（只重合成改过的拍）、Blender 两段和成片。只改某拍的最短时长（`min`）：不用重合成，从 `timeline.py` 往下跑。只改画面代码：直接第 4 步。

各步用时（RTX 3080，16 线程）：Breeze 13 拍 40 s；对齐 + ASR 质检约 1 分钟；截图约 3.5 分钟；Blender 两段渲染 + 量化编码约 8 分钟（640×360、16 采样）；抽帧 42 张约 1.5 分钟；成片渲染 + 混音约 10 分钟（并发 6）；封面 4 张约 30 s。

## 依赖本仓库以外的东西

宣传片是在作者本地的工作区里做的，下面这些在同一工作区的其他项目里（路径按 `projects/<项目>/` 并排），不在本仓库：

- `os-review-bilingual`：旁白管线（Breeze TTS 2 服务、对齐、质检、`timeline.py`、`mix-bgm.py` / `loudnorm.py`）、开场和片尾的两个过渡音（`video/public/sfx` 的 riser、whoomp，代码合成）。
- `cs-math-skill-tree`：开场“上一集”的缩略图（`docs/images/cover.webp`）；`word-times.mjs`、`stills.mjs` 和画面的镜头 / 时刻函数照搬自那边的 `src/promo/`。

所以在别的机器上，第 1 步（旁白）要换成自己的配音；截图、数据、音效、Blender 场景和 Remotion 画面只依赖本仓库（加上 `../cs-math-skill-tree` 的那张缩略图）。

## 画面代码

`src/promo/`（Remotion 4.0.533，和技能树那边同版本）：

- `src/lib/core.ts`：尺寸、游戏深色主题的配色、数据、取时刻。画面只按“拍”和“旁白说到哪个词”取帧号：`w("race", "竞态")` 返回说到这个词的那一帧，找不到直接报错。
- `src/lib/ui.tsx`：像素边框 `frame()`、夜空背景、字幕（游戏对白框配色）、音效、截图窗口 `AppWindow` + 镜头 `Shot` / `camAt`、像素鼠标 `Cursor`、描边 `Glow`、标注 `Tag`、打字机 `TypeText` / `TypeBlips`、像素溶解 `Wipe`、像素彩带 `Confetti`。
- `src/lib/sprite.tsx`：导师精灵，和游戏 `cast.jsx` 同一套“舞台”摆法，帧号按视频帧算。
- `src/scenes/`：`Intro`、`Desk`（开场对白到页面置换，同一个窗口连着演）、`Lab`、`Boss`、`Review`、`Tree`、`Check`、`Outro`。`Promo.tsx` 叠在一起，段与段之间放 `Wipe`。`Cover.tsx` 是封面的四种尺寸（`Cover-16x9` 等）。
- 窗口是 1584×891，下面留出字幕的位置：游戏底部的反馈栏不会被字幕压住。截图视口 1216×684（3 倍像素），窗口里正好 1.3 倍。
- 字幕在屏幕上已有同样大字的拍（hook、title）不出。

## 用到的现成组件

- Remotion（画面合成）、Blender 5.2 Eevee + 合成器的雾（Mist pass）和 Bloom、ffmpeg 的 `palettegen` / `paletteuse`（调色板量化）和最近邻缩放、playwright-core + 系统 Edge（截图，共用 `scripts/lib/edge.mjs`）。
- 游戏本身：`tests/lib/play.mjs` 的答题函数（截图时按正确答案往前走）、`src/game/core/graph.js` 的 `planRoute`、`review.js`（ts-fsrs）、`lesson.js` 的 `PASS_SHARE`、ZzFX 1.4.0 的 `buildSamples`。
- os-review-bilingual 的旁白管线和 `mix-bgm.py`；BGM 是游戏自带的 `assets/music/grasslands.ogg`（Juhani Junkala，CC0，来源见 `assets/music/README.md`）。
- 自己写的：`scripts/promo/` 的截图、数据、音效离线合成、Blender 场景、封面脚本，和 `src/promo/` 的画面。

## 坑

- 截图要可复现：存档里打开“减少动画”（`settings.reduceMotion`），角色不动、不放彩带、开场文字直接显示；动的部分都在视频里补（精灵、打字机、彩带）。
- 开场对白第 3 句要从第 1 句点两下（第 2 句是姐姐说的）；每点一下前都等文字出完，否则这一下只是“把这句打完”。
- 页面置换每一步的可选页顺序跟着页框变，按截图里记下的 `labels` 找要点的那个，不按位置。
- Remotion 第一次渲染会下载自己的无头浏览器到 cwd 的 `node_modules/.remotion`（约 110 MB）：脚本都在 `src/promo` 里跑，别在项目根目录跑出第二份。
- Remotion 会往系统 TEMP 写打包副本和 Chrome 配置：渲染、抽帧前把 `TEMP` / `TMP` 指到 `temp/promo/tmp`，完了删掉（`render.sh`、`stills.mjs`、`cover.mjs` 已处理）。
- Blender 像素画：`render.filter_size = 0` 才是硬边；量化要两段共用一套调色板（各取 12 帧统计），否则段与段、帧与帧之间颜色会跳。中间片用 yuv444p，像素边上不串色。
- 发光太强会把领域色洗成白色：关卡发光强度 2.2 × 0.75，只在亮起的那一下冲到白。
