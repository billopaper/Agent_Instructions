from heapq import heappush, heappop
from array import array


def shortest_path(n, edges, src, dst):
    if src == dst:
        return 0
    off = array('i', bytes(4 * (n + 1)))
    for u, v, w in edges:
        if u != v:
            off[u + 1] += 1; off[v + 1] += 1
    for i in range(n):
        off[i + 1] += off[i]
    nbr = array('i', bytes(4 * off[n]))
    wgt = array('i', bytes(4 * off[n]))
    pos = array('i', off[:n])
    for u, v, w in edges:
        if u != v:
            nbr[pos[u]] = v; wgt[pos[u]] = w; pos[u] += 1; nbr[pos[v]] = u; wgt[pos[v]] = w; pos[v] += 1
    dist = array('i', [2 ** 31 - 1]) * n
    dist[src] = 0
    heap = [(0, src)]
    while heap:
        d, u = heappop(heap)
        if u == dst:
            return d
        if d > dist[u]:
            continue
        for i in range(off[u], off[u + 1]):
            v = nbr[i]; nd = d + wgt[i]
            if nd < dist[v]:
                dist[v] = nd
                heappush(heap, (nd, v))
    return -1
