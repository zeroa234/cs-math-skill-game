"""Verify D.1.3 consistent hashing, mod-N reshuffling, quorum intersection, 2PC state machine, and cache TTL."""

from itertools import combinations


def ring_owner(key, sorted_nodes, ring_size=100):
    pos = key % ring_size
    for node in sorted_nodes:
        if node >= pos:
            return node
    return sorted_nodes[0]


def check_sharding_and_consistent_hashing():
    # Consistent hashing ring (size 100): nodes (10, 50, 90) -> add node 30 -> (10, 30, 50, 90)
    old_nodes = [10, 50, 90]
    new_nodes = [10, 30, 50, 90]
    moved = {k for k in range(100) if ring_owner(k, old_nodes) != ring_owner(k, new_nodes)}
    assert moved == set(range(11, 31))
    assert all(ring_owner(k, new_nodes) == 30 for k in moved)
    assert len(moved) == 20  # Close to 100 / 4 = 25 average

    # Naive key % N when growing from N=3 to N=4
    naive_moved = [k for k in range(12) if (k % 3) != (k % 4)]
    assert len(naive_moved) == 9
    assert (len(naive_moved) * 1200) // 12 == 900  # 75% of 1200 keys move

    # Uniform hash shares when partitioning K keys across N shards
    assert 1200 // 4 == 300
    assert 1500 // 5 == 300
    assert 2500 // 5 == 500


def check_quorum_intersection():
    # N=3, W=2, R=2 => W+R = 4 > 3 => every write-quorum and read-quorum must intersect
    replicas_3 = {"A", "B", "C"}
    w_sets = [set(c) for c in combinations(replicas_3, 2)]
    r_sets = [set(c) for c in combinations(replicas_3, 2)]
    assert all(w & r for w in w_sets for r in r_sets)

    # N=5, W=3, R=2 => W+R = 5 <= 5 => disjoint counterexample exists (e.g. write {C,D,E}, read {A,B})
    assert set("AB") & set("CDE") == set()


def check_2pc_and_cache_ttl():
    # Simulated 2PC decision transitions: all YES -> COMMIT; any NO -> ABORT; coordinator crash after YES -> UNCERTAIN/BLOCKED
    def two_phase_decision(votes, coord_alive=True):
        if "NO" in votes:
            return "ABORT"
        if not coord_alive:
            return "BLOCKED_HOLDING_LOCKS"
        return "COMMIT"

    assert two_phase_decision(["YES", "YES"]) == "COMMIT"
    assert two_phase_decision(["YES", "NO"]) == "ABORT"
    assert two_phase_decision(["YES", "YES"], coord_alive=False) == "BLOCKED_HOLDING_LOCKS"

    # Simulated TTL + cache-aside flow
    db = {"product:42": '{"id": 42, "price": 99}'}
    cache = {}  # key -> (value, expire_at)
    now = 100

    def get_product(pid, now_t):
        entry = cache.get(pid)
        if entry and entry[1] > now_t:
            return ("HIT", entry[0])
        cache.pop(pid, None)
        val = db[pid]
        cache[pid] = (val, now_t + 60)
        return ("MISS", val)

    assert get_product("product:42", 100)[0] == "MISS"
    assert get_product("product:42", 120)[0] == "HIT"
    assert cache["product:42"][1] - 120 == 40  # Remaining TTL = 40s
    assert get_product("product:42", 160)[0] == "MISS"  # Expired at t=160 -> reloads from DB


if __name__ == "__main__":
    check_sharding_and_consistent_hashing()
    check_quorum_intersection()
    check_2pc_and_cache_ttl()
    print("D.1.3 verify: all consistent hashing, mod-N, quorum, 2PC blocking, and cache TTL checks passed.")
