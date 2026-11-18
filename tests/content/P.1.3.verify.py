"""Verify every OCaml, SWI-Prolog, SQLite, and arithmetic example in data/content/P.1.3.yaml."""

from contextlib import closing
import os
from pathlib import Path
import re
import shutil
import sqlite3
import subprocess
from tempfile import TemporaryDirectory
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "data/content/P.1.3.yaml"
RUNTIME_DIR = ROOT / "temp/p-1-3-runtimes"


def to_wsl_path(p: Path) -> str:
    s = str(p.resolve()).replace("\\", "/")
    if len(s) >= 2 and s[1] == ":":
        return f"/mnt/{s[0].lower()}{s[2:]}"
    return s


def run_tool(linux_cmd: str, timeout: int = 20) -> subprocess.CompletedProcess:
    if os.name == "nt":
        args = ["wsl", "-e", "bash", "-c", linux_cmd]
    else:
        args = ["bash", "-c", linux_cmd]
    return subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)


def run_ocaml(source_path: Path, *, check: bool = True) -> subprocess.CompletedProcess:
    if shutil.which("ocaml") and os.name != "nt":
        cmd = f"ocaml -noinit '{source_path}'"
    else:
        ocaml_local = RUNTIME_DIR / "ocaml-local"
        assert ocaml_local.exists(), f"Missing OCaml runtime at {ocaml_local}"
        cmd = f"'{to_wsl_path(ocaml_local)}' -noinit '{to_wsl_path(source_path)}'"
    res = run_tool(cmd)
    if check and res.returncode != 0:
        raise AssertionError(f"OCaml failed:\n{res.stderr}\n{res.stdout}")
    return res


def run_prolog(source_path: Path, goal: str | None = None, *, check: bool = True) -> subprocess.CompletedProcess:
    goal_flag = f" -g '{goal}'" if goal else ""
    if shutil.which("swipl") and os.name != "nt":
        cmd = f"swipl -q -f none -s '{source_path}'{goal_flag}"
    else:
        unpacked = RUNTIME_DIR / "unpacked/usr"
        swipl_bin = unpacked / "bin/swipl"
        lib_dir = to_wsl_path(unpacked / "lib/x86_64-linux-gnu")
        home_dir = to_wsl_path(unpacked / "lib/swi-prolog")
        cmd = (
            f"LD_LIBRARY_PATH='{lib_dir}' '{to_wsl_path(swipl_bin)}' "
            f"--home='{home_dir}' -q -f none -s '{to_wsl_path(source_path)}'{goal_flag}"
        )
    res = run_tool(cmd)
    if check and res.returncode != 0:
        raise AssertionError(f"SWI-Prolog failed:\n{res.stderr}\n{res.stdout}")
    return res


def extract_fenced(text: str, language: str) -> list[str]:
    return [
        dedent(b).strip()
        for b in re.findall(rf"^ +```{language}\n(.*?)^ +```$", text, re.MULTILINE | re.DOTALL)
    ]


def extract_item_code(text: str, language: str) -> list[str]:
    return [
        dedent(b).strip()
        for b in re.findall(rf"^ +code: \|\n(.*?)\n +lang: {language}$", text, re.MULTILINE | re.DOTALL)
    ]


