from heapq import heappush, heappop
from itertools import accumulate


def shortest_path(n, edges, src, dst):
    if src == dst:
        return 0
    deg = [0] * n
    for u, v, w in edges:
        if u != v:
            deg[u] += 1
            deg[v] += 1
    off = [0, *accumulate(deg)]
    nbr = [0] * off[n]
    wgt = [0] * off[n]
    cur = off[:n]
    for u, v, w in edges:
        if u != v:
            p = cur[u]; nbr[p] = v; wgt[p] = w; cur[u] = p + 1
            q = cur[v]; nbr[q] = u; wgt[q] = w; cur[v] = q + 1
    INF = float("inf")
    dist = [INF] * n
    dist[src] = 0
    pq = [src]
    while pq:
        x = heappop(pq)
        d = x // n
        u = x - d * n
        if u == dst:
            return d
        if d > dist[u]:
            continue
        for p in range(off[u], off[u + 1]):
            nd = d + wgt[p]
            v = nbr[p]
            if nd < dist[v]:
                dist[v] = nd
                heappush(pq, nd * n + v)
    return -1
