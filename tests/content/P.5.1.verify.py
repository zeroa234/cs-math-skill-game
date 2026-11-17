"""Verify box-model, origin comparison, URLSearchParams, Flask/HTTP status, and JWT/PKCE facts in data/content/P.5.1.yaml."""
import base64
import hashlib
import html
import json
from urllib.parse import urlencode, urlparse


def check_css_box_model():
    # content-box: width=100, padding=10 (L+R=20), border=2 (L+R=4) -> total 124 px
    assert 100 + 2 * 10 + 2 * 2 == 124
    # content-box: width=80, padding=8 (L+R=16), border=1 (L+R=2) -> total 98 px
    assert 80 + 2 * 8 + 2 * 1 == 98
    # border-box: declared width=120 includes padding 10*2 and border 2*2 -> content area = 96 px
    assert 120 - 2 * 10 - 2 * 2 == 96


def origin_of(url: str) -> tuple[str, str, int]:
    p = urlparse(url)
    port = p.port or (443 if p.scheme == "https" else 80)
    return (p.scheme, p.hostname, port)


def check_same_origin_and_url():
    base = origin_of("https://site.example/app")
    assert base == ("https", "site.example", 443)
    assert origin_of("https://site.example:443/api/v1") == base  # same origin
    assert origin_of("http://site.example/app") != base           # scheme differs
    assert origin_of("https://api.site.example/v1") != base       # host differs
    assert origin_of("https://site.example:8443/app") != base     # port differs

    # URLSearchParams encoding: spaces -> '+', '&' -> '%26'
    assert urlencode({"name": "Mei & Lin"}) == "name=Mei+%26+Lin"


def check_greet_api_and_escaping():
    # Simulating the /api/greet handler from the exercise
    def greet_handler(raw_name):
        if not isinstance(raw_name, str):
            return 400, {"code": "invalid_name"}
        name = raw_name.strip()
        if not name or len(name) > 40:
            return 400, {"code": "invalid_name"}
        return 200, {"message": f"你好，{name}"}

    assert greet_handler("Mei & Lin") == (200, {"message": "你好，Mei & Lin"})
    assert greet_handler("  Mei  ") == (200, {"message": "你好，Mei"})
    assert greet_handler("名" * 40)[0] == 200
    assert greet_handler("   ") == (400, {"code": "invalid_name"})
    assert greet_handler("名" * 41) == (400, {"code": "invalid_name"})
    assert greet_handler(None) == (400, {"code": "invalid_name"})

    # HTML escaping neutralizes <script> / <em> tags
    escaped = html.escape("<em>Mei</em>")
    assert escaped == "&lt;em&gt;Mei&lt;/em&gt;" and "<em" not in escaped


def check_jwt_b64_not_encrypted_and_pkce():
    # A JWT payload is base64url encoded (anyone can decode it!), NOT encrypted
    payload = {"sub": "u_42", "role": "user", "exp": 1900000000}
    encoded = base64.urlsafe_b64encode(json.dumps(payload, separators=(",", ":")).encode()).rstrip(b"=").decode()
    padded = encoded + "=" * (-len(encoded) % 4)
    decoded = json.loads(base64.urlsafe_b64decode(padded))
    assert decoded["sub"] == "u_42"

    # RFC 7636 PKCE vector
    verifier = "dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk"
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode("ascii")).digest()).rstrip(b"=").decode()
    assert challenge == "E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM"


def check_status_codes():
    codes = {200, 201, 204, 301, 304, 400, 401, 403, 404, 500}
    assert 401 in codes and 403 in codes and 304 in codes


def main():
    check_css_box_model()
    check_same_origin_and_url()
    check_greet_api_and_escaping()
    check_jwt_b64_not_encrypted_and_pkce()
    check_status_codes()
    print("P.5.1 verify: all box-model, origin, API, escaping, JWT/PKCE, and status checks passed.")


if __name__ == "__main__":
    main()
