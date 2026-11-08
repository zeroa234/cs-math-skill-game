"""Run the Python, TypeScript, Rust and gprof teaching examples."""

from argparse import ArgumentParser
from pathlib import Path
import re
import subprocess
import sys
from tempfile import TemporaryDirectory
from textwrap import dedent
from timeit import repeat


ROOT = Path(__file__).resolve().parents[2]
TEXT = (ROOT / "data/content/P.1.4.yaml").read_text(encoding="utf-8")


def examples(language, marker, suffix=""):
    blocks = re.findall(rf"^ +```{language}\n(.*?)^ +```$", TEXT, re.MULTILINE | re.DOTALL)
    assert blocks, language
    for block in blocks:
        source, expected = dedent(block).strip().rsplit("\n" + marker + " expect: ", 1)
        yield source, expected.removesuffix(suffix).split("|")


def run(args, cwd, check=True):
    result = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=25)
    if check:
        assert result.returncode == 0, result.stderr or result.stdout
    return result


def check_python(work):
    count = 0
    for source, expected in examples("python", "#"):
        actual = run([sys.executable, "-I", "-c", source], work).stdout.strip().splitlines()
        assert actual == expected, (source, actual, expected)
        count += 1
    size = 10 ** 6
    items = list(range(size))
    members = set(items)
    for key in (size - 1, size):
        assert (key in items) == (key in members)
        for container in (items, members):
            timings = repeat(lambda: key in container, number=3, repeat=3)
            assert len(timings) == 3 and all(time >= 0 for time in timings)
    print(f"P.1.4 {count} Python snippets and equal-input lookup measurements passed")


def check_typescript(work, tsc):
    source = work / "example.ts"
    types = work / "empty-types"
    types.mkdir()
    compiler = ["node", str(tsc), "--strict", "--target", "ES2022", "--module",
                "ES2022", "--typeRoots", str(types), "--outDir", str(work), str(source)]
    for program, expected in examples("typescript", "//"):
        source.write_text(program, encoding="utf-8")
        run(compiler, work)
        assert run(["node", str(work / "example.js")], work).stdout.strip().splitlines() == expected
    source.write_text("function use(n: number) { return n; }\nuse('text');\n", encoding="utf-8")
    rejected = run(compiler, work, check=False)
    assert rejected.returncode and "not assignable" in rejected.stdout
    print("P.1.4 TypeScript samples and type rejection passed")


def check_rust(work, rustc):
    source = work / "example.rs"
    target = work / "example-rust"
    compiler = [str(rustc), str(source), "-o", str(target)]
    for program, expected in examples("rust", "//"):
        source.write_text(program, encoding="utf-8")
        run(compiler, work)
        assert run([str(target)], work).stdout.strip().splitlines() == expected
    source.write_text(
        'fn main() { let a = String::from("ready"); let b = a; println!("{}", a); }\n',
        encoding="utf-8",
    )
    rejected = run(compiler, work, check=False)
    assert rejected.returncode and "E0382" in rejected.stderr
    print("P.1.4 Rust move, borrow and moved-value rejection passed")


def check_gprof(work):
    (program, expected), = examples("c", "/*", " */")
    (work / "example.c").write_text(program, encoding="utf-8")
    run(["gcc", "-O0", "-g", "-pg", "-no-pie", "example.c", "-o", "example"], work)
    assert run(["./example"], work).stdout.strip().splitlines() == expected
    output = run(["gprof", "-b", "./example", "gmon.out"], work).stdout
    assert "Flat profile:" in output and "Call graph" in output
    assert re.search(r"(?m)^\s*(?:[\d.]+\s+){3}2\s+(?:[\d.]+\s+){2}work\s*$", output), output
    print("P.1.4 GCC/gprof example and two work calls passed")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--tsc", type=Path)
    parser.add_argument("--rustc", type=Path)
    parser.add_argument("--gprof", action="store_true")
    args = parser.parse_args()
    temp = ROOT / "temp"
    temp.mkdir(exist_ok=True)
    with TemporaryDirectory(dir=temp, prefix="p-1-4-verify-") as directory:
        work = Path(directory)
        check_python(work)
        if args.tsc:
            check_typescript(work, args.tsc.resolve())
        if args.rustc:
            check_rust(work, args.rustc.resolve())
        if args.gprof:
            check_gprof(work)
