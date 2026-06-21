import heapq


def shortest_path(n, edges, src, dst):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        if u != v: adj[u].append((w, v)); adj[v].append((w, u))
    INF = 1 << 62; dist = [INF] * n; dist[src] = 0; pq = [src]
    while pq:
        x = heapq.heappop(pq); d, u = divmod(x, n)
        if u == dst: return d
        if d > dist[u]: continue
        for w, v in adj[u]:
            if (nd := d + w) < dist[v]: dist[v] = nd; heapq.heappush(pq, nd * n + v)
    return -1
