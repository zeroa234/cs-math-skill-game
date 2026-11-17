"""Checks every numerical, protocol, routing, congestion, Base64, and socket claim in data/content/C.3.2.yaml."""
import base64
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction as F
from heapq import heappop, heappush
from ipaddress import ip_address, ip_network
from socket import SHUT_WR, create_connection, create_server

checks = []
add = lambda got, want, what="": checks.append((got, want, what))

# ------------------------------------------------------------------------ layers-perf
add((F(100_000, 200_000_000) * 1000, F(1000 * 8, 10_000_000) * 1000), (F(1, 2), F(4, 5)),
    "100km @ 10Mbps, 1000B: 0.5ms prop + 0.8ms tx")
add(F(100_000, 200_000_000) * 1000 + F(1000 * 8, 10_000_000) * 1000, F(13, 10),
    "100km @ 10Mbps total latency = 1.3 ms")
add(F(300_000, 200_000_000) * 1000, F(3, 2),
    "delay-prop-only: 300km propagation delay = 1.5 ms")
add(F(200_000, 200_000_000) * 1000 + F(2500 * 8, 20_000_000) * 1000, F(2),
    "delay-calc: 200km @ 20Mbps, 2500B = 2 ms")
add(F(1_500_000) * F(45, 1000), F(67_500), "textbook BDP: 1.5Mbps * 45ms = 67500 bits")
add(F(10_000_000) * F(80, 1000) / 8 / 1000, F(100), "bdp-calc: 10Mbps * 80ms = 100 KB")
add(F(40_000_000) * F(50, 1000) / 8 / 1000, F(250), "boss-bdp: 40Mbps * 50ms = 250 KB")

# ------------------------------------------------------------------------ encoding-framing
add(F(80) * F(5, 4), F(100), "encoding-eff: 80 Mbps user data over 4B/5B = 100 Mbps line rate")

def bit_stuff(bits):
    out, ones = [], 0
    for ch in bits:
        out.append(ch)
        if ch == "1":
            ones += 1
            if ones == 5:
                out.append("0")
                ones = 0
        else:
            ones = 0
    return "".join(out)

def bit_destuff(bits):
    out, ones, skip = [], 0, False
    for ch in bits:
        if skip:
            assert ch == "0"
            skip = False
            continue
        out.append(ch)
        if ch == "1":
            ones += 1
            if ones == 5:
                skip = True
                ones = 0
        else:
            ones = 0
    return "".join(out)

s1 = bit_stuff("01111110111110")
add(s1, "0111110101111100", "HDLC bit stuffing worked example")
add(bit_destuff(s1), "01111110111110", "HDLC bit destuffing round-trip")
s2 = bit_stuff("01111101")
add(s2, "011111001", "bit-stuff item: 01111101 -> 011111001")
add(bit_destuff(s2), "01111101", "bit-stuff item round-trip")
s3 = bit_stuff("1111110")
add(s3, "11111010", "bit-stuff-half item: 1111110 -> 11111010")
add(bit_destuff(s3), "1111110", "bit-stuff-half item round-trip")

# ------------------------------------------------------------------------ error-detection
def ones_comp_checksum(words):
    s = sum(words)
    while s >> 16:
        s = (s & 0xFFFF) + (s >> 16)
    return (~s) & 0xFFFF

add(ones_comp_checksum([0x1234, 0xABCD]), 0x41FE, "checksum worked example 1")
add(ones_comp_checksum([0x1234, 0xABCD, 0x41FE]), 0, "checksum verify worked example 1")
add(ones_comp_checksum([0x1235, 0xABCC, 0x41FE]), 0, "compensating +1/-1 errors cancel in checksum")
add(ones_comp_checksum([0xFF00, 0x0200]), 0xFEFE, "checksum worked example 2 with end-around carry")
add(ones_comp_checksum([0xFFFF, 0x0002]), 0xFFFD, "checksum-carry item = 0xFFFD")
add(ones_comp_checksum([0x0001, 0xFFFE]), 0x0000, "checksum-hex item = 0x0000")

def crc_mod2(msg_bits, gen_bits):
    k = len(gen_bits) - 1
    buf = [int(b) for b in msg_bits] + [0] * k
    gen = [int(b) for b in gen_bits]
    for i in range(len(msg_bits)):
        if buf[i] == 1:
            for j in range(len(gen)):
                buf[i + j] ^= gen[j]
    return "".join(str(b) for b in buf[-k:])

def crc_check(tx_bits, gen_bits):
    buf = [int(b) for b in tx_bits]
    gen = [int(b) for b in gen_bits]
    for i in range(len(tx_bits) - len(gen) + 1):
        if buf[i] == 1:
            for j in range(len(gen)):
                buf[i + j] ^= gen[j]
    return "".join(str(b) for b in buf[-(len(gen) - 1):])

