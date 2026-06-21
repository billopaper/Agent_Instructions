import heapq
from array import array

def shortest_path(n, edges, src, dst):
    if src == dst: return 0
    head = array('i', bytes(4 * (n + 1)))
    for u, v, w in edges:
        if u != v: head[u + 1] += 1; head[v + 1] += 1
    for i in range(n): head[i + 1] += head[i]
    m = head[n]
    nbr = array('i', bytes(4 * m)); wt = array('I', bytes(4 * m)); pos = array('i', head[:n])
    for u, v, w in edges:
        if u != v:
            p = pos[u]; nbr[p] = v; wt[p] = w; pos[u] = p + 1
            p = pos[v]; nbr[p] = u; wt[p] = w; pos[v] = p + 1
    dist = array('q', [1 << 62]) * n; dist[src] = 0; pq = [src]
    while pq:
        key = heapq.heappop(pq); u = key % n; d = key // n
        if u == dst: return d
        if d > dist[u]: continue
        for i in range(head[u], head[u + 1]):
            nd = d + wt[i]; v = nbr[i]
            if nd < dist[v]: dist[v] = nd; heapq.heappush(pq, nd * n + v)
    return -1
