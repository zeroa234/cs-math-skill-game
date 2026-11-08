"""Check the P.2.4 examples with real Git, pdb, GNU Make/GCC, Bash and npm."""

import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[2]
TEMP = ROOT / "temp"
NPM = "npm.cmd" if os.name == "nt" else "npm"


def run(*args, cwd, env=None, stdin=None, status=0):
    result = subprocess.run(
        args, cwd=cwd, env=env, input=stdin, capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    )
    assert result.returncode == status, (args, result.returncode, result.stdout, result.stderr)
    return result.stdout.strip()


def code_examples():
    output = run("node", "--input-type=module", "-e", """
      import fs from 'node:fs';
      import {load} from 'js-yaml';
      const pack = load(fs.readFileSync('data/content/P.2.4.yaml', 'utf8'));
      const ids = ['breakpoint', 'make-rules', 'build-graph'];
      console.log(JSON.stringify(ids.map(id => {
        const lesson = pack.lessons.find(l => l.id === id);
        return lesson.flow.find(s => s.card?.body.includes('```')).card.body;
      })));
    """, cwd=ROOT)
    return [re.search(r"```\w+\n([\s\S]+?)```", body)[1] for body in json.loads(output)]


def verify_git(work):
    work.mkdir()
    env = dict(os.environ, GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=str(work / "no-gitconfig"))

    def git(*args, **kwargs):
        return run("git", "-c", "user.name=Lesson", "-c", "user.email=lesson@example.invalid",
                   *args, cwd=work, env=env, **kwargs)

    git("init", "-b", "main")
    hours = work / "hours.txt"
    hours.write_text("closed\n", encoding="utf-8")
    git("add", hours.name)
    hours.write_text("unfinished\n", encoding="utf-8")
    git("commit", "-m", "Initial hours")
    assert git("show", "HEAD:hours.txt") == "closed"
    hours.write_text("closed\n", encoding="utf-8")
    git("switch", "-c", "feature")
    hours.write_text("morning\n", encoding="utf-8")
    git("add", hours.name)
    git("commit", "-m", "Morning")
    (work / "help.txt").write_text("Help\n", encoding="utf-8")
    git("add", "help.txt")
    git("commit", "-m", "Clarify help")
    original = git("rev-parse", "HEAD")
    git("switch", "main")
    assert git("rev-parse", "HEAD") != original
    hours.write_text("afternoon\n", encoding="utf-8")
    git("commit", "-am", "Afternoon")
    git("merge", "feature", status=1)
    assert "<<<<<<<" in hours.read_text(encoding="utf-8")
    hours.write_text("all day\n", encoding="utf-8")
    git("add", hours.name)
    git("commit", "--no-edit")
    assert len(git("show", "-s", "--format=%P", "HEAD").split()) == 2

    git("switch", "-c", "scratch")
    hours.write_text("wrong\n", encoding="utf-8")
    git("commit", "-am", "Wrong")
    wrong = git("rev-parse", "HEAD")
    git("commit", "--amend", "-m", "Still wrong")
    assert git("rev-parse", "HEAD") != wrong
    git("reset", "--soft", "HEAD~1")
    assert git("show", ":hours.txt") == "wrong"
    git("commit", "-m", "Wrong")
    git("revert", "--no-edit", "HEAD")
    assert git("show", "HEAD:hours.txt") == "all day"

    git("branch", "behind", "main")
    git("switch", "behind")
    git("merge", "scratch")
    assert git("rev-parse", "behind") == git("rev-parse", "scratch")


def verify_pdb(work, source):
    path = work / "sum_items.py"
    path.write_text(source, encoding="utf-8")
    assert run(sys.executable, str(path), cwd=work) == "7"
    debug = run(sys.executable, "-m", "pdb", str(path), cwd=work,
                stdin="b 4, i == len(xs) - 1\nc\np i\np len(xs)\nn\nq\n")
    assert "(4)<module>()" in debug and "(Pdb) 2" in debug and "(Pdb) 3" in debug
    assert "-> print(total)" in debug
    fixed = source.replace("len(xs) - 1", "len(xs)")
    path.write_text(fixed, encoding="utf-8")
    assert run(sys.executable, str(path), cwd=work) == "14"
    path.write_text(fixed.replace("[2, 5, 7]", "[4, 6, 8]"), encoding="utf-8")
    assert run(sys.executable, str(path), cwd=work) == "18"
    assert sum((80, 20)) == 100 and 80 // 2 + 20 == 60 and 60 // 2 + 30 == 60
    assert list(range(5))[-1] == 4


