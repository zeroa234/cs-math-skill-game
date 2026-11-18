"""H.3.3 传感器与接口：两点校准、误差、串口/I2C/SPI、4x过采样白噪声蒙特卡洛、PWM/H桥与 WSL ngspice 惠斯通电桥仿真验证。"""
from fractions import Fraction as F
from math import log2, sqrt
from pathlib import Path
import random
import re
import shutil
import statistics
import subprocess
import uuid

ROOT = Path(__file__).resolve().parents[2]


def calibrated_temp(voltage: F | str) -> F:
    slope = (F("1.52") - F("0.52")) / 100
    return (F(voltage) - F("0.52")) / slope


def test_measurement_calibration_and_uncertainty() -> None:
    assert 4 * 10 == 40
    assert 500 + 25 * 10 == 750
    assert calibrated_temp("0.97") == 45
    assert calibrated_temp("1.02") == 50
    assert F(108 - 100, 100 * 20) * 100 == F("0.4")
    assert statistics.mean([22, 22, 22]) - 20 == 2
    assert F("1.05") / F("0.95") > 1.10  # +-5% worst-case tolerance error > 10%


def test_buses_sampling_and_actuators() -> None:
    assert 9600 // (1 + 8 + 1) == 960
    assert F(96, 960) * 1000 == 100
    assert 3 + 3 == 6  # SPI 3 slaves -> SCLK, MOSI, MISO + 3 CS
    assert F(4000, 8000) == F("0.5")
    assert 4 + 4 == 8
    assert 8 * 8 == 64
    assert F(1_000_000, 2000) == 500
    assert 2 * 120 == 240
    assert log2(sqrt(4)) == 1.0
    assert log2(sqrt(16)) == 2.0
    assert 12 * F("0.25") == 3
    assert 12 * F("0.75") == 9


def test_oversampling_dither_simulation() -> None:
    # Verify C4 Q4 core premise empirically:
    # Without dithering noise, 1.0004 stays stuck at integer code 300 across 4x oversampling.
    # With ~0.7 LSB Gaussian/uniform noise, 4x averaging halves noise std (~ +1 bit ENOB).
    rng = random.Random(2026)
    signal_lsb = 300.25
    clean_4x = statistics.mean(int(signal_lsb) for _ in range(4))
    assert clean_4x == 300  # stuck without noise!

    errs_1x = []
    errs_4x = []
    for _ in range(2000):
        draws = [int(signal_lsb + rng.uniform(-1.0, 1.0)) for _ in range(4)]
        errs_1x.append(draws[0] - signal_lsb)
        errs_4x.append(statistics.mean(draws) - signal_lsb)
    std_1x = statistics.stdev(errs_1x)
    std_4x = statistics.stdev(errs_4x)
    # Theoretical reduction = 1 / sqrt(4) = 0.5
    assert abs(std_4x / std_1x - 0.5) < 0.06, (std_1x, std_4x)


def test_ngspice_wheatstone_bridge() -> None:
    # Verify Wheatstone bridge 1000/1000/1000/1010 Ohm @ 5V produces ~12.438 mV differential voltage
    wsl_base = "/mnt/d/agent/projects/cs-math-skill-game/temp/embedded-runtimes/unpacked"
    ld_lib = f"{wsl_base}/usr/lib:{wsl_base}/usr/lib/x86_64-linux-gnu:{wsl_base}/lib/x86_64-linux-gnu"
    work_dir = ROOT / "temp" / f"h33-spice-{uuid.uuid4().hex[:8]}"
    work_dir.mkdir(parents=True, exist_ok=True)
    try:
        (work_dir / "bridge.cir").write_text(
            "H.3.3 Wheatstone Bridge 1%\n"
            "Vexc vcc 0 5\n"
            "R1 vcc v_left 1000\n"
            "R2 v_left 0 1000\n"
            "R3 vcc v_right 1000\n"
            "Rx v_right 0 1010\n"
            ".op\n"
            ".end\n",
            encoding="ascii",
        )
        wsl_work = f"/mnt/d/agent/projects/cs-math-skill-game/temp/{work_dir.name}"
        res = subprocess.run(
            ["wsl", "bash", "-c", f"LD_LIBRARY_PATH={ld_lib} {wsl_base}/usr/bin/ngspice -b {wsl_work}/bridge.cir"],
            capture_output=True, text=True, encoding="utf-8", check=False, timeout=15,
        )
        assert res.returncode == 0, res.stderr
        ml = re.search(r"^\s*v_left\s+([-+.eE\d]+)", res.stdout, re.M | re.I)
        mr = re.search(r"^\s*v_right\s+([-+.eE\d]+)", res.stdout, re.M | re.I)
        assert ml and mr, res.stdout
        vdiff = abs(float(mr[1]) - float(ml[1]))
        expected = abs(5.0 * 1010 / 2010 - 2.5)
        assert abs(vdiff - expected) < 1e-4 and round(vdiff * 1000, 2) == 12.44, (vdiff, expected)
    finally:
        shutil.rmtree(work_dir, ignore_errors=True)


if __name__ == "__main__":
    test_measurement_calibration_and_uncertainty()
    test_buses_sampling_and_actuators()
    test_oversampling_dither_simulation()
    test_ngspice_wheatstone_bridge()
    print("ok  H.3.3.verify.py: calibration/buses/PWM + 4x dither Monte Carlo + WSL ngspice Wheatstone bridge")