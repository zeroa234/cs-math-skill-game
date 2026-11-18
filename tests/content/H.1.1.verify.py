"""H.1.1 电路与模拟电子基础：欧姆/KCL/KVL/戴维南、RC/RL 暂态、运放、滤波器、量化/SNR 与 WSL ngspice 仿真验证。"""
from fractions import Fraction
from math import exp, floor, log10, pi, sqrt
from pathlib import Path
import re
import shutil
import subprocess
import uuid

ROOT = Path(__file__).resolve().parents[2]


def rc_charge(t: float, r: float, c: float, vs: float) -> float:
    return vs * (1.0 - exp(-t / (r * c)))


def test_dc_laws_and_equivalents() -> None:
    # ohm
    assert Fraction(12, 4) == 3  # 12 V / 4 kOhm = 3 mA
    r23 = Fraction(3 * 6, 3 + 6)
    assert r23 == 2  # 3k || 6k = 2 kOhm
    assert Fraction(5 * 3, 2 + 3) == 3  # 5 V divider 2k / 3k -> 3 V

    # nodes (C4 Q1)
    r_total = 2 + r23
    i_total_ma = Fraction(12, r_total)
    v_parallel = 12 - i_total_ma * 2
    i_r2 = Fraction(v_parallel, 3)
    i_r3 = Fraction(v_parallel, 6)
    assert (r_total, i_total_ma, v_parallel, i_r2, i_r3) == (4, 3, 6, 2, 1)
    assert i_r2 + i_r3 == i_total_ma  # KCL check
    assert 5 + 3 - 6 == 2  # 4-branch KCL

    # loops & power
    assert 12 - 4 - 8 == 0
    assert 6 * 3 == 18  # 6 V * 3 mA = 18 mW

    # equivalent (Thevenin / Norton)
    assert Fraction(12 * 6, 3 + 6) == 8  # 12 V divider 3k / 6k -> Vth=8 V
    assert Fraction(3 * 6, 3 + 6) == 2   # Rth=2 kOhm
    assert Fraction(8 * 2, 2 + 2) == 4   # 8 V with 2k load on 2k -> 4 V
    assert Fraction(6 * 2, 1 + 2) == 4   # Vth=6 V, Rth=1k, RL=2k -> 4 V
    assert Fraction(6, 1) == 6           # In = 6 mA


def test_transient_and_filters() -> None:
    # RC C4 Q2: R=10k, C=10uF -> tau=0.1s
    tau = 10_000 * 10e-6
    assert abs(tau - 0.1) < 1e-12
    assert round(rc_charge(0.1, 10_000, 10e-6, 5.0), 2) == 3.16
    assert round(rc_charge(0.3, 10_000, 10e-6, 5.0), 2) == 4.75
    assert round(2000 * 10e-6 * 1000) == 20  # 2k * 10uF = 20 ms
    assert round((0.02 / 10) * 1000) == 2    # 20 mH / 10 Ohm = 2 ms

    fc = 1.0 / (2 * pi * tau)
    assert round(fc, 2) == 1.59
    assert abs(10 * log10(0.5) - (-3.0103)) < 1e-3


def test_amplifiers_opamp_and_adc() -> None:
    # gain & differential
    assert Fraction("1.0") / Fraction("0.2") == 5
    assert (-4) * (-3) == 12
    assert (-2) * (-5) == 10
    assert 20 * log10(100) == 40
    assert -2e-3 * 5e3 == -10

    # ideal & real op amp (C4 Q3)
    assert Fraction(-100, 10) == -10
    assert 1 + Fraction(100, 10) == 11
    assert Fraction(10, 20) == Fraction("0.5")  # GBW 10 MHz / 20 -> 0.5 MHz
    assert 2 * pi * 500e3 * 10 > 30e6  # 31.4 V/us slew check

    # noise, quantization & aliasing (C4 Q4, Q5)
    assert sqrt(3**2 + 4**2) == 5.0
    assert round(20 * log10(1.0 / 0.01)) == 40
    lsb_mv = 3300.0 / 1024.0
    assert round(lsb_mv, 2) == 3.22
    code = floor(1.2 / 3.3 * 1024)
    assert code == 372
    assert round(64 * 2.56 / 256, 2) == 0.64
    snr_db = 6.02 * 10 + 1.76
    assert round(snr_db) == 62
    assert 2 * 5 == 10
    assert abs(900 - 1000) == 100


