"""Verify all Python code examples and quantitative architecture assertions in data/content/P.4.4.yaml."""

from __future__ import annotations

import io
import math
import pathlib
import re
from contextlib import redirect_stdout

ROOT = pathlib.Path(__file__).resolve().parents[2]
PACK_PATH = ROOT / "data" / "content" / "P.4.4.yaml"


def extract_fenced_python_blocks(markdown_text: str) -> list[str]:
    blocks: list[str] = []
    lines = markdown_text.splitlines()
    i = 0
    while i < len(lines):
        m = re.match(r"^(\s*)```python\s*$", lines[i])
        if m:
            indent = m.group(1)
            i += 1
            body: list[str] = []
            while i < len(lines) and not re.match(r"^\s*```\s*$", lines[i]):
                line = lines[i]
                if line.startswith(indent):
                    line = line[len(indent) :]
                body.append(line)
                i += 1
            blocks.append("\n".join(body))
        i += 1
    return blocks


def main() -> None:
    text = PACK_PATH.read_text(encoding="utf-8")
    blocks = extract_fenced_python_blocks(text)
    assert len(blocks) == 7, f"Expected 7 fenced Python blocks in P.4.4.yaml, got {len(blocks)}"

    # Block 2 is the self-contained definition repeated in pipeline-filter-calc prompt (no print).
    card_indices = [0, 2, 3, 4, 5, 6]
    card_blocks = [blocks[i] for i in card_indices]

    expected_outputs = [
        "[502, 404]",
        "10 10",
        "avg: 27.8 p99: 20",
        "920 50 870",
        "['book', 'cup', 'pen']",
        "5 95",
    ]

    namespaces: list[dict] = []
    for idx, (code, expected) in enumerate(zip(card_blocks, expected_outputs), start=1):
        buf = io.StringIO()
        ns: dict = {}
        with redirect_stdout(buf):
            exec(compile(code, f"P.4.4_block_{idx}.py", "exec"), ns)
        actual = buf.getvalue().strip()
        assert actual == expected, f"Block {idx} stdout mismatch: got {actual!r}, expected {expected!r}"
        namespaces.append(ns)

    # Also execute the repeated prompt snippet (blocks[1]) directly.
    prompt_ns: dict = {}
    exec(compile(blocks[1], "P.4.4_prompt_pipeline.py", "exec"), prompt_ns)
    assert (
        prompt_ns["extract_codes"](
            prompt_ns["filter_errors"](["INFO:ok", "ERR:502", "ERR:404", "INFO:done"])
        )
        == [502, 404]
    )

    # 1. Pipeline-filter composition assertions (lesson: pipeline-microkernel)
    filter_errors = namespaces[0]["filter_errors"]
    extract_codes = namespaces[0]["extract_codes"]
    assert extract_codes(filter_errors(["INFO:ok", "ERR:502", "ERR:404", "INFO:done"])) == [502, 404]
    assert extract_codes(filter_errors(["INFO:ok"])) == []

    # 2. Event-driven idempotency follow-up calculation (lesson: event-driven, item: idempotent-points-num)
    ev_ns = namespaces[1]
    handle_order_paid = ev_ns["handle_order_paid"]
    assert handle_order_paid("e1", 100) == 10
    assert handle_order_paid("e2", 50) == 15
    assert handle_order_paid("e2", 50) == 15

    # 3. Tail latency p99 formula check (lesson: quality-scenarios + boss-p99-calc)
    p99_ms = namespaces[2]["p99_ms"]
    assert p99_ms([20] * 99 + [800]) == 20
    assert p99_ms([20] * 98 + [800, 900]) == 800
    assert p99_ms([45] * 99 + [645]) == 45
    assert p99_ms([35] * 99 + [235]) == 35
    # Verify integer ceiling formula equals math.ceil(0.99 * n) - 1 across n = 1..500
    for n in range(1, 501):
        assert (99 * n + 99) // 100 - 1 == math.ceil(0.99 * n) - 1

    # 4. Async queue + cache latency math (lesson: tactics-latency, item: tactic-latency-saved)
    assert namespaces[3]["sync_ms"] == 920
    assert namespaces[3]["async_ms"] == 50
    assert namespaces[3]["sync_ms"] - namespaces[3]["async_ms"] == 870

    # 5. CAP AP naive union anomaly check (lesson: cap-pacelc)
    assert sorted(namespaces[4]["naive_merge"]) == ["book", "cup", "pen"]
    # Versioned delete tombstone resolves the anomaly cleanly
    tombstoned_a = {"book": ("add", 1), "pen": ("del", 2)}
    tombstoned_b = {"book": ("add", 1), "pen": ("add", 1), "cup": ("add", 3)}
    merged = {}
    for k in tombstoned_a.keys() | tombstoned_b.keys():
        va = tombstoned_a.get(k, ("none", 0))
        vb = tombstoned_b.get(k, ("none", 0))
        merged[k] = max(va, vb, key=lambda x: x[1])
    active_items = sorted(k for k, (op, _) in merged.items() if op == "add")
    assert active_items == ["book", "cup"]

    # 6. Canary 5% traffic calculation (lesson: release-deployments, item: canary-count-num)
    routed_200 = ["canary" if req_id % 100 < 5 else "stable" for req_id in range(200)]
    assert routed_200.count("canary") == 10
    assert routed_200.count("stable") == 190

    print("ok — verified 6 Python blocks and architecture quantitative assertions in P.4.4.yaml")


if __name__ == "__main__":
    main()
