import heapq


def shortest_path(n, edges, src, dst):
    if src == dst:
        return 0
    deg = [0] * n
    for u, v, w in edges:
        if u != v:
            deg[u] += 1
            deg[v] += 1
    start = [0] * (n + 1)
    for i in range(n):
        start[i + 1] = start[i] + deg[i]
    to = [0] * start[n]
    wt = [0] * start[n]
    pos = start[:n]
    for u, v, w in edges:
        if u == v:
            continue
        p = pos[u]; to[p] = v; wt[p] = w; pos[u] = p + 1
        q = pos[v]; to[q] = u; wt[q] = w; pos[v] = q + 1
    dist = [float('inf')] * n
    dist[src] = 0
    pq = [src]
    push = heapq.heappush; pop = heapq.heappop
    while pq:
        d, u = divmod(pop(pq), n)
        if d > dist[u]:
            continue
        if u == dst:
            return d
        for i in range(start[u], start[u + 1]):
            v = to[i]; nd = d + wt[i]
            if nd < dist[v]:
                dist[v] = nd; push(pq, nd * n + v)
    return -1
