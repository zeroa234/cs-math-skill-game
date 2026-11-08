"""Compile and run the Java snippets and optionally build the lesson's Maven project."""

from argparse import ArgumentParser
import os
from pathlib import Path
import re
import subprocess
from tempfile import TemporaryDirectory
from textwrap import dedent
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "data/content/P.1.2.yaml"


def blocks(text, language):
    pattern = rf"^ +```{language}\n(.*?)^ +```$"
    return [dedent(block).strip() for block in re.findall(pattern, text, re.MULTILINE | re.DOTALL)]


def run(args, directory, *, check=True, input=None, env=None, timeout=30):
    result = subprocess.run(
        args, cwd=directory, input=input, env=env, timeout=timeout,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8",
    )
    if check and result.returncode:
        raise AssertionError(result.stdout)
    return result


def compile_source(javac, directory, source, *, check=True):
    (directory / "Main.java").write_text(source, encoding="utf-8")
    return run([javac, "-encoding", "UTF-8", "-XDrawDiagnostics", "Main.java"], directory, check=check)


def split_imports(source):
    imports = re.findall(r"^import .+;$", source, re.MULTILINE)
    return imports, re.sub(r"^import .+;\n", "", source, flags=re.MULTILINE)


def check_java(text, directory, javac, java):
    samples = {}
    jvm = [java, "-Dfile.encoding=UTF-8", f"-Djava.io.tmpdir={directory}", "Main"]
    verified = 0
    for section in re.split(r"^  - id: ", text, flags=re.MULTILINE)[1:]:
        lesson = section.splitlines()[0]
        examples = blocks(section, "java")
        if examples:
            samples[lesson] = examples[0].split("\n// expect:")[0]
        for index, example in enumerate(examples):
            source, expected = example.rsplit("\n// expect: ", 1)
            example_input = None
            if "\n// input: " in source:
                source, example_input = source.rsplit("\n// input: ", 1)
                example_input += "\n"
            if lesson != "java-start":
                imports, statements = split_imports(source)
                members = ""
                if lesson == "java-flow" and index == 0:
                    members, print_call = statements.rsplit("\nSystem.out.", 1)
                    members = "static " + members
                    statements = "System.out." + print_call
                source = "\n".join(imports) + f"""
                    class Main {{
                        {members}
                        public static void main(String[] args) throws Exception {{
                            {statements}
                        }}
                    }}
                """
            compile_source(javac, directory, source)
            actual = run(jvm, directory, input=example_input).stdout.strip().splitlines()
            assert actual == expected.split("|"), (lesson, index, actual, expected)
            if lesson == "java-start":
                assert run(jvm, directory, input="9\n").stdout.strip() == "18"
            verified += 1

    source = samples["account"].split("\nBankAccount account =", 1)[0]
    compile_source(javac, directory, """
        class Main {
            static void reject(Class<? extends Exception> type, Runnable operation) {
                try { operation.run(); }
                catch (Exception error) {
                    if (type.isInstance(error)) return;
                    throw error;
                }
                throw new AssertionError("invalid operation succeeded");
            }
            public static void main(String[] args) {
        """ + source + """
                BankAccount account = new BankAccount(12);
                reject(IllegalArgumentException.class, () -> new BankAccount(-1));
                reject(IllegalArgumentException.class, () -> account.withdraw(-4));
                reject(IllegalArgumentException.class, () -> account.withdraw(0));
                reject(IllegalArgumentException.class, () -> account.deposit(0));
                reject(IllegalArgumentException.class, () -> account.deposit(-4));
                reject(IllegalStateException.class, () -> account.withdraw(13));
                reject(ArithmeticException.class, () -> account.deposit(Long.MAX_VALUE));
                if (account.balance() != 12) throw new AssertionError("balance changed");
                account.withdraw(12);
                if (account.balance() != 0) throw new AssertionError("full withdrawal");
            }
        }
    """)
    run(jvm, directory)

    imports, stack = split_imports(samples["generic-stack"].split("\nStack<String> stack", 1)[0])
    stack_check = "\n".join(imports) + f"""
        class Main {{
            public static void main(String[] args) {{
                {stack}
                Stack<String> stack = new Stack<>();
                stack.push("A");
                if (!stack.pop().equals("A") || !stack.isEmpty()) throw new AssertionError();
                try {{ stack.pop(); }}
                catch (IndexOutOfBoundsException expected) {{ return; }}
                throw new AssertionError("empty pop succeeded");
            }}
        }}
    """
    compile_source(javac, directory, stack_check)
    run(jvm, directory)
    bad_stack = compile_source(javac, directory, stack_check.replace('stack.push("A");', 'stack.push(3);'), check=False)
    assert bad_stack.returncode and "compiler.err.cant.apply.symbol" in bad_stack.stdout, bad_stack.stdout

    checked = samples["exceptions"].split("\ntry {", 1)[0]
    bad_call = compile_source(javac, directory, f"""
        class Main {{
            public static void main(String[] args) {{
                {checked}
                wallet.withdraw(7);
            }}
        }}
    """, check=False)
    assert bad_call.returncode and "compiler.err.unreported.exception" in bad_call.stdout, bad_call.stdout

    assert sum(range(1, 3)) == 3 and 3 * 4 == 12
    assert (2 * 5, 5 * 5) == (10, 25)
    assert 2 * 6 == 12 and len(["A", "B", "C"]) == 3
    assert max(range(5)) == 4
    print(f"P.1.2 {verified} Java snippets, account/stack boundaries and compiler rejections passed")


