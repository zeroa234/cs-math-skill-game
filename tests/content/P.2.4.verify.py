"""Verify git, pdb, semver, make/dependency, and profiling calculations in data/content/P.2.4.yaml."""
import io
import os
import pdb
import re
import shutil
import subprocess
import tempfile
from pathlib import Path


def check_git_workflows():
    if not shutil.which("git"):
        return
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        env = {
            **os.environ,
            "GIT_AUTHOR_NAME": "Test",
            "GIT_AUTHOR_EMAIL": "t@example.com",
            "GIT_COMMITTER_NAME": "Test",
            "GIT_COMMITTER_EMAIL": "t@example.com",
        }
        run = lambda *args: subprocess.run(
            ["git", *args], cwd=d, env=env, check=True, capture_output=True, text=True
        ).stdout.strip()

        run("init", "-b", "main")
        (d / "a.txt").write_text("v1\n", encoding="utf-8")
        run("add", "a.txt")
        # Modify working tree AFTER git add -> commit still snapshots staged v1!
        (d / "a.txt").write_text("v2-working\n", encoding="utf-8")
        run("commit", "-m", "c1")
        assert run("show", "HEAD:a.txt") == "v1"

        # Reset working file and test amend changes commit SHA
        (d / "a.txt").write_text("v2\n", encoding="utf-8")
        run("add", "a.txt")
        old_sha = run("rev-parse", "HEAD")
        run("commit", "--amend", "-m", "c1-amended")
        new_sha = run("rev-parse", "HEAD")
        assert old_sha != new_sha

        # Branch + merge conflict + revert
        run("switch", "-c", "feature")
        (d / "a.txt").write_text("from-feature\n", encoding="utf-8")
        run("commit", "-am", "feat")
        run("switch", "main")
        (d / "a.txt").write_text("from-main\n", encoding="utf-8")
        run("commit", "-am", "main-diverge")
        p = subprocess.run(["git", "merge", "feature"], cwd=d, env=env, capture_output=True, text=True)
        assert p.returncode != 0
        conflict_text = (d / "a.txt").read_text(encoding="utf-8")
        assert "<<<<<<<" in conflict_text and "=======" in conflict_text and ">>>>>>>" in conflict_text
        run("merge", "--abort")

        # Revert adds a new inverse commit instead of deleting history
        cnt_before = int(run("rev-list", "--count", "HEAD"))
        run("revert", "--no-edit", "HEAD")
        cnt_after = int(run("rev-list", "--count", "HEAD"))
        assert cnt_after == cnt_before + 1
        assert (d / "a.txt").read_text(encoding="utf-8") == "v2\n"


def check_pdb_and_off_by_one():
    # Buggy off-by-one loop: range(len(xs) - 1) drops last element
    def sum_buggy(xs):
        total = 0
        for i in range(len(xs) - 1):
            total += xs[i]
        return total

    def sum_fixed(xs):
        total = 0
        for i in range(len(xs)):
            total += xs[i]
        return total

    assert sum_buggy([2, 5, 7]) == 7
    assert sum_fixed([2, 5, 7]) == 14
    assert sum_buggy([4, 6, 8]) == 10
    assert sum_fixed([4, 6, 8]) == 18

    # Trace range(5)[-1] == 4
    assert list(range(5))[-1] == 4


def semver_caret_matches(ver: tuple[int, int, int], spec: tuple[int, int, int]) -> bool:
    maj, min_, pat = spec
    if maj > 0:
        upper = (maj + 1, 0, 0)
    elif min_ > 0:
        upper = (0, min_ + 1, 0)
    else:
        upper = (0, 0, pat + 1)
    return spec <= ver < upper


def check_semver_and_make():
    # ^1.2.3 means >= 1.2.3 and < 2.0.0
    assert not semver_caret_matches((1, 2, 2), (1, 2, 3))
    assert semver_caret_matches((1, 2, 3), (1, 2, 3))
    assert semver_caret_matches((1, 2, 5), (1, 2, 3))
    assert semver_caret_matches((1, 9, 9), (1, 2, 3))
    assert not semver_caret_matches((2, 0, 0), (1, 2, 3))

    # ^0.2.3 means >= 0.2.3 and < 0.3.0
    assert semver_caret_matches((0, 2, 9), (0, 2, 3))
    assert not semver_caret_matches((0, 3, 0), (0, 2, 3))

    # Incremental make rebuild count:
    # Target app depends on main.o, util.o; main.o depends on main.c, util.h; util.o depends on util.c, util.h
    deps = {
        "main.o": {"main.c", "util.h"},
        "util.o": {"util.c", "util.h"},
        "app": {"main.o", "util.o"},
    }
    def affected(changed_file):
        rebuilt = set()
        frontier = {changed_file}
        while frontier:
            nxt = set()
            for t, ds in deps.items():
                if ds & frontier and t not in rebuilt:
                    rebuilt.add(t)
                    nxt.add(t)
            frontier = nxt
        return rebuilt

    assert affected("util.c") == {"util.o", "app"}  # only util.o recompiled + app relinked
    assert affected("util.h") == {"main.o", "util.o", "app"}  # both .o recompiled + app relinked


def check_profiling_and_coverage():
    # Profiling example: parse 80 ms + query 20 ms = 100 ms; query 2x faster -> 80 + 10 = 90 ms (only 10% saved)
    # parse 2x faster -> 40 + 20 = 60 ms (40% saved)
    assert 80 + 20 == 100
    assert 80 + 20 / 2 == 90
    assert 80 / 2 + 20 == 60

    # Branch / line coverage example: 18 of 24 lines covered = 75%
    assert 18 / 24 == 0.75


def main():
    check_git_workflows()
    check_pdb_and_off_by_one()
    check_semver_and_make()
    check_profiling_and_coverage()
    print("P.2.4 verify: all git, pdb, semver, make, and profiling checks passed.")


if __name__ == "__main__":
    main()
