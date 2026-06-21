from heapq import heappush, heappop


def shortest_path(n, edges, src, dst):
    if src == dst:
        return 0
    head = [0] * (n + 1)
    for u, v, w in edges:
        if u != v:
            head[u + 1] += 1; head[v + 1] += 1
    for i in range(n):
        head[i + 1] += head[i]
    nbr = [0] * head[n]
    wt = [0] * head[n]
    cur = head[:n]
    for u, v, w in edges:
        if u != v:
            p = cur[u]; nbr[p] = v; wt[p] = w; cur[u] = p + 1
            q = cur[v]; nbr[q] = u; wt[q] = w; cur[v] = q + 1
    INF = float('inf')
    dist = ([INF] * n, [INF] * n)
    dist[0][src] = 0; dist[1][dst] = 0
    pq = ([src], [dst])  # heap of encoded keys: dist * n + node
    mu = INF
    while pq[0] and pq[1]:
        if pq[0][0] // n + pq[1][0] // n >= mu:
            break
        s = 0 if pq[0][0] <= pq[1][0] else 1
        ds, do = dist[s], dist[1 - s]
        x = heappop(pq[s]); d = x // n; u = x % n
        if d > ds[u]:
            continue
        for p in range(head[u], head[u + 1]):
            v = nbr[p]; nd = d + wt[p]
            if nd < ds[v] and nd < mu:
                ds[v] = nd; heappush(pq[s], nd * n + v)
                t = nd + do[v]
                if t < mu: mu = t
    return -1 if mu == INF else mu