def linux(*args, cwd):
    if os.name != "nt":
        return run(*args, cwd=cwd)
    drive, suffix = os.path.splitdrive(cwd.as_posix())
    directory = "/mnt/" + drive[0].lower() + suffix
    return run("wsl.exe", "--cd", directory, "-e", *args, cwd=cwd)


def verify_make(work, rules):
    work.mkdir()
    (work / "Makefile").write_text(rules, encoding="utf-8", newline="\n")
    (work / "main.c").write_text('#include "util.h"\nint main(void) { return check(); }\n', encoding="utf-8")
    util = work / "util.c"
    util.write_text('#include "util.h"\nint check(void) { return 0; }\n', encoding="utf-8")
    header = work / "util.h"
    header.write_text("int check(void);\n", encoding="utf-8")
    initial = linux("make", "-j2", cwd=work)
    assert "main.c" in initial and "util.c" in initial and "main.o util.o" in initial
    linux("./app", cwd=work)
    assert "gcc" not in linux("make", cwd=work)

    def age_outputs(seconds):
        for name in ("main.o", "util.o", "app"):
            output = work / name
            t = output.stat().st_mtime + seconds
            os.utime(output, (t, t))

    # Make timestamp differences explicit on filesystems with different resolutions.
    for path in (work / "main.c", util, header):
        os.utime(path, (1_600_000_000, 1_600_000_000))
    age_outputs(-4)
    util.touch()
    rebuilt = linux("make", cwd=work)
    assert "util.c" in rebuilt and "main.c" not in rebuilt and "main.o util.o" in rebuilt
    header.touch()
    rebuilt = linux("make", cwd=work)
    assert "util.c" in rebuilt and "main.c" in rebuilt and "main.o util.o" in rebuilt
    linux("./app", cwd=work)


def verify_shell_and_npm(work):
    (work / "tasks.txt").write_text("ready one\nwaiting\nready two\n", encoding="utf-8", newline="\n")
    linux("bash", "-c", "grep ready tasks.txt | wc -l > count.txt", cwd=work)
    assert int((work / "count.txt").read_text()) == 2
    assert linux("bash", "-c", "unset MODE; MODE=test bash -c 'echo \"$MODE\"'; test -z \"$MODE\"", cwd=work) == "test"
    assert linux("bash", "-c", "false && echo unexpected; echo $?", cwd=work) == "1"

    npm_modules = Path(shutil.which("node")).resolve().parent / "node_modules" / "npm" / "node_modules"
    env = dict(os.environ, NODE_PATH=str(npm_modules), npm_config_cache=str(work / "npm-cache"))
    assert run("node", "-e", """
      const s = require('semver');
      console.log(['1.2.2', '1.2.3', '1.2.5', '1.7.0', '2.0.0']
        .map(v => s.satisfies(v, '^1.2.3')).join(','));
    """, cwd=work, env=env) == "false,true,true,true,false"
    dep = work / "dep"
    dep.mkdir()
    (dep / "package.json").write_text('{"name":"lesson-dep","version":"1.2.5"}', encoding="utf-8")
    (work / "package.json").write_text('{"name":"lesson-app","version":"1.0.0","private":true}', encoding="utf-8")
    flags = ("--offline", "--ignore-scripts", "--no-audit", "--no-fund")
    run(NPM, "install", "./dep", *flags, cwd=work, env=env)
    lock = work / "package-lock.json"
    saved = lock.read_bytes()
    run(NPM, "ci", *flags, cwd=work, env=env)
    assert lock.read_bytes() == saved
    installed = json.loads((work / "node_modules/lesson-dep/package.json").read_text())
    assert installed["version"] == "1.2.5"


TEMP.mkdir(exist_ok=True)
with TemporaryDirectory(prefix="p-2-4-", dir=TEMP) as directory:
    work = Path(directory)
    pdb, make, graph = code_examples()
    verify_git(work / "git")
    verify_pdb(work, pdb)
    verify_make(work / "make", make)
    verify_make(work / "graph", graph)
    verify_shell_and_npm(work)
print("P.2.4: Git, pdb, example arithmetic, both Makefiles, Bash and npm verified")
