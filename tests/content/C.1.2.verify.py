"""C.1.2 计算机体系结构：MIPS/SPIM 汇编实测、5 级流水线冒险相位、Cache/VM、AMAT、2 位分支预测与 Amdahl 精确验算。"""
from fractions import Fraction as F
from pathlib import Path
import re
import shutil
import subprocess
import uuid

ROOT = Path(__file__).resolve().parents[2]
PACK = (ROOT / "data/content/C.1.2.yaml").read_text(encoding="utf-8")


def branch_correct(results: list[bool]) -> int:
    # 2-bit saturating counter: 00/01 -> predict N, 10/11 -> predict T; starts at 11 (state 3)
    state = 3
    correct = 0
    for taken in results:
        correct += int((state >= 2) == taken)
        state = max(0, min(3, state + (1 if taken else -1)))
    return correct


def amat(hit: F | int, miss_rate: F, extra: F | int) -> F:
    return hit + miss_rate * extra


def elapsed(instructions: int, cpi: F, hz: int) -> F:
    return instructions * cpi / hz


def test_isa_datapath_pipeline_arithmetic() -> None:
    assert 8 + 5 == 13
    assert 100 + 8 == 108
    assert 100 + 12 == 112
    assert 4 + 2 + 3 + 6 + 3 == 18
    assert 5 + 4 - 1 == 8
    assert (5 + 6 - 1) * 3 == 30
    assert 100 + 10 * 2 == 120

    # 5-stage pipeline hazard timing with full forwarding:
    # lw x1, 0(x2); add x3, x1, x4; sub x5, x3, x6
    fetch = 0
    load_available = fetch + 3 + 1  # end of MEM (4)
    add_fetch = max(fetch + 1, load_available - 2)  # EX is at +2 -> fetch=2 (1 stall!)
    add_available = add_fetch + 2 + 1  # end of EX (5)
    sub_fetch = max(add_fetch + 1, add_available - 2)  # +3 -> 0 stalls!
    assert (add_fetch - fetch - 1, sub_fetch - add_fetch - 1) == (1, 0)


def test_cache_vm_and_amat() -> None:
    assert divmod(52, 16) == (3, 4)
    assert divmod(84 // 16, 4) == (1, 1)  # index 1, tag 1
    assert 4 * 2 * 16 == 128
    assert 1 * 1024 + 12 == 1036

    assert amat(1, F(5, 100), 100) == 6
    assert amat(1, F(5, 100), amat(10, F(1, 5), 100)) == F(5, 2)  # 2.5
    assert amat(1, F(1, 10), amat(8, F(1, 4), 80)) == F(19, 5)    # 3.8


def test_branch_cpu_time_and_amdahl() -> None:
    pattern = [True, True, True, False]  # T T T N
    assert branch_correct(pattern * 2) == 6
    assert F(branch_correct(pattern * 3), 12) == F(3, 4)  # 75%

    t_old = elapsed(10**9, F(3, 2), 2 * 10**9)
    t_new = elapsed(10**9, F(6, 5), 18 * 10**8)
    assert t_old == F(3, 4)  # 0.75 s
    assert t_old / t_new == F(9, 8)  # 1.125 speedup
    assert elapsed(2 * 10**8, F(3, 2), 2 * 10**9) == F(3, 20)  # 0.15 s

    assert 1 / (F(1, 5) + F(4, 5) / 16) == 4
    assert 1 / F(1, 5) == 5
    assert 1 / F(1, 4) == 4


def test_spim_mips_execution() -> None:
    m = re.search(r"```asm\n(.*?)```", PACK, re.S)
    assert m, "Missing ```asm snippet in C.1.2.yaml"
    asm_snippet = "\n".join(line.strip() for line in m.group(1).splitlines() if line.strip())

    # Wrap snippet with spim print/exit syscalls so we observe $t0 (add) and $t3 (lw 4($s0)) directly.
    prog = f"""{asm_snippet}
  move $a0, $t0
  li $v0, 1
  syscall
  li $a0, 10
  li $v0, 11
  syscall
  move $a0, $t3
  li $v0, 1
  syscall
  li $a0, 10
  li $v0, 11
  syscall
  li $v0, 10
  syscall
"""
    work_dir = ROOT / "temp" / f"c12-spim-{uuid.uuid4().hex[:8]}"
    work_dir.mkdir(parents=True, exist_ok=True)
    try:
        (work_dir / "lesson.s").write_text(prog, encoding="ascii")
        wsl_base = "/mnt/d/agent/projects/cs-math-skill-game/temp/embedded-runtimes/unpacked"
        wsl_work = f"/mnt/d/agent/projects/cs-math-skill-game/temp/{work_dir.name}"
        ld = f"{wsl_base}/usr/lib:{wsl_base}/usr/lib/x86_64-linux-gnu:{wsl_base}/lib/x86_64-linux-gnu"
        res = subprocess.run(
            ["wsl", "bash", "-c", f"LD_LIBRARY_PATH={ld} {wsl_base}/usr/bin/spim -exception_file {wsl_base}/usr/lib/spim/exceptions.s -file {wsl_work}/lesson.s"],
            capture_output=True, text=True, encoding="utf-8", check=False, timeout=15,
        )
        assert res.returncode == 0, (res.returncode, res.stdout, res.stderr)
        nums = [line.strip() for line in res.stdout.splitlines() if line.strip().isdigit()]
        assert nums[-2:] == ["13", "17"], (res.stdout, nums)
    finally:
        shutil.rmtree(work_dir, ignore_errors=True)


if __name__ == "__main__":
    test_isa_datapath_pipeline_arithmetic()
    test_cache_vm_and_amat()
    test_branch_cpu_time_and_amdahl()
    test_spim_mips_execution()
    print("ok  C.1.2.verify.py: pipeline hazards + cache/VM + AMAT + 2-bit branch + CPU/Amdahl + WSL SPIM 8.0")
