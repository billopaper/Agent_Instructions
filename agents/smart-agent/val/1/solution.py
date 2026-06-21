from heapq import heappush, heappop
from array import array


def shortest_path(n, edges, src, dst):
    if src == dst: return 0
    h = array('i', bytes(4 * (n + 1)))
    for u, v, w in edges:
        if u != v: h[u + 1] += 1; h[v + 1] += 1
    for i in range(n): h[i + 1] += h[i]
    e = h[n]; nb = array('i', bytes(4 * e)); wg = array('i', bytes(4 * e)); p = array('i', h[:n])
    for u, v, w in edges:
        if u != v: a = p[u]; nb[a] = v; wg[a] = w; p[u] = a + 1; b = p[v]; nb[b] = u; wg[b] = w; p[v] = b + 1
    INF = float('inf'); dist = [INF] * n; dist[src] = 0; pq = [src]
    while pq:
        d, u = divmod(heappop(pq), n)
        if d != dist[u]: continue
        if u == dst: return d
        for v, w in zip(nb[h[u]:h[u + 1]].tolist(), wg[h[u]:h[u + 1]].tolist()):
            nd = d + w
            if nd < dist[v]: dist[v] = nd; heappush(pq, nd * n + v)
    return -1
