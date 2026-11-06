"""Check the lesson's arithmetic, lock schedule and actual pipe EOF behavior."""
import itertools
import json
import os
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

assert len(b"abcdefghij"[6:]) == 4
assert sum([2, 7, 3, 6]) == 18
read_a = read_b = 0
write_a, write_b = read_a + 1, read_b + 1
assert write_a == write_b == 1
assert 5 + 2 == 7
assert 20 + 3 == 23

# Any serialization of two atomic additions returns the old values 8, 9.
for order in itertools.permutations(("A", "B")):
    count = 8
    prior = {}
    for thread in order:
        prior[thread] = count
        count += 1
    assert [prior[thread] for thread in order] == [8, 9]
    assert count == 10

# Each thread now waits for the other thread to free its next lock.
held = {"a": "A", "b": "B"}
wanted = {"A": "b", "B": "a"}
assert held[wanted["A"]] == "B"
assert held[wanted["B"]] == "A"

reader, writer = os.pipe()
try:
    other_writer = os.dup(writer)
    try:
        assert os.write(other_writer, b"hello") == 5
        assert os.read(reader, 16) == b"hello"
    finally:
        os.close(other_writer)
finally:
    os.close(writer)
    try:
        assert os.read(reader, 16) == b""
    finally:
        os.close(reader)


# Compile the exact fenced C examples from the pack. Node uses the same YAML parser as the build.
project = Path(__file__).resolve().parents[2]
examples = json.loads(subprocess.check_output(
    ["node", "--input-type=module", "-e", """
      import fs from 'node:fs';
      import {load} from 'js-yaml';
      const pack = load(fs.readFileSync('data/content/C.2.2.yaml', 'utf8'));
      const snippets = {};
      for (const lesson of pack.lessons) {
        for (const {card} of lesson.flow.filter(step => step.card)) {
          for (const {body} of [card, ...(card.reveal || [])]) {
            const match = /```c\\n([\\s\\S]+?)\\n```/.exec(body);
            if (match) snippets[lesson.id] = match[1];
          }
        }
      }
      console.log(JSON.stringify(snippets));
    """], cwd=project, encoding="utf-8",
))
expected = {"threads": "18", "pipe": "hello"}
assert examples.keys() == expected.keys()

if os.name == "nt":
    linux = ["wsl.exe", "-e"]
    def compiler_path(path):
        return subprocess.check_output(
            linux + ["wslpath", "-a", str(path)], text=True, timeout=15
        ).strip()
else:
    linux = []
    def compiler_path(path):
        return str(path)

(project / "temp").mkdir(exist_ok=True)
with TemporaryDirectory(prefix="c22-verify-", dir=project / "temp") as work:
    for name, source in examples.items():
        c_file = Path(work) / (name + ".c")
        c_file.write_text(source, encoding="utf-8")
        program = Path(work) / name
        subprocess.run(linux + [
            "gcc", "-std=c11", "-Wall", "-Wextra", "-Werror", "-pthread",
            compiler_path(c_file), "-o", compiler_path(program),
        ], check=True, timeout=30)
        output = subprocess.check_output(linux + [compiler_path(program)], text=True, timeout=15)
        assert output.strip() == expected[name], (name, output)

print("C.2.2: arithmetic, lock and atomic models, pipe EOF and exact gcc examples verified")
