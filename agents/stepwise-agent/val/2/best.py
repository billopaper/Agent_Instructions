import heapq


def shortest_path(n, edges, src, dst):
    if src == dst:
        return 0
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        if u == v:
            continue
        adj[u].append((v, w))
        adj[v].append((u, w))
    dist = [float("inf")] * n
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
    return -1
