"""Check circuit lesson numerics and optionally cross-check RC with ngspice."""

from argparse import ArgumentParser
from math import exp, pi, sqrt
import re
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory


def rc(t, resistance, capacitance, voltage):
    return voltage * (1 - exp(-t / (resistance * capacitance)))


assert 5 - 2 == 3 and 6 / 2 == 3
parallel = 1 / (1 / 3000 + 1 / 6000)
total_ma = 12 / (2000 + parallel) * 1000
node_v = total_ma * parallel / 1000
assert (parallel, total_ma, node_v) == (2000, 3, 6)
assert node_v / 3 + node_v / 6 == total_ma
assert 1 / (1 / 4 + 1 / 12) == 3 and 12 / (2 + 4) == 2
assert 6 * 2 / (1 + 2) == 4 and 6 / 1 == 6
assert round(rc(.1, 10_000, 10e-6, 5), 2) == 3.16
assert round(rc(.3, 10_000, 10e-6, 5), 2) == 4.75
assert round(1000 * 2000 * 10e-6) == 20 and round(1000 * .02 / 10) == 2
assert 1 / .2 == 5 and -4 * -3 == 12 and -2 * -5 == 10
assert -100 / 10 == -10 and 1 + 100 / 10 == 11 and 1 + 20 / 5 == 5
assert round(1 / (2 * pi * .1), 2) == 1.59 and sqrt(3**2 + 4**2) == 5
assert round(3300 / 1024, 2) == 3.22 and int(1.2 * 1024 / 3.3) == 372
assert 64 * 2.56 / 256 == .64 and round(6.02 * 10 + 1.76, 1) == 62


def check_spice(executable):
    root = Path(__file__).resolve().parents[2]
    with TemporaryDirectory(dir=root / "temp", prefix="h-1-1-spice-") as directory:
        work = Path(directory)
        netlist = work / "charge.cir"
        netlist.write_text(
            "RC charge\nV1 in 0 5\nR1 in out 10k\nC1 out 0 10u ic=0\n"
            ".tran 0.1m 310m uic\n.measure tran at100 FIND v(out) AT=0.1\n"
            ".measure tran at300 FIND v(out) AT=0.3\n.end\n", encoding="ascii",
        )
        result = subprocess.run([executable, "-b", netlist.name], cwd=work,
                                capture_output=True, text=True, check=True, timeout=15)
        for name, t in [("at100", .1), ("at300", .3)]:
            match = re.search(rf"^{name}\s*=\s*([-+.eE\d]+)", result.stdout, re.MULTILINE)
            assert match and abs(float(match[1]) - rc(t, 10_000, 10e-6, 5)) < .005, result.stdout


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--ngspice")
    args = parser.parse_args()
    if args.ngspice:
        check_spice(args.ngspice)
    print("H.1.1 circuit calculations passed" + (" with ngspice" if args.ngspice else ""))
