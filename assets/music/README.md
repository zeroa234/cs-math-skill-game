# 背景音乐

25 首曲子，全部来自 OpenGameArt，**每个包的许可证都是 CC0（公有领域）**：可以自由使用、修改、商用，不要求署名。游戏仍在“我的 → 设置 → 音乐来源”里列出作者。许可证于 2026-11-03 在每个包的页面上逐个核对过。

清单和来源链接在 `data/music.yaml`，这个目录里的 `<曲目 id>.ogg` 由 `node scripts/music/encode-music.mjs` 生成，可以重做：

1. 按清单下载每个包到 `temp/music-src/<包>/`（zip 会解开；已经下载过的直接用）。
2. 用 ffmpeg 的 `ebur128` 滤镜量每首的响度和真峰值，整首乘同一个增益，统一到 -18 LUFS（真峰值不超过 -1 dBTP）。只调增益，不用动态压缩，所以原本能无缝循环的曲子仍然能无缝循环。
3. 编码为 Opus 64 kbit/s、48 kHz 立体声（`.ogg`），去掉元数据。安卓 WebView、Edge、Chrome、Firefox 都能播放。

| 来源 | 作者 | 用在哪 |
|---|---|---|
| [JRPG Music Pack #1–#5（取 1、2、4、5）](https://opengameart.org/content/jrpg-pack-1-exploration) | Juhani Junkala（SubspaceAudio） | “像素 RPG”：探索、城镇、平静、战斗四类分别对应开场和营地、上课、结业挑战 |
| [4 Chiptunes (Adventure)](https://opengameart.org/content/4-chiptunes-adventure)、[5 Chiptunes (Action)](https://opengameart.org/content/5-chiptunes-action) | Juhani Junkala（SubspaceAudio） | “8-bit 芯片” |
| [Medieval: The Bard's Tale / The Old Tower Inn / Minstrel Dance / King's Feast / Battle](https://opengameart.org/content/medieval-the-bards-tale)，以及 Old Tower Inn 的芯片版 | RandomMind | “中世纪奇幻”；芯片版的 Old Tower Inn 用在“8-bit 芯片”的上课场景 |
| [Chill Beats (Collection)](https://opengameart.org/content/chill-beats-collection)（取 Families、Opinions、Autumn） | HoliznaCC0 | “Lo-fi 学习” |

选曲依据：作曲者给的情绪分类（包名里的 Exploration / Towns / Calm / Action，或曲名）、下载量和评论、能不能无缝循环。**选曲的人（主代理）听不到声音**，好不好听要靠真人试听；换曲子只需改 `data/music.yaml`，再跑编码脚本和 `npm run build`。

没有用上的：Kenney 的 85 段短曲（CC0）。不听没法判断哪段听起来像“成功”，现在庆祝页仍然用程序合成的音效。

体积：25 首共约 18 MB，App 安装包因此从约 9.5 MB 变成约 27 MB。
