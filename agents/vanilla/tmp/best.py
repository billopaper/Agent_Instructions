import heapq
from array import array


def shortest_path(n, edges, src, dst):
    off = array('i', bytes(4 * (n + 1)))
    for u, v, w in edges:
        if u != v: off[u + 1] += 1; off[v + 1] += 1
    for i in range(n): off[i + 1] += off[i]
    nbr = array('i', bytes(4 * off[n])); wgt = array('i', bytes(4 * off[n])); pos = array('i', off[:n])
    for u, v, w in edges:
        if u != v:
            p = pos[u]; nbr[p] = v; wgt[p] = w; pos[u] = p + 1; q = pos[v]; nbr[q] = u; wgt[q] = w; pos[v] = q + 1
    INF = 1 << 62; dist = array('q', [INF]) * n; dist[src] = 0; pq = [src]; del pos
    while pq:
        x = heapq.heappop(pq); u = x % n; d = x // n
        if u == dst: return d
        for i in range(off[u], off[u + 1]):
            v = nbr[i]; nd = d + wgt[i]
            if nd < dist[v]: dist[v] = nd; heapq.heappush(pq, nd * n + v)
    return -1
