import heapq

def shortest_path(n, edges, src, dst):
    if src == dst:
        return 0
    off = [0] * (n + 1)
    for u, v, w in edges:
        if u != v:
            off[u + 1] += 1; off[v + 1] += 1
    for i in range(n):
        off[i + 1] += off[i]
    nbr = [0] * off[n]; wt = [0] * off[n]; pos = off[:n]
    for u, v, w in edges:
        if u != v:
            p = pos[u]; nbr[p] = v; wt[p] = w; pos[u] = p + 1
            q = pos[v]; nbr[q] = u; wt[q] = w; pos[v] = q + 1
    dist = [float('inf')] * n; dist[src] = 0; pq = [src]
    while pq:
        x = heapq.heappop(pq); u = x % n; d = x // n
        if u == dst:
            return d
        if d > dist[u]:
            continue
        for i in range(off[u], off[u + 1]):
            v = nbr[i]; nd = d + wt[i]
            if nd < dist[v]:
                dist[v] = nd; heapq.heappush(pq, nd * n + v)
    return -1
