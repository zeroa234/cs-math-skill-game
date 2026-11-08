"""Recompute subnetting, path, ACK and window answers, and run a loopback echo."""
from heapq import heappop, heappush
from ipaddress import ip_address, ip_network
from socket import SHUT_WR, create_connection, create_server
from concurrent.futures import ThreadPoolExecutor

subnet = ip_network("192.168.10.77/26", strict=False)
assert str(subnet.network_address) == "192.168.10.64"
assert str(subnet.broadcast_address) == "192.168.10.127"
assert [str(ip) for ip in (subnet[1], subnet[-2])] == [
    "192.168.10.65", "192.168.10.126"
]
assert len(list(subnet.hosts())) == 62
assert len(list(ip_network("192.168.10.0/27").hosts())) == 30
assert str(ip_network("192.168.10.150/26", strict=False).network_address) == "192.168.10.128"
dest = ip_address("10.1.2.3")
prefixes = [ip_network("10.0.0.0/8"), ip_network("10.1.0.0/16")]
assert max((net for net in prefixes if dest in net), key=lambda net: net.prefixlen) == prefixes[1]
assert max(range(50, 60)) + 1 == 60
assert 2000 / 1000 == 2
assert 9 - 6 == 3

links = {
    "A": {"B": 1, "C": 4}, "B": {"A": 1, "C": 2, "D": 5},
    "C": {"A": 4, "B": 2, "D": 1}, "D": {"B": 5, "C": 1},
}
queue = [(0, ("A",))]
settled = {}
while queue:
    cost, route = heappop(queue)
    end = route[-1]
    if end in settled:
        continue
    settled[end] = (cost, route)
    for neighbor, edge_cost in links[end].items():
        if neighbor not in settled:
            heappush(queue, (cost + edge_cost, route + (neighbor,)))
assert list(settled) == list("ABCD")
assert settled["D"] == (4, ("A", "B", "C", "D"))
assert 2 + 3 == 5

def windows(start, threshold, count):
    for _ in range(count):
        yield start
        start = 2 * start if start < threshold else start + 1

assert list(windows(1, 8, 6)) == [1, 2, 4, 8, 9, 10]
assert list(windows(2, 8, 4)) == [2, 4, 8, 9]

def echo(server):
    conn, _ = server.accept()
    with conn:
        conn.settimeout(3)
        while chunk := conn.recv(2):
            conn.sendall(chunk)

# Bind a free loopback port, with deliberately small reads to demonstrate the byte stream.
with create_server(("127.0.0.1", 0)) as server:
    server.settimeout(3)
    with ThreadPoolExecutor(max_workers=1) as pool:
        worker = pool.submit(echo, server)
        with create_connection(server.getsockname(), timeout=3) as client:
            client.sendall(b"hello")
            client.shutdown(SHUT_WR)
            chunks = []
            while chunk := client.recv(2):
                chunks.append(chunk)
            assert b"".join(chunks) == b"hello"
        worker.result(timeout=3)

print("C.3.2: subnets, forwarding, TCP windows, shortest paths and loopback echo verified")