def verify_ocaml(text: str, tmp: Path) -> None:
    src = tmp / "example.ml"
    fenced = extract_fenced(text, "ocaml")
    item_codes = extract_item_code(text, "ocaml")
    assert len(fenced) == 20, f"Expected 20 fenced OCaml blocks, got {len(fenced)}"
    assert len(item_codes) == 10, f"Expected 10 item OCaml blocks, got {len(item_codes)}"

    # Run each fenced OCaml block and match its exact output
    actual_fenced = []
    for block in fenced:
        src.write_text(block + "\n", encoding="utf-8")
        out = run_ocaml(src).stdout.strip()
        actual_fenced.append(out)

    # Match outputs by unique content markers
    checks = {
        "let area = width * height": "10 5.5",
        "let rec fact n =": "24",
        "let new_list = 1 :: old_list": "2 3",
        "let () = Printf.printf \"%d\\n\" (sum [4; 5; 6])": "15",
        "type counter = { label : string; mutable hits : int }": "15 2",
        "a.(i) <- a.(i) + i": "2 5 8",
        "apply_twice (fun x -> x * 2) 3": "12",
        "let add5 = add 5": "12",
        "my_map (fun x -> x * 2) [1; 3; 5]": "2 6 10",
        "my_filter (fun x -> x >= 60) [55; 60; 75]": "60 75",
        "let right_res = List.fold_right": "5 9",
        "let sum_tail xs = foldl": "60",
        "let total =": "145",
        "let slow = [1; 2; 3]": "true",
        "area (Rect (3.0, 4.0))": "12.0",
        "show_div 10 2": "5 | cannot divide by zero",
        "let s2 = { s1 with score = 95 }": "Lin:88 Lin:95",
        "grade (Some 75)": "Pass Missing",
        "int_of_nat two": "2",
        "depth (mirror sample)": "3 3",
    }
    # Verify actual count & every block containing a marker
    assert len(fenced) >= 13
    for i, block in enumerate(fenced):
        matched = [exp for key, exp in checks.items() if key in block]
        assert len(matched) == 1, f"Block {i} matched {matched}: {block[:60]}"
        assert actual_fenced[i] == matched[0], f"Block {i} expected {matched[0]!r}, got {actual_fenced[i]!r}"

    # Check each of the 9 item `code:` snippets directly
    expected_items = [
        (item_codes[0] + "\nlet () = Printf.printf \"%d\\n\" (fact 4)", "24"),
        (item_codes[1], "25"),
        (item_codes[2], "2 3"),
        (item_codes[3], "17"),
        (item_codes[4] + "\nlet () = Printf.printf \"%d\\n\" a.(2)", "8"),
        (item_codes[5] + "\nlet () = Printf.printf \"%d\\n\" ans", "60"),
        (item_codes[6] + "\nlet () = Printf.printf \"%d\\n\" (s1.score + s2.score)", "183"),
        ("type 'a tree = Leaf | Node of 'a tree * 'a * 'a tree\n"
         "let rec depth = function Leaf -> 0 | Node (l, _, r) -> 1 + max (depth l) (depth r)\n"
         + item_codes[7] + "\nlet () = Printf.printf \"%d\\n\" (depth sample)", "3"),
        (item_codes[8] + "\nlet () = Printf.printf \"%d\\n\" score", "45"),
        (item_codes[9], "27"),
    ]
    # Plus check tree sample + boss pipeline + currying + foldl + pattern matching + option + nat
    pack_evals = [
        ("type 'a tree = Leaf | Node of 'a tree * 'a * 'a tree\n"
         "let rec depth = function Leaf -> 0 | Node (l, _, r) -> 1 + max (depth l) (depth r)\n"
         "let rec mirror = function Leaf -> Leaf | Node (l, v, r) -> Node (mirror r, v, mirror l)\n"
         "let sample = Node (Node (Leaf, 1, Leaf), 2, Node (Leaf, 3, Node (Leaf, 4, Leaf)))\n"
         "let t = Node (Node (Leaf, 1, Leaf), 2, Leaf)\n"
         "let boss_t = Node (Node (Node (Leaf, 1, Leaf), 2, Leaf), 3, Node (Leaf, 4, Leaf))\n"
         "let () = Printf.printf \"%d %b %d\\n\" (depth sample) (mirror t = Node (Leaf, 2, Node (Leaf, 1, Leaf))) (depth boss_t)",
         "3 true 3"),
        ("let score =\n"
         "  [10; 25; 30; 15]\n"
         "  |> List.filter (fun x -> x >= 20)\n"
         "  |> List.map (fun x -> x - 5)\n"
         "  |> List.fold_left ( + ) 0\n"
         "let () = Printf.printf \"%d\\n\" score",
         "45"),
        ("let mul x y = x * y\nlet triple = mul 3\n"
         "let f = function Some (0, y) -> y * 10 | Some (x, y) -> x + y | None -> -1\n"
         "let safe_div a b = if b = 0 then None else Some (a / b)\n"
         "let unwrap_or d = function Some x -> x | None -> d\n"
         "type nat = Zero | Succ of nat\n"
         "let rec int_of_nat = function Zero -> 0 | Succ n -> 1 + int_of_nat n\n"
         "let rec add a b = match a with Zero -> b | Succ n -> Succ (add n b)\n"
         "let () = Printf.printf \"%d %d %d %d\\n\" (triple 8) (f (Some (0, 4)) + f (Some (3, 4))) "
         "(unwrap_or 100 (safe_div 20 0) + unwrap_or 100 (safe_div 20 4)) "
         "(int_of_nat (add (Succ (Succ Zero)) (Succ Zero)))",
         "24 47 105 3"),
        ("let ans = [55; 60; 75] |> List.filter (fun x -> x >= 60) |> List.map (fun x -> x + 5) |> List.fold_left (+) 0\n"
         "let f_pipe = 5 |> (fun x -> x + 2) |> (fun y -> y * 3)\n"
         "let rec foldl f acc = function [] -> acc | x :: xs -> foldl f (f acc x) xs\n"
         "let () = Printf.printf \"%d %d %d\\n\" ans f_pipe (foldl ( * ) 1 [2; 3; 4])",
         "145 21 24"),
    ]
    for code, expected in expected_items + pack_evals:
        src.write_text(code + "\n", encoding="utf-8")
        out = run_ocaml(src).stdout.strip()
        assert out == expected, f"Expected {expected!r}, got {out!r} for:\n{code}"

    # Verify type errors / non-exhaustiveness
    src.write_text("let bad = 2 + 3.5\n", encoding="utf-8")
    bad = run_ocaml(src, check=False)
    assert bad.returncode != 0 and "float" in bad.stderr and "int" in bad.stderr

    src.write_text('let bad_if = if 3 > 2 then 1 else "no"\n', encoding="utf-8")
    bad_if = run_ocaml(src, check=False)
    assert bad_if.returncode != 0 and "string" in bad_if.stderr and "int" in bad_if.stderr

    src.write_text('type light = Red | Yellow | Green\nlet f x = match x with Red -> "stop" | Green -> "go"\n', encoding="utf-8")
    non_exh = run_ocaml(src, check=False)
    assert "not exhaustive" in non_exh.stderr or "Yellow" in non_exh.stderr

    print(f"P.1.3 OCaml: {len(fenced)} fenced blocks + {len(expected_items)} item snippets + {len(pack_evals)} evals + type/exhaustiveness checks passed")


