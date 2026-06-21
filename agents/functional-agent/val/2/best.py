from heapq import heappush, heappop
from itertools import accumulate


def shortest_path(n, edges, src, dst):
    if src == dst: return 0
    deg = [0] * n
    for u, v, w in edges:
        if u != v: deg[u] += 1; deg[v] += 1
    head = [0] + list(accumulate(deg))
    nbr = [0] * head[n]; wgt = [0] * head[n]; cur = head[:n]
    for u, v, w in edges:
        if u != v: nbr[cur[u]] = v; wgt[cur[u]] = w; cur[u] += 1; nbr[cur[v]] = u; wgt[cur[v]] = w; cur[v] += 1
    dist = [float("inf")] * n; dist[src] = 0; heap = [(0, src)]
    while heap:
        d, u = heappop(heap)
        if u == dst: return d
        if d > dist[u]: continue
        a = head[u]; b = head[u + 1]
        for v, wt in zip(nbr[a:b], wgt[a:b]):
            nd = d + wt
            if nd < dist[v]: dist[v] = nd; heappush(heap, (nd, v))
    return -1
