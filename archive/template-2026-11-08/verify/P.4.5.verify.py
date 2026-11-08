"""Run the exact lesson snippets and check their numerical examples.

Install pytest, hypothesis and coverage in the Python environment or under
temp/p-4-5-verify/libs using pip --target before running this script.
"""

from contextlib import redirect_stdout
from collections import Counter
from fractions import Fraction
from io import StringIO
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / "temp/p-4-5-verify"
LIBS = WORK / "libs"
if LIBS.is_dir():
    sys.path.insert(0, str(LIBS))

from hypothesis import find, settings, strategies as st


def examples():
    output = subprocess.check_output(
        ["node", "--input-type=module", "-e", """
          import fs from 'node:fs';
          import {load} from 'js-yaml';
          const pack = load(fs.readFileSync('data/content/P.4.5.yaml', 'utf8'));
          const examples = ['unit-python', 'hypothesis', 'fault-injection'].map(id => {
            const lesson = pack.lessons.find(l => l.id === id);
            const body = lesson.flow.find(s => s.card?.body.includes('```python')).card.body;
            return body.split('```')[1].slice('python\\n'.length);
          });
          console.log(JSON.stringify(examples));
        """], cwd=ROOT, encoding="utf-8",
    )
    return json.loads(output)


def run_tool(module, args, work, expected_status=0):
    result = subprocess.run(
        [sys.executable, "-I", "-X", "utf8", "-c", """
import runpy, sys
from pathlib import Path
lib, module, *args = sys.argv[1:]
if Path(lib).is_dir():
    sys.path.insert(0, lib)
sys.argv[:] = [module, *args]
runpy.run_module(module, run_name="__main__")
""", str(LIBS), module, *args],
        cwd=work, capture_output=True, encoding="utf-8", errors="replace",
    )
    assert result.returncode == expected_status, (result.stdout, result.stderr)
    return result.stdout


def check_triangles(work, source):
    path = work / "test_triangle.py"
    path.write_text(source, encoding="utf-8")
    assert "4 passed" in run_tool("pytest", ["-q", path.name], work)

    namespace = {}
    exec(compile(source, path.name, "exec"), namespace)
    classify = namespace["classify_triangle"]
    cases = [
        ((3, 3, 3), "等边"), ((3, 3, 4), "等腰"), ((3, 4, 3), "等腰"),
        ((4, 3, 3), "等腰"), ((3, 4, 5), "不等边"), ((0, 4, 5), "非法"),
        ((-1, 4, 5), "非法"), ((1, 2, 5), "非法"), ((1, 2, 3), "非法"),
        ((2, 2, 3), "等腰"), ((2, 3, 4), "不等边"), ((2, 3, 5), "非法"),
        ((2, 3, 6), "非法"), ((5, 5, 6), "等腰"),
    ]
    for sides, expected in cases:
        assert classify(*sides) == expected

    mutated = source.replace("x + y <= z", "x + y < z")
    assert mutated != source
    path.write_text(mutated, encoding="utf-8")
    report = run_tool("pytest", ["-q", path.name], work, expected_status=1)
    assert "1 failed, 3 passed" in report
    path.write_text(source, encoding="utf-8")
    assert "4 passed" in run_tool("coverage", ["run", "--branch", "-m", "pytest", "-q", path.name], work)
    assert "test_triangle.py" in run_tool("coverage", ["report", "-m"], work)


def check_properties(work, source):
    path = work / "test_counts.py"
    path.write_text(source, encoding="utf-8")
    failed = run_tool("pytest", ["-q", path.name], work, expected_status=1)
    assert "1 failed" in failed and "[1, 1]" in failed

    generated_only = source.replace("@example([1, 1])\n", "")
    path.write_text(generated_only, encoding="utf-8")
    discovered = run_tool("pytest", ["-q", "--hypothesis-seed=1", path.name], work, expected_status=1)
    assert "1 failed" in discovered
    counterexample = find(
        st.lists(st.integers(), max_size=8),
        lambda values: Counter(sorted(set(values))) != Counter(values),
        settings=settings(derandomize=True, database=None),
    )
    assert len(set(counterexample)) < len(counterexample)

    fixed = source.replace("sorted(set(xs))", "sorted(xs)")
    assert fixed != source
    path.write_text(fixed, encoding="utf-8")
    assert "1 passed" in run_tool("pytest", ["-q", path.name], work)


def check_short_circuit():
    def decision(a, b):
        observations = []

        def right():
            observations.append(b > 0)
            return observations[-1]

        result = a > 0 and right()
        return result, observations

    assert decision(1, 1) == (True, [True])
    assert decision(1, -1) == (False, [False])
    assert decision(-1, 1) == (False, [])
    assert decision(-1, 2) == (False, [])
    assert decision(2, 2) == (True, [True])


def check_values():
    assert Fraction(4, 5) == Fraction("0.8")
    assert Fraction(6, 8) == Fraction(9, 12) == Fraction("0.75")
    assert Fraction(6, 10 - 2) == Fraction("0.75")
    assert Fraction(8, 10) == Fraction("0.8")
    assert Fraction(6, 3000 // 1000) == 2
    assert round(float(Fraction(500, 502) * 100), 2) == 99.60
    assert Fraction(198, 198 + 2) == Fraction(99, 99 + 1) == Fraction("0.99")
    assert 365 * 24 == 8760
    assert 8760 * Fraction("0.0001") == Fraction("0.876")
    assert 8760 * 60 * Fraction("0.0001") == Fraction("52.56")
    assert 24 * 60 * Fraction("0.001") == Fraction("1.44")


triangle, properties, injection = examples()
WORK.mkdir(parents=True, exist_ok=True)
with TemporaryDirectory(dir=WORK, prefix="example-") as directory:
    work = Path(directory)
    check_triangles(work, triangle)
    check_properties(work, properties)
with redirect_stdout(StringIO()) as output:
    exec(injection, {})
assert output.getvalue().strip() == "暂不可用"
check_short_circuit()
check_values()
print("P.4.5: pytest and Hypothesis failures and fixes, coverage, timeout and numerical examples verified")
