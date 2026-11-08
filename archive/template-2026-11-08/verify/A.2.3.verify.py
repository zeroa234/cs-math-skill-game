"""Check the forward/backward examples and validate the exact loop's Python syntax."""
from fractions import Fraction as F
from itertools import product
from math import isclose
from pathlib import Path
import json
import subprocess

assert [(a+b-F("1.5") > 0) for a, b in product((0, 1), repeat=2)] == [False, False, False, True]
assert 1-F("1.5") == F("-.5")
assert 2-F(".1")*3 == F("1.7") and 5-F(".25")*4 == 4
assert F(".5")**3 == F(".125") and F(2, 50) == F(".04")
assert 3-1 == 2 and 4-2 == 2
x = [1, 2]
def predict(w):
    w11, w12, w21, w22, w31, w32, bias = w
    h1 = max(0, w11*x[0]+w12*x[1])
    h2 = max(0, w21*x[0]+w22*x[1])
    return w31*h1 + w32*h2 + bias
def loss(w):
    return (predict(w)-1)**2/2

weights = [1, -1, .5, 1, 1, -2, .5]
assert predict(weights) == -4.5
for i, expected in enumerate([0, 0, 11, 22, 0, -13.75, -5.5]):
    plus, minus = weights[:], weights[:]
    plus[i] += .0001
    minus[i] -= .0001
    numerical = (loss(plus)-loss(minus))/.0002
    assert isclose(numerical, expected, rel_tol=1e-8, abs_tol=1e-8)

project = Path(__file__).resolve().parents[2]
source = json.loads(subprocess.check_output(
    ["node", "--input-type=module", "-e", """
      import fs from 'node:fs';
      import {load} from 'js-yaml';
      const pack = load(fs.readFileSync('data/content/A.2.3.yaml', 'utf8'));
      const lesson = pack.lessons.find(l => l.id === 'torch-loop');
      const body = lesson.flow.find(step => step.card?.body.includes('```python')).card.body;
      console.log(JSON.stringify(body.split('```')[1].slice('python\\n'.length)));
    """], cwd=project, encoding="utf-8",
))
compile(source, "A.2.3 torch-loop", "exec")
print("A.2.3: forward pass, independent finite-difference gradients and Python syntax verified")