add(crc_mod2("10011010", "1101"), "101", "trace-crc: Peterson & Davie M=10011010 G=1101 -> 101")
add(crc_check("10011010101", "1101"), "000", "CRC receiver verifies 10011010101 -> 000")
add(crc_mod2("1001", "1101"), "011", "crc-calc: 1001 mod2/1101 -> 011")
add(crc_check("1001011", "1101"), "000", "crc-calc receiver verifies -> 000")
add(crc_mod2("11010", "1101"), "000", "boss-crc: 11010 mod2/1101 -> 000")

# ------------------------------------------------------------------------ reliable-link
add(round(1024 * 8 / 0.045), 182044, "Stop-and-Wait on 1.5Mbps 45ms RTT ~ 182 kbps")
add(F(1000 * 8, 10_000_000 * F(10, 1000)) * 100, F(8), "stop-wait-util: 8%")

# Sliding window finite sequence check (3-bit: MaxSeqNum=8, 4-bit: MaxSeqNum=16)
add(set(range(0, 4)).isdisjoint({4, 5, 6, 7}), True, "3-bit seq SWS=RWS=4 has zero overlap")
add(set(range(0, 5)).isdisjoint({5, 6, 7, 0, 1}), False, "3-bit seq SWS=RWS=5 overlaps at 0,1")
add(set(range(0, 8)).isdisjoint(set(range(8, 16))), True, "4-bit seq SWS=RWS=8 has zero overlap")
add(set(range(0, 9)).isdisjoint({(8 + 1 + i) % 16 for i in range(9)}), False, "4-bit seq SWS=RWS=9 overlaps")

# ------------------------------------------------------------------------ shared-media
add(64 - 14 - 4 - 10, 36, "eth-min-frame: 36 bytes padding for 10B payload")
add(51.2 * 10, 512.0, "51.2 us at 10 Mbps = 512 bits")
add(len(range(0, 2**3)), 8, "backoff-range: n=3 -> 8 choices")