def verify_prolog(text: str, tmp: Path) -> None:
    src = tmp / "prog.pl"
    fenced = extract_fenced(text, "prolog")
    assert len(fenced) == 4, f"Expected 4 Prolog blocks, got {len(fenced)}"

    # Block 0: grandparent/2
    src.write_text(fenced[0] + "\n", encoding="utf-8")
    out0 = run_prolog(src, "findall(Who, grandparent(tom, Who), Ws), writeln(Ws), halt").stdout.strip()
    assert out0 == "[ann,pat]", out0

    # Block 1: ancestor/2
    src.write_text(fenced[1] + "\n", encoding="utf-8")
    out1 = run_prolog(src).stdout.strip()
    assert out1 == "[bob,tom]", out1

    # Block 2: member_of/2
    src.write_text(fenced[2] + "\n", encoding="utf-8")
    out2 = run_prolog(src).stdout.strip().splitlines()
    assert out2 == ["yes", "no"], out2

    # Block 3: dynamic available/1
    src.write_text(fenced[3] + "\n", encoding="utf-8")
    out3 = run_prolog(src).stdout.strip()
    assert out3 == "[room2]", out3

    # Unification checks
    src.write_text("main :- (edge(A, b) = edge(a, B) -> writeln([A, B]) ; writeln(fail)), "
                   "(\\+ (edge(C, C) = edge(a, b)) -> writeln(unify_fail) ; writeln(bad)), "
                   "(book(Title, 2024) = book(ocaml, Year) -> writeln([Title, Year]) ; writeln(fail)), halt.\n"
                   ":- initialization(main).\n", encoding="utf-8")
    out_u = run_prolog(src).stdout.strip().splitlines()
    assert out_u == ["[a,b]", "unify_fail", "[ocaml,2024]"], out_u

    print("P.1.3 SWI-Prolog: 4 fenced blocks + unification checks passed")


def verify_sql(text: str) -> None:
    queries = extract_fenced(text, "sql")
    assert len(queries) == 1
    with closing(sqlite3.connect(":memory:")) as db:
        db.executescript("""
            CREATE TABLE Enroll(sid INTEGER, course TEXT, grade INTEGER);
            INSERT INTO Enroll VALUES
                (1,'Databases',70), (2,'Databases',90), (3,'Databases',NULL),
                (1,'Logic',92), (2,'Logic',88),
                (1,'Systems',78), (2,'Systems',80),
                (1,'NoGrades',NULL);
        """)
        rows = db.execute(queries[0]).fetchall()
        assert rows == [("Logic", 90.0), ("Databases", 80.0)], rows
        db_only = db.execute("SELECT AVG(grade) FROM Enroll WHERE course='Databases'").fetchone()[0]
        assert db_only == 80.0, db_only
    print("P.1.3 SQLite: GROUP BY, HAVING, NULL handling, ORDER BY DESC passed")


def main() -> None:
    text = PACK.read_text(encoding="utf-8")
    temp_root = ROOT / "temp"
    temp_root.mkdir(exist_ok=True)
    with TemporaryDirectory(dir=temp_root, prefix="p-1-3-verify-") as d:
        tmp = Path(d)
        verify_ocaml(text, tmp)
        verify_prolog(text, tmp)
        verify_sql(text)


if __name__ == "__main__":
    main()
