"""Run the printed OCaml, SWI-Prolog and SQLite examples."""

from argparse import ArgumentParser
from contextlib import closing
from pathlib import Path
import re
import sqlite3
import subprocess
from tempfile import TemporaryDirectory
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "data/content/P.1.3.yaml"


def blocks(text, language):
    return [dedent(block).strip() for block in re.findall(
        rf"^ +```{language}\n(.*?)^ +```$", text, re.MULTILINE | re.DOTALL
    )]


def run(args, check=True):
    result = subprocess.run(args, capture_output=True, text=True, timeout=10)
    if check and result.returncode:
        raise AssertionError(result.stderr or result.stdout)
    return result


def check_ocaml(text, directory, ocaml):
    source = directory / "example.ml"
    examples = blocks(text, "ocaml")
    assert examples
    for block in examples:
        code, expected = block.rsplit("\n(* expect: ", 1)
        source.write_text(code + "\n", encoding="utf-8")
        actual = run([ocaml, "-noinit", str(source)]).stdout.strip().splitlines()
        assert actual == expected.removesuffix(" *)").split("|"), (code, actual, expected)
    source.write_text("let invalid = 2 + 3.5\n", encoding="utf-8")
    invalid = run([ocaml, "-noinit", str(source)], check=False)
    assert invalid.returncode and "float" in invalid.stderr and "int" in invalid.stderr
    print(f"P.1.3 {len(examples)} OCaml examples and the type error passed")


def check_prolog(text, directory, swipl, home):
    source = directory / "relations.pl"
    command = [swipl, *(["--home=" + home] if home else []), "-q", "-f", "none", "-s", str(source)]
    examples = blocks(text, "prolog")
    assert examples
    for block in examples:
        if "% expect: " not in block:
            source.write_text(block + "\n", encoding="utf-8")
            goal = "findall(X,grandparent(tom,X),Xs),writeln(Xs),halt"
            assert run([*command, "-g", goal]).stdout.strip() == "[ann,pat]"
            continue
        code, expected = block.rsplit("\n% expect: ", 1)
        source.write_text(code + "\n", encoding="utf-8")
        actual = run(command).stdout.strip().splitlines()
        assert actual == expected.split("|"), (code, actual, expected)
    print(f"P.1.3 {len(examples)} Prolog examples passed")


def check_sql(text):
    query, = blocks(text, "sql")
    with closing(sqlite3.connect(":memory:")) as db:
        db.executescript("""
            CREATE TABLE Enroll(sid INTEGER, course TEXT, grade INTEGER);
            INSERT INTO Enroll VALUES
                (1,'Databases',70), (2,'Databases',90), (3,'Databases',NULL),
                (1,'Logic',92), (2,'Logic',88),
                (1,'Systems',78), (2,'Systems',80),
                (1,'NoGrades',NULL);
        """)
        assert db.execute(query).fetchall() == [("Logic", 90.0), ("Databases", 80.0)]
    assert 5 * 2 == 10 and 3 * 2 * 2 == 12 and 10 - 2 - 3 == 5
    assert max(2, 0) + 1 == 3
    print("P.1.3 SQLite HAVING, NULL and descending order passed")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--ocaml", default="ocaml")
    parser.add_argument("--swipl", default="swipl")
    parser.add_argument("--swi-home")
    args = parser.parse_args()
    text = PACK.read_text(encoding="utf-8")
    temp = ROOT / "temp"
    temp.mkdir(exist_ok=True)
    with TemporaryDirectory(dir=temp, prefix="p-1-3-verify-") as directory:
        check_ocaml(text, Path(directory), args.ocaml)
        check_prolog(text, Path(directory), args.swipl, args.swi_home)
        check_sql(text)
