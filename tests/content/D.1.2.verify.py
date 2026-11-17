"""Verify D.1.2 B+Tree heights/IO, join IO costs, precedence graphs, WAL/ARIES, and SQLite query plans."""

from graphlib import CycleError, TopologicalSorter
from math import ceil
import sqlite3


def bplus_levels(num_rows, leaf_cap=200, fanout=200):
    leaves = ceil(num_rows / leaf_cap)
    levels = [leaves]
    cur = leaves
    while cur > 1:
        cur = ceil(cur / fanout)
        levels.append(cur)
    return levels  # [leaves, ..., 1] -> total index tree depth = len(levels)


def check_bplus_and_joins():
    # 10^7 rows, 200 leaf entries & internal fanout -> [50_000, 250, 2, 1] => 4 index tree levels
    lvls = bplus_levels(10_000_000, 200, 200)
    assert lvls == [50_000, 250, 2, 1]
    assert len(lvls) == 4  # 4 index page I/Os; +1 for heap fetch if non-clustered (= 5)
    assert ceil(10_000_000 / 100) == 100_000

    assert bplus_levels(400 * 200, 200, 20) == [400, 20, 1]
    assert bplus_levels(100 * 200, 200, 10) == [100, 10, 1]

    # Join IO calculations: R=1000, S=500, B=102
    r_pages, s_pages, b_buf = 1000, 500, 102
    bnl_chunk = b_buf - 2  # 100 pages per chunk + 1 input + 1 output
    assert bnl_chunk == 100
    assert s_pages + ceil(s_pages / bnl_chunk) * r_pages == 5500

    # Smaller illustration: R=60, S=40, B=12 -> chunk=10 -> 40 + 4*60 = 280
    assert 40 + ceil(40 / 10) * 60 == 280
    # R=40, S=25, B=12 -> chunk=10 -> 25 + 3*40 = 145
    assert 25 + ceil(25 / 10) * 40 == 145

    # External merge sort passes check: ceil(1000/102)=10 runs, ceil(500/102)=5 runs, 10+5 <= 101
    r_runs = ceil(r_pages / b_buf)
    s_runs = ceil(s_pages / b_buf)
    assert (r_runs, s_runs) == (10, 5) and r_runs + s_runs <= b_buf - 1
    # Unoptimized SMJ (sort R: 2*2 passes? No, 10 runs merge in 1 pass => 2 passes*2 I/O=4*R + join scan R+S => 5*(R+S)=7500)
    assert 5 * (r_pages + s_pages) == 7500
    # Combined merge + join optimization saves 2*(R+S) = 3000 -> 4500 I/Os
    assert 5 * (r_pages + s_pages) - 2 * (r_pages + s_pages) == 4500
    # Grace Hash Join: 3 * (R + S) = 4500 I/Os
    assert 3 * (r_pages + s_pages) == 4500


def check_conflict_serializability():
    # Schedule: R1(A) W1(A) R2(A) W2(A) R2(B) W2(B) R1(B) W1(B)
    ops = [
        ("1", "R", "A"), ("1", "W", "A"),
        ("2", "R", "A"), ("2", "W", "A"),
        ("2", "R", "B"), ("2", "W", "B"),
        ("1", "R", "B"), ("1", "W", "B"),
    ]
    edges = set()
    for i in range(len(ops)):
        t1, m1, obj1 = ops[i]
        for j in range(i + 1, len(ops)):
            t2, m2, obj2 = ops[j]
            if t1 != t2 and obj1 == obj2 and ("W" in (m1, m2)):
                edges.add((t1, t2))
    assert edges == {("1", "2"), ("2", "1")}
    ts = TopologicalSorter()
    for u, v in edges:
        ts.add(v, u)
    try:
        list(ts.static_order())
        raise AssertionError("Expected cycle in precedence graph")
    except CycleError:
        pass


def check_sqlite_plan_wal_and_aries():
    conn = sqlite3.connect(":memory:")
    conn.executescript(
        """
        CREATE TABLE orders (oid INTEGER PRIMARY KEY, status TEXT NOT NULL, amount INTEGER NOT NULL);
        INSERT INTO orders VALUES (1, 'paid', 50), (2, 'refunded', 30), (3, 'paid', 20), (4, 'paid', 40);
        """
    )
    plan_no_idx = conn.execute("EXPLAIN QUERY PLAN SELECT oid, status, amount FROM orders WHERE status = 'refunded'").fetchall()
    assert any("SCAN orders" in row[3] for row in plan_no_idx)

    conn.execute("CREATE INDEX orders_status ON orders(status);")
    plan_idx = conn.execute("EXPLAIN QUERY PLAN SELECT oid, status, amount FROM orders WHERE status = 'refunded'").fetchall()
    assert any("SEARCH orders USING INDEX orders_status" in row[3] for row in plan_idx)
    assert conn.execute("SELECT oid, status, amount FROM orders WHERE status = 'refunded'").fetchall() == [(2, "refunded", 30)]

    # ARIES redo/undo state trace: initial {A: 10, B: 20}, T1 commits A=12, T2 uncommitted B=25 crashes
    disk = {"A": 10, "B": 20}
    wal = [("T1", "W", "A", 10, 12), ("T1", "COMMIT"), ("T2", "W", "B", 20, 25)]
    for rec in wal:
        if rec[1] == "W":
            disk[rec[2]] = rec[4]
    assert disk == {"A": 12, "B": 25}  # After Redo phase
    uncommitted = {"T2"}
    for rec in reversed(wal):
        if rec[0] in uncommitted and rec[1] == "W":
            disk[rec[2]] = rec[3]
    assert disk == {"A": 12, "B": 20}  # After Undo phase


if __name__ == "__main__":
    check_bplus_and_joins()
    check_conflict_serializability()
    check_sqlite_plan_wal_and_aries()
    print("D.1.2 verify: all B+Tree, join I/O, precedence graph, query plan, and ARIES checks passed.")
