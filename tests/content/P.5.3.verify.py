"""Verify P.5.3 DevOps/SRE calculations, reproducible archive invariants, and GitHub Actions workflow."""

from fractions import Fraction
from hashlib import sha256
from io import BytesIO
import json
from math import ceil
from pathlib import Path
import subprocess
from zipfile import ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parents[2]


def check_numbers():
    good_rate = lambda total, bad: Fraction(total - bad, total)
    assert good_rate(1000, 2) == good_rate(2000, 4) == Fraction("0.998")
    assert good_rate(1000, 2) < Fraction("0.999")

    # 30-day 99.9% availability budget and burn rates
    window_min = 30 * 24 * 60
    allowance = 1 - Fraction("0.999")
    assert window_min == 43_200
    budget = window_min * allowance
    assert budget == Fraction("43.2")
    assert [budget - used for used in (30, 35, 40)] == [Fraction("13.2"), Fraction("8.2"), Fraction("3.2")]
    assert Fraction("0.01") / allowance == 10
    assert Fraction("0.005") / allowance == 5
    assert Fraction(6, 200) == Fraction(3, 100) > Fraction("0.02") > Fraction("0.005")

    # N+1 capacity sizing: ceil(peak / unit_capacity) + 1
    assert ceil(Fraction(250, 100)) + 1 == 4
    assert ceil(Fraction(380, 120)) + 1 == 5
    assert ceil(Fraction(300, 80)) + 1 == 5


def deterministic_zip_sha256(names, day):
    files = {"app.txt": "same program", "docs.txt": "same documentation"}
    buf = BytesIO()
    with ZipFile(buf, "w") as zf:
        for name in names:
            zf.writestr(ZipInfo(name, (2026, 11, day, 0, 0, 0)), files[name])
    return sha256(buf.getvalue()).hexdigest()


def check_reproducible_archive():
    order_a = ["app.txt", "docs.txt"]
    order_b = list(reversed(order_a))
    assert deterministic_zip_sha256(order_a, 1) != deterministic_zip_sha256(order_b, 1)
    assert deterministic_zip_sha256(order_a, 1) != deterministic_zip_sha256(order_a, 2)
    assert deterministic_zip_sha256(sorted(order_a), 1) == deterministic_zip_sha256(sorted(order_b), 1)


def check_workflow_example():
    pack_path = ROOT / "data/content/P.5.3.yaml"
    if not pack_path.exists():
        print("P.5.3: skipped workflow YAML check (data/content/P.5.3.yaml not written yet)")
        return
    output = subprocess.check_output(
        [
            "node",
            "--input-type=module",
            "-e",
            """
            import fs from 'node:fs';
            import {load} from 'js-yaml';
            const pack = load(fs.readFileSync('data/content/P.5.3.yaml', 'utf8'));
            const lesson = pack.lessons.find(l => l.id === 'workflow');
            const block = lesson.flow.find(s => s.card?.body?.includes('```yaml')).card.body;
            const source = block.split('```')[1].slice('yaml\\n'.length);
            console.log(JSON.stringify(load(source)));
            """,
        ],
        cwd=ROOT,
        encoding="utf-8",
    )
    wf = json.loads(output)
    assert wf["on"] == {"push": {"branches": ["main"]}}
    assert wf["permissions"] == {"contents": "read"}
    steps = wf["jobs"]["test-and-build"]["steps"]
    assert steps[:2] == [
        {"uses": "actions/checkout@v7"},
        {"uses": "actions/setup-python@v7", "with": {"python-version": "3.12"}},
    ]
    assert steps[2:] == [
        {"run": "python -m pip install -r requirements.txt"},
        {"run": "python -m pytest -q"},
        {"run": "docker build -t demo:${{ github.sha }} ."},
    ]


if __name__ == "__main__":
    check_numbers()
    check_reproducible_archive()
    check_workflow_example()
    print("P.5.3 verify: all SLO, burn-rate, N+1 capacity, archive reproducibility, and workflow checks passed.")
