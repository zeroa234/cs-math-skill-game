"""Verify D.1.1 SQLite schema/constraints, queries, three-valued NULLs, views, and normalization math."""

from itertools import combinations
import sqlite3


def create_sample_db(on_delete="RESTRICT"):
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.executescript(
        f"""
        CREATE TABLE Student (
            sid TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            major TEXT NOT NULL
        ) STRICT;

        CREATE TABLE Course (
            cid TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            credits INTEGER NOT NULL CHECK (credits > 0)
        ) STRICT;

        CREATE TABLE Enroll (
            sid TEXT NOT NULL REFERENCES Student(sid) ON DELETE {on_delete},
            cid TEXT NOT NULL REFERENCES Course(cid) ON DELETE RESTRICT,
            grade INTEGER CHECK (grade IS NULL OR (grade BETWEEN 0 AND 100)),
            PRIMARY KEY (sid, cid)
        ) STRICT;

        CREATE VIEW StudentAverage AS
        SELECT s.sid, s.name, AVG(e.grade) AS avg_grade
        FROM Student s
        JOIN Enroll e ON s.sid = e.sid
        GROUP BY s.sid, s.name;
        """
    )
    conn.executemany(
        "INSERT INTO Student VALUES (?, ?, ?)",
        [("S1", "Mei", "CS"), ("S2", "Lin", "Math"), ("S3", "Jia", "CS"), ("S4", "Mei", "Math")],
    )
    conn.executemany(
        "INSERT INTO Course VALUES (?, ?, ?)",
        [("C1", "Databases", 4), ("C2", "Systems", 4), ("C3", "Algorithms", 3)],
    )
    conn.executemany(
        "INSERT INTO Enroll VALUES (?, ?, ?)",
        [("S1", "C1", 96), ("S1", "C2", 84), ("S1", "C3", None), ("S2", "C1", 80), ("S4", "C3", None)],
    )
    conn.commit()
    return conn


def check_constraints_and_queries():
    conn = create_sample_db("RESTRICT")
    bad_statements = [
        ("INSERT INTO Student VALUES (NULL, 'X', 'CS')", ()),
        ("INSERT INTO Course VALUES ('C9', 'Bad', 0)", ()),
        ("INSERT INTO Course VALUES ('C9', 'NullCr', NULL)", ()),
        ("INSERT INTO Enroll VALUES ('S2', 'C2', 120)", ()),
        ("INSERT INTO Enroll VALUES ('S1', 'C1', 90)", ()),
        ("INSERT INTO Enroll VALUES ('S9', 'C1', 80)", ()),
        ("DELETE FROM Student WHERE sid = 'S1'", ()),
    ]
    for sql, params in bad_statements:
        try:
            conn.execute(sql, params)
            raise AssertionError(f"Expected constraint error for: {sql}")
        except sqlite3.IntegrityError:
            pass

    assert conn.execute("SELECT grade FROM Enroll WHERE sid = 'S1' AND cid = 'C2'").fetchall() == [(84,)]

    # Algebraic projection + join equivalent to π_name(Student ⋈ Enroll ⋈ σ_title='Databases'(Course))
    db_students = conn.execute(
        """
        SELECT DISTINCT s.name
        FROM Student s
        JOIN Enroll e ON s.sid = e.sid
        JOIN Course c ON e.cid = c.cid
        WHERE c.title = 'Databases'
        ORDER BY s.name
        """
    ).fetchall()
    assert db_students == [("Lin",), ("Mei",)]

    # Left join keeps students with zero enrollments
    assert conn.execute(
        "SELECT s.sid, e.cid FROM Student s LEFT JOIN Enroll e ON s.sid = e.sid WHERE s.sid = 'S3'"
    ).fetchall() == [("S3", None)]

    # Major counts & >85 average
    assert conn.execute("SELECT major, COUNT(*) FROM Student GROUP BY major ORDER BY major").fetchall() == [
        ("CS", 2),
        ("Math", 2),
    ]
    assert conn.execute(
        "SELECT sid, AVG(grade) FROM Enroll GROUP BY sid HAVING AVG(grade) > 85"
    ).fetchall() == [("S1", 90.0)]

    # NOT EXISTS & three-valued NULL trap
    assert conn.execute(
        """
        SELECT s.sid, s.name FROM Student s
        WHERE NOT EXISTS (SELECT 1 FROM Enroll e WHERE e.sid = s.sid)
        """
    ).fetchall() == [("S3", "Jia")]
    assert conn.execute("SELECT COUNT(*) FROM Enroll WHERE grade IS NULL").fetchone()[0] == 2
    assert conn.execute("SELECT COUNT(*) FROM Enroll WHERE grade = NULL").fetchone()[0] == 0
    assert conn.execute("SELECT CASE WHEN 70 NOT IN (SELECT grade FROM Enroll) THEN 1 ELSE 0 END").fetchone()[0] == 0

    # Dynamic view reflects underlying DML changes
    assert conn.execute("SELECT sid, avg_grade FROM StudentAverage ORDER BY sid").fetchall() == [
        ("S1", 90.0),
        ("S2", 80.0),
        ("S4", None),
    ]
    conn.execute("UPDATE Enroll SET grade = 82 WHERE sid = 'S1' AND cid = 'C2'")
    assert conn.execute("SELECT avg_grade FROM StudentAverage WHERE sid = 'S1'").fetchone()[0] == 89.0

    # Cascade delete demo
    c_conn = create_sample_db("CASCADE")
    c_conn.execute("DELETE FROM Student WHERE sid = 'S1'")
    assert c_conn.execute("SELECT sid, cid FROM Enroll ORDER BY sid, cid").fetchall() == [
        ("S2", "C1"),
        ("S4", "C3"),
    ]


