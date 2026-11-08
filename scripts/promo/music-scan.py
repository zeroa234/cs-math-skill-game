"""配乐候选初筛：每首曲子的长度、速度（librosa beat_track）和每 2 秒一格的响度曲线（RMS dB），
打印成一行“火花线”，用来挑有前奏、渐强、高潮的曲子（PV）和平稳轻快的曲子（广告垫底）。
听不到声音，这只是结构上的初筛，最后由用户试听定。
用法（WSL，librosa 在 ~/vd/venv-asr）：python music-scan.py <曲子目录> [...] > 结果.txt
"""
import sys, glob, os
import numpy as np, librosa

BARS = " ▁▂▃▄▅▆▇█"
for d in sys.argv[1:]:
    for f in sorted(glob.glob(os.path.join(d, "*.wav"))):
        y, sr = librosa.load(f, sr=22050, mono=True)
        dur = len(y) / sr
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
        hop = sr * 2
        rms = np.array([np.sqrt(np.mean(y[i:i + hop] ** 2) + 1e-12) for i in range(0, len(y) - hop // 2, hop)])
        db = 20 * np.log10(rms)
        top = db.max()
        line = "".join(BARS[int(np.clip((v - (top - 24)) / 24 * 8, 0, 8))] for v in db)
        onset = librosa.onset.onset_strength(y=y, sr=sr)
        print(f"{os.path.basename(f)[:-4]:32s} {dur:6.1f}s {float(np.atleast_1d(tempo)[0]):6.1f}bpm  range {db.max()-np.percentile(db,10):4.1f}dB  {line}")
