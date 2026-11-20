# 角色（导师）

游戏里的两位导师是鲸鱼娘姐妹：**鲸鱼姐姐**（蓝发，活泼，课里陪练，代码里 `blue`）和**鲸鱼妹妹**（黑发，沉稳，开场讲解、复习时陪着，代码里 `black`）。设定里姐姐反而更孩子气、妹妹更成熟。换角色只需替换这个目录并改 `src/game/ui/cast.jsx` 里的 `CAST`；没有这个目录时（或 `CAST=none`）游戏照常构建，只是没有导师。

## 署名和许可

角色设计作者 **ZipZipPipe**，许可 [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)。这个目录里的素材和本游戏一样按 CC BY-NC 4.0 发布：可以分享和改编，要同时署名角色设计者 ZipZipPipe 和本项目，不能商用。署名也写在 `README.md` 的“署名”、`LICENSE` 和游戏里“我的 → 角色来源”。本游戏做的改动：

- 蓝发姐姐的立绘：原画去掉了背景（用图像模型抠的）。
- 黑发妹妹：在原设计上衍生的黑色女仆版（同一画风的立绘和三视图）。
- Q 版像素精灵：参考两位角色的立绘生成 Q 版多动作（短裙以便看清步态、坐姿和跳跃动作），经色键去背景、按 240 px 高度（约 256×256 级高分辨率像素）缩放到统一 96 色调色板并对齐脚部锚点，合成为逐帧抽帧播放的 WebP 精灵带。

## 文件

| 文件 | 内容 | 怎么做的 |
|---|---|---|
| `sprites/<角色>/<动作>.webp`、`sprites.json` | Q 版像素小人的 12 个动作：待机、走、挥手、跳舞/施法、跳（起跳、空中、落地）、害羞、坐、思考、看书讲解、欢呼 | 由 `source/whale-*-chibi-sheet*.jpg` 经 `scripts/cast/build-chibi-sprites.py` 切分、色键抠图、高清像素化限色并合成为无损 WebP 动画带；`sprites.json` 记每条的尺寸、帧数、帧率、脚的位置和缩放基准（`unit`） |
| `portraits/blue.webp`、`portraits/black.webp` | 开场和对白里的立绘 | 由 `source/whale-blue-portrait.png`、`source/whale-black-portrait.png`（透明背景的原图）经 `scripts/cast/make-portraits.py` 得到：按不透明区域裁边，缩到 1200px 高（先预乘透明度再 Lanczos，边缘不发黑），存成 WebP（质量 90，透明度无损） |
