"""Verify the Web course's exact Flask, HTML and JavaScript examples.

Install Flask in the active environment, or with
python -m pip install --target temp/p-5-1-verify/libs Flask.
Pass --browser to exercise the page and React example in the project's Edge.
For that mode, install React and React DOM under temp/p-5-1-verify with npm.
"""

from contextlib import contextmanager
from http import HTTPStatus
import json
from pathlib import Path
from runpy import run_path
import subprocess
import sys
from tempfile import TemporaryDirectory
from threading import Thread


ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / "temp/p-5-1-verify"
if (WORK / "libs").is_dir():
    sys.path.insert(0, str(WORK / "libs"))

from werkzeug.serving import make_server


def node(source, *args, stdin=None):
    return subprocess.run(
        ["node", "--input-type=module", "-e", source, *map(str, args)],
        cwd=ROOT, input=stdin, check=True, text=True, encoding="utf-8",
        capture_output=False if stdin else True,
    ).stdout


def lesson_examples():
    return json.loads(node("""
      import fs from 'node:fs';
      import {load} from 'js-yaml';
      const pack = load(fs.readFileSync('data/content/P.5.1.yaml', 'utf8'));
      const snippets = {};
      for (const lesson of pack.lessons) {
        snippets[lesson.id] = Object.fromEntries(lesson.flow.flatMap(({card}) =>
          card ? [card.body, ...card.reveal?.map(step => step.body) ?? []] : []
        ).flatMap(body =>
          [...body.matchAll(/```(\\w+)\\n([\\s\\S]+?)```/g)].map(([, language, code]) => [language, code])
        ));
      }
      console.log(JSON.stringify(snippets));
    """))


@contextmanager
def serve(app):
    server = make_server("127.0.0.1", 0, app)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        thread.join()
        server.server_close()


def check_protocol_and_math():
    assert [s.value for s in (
        HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.NO_CONTENT, HTTPStatus.MOVED_PERMANENTLY,
        HTTPStatus.NOT_MODIFIED, HTTPStatus.BAD_REQUEST, HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN,
        HTTPStatus.NOT_FOUND, HTTPStatus.INTERNAL_SERVER_ERROR,
    )] == [200, 201, 204, 301, 304, 400, 401, 403, 404, 500]
    assert 100 + 2 * 10 + 2 * 2 == 124
    assert 80 + 2 * 8 + 2 * 1 == 98


def check_server(app):
    with app.test_client() as client:
        reply = client.get("/", buffered=True)
        assert reply.status_code == 200 and b'<label for="name">' in reply.data
        for value in ("Mei & Lin", "<em>Mei</em>", "梅 🌱", "名" * 40):
            reply = client.get("/api/greet", query_string={"name": f" {value} "})
            assert reply.status_code == 200 and reply.is_json
            assert reply.json == {"message": f"你好，{value}"}
        for values in ({}, {"name": "  "}, {"name": "名" * 41}):
            reply = client.get("/api/greet", query_string=values)
            assert reply.status_code == 400 and reply.json == {"code": "invalid_name"}
        reply = client.get("/greet.js", buffered=True)
        assert reply.status_code == 200 and b"URLSearchParams" in reply.data
        cached = client.get("/greet.js", headers={"If-None-Match": reply.headers["ETag"]}, buffered=True)
        assert cached.status_code == 304 and not cached.data
        assert client.post("/api/greet").status_code in (404, 405)


def check_javascript(snippets):
    source = snippets["javascript"]["javascript"]
    assert node(source).strip() == "你好，Mei"
    node("""
      import assert from 'node:assert/strict';
      const url = new URL('https://learn.example/lessons?id=3');
      assert.deepEqual([url.protocol, url.hostname, url.pathname, url.searchParams.get('id')],
        ['https:', 'learn.example', '/lessons', '3']);
      assert.equal(new URL('https://site.example:443/help').origin, 'https://site.example');
      assert.notEqual(new URL('https://site.example:8443/help').origin, 'https://site.example');
      assert.notEqual(new URL('https://api.site.example/help').origin, 'https://site.example');
      assert.equal(new URLSearchParams({name: 'Mei & Lin'}).toString(), 'name=Mei+%26+Lin');
    """)


