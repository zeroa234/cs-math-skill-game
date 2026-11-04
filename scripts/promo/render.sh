#!/usr/bin/env bash
# 宣传片成片：Remotion 整片渲染 → 混 BGM（旁白旁链压低）+ 统一响度 → output/promo/cs-math-game-promo.mp4
# 用法（Git Bash，项目根目录）：bash scripts/promo/render.sh
# 前提：旁白、时间轴、截图、音效、Blender 两段都已生成（顺序见 docs/promo-video.md）。约 10–15 分钟。
set -euo pipefail
cd "$(dirname "$0")/../.."
OSR=../os-review-bilingual
# 游戏“像素 RPG”风格的开场曲：Juhani Junkala《Grasslands》（JRPG Music Pack #1，CC0，来源见 assets/music/README.md）
BGM=${BGM:-assets/music/grasslands.ogg}
mkdir -p output/promo temp/promo/tmp
export TEMP; TEMP=$(cygpath -w "$PWD/temp/promo/tmp"); export TMP=$TEMP   # Remotion 的打包副本、Chrome 配置别写系统盘
node scripts/promo/build-facts.mjs
node scripts/promo/word-times.mjs
(cd src/promo && npx remotion render src/index.ts Promo ../../output/promo/cs-math-game-promo.raw.mp4 --concurrency=6 --log=error)
python -X utf8 "$OSR/scripts/mix-bgm.py" output/promo/cs-math-game-promo.raw.mp4 output/promo/cs-math-game-promo.mp4 \
  --key src/promo/public/build/narration.wav --bgm "$BGM"
rm -rf temp/promo/tmp/remotion-* temp/promo/tmp/puppeteer_dev_chrome_profile-* 2>/dev/null || true
ffprobe -v error -show_entries format=duration:stream=codec_name -of compact output/promo/cs-math-game-promo.mp4
