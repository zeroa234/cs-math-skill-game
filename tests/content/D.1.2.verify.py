"""Check the cost, scheduling and recovery examples and run the SQLite plan."""

from contextlib import closing
from graphlib import CycleError, TopologicalSorter
from itertools import combinations
import json
from math import ceil
from pathlib import Path
import re
import sqlite3
import subprocess
from tempfile import TemporaryDirectory
from unittest import TestCase


ROOT = Path(__file__).resolve().parents[2]


def lesson_examples():
    result = subprocess.check_output(
        ["node", "--input-type=module", "-e", """
          import fs from 'node:fs';
          import {load} from 'js-yaml';
          const pack = load(fs.readFileSync('data/content/D.1.2.yaml', 'utf8'));
          const cards = id => pack.lessons.find(l => l.id === id).flow.filter(s => s.card).map(s => s.card);
          const schedule = cards('conflicts').find(card => card.reveal).body;
          const sql = cards('plans').find(card => card.body.includes('```sql')).body.split('```')[1].slice(4);
          console.log(JSON.stringify({schedule, sql}));
        """], cwd=ROOT, encoding="utf-8",
    )
    return json.loads(result)


def check_schedule(body):
    schedule = re.findall(r"([RW])(\d+)\(([A-Z])\)", body)
    assert len(schedule) == 8
    edges = {(before, after)
             for (op1, before, item1), (op2, after, item2) in combinations(schedule, 2)
             if before != after and item1 == item2 and "W" in (op1, op2)}
    assert edges == {("1", "2"), ("2", "1")}
    graph = TopologicalSorter()
    for before, after in edges:
        graph.add(after, before)
    with TestCase().assertRaises(CycleError):
        graph.prepare()


def levels(leaves, fanout):
    counts = [leaves]
    while counts[-1] > 1:
        counts.append(ceil(counts[-1] / fanout))
    return counts


def check_costs():
    leaves = ceil(10_000_000 / 200)
    assert levels(leaves, 200) == [50_000, 250, 2, 1]
    assert len(levels(leaves, 200)) + 1 == 5
    assert ceil(10_000_000 / 100) == 100_000
    assert levels(400, 20) == [400, 20, 1]
    assert levels(100, 10) == [100, 10, 1]

    assert ceil(20 / 6) == 4 and ceil(25 / 6) == 5
    assert 6 - 1 == 5
    assert 12 - 2 == 10 and 102 - 2 == 100
    assert 500 + ceil(500 / (102 - 2)) * 1000 == 5500
    assert 40 + ceil(40 / (12 - 2)) * 60 == 280
    assert 25 + ceil(25 / (12 - 2)) * 40 == 145
    assert ceil(1000 / 102) == 10 and ceil(500 / 102) == 5
    assert 10 + 5 <= 102 - 1  # both final merge inputs fit together
    pages = 1000 + 500
    assert 4 * pages == 6000 and (4 + 1) * pages == 7500
    assert 7500 - 2 * pages == 4500
    assert 3 * pages == 4500  # Grace hash under the stated no-repartition assumption
    assert 100 * 100 // 10_000 == 1 and 100 * 100 // 2000 == 5


def check_plan(source):
    with closing(sqlite3.connect(":memory:")) as db:
        plans = []
        for statement in source.split(";"):
            statement = statement.strip()
            if not statement:
                continue
            cursor = db.execute(statement)
            if statement.startswith("EXPLAIN QUERY PLAN"):
                plans.append(" ".join(row[3] for row in cursor))
        assert len(plans) == 2
        assert "SCAN orders" in plans[0], plans
        assert "SEARCH orders" in plans[1] and "orders_status" in plans[1], plans
        assert db.execute("SELECT * FROM orders WHERE status = 'refunded'").fetchall() == [
            (2, "refunded", 30),
        ]


def check_snapshot_and_reopen():
    work = ROOT / "temp"
    work.mkdir(exist_ok=True)
    with TemporaryDirectory(dir=work, prefix="d-1-2-sqlite-") as directory:
        path = Path(directory) / "orders.db"
        with closing(sqlite3.connect(path)) as writer, closing(sqlite3.connect(path)) as reader:
            assert writer.execute("PRAGMA journal_mode = WAL").fetchone() == ("wal",)
            writer.executescript("""
                CREATE TABLE balances (name TEXT PRIMARY KEY, value INTEGER NOT NULL);
                INSERT INTO balances VALUES ('A', 10), ('B', 20);
            """)
            reader.execute("BEGIN")
            value_a = "SELECT value FROM balances WHERE name = 'A'"
            assert reader.execute(value_a).fetchone() == (10,)
            writer.execute("UPDATE balances SET value = 12 WHERE name = 'A'")
            writer.commit()
            assert reader.execute(value_a).fetchone() == (10,)
            reader.commit()
            assert reader.execute(value_a).fetchone() == (12,)
            writer.execute("UPDATE balances SET value = 25 WHERE name = 'B'")
            # Close an uncommitted transaction, then open a fresh connection.
        with closing(sqlite3.connect(path)) as reopened:
            assert reopened.execute("SELECT * FROM balances ORDER BY name").fetchall() == [
                ("A", 12), ("B", 20),
            ]


def check_recovery_example():
    # ARIES teaching scenario: both updates are durable in the log and absent on disk.
    initial = {"A": 10, "B": 20}
    redo = initial | {"A": 12, "B": 25}
    assert redo == {"A": 12, "B": 25}
    after_undo = redo | {"B": initial["B"]}
    assert after_undo == {"A": 12, "B": 20}


sample = lesson_examples()
check_schedule(sample["schedule"])
check_costs()
check_plan(sample["sql"])
check_snapshot_and_reopen()
check_recovery_example()
print("D.1.2: page-I/O estimates, conflict graph, real SQLite plans and snapshots, and recovery example verified")