# ------------------------------------------------------------------------ ip-cidr
# Fragmentation of 1400B packet (20B header + 1380B payload) over MTU 532 (max 512B payload)
payload = 1380
frags = []
off = 0
while payload > 0:
    take = min(512, payload)
    frags.append((off // 8, take))
    off += take
    payload -= take
add(frags, [(0, 512), (64, 512), (128, 356)], "ipv4-frag offsets and sizes")

n1 = ip_network("192.168.10.77/26", strict=False)
add((str(n1.network_address), str(n1.broadcast_address), len(list(n1.hosts()))),
    ("192.168.10.64", "192.168.10.127", 62), "192.168.10.77/26 subnet")
n2 = ip_network("192.168.10.150/26", strict=False)
add((str(n2.network_address), str(n2.broadcast_address), len(list(n2.hosts()))),
    ("192.168.10.128", "192.168.10.191", 62), "192.168.10.150/26 subnet")
n3 = ip_network("192.168.10.200/26", strict=False)
add((str(n3.network_address), str(n3.broadcast_address)),
    ("192.168.10.192", "192.168.10.255"), "192.168.10.200/26 subnet")
add(len(list(ip_network("192.168.10.0/27").hosts())), 30, "/27 has 30 usable hosts")

# ------------------------------------------------------------------------ ipv6-multicast & udp-rpc-rtp
add(2 ** (28 - 23), 32, "mcast-mac-collision: 32 IP multicast groups map to one Ethernet MAC")
add(20 + 8 + 12, 40, "udp-header: 20 + 8 + 12 = 40 bytes")

# ------------------------------------------------------------------------ tcp-reliable
est, dev, sample = F(100), F(10), F(140)
diff = sample - est
est_new = est + F(1, 8) * diff
dev_new = dev + F(1, 8) * (abs(diff) - dev)
to_new = est_new + 4 * dev_new
add((est_new, dev_new, to_new), (F(105), F(55, 4), F(160)), "Jacobson/Karels worked example")
add(F(80) + F(1, 8) * (120 - 80), F(85), "tcp-jacobson-half item = 85 ms")
add(80 + 4 * 15, 140, "tcp-jacobson item = 140 ms")
add(1000 + 400 + 300, 1700, "tcp-ack-byte = 1700")
add(4096 - 1800, 2296, "tcp-flow-ctrl = 2296")

# ------------------------------------------------------------------------ forwarding-lpm
def lpm(dst_str, table):
    dst = ip_address(dst_str)
    matches = [(ip_network(cidr).prefixlen, hop) for cidr, hop in table if dst in ip_network(cidr)]
    return max(matches)

add(lpm("10.1.2.3", [("0.0.0.0/0", "default"), ("10.0.0.0/8", "A"), ("10.1.0.0/16", "B")]),
    (16, "B"), "trace-lpm: 10.1.2.3 -> B (/16)")
add(lpm("192.168.12.50", [("192.168.0.0/16", "1"), ("192.168.12.0/24", "2"), ("192.168.12.128/25", "3"), ("0.0.0.0/0", "4")]),
    (24, "2"), "lpm-practice: 192.168.12.50 -> 口2 (/24)")
add(lpm("172.16.8.42", [("172.16.0.0/16", "1"), ("172.16.8.0/24", "2"), ("172.16.8.0/22", "3"), ("0.0.0.0/0", "4")]),
    (24, "2"), "boss-lpm: 172.16.8.42 -> 口2 (/24)")

# ------------------------------------------------------------------------ link-state & distance-vector
def dijkstra(edges, start):
    adj = {}
    for u, v, w in edges:
        adj.setdefault(u, []).append((v, w))
        adj.setdefault(v, []).append((u, w))
    q = [(0, start, (start,))]
    settled = {}
    order = []
    while q:
        d, u, path = heappop(q)
        if u in settled:
            continue
        settled[u] = (d, path)
        order.append(u)
        for v, w in sorted(adj.get(u, [])):
            if v not in settled:
                heappush(q, (d + w, v, path + (v,)))
    return order, settled

order1, settled1 = dijkstra([("A", "B", 1), ("A", "C", 4), ("B", "C", 2), ("B", "D", 5), ("C", "D", 1)], "A")
add((order1, settled1["C"][0], settled1["D"]), (["A", "B", "C", "D"], 3, (4, ("A", "B", "C", "D"))),
    "spf-sim A-B-C-D Dijkstra")

order2, settled2 = dijkstra([("R1", "R2", 2), ("R1", "R3", 5), ("R2", "R3", 1), ("R2", "R4", 6),
                             ("R3", "R4", 2), ("R3", "R5", 7), ("R4", "R5", 1)], "R1")
add((order2, {k: v[0] for k, v in settled2.items()}),
    (["R1", "R2", "R3", "R4", "R5"], {"R1": 0, "R2": 2, "R3": 3, "R4": 5, "R5": 6}),
    "boss-dijkstra R1-R5")

add(min(2 + 6, 5 + 2), 7, "dv-update: min(2+6, 5+2) = 7")
dB, dC = 1, 2
dB = 999
hist = []
for _ in range(4):
    dB = 1 + dC
    dC = 1 + dB
    hist.append((dB, dC))
add(hist, [(3, 4), (5, 6), (7, 8), (9, 10)], "trace-cti count-to-infinity progression")

# ------------------------------------------------------------------------ queues-aqm & cwnd-aimd
f1_1 = max(0, 0) + 8
f1_2 = max(f1_1, 0) + 4
f2_1 = max(0, 0) + 6
add(sorted([("F1P1", f1_1), ("F1P2", f1_2), ("F2P1", f2_1)], key=lambda x: x[1]),
    [("F2P1", 6), ("F1P1", 8), ("F1P2", 12)], "FQ finish timestamps")
fq_a1 = max(0, 0) + 5
fq_b1 = max(0, 0) + 3
fq_b2 = max(fq_b1, 0) + 4
add(sorted([("A1", fq_a1), ("B1", fq_b1), ("B2", fq_b2)], key=lambda x: x[1]),
    [("B1", 3), ("A1", 5), ("B2", 7)], "fq-finish item order")
add(F(3, 2 + 1 + 3) * 60, F(30), "wfq-share: 3/6 of 60 Mbps = 30 Mbps")

def cwnd_sim(start, ssthresh, rounds):
    c, log = start, []
    for _ in range(rounds):
        log.append(c)
        c = min(c * 2, ssthresh) if c < ssthresh else c + 1
    return log

add(cwnd_sim(1, 8, 6), [1, 2, 4, 8, 9, 10], "cwnd(1, ssthresh=8) 6 RTTs")
add(cwnd_sim(2, 10, 6), [2, 4, 8, 10, 11, 12], "trace-cwnd(2, ssthresh=10) 6 RTTs")
add(cwnd_sim(2, 4, 6), [2, 4, 5, 6, 7, 8], "cwnd-modify(2, ssthresh=4) 6 RTTs -> 8")
add(cwnd_sim(1, 16, 6), [1, 2, 4, 8, 16, 17], "cwnd-round6(1, ssthresh=16) 6 RTTs")
add(min(12, 8) - 3, 5, "cwnd-vs-rwnd: min(12,8)-3 = 5 KB")

a, b = 16, 4
a2, b2 = a // 2 + 5, b // 2 + 5
add(((a + b), (a2 + b2), (a - b) - (a2 - b2), (a2 - b2)), (20, 20, 6, 6), "aimd-fairness gap 12 -> 6 MSS")

# ------------------------------------------------------------------------ sockets-echo & email-snmp
def echo(server):
    conn, _ = server.accept()
    with conn:
        conn.settimeout(3)
        while chunk := conn.recv(2):
            conn.sendall(chunk)

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
            add(b"".join(chunks), b"hello", "loopback TCP socket echo with 2-byte chunks")
        worker.result(timeout=3)

add(base64.b64encode(b"Cat").decode(), "Q2F0", "Base64 'Cat' -> 'Q2F0'")
add(300 * 4 // 3, 400, "base64-size: 300B -> 400B")

# ------------------------------------------------------------------------ report
bad = [(i + 1, what, got, want) for i, (got, want, what) in enumerate(checks) if got != want]
if bad:
    for idx, what, got, want in bad:
        print(f"FAIL #{idx} ({what}): got {got!r}, want {want!r}")
    raise SystemExit(1)
print(f"{len(checks)}/{len(checks)} claims hold")
