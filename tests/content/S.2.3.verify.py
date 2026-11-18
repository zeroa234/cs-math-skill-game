"""Verify resource allowlist defense, Android XML policies, and real OpenSSL certificate/hostname checks for S.2.3."""

from __future__ import annotations

import io
import pathlib
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
from contextlib import redirect_stdout
from tempfile import TemporaryDirectory
from textwrap import dedent

ROOT = pathlib.Path(__file__).resolve().parents[2]
PACK_PATH = ROOT / "data" / "content" / "S.2.3.yaml"
ANDROID_NS = "{http://schemas.android.com/apk/res/android}"


def blocks(text: str, lang: str) -> list[str]:
    return [
        dedent(block).strip()
        for block in re.findall(rf"^ +```{re.escape(lang)}\n(.*?)^ +```$", text, re.MULTILINE | re.DOTALL)
    ]


def find_openssl() -> str | None:
    cand = shutil.which("openssl")
    if cand:
        return cand
    conda_ssl = pathlib.Path(r"C:\Users\bmh05\miniconda3\Library\bin\openssl.exe")
    if conda_ssl.exists():
        return str(conda_ssl)
    return None


def verify_allowlist(text: str) -> None:
    py_blocks = blocks(text, "python")
    assert len(py_blocks) == 2, f"Expected 2 python blocks in S.2.3.yaml, got {len(py_blocks)}"

    # Execute card block (prints 3 lines)
    buf = io.StringIO()
    ns: dict = {}
    with redirect_stdout(buf):
        exec(compile(py_blocks[0], "S.2.3_ipc_allowlist.py", "exec"), ns)
    lines = buf.getvalue().strip().splitlines()
    assert lines == ["receipt-preview", "None", "None"], f"Unexpected lines: {lines}"

    # Verify item block resolves identically
    item_ns: dict = {}
    exec(compile(py_blocks[1], "S.2.3_ipc_item.py", "exec"), item_ns)
    resolve = item_ns["resolve"]
    assert resolve("reader", "preview", "receipt") == "receipt-preview"
    assert resolve("stranger", "preview", "receipt") is None
    assert resolve("reader", "preview", "../private") is None
    assert resolve("reader", "delete", "receipt") is None


def verify_android_xml(text: str) -> None:
    xml_blocks = blocks(text, "xml")
    assert len(xml_blocks) == 2, f"Expected 2 xml blocks in S.2.3.yaml, got {len(xml_blocks)}"
    manifest, policy = xml_blocks

    app = ET.fromstring(manifest).find("application")
    assert app is not None
    assert app.get(ANDROID_NS + "networkSecurityConfig") == "@xml/network_security_config"
    activity = app.find("activity")
    assert activity is not None
    assert activity.get(ANDROID_NS + "exported") == "false"

    base_cfg = ET.fromstring(policy).find("base-config")
    assert base_cfg is not None
    assert base_cfg.get("cleartextTrafficPermitted") == "false"


def verify_openssl_tls() -> None:
    openssl = find_openssl()
    assert openssl, "openssl binary not found for real TLS verification"

    temp_root = ROOT / "temp"
    temp_root.mkdir(exist_ok=True)
    with TemporaryDirectory(dir=temp_root, prefix="s-2-3-tls-") as tmp:
        work = pathlib.Path(tmp)
        cnf = work / "req.cnf"
        cnf.write_text(
            "[req]\ndistinguished_name = dn\nprompt = no\n[dn]\nCN = api.example.test\n",
            encoding="utf-8",
        )
        subprocess.run(
            [
                openssl,
                "req",
                "-x509",
                "-config",
                str(cnf),
                "-newkey",
                "rsa:2048",
                "-nodes",
                "-keyout",
                "key.pem",
                "-out",
                "cert.pem",
                "-days",
                "1",
                "-addext",
                "subjectAltName=DNS:api.example.test",
            ],
            cwd=work,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        # Valid CA + matching hostname must pass
        ok = subprocess.run(
            [openssl, "verify", "-CAfile", "cert.pem", "-verify_hostname", "api.example.test", "cert.pem"],
            cwd=work,
            capture_output=True,
            text=True,
        )
        assert ok.returncode == 0, ok.stderr or ok.stdout

        # Valid CA + wrong hostname ("other.invalid") must fail
        mismatch = subprocess.run(
            [openssl, "verify", "-CAfile", "cert.pem", "-verify_hostname", "other.invalid", "cert.pem"],
            cwd=work,
            capture_output=True,
            text=True,
        )
        assert mismatch.returncode != 0, "Expected hostname mismatch to fail verify"

        # Untrusted self-signed cert with no CA trust store must fail
        untrusted = subprocess.run(
            [openssl, "verify", "-no-CAfile", "-no-CApath", "-no-CAstore", "cert.pem"],
            cwd=work,
            capture_output=True,
            text=True,
        )
        assert untrusted.returncode != 0, "Expected untrusted cert without CA to fail verify"


def main() -> None:
    text = PACK_PATH.read_text(encoding="utf-8")
    verify_allowlist(text)
    verify_android_xml(text)
    verify_openssl_tls()
    print("ok — verified resource allowlist, Android XML security config, and OpenSSL X.509/hostname checks in S.2.3.yaml")


if __name__ == "__main__":
    main()
