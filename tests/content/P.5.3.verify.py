"""Verify the DevOps lesson calculations, archive behavior, and exact workflow.

Pass the path to actionlint as an optional argument to lint the workflow.
"""

from fractions import Fraction
from hashlib import sha256
from io import BytesIO
import json
from math import ceil
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parents[2]


def check_numbers():
    good = lambda total, bad: Fraction(total - bad, total)
    assert good(1000, 2) == good(2000, 4) == Fraction("0.998")
    assert good(1000, 2) < Fraction("0.999")
    window = 30 * 24 * 60
    allowance = 1 - Fraction("0.999")
    assert window == 43_200
    budget = window * allowance
    assert budget == Fraction("43.2")
    assert [budget - n for n in (30, 35, 40)] == [Fraction(x) for x in ("13.2", "8.2", "3.2")]
    assert Fraction("0.01") / allowance == 10
    assert Fraction("0.005") / allowance == 5
    assert Fraction(6, 200) == Fraction(3, 100) > Fraction("0.02") > Fraction("0.005")
    assert ceil(Fraction(250, 100)) + 1 == 4
    assert ceil(Fraction(380, 120)) + 1 == 5
    assert ceil(Fraction(300, 80)) + 1 == 5


def archive(names, day):
    contents = {"app.txt": "same program", "docs.txt": "same documentation"}
    buffer = BytesIO()
    with ZipFile(buffer, "w") as archive_file:
        for name in names:
            archive_file.writestr(ZipInfo(name, (2026, 11, day, 0, 0, 0)), contents[name])
    return sha256(buffer.getvalue()).hexdigest()


def check_archive():
    left = ["app.txt", "docs.txt"]
    right = list(reversed(left))
    assert archive(left, 1) != archive(right, 1)
    assert archive(left, 1) != archive(left, 2)
    assert archive(sorted(left), 1) == archive(sorted(right), 1)


def check_workflow(actionlint):
    output = subprocess.check_output(
        ["node", "--input-type=module", "-e", """
          import fs from 'node:fs';
          import {load} from 'js-yaml';
          const pack = load(fs.readFileSync('data/content/P.5.3.yaml', 'utf8'));
          const lesson = pack.lessons.find(l => l.id === 'workflow');
          const block = lesson.flow.find(s => s.card?.body.includes('```yaml')).card.body;
          const source = block.split('```')[1].slice('yaml\\n'.length);
          console.log(JSON.stringify({source, workflow: load(source)}));
        """], cwd=ROOT, encoding="utf-8",
    )
    example = json.loads(output)
    workflow = example["workflow"]
    assert workflow["on"] == {"push": {"branches": ["main"]}}
    assert workflow["permissions"] == {"contents": "read"}
    steps = workflow["jobs"]["test-and-build"]["steps"]
    assert steps[:2] == [
        {"uses": "actions/checkout@v7"},
        {"uses": "actions/setup-python@v7", "with": {"python-version": "3.12"}},
    ]
    assert steps[2:] == [
        {"run": "python -m pip install -r requirements.txt"},
        {"run": "python -m pytest -q"},
        {"run": "docker build -t demo:${{ github.sha }} ."},
    ]
    if actionlint:
        temp = ROOT / "temp"
        temp.mkdir(exist_ok=True)
        with TemporaryDirectory(dir=temp, prefix="p-5-3-workflow-") as directory:
            path = Path(directory) / "ci.yml"
            path.write_text(example["source"], encoding="utf-8")
            subprocess.run([actionlint, "-color=false", str(path)], check=True, cwd=ROOT)


check_numbers()
check_archive()
check_workflow(Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else None)
print("P.5.3: SLO, burn rate, rollout, capacity, reproducible archive and workflow verified")
