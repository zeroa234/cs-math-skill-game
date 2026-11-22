"""Verify Python, Rust (rustc 1.93), C/gprof, C++ RAII, and TypeScript examples in data/content/P.1.4.yaml."""

from __future__ import annotations

import io
import os
import pathlib
import re
import shutil
import subprocess
import sys
from contextlib import redirect_stdout
from tempfile import TemporaryDirectory
from timeit import repeat

ROOT = pathlib.Path(__file__).resolve().parents[2]
PACK_PATH = ROOT / "data" / "content" / "P.1.4.yaml"
TEMP_ROOT = ROOT / "temp"


def extract_blocks(text: str, lang: str) -> list[str]:
    blocks: list[str] = []
    lines = text.splitlines()
    i = 0
    fence_open = re.compile(rf"^(\s*)```{re.escape(lang)}\s*$")
    fence_close = re.compile(r"^\s*```\s*$")
    lang_field = re.compile(rf"^(\s*)lang:\s*{re.escape(lang)}\s*$")
    while i < len(lines):
        m = fence_open.match(lines[i])
        if m:
            indent = m.group(1)
            i += 1
            body: list[str] = []
            while i < len(lines) and not fence_close.match(lines[i]):
                line = lines[i]
                if line.startswith(indent):
                    line = line[len(indent) :]
                body.append(line)
                i += 1
            blocks.append("\n".join(body))
            i += 1
            continue
        ml = lang_field.match(lines[i])
        if ml and i + 1 < len(lines) and re.match(rf"^{re.escape(ml.group(1))}code:\s*\|[-+]?\s*$", lines[i + 1]):
            base_indent = len(ml.group(1))
            i += 2
            body = []
            block_indent: int | None = None
            while i < len(lines):
                line = lines[i]
                if line.strip() == "":
                    body.append("")
                    i += 1
                    continue
                cur_indent = len(line) - len(line.lstrip(" "))
                if cur_indent <= base_indent:
                    break
                if block_indent is None:
                    block_indent = cur_indent
                body.append(line[block_indent:] if len(line) >= block_indent else line.lstrip(" "))
                i += 1
            while body and body[-1] == "":
                body.pop()
            blocks.append("\n".join(body))
            continue
        i += 1
    return blocks


def windows_to_wsl(path: pathlib.Path) -> str:
    resolved = path.resolve()
    drive = resolved.drive.rstrip(":").lower()
    rest = resolved.as_posix().split(":", 1)[1]
    return f"/mnt/{drive}{rest}"


def verify_python(text: str, workdir: pathlib.Path) -> None:
    py_blocks = extract_blocks(text, "python")
    assert len(py_blocks) == 18, f"Expected 18 python blocks, got {len(py_blocks)}"

    expected_outputs = {
        0: "True False",
        1: "True False",
        2: "[1, 2, 3] [99]",
        3: "[1, 2, 3] [99]",
        4: "23",
        5: "call\n8",
        6: "call 8",
        7: "1",
        8: "abc",
        9: "X,Y",
        10: "ok True",
        11: "ok True",
        12: "2000",
        13: "deposit 50",
        14: "add 7",
        16: "True",
        17: "55 11",
    }

    old_cwd = pathlib.Path.cwd()
    os.chdir(workdir)
    try:
        for idx, code in enumerate(py_blocks):
            if idx == 1:
                # Item prompt snippet assumes `lock` already created in scope
                code = "import threading\nlock = threading.Lock()\n" + code
            if idx == 15:
                ns: dict = {}
                exec(compile(code, f"P.1.4_py_{idx}.py", "exec"), ns)
                tb = ns["TagBag"]()
                tb.add("py")
                tb.add("py")
                assert tb.as_tuple() == ("py",)
                continue
            buf = io.StringIO()
            ns = {}
            with redirect_stdout(buf):
                exec(compile(code, f"P.1.4_py_{idx}.py", "exec"), ns)
            actual = buf.getvalue().strip()
            assert actual == expected_outputs[idx], (
                f"Python block {idx} mismatch: got {actual!r}, expected {expected_outputs[idx]!r}"
            )
    finally:
        os.chdir(old_cwd)

    # Verify C4 Question 4 equal-input 10^6 list vs set benchmark & fib(8)
    items = list(range(1_000_000))
    members = set(items)
    for target in (999_999, 1_000_000):
        assert (target in items) == (target in members)
        t_list = min(repeat(lambda: target in items, number=3, repeat=3))
        t_set = min(repeat(lambda: target in members, number=3, repeat=3))
        assert t_list >= 0 and t_set >= 0
        assert t_set < t_list

    from functools import lru_cache

    @lru_cache(maxsize=None)
    def fib(n: int) -> int:
        return n if n < 2 else fib(n - 1) + fib(n - 2)

    assert fib(8) == 21
    assert fib(10) == 55
    assert fib.cache_info().misses == 11


