"""Verify lesson calculations and, with --redis SERVER CLI, the Redis example."""

from argparse import ArgumentParser
from bisect import bisect_left
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import re
import shlex
from socket import socket
import subprocess
from tempfile import TemporaryDirectory
from time import monotonic, sleep


ROOT = Path(__file__).resolve().parents[2]


def check_distribution():
    old_nodes = (10, 50, 90)
    new_nodes = (10, 30, 50, 90)

    def owner(nodes, key):
        return nodes[bisect_left(nodes, key) % len(nodes)]

    moved = {key for key in range(100) if owner(old_nodes, key) != owner(new_nodes, key)}
    assert moved == set(range(11, 31))
    assert all(owner(new_nodes, key) == 30 for key in moved)

    # Uniform integer hashes, using one full period of the two modulus functions.
    moves = sum(key % 3 != key % 4 for key in range(12))
    assert Fraction(moves, 12) * 1200 == 900
    # Uniform, exchangeable ring positions give each node the same expected share.
    assert Fraction(1200, 4) == 300
    assert Fraction(1500, 5) == 300
    assert Fraction(2500, 5) == 500


def check_quorums():
    two_of_three = [set(group) for group in combinations("ABC", 2)]
    assert all(read & write for read in two_of_three for write in two_of_three)
    assert set("AB") & set("BC") == {"B"}
    assert set("AB").isdisjoint("CDE")  # a possible read and write for N=5, R=2, W=3


def check_redis(server, client):
    content = (ROOT / "data/content/D.1.3.yaml").read_text(encoding="utf-8")
    block, = re.findall(r"```text\n(.*?)```", content, flags=re.DOTALL)
    write, read, ttl = map(shlex.split, block.strip().splitlines())
    work = ROOT / "temp"
    work.mkdir(exist_ok=True)
    with socket() as local:
        local.bind(("127.0.0.1", 0))
        port = str(local.getsockname()[1])
    with TemporaryDirectory(dir=work, prefix="rd-") as directory:
        with subprocess.Popen(
            [server, "--bind", "127.0.0.1", "--port", port,
             "--save", "", "--appendonly", "no", "--dir", directory],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
        ) as process:
            def execute(*args, check=True):
                return subprocess.run(
                    [client, "-h", "127.0.0.1", "-p", port, "--raw", *args],
                    check=check, capture_output=True, text=True, timeout=3,
                )

            try:
                deadline = monotonic() + 5
                while execute("PING", check=False).stdout.strip() != "PONG":
                    if process.poll() is not None:
                        raise RuntimeError(process.stdout.read())
                    assert monotonic() < deadline, "Redis did not become ready"
                    sleep(0.05)
                assert f"process_id:{process.pid}" in execute("INFO", "server").stdout.splitlines()

                assert execute(*write).stdout.strip() == "OK"
                assert execute(*read).stdout.strip() == '{"user":"Mei"}'
                assert 0 < int(execute(*ttl).stdout) <= 60
                # Observe actual expiry with the same EX command and a shorter duration.
                assert execute(*write[:-1], "1").stdout.strip() == "OK"
                deadline = monotonic() + 4
                while execute(*read).stdout.strip():
                    assert monotonic() < deadline, "Session key did not expire"
                    sleep(0.05)
                assert execute(*ttl).stdout.strip() == "-2"

                assert execute("SET", "product:42", "99", "EX", "60").stdout.strip() == "OK"
                assert execute("DEL", "product:42").stdout.strip() == "1"
                assert execute("GET", "product:42").stdout.strip() == ""
            finally:
                if process.poll() is None:
                    process.terminate()
                    process.wait(timeout=5)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--redis", nargs=2, metavar=("SERVER", "CLI"))
    args = parser.parse_args()
    check_distribution()
    check_quorums()
    print("D.1.3 ring movement and quorum calculations passed")
    if args.redis:
        check_redis(*args.redis)
        print("D.1.3 Redis SET/GET/TTL, expiry and DEL passed")
