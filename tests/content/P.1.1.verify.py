# Checks every value, output and error that data/content/P.1.1.yaml states, by running Python.
# usage: python -I tests/content/P.1.1.verify.py   (prints "N/N claims hold"; exit code 1 on any mismatch)
import io, contextlib, math

def out(code):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(code, {})
    return buf.getvalue()

def raises(code, exc):
    try:
        exec(code, {})
    except exc:
        return True
    return False

checks = [
    # first-program
    (out('print("早上好")\nprint("晚上好")'), "早上好\n晚上好\n"),
    (out('print(3 + 4)\nprint("3 + 4")'), "7\n3 + 4\n"),
    (out('print(2 + 2)'), "4\n"), (out('print("2 + 2")'), "2 + 2\n"),
    (raises('Print("你好")', NameError), True),
    (raises('print("你好)', SyntaxError), True),
    (raises('print（"你好"）', SyntaxError), True),
    (out("print('hello')"), "hello\n"),
    (10 - 4, 6),
    # numbers
    (7 / 2, 3.5), (3 * 4 + 1, 13), (2 + 3 * 4, 14), ((2 + 3) * 4, 20), ((10 - 4) * 2 + 1, 13),
    (out('print(6 / 2)'), "3.0\n"), (7 // 2, 3), (7 % 2, 1), (2 ** 3, 8),
    (17 // 5, 3), (17 % 5, 2), (out('print(17 / 5)'), "3.4\n"), (2 ** 4, 16),
    (23 // 6, 3), (23 % 6, 5), (50 // 12, 4), (50 % 12, 2), (200 // 60, 3), (200 % 60, 20),
    # text-and-truth
    (out('print("3" + "4")'), "34\n"), ("ha" * 3, "hahaha"), (len("hello"), 5), (out('print("ab" * 3)'), "ababab\n"),
    (len("Python"), 6), (out('print(type(7))'), "<class 'int'>\n"), ("7" * 2, "77"),
    (3 > 2, True), (3 == 2, False), (3 != 2, True), (out('print(10 >= 10)'), "True\n"),
    (type(4 > 2).__name__, "bool"), (type(4.0).__name__, "float"),
    (raises('"3" + 4', TypeError), True), (int("3") + 4, 7), ("3" + str(4), "34"),
    (int("12") + 3, 15), ("12" + str(3), "123"), (out('print("我今年 " + str(18) + " 岁")'), "我今年 18 岁\n"),
    (raises('print("我今年 " + 18 + " 岁")', TypeError), True), (raises('print("我今年 " + int("18") + " 岁")', TypeError), True),
    # lists-dicts
    (len([3, 8, 5]), 3), (len([10, 20, 30, 40]), 4), ([3, 8, 5][0], 3), ([3, 8, 5][2], 5),
    (raises('[3, 8, 5][3]', IndexError), True), ([7, 9, 4, 6][1], 9), (raises('[7, 9, 4, 6][4]', IndexError), True),
    (len(["春", "夏", "秋", "冬"]) - 1, 3), (out('print({"苹果": 5, "梨": 3}["梨"])'), "3\n"),
    ({"a": 1, "b": 2, "c": 3}["c"], 3), (raises('{"苹果": 5}["香蕉"]', KeyError), True), ({"小明": 150, "小红": 147}["小红"], 147),
    # naming
    (out('x = 5\nprint(x + 1)'), "6\n"), (out('price = 8\nprint(price * 3)'), "24\n"),
    (out('n = 3\nn = n * 2\nn = n + 1\nprint(n)'), "7\n"), (out('price = 8\ncount = 3\ntotal = price * count\nprice = 10\nprint(total)'), "24\n"),
    (out('a = 2\nb = a + 3\na = 10\nprint(a, b)'), "10 5\n"), (raises('2age = 1', SyntaxError), True),
    (raises('my-price = 1', SyntaxError), True), (raises('for = 1', SyntaxError), True),
    (out('w = 4\nh = 3\narea = w * h\nw = 10\nprint(area)'), "12\n"),
    # aliasing
    (out('nums = [1, 2]\nnums.append(3)\nprint(nums)'), "[1, 2, 3]\n"), (out('xs = ["a"]\nxs.append("b")\nprint(xs)'), "['a', 'b']\n"),
    (out('a = [1, 2]\nb = a\nb.append(3)\nprint(a)'), "[1, 2, 3]\n"),
    (out('a = [1, 2]\nb = a\nb.append(3)\nc = a.copy()\nc.append(4)\nprint(a, b, c)'), "[1, 2, 3] [1, 2, 3] [1, 2, 3, 4]\n"),
    (out('x = [5]\ny = x.copy()\ny.append(6)\nprint(x)'), "[5]\n"), (out('a = 1\nb = a\nb = b + 1\nprint(a, b)'), "1 2\n"),
    (out('s = "hi"\nt = s\nt = t + "!"\nprint(s)'), "hi\n"), (out('a, b = 1, 2\nprint(a, b)'), "1 2\n"),
    (out('a = 3\nb = 4\na, b = b, a + b\nprint(a, b)'), "4 7\n"),
    # if-else
    (out('score = 75\nif score >= 60:\n    print("及格")\nprint("结束")'), "及格\n结束\n"),
    (out('score = 50\nif score >= 60:\n    print("及格")\n    print("恭喜")\nprint("结束")'), "结束\n"),
    (out('t = 30\nif t > 35:\n    print("很热")\n    print("开空调")\nprint("看温度")'), "看温度\n"),
    (out('n = 7\nif n % 2 == 0:\n    print("偶数")\nelse:\n    print("奇数")'), "奇数\n"),
    *[(out(f'score = {s}\nif score >= 90:\n    grade = "A"\nelif score >= 80:\n    grade = "B"\nelse:\n    grade = "C"\nprint(grade)'), g + "\n") for s, g in [(85, "B"), (92, "A"), (59, "C")]],
    ((lambda age: age >= 12 and age < 18)(15), True),
    (out('t = 33\nif t > 30:\n    print("热")\nelse:\n    print("不热")'), "热\n"),
    # for-loops
    (out('for i in range(5):\n    print("嗨")').count("嗨"), 5), (out('for x in [3, 1, 4]:\n    print(x)'), "3\n1\n4\n"),
    (out('for c in ["红", "绿"]:\n    print(c + "灯")'), "红灯\n绿灯\n"),
    (list(range(5)), [0, 1, 2, 3, 4]), (list(range(1, 5)), [1, 2, 3, 4]), (list(range(0, 10, 3)), [0, 3, 6, 9]), (len(range(2, 10, 3)), 3),
    (out('total = 0\nfor i in range(1, 5):\n    total = total + i\nprint(total)'), "10\n"),
    (out('total = 0\nfor x in [5, 2, 8]:\n    total = total + x\nprint(total)'), "15\n"),
    (out('total = 0\nfor x in [4, 6, 1]:\n    total = total + x\nprint(total)'), "11\n"),
    (3 + 5 + 2, 10), (out('total = 0\nfor x in [3, 5, 2, 6]:\n    total = total + x\nprint(total)'), "16\n"),
    (sum(range(1, 101)), 5050),
    (out('count = 0\nfor x in [3, 8, 5, 10]:\n    if x > 4:\n        count = count + 1\nprint(count)'), "3\n"),
    (sum(1 for x in [3, 8, 5, 10] if x % 2 == 0), 2),
    # while-loops
    (out('n = 3\nwhile n > 0:\n    print(n)\n    n = n - 1'), "3\n2\n1\n"),
    (out('x = 1\nwhile x < 50:\n    x = x * 2\nprint(x)'), "64\n"),
    (out('i = 10\nseq = []\nwhile i > 0:\n    seq.append(i)\n    i = i - 3\nprint(seq, i)'), "[10, 7, 4, 1] -2\n"),
    (out('n = 1\nwhile True:\n    if n * n > 50:\n        break\n    n = n + 1\nprint(n)'), "8\n"),
    (out('n = 1\nwhile True:\n    if n * n > 20:\n        break\n    n = n + 1\nprint(n)'), "5\n"),
    # functions
    (out('def double(x):\n    return x * 2\n\nprint(double(5) + 1)'), "11\n"),
    (out('def square(n):\n    return n * n\nprint(square(3), square(3) + 1, square(square(2)))'), "9 10 16\n"),
    (out('def f(x):\n    return x * 3 - 1\nprint(f(4))'), "11\n"), (out('def area(w, h):\n    return w * h\nprint(area(3, 4))'), "12\n"),
    (out('def area(w, h):\n    s = w * h\n    return s\n\na = area(3, 4)\nb = area(a, 2)\nprint(b)'), "24\n"),
    (out('def area(w, h):\n    s = w * h\n    return s\n\na = area(2, 5)\nb = area(a, 3)\nprint(b)'), "30\n"),
    (out('def f(x):\n    print(x * 2)\n\ny = f(3)\nprint(y)'), "6\nNone\n"),
    (out('def is_even(n):\n    return n % 2 == 0\nprint(is_even(4), is_even(7))'), "True False\n"),
    (out('def f(n): return n % 3 == 0\nprint(f(9), f(10))'), "True False\n"), (out('def f(n): return n / 3 == 0\nprint(f(9))'), "False\n"),
    (out('def bigger(a, b):\n    if a > b:\n        return a\n    return b\nprint(bigger(4, 9) + bigger(7, 2))'), "16\n"),
    # scope-defaults
    (out('x = 1\ndef f():\n    x = 2\nf()\nprint(x)'), "1\n"), (raises('def g():\n    y = 5\ng()\nprint(y)', NameError), True),
    (out('count = 0\ndef add():\n    global count\n    count = count + 1\nadd()\nadd()\nprint(count)'), "2\n"),
    (out('def greet(name, word="你好"):\n    return word + "，" + name\nprint(greet("小明"))\nprint(greet("小明", word="早"))'), "你好，小明\n早，小明\n"),
    (out('def f(a, b=10): return a - b\nprint(f(3), f(b=1, a=5))'), "-7 4\n"),
    (out('def add(x, box=[]):\n    box.append(x)\n    return box\nprint(add(1))\nprint(add(2))'), "[1]\n[1, 2]\n"),
    (out('def add(x, box=list()):\n    box.append(x)\n    return box\nadd(1)\nprint(add(2))'), "[1, 2]\n"),
    (out('def add(x, box=None):\n    if box is None:\n        box = []\n    box.append(x)\n    return box\nadd(1)\nprint(add(2))'), "[2]\n"),
    # modules
    (out('import math\nprint(math.sqrt(16))'), "4.0\n"), (math.sqrt(81), 9.0), (raises('import math\nsqrt(16)', NameError), True),
    (out('from math import sqrt\nprint(sqrt(16))'), "4.0\n"), (out('import math as m\nprint(m.sqrt(16))'), "4.0\n"),
    (raises('import math\nmath(math.sqrt(16))', TypeError), True), (out('from random import randint\nprint(1 <= randint(1, 6) <= 6)'), "True\n"),
    (math.gcd(12, 18), 6), (math.floor(3.7), 3), (math.floor(9.99), 9), (math.gcd(24, 36), 12),
    # input-output
    (raises('x = "5"\nx + 1', TypeError), True), ("12" * 2, "1212"),
    (out('print(1, 2, 3, sep="-")'), "1-2-3\n"), (out('print("a", end="")\nprint("b")'), "ab\n"),
    (out('name = "小明"\nage = 12\nprint(f"{name}今年{age}岁，明年{age + 1}岁")'), "小明今年12岁，明年13岁\n"),
    (out('n = 3\nprint(f"{n}的平方是{n * n}")'), "3的平方是9\n"),
    (out('name = "小红"\nage = int("9")\nprint(f"你好，{name}！10 年后你 {age + 10} 岁。")'), "你好，小红！10 年后你 19 岁。\n"),
    (raises('age = "9"\nage + 10', TypeError), True),
    # debugging
    (raises('prnt("hi")', NameError), True), (raises('1 / 0', ZeroDivisionError), True), (raises('[1, 2][5]', IndexError), True),
    (raises('"a" + 1', TypeError), True), (raises('{"a": 1}["b"]', KeyError), True),
    (out('xs = [2, 4, 6]\ntotal = 0\nfor i in range(1, len(xs)):\n    total = total + xs[i]\nprint(total / len(xs))'), "3.3333333333333335\n"),
    (raises('assert 2 + 2 == 5', AssertionError), True),
    (raises('def average(xs): return sum(xs) / len(xs)\naverage([])', ZeroDivisionError), True),
    (out('def average(xs):\n    if len(xs) == 0:\n        raise ValueError\n    return sum(xs) / len(xs)\nassert average([2, 4, 6]) == 4\nassert average([5]) == 5\nprint("ok")'), "ok\n"),
    # boss
    (len("abc" * 2) + 7 // 2, 9), (out('a = 4\nb = a\na = a + 3\nb = b * 2\nprint(a + b)'), "15\n"),
    (out('count = 0\nfor n in range(1, 21):\n    if n % 3 == 0:\n        count = count + 1\nprint(count)'), "6\n"),
    (out('n = 100\nsteps = 0\nwhile n > 1:\n    n = n // 2\n    steps = steps + 1\nprint(steps)'), "6\n"),
    (out('def is_prime(n):\n    if n < 2:\n        return False\n    d = 2\n    while d * d <= n:\n        if n % d == 0:\n            return False\n        d = d + 1\n    return True\n\ncount = 0\nfor n in range(1, 51):\n    if is_prime(n):\n        count = count + 1\nprint(count)'), "15\n"),
    (out('def average(xs):\n    total = 0\n    for i in range(1, len(xs)):\n        total = total + xs[i]\n    return total / len(xs)\nprint(round(average([2, 4, 6]), 4))'), "3.3333\n"),
]

# ---- lessons added 2026-11-03 for knowledge coverage (reports/coverage/P.1.1.md) ----
import os, json, shutil, subprocess, sys
from collections import Counter, deque

def err(code):
    """'TypeName: message' of the exception the code raises, or None."""
    try:
        exec(code, {})
    except BaseException as e:
        return f"{type(e).__name__}: {e}"
    return None

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WORK = os.path.join(ROOT, "temp", "verify-P.1.1")   # inside the project, deleted at the end

def files_run(files, main):
    """Write files into a fresh folder and run `python main` there; returns (stdout, stderr, returncode)."""
    shutil.rmtree(WORK, ignore_errors=True)
    for name, text in files.items():
        path = os.path.join(WORK, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
    # -E -s: ignore PYTHON* variables and user site-packages, but keep the script's folder on the
    # import path (-I would drop it, and that folder is exactly what the module lessons are about).
    args = [sys.executable, "-X", "utf8", "-E", "-s", main]
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    env.pop("PYTHONDONTWRITEBYTECODE", None)
    r = subprocess.run(args, cwd=WORK, capture_output=True, text=True, encoding="utf-8", env=env)
    return r.stdout, r.stderr, r.returncode

def in_work(code):
    """Run code with a fresh WORK folder as the current directory, capturing print output."""
    shutil.rmtree(WORK, ignore_errors=True); os.makedirs(WORK)
    old = os.getcwd(); os.chdir(WORK)
    try:
        return out(code)
    finally:
        os.chdir(old)

MATCH_STATUS = 'match status:\n    case 200:\n        print("成功")\n    case 404:\n        print("找不到页面")\n    case _:\n        print("其他")'
MATCH_CMD = 'match cmd:\n    case "quit" | "q":\n        print("退出")\n    case _:\n        print("继续")'
MATCH_POINT = 'match point:\n    case (0, 0):\n        print("原点")\n    case (0, y):\n        print("在 y 轴上", y)\n    case (x, 0):\n        print("在 x 轴上", x)\n    case (x, y):\n        print("别处", x, y)'
TOP_WORDS = '''def top_words(text, k=3):
    clean = ""
    for c in text.lower():
        if c.isalpha() or c == "'":
            clean = clean + c
        else:
            clean = clean + " "
    counts = {}
    for w in clean.split():
        counts[w] = counts.get(w, 0) + 1
    pairs = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)
    return pairs[:k]
'''
tw = {}; exec(TOP_WORDS, tw); top_words = tw["top_words"]
PAY = 'class NotEnoughMoney(Exception):\n    pass\n\ndef pay(balance, price):\n    if price > balance:\n        raise NotEnoughMoney(f"还差 {price - balance} 元")\n    return balance - price\n'
REPORT = 'def average(xs):\n    return sum(xs) / len(xs)\n\ndef report(xs):\n    return "平均 " + str(average(xs))\n\nprint(report([]))\n'
TB = """Traceback (most recent call last):
  File "report.py", line 7, in <module>
    print(report([]))
          ~~~~~~^^^^
  File "report.py", line 5, in report
    return "平均 " + str(average(xs))
                         ~~~~~~~^^^^
  File "report.py", line 2, in average
    return sum(xs) / len(xs)
           ~~~~~~~~^~~~~~~~~
ZeroDivisionError: division by zero
"""
SQ = "def square(x):\n    return x * x\n\ndef sum_squares(a, b):\n    return square(a) + square(b)\n\nprint(sum_squares(3, 4))\n"
def stack_at_first(code, func):
    r = subprocess.run([sys.executable, "-X", "utf8", "-I", os.path.join(ROOT, "scripts", "lib", "pytrace.py")], input=json.dumps({"code": code}), capture_output=True, text=True, encoding="utf-8")
    return next(s.get("stack") for s in json.loads(r.stdout)["steps"] if s["func"] == func)
A, B = {1, 2, 3}, {2, 3, 4}

checks += [
    # slicing
    ("Python"[-1], "n"), ("Python"[0], "P"), ("Python"[-2], "o"), ("Python"[-6], "P"), ("Python"[0:2], "Py"), ("Python"[2:5], "tho"),
    ("Python"[1:4], "yth"), ("Python"[:2], "Py"), ("Python"[2:], "thon"), ("Python"[-3:], "hon"), ("Python"[:], "Python"), ("Python"[4:42], "on"),
    ("hello"[1:], "ello"), ("hello"[:-1], "hell"), ("hello"[:4], "hell"), (len("abcdefgh"[2:6]), 4), ("abcdefgh"[2:6], "cdef"),
    ([10, 20, 30, 40, 50][1:3], [20, 30]), ([1, 2] + [3], [1, 2, 3]), ([[1, 2], [3, 4]][1], [3, 4]), ([[1, 2], [3, 4]][1][0], 3),
    (err('"Python"[0] = "J"'), "TypeError: 'str' object does not support item assignment"), ("J" + "Python"[1:], "Jython"),
    (err('"cat"[0] = "b"').split(":")[0], "TypeError"), ("b" + "cat"[1:], "bat"),
    ("Hello".lower(), "hello"), ("Hello".upper(), "HELLO"), ("  hi  ".strip(), "hi"), ("a,b,c".split(","), ["a", "b", "c"]),
    ("one two  three".split(), ["one", "two", "three"]), ("a-b".replace("-", "+"), "a+b"), ("th" in "Python", True),
    ("Hi".upper(), "HI"), (" ok ".strip(), "ok"), (str("a b".split()), "['a', 'b']"), ("2026-11".replace("-", "/"), "2026/11"),
    ("photo.png".split("."), ["photo", "png"]), ("photo.png".split(".")[-1], "png"), ("a.tar.gz".split("."), ["a", "tar", "gz"]),
    ("report.final.pdf".split(".")[-1], "pdf"), ("Hello, World!".lower(), "hello, world!"), ("Hello, World!".lower().split(), ["hello,", "world!"]),
    ("Hello, World!".split(), ["Hello,", "World!"]),
    # tuples-sets
    ((10, 20, 30)[1], 20), ((10, 20, 30)[-1], 30), (err("(3, 4)[0] = 5"), "TypeError: 'tuple' object does not support item assignment"),
    (err("(1, 2)[0] = 5").split(":")[0], "TypeError"), (eval("3, 4"), (3, 4)), (type((5)), int), (type((5,)), tuple), (type(()), tuple),
    (type((7,)).__name__, "tuple"), ({(0, 0): "原点"}[(0, 0)], "原点"), (err('{[0, 0]: "原点"}'), "TypeError: cannot use 'list' as a dict key (unhashable type: 'list')"),
    ({(3, 5): "学校"}[(3, 5)], "学校"), (err('{[3, 5]: "学校"}').split(":")[0], "TypeError"),
    (len({3, 1, 3, 2, 1}), 3), ({3, 1, 3, 2, 1}, {1, 2, 3}), (err("x = {1, 2}\nx[0]").split(":")[0], "TypeError"), (2 in {1, 2, 3}, True),
    (set("hello"), {"h", "e", "l", "o"}), (len(set("hello")), 4), (len(set("banana")), 3),
    ({1, 2, 3} | {3, 4}, {1, 2, 3, 4}), ({1, 2, 3} & {3, 4}, {3}), ({1, 2, 3} - {3, 4}, {1, 2}),
    (str(A & B), "{2, 3}"), (str(A | B), "{1, 2, 3, 4}"), (str(A - B), "{1}"), (str(B - A), "{4}"),
    (type({}), dict), (type(set()), set), ("梨" in {"苹果": 5, "梨": 3}, True), ({"苹果": 5}.get("香蕉", 0), 0),
    (len({"a": 1, "b": 2}), 2), (list({"a": 1, "b": 2}), ["a", "b"]), ({"a": 1}.get("b", 0), 0), ({"a": 1}.get("b"), None),
    (err('{"a": 1}["b"]').split(":")[0], "KeyError"), (5 in {"a": 5}, False), (5 in {"a": 5}.values(), True),
    # list-methods
    (out('nums = [10, 20, 30]\nx = nums.pop()\nprint(nums, x)'), "[10, 20] 30\n"),
    (out('xs = [1, 2, 3]\nxs.insert(0, 9)\nprint(xs)\nxs.remove(2)\nprint(xs)\nlast = xs.pop()\nprint(xs, last)'), "[9, 1, 2, 3]\n[9, 1, 3]\n[9, 1] 3\n"),
    ([1, 2, 1].index(1), 0), ([1, 2, 1].count(1), 2), (out('xs = [5, 6]\nprint(xs.pop(0), xs)'), "5 [6]\n"),
    (out('xs = [3, 1, 2]\nys = sorted(xs)\nprint(xs, ys)'), "[3, 1, 2] [1, 2, 3]\n"), (out('xs = [3, 1, 2]\nys = xs.sort()\nprint(ys, xs)'), "None [1, 2, 3]\n"),
    (sorted([5, 2, 9], reverse=True), [9, 5, 2]), (sorted(["b", "a"]), ["a", "b"]),
    (out('xs = [1, 2, 3, 4]\ndel xs[1:3]\nprint(xs)'), "[1, 4]\n"), (out('xs = [1, 2, 3]\ndel xs[0]\nprint(xs)'), "[2, 3]\n"),
    (out('prices = {"苹果": 5, "梨": 3}\ndel prices["梨"]\nprint(prices)'), "{'苹果': 5}\n"), (raises('x = 1\ndel x\nprint(x)', NameError), True),
    (out('prices = {"苹果": 5}\nprices["梨"] = 3\nprices["苹果"] = 6\nprint(prices)'), "{'苹果': 6, '梨': 3}\n"),
    (out('counts = {}\nfor w in ["a", "b", "a", "a"]:\n    counts[w] = counts.get(w, 0) + 1\nprint(counts["a"])'), "3\n"),
    (out('s = []\ns.append(1)\ns.append(2)\ns.append(3)\ns.pop()\nprint(s.pop())'), "2\n"),
    (out('a, b = 1, 2\nprint(a, b)'), "1 2\n"), (err('a, b = [1, 2, 3]'), "ValueError: too many values to unpack (expected 2, got 3)"),
    # loop-control
    (out('for n in range(1, 6):\n    if n % 2 == 0:\n        continue\n    print(n)'), "1\n3\n5\n"),
    (out('total = 0\nfor n in range(1, 8):\n    if n % 3 == 0:\n        continue\n    total = total + n\nprint(total)'), "19\n"),
    (out('for n in [1, 2, 3, 4]:\n    if n == 3:\n        break\n    print(n)'), "1\n2\n"),
    (out('for n in [1, 2, 3, 4]:\n    if n == 3:\n        continue\n    print(n)'), "1\n2\n4\n"),
    *[(out(f'n = {n}\nfor d in range(2, n):\n    if n % d == 0:\n        print("不是素数，能被", d, "整除")\n        break\nelse:\n    print(n, "是素数")'), want)
      for n, want in [(7, "7 是素数\n"), (9, "不是素数，能被 3 整除\n")]],
    (out('for x in []:\n    print(x)\nelse:\n    print("完")'), "完\n"), (out('for x in range(3):\n    pass\nprint("ok")'), "ok\n"),
    (err('if 3 > 2:\n'), "IndentationError: expected an indented block after 'if' statement on line 1 (<string>, line 1)"),
    (out('xs = [4, 15, 7, 22]\nfor x in xs:\n    if x > 10:\n        print(x)\n        break\nelse:\n    print(0)'), "15\n"),
    (out('xs = [3, -2, -5]\nfor x in xs:\n    if x < 0:\n        print(x)\n        break\nelse:\n    print("没有负数")'), "-2\n"),
    (out('xs = [3, 4]\nfor x in xs:\n    if x < 0:\n        print(x)\n        break\nelse:\n    print("没有负数")'), "没有负数\n"),
    # loop-techniques
    (out('for i, c in enumerate("ab"):\n    print(i, c)'), "0 a\n1 b\n"), (out('for i, x in enumerate(["甲", "乙"]):\n    print(i, x)'), "0 甲\n1 乙\n"),
    (out('for i, x in enumerate([5, 7, 9], 1):\n    print(i * x)'), "5\n14\n27\n"),
    (out('for name, score in zip(["小明", "小红"], [90, 85]):\n    print(name, score)'), "小明 90\n小红 85\n"),
    (out('for a, b in zip([1, 2, 3], [10, 20]):\n    print(a + b)'), "11\n22\n"),
    (list({"苹果": 5, "梨": 3}.items()), [("苹果", 5), ("梨", 3)]), (list({"苹果": 5, "梨": 3}), ["苹果", "梨"]),
    (list(reversed([1, 2, 3])), [3, 2, 1]), (sorted(set([3, 1, 3, 2])), [1, 2, 3]),
    ([x * x for x in range(5)], [0, 1, 4, 9, 16]), ([x for x in range(10) if x % 3 == 0], [0, 3, 6, 9]),
    ([x * 2 for x in [1, 2, 3]], [2, 4, 6]), (len([x for x in range(1, 21) if x % 4 == 0]), 5),
    ("I love Python".split(), ["I", "love", "Python"]), ([len(w) for w in "I love Python".split()], [1, 4, 6]),
    ([w.upper() for w in "a bc".split()], ["A", "BC"]),
    (out('xs = [1, 2, 2, 3]\nfor x in xs:\n    if x == 2:\n        xs.remove(x)\nprint(xs)'), "[1, 2, 3]\n"), ([x for x in [1, 2, 2, 3] if x != 2], [1, 3]),
    # conditions-more
    (out('print(1 < 3 < 5)'), "True\n"), (0 < 10 < 5, False), ("py" in "python", True), (3 not in [1, 2], True),
    (out('a = [1, 2]\nb = [1, 2]\nc = a\nprint(a == b, a is b, a is c)'), "True False True\n"),
    (out('x = [5]\ny = [5]\nprint(x == y, x is y)'), "True False\n"), (out('x = 0\nprint(x != 0 and 10 / x > 1)'), "False\n"),
    ("" or "无名", "无名"), (out('print("" or "无名")'), "无名\n"),
    (bool(0), False), (bool(""), False), (bool([]), False), (bool({}), False), (bool(None), False), (bool("0"), True), (bool(" "), True),
    ([1, 2, 3] < [1, 2, 4], True), ((1, 2) < (1, 2, 0), True), ("apple" < "banana", True), ("Zebra" < "apple", True),
    (err('1 < "2"').split(":")[0], "TypeError"), ([2, 1] < [1, 9, 9], False), ("Zoo" < "apple", True),
    # match
    *[(out(f'status = {v}\n' + MATCH_STATUS), want) for v, want in [(404, "找不到页面\n"), (500, "其他\n"), (200, "成功\n")]],
    *[(out(f'cmd = "{v}"\n' + MATCH_CMD), want) for v, want in [("q", "退出\n"), ("quit", "退出\n"), ("x", "继续\n")]],
    *[(out(f'point = {v}\n' + MATCH_POINT), want) for v, want in [((0, 5), "在 y 轴上 5\n"), ((3, 0), "在 x 轴上 3\n"), ((0, 0), "原点\n"), ((2, 7), "别处 2 7\n")]],
    (out('n = -7\nmatch n:\n    case 0:\n        r = 0\n    case x if x > 0:\n        r = 1\n    case _:\n        r = -1\nprint(r)'), "-1\n"),
    (out('n = 5\nmatch n:\n    case 1:\n        print("一")\nprint("完")'), "完\n"),
    # more-functions
    (max(3, 9, 4, 7), 9), (out('def total(*nums):\n    return sum(nums)\n\nprint(total(1, 2, 3))\nprint(total())'), "6\n0\n"),
    (out('def f(*nums):\n    return nums\nprint(f(1, 2, 3), f())'), "(1, 2, 3) ()\n"),
    (out('def count(*xs): return len(xs)\nprint(count(5, 6, 7, 8))'), "4\n"),
    (out('def info(**kw):\n    return kw\n\nprint(info(name="小明", age=12))'), "{'name': '小明', 'age': 12}\n"),
    (out('def f(**kw): return len(kw)\nprint(f(a=1, b=2, c=3))'), "3\n"),
    (list(range(*[3, 7])), list(range(3, 7))), (out('print(*[1, 2, 3])'), "1 2 3\n"), (out('print(*["a", "b"], sep="-")'), "a-b\n"),
    (out('def f(a): return a\nprint(f(**{"a": 1}))'), "1\n"), ((lambda x: x * 2)(5), 10),
    (sorted(["ccc", "a", "bb"], key=len), ["a", "bb", "ccc"]),
    (sorted([("甲", 3), ("乙", 1), ("丙", 2)], key=lambda p: p[1]), [("乙", 1), ("丙", 2), ("甲", 3)]),
    (sorted([("甲", 3), ("乙", 1), ("丙", 2)]), [("丙", 2), ("乙", 1), ("甲", 3)]),
    (sorted([("甲", 3), ("乙", 1), ("丙", 2)], key=lambda p: p[1], reverse=True), [("甲", 3), ("丙", 2), ("乙", 1)]),
    (out('def area(w: float, h: float) -> float:\n    """长方形的面积：宽 w 乘高 h。"""\n    return w * h\nprint(area.__doc__, area(3, 4))'), "长方形的面积：宽 w 乘高 h。 12\n"),
    (out('def double(x: int) -> int: return x * 2\nprint(double("ab"))'), "abab\n"),
    (out('def f(a, /, b, *, c):\n    return a + b + c\nprint(f(1, 2, c=3), f(1, b=2, c=3))'), "6 6\n"),
    (raises('def f(a, /, b, *, c):\n    return a + b + c\nf(1, 2, 3)', TypeError), True),
    (raises('def f(a, /, b, *, c):\n    return a + b + c\nf(a=1, b=2, c=3)', TypeError), True),
    (out('def g(a, *, b): return a + b\nprint(g(1, b=2))'), "3\n"), (raises('def g(a, *, b): return a + b\ng(1, 2)', TypeError), True),
    # word-count
    ("Hi, hi!".lower().split(), ["hi,", "hi!"]), ("hi," == "hi!", False),
    (out('text = "Hi, hi!"\nclean = ""\nfor c in text.lower():\n    if c.isalpha() or c == "\'":\n        clean = clean + c\n    else:\n        clean = clean + " "\nprint(repr(clean), clean.split())'), "'hi  hi ' ['hi', 'hi']\n"),
    (out('words = "to be or not to be".split()\ncounts = {}\nfor w in words:\n    counts[w] = counts.get(w, 0) + 1\nprint(counts["be"], counts["or"])'), "2 1\n"),
    (sorted([("a", 1), ("b", 3), ("c", 3)], key=lambda kv: kv[1], reverse=True), [("b", 3), ("c", 3), ("a", 1)]),
    (sorted([("a", 1), ("b", 3), ("c", 3)], key=lambda kv: kv[1]), [("a", 1), ("b", 3), ("c", 3)]),
    (top_words("The cat and the hat. The end!", 1), [("the", 3)]), ("The cat and the hat. The end!".split().count("The"), 2),
    (len(top_words("a b c d", 3)), 3), (top_words("don't stop, don't", 1), [("don't", 2)]),
    # modules-packages
    (files_run({"tools.py": 'print("tools 被运行了")\n', "main.py": "import tools\n"}, "main.py")[0], "tools 被运行了\n"),
    (files_run({"tools.py": 'print("hi")\n', "main.py": "import tools\nimport tools\n"}, "main.py")[0], "hi\n"),
    (files_run({"tools.py": "print(__name__)\n", "main.py": "import tools\n"}, "main.py")[0], "tools\n"),
    (files_run({"tools.py": "print(__name__)\n"}, "tools.py")[0], "__main__\n"),
    (files_run({"tools.py": 'def add(a, b):\n    return a + b\n\nif __name__ == "__main__":\n    print(add(2, 3))\n', "main.py": "import tools\nprint(tools.add(1, 1))\n"}, "main.py")[0], "2\n"),
    (files_run({"tools.py": 'def add(a, b):\n    return a + b\n\nif __name__ == "__main__":\n    print(add(2, 3))\n'}, "tools.py")[0], "5\n"),
    (files_run({"tools.py": "x = 1\n", "main.py": "import tools\n"}, "main.py") and os.path.isdir(os.path.join(WORK, "__pycache__")), True),
    ("AttributeError" in files_run({"random.py": "import random\nprint(random.randint(1, 6))\n"}, "random.py")[1], True),
    (out('import math\nprint("sqrt" in dir(math))'), "True\n"),
    (files_run({"game/__init__.py": "", "game/sound.py": 'def play():\n    print("play")\n', "main.py": "from game import sound\nsound.play()\n"}, "main.py")[0], "play\n"),
    ("ModuleNotFoundError" in files_run({"game/__init__.py": "", "game/sound.py": "def play(): pass\n", "main.py": "import sound\n"}, "main.py")[1], True),
    ("ModuleNotFoundError" in files_run({"game/__init__.py": "", "game/sound.py": "def play(): pass\n", "main.py": "import game.sound.play\n"}, "main.py")[1], True),
    (files_run({"game/__init__.py": "", "game/sound.py": 'def play():\n    print("p")\n', "main.py": "from game.sound import play\nplay()\n"}, "main.py")[0], "p\n"),
    (files_run({"shapes/__init__.py": "", "shapes/circle.py": "def area(r):\n    return 3 * r * r\n", "main.py": "import shapes.circle\nprint(shapes.circle.area(2))\nfrom shapes import circle\nprint(circle.area(2))\nfrom shapes.circle import area\nprint(area(2))\n"}, "main.py")[0], "12\n12\n12\n"),
    (Counter("banana").most_common(2), [("a", 3), ("n", 2)]), (Counter("hello").most_common(1), [("l", 2)]),
    (out('from collections import deque\nq = deque([5, 6])\nq.append(7)\nq.popleft()\nprint(q.popleft())'), "6\n"),
    # input-output (format specs)
    (f"{3.14159:.2f}", "3.14"), (f"{42:5}", "   42"), (f"{'ab':<5}", "ab   "), (f"{'ab':>5}", "   ab"), (f"{'ab':^6}", "  ab  "),
    (f"{1234567:,}", "1,234,567"), (f"{0.25:.0%}", "25%"), (out('x = 3\nprint(f"{x=}")'), "x=3\n"), (out('print(f"{2 / 3:.3f}")'), "0.667\n"),
    ("{} 加 {} 等于 {}".format(1, 2, 3), "1 加 2 等于 3"), ("%d 岁" % 18, "18 岁"), (str("hi"), "hi"), (repr("hi"), "'hi'"),
    (out('print(["hi"])'), "['hi']\n"), (out('print(repr("5"))'), "'5'\n"),
    # files
    (in_work('with open("note.txt", "w", encoding="utf-8") as f:\n    f.write("第一行\\n")\n    f.write("第二行\\n")\nwith open("note.txt", encoding="utf-8") as f:\n    for line in f:\n        print(line.strip())\nwith open("note.txt", encoding="utf-8") as f:\n    print(len(f.readlines()))\nwith open("note.txt", encoding="utf-8") as f:\n    print(repr(f.readline()))'), "第一行\n第二行\n2\n'第一行\\n'\n"),
    (in_work('with open("a.txt", "w", encoding="utf-8") as f:\n    f.write("a")\n    f.write("b")\nprint(open("a.txt", encoding="utf-8").read())'), "ab\n"),
    (in_work('with open("log.txt", "w", encoding="utf-8") as f:\n    f.write("旧\\n")\nwith open("log.txt", "w", encoding="utf-8") as f:\n    f.write("新\\n")\nwith open("log.txt", encoding="utf-8") as f:\n    print(repr(f.read()))'), "'新\\n'\n"),
    (in_work('with open("log.txt", "w", encoding="utf-8") as f:\n    f.write("旧\\n")\nwith open("log.txt", "a", encoding="utf-8") as f:\n    f.write("新\\n")\nwith open("log.txt", encoding="utf-8") as f:\n    print(repr(f.read()))'), "'旧\\n新\\n'\n"),
    (in_work('try:\n    open("没有这个文件.txt", encoding="utf-8")\nexcept FileNotFoundError:\n    print("FileNotFoundError")'), "FileNotFoundError\n"),
    (in_work('with open("run.log", "w", encoding="utf-8") as f:\n    f.write("ok\\n错误：磁盘满\\nok\\n又一个错误\\n")\nwith open("run.log", encoding="utf-8") as f:\n    count = 0\n    for line in f:\n        if "错误" in line:\n            count = count + 1\nprint(count)'), "2\n"),
    (in_work('import json\nwith open("data.json", "w", encoding="utf-8") as f:\n    json.dump({"name": "小明", "scores": [90, 85]}, f, ensure_ascii=False)\nwith open("data.json", encoding="utf-8") as f:\n    data = json.load(f)\nprint(data["scores"][0])\nwith open("data.json", encoding="utf-8") as f:\n    print("小明" in f.read())'), "90\nTrue\n"),
    (json.dumps("小"), '"\\u5c0f"'), (json.dumps([1, "a", True]), '[1, "a", true]'), (json.loads(json.dumps((1, 2))), [1, 2]),
    # exceptions
    (err('int("abc")'), "ValueError: invalid literal for int() with base 10: 'abc'"), (err('int("")').split(":")[0], "ValueError"),
    (in_work('try:\n    open("无.txt")\nexcept FileNotFoundError:\n    print("F")'), "F\n"), (raises("10 / 0", ZeroDivisionError), True), (raises("[1][3]", IndexError), True),
    (out('total = 0\nfor s in ["3", "x", "5"]:\n    try:\n        total = total + int(s)\n    except ValueError:\n        print("跳过", s)\nprint(total)'), "跳过 x\n8\n"),
    (out('total = 0\nfor s in ["10", "", "2", "a"]:\n    try:\n        total = total + int(s)\n    except ValueError:\n        total = total - 1\nprint(total)'), "10\n"),
    (out('try:\n    int("abc")\nexcept ValueError as e:\n    print(e)'), "invalid literal for int() with base 10: 'abc'\n"),
    (out('try:\n    x = 1 / 0\n    print("a")\nexcept ZeroDivisionError:\n    print("b")\nelse:\n    print("c")'), "b\n"),
    (out('try:\n    x = 1 / 1\nexcept ZeroDivisionError:\n    print("b")\nelse:\n    print("c")'), "c\n"),
    (raises('try:\n    print([1, 2][5])\nexcept ValueError:\n    print("出错了")', IndexError), True),
    (err('def check_age(a):\n    if a < 0:\n        raise ValueError("年龄不能是负数")\n    return a\ncheck_age(-1)'), "ValueError: 年龄不能是负数"),
    (out('def average(xs):\n    if not xs:\n        raise ValueError("空列表没有平均数")\n    return sum(xs) / len(xs)\nassert average([2, 4, 6]) == 4\nassert average([5]) == 5\ntry:\n    average([])\n    assert False, "应该报 ValueError"\nexcept ValueError:\n    pass\nprint("ok")'), "ok\n"),
    # cleanup
    (out('try:\n    try:\n        print("a")\n        x = 1 / 0\n    finally:\n        print("b")\nexcept ZeroDivisionError:\n    print("ZeroDivisionError")'), "a\nb\nZeroDivisionError\n"),
    (out('def f():\n    try:\n        return "try"\n    finally:\n        print("finally")\n\nprint(f())'), "finally\ntry\n"),
    (in_work('try:\n    with open("a.txt", "w", encoding="utf-8") as f:\n        1 / 0\nexcept ZeroDivisionError:\n    pass\nprint(f.closed)'), "True\n"),
    (out(PAY + 'try:\n    pay(50, 80)\nexcept NotEnoughMoney as e:\n    print("付不了：", e)'), "付不了： 还差 30 元\n"), (out(PAY + 'print(pay(80, 50))'), "30\n"),
    ("The above exception was the direct cause of the following exception" in files_run({"c.py": 'text = "abc"\ntry:\n    port = int(text)\nexcept ValueError as e:\n    raise RuntimeError("配置里的端口不是数字") from e\n'}, "c.py")[1], True),
    (all(w in files_run({"c.py": 'try:\n    int("abc")\nexcept ValueError as e:\n    raise RuntimeError("x") from e\n'}, "c.py")[1] for w in ["ValueError", "RuntimeError"]), True),
    # call-stack
    (files_run({"report.py": REPORT}, "report.py")[1].replace('"' + os.path.join(WORK, "report.py") + '"', '"report.py"'), TB),
    (stack_at_first(SQ, "square"), ["<module>", "sum_squares", "square"]), (out(SQ), "25\n"),
    # boss (added)
    ("Python"[1:-1], "ytho"), (len({1, 2, 3} | {3, 4, 5}), 5), (sum([x * x for x in range(4)]), 14),
    (out('count = 0\nfor s in ["7", "seven", "0", "3.5"]:\n    try:\n        int(s)\n        count = count + 1\n    except ValueError:\n        pass\nprint(count)'), "2\n"),
    (raises('counts = {}\nw = "a"\ncounts[w] = counts[w] + 1', KeyError), True),
]
shutil.rmtree(WORK, ignore_errors=True)

bad = [(i, got, want) for i, (got, want) in enumerate(checks) if got != want]
for i, got, want in bad:
    print(f"#{i}: got {got!r}, want {want!r}")
print(f"{len(checks) - len(bad)}/{len(checks)} claims hold")
raise SystemExit(1 if bad else 0)
