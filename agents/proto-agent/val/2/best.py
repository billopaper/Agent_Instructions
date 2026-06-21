from heapq import heappush, heappop


def shortest_path(n, edges, src, dst):
    if src == dst:
        return 0
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        if u != v:
            au = adj[u]; au.append(v); au.append(w)
            av = adj[v]; av.append(u); av.append(w)
    dist = [float('inf')] * n
    dist[src] = 0
    pq = [src]
    while pq:
        key = heappop(pq)
        u = key % n; d = key // n
        if d > dist[u]:
            continue
        if u == dst:
            return d
        lst = adj[u]
        for k in range(0, len(lst), 2):
            v = lst[k]; nd = d + lst[k + 1]
            if nd < dist[v]:
                dist[v] = nd; heappush(pq, nd * n + v)
    return -1
