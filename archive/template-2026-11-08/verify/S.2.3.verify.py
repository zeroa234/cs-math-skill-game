"""Verify the resource-access example, Android XML and certificate checks."""

from argparse import ArgumentParser
from pathlib import Path
import re
import subprocess
import sys
from tempfile import TemporaryDirectory
from textwrap import dedent
import xml.etree.ElementTree as ET
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[2]
TEXT = (ROOT / "data/content/S.2.3.yaml").read_text(encoding="utf-8")
ANDROID = "{http://schemas.android.com/apk/res/android}"


def blocks(language):
    return [dedent(block) for block in re.findall(
        rf"^ +```{language}\n(.*?)^ +```$", TEXT, re.MULTILINE | re.DOTALL
    )]


def run(command, cwd, expected=0):
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=20)
    if expected == 0:
        assert result.returncode == 0, result.stderr or result.stdout
    else:
        assert result.returncode != 0, result.stdout
    return result.stdout


def check_apk(work, sdk, manifest, policy):
    platform = sdk / "platforms/android-34/android.jar"
    aapt = sdk / "build-tools/34.0.0/aapt2.exe"
    manifest_file = work / "AndroidManifest.xml"
    manifest_file.write_text(manifest, encoding="utf-8")
    res = work / "res/xml"
    res.mkdir(parents=True)
    (res / "network_security_config.xml").write_text(policy, encoding="utf-8")
    run([aapt, "compile", "--dir", "res", "-o", "res.zip"], work)
    run([aapt, "link", "-I", platform, "--manifest", "AndroidManifest.xml",
         "--min-sdk-version", "23", "--target-sdk-version", "34",
         "-o", "lesson.apk", "res.zip"], work)
    with ZipFile(work / "lesson.apk") as apk:
        assert "AndroidManifest.xml" in apk.namelist()
        assert "res/xml/network_security_config.xml" in apk.namelist()
    dump = run([aapt, "dump", "xmltree", "lesson.apk", "--file", "AndroidManifest.xml"], work)
    assert re.search(r"exported.*(?:0x0\b|false)", dump), dump
    print("S.2.3 Android manifest and network policy packaged with aapt2")


def check_certificates(work, openssl):
    run([openssl, "req", "-x509", "-newkey", "rsa:2048", "-nodes",
         "-keyout", "key.pem", "-out", "cert.pem", "-days", "1",
         "-subj", "/CN=lesson.invalid", "-addext", "subjectAltName=DNS:lesson.invalid"], work)
    verify = [openssl, "verify"]
    run([*verify, "-CAfile", "cert.pem", "-verify_hostname", "lesson.invalid", "cert.pem"], work)
    run([*verify, "-CAfile", "cert.pem", "-verify_hostname", "other.invalid", "cert.pem"],
        work, expected=1)
    run([*verify, "-no-CAfile", "-no-CApath", "-no-CAstore", "cert.pem"], work, expected=1)
    print("S.2.3 local certificate trust and name checks passed")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--android-sdk", type=Path)
    parser.add_argument("--openssl")
    args = parser.parse_args()
    manifest, policy = blocks("xml")
    app = ET.fromstring(manifest).find("application")
    assert app.find("activity").get(ANDROID + "exported") == "false"
    assert app.get(ANDROID + "networkSecurityConfig") == "@xml/network_security_config"
    assert ET.fromstring(policy).find("base-config").get("cleartextTrafficPermitted") == "false"

    source, = blocks("python")
    temp = ROOT / "temp"
    temp.mkdir(exist_ok=True)
    with TemporaryDirectory(dir=temp, prefix="s-2-3-verify-") as directory:
        work = Path(directory)
        output = run([sys.executable, "-I", "-c", source], work).splitlines()
        assert output == ["receipt-preview", "None", "None"]
        print("S.2.3 resource allowlist and Android XML checks passed")
        if args.android_sdk:
            check_apk(work, args.android_sdk.resolve(), manifest, policy)
        if args.openssl:
            check_certificates(work, args.openssl)
