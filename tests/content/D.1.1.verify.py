"""Execute the lesson SQL and independently check the worked dependency examples."""

from contextlib import closing
from itertools import combinations
import json
from pathlib import Path
import sqlite3
import subprocess
from unittest import TestCase


ROOT = Path(__file__).resolve().parents[2]


def lesson_sql():
    result = subprocess.check_output(
        ["node", "--input-type=module", "-e", """
          import fs from 'node:fs';
          import {load} from 'js-yaml';
          const pack = load(fs.readFileSync('data/content/D.1.1.yaml', 'utf8'));
          const ids = ['schema', 'rows', 'joins', 'groups', 'subqueries', 'views'];
          const snippets = Object.fromEntries(ids.map(id => {
            const lesson = pack.lessons.find(l => l.id === id);
            const sql = lesson.flow.flatMap(({card}) => [
              ...String(card?.body ?? '').matchAll(/```sql\\n([\\s\\S]+?)```/g),
            ]).map(match => match[1]);
            return [id, sql];
          }));
          console.log(JSON.stringify(snippets));
        """], cwd=ROOT, encoding="utf-8",
    )
    return json.loads(result)


def check_database(db, source):
    db.executescript(source["schema"][0])
    db.executescript(source["rows"][0])
    assert db.execute("PRAGMA foreign_keys").fetchone() == (1,)

    with TestCase().assertRaises(sqlite3.IntegrityError):
        db.execute("INSERT INTO Student VALUES (NULL, 'A', 'CS')")
    with TestCase().assertRaises(sqlite3.IntegrityError):
        db.execute("INSERT INTO Course VALUES ('C4', 'Invalid', 0)")
    with TestCase().assertRaises(sqlite3.IntegrityError):
        db.execute("INSERT INTO Course VALUES ('C4', 'Invalid', NULL)")
    with TestCase().assertRaises(sqlite3.IntegrityError):
        db.execute("INSERT INTO Enroll VALUES ('S3', 'C1', 120)")
    with TestCase().assertRaises(sqlite3.IntegrityError):
        db.execute("INSERT INTO Enroll VALUES ('S1', 'C1', 96)")
    with TestCase().assertRaises(sqlite3.IntegrityError):
        db.execute("INSERT INTO Enroll VALUES ('S9', 'C1', 100)")
    with TestCase().assertRaises(sqlite3.IntegrityError):
        db.execute("DELETE FROM Student WHERE sid = 'S1'")

    assert db.execute("SELECT grade FROM Enroll WHERE sid = 'S1' AND cid = 'C2'").fetchall() == [(84.0,)]
    joins = source["joins"][0]
    assert db.execute(joins).fetchall() == [("S1", "Mei"), ("S2", "Lin"), ("S4", "Mei")]
    names = joins.replace("s.sid, s.name", "s.name").replace("ORDER BY s.sid", "ORDER BY s.name")
    assert db.execute(names).fetchall() == [("Lin",), ("Mei",)]
    assert len(db.execute(joins.replace("DISTINCT ", "")).fetchall()) == 4
    assert db.execute("""
        SELECT s.sid, e.cid FROM Student s LEFT JOIN Enroll e ON e.sid = s.sid
        WHERE s.sid = 'S3'
    """).fetchall() == [("S3", None)]

    counts, averages = source["groups"]
    assert db.execute(counts).fetchall() == [("CS", 2), ("Math", 2)]
    assert db.execute(averages).fetchall() == [("S1", 90.0)]
    assert db.execute(source["subqueries"][0]).fetchall() == [("S3", "Jia")]
    assert db.execute("SELECT COUNT(*) FROM Enroll WHERE grade IS NULL").fetchone() == (2,)
    assert db.execute("SELECT COUNT(*) FROM Enroll WHERE grade = NULL").fetchone() == (0,)
    assert db.execute("SELECT 70 NOT IN (SELECT grade FROM Enroll)").fetchone() == (None,)

    db.execute(source["views"][0])
    read_view = "SELECT sid, average_grade FROM StudentAverage ORDER BY sid"
    assert db.execute(read_view).fetchall() == [("S1", 90.0), ("S2", 80.0), ("S4", None)]
    db.execute("UPDATE Enroll SET grade = 82 WHERE sid = 'S1' AND cid = 'C2'")
    assert db.execute(read_view).fetchall() == [("S1", 89.0), ("S2", 80.0), ("S4", None)]
    db.execute("DELETE FROM Enroll WHERE sid = 'S1' AND cid = 'C2'")
    assert db.execute(read_view).fetchall() == [("S1", 96.0), ("S2", 80.0), ("S4", None)]