def check_maven(text, directory, maven, jdk):
    pom, = blocks(text, "xml")
    pom = pom.replace("</project>", """
      <dependencies>
        <dependency>
          <groupId>junit</groupId><artifactId>junit</artifactId><version>4.13.2</version><scope>test</scope>
        </dependency>
      </dependencies>
    </project>""")
    (directory / "pom.xml").write_text(pom, encoding="utf-8")
    source = directory / "src/main/java"
    source.mkdir(parents=True)
    (source / "Desk.java").write_text("class Desk { static int limit() { return 3; } }", encoding="utf-8")
    tests = directory / "src/test/java"
    tests.mkdir(parents=True)
    test_file = tests / "DeskTest.java"
    test = """
        import org.junit.Test;
        import static org.junit.Assert.assertEquals;
        public class DeskTest {
            @Test public void limit() { assertEquals(3, Desk.limit()); }
        }
    """
    test_file.write_text(test, encoding="utf-8")
    env = os.environ.copy()
    if jdk:
        env["JAVA_HOME"] = str(jdk)
    env["JAVA_TOOL_OPTIONS"] = f'-Duser.home="{directory}" -Djava.io.tmpdir="{directory}"'
    command = [maven, "-B", "-ntp", f"-Dmaven.repo.local={ROOT / 'temp/p-1-2-maven-repo'}"]
    output = run([*command, "test"], directory, env=env, timeout=180).stdout
    jar = directory / "target/desk-1.0.jar"
    assert "Tests run: 1, Failures: 0, Errors: 0" in output and not jar.exists(), output
    run([*command, "package"], directory, env=env, timeout=180)
    with ZipFile(jar) as archive:
        assert "Desk.class" in archive.namelist()
    run([*command, "clean"], directory, env=env, timeout=180)
    assert not jar.exists()
    test_file.write_text(test.replace("assertEquals(3", "assertEquals(4"), encoding="utf-8")
    result = run([*command, "package"], directory, env=env, timeout=180, check=False)
    assert result.returncode and "Tests run: 1, Failures: 1, Errors: 0" in result.stdout, result.stdout
    assert not jar.exists()
    print("P.1.2 Maven test, package, clean and failed-test behavior passed")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--jdk", type=Path, help="JDK 21 directory (defaults to javac/java in PATH)")
    parser.add_argument("--maven", type=Path, help="optional Maven executable")
    args = parser.parse_args()
    text = PACK.read_text(encoding="utf-8")
    jdk = args.jdk.resolve() if args.jdk else None
    bin_dir = jdk / "bin" if jdk else None
    javac = str(bin_dir / "javac") if bin_dir else "javac"
    java = str(bin_dir / "java") if bin_dir else "java"
    work = ROOT / "temp"
    work.mkdir(exist_ok=True)
    with TemporaryDirectory(dir=work, prefix="p-1-2-verify-") as directory:
        check_java(text, Path(directory), javac, java)
        if args.maven:
            check_maven(text, Path(directory), str(args.maven.resolve()), jdk)
