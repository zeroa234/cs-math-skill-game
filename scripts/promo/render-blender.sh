#!/usr/bin/env bash
# 渲像素 3D 的开场、片尾两段（Blender 5.2 Eevee，640×360），量化成一套固定的 48 色调色板（无抖动，和 assets/bg 像素背景同一个做法）、
# 最近邻放大 3 倍到 1920×1080，编成 Remotion 读的 mp4（4:4:4，像素边上不串色）。约 5–8 分钟（RTX 3080）。
# 用法（Git Bash，项目根目录）：bash scripts/promo/render-blender.sh [intro|outro ...]
# 依赖：src/promo/public/build/{timeline,words,facts}.json（动画时刻跟旁白走，旁白改了要重渲）
set -euo pipefail
cd "$(dirname "$0")/../.."
B=${BLENDER:-D:/steam/steamapps/common/Blender/blender.exe}
mkdir -p temp/promo/logs src/promo/public/blender
shots=${*:-intro outro}
for s in $shots; do
  rm -rf "temp/promo/blender/$s"
  "$B" -b --factory-startup -P scripts/promo/blender-route.py -- --shot "$s" --out "temp/promo/blender/$s" --samples 16 \
    > "temp/promo/logs/blender-$s.log" 2>&1 || { tail -20 "temp/promo/logs/blender-$s.log"; exit 1; }
  echo "$s: $(ls temp/promo/blender/$s | wc -l) 帧"
done
# 一套调色板给两段共用（各取 12 帧统计），两段之间、帧与帧之间颜色不跳
pal=temp/promo/blender/palette.png
files=()
for s in intro outro; do
  n=$(ls temp/promo/blender/$s | wc -l)
  for k in 1 2 3 4 5 6 7 8 9 10 11 12; do files+=(-i "temp/promo/blender/$s/$(printf %04d $(( (n - 1) * k / 12 ))).png"); done
done
ffmpeg -nostdin -y -loglevel error "${files[@]}" -filter_complex "$(for i in $(seq 0 23); do printf "[%d]" $i; done)concat=n=24:v=1,palettegen=max_colors=48:stats_mode=full:reserve_transparent=0" "$pal"
for s in $shots; do
  ffmpeg -nostdin -y -loglevel error -framerate 30 -start_number 0 -i "temp/promo/blender/$s/%04d.png" -i "$pal" \
    -lavfi "[0][1]paletteuse=dither=none,scale=1920:1080:flags=neighbor,format=yuv444p" -c:v libx264 -preset slow -crf 10 "src/promo/public/blender/$s.mp4"
  echo "$s → src/promo/public/blender/$s.mp4"
done