def check_browser(app, snippets, public):
    (public / "counter.html").write_text(
        '<!doctype html><div id="root"></div><script src="/counter.js" defer></script>',
        encoding="utf-8",
    )
    with serve(app) as origin:
        node("""
          import assert from 'node:assert/strict';
          import fs from 'node:fs';
          import path from 'node:path';
          import {build} from 'esbuild';
          import {launchEdge} from './scripts/lib/edge.mjs';

          const [origin, publicDir] = process.argv.slice(1);
          const counter = fs.readFileSync(0, 'utf8');
          await build({
            stdin: {contents: counter + `
              import {createRoot} from "react-dom/client";
              createRoot(document.getElementById("root")).render(
                <><Counter label="点赞" /><Counter label="收藏" /></>
              );`, loader: 'jsx', resolveDir: path.join(process.cwd(), 'temp/p-5-1-verify')},
            bundle: true, jsx: 'automatic', outfile: path.join(publicDir, 'counter.js'),
          });

          const browser = await launchEdge();
          try {
            const page = await browser.newPage({viewport: {width: 360, height: 780}});
            const errors = [];
            page.on('pageerror', error => errors.push(error.message));
            await page.goto(origin);
            const name = page.getByRole('textbox', {name: '你的名字'});
            const status = page.getByRole('status');
            const checkStatus = async expected => {
              await status.filter({hasText: expected}).waitFor();
              assert.equal(await status.innerText(), expected);
            };
            await page.keyboard.press('Tab');
            assert(await name.evaluate(el => el === document.activeElement));
            await name.fill('Mei & Lin');
            await page.keyboard.press('Enter');
            await checkStatus('你好，Mei & Lin');
            assert.equal(page.url(), origin + '/');
            await name.fill('<em>Mei</em>');
            await page.getByRole('button', {name: '问好'}).click();
            await checkStatus('你好，<em>Mei</em>');
            assert.equal(await status.locator('em').count(), 0);
            await name.fill('  ');
            await name.press('Enter');
            await checkStatus('没有取到问候，请检查输入后重试');
            assert(await page.getByRole('button', {name: '问好'}).isEnabled());
            await name.fill('梅');
            await name.press('Enter');
            await checkStatus('你好，梅');

            const measured = await page.evaluate(() => {
              const el = document.createElement('div');
              document.body.append(el);
              el.style.cssText = 'width:100px;padding:0 10px;border:2px solid;box-sizing:content-box';
              const first = el.getBoundingClientRect().width;
              el.style.cssText = 'width:80px;padding:0 8px;border:1px solid;box-sizing:content-box';
              return [first, el.getBoundingClientRect().width];
            });
            assert.deepEqual(measured, [124, 98]);

            await page.goto(origin + '/counter.html');
            await page.getByRole('button', {name: '点赞 0'}).click();
            assert.equal(await page.getByRole('button', {name: '点赞 1'}).count(), 1);
            assert.equal(await page.getByRole('button', {name: '收藏 0'}).count(), 1);
            assert.deepEqual(errors, []);
          } finally {
            await browser.close();
          }
        """, origin, public, stdin=snippets["react"]["jsx"])


WORK.mkdir(parents=True, exist_ok=True)
snippets = lesson_examples()
with TemporaryDirectory(dir=WORK, prefix="example-") as directory:
    root = Path(directory)
    public = root / "public"
    public.mkdir()
    (public / "index.html").write_text(snippets["dom"]["html"], encoding="utf-8")
    (public / "greet.js").write_text(snippets["fetch"]["javascript"] + snippets["dom"]["javascript"], encoding="utf-8")
    source = root / "app.py"
    source.write_text(snippets["greet-server"]["python"], encoding="utf-8")
    app = run_path(str(source))["app"]
    check_protocol_and_math()
    check_javascript(snippets)
    check_server(app)
    if "--browser" in sys.argv:
        check_browser(app, snippets, public)
print("P.5.1: HTTP examples, CSS widths, JavaScript and the Flask endpoint verified"
      + (" in Edge with the keyboard and React examples" if "--browser" in sys.argv else ""))
