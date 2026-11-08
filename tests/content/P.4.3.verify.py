"""Run the Java examples as printed in P.4.3, including their boundary cases."""

from argparse import ArgumentParser
from pathlib import Path
import re
import subprocess
from tempfile import TemporaryDirectory
from textwrap import dedent, indent


ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "data/content/P.4.3.yaml"


def examples():
    text = PACK.read_text(encoding="utf-8")
    sections = re.split(r"^  - id: ", text, flags=re.MULTILINE)[1:]
    for section in sections:
        lesson_id = section.splitlines()[0]
        for block in re.findall(r"^ +```java\n(.*?)^ +```$", section, re.MULTILINE | re.DOTALL):
            source, expected = dedent(block).strip().rsplit("\n// expect: ", 1)
            yield lesson_id, source, expected.split("|")


def check_java(java, work):
    verified = []
    for lesson, source, expected in examples():
        imports = re.findall(r"^import .+;$", source, re.MULTILINE)
        statements = re.sub(r"^import .+;\n", "", source, flags=re.MULTILINE)
        entry = work / "LessonExample.java"
        entry.write_text(
            "\n".join(imports) + "\nclass LessonExample {\n"
            "    public static void main(String[] args) {\n"
            + indent(statements, "        ") + "\n    }\n}\n",
            encoding="utf-8",
        )
        result = subprocess.run(
            [java, "-Dfile.encoding=UTF-8", "--source", "21", str(entry)],
            cwd=work, capture_output=True, encoding="utf-8", timeout=20,
        )
        assert result.returncode == 0, (lesson, result.stderr)
        actual = result.stdout.strip().splitlines()
        assert actual == expected, (lesson, actual, expected)
        verified.append(lesson)

    # These exercises use concrete outcomes rather than only naming a pattern.
    for required in ("ownership", "injection", "observer", "composite-flyweight", "local-refactor"):
        assert required in verified, required
    print(f"P.4.3 {len(verified)} Java snippets passed")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--jdk", type=Path, help="JDK 21 directory (defaults to java in PATH)")
    args = parser.parse_args()
    java = str(args.jdk.resolve() / "bin" / "java") if args.jdk else "java"
    temp = ROOT / "temp"
    temp.mkdir(exist_ok=True)
    with TemporaryDirectory(dir=temp, prefix="p-4-3-verify-") as directory:
        check_java(java, Path(directory))
