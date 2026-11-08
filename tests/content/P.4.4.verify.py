"""Check the measurements and small failure models used by P.4.4."""

from contextlib import closing
from fractions import Fraction
from math import ceil
import sqlite3


def rank99(count):
    return ceil(Fraction(99 * count, 100))


assert rank99(100) == 99
assert rank99(1000) == 990
latencies = [300] * 990 + [900] * 10
assert sorted(latencies)[rank99(len(latencies)) - 1] == 300
assert Fraction(20, 1000) == Fraction(2, 100) > Fraction(1, 100)

# A presence-only example: removal covers the exact addition it had seen.
seen_add = ("book", "site-a", 1)
concurrent_add = ("book", "site-b", 1)
assert {"book"} | set() == {"book"}  # visible-state union resurrects the item
assert ({seen_add} | {seen_add}) - {seen_add} == set()
assert ({seen_add} | {concurrent_add}) - {seen_add} == {concurrent_add}

# A repeated queue delivery is distinguishable by its stable event identifier.
deliveries = ["order-1", "order-1", "order-2"]
assert list(dict.fromkeys(deliveries)) == ["order-1", "order-2"]

# One local transaction can roll back both statements together.
with closing(sqlite3.connect(":memory:")) as db:
    db.executescript("""
        CREATE TABLE inventory (qty INTEGER);
        CREATE TABLE orders (id INTEGER PRIMARY KEY);
        INSERT INTO inventory VALUES (3);
        INSERT INTO orders VALUES (1);
    """)
    try:
        with db:
            db.execute("UPDATE inventory SET qty = qty - 1")
            db.execute("INSERT INTO orders VALUES (1)")
    except sqlite3.IntegrityError:
        pass
    else:
        raise AssertionError("duplicate order should fail")
    assert db.execute("SELECT qty FROM inventory").fetchone() == (3,)

print("P.4.4 p99, canary rate, merge, repeated delivery and local rollback passed")
