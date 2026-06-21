import heapq


def shortest_path(n, edges, src, dst):
    if src == dst: return 0
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        if u != v: adj[u].append((v, w)); adj[v].append((u, w))
    INF = float('inf'); dist = [INF] * n; dist[src] = 0; heap = [src]; push = heapq.heappush; pop = heapq.heappop
    while heap:
        d, u = divmod(pop(heap), n)
        if d > dist[u]: continue
        if u == dst: return d
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]: dist[v] = nd; push(heap, nd * n + v)
    return dist[dst] if dist[dst] != INF else -1
