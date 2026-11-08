"""配乐的拍点网格：beat_this（CPJKU，现成的拍点 + 强拍检测）算拍和小节的起点，
再按小节量响度（RMS dB），写成 JSON 给 Remotion 卡拍用（src/promo/public/build/beats-<名>.json）。
用法（WSL）：PYTHONPATH=temp/pylib TORCH_HOME=temp/torch ~/vd/venv-asr/bin/python scripts/promo/beats.py <音频> <输出.json>
"""
import sys, json
import numpy as np, soundfile as sf
from beat_this.inference import File2Beats

src, out = sys.argv[1], sys.argv[2]
beats, downs = File2Beats(checkpoint_path="final0", device="cpu", dbn=False)(src)
y, sr = sf.read(src, always_2d=True)
y = y.mean(axis=1)
def db(a, b):
    seg = y[int(a * sr):int(b * sr)]
    return round(float(20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-9)), 1) if len(seg) else None
bars = [{"t": round(float(t), 3), "db": db(t, downs[i + 1] if i + 1 < len(downs) else len(y) / sr)} for i, t in enumerate(downs)]

# 恒定速度的拍网格：游戏配乐多是宿主软件按固定速度导出的，检测出的拍在安静段会跳成半拍或错位。
# 用拍间隔接近中位数（±10%）的那些拍做最小二乘 t = t0 + P·k，再按检测到的强拍多数票定小节从第几拍开始。
P = float(np.median(np.diff(beats)))
good = [i for i in range(len(beats) - 1) if abs(beats[i + 1] - beats[i] - P) < 0.1 * P]
k = np.round((beats[good] - beats[good[0]]) / P)
A = np.vstack([np.ones_like(k), k]).T
t0, P = np.linalg.lstsq(A, beats[good], rcond=None)[0]
t0 -= np.ceil(t0 / P) * P if t0 > 0 else 0          # 让 t0 落在第一拍之前最近的格点上（可为负）
while t0 + P < 0: t0 += P
phase = np.bincount([int(round((d - t0) / P)) % 4 for d in downs], minlength=4).argmax()
resid = np.abs((beats - t0) / P - np.round((beats - t0) / P)) * P
grid = {"t0": round(float(t0 + phase * P), 4), "beat": round(float(P), 5), "beats_per_bar": 4,
        "fit_beats": len(good), "median_resid_s": round(float(np.median(resid)), 4)}
json.dump({"source": src, "duration": round(len(y) / sr, 3), "bpm": round(float(60 / P), 2), "grid": grid,
           "beats": [round(float(t), 3) for t in beats], "bars": bars}, open(out, "w"), indent=1)
print("grid", grid)
print(f"{len(beats)} beats, {len(downs)} bars, bpm {60 / np.median(np.diff(beats)):.1f}")
for i, b in enumerate(bars):
    print(f"bar {i:3d} {b['t']:7.2f}s {b['db']:6.1f} dB " + "#" * max(0, int((b['db'] + 40))))
