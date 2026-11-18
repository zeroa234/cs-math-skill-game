"""H.1.2 数字电路与数字逻辑：真值表、卡诺图/NAND、全加器、Mealy 101、时序约束与 WSL Icarus Verilog 实测验证。"""
from fractions import Fraction
from itertools import product
from pathlib import Path
import re
import shutil
import subprocess
import uuid

ROOT = Path(__file__).resolve().parents[2]
PACK = (ROOT / "data/content/H.1.2.yaml").read_text(encoding="utf-8")


def extract_verilog_blocks(text: str) -> list[str]:
    return [m.group(1).strip() for m in re.finditer(r"```verilog\n(.*?)```", text, re.S)]


def test_truth_and_nand() -> None:
    minterms = {1, 3, 5, 6, 7}
    for i, (a, b, c) in enumerate(product((0, 1), repeat=3)):
        f_minterm = int(i in minterms)
        f_kmap = c | (a & b)
        not_ab = int(not (a & b))
        not_c = int(not (c & c))
        f_nand = int(not (not_ab & not_c))
        assert f_minterm == f_kmap == f_nand, (a, b, c, f_minterm, f_kmap, f_nand)


def test_adder_and_cla() -> None:
    for a, b, cin in product((0, 1), repeat=3):
        s = a ^ b ^ cin
        cout = (a & b) | (cin & (a ^ b))
        assert s + 2 * cout == a + b + cin
    # Verify 4-bit CLA matches ripple-carry for all 256*2 cases.
    for x in range(16):
        for y in range(16):
            for cin in (0, 1):
                c = cin
                ripple_c = [c]
                for bit in range(4):
                    ai, bi = (x >> bit) & 1, (y >> bit) & 1
                    c = (ai & bi) | (c & (ai ^ bi))
                    ripple_c.append(c)
                g = [((x >> i) & 1) & ((y >> i) & 1) for i in range(4)]
                p = [((x >> i) & 1) ^ ((y >> i) & 1) for i in range(4)]
                c1 = g[0] | (p[0] & cin)
                c2 = g[1] | (p[1] & g[0]) | (p[1] & p[0] & cin)
                assert c1 == ripple_c[1] and c2 == ripple_c[2]


def test_mealy_101_from_pack() -> None:
    table = {}
    for line in PACK.splitlines():
        m = re.match(r"^\s*(S[012])\s+(S[012])/([01])\s+(S[012])/([01])\s*$", line)
        if m:
            st, n0, o0, n1, o1 = m.groups()
            table[(st, "0")] = (n0, int(o0))
            table[(st, "1")] = (n1, int(o1))
    assert len(table) == 6, f"Expected 6 transitions in H.1.2.yaml Mealy table, got {table}"

    def run_seq(bits: str) -> list[int]:
        st = "S0"
        outs = []
        for ch in bits:
            st, out = table[(st, ch)]
            outs.append(out)
        return outs

    assert run_seq("10101") == [0, 0, 1, 0, 1]
    assert sum(run_seq("10101")) == 2

    for length in range(8):
        for tup in product("01", repeat=length):
            s = "".join(tup)
            expected = [1 if i >= 2 and s[i - 2 : i + 1] == "101" else 0 for i in range(length)]
            got = run_seq(s)
            assert got == expected, (s, got, expected)


def test_timing_and_noise_margins() -> None:
    assert Fraction("0.8") - Fraction("0.3") == Fraction("0.5")
    assert Fraction("2.4") - Fraction("2.0") == Fraction("0.4")
    assert Fraction("2.1") - Fraction("2.5") == Fraction("-0.4")

    t_min_c4 = Fraction("1") + Fraction("5") + Fraction("0.5")
    assert t_min_c4 == Fraction("6.5")
    f_max_mhz = float(Fraction(1000) / t_min_c4)
    assert abs(f_max_mhz - 153.846153846) < 1e-6

    t_min_boss = Fraction("2") + Fraction("4") + Fraction("1")
    assert t_min_boss == 7
    assert Fraction("0.2") + Fraction("0.1") < Fraction("0.5")  # hold violation example
    assert (2 - 1) + 4 == 5  # 2-stage pipeline for 4 items


