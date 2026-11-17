"""Verify S.3.1 Web/API security boundary examples locally against data/content/S.3.1.yaml."""

from base64 import urlsafe_b64encode
from contextlib import closing
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from html.parser import HTMLParser
from ipaddress import ip_address
import json
from pathlib import Path
import secrets
import sqlite3
import subprocess
from unittest import TestCase
from urllib.parse import parse_qs, urlencode

import jwt
from markupsafe import escape


ROOT = Path(__file__).resolve().parents[2]


def load_pack_examples():
    script = """
      import fs from 'node:fs';
      import * as yaml from 'js-yaml';
      const pack = yaml.load(fs.readFileSync('data/content/S.3.1.yaml', 'utf8'));
      const snippets = ['sql-boundary', 'objects', 'jwt'].map(id => {
        const lesson = pack.lessons.find(l => l.id === id);
        if (!lesson) throw new Error('missing lesson ' + id);
        const step = lesson.flow.find(s => s.card?.body && s.card.body.includes('```python'));
        if (!step) throw new Error('missing python block in ' + id);
        return step.card.body.split('```python\\n')[1].split('```')[0];
      });
      console.log(JSON.stringify(snippets));
    """
    output = subprocess.check_output(
        ["node", "--input-type=module", "-e", script],
        cwd=ROOT,
        encoding="utf-8",
    )
    ns = {}
    for code in json.loads(output):
        exec(code, ns)
    return ns


def check_sql_and_idor(ns):
    with closing(sqlite3.connect(":memory:")) as db:
        db.executescript("""
            CREATE TABLE Products (name TEXT, brand TEXT, published INTEGER);
            INSERT INTO Products VALUES
                ('Book', 'O''Reilly', 1),
                ('Draft', 'O''Reilly', 0),
                ('Another', 'Other', 1);
            CREATE TABLE Orders (id INTEGER PRIMARY KEY, user_id TEXT, total INTEGER, status TEXT);
            INSERT INTO Orders VALUES
                (123, 'Lin', 20, 'pending'),
                (124, 'Mei', 30, 'pending'),
                (125, 'Mei', 40, 'shipped');
        """)
        public_products = ns["public_products"]
        assert public_products(db, "O'Reilly") == [("Book",)]
        assert public_products(db, "O'Reilly' OR 1=1 --") == []

        read_order = ns["read_order"]
        cancel_order = ns["cancel_order"]
        assert read_order(db, 123, "Mei") is None
        assert read_order(db, 123, "Lin") == (123, 20)
        assert read_order(db, 124, "Lin") is None
        assert read_order(db, 124, "Mei") == (124, 30)
        assert read_order(db, 999, "Mei") is None

        assert cancel_order(db, 123, "Mei") == 0
        assert cancel_order(db, 124, "Lin") == 0
        assert cancel_order(db, 125, "Mei") == 0
        assert cancel_order(db, 124, "Mei") == 1
        assert cancel_order(db, 124, "Mei") == 0
        assert db.execute("SELECT id, status FROM Orders ORDER BY id").fetchall() == [
            (123, "pending"),
            (124, "cancelled"),
            (125, "shipped"),
        ]


def check_jwt(verify_access_token):
    key = secrets.token_bytes(64)
    now = datetime.now(timezone.utc)
    claims = {
        "iss": "https://issuer.example",
        "aud": "orders-api",
        "sub": "Mei",
        "nbf": now - timedelta(minutes=1),
        "exp": now + timedelta(minutes=10),
    }
    valid = jwt.encode(claims, key, algorithm="HS256")
    assert verify_access_token(valid, key)["sub"] == "Mei"

    bad_cases = [
        ({"aud": "other-api"}, jwt.InvalidAudienceError),
        ({"iss": "https://other.example"}, jwt.InvalidIssuerError),
        ({"exp": now - timedelta(seconds=1)}, jwt.ExpiredSignatureError),
        ({"nbf": now + timedelta(minutes=1)}, jwt.ImmatureSignatureError),
    ]
    for patch, err in bad_cases:
        with TestCase().assertRaises(err):
            verify_access_token(jwt.encode(claims | patch, key, algorithm="HS256"), key)

    no_sub = {k: v for k, v in claims.items() if k != "sub"}
    with TestCase().assertRaises(jwt.MissingRequiredClaimError):
        verify_access_token(jwt.encode(no_sub, key, algorithm="HS256"), key)

    with TestCase().assertRaises(jwt.InvalidAlgorithmError):
        verify_access_token(jwt.encode(claims, "", algorithm="none"), key)
    with TestCase().assertRaises(jwt.InvalidAlgorithmError):
        verify_access_token(jwt.encode(claims, key, algorithm="HS512"), key)
    with TestCase().assertRaises(jwt.InvalidSignatureError):
        verify_access_token(jwt.encode(claims, secrets.token_bytes(64), algorithm="HS256"), key)


def check_pkce_hpp_ssrf_xss():
    # RFC 7636 Appendix B test vector
    verifier = "dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk"
    challenge = urlsafe_b64encode(sha256(verifier.encode("ascii")).digest()).rstrip(b"=")
    assert challenge == b"E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM"

    # Parameter pollution & form encoding round-trip
    assert parse_qs("order=123&order=124") == {"order": ["123", "124"]}
    assert parse_qs(urlencode({"name": "A&B"})) == {"name": ["A&B"]}

    # SSRF IP boundary checks (including IPv4-mapped IPv6)
    assert ip_address("169.254.169.254").is_link_local
    assert ip_address("127.0.0.1").is_loopback
    assert ip_address("::ffff:127.0.0.1").ipv4_mapped.is_loopback

    # HTML context escaping
    class TagTextParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.tags = []
            self.text = ""

        def handle_starttag(self, tag, attrs):
            self.tags.append(tag)

        def handle_data(self, data):
            self.text += data

    sample = "<em>Mei</em>"
    parser = TagTextParser()
    parser.feed(f"<p>{escape(sample)}</p>")
    assert parser.tags == ["p"] and parser.text == sample


def main():
    ns = load_pack_examples()
    check_sql_and_idor(ns)
    check_jwt(ns["verify_access_token"])
    check_pkce_hpp_ssrf_xss()
    print("S.3.1 verify: SQL binding, two-user IDOR, PyJWT, RFC7636 PKCE, HPP, SSRF IP, and XSS escape checks passed.")


if __name__ == "__main__":
    main()
