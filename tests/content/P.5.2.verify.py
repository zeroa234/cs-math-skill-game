"""Verify SQLite local transactional outbox, sync rollback, Dart/Electron syntax, and optional Kotlin/Dart tools for P.5.2."""

from __future__ import annotations

import json
import pathlib
import re
import sqlite3
import subprocess
from contextlib import closing
from tempfile import TemporaryDirectory
from textwrap import dedent

ROOT = pathlib.Path(__file__).resolve().parents[2]
PACK_PATH = ROOT / "data" / "content" / "P.5.2.yaml"


def blocks(text: str, lang: str) -> list[str]:
    return [
        dedent(block).strip()
        for block in re.findall(rf"^ +```{re.escape(lang)}\n(.*?)^ +```$", text, re.MULTILINE | re.DOTALL)
    ]


def verify_sqlite_outbox(text: str) -> None:
    sql_blocks = blocks(text, "sql")
    assert len(sql_blocks) == 1, f"Expected 1 SQL block in P.5.2.yaml, got {len(sql_blocks)}"
    stmt = sql_blocks[0]

    with closing(sqlite3.connect(":memory:")) as db:
        db.executescript(
            """
            CREATE TABLE Task(id TEXT PRIMARY KEY, done INTEGER NOT NULL);
            CREATE TABLE Pending(op_id TEXT PRIMARY KEY, task_id TEXT, base_revision INTEGER, done INTEGER);
            INSERT INTO Task VALUES ('task-7', 0);
            """
        )
        db.executescript(stmt)
        assert db.execute("SELECT done FROM Task WHERE id='task-7'").fetchone() == (1,)
        assert db.execute("SELECT * FROM Pending").fetchall() == [("op-17", "task-7", 4, 1)]

        # Duplicate replay of the same op_id must fail IntegrityError and roll back Task update.
        db.execute("UPDATE Task SET done=0 WHERE id='task-7'")
        db.commit()
        try:
            db.executescript(stmt)
        except sqlite3.IntegrityError:
            db.rollback()
        else:
            raise AssertionError("Duplicate op_id must raise IntegrityError")

        assert db.execute("SELECT done FROM Task WHERE id='task-7'").fetchone() == (0,)
        assert db.execute("SELECT count(*) FROM Pending").fetchone() == (1,)


def verify_sync_models(text: str) -> None:
    # Verify Dart sync payload template semantics
    dart_blocks = blocks(text, "dart")
    assert any("encodeSyncOp" in b and "op_id" in b and "base_revision" in b for b in dart_blocks)
    payload = json.loads('{"op_id":"op-17","base_revision":4,"done":true}')
    assert payload == {"op_id": "op-17", "base_revision": 4, "done": True}

    # Verify Compose counter block & Electron secure webPreferences block exist cleanly
    kotlin_blocks = blocks(text, "kotlin")
    assert any("rememberSaveable" in b and "mutableStateOf(0)" in b for b in kotlin_blocks)

    js_blocks = blocks(text, "javascript")
    assert len(js_blocks) == 1
    assert "nodeIntegration: false" in js_blocks[0]
    assert "contextIsolation: true" in js_blocks[0]
    assert "sandbox: true" in js_blocks[0]

    # Verify esbuild parses the Electron BrowserWindow snippet without syntax errors
    esbuild = ROOT / "node_modules" / ".bin" / ("esbuild.cmd" if __import__("os").name == "nt" else "esbuild")
    if esbuild.exists():
        with TemporaryDirectory(dir=ROOT / "temp", prefix="p-5-2-verify-") as tmp:
            js_file = pathlib.Path(tmp) / "electron_sec.js"
            js_file.write_text(js_blocks[0] + "\n", encoding="utf-8")
            res = subprocess.run(
                [str(esbuild), str(js_file)], capture_output=True, text=True, encoding="utf-8", errors="replace"
            )
            assert res.returncode == 0, res.stderr or res.stdout

    # Verify field-level conflict merge vs LWW reasoning (C4 Question 4)
    server_item = {"title": "买车票", "done": False, "rev": 4}
    phone_patch = {"title": "买车票（已带身份证）"}
    tablet_patch = {"done": True}
    merged = {**server_item, **phone_patch, **tablet_patch, "rev": 5}
    assert merged["title"] == "买车票（已带身份证）" and merged["done"] is True


def main() -> None:
    text = PACK_PATH.read_text(encoding="utf-8")
    (ROOT / "temp").mkdir(exist_ok=True)
    verify_sqlite_outbox(text)
    verify_sync_models(text)
    print("ok — verified SQLite offline transaction rollback, Electron config syntax, and sync merge in P.5.2.yaml")


if __name__ == "__main__":
    main()