def closure(attrs, fds):
    res = set(attrs)
    changed = True
    while changed:
        changed = False
        for lhs, rhs in fds:
            if set(lhs) <= res and not (set(rhs) <= res):
                res |= set(rhs)
                changed = True
    return res


def candidate_keys(schema, fds):
    all_attrs = set(schema)
    keys = []
    for r in range(1, len(schema) + 1):
        for sub in combinations(sorted(all_attrs), r):
            s = frozenset(sub)
            if closure(s, fds) == all_attrs and not any(k <= s for k in keys):
                keys.append(s)
    return set(keys)


def check_normalization():
    # R(sid, name, cid, title, grade) encoded as S,N,C,T,G
    fds = [("S", "N"), ("C", "T"), ("SC", "G")]
    assert candidate_keys("SNCTG", fds) == {frozenset({"S", "C"})}
    assert candidate_keys("SN", [("S", "N")]) == {frozenset({"S"})}
    assert candidate_keys("CT", [("C", "T")]) == {frozenset({"C"})}
    assert candidate_keys("SCG", [("SC", "G")]) == {frozenset({"S", "C"})}

    # 3NF but not BCNF example: (Student, Course, Teacher) with {T->C, SC->T}
    fds_3nf = [("T", "C"), ("SC", "T")]
    assert candidate_keys("SCT", fds_3nf) == {frozenset({"S", "C"}), frozenset({"S", "T"})}

    # Dependency preservation counterexample on BCNF decomposition (T, C) and (S, T)
    conn = sqlite3.connect(":memory:")
    conn.executescript(
        """
        CREATE TABLE TC (teacher TEXT PRIMARY KEY, course TEXT);
        CREATE TABLE ST (student TEXT, teacher TEXT REFERENCES TC(teacher), PRIMARY KEY (student, teacher));
        INSERT INTO TC VALUES ('Wu', 'DB'), ('Li', 'DB');
        INSERT INTO ST VALUES ('S1', 'Wu'), ('S1', 'Li');
        """
    )
    dups = conn.execute(
        """
        SELECT st.student, tc.course, COUNT(*)
        FROM ST st JOIN TC tc ON st.teacher = tc.teacher
        GROUP BY st.student, tc.course
        HAVING COUNT(*) > 1
        """
    ).fetchall()
    assert dups == [("S1", "DB", 2)]


if __name__ == "__main__":
    check_constraints_and_queries()
    check_normalization()
    print("D.1.1 verify: all SQLite constraints, joins, NULL 3VL, views, and BCNF/3NF checks passed.")
