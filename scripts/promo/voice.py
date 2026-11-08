"""广告向配音：Breeze TTS 2 整批合成（data/promo/voices.json 的候选 × data/promo/ad.json 的台词）。

用法：python scripts/promo/voice.py [--cand blue-direct,black-design] [--only a01,a02] [--sample] [--seeds 3]
  不给 --cand：试听阶段合成全部候选；定了以后用 voices.json 的 pick。
  --sample：只合成样片要的几句（ad.json 里 sample: true）。
  --seeds N：每句抽 N 个种子（seed, seed+1, …），挑结尾没被切、时长合适的一条（见下）。
输出：src/promo/public/build/voice/<候选>/<句 id>.wav，和 manifest.json（每句的文本、种子、时长、结尾电平）。

服务先起：wsl -e bash -lc "bash /mnt/d/agent/projects/os-review-bilingual/scripts/start-breeze.sh"
接口和用法依据 ~/vd/breeze-tts/README.md（Voice Clone / Voice Design / Voice Direction、Batch API）。
尾字截断：Breeze 偶尔在最后一个字没念完时就结束（os-review-bilingual 实测，句号结尾约 6–7%，问号、感叹号几乎没有）。
用 os-review-bilingual/scripts/narrate.py 同一个判据（最后 20 ms 的电平比有声帧中位电平高于 -25 dB 算被切），
多抽几个种子，留结尾最干净的一条。
"""
from __future__ import annotations

import argparse
import io
import json
import math
import sys
import time
import wave
from array import array
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "src/promo/public/build/voice"
SR_LEAD, FADE = 0.05, 0.005


def tail_db(a: array, sr: int) -> float:
    """结尾电平（照抄 os-review-bilingual/scripts/narrate.py 的 tail_db，判据见那里的注释）。"""
    n = round(sr * 0.02)
    end = len(a)
    while end > n and abs(a[end - 1]) <= 3:
        end -= 1
    rms = [math.sqrt(sum(x * x for x in a[i:i + n]) / n) for i in range(0, end - n + 1, n)]
    peak = max(rms)
    voiced = sorted(r for r in rms if r > peak * 10 ** (-35 / 20))
    last = math.sqrt(sum(x * x for x in a[end - n:end]) / n)
    return round(20 * math.log10(max(last, 1e-6) / voiced[len(voiced) // 2]), 1)


def synth(cfg: dict, cand: dict, texts: list[str], seed: int) -> tuple[list[array], int]:
    data = {"texts": json.dumps(texts, ensure_ascii=False), "cfg_scale": str(cfg["cfg_scale"]), "seed": str(seed),
            "instruction": cand["instruction"]}
    files = None
    if cand["ref"]:
        ref = (ROOT / cfg["reference"]["audio"]).resolve()
        data["ref_text"] = cfg["reference"]["text"]
        files = {"ref_audio": (ref.name, ref.read_bytes(), "audio/wav")}
    r = requests.post(f"{cfg['url']}/v1/audio/speech/batch", data=data, files=files, timeout=3600)
    if r.status_code != 200:
        raise RuntimeError(f"{r.status_code}: {r.text[:300]}")
    sizes = [int(n) for n in r.headers["X-Segment-Bytes"].split(",")]
    segs, o = [], 0
    for n in sizes:
        segs.append(array("h", r.content[o:o + n]))
        o += n
    return segs, int(r.headers["X-Sample-Rate"])


def write(path: Path, a: array, sr: int):
    a = array("h", a)
    for i in range(min(len(a), round(FADE * sr))):
        a[i] = round(a[i] * i / (FADE * sr))
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(bytes(2 * round(SR_LEAD * sr)) + a.tobytes())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cand")
    ap.add_argument("--only")
    ap.add_argument("--sample", action="store_true")
    ap.add_argument("--seeds", type=int, default=3)
    args = ap.parse_args()
    cfg = json.loads((ROOT / "data/promo/voices.json").read_text("utf-8"))
    lines = json.loads((ROOT / "data/promo/ad.json").read_text("utf-8"))["lines"]
    if args.sample:
        lines = [l for l in lines if l.get("sample")]
    if args.only:
        keep = set(args.only.split(","))
        lines = [l for l in lines if l["id"] in keep]
    if args.cand:
        names = args.cand.split(",")
    elif all(cfg["pick"].values()):
        names = list(cfg["pick"].values())
    else:
        names = list(cfg["candidates"])
    for name in names:
        cand = cfg["candidates"][name]
        mine = [l for l in lines if l["who"] in (cand["who"], "both")]
        if not mine:
            continue
        d = OUT / name
        d.mkdir(parents=True, exist_ok=True)
        man_path = d / "manifest.json"
        man = json.loads(man_path.read_text("utf-8")) if man_path.exists() else {}
        takes: dict[str, list] = {l["id"]: [] for l in mine}
        t0 = time.time()
        # 按 ad.json 的 batch 分组合成：同一批的句子会互相影响，分组固定了，重跑每句都和上次一样
        groups: dict[str, list] = {}
        for l in mine:
            groups.setdefault(l.get("batch", "main"), []).append(l)
        for group in groups.values():
            for k in range(args.seeds):
                seed = cfg["seed"] + k
                segs, sr = synth(cfg, cand, [l["text"] for l in group], seed)
                for l, a in zip(group, segs):
                    takes[l["id"]].append((tail_db(a, sr), seed, a))
        for l in mine:
            # 结尾最干净的一条（被切的电平高）；都没被切时取第一个种子，保持可复现
            ok = [t for t in takes[l["id"]] if t[0] < -25]
            db, seed, a = ok[0] if ok else min(takes[l["id"]], key=lambda t: t[0])
            write(d / f"{l['id']}.wav", a, sr)
            man[l["id"]] = {"text": l["text"], "seed": seed, "sec": round(len(a) / sr + SR_LEAD, 3), "tail_db": db,
                            "all_tail_db": [t[0] for t in takes[l["id"]]]}
            print(f"{name} {l['id']} seed {seed} {man[l['id']]['sec']:.2f}s tail {db} dB  {l['text']}")
        man_path.write_text(json.dumps(man, ensure_ascii=False, indent=1), "utf-8")
        print(f"{name}: {time.time() - t0:.0f} s")


if __name__ == "__main__":
    sys.exit(main())
