"""Exercise the exact boundary examples locally with PyJWT and MarkupSafe installed."""

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


def examples():
    output = subprocess.check_output(
        ["node", "--input-type=module", "-e", """
          import fs from 'node:fs';
          import {load} from 'js-yaml';
          const pack = load(fs.readFileSync('data/content/S.3.1.yaml', 'utf8'));
          const examples = ['sql-boundary', 'objects', 'jwt'].map(id => {
            const lesson = pack.lessons.find(l => l.id === id);
            const body = lesson.flow.find(s => s.card?.body.includes('```python')).card.body;
            return body.split('```')[1].slice('python\\n'.length);
          });
          console.log(JSON.stringify(examples));
        """], cwd=ROOT, encoding="utf-8",
    )
    definitions = {}
    for snippet in json.loads(output):
        exec(snippet, definitions)
    return definitions


def check_database(definitions):
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
        products = definitions["public_products"]
        assert products(db, "O'Reilly") == [("Book",)]
        assert products(db, "O'Reilly' OR 1=1 --") == []

        read = definitions["read_order"]
        cancel = definitions["cancel_order"]
        assert read(db, 123, "Mei") is None
        assert read(db, 123, "Lin") == (123, 20)
        assert read(db, 124, "Lin") is None
        assert read(db, 124, "Mei") == (124, 30)
        assert read(db, 999, "Mei") is None
        assert cancel(db, 123, "Mei") == 0
        assert cancel(db, 124, "Lin") == 0
        assert cancel(db, 125, "Mei") == 0
        assert cancel(db, 124, "Mei") == 1
        assert cancel(db, 124, "Mei") == 0
        assert db.execute("SELECT id, status FROM Orders ORDER BY id").fetchall() == [
            (123, "pending"), (124, "cancelled"), (125, "shipped"),
        ]


def check_token(verify):
    key = secrets.token_bytes(64)
    now = datetime.now(timezone.utc)
    claims = {
        "iss": "https://issuer.example", "aud": "orders-api", "sub": "Mei",
        "nbf": now - timedelta(minutes=1), "exp": now + timedelta(minutes=10),
    }
    assert verify(jwt.encode(claims, key, algorithm="HS256"), key)["sub"] == "Mei"
    wrong_claims = [
        ({"aud": "another-api"}, jwt.InvalidAudienceError),
        ({"iss": "https://other.example"}, jwt.InvalidIssuerError),
        ({"exp": now - timedelta(seconds=1)}, jwt.ExpiredSignatureError),
        ({"nbf": now + timedelta(minutes=1)}, jwt.ImmatureSignatureError),
    ]
    for changes, error in wrong_claims:
        with TestCase().assertRaises(error):
            verify(jwt.encode(claims | changes, key, algorithm="HS256"), key)
    with TestCase().assertRaises(jwt.MissingRequiredClaimError):
        verify(jwt.encode({k: v for k, v in claims.items() if k != "sub"}, key, algorithm="HS256"), key)
    with TestCase().assertRaises(jwt.InvalidAlgorithmError):
        verify(jwt.encode(claims, "", algorithm="none"), key)
    with TestCase().assertRaises(jwt.InvalidAlgorithmError):
        verify(jwt.encode(claims, key, algorithm="HS512"), key)
    with TestCase().assertRaises(jwt.InvalidSignatureError):
        verify(jwt.encode(claims, secrets.token_bytes(64), algorithm="HS256"), key)


def check_other_boundaries():
    # RFC 7636 Appendix B test vector, with no actual provider or redirect.
    verifier = "dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk"
    challenge = urlsafe_b64encode(sha256(verifier.encode("ascii")).digest()).rstrip(b"=")
    assert challenge == b"E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM"
    assert parse_qs("order=123&order=124") == {"order": ["123", "124"]}
    assert parse_qs(urlencode({"name": "A&B"})) == {"name": ["A&B"]}
    assert ip_address("169.254.169.254").is_link_local
    assert ip_address("127.0.0.1").is_loopback
    assert ip_address("::ffff:127.0.0.1").ipv4_mapped.is_loopback

    class TextExample(HTMLParser):
        tags = ()
        text = ""

        def handle_starttag(self, tag, attrs):
            self.tags += (tag,)

        def handle_data(self, data):
            self.text += data

    sample = "<em>Mei</em>"
    parsed = TextExample()
    parsed.feed(f"<p>{escape(sample)}</p>")
    assert parsed.tags == ("p",) and parsed.text == sample


sample = examples()
check_database(sample)
check_token(sample["verify_access_token"])
check_other_boundaries()
print("S.3.1: SQL binding, two-user order authorization, JWT rejection, PKCE and local boundary examples verified")