def check_referential_actions(source):
    with closing(sqlite3.connect(":memory:")) as db:
        db.executescript(source["schema"][0].replace("ON DELETE RESTRICT", "ON DELETE CASCADE"))
        db.executescript(source["rows"][0])
        db.execute("DELETE FROM Student WHERE sid = 'S1'")
        assert db.execute("SELECT sid, cid FROM Enroll ORDER BY sid").fetchall() == [("S2", "C1"), ("S4", "C3")]


def subsets(attributes):
    return {frozenset(items) for size in range(len(attributes) + 1)
            for items in combinations(sorted(attributes), size)}


def agreements(attributes, rules):
    # Each subset represents columns on which an arbitrary pair of rows agree.
    # An FD rules out precisely those pairs agreeing on its left but not its right.
    return {same for same in subsets(attributes)
            if all(not set(left) <= same or set(right) <= same for left, right in rules)}


def candidate_keys(attributes, allowed):
    # A determinant is a superkey only when the sole possible agreement superset is the full row.
    superkeys = {key for key in subsets(attributes)
                 if not any(key <= same < attributes for same in allowed)}
    return {key for key in superkeys if not any(other < key for other in superkeys)}


def check_dependencies():
    original = set("SNCTG")
    rules = [("S", "N"), ("C", "T"), ("SC", "G")]
    valid = agreements(original, rules)
    assert candidate_keys(original, valid) == {frozenset("SC")}
    assert set.intersection(*(set(same) for same in valid if "C" in same)) == set("CT")
    assert set.intersection(*(set(same) for same in valid if "S" in same)) == set("SN")

    parts = [set("SN"), set("CT"), set("SCG")]
    for left, right in rules:
        assert any(set(left + right) <= part for part in parts)
    assert {frozenset("S")} == candidate_keys(parts[0], {row & parts[0] for row in valid})
    assert {frozenset("C")} == candidate_keys(parts[1], {row & parts[1] for row in valid})
    assert {frozenset("SC")} == candidate_keys(parts[2], {row & parts[2] for row in valid})

    another = set("SCT")
    restricted = agreements(another, [("T", "C"), ("SC", "T")])
    assert candidate_keys(another, restricted) == {frozenset("SC"), frozenset("ST")}
    assert set.intersection(*(set(same) for same in restricted if "T" in same)) == set("TC")
    assert agreements(set("ABC"), [("A", "B"), ("B", "C"), ("A", "C")]) == agreements(
        set("ABC"), [("A", "B"), ("B", "C")],
    )

    with closing(sqlite3.connect(":memory:")) as db:
        db.executescript("""
            CREATE TABLE TC (teacher TEXT PRIMARY KEY, course TEXT);
            CREATE TABLE ST (student TEXT, teacher TEXT, PRIMARY KEY (student, teacher));
            INSERT INTO TC VALUES ('T1', 'C1'), ('T2', 'C1');
            INSERT INTO ST VALUES ('S1', 'T1'), ('S1', 'T2');
        """)
        assert db.execute("""
            SELECT student, course, COUNT(*) FROM ST JOIN TC USING (teacher)
            GROUP BY student, course HAVING COUNT(*) > 1
        """).fetchall() == [("S1", "C1", 2)]


sql = lesson_sql()
with closing(sqlite3.connect(":memory:")) as connection:
    check_database(connection, sql)
check_referential_actions(sql)
check_dependencies()
print("D.1.1: exact SQLite snippets, constraints, queries, views and dependency examples verified")
