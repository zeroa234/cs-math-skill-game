"""Recompute periodic releases, queue overflow and deadline examples."""

from collections import deque


def produce_without_waiting(values, capacity):
    queue = deque()
    dropped = 0
    for value in values:
        if len(queue) == capacity:
            dropped += 1
        else:
            queue.append(value)
    return list(queue), dropped


releases = range(0, 60, 10)
assert releases[3] == 30 and releases[5] == 50
assert produce_without_waiting(range(6), 4) == ([0, 1, 2, 3], 2)
assert 8 - sum((3, 1, 2)) == 2
assert sum((4, 1, 3)) == 8
assert 10 - sum((2, 1, 3)) == 4
assert 4 * 512 + 1024 == 3072 and 6 * 512 + 2048 == 5120
print("H.3.2 task periods, queue overflow and time/space budgets passed")
