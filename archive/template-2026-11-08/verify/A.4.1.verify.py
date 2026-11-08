"""Verify PSI and exercise the exact FastAPI example with its test client."""
from math import log
from pathlib import Path
import json
import subprocess
import sys

reference, current = [.25] * 4, [.10, .20, .30, .40]
contributions = [(a-e)*log(a/e) for a, e in zip(current, reference)]
assert round(contributions[0], 4) == .1374
assert round(sum(contributions), 4) == .2282
assert sum(contributions) > .2 and round(.07+.05, 2) == .12

project = Path(__file__).resolve().parents[2]
verification_libs = project / "temp/ai-verify/libs"
if verification_libs.is_dir():
    sys.path.insert(0, str(verification_libs))
from fastapi.testclient import TestClient

source = json.loads(subprocess.check_output(
    ["node", "--input-type=module", "-e", """
      import fs from 'node:fs';
      import {load} from 'js-yaml';
      const pack = load(fs.readFileSync('data/content/A.4.1.yaml', 'utf8'));
      const lesson = pack.lessons.find(l => l.id === 'serve');
      const body = lesson.flow.find(step => step.card?.reveal).card.reveal.at(-1).body;
      console.log(JSON.stringify(body.split('```')[1].slice('python\\n'.length)));
    """], cwd=project, encoding="utf-8",
))
namespace = {}
exec(compile(source, "A.4.1 serve", "exec"), namespace)
with TestClient(namespace["app"]) as client:
    reply = client.post("/predict", json={"x": 3})
    assert reply.status_code == 200 and reply.json() == {"prediction": 7, "model_version": "demo-1"}
    assert client.post("/predict", json={}).status_code == 422
    assert client.post("/predict", json={"x": "inf"}).status_code == 422
print("A.4.1: PSI and exact FastAPI inference/validation example verified")
