"""HIDDEN suite for train/01_lru-cache. Never expose to agents.

A case here is a SEQUENCE of operations (LRU is stateful), shape:
    {"capacity": <int>, "ops": [("put", key, value) | ("get", key), ...]}

The "expected output" is the list of return values per op (put -> None, get -> int).
The candidate's `put` return value is ignored (normalized to None) so any convention works.

The reference oracle uses collections.OrderedDict, the well-known correct LRU impl.
"""

import random
from collections import OrderedDict


# --- reference oracle ----------------------------------------------------------
class _Ref:
    def __init__(self, capacity):
        self.cap = capacity
        self.od = OrderedDict()

    def get(self, key):
        if key not in self.od:
            return -1
        self.od.move_to_end(key)
        return self.od[key]

    def put(self, key, value):
        if key in self.od:
            self.od.move_to_end(key)
        self.od[key] = value
        if len(self.od) > self.cap:
            self.od.popitem(last=False)


def _replay(cache, ops):
    """Replay an op sequence on any cache-like object; return list of results."""
    out = []
    for op in ops:
        if op[0] == "put":
            cache.put(op[1], op[2])
            out.append(None)
        elif op[0] == "get":
            out.append(cache.get(op[1]))
        else:
            raise ValueError(f"unknown op: {op[0]}")
    return out


def reference(case):
    return _replay(_Ref(case["capacity"]), case["ops"])


def run(candidate, case):
    # The candidate must expose a class named LRUCache(capacity).
    instance = candidate.LRUCache(case["capacity"])
    return _replay(instance, case["ops"])


# --- hidden inputs -------------------------------------------------------------
def _stress(capacity, n, key_range, seed):
    """Deterministic mixed-op sequence for runtime/memory measurement."""
    rng = random.Random(seed)
    ops = []
    for _ in range(n):
        if rng.random() < 0.6:
            ops.append(("put", rng.randint(0, key_range - 1), rng.randint(0, 1000)))
        else:
            ops.append(("get", rng.randint(0, key_range - 1)))
    return ops


CASES = [
    # 1. Spec example
    {"capacity": 2, "ops": [("put", 1, 1), ("put", 2, 2), ("get", 1), ("put", 3, 3), ("get", 2)]},
    # 2. Capacity-1 cache (every put evicts)
    {"capacity": 1, "ops": [("put", 1, 1), ("get", 1), ("put", 2, 2), ("get", 1), ("get", 2)]},
    # 3. `get` refreshes recency (1 stays because we got it, 2 gets evicted)
    {"capacity": 2, "ops": [("put", 1, 1), ("put", 2, 2), ("get", 1),
                            ("put", 3, 3), ("get", 2), ("get", 1), ("get", 3)]},
    # 4. `put` to existing key updates value AND refreshes recency (no eviction)
    {"capacity": 2, "ops": [("put", 1, 1), ("put", 2, 2), ("put", 1, 10),
                            ("put", 3, 3), ("get", 2), ("get", 1), ("get", 3)]},
    # 5. `get` on missing key returns -1; cache stays valid
    {"capacity": 3, "ops": [("get", 5), ("put", 1, 1), ("get", 2)]},
    # 6. Repeated `get` keeps refreshing recency
    {"capacity": 2, "ops": [("put", 1, 1), ("put", 2, 2), ("get", 1), ("get", 1),
                            ("put", 3, 3), ("get", 2)]},
    # 7. Update on a capacity-1 cache
    {"capacity": 1, "ops": [("put", 1, 1), ("put", 1, 2), ("get", 1)]},
    # 8. Fill exactly, then one more put evicts the oldest
    {"capacity": 3, "ops": [("put", 1, 1), ("put", 2, 2), ("put", 3, 3), ("put", 4, 4),
                            ("get", 1), ("get", 2), ("get", 3), ("get", 4)]},
    # 9. Small deterministic stress (kept for an extra correctness check)
    {"capacity": 100, "ops": _stress(capacity=100, n=600, key_range=200, seed=42)},
    # 10-11. LARGE stress: a big resident cache (~50k entries) under heavy churn makes the
    #        cache-structure overhead (dict vs OrderedDict vs hand-rolled linked list) a real
    #        peak-memory difference, and the per-op cost a real runtime difference. The output
    #        list is identical across solutions, so it only shifts the floor - the spread comes
    #        from the cache representation.
    {"capacity": 50000, "ops": _stress(capacity=50000, n=300000, key_range=120000, seed=7)},
    {"capacity": 50000, "ops": _stress(capacity=50000, n=300000, key_range=120000, seed=8)},
]
