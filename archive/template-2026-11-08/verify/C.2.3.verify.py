"""Check resource examples and the exact namespace, Pod and Dockerfile snippets.

Requires Linux or WSL with unprivileged user namespaces enabled for --linux.
The Dockerfile and Pod are checked as configuration; no daemon or cluster is needed.
"""

from fractions import Fraction
import json
from pathlib import Path
import re
import shlex
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]


def examples():
    result = subprocess.check_output(
        ["node", "--input-type=module", "-e", """
          import fs from 'node:fs';
          import {load} from 'js-yaml';
          const pack = load(fs.readFileSync('data/content/C.2.3.yaml', 'utf8'));
          const snippets = Object.fromEntries(['isolation', 'requests', 'docker-build'].map(id => {
            const lesson = pack.lessons.find(l => l.id === id);
            const block = lesson.flow.find(s => s.card?.body.includes('```')).card.body;
            return [id, block.split('```')[1].split('\\n').slice(1).join('\\n')];
          }));
          console.log(JSON.stringify({...snippets, requests: load(snippets.requests)}));
        """], cwd=ROOT, encoding="utf-8",
    )
    return json.loads(result)


def check_resources(pod):
    assert Fraction(200_000, 100_000) == 2
    assert Fraction(150_000, 100_000) == Fraction("1.5")
    assert Fraction(250_000, 100_000) == Fraction("2.5")
    assert 100_000 // 1000 == 100  # microseconds to milliseconds
    assert 4 * 1024**3 == 4_294_967_296
    assert Fraction(500 + 500, 1000) == 1
    assert 128 * 2 == 256 > 200

    assert pod["apiVersion"] == "v1" and pod["kind"] == "Pod"
    assert len(pod["spec"]["containers"]) == 1
    resources = pod["spec"]["containers"][0]["resources"]
    assert resources == {
        "requests": {"cpu": "500m", "memory": "128Mi"},
        "limits": {"cpu": "1", "memory": "256Mi"},
    }

    for request, nodes in [
        ((700, 256), {"A": (600, 512), "B": (1000, 300), "C": (900, 200)}),
        ((600, 300), {"A": (1000, 200), "B": (800, 400), "C": (500, 600)}),
    ]:
        feasible = [name for name, (cpu, memory) in nodes.items()
                    if cpu >= request[0] and memory >= request[1]]
        assert feasible == ["B"]


def check_dockerfile(dockerfile):
    lines = dockerfile.strip().splitlines()
    assert lines[:6] == [
        "FROM python:3.12-slim", "WORKDIR /app", "COPY requirements.txt ./",
        "RUN python -m pip install --no-cache-dir -r requirements.txt", "COPY app.py ./",
        "EXPOSE 8000",
    ]
    assert json.loads(lines[6].removeprefix("CMD ")) == [
        "python", "-m", "flask", "--app", "app", "run", "--host", "0.0.0.0", "--port", "8000",
    ]
    pack = (ROOT / "data/content/C.2.3.yaml").read_text(encoding="utf-8")
    host, exposed, target = re.search(r"-p (127\.0\.0\.1):(\d+):(\d+)", pack).groups()
    assert (host, int(exposed), int(target)) == ("127.0.0.1", 8080, 8000)


def check_namespaces(command):
    prefix = ["wsl.exe", "-e"] if sys.platform == "win32" else []
    inside = subprocess.check_output(prefix + shlex.split(command), encoding="utf-8")
    lines = inside.splitlines()
    assert lines[0] == "1"
    assert lines[2].split() == ["1", "sh"]
    assert lines[3].split() == ["2", "ps"]
    path = subprocess.check_output(prefix + [
        "unshare", "--user", "--map-root-user", "--cgroup", "cat", "/proc/self/cgroup",
    ], encoding="utf-8")
    assert "0::/" in path.splitlines()


sample = examples()
check_resources(sample["requests"])
check_dockerfile(sample["docker-build"])
if "--linux" in sys.argv:
    check_namespaces(sample["isolation"])
print("C.2.3: resource arithmetic, Pod and Dockerfile checked"
      + (", Linux namespace examples executed" if "--linux" in sys.argv else ""))