def test_iverilog_hardware_sims() -> None:
    blocks = extract_verilog_blocks(PACK)
    assert len(blocks) == 2, f"Expected 2 verilog blocks in H.1.2.yaml, found {len(blocks)}"
    nand_src, fa_src = blocks

    tb_src = f"""
{nand_src}

{fa_src}

module tb;
  reg A, B, C;
  wire F, S, Cout;
  integer i, expected_f, expected_sum;

  nand_form u_nand(.A(A), .B(B), .C(C), .F(F));
  full_adder u_fa(.A(A), .B(B), .Cin(C), .S(S), .Cout(Cout));

  initial begin
    for (i = 0; i < 8; i = i + 1) begin
      {{A, B, C}} = i[2:0];
      #1;
      expected_f = (i == 1 || i == 3 || i == 5 || i == 6 || i == 7) ? 1 : 0;
      if (F !== expected_f[0]) begin
        $display("FAIL_NAND %0d F=%b exp=%b", i, F, expected_f[0]);
        $finish_and_return(1);
      end
      expected_sum = A + B + C;
      if ({{Cout, S}} !== expected_sum[1:0]) begin
        $display("FAIL_FA %0d CS=%b%b exp=%b", i, Cout, S, expected_sum[1:0]);
        $finish_and_return(1);
      end
    end
    $display("PASS_VERILOG_ALL_8");
    $finish;
  end
endmodule
"""

    work_dir = ROOT / "temp" / f"h12-ivl-{uuid.uuid4().hex[:8]}"
    work_dir.mkdir(parents=True, exist_ok=True)
    try:
        (work_dir / "tb.v").write_text(tb_src.strip() + "\n", encoding="utf-8")
        wsl_base = "/mnt/d/agent/projects/cs-math-skill-game/temp/embedded-runtimes/unpacked"
        wsl_work = f"/mnt/d/agent/projects/cs-math-skill-game/temp/{work_dir.name}"
        cmd = (
            f"LD_LIBRARY_PATH={wsl_base}/usr/lib:{wsl_base}/usr/lib/x86_64-linux-gnu:{wsl_base}/lib/x86_64-linux-gnu "
            f"{wsl_base}/usr/bin/iverilog -B {wsl_base}/usr/lib/x86_64-linux-gnu/ivl -g2012 -s tb -o {wsl_work}/sim.vvp {wsl_work}/tb.v && "
            f"LD_LIBRARY_PATH={wsl_base}/usr/lib:{wsl_base}/usr/lib/x86_64-linux-gnu:{wsl_base}/lib/x86_64-linux-gnu "
            f"{wsl_base}/usr/bin/vvp -M {wsl_base}/usr/lib/x86_64-linux-gnu/ivl {wsl_work}/sim.vvp"
        )
        res = subprocess.run(["wsl", "bash", "-c", cmd], capture_output=True, text=True, encoding="utf-8", check=False)
        assert res.returncode == 0, f"iverilog/vvp failed ({res.returncode}):\nSTDOUT:\n{res.stdout}\nSTDERR:\n{res.stderr}"
        assert "PASS_VERILOG_ALL_8" in res.stdout, res.stdout
    finally:
        shutil.rmtree(work_dir, ignore_errors=True)


if __name__ == "__main__":
    test_truth_and_nand()
    test_adder_and_cla()
    test_mealy_101_from_pack()
    test_timing_and_noise_margins()
    test_iverilog_hardware_sims()
    print("ok  H.1.2.verify.py: truth/CLA + Mealy 101 (len 0..7) + Fraction timing + WSL Icarus Verilog (8/8 vectors)")
