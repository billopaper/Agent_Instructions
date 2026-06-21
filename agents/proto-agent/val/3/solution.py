import heapq
from array import array


def shortest_path(n, edges, src, dst):
    if src == dst: return 0
    head = [0] * (n + 1)
    for u, v, w in edges:
        if u != v: head[u + 1] += 1; head[v + 1] += 1
    for i in range(n): head[i + 1] += head[i]
    adj = array('q', bytes(8 * head[n])); pos = head[:]
    for u, v, w in edges:
        if u != v: p = pos[u]; adj[p] = w * n + v; pos[u] = p + 1; q = pos[v]; adj[q] = w * n + u; pos[v] = q + 1
    dist = [-1] * n; dist[src] = 0; pq = [src]
    while pq:
        d, u = divmod(heapq.heappop(pq), n)
        if d > dist[u]: continue
        if u == dst: return d
        for i in range(head[u], head[u + 1]):
            w, v = divmod(adj[i], n); nd = d + w
            if dist[v] < 0 or nd < dist[v]:
                dist[v] = nd; heapq.heappush(pq, nd * n + v)
    return -1