def test_ngspice_circuits() -> None:
    wsl_base = "/mnt/d/agent/projects/cs-math-skill-game/temp/embedded-runtimes/unpacked"
    ld_lib = f"{wsl_base}/usr/lib:{wsl_base}/usr/lib/x86_64-linux-gnu:{wsl_base}/lib/x86_64-linux-gnu"
    work_dir = ROOT / "temp" / f"h11-spice-{uuid.uuid4().hex[:8]}"
    work_dir.mkdir(parents=True, exist_ok=True)
    try:
        # 1. C4 Q1 DC resistor network + Q2 RC transient + low-pass AC -3dB test
        (work_dir / "dc_kcl.cir").write_text(
            "H.1.1 C4 Q1 DC KCL\n"
            "V1 in 0 12\n"
            "R1 in nodeA 2k\n"
            "R2 nodeA 0 3k\n"
            "R3 nodeA 0 6k\n"
            ".op\n"
            ".print dc v(nodeA) i(V1)\n"
            ".end\n",
            encoding="ascii",
        )
        (work_dir / "rc_tran.cir").write_text(
            "H.1.1 C4 Q2 RC transient\n"
            "V1 in 0 5\n"
            "R1 in out 10k\n"
            "C1 out 0 10u ic=0\n"
            ".tran 0.1m 310m uic\n"
            ".measure tran at100 FIND v(out) AT=0.1\n"
            ".measure tran at300 FIND v(out) AT=0.3\n"
            ".end\n",
            encoding="ascii",
        )
        (work_dir / "rc_ac.cir").write_text(
            "H.1.1 C4 Q2 RC lowpass AC -3dB\n"
            "V1 in 0 DC 0 AC 1\n"
            "R1 in out 10k\n"
            "C1 out 0 10u\n"
            ".ac dec 200 0.1 100\n"
            ".control\n"
            "run\n"
            "meas ac fc WHEN vmag(out)=0.70710678\n"
            "quit\n"
            ".endc\n"
            ".end\n",
            encoding="ascii",
        )
        wsl_work = f"/mnt/d/agent/projects/cs-math-skill-game/temp/{work_dir.name}"
        r_dc = subprocess.run(
            ["wsl", "bash", "-c", f"LD_LIBRARY_PATH={ld_lib} {wsl_base}/usr/bin/ngspice -b {wsl_work}/dc_kcl.cir"],
            capture_output=True, text=True, encoding="utf-8", check=False, timeout=15,
        )
        assert r_dc.returncode == 0, r_dc.stderr
        m_va = re.search(r"^\s*nodea\s+([-+.eE\d]+)", r_dc.stdout, re.M | re.I)
        m_iv = re.search(r"^\s*v1#branch\s+([-+.eE\d]+)", r_dc.stdout, re.M | re.I)
        assert m_va and abs(float(m_va[1]) - 6.0) < 1e-4, r_dc.stdout
        assert m_iv and abs(abs(float(m_iv[1])) - 0.003) < 1e-6, r_dc.stdout

        r_tran = subprocess.run(
            ["wsl", "bash", "-c", f"LD_LIBRARY_PATH={ld_lib} {wsl_base}/usr/bin/ngspice -b {wsl_work}/rc_tran.cir"],
            capture_output=True, text=True, encoding="utf-8", check=False, timeout=15,
        )
        assert r_tran.returncode == 0, r_tran.stderr
        for name, expected in [
            ("at100", rc_charge(0.1, 10_000, 10e-6, 5.0)),
            ("at300", rc_charge(0.3, 10_000, 10e-6, 5.0)),
        ]:
            m = re.search(rf"^{name}\s*=\s*([-+.eE\d]+)", r_tran.stdout, re.MULTILINE | re.I)
            assert m and abs(float(m[1]) - expected) < 0.005, (name, m, r_tran.stdout)

        r_ac = subprocess.run(
            ["wsl", "bash", "-c", f"LD_LIBRARY_PATH={ld_lib} {wsl_base}/usr/bin/ngspice -b {wsl_work}/rc_ac.cir"],
            capture_output=True, text=True, encoding="utf-8", check=False, timeout=15,
        )
        assert r_ac.returncode == 0, r_ac.stderr
        m_fc = re.search(r"^fc\s*=\s*([-+.eE\d]+)", r_ac.stdout, re.MULTILINE | re.I)
        assert m_fc and abs(float(m_fc[1]) - 1.0 / (2 * pi * 0.1)) < 0.005, (m_fc, r_ac.stdout)
    finally:
        shutil.rmtree(work_dir, ignore_errors=True)


if __name__ == "__main__":
    test_dc_laws_and_equivalents()
    test_transient_and_filters()
    test_amplifiers_opamp_and_adc()
    test_ngspice_circuits()
    print("ok  H.1.1.verify.py: DC/KCL/KVL + RC/RL + OpAmp/Filter + ADC/SNR + WSL ngspice (OP/TRAN/AC)")
