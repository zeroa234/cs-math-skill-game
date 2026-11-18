"""Verify every Python code example and numeric/string check in data/content/P.4.3.yaml."""

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import re
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "data/content/P.4.3.yaml"


def extract_fenced(text: str) -> list[str]:
    return [
        dedent(b).strip()
        for b in re.findall(r"^ +```python\n(.*?)^ +```$", text, re.MULTILINE | re.DOTALL)
    ]


def extract_item_code(text: str) -> list[str]:
    return [
        dedent(b).strip()
        for b in re.findall(r"^ +code: \|\n(.*?)\n +lang: python$", text, re.MULTILINE | re.DOTALL)
    ]


def run_py(code: str) -> tuple[str, dict]:
    buf = StringIO()
    ns: dict = {}
    with redirect_stdout(buf):
        exec(compile(code, "<P.4.3>", "exec"), ns, ns)
    return buf.getvalue().strip(), ns


def main() -> None:
    text = PACK.read_text(encoding="utf-8")
    fenced = extract_fenced(text)
    item_codes = extract_item_code(text)
    assert len(fenced) == 14, f"Expected 14 fenced Python blocks, got {len(fenced)}"
    assert len(item_codes) == 7, f"Expected 7 item Python blocks, got {len(item_codes)}"

    # Verify each fenced block by marker
    markers = {
        "OrderLine": "75",
        "Inventory": "10 0",
        "TRANSITIONS": "Shipped",
        "FakeRepo": "total,7",
        "PayAdapter": "1250",
        "MacFactory": "MacBtn WinBtn",
        "RequestBuilder": "('https://api.example', 5, 2)",
        "BracketDecorator": "[HI]",
        "Folder": "35",
        "HtmlFormatter": "<b>7</b>\ntotal,7",
        "PriceAlert": "1 16.0",
        "AddTextCmd": "Hello",
        "Draft": "moved to published | already published",
        "EvalVisitor": "15",
    }
    matched_keys = set()
    for idx, block in enumerate(fenced):
        out, ns = run_py(block)
        hits = [k for k in markers if k in block]
        assert len(hits) == 1, f"Fenced block {idx} matched {hits}"
        k = hits[0]
        matched_keys.add(k)
        assert out == markers[k], f"Block {k}: expected {markers[k]!r}, got {out!r}"

    # Additional exercise-level assertions on fenced namespaces
    # 1. Inventory stock after A commits 4 and B releases 3
    _, inv_ns = run_py(fenced[1])
    inv2 = inv_ns["Inventory"](10)
    assert inv2.reserve(4)
    inv2.commit(4)
    assert inv2.reserve(3)
    inv2.release(3)
    assert inv2.stock == 6

    # 2. State machine illegal Shipped + cancel
    _, sm_ns = run_py(fenced[2])
    st = sm_ns["apply_event"]("Paid", "ship")
    assert st == "Shipped"
    try:
        sm_ns["apply_event"](st, "cancel")
        raise AssertionError("Expected ValueError")
    except ValueError:
        pass

    # 3. Adapter cents(19.99)
    _, ad_ns = run_py(fenced[4])
    assert ad_ns["PayAdapter"](ad_ns["LegacyPay"]()).pay(19.99) == 1999

    # 4. Builder (10, 3) -> 13
    _, bd_ns = run_py(fenced[6])
    r = bd_ns["RequestBuilder"]("https://a").timeout(10).retries(3).build()
    assert r[1] + r[2] == 13

    # 5. Bridge count 4 + 5 = 9 vs 4 * 5 = 20
    assert 4 + 5 == 9 and 4 * 5 == 20

    # 6. Composite tree size = 35
    _, comp_ns = run_py(fenced[8])
    File, Folder = comp_ns["File"], comp_ns["Folder"]
    assert Folder([File(12), Folder([File(8), Folder([File(15)])])]).size() == 35

    # 7. Strategy HtmlFormatter([10,15,5]) == "<b>30</b>" and boss Csv([12,8,5]) == "total,25"
    _, st_ns = run_py(fenced[9])
    RG = st_ns["ReportGenerator"]
    assert RG(st_ns["HtmlFormatter"]()).render([10, 15, 5]) == "<b>30</b>"
    assert RG(st_ns["CsvFormatter"]()).render([12, 8, 5]) == "total,25"

    # 8. Observer 3 price updates -> 2 hits
    _, ob_ns = run_py(fenced[10])
    s = ob_ns["Stock"]("ACME", 10.0)
    alert = ob_ns["PriceAlert"](15.0)
    s.attach(alert)
    for p in (12.0, 16.0, 18.0):
        s.set_price(p)
    assert len(alert.hits) == 2

    # 9. EvalVisitor Add(Add(Num(2), Num(3)), Num(10)) == 15
    _, ev_ns = run_py(fenced[13])
    Num, Add, EvalVisitor = ev_ns["Num"], ev_ns["Add"], ev_ns["EvalVisitor"]
    assert Add(Add(Num(2), Num(3)), Num(10)).accept(EvalVisitor()) == 15

    # Verify all 6 item `code:` snippets
    # 0: Order.add_item
    _, it0 = run_py(item_codes[0])
    o = it0["Order"]()
    o.add_item(12, 2)
    o.add_item(5, 4)
    assert o.total() == 44

    # 1: Account contract
    _, it1 = run_py(item_codes[1])
    acc = it1["Account"](100)
    acc.withdraw(35)
    try:
        acc.withdraw(80)
        raise AssertionError("Expected ValueError")
    except ValueError:
        pass
    assert acc.balance == 65

    # 2: Square/Rectangle LSP
    out2, it2 = run_py(item_codes[2])
    assert out2 == "16"
    s2 = it2["Square"]()
    s2.set_width(7)
    s2.set_height(3)
    assert s2.area() == 9

    # 3: BracketDecorator item
    out3, _ = run_py(item_codes[3])
    assert out3 == "[HI]"

    # 4: AddTextCmd item
    _, it4_cmd = run_py(item_codes[4])
    assert "".join(it4_cmd["doc"]) == "Hello "

    # 5: Guard clause refactoring equivalence
    _, it4 = run_py(item_codes[5])
    class Emp:
        def __init__(self, dead, sep, base):
            self.is_dead = dead
            self.is_separated = sep
            self.base = base
    def pay_refactored(emp):
        if emp.is_dead:
            return 0
        if emp.is_separated:
            return 0
        return emp.base * 12
    for case in [(True, False, 100), (False, True, 100), (False, False, 100)]:
        e = Emp(*case)
        assert it4["pay_amount"](e) == pay_refactored(e)

    # 6: checkout([10, 20, 30], vip=True) == 50
    _, it5 = run_py(item_codes[6])
    assert it5["checkout"]([10, 20, 30], vip=True) == 50

    print(f"P.4.3 verify: {len(fenced)} fenced blocks + {len(item_codes)} item snippets + SOLID/LSP/pattern assertions passed")


if __name__ == "__main__":
    main()
