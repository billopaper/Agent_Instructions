"""HIDDEN suite for validation/weighted-shortest-path. Never expose to agents.

Entry point graded: candidate.shortest_path(n, edges, src, dst) -> int (or -1).

`edges` is passed as an immutable tuple of (u, v, w) tuples, so a candidate cannot
corrupt the shared case across the grader's repeat measurements. The large cases are
built once at import (before the grader starts tracemalloc), so the measured peak
memory reflects the CANDIDATE's own working set (adjacency / distances / frontier),
not the input - which is what makes peak memory a real, discriminating metric here.
"""
import heapq
import random


def _dijkstra(n, edges, src, dst):
    if src == dst:
        return 0
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        if u == v:
            continue
        adj[u].append((v, w))
        adj[v].append((u, w))
    INF = float("inf")
    dist = [INF] * n
    dist[src] = 0
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        if u == dst:
            return d
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist[dst] if dist[dst] != INF else -1


def reference(case):
    """Trusted oracle."""
    return _dijkstra(*case)


def run(candidate, case):
    """Call adapter."""
    n, edges, src, dst = case
    return candidate.shortest_path(n, edges, src, dst)


# ---- hidden case construction -------------------------------------------------

def _connected(n, m, seed, wmax=100):
    """A connected weighted graph on 0..n-1 (random spanning path + extra edges)."""
    rng = random.Random(seed)
    edges = []
    perm = list(range(n))
    rng.shuffle(perm)
    for i in range(n - 1):                       # spanning path -> whole graph connected
        edges.append((perm[i], perm[i + 1], rng.randint(1, wmax)))
    for _ in range(max(0, m - (n - 1))):         # extra edges (may multi-edge / self-loop)
        edges.append((rng.randrange(n), rng.randrange(n), rng.randint(1, wmax)))
    return tuple(edges)


def _two_components(n, m, seed, wmax=100):
    """Two internally-connected halves with NO bridge -> 0 cannot reach n-1 (-> -1)."""
    rng = random.Random(seed)
    half = n // 2
    edges = []
    a = list(range(half)); rng.shuffle(a)
    for i in range(len(a) - 1):
        edges.append((a[i], a[i + 1], rng.randint(1, wmax)))
    b = list(range(half, n)); rng.shuffle(b)
    for i in range(len(b) - 1):
        edges.append((b[i], b[i + 1], rng.randint(1, wmax)))
    for _ in range(m):                           # extra edges stay within a component
        if rng.random() < 0.5:
            edges.append((rng.randrange(half), rng.randrange(half), rng.randint(1, wmax)))
        else:
            edges.append((rng.randrange(half, n), rng.randrange(half, n), rng.randint(1, wmax)))
    return tuple(edges)


CASES = (
    # --- small, hand-checkable / edge cases (correctness) ---
    (5, ((0, 1, 4), (0, 2, 1), (2, 1, 1), (1, 3, 1), (3, 4, 3)), 0, 4),     # 7
    (3, ((0, 1, 2),), 0, 2),                                                # -1 (unreachable)
    (1, (), 0, 0),                                                          # 0 (single node)
    (2, (), 0, 1),                                                          # -1 (no edges)
    (4, ((0, 1, 1), (1, 2, 1)), 2, 2),                                      # 0 (src == dst)
    (2, ((0, 1, 5), (0, 1, 2), (0, 1, 9)), 0, 1),                           # 2 (multi-edge min)
    (3, ((0, 0, 1), (0, 1, 3), (1, 2, 4)), 0, 2),                           # 7 (self-loop ignored)
    (6, ((0, 1, 7), (0, 2, 9), (0, 5, 14), (1, 2, 10), (1, 3, 15),
         (2, 3, 11), (2, 5, 2), (3, 4, 6), (4, 5, 9)), 0, 4),              # classic (=20)
    # --- medium ---
    (300, _connected(300, 1200, 11), 0, 299),
    # --- large (scale makes runtime AND peak memory real, discriminating metrics, and
    #     pushes per-run relative noise below the runtime tolerance band) ---
    (20000, _connected(20000, 100000, 101), 0, 19999),
    (20000, _connected(20000, 100000, 102), 0, 19999),
    (30000, _connected(30000, 150000, 103), 0, 29999),
    (20000, _two_components(20000, 80000, 104), 0, 19999),                  # -1 at scale
)