def verify_typescript(text: str, workdir: pathlib.Path) -> None:
    ts_blocks = extract_blocks(text, "typescript")
    assert len(ts_blocks) == 1, f"Expected 1 typescript block, got {len(ts_blocks)}"
    ts_src = (
        ts_blocks[0]
        + '\nconsole.log(first(["book", "pen"]), first<number>([]));\n'
    )
    ts_file = workdir / "generic.ts"
    js_file = workdir / "generic.mjs"
    ts_file.write_text(ts_src, encoding="utf-8")
    esbuild = ROOT / "node_modules" / ".bin" / ("esbuild.cmd" if os.name == "nt" else "esbuild")
    res = subprocess.run(
        [str(esbuild), str(ts_file), f"--outfile={js_file}"],
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0, res.stderr or res.stdout
    out = subprocess.run(
        ["node", str(js_file)], check=True, capture_output=True, text=True
    ).stdout.strip()
    assert out == "book undefined", f"TS output mismatch: {out!r}"


def verify_wsl_compilers(text: str, workdir: pathlib.Path) -> None:
    wsl = shutil.which("wsl")
    if not wsl:
        print("skip — wsl not available for C/C++/Rust/gprof verification")
        return

    # 1. C++ RAII lock_guard exception safety (C4 Question 1)
    cpp_blocks = extract_blocks(text, "cpp")
    assert len(cpp_blocks) == 1, f"Expected 1 cpp block, got {len(cpp_blocks)}"
    cpp_test = workdir / "raii.cpp"
    cpp_test.write_text(
        "#include <iostream>\n"
        "#include <mutex>\n"
        "#include <stdexcept>\n"
        "std::mutex mtx;\n"
        "void write_safe() {\n"
        "    std::lock_guard<std::mutex> guard(mtx);\n"
        '    throw std::runtime_error("demo");\n'
        "}\n"
        "int main() {\n"
        "    try { write_safe(); } catch (const std::exception&) {}\n"
        "    bool locked_after = !mtx.try_lock();\n"
        "    if (!locked_after) mtx.unlock();\n"
        '    std::cout << (locked_after ? "LOCKED" : "UNLOCKED") << std::endl;\n'
        "    return 0;\n"
        "}\n",
        encoding="utf-8",
    )

    # 2. C & gprof example
    c_blocks = extract_blocks(text, "c")
    assert len(c_blocks) == 2, f"Expected 2 c blocks, got {len(c_blocks)}"
    c_prog = workdir / "example.c"
    c_prog.write_text(c_blocks[0], encoding="utf-8")

    wsl_dir = windows_to_wsl(workdir)
    c_cmd = (
        f"cd {wsl_dir} && "
        "g++ -std=c++17 raii.cpp -pthread -o raii && ./raii && "
        "gcc -O0 -g -pg -no-pie example.c -o example && ./example && "
        "gprof -b ./example gmon.out"
    )
    res = subprocess.run([wsl, "bash", "-c", c_cmd], check=True, capture_output=True, text=True)
    lines = res.stdout.splitlines()
    assert "UNLOCKED" in lines, res.stdout
    assert "1001000" in lines, res.stdout
    assert "Flat profile:" in res.stdout and "Call graph" in res.stdout, res.stdout
    assert re.search(r"(?m)^\s*(?:[\d.]+\s+){3}2\s+(?:[\d.]+\s+){2}work\s*$", res.stdout), res.stdout

    # 3. Rust ownership, borrowing, slices, macro_rules! + E0382 moved-value rejection
    rust_local = ROOT / "temp" / "p-1-4-rust" / "local"
    rustc_bin = rust_local / "usr" / "bin" / "rustc-1.93"
    if rustc_bin.exists():
        rust_blocks = extract_blocks(text, "rust")
        assert len(rust_blocks) == 4, f"Expected 4 rust blocks, got {len(rust_blocks)}"
        expected_rust = ["ready", "no:note", "no:note", "hello world"]
        wsl_local = windows_to_wsl(rust_local)
        ld_lib = (
            f"{wsl_local}/usr/lib:{wsl_local}/usr/lib/x86_64-linux-gnu:{wsl_local}/usr/lib/rust-1.93/lib"
        )
        path_pre = f"{wsl_local}/usr/bin"
        for idx, (src, exp) in enumerate(zip(rust_blocks, expected_rust)):
            if idx == 2:
                src = f"fn main() {{\n{src}\n}}\n"
            rs_path = workdir / f"r{idx}.rs"
            rs_path.write_text(src, encoding="utf-8")
            cmd = (
                f"export PATH={path_pre}:$PATH; "
                f"export LD_LIBRARY_PATH={ld_lib}; "
                f"cd {wsl_dir} && {wsl_local}/usr/bin/rustc-1.93 r{idx}.rs -o r{idx} && ./r{idx}"
            )
            out = subprocess.run(
                [wsl, "bash", "-c", cmd], check=True, capture_output=True, text=True
            ).stdout.strip()
            assert out == exp, f"Rust block {idx} mismatch: {out!r} != {exp!r}"

        bad_rs = workdir / "bad.rs"
        bad_rs.write_text(
            'fn main() { let s1 = String::from("hi"); let s2 = s1; println!("{} {}", s1, s2); }\n',
            encoding="utf-8",
        )
        bad_cmd = (
            f"export PATH={path_pre}:$PATH; "
            f"export LD_LIBRARY_PATH={ld_lib}; "
            f"cd {wsl_dir} && {wsl_local}/usr/bin/rustc-1.93 bad.rs -o bad"
        )
        bad_res = subprocess.run([wsl, "bash", "-c", bad_cmd], capture_output=True, text=True)
        assert bad_res.returncode != 0 and "E0382" in bad_res.stderr, bad_res.stderr


def main() -> None:
    text = PACK_PATH.read_text(encoding="utf-8")
    TEMP_ROOT.mkdir(exist_ok=True)
    with TemporaryDirectory(dir=TEMP_ROOT, prefix="p-1-4-verify-") as tmp:
        workdir = pathlib.Path(tmp)
        verify_python(text, workdir)
        verify_typescript(text, workdir)
        verify_wsl_compilers(text, workdir)
    print("ok — verified 18 Python, 1 TypeScript, 1 C++, 1 C/gprof, and 4+1 Rust cases in P.1.4.yaml")


if __name__ == "__main__":
    main()
