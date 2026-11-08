"""Check Boolean logic, Mealy overlaps and timing, plus the printed Verilog."""

from argparse import ArgumentParser
from fractions import Fraction
from itertools import product
from pathlib import Path
import re
import subprocess
from tempfile import TemporaryDirectory
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[2]
TEXT = (ROOT / "data/content/H.1.2.yaml").read_text(encoding="utf-8")


def check_models():
    minterms = {1, 3, 5, 6, 7}
    for a, b, c in product(range(2), repeat=3):
        assert bool(c or (a and b)) == (4 * a + 2 * b + c in minterms)
        total = a + b + c
        assert (a ^ b ^ c, (a & b) | (c & (a ^ b))) == (total % 2, total // 2)

    rows = re.findall(r"^\s*(S[012])\s+(S[012])/([01])\s+(S[012])/([01])$", TEXT, re.MULTILINE)
    assert len(rows) == 3
    table = {state: [(zero, out0), (one, out1)] for state, zero, out0, one, out1 in rows}
    for length in range(8):
        for bits in product(range(2), repeat=length):
            state = "S0"
            for index, bit in enumerate(bits):
                state, output = table[state][bit]
                assert (output == "1") == (bits[max(0, index - 2):index + 1] == (1, 0, 1))

    assert Fraction(8, 10) - Fraction(4, 10) == Fraction(4, 10)
    assert Fraction(24, 10) - 2 == Fraction(4, 10)
    period = 1 + 5 + Fraction(1, 2)
    assert period == Fraction(13, 2) and round(1000 / period, 2) == Fraction(15385, 100)
    assert 2 + 4 + 1 == 7 and 2 + (4 - 1) == 5
    print("H.1.2 truth tables, every short Mealy input and timing calculations passed")


def check_verilog(work, iverilog, base):
    blocks = re.findall(r"^ +```verilog\n(.*?)^ +```$", TEXT, re.MULTILINE | re.DOTALL)
    assert len(blocks) == 2
    source = work / "lesson.v"
    source.write_text("\n".join(dedent(block) for block in blocks) + """
        module tb;
            reg a, b, c;
            wire f, sum, carry;
            integer i, total;
            nand_form gate(a, b, c, f);
            full_adder add(a, b, c, sum, carry);
            initial begin
                for (i = 0; i < 8; i = i + 1) begin
                    {a, b, c} = i[2:0];
                    #1;
                    if (f !== (c | (a & b))) $fatal(1, "nand case %d", i);
                    total = a + b + c;
                    if ({carry, sum} !== total[1:0]) $fatal(1, "adder case %d", i);
                end
                $display("eight gate and adder cases passed");
            end
        endmodule
    """, encoding="utf-8")
    path_flags = ["-B", str(base)] if base else []
    result = subprocess.run([str(iverilog), *path_flags, "-g2012", "-s", "tb", "-o", "test.vvp", "lesson.v"],
                            cwd=work, capture_output=True, text=True, timeout=15)
    assert result.returncode == 0, result.stderr
    modules = ["-M", str(base)] if base else []
    result = subprocess.run([str(iverilog.with_name("vvp")), *modules, "test.vvp"],
                            cwd=work, capture_output=True, text=True, timeout=15)
    assert result.returncode == 0 and "eight gate and adder cases passed" in result.stdout, result.stderr
    print("H.1.2 Icarus Verilog: all eight gate and full-adder cases passed")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--iverilog", type=Path)
    parser.add_argument("--ivl-base", type=Path)
    args = parser.parse_args()
    check_models()
    if args.iverilog:
        with TemporaryDirectory(dir=ROOT / "temp", prefix="h-1-2-verify-") as directory:
            base = args.ivl_base.resolve() if args.ivl_base else None
            check_verilog(Path(directory), args.iverilog.resolve(), base)
