"""Run the independent Kotlin, Dart and SQLite teaching examples."""

from argparse import ArgumentParser
from contextlib import closing
import os
from pathlib import Path
import re
import sqlite3
import subprocess
from tempfile import TemporaryDirectory
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[2]
TEXT = (ROOT / "data/content/P.5.2.yaml").read_text(encoding="utf-8")


def blocks(language):
    return [dedent(block).strip() for block in re.findall(
        rf"^ +```{language}\n(.*?)^ +```$", TEXT, re.MULTILINE | re.DOTALL
    )]


def run(command, directory, env):
    result = subprocess.run(command, cwd=directory, env=env, capture_output=True,
                            text=True, timeout=30)
    assert result.returncode == 0, result.stderr or result.stdout
    return result.stdout.strip()


def check_sync():
    statement, = blocks("sql")
    with closing(sqlite3.connect(":memory:")) as db:
        db.executescript("""
            CREATE TABLE Task(id TEXT PRIMARY KEY, done INTEGER NOT NULL);
            CREATE TABLE Pending(op_id TEXT PRIMARY KEY, task_id TEXT, base_revision INTEGER, done INTEGER);
            INSERT INTO Task VALUES ('task-7', 0);
        """)
        db.executescript(statement)
        assert db.execute("SELECT done FROM Task WHERE id='task-7'").fetchone() == (1,)
        assert db.execute("SELECT * FROM Pending").fetchall() == [("op-17", "task-7", 4, 1)]

        # Replaying a duplicate local transaction must not leave its partial write.
        db.execute("UPDATE Task SET done=0 WHERE id='task-7'")
        db.commit()
        try:
            db.executescript(statement)
        except sqlite3.IntegrityError:
            db.rollback()
        else:
            raise AssertionError("the existing operation identifier must reject the duplicate")
        assert db.execute("SELECT done FROM Task WHERE id='task-7'").fetchone() == (0,)
        assert db.execute("SELECT count(*) FROM Pending").fetchone() == (1,)

    assert 2 + 3 == 5
    print("P.5.2 local transaction and duplicate-operation rollback passed")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--kotlinc", type=Path)
    parser.add_argument("--java", type=Path)
    parser.add_argument("--dart", type=Path)
    args = parser.parse_args()
    if bool(args.kotlinc) != bool(args.java):
        parser.error("--kotlinc and --java must be used together")

    check_sync()
    temp = ROOT / "temp"
    temp.mkdir(exist_ok=True)
    with TemporaryDirectory(dir=temp, prefix="p-5-2-verify-") as directory:
        work = Path(directory)
        env = os.environ.copy()
        env["TMP"] = env["TEMP"] = directory
        env["PUB_CACHE"] = str(work / "pub-cache")
        env["DART_DISABLE_ANALYTICS"] = "true"
        if args.kotlinc:
            java = args.java.resolve()
            env["JAVA_HOME"] = str(java.parents[1])
            kotlin, = [block for block in blocks("kotlin") if "\n// expect: " in block]
            source, expected = kotlin.rsplit("\n// expect: ", 1)
            (work / "Counter.kt").write_text(source, encoding="utf-8")
            run([str(args.kotlinc.resolve()), "Counter.kt", "-include-runtime", "-d", "counter.jar"], work, env)
            assert run([str(java), "-jar", "counter.jar"], work, env) == expected
            print("P.5.2 Kotlin counter state passed")
        if args.dart:
            dart, = blocks("dart")
            source, expected = dart.rsplit("\n// expect: ", 1)
            (work / "operation.dart").write_text(source, encoding="utf-8")
            assert run([str(args.dart.resolve()), "operation.dart"], work, env) == expected
            print("P.5.2 Dart operation payload passed")
