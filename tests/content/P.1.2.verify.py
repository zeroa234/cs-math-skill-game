"""Verify P.1.2 Java OOP examples, invariant checks, generics and checked-exception rejections using JDK 21."""

from argparse import ArgumentParser
from pathlib import Path
import re
import shutil
import subprocess
from tempfile import TemporaryDirectory
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "data/content/P.1.2.yaml"
DEFAULT_JDK_CANDIDATES = [
    Path(r"D:\java\jdk-21.0.12.1+1"),
]


def resolve_jdk(explicit_jdk):
    if explicit_jdk:
        return explicit_jdk.resolve()
    if shutil.which("javac") and shutil.which("java"):
        return None
    for cand in DEFAULT_JDK_CANDIDATES:
        if (cand / "bin/javac.exe").exists() or (cand / "bin/javac").exists():
            return cand.resolve()
    raise FileNotFoundError("JDK 21 not found on PATH or default D:\\java location; pass --jdk")


def extract_java_blocks(section_text):
    pattern = r"^ +```java\n(.*?)^ +```$"
    return [dedent(b).strip() for b in re.findall(pattern, section_text, re.MULTILINE | re.DOTALL)]


def run_cmd(args, cwd, *, check=True, stdin_text=None):
    res = subprocess.run(
        args,
        cwd=cwd,
        input=stdin_text,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding="utf-8",
        errors="replace",
        timeout=30,
    )
    if check and res.returncode != 0:
        raise AssertionError(f"Command failed {args}:\n{res.stdout}")
    return res


def compile_java(javac, cwd, src, *, check=True):
    (cwd / "Main.java").write_text(src, encoding="utf-8")
    return run_cmd([javac, "-encoding", "UTF-8", "-XDrawDiagnostics", "Main.java"], cwd, check=check)


def split_imports(src):
    imports = re.findall(r"^import .+;$", src, re.MULTILINE)
    body = re.sub(r"^import .+;\n?", "", src, flags=re.MULTILINE)
    return imports, body


def verify_java_pack(text, tmpdir, javac, java):
    samples = {}
    verified = 0
    jvm = [java, "-Dfile.encoding=UTF-8", f"-Djava.io.tmpdir={tmpdir}", "Main"]

    for section in re.split(r"^  - id: ", text, flags=re.MULTILINE)[1:]:
        lesson_id = section.splitlines()[0].strip()
        blocks = extract_java_blocks(section)
        if blocks:
            samples[lesson_id] = blocks[0].split("\n// expect:")[0]
        for idx, example in enumerate(blocks):
            if "\n// expect: " not in example:
                continue
            code, expected = example.rsplit("\n// expect: ", 1)
            stdin_val = None
            if "\n// input: " in code:
                code, stdin_val = code.rsplit("\n// input: ", 1)
                stdin_val += "\n"
            if "class Main" not in code:
                imports, body = split_imports(code)
                extra_members = ""
                if lesson_id == "java-flow" and idx == 0:
                    extra_members, call = body.rsplit("\nSystem.out.", 1)
                    if not extra_members.lstrip().startswith("static "):
                        extra_members = "static " + extra_members
                    body = "System.out." + call
                code = "\n".join(imports) + f"""
class Main {{
    {extra_members}
    public static void main(String[] args) throws Exception {{
        {body}
    }}
}}
"""
            compile_java(javac, tmpdir, code)
            actual = run_cmd(jvm, tmpdir, stdin_text=stdin_val).stdout.strip().splitlines()
            assert actual == expected.split("|"), (lesson_id, idx, actual, expected)
            if lesson_id == "java-start" and idx == 0:
                assert run_cmd(jvm, tmpdir, stdin_text="9\n").stdout.strip() == "18"
            verified += 1

    # 1. Comprehensive exercise BankAccount invariant assertions
    assert "account" in samples, "account lesson java block missing"
    acct_src = samples["account"].split("\nBankAccount ", 1)[0]
    compile_java(
        javac,
        tmpdir,
        """
class Main {
    static void reject(Class<? extends Exception> cls, Runnable fn) {
        try { fn.run(); }
        catch (Exception e) {
            if (cls.isInstance(e)) return;
            throw e;
        }
        throw new AssertionError("expected " + cls.getName());
    }
    public static void main(String[] args) {
""" + acct_src + """
        BankAccount acc = new BankAccount(12);
        reject(IllegalArgumentException.class, () -> new BankAccount(-1));
        reject(IllegalArgumentException.class, () -> acc.deposit(0));
        reject(IllegalArgumentException.class, () -> acc.deposit(-5));
        reject(IllegalArgumentException.class, () -> acc.withdraw(0));
        reject(IllegalArgumentException.class, () -> acc.withdraw(-2));
        reject(IllegalStateException.class, () -> acc.withdraw(13));
        reject(ArithmeticException.class, () -> acc.deposit(Long.MAX_VALUE));
        acc.withdraw(12);
        if (acc.balance() != 0) throw new AssertionError("balance mismatch");
    }
}
""",
    )
    run_cmd(jvm, tmpdir)

    # 2. Generic Stack<T> compile-time type rejection
    assert "generic-stack" in samples, "generic-stack lesson java block missing"
    imp, stack_src = split_imports(samples["generic-stack"].split("\nStack<String>", 1)[0])
    stack_ok = "\n".join(imp) + f"""
class Main {{
    public static void main(String[] args) {{
        {stack_src}
        Stack<String> s = new Stack<>();
        s.push("A");
        if (!s.pop().equals("A") || !s.isEmpty()) throw new AssertionError();
        try {{ s.pop(); }} catch (IndexOutOfBoundsException ok) {{ return; }}
        throw new AssertionError("empty pop should fail");
    }}
}}
"""
    compile_java(javac, tmpdir, stack_ok)
    run_cmd(jvm, tmpdir)
    stack_bad = compile_java(javac, tmpdir, stack_ok.replace('s.push("A");', "s.push(3);"), check=False)
    assert stack_bad.returncode != 0 and "compiler.err.cant.apply.symbol" in stack_bad.stdout, stack_bad.stdout

    # 3. Checked exception compile-time enforcement
    assert "exceptions" in samples, "exceptions lesson java block missing"
    exc_src = samples["exceptions"].split("\ntry {", 1)[0]
    exc_bad = compile_java(
        javac,
        tmpdir,
        f"""
class Main {{
    public static void main(String[] args) {{
        {exc_src}
        wallet.withdraw(7);
    }}
}}
""",
        check=False,
    )
    assert exc_bad.returncode != 0 and "compiler.err.unreported.exception" in exc_bad.stdout, exc_bad.stdout

    assert verified >= 10, f"expected >=10 verified java snippets, got {verified}"
    print(f"P.1.2 verify: {verified} real JDK 21 snippets, BankAccount invariants, Stack<T> & checked-exception compiler checks passed.")


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--jdk", type=Path, help="Optional JDK 21 home directory")
    args = parser.parse_args()
    jdk = resolve_jdk(args.jdk)
    javac = str(jdk / "bin/javac") if jdk else "javac"
    java = str(jdk / "bin/java") if jdk else "java"
    work = ROOT / "temp"
    work.mkdir(exist_ok=True)
    text = PACK.read_text(encoding="utf-8")
    with TemporaryDirectory(dir=work, prefix="p12-verify-") as tmp:
        verify_java_pack(text, Path(tmp), javac, java)


if __name__ == "__main__":
    main()
