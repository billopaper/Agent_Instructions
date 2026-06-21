import heapq


def shortest_path(n, edges, src, dst):
    if src == dst:
        return 0

    head = [0] * (n + 1)
    for u, v, w in edges:
        if u != v: head[u + 1] += 1; head[v + 1] += 1
    for i in range(n): head[i + 1] += head[i]

    to = [0] * head[n]; wt = [0] * head[n]
    for u, v, w in edges:
        if u == v: continue
        to[head[u]] = v; wt[head[u]] = w; head[u] += 1
        to[head[v]] = u; wt[head[v]] = w; head[v] += 1

    dist = [float("inf")] * n
    dist[src] = 0
    pq = [src]; push = heapq.heappush; pop = heapq.heappop
    while pq:
        d, u = divmod(pop(pq), n)
        if d > dist[u]:
            continue
        if u == dst:
            return d
        lo = head[u - 1] if u else 0
        for i in range(lo, head[u]):
            v = to[i]; nd = d + wt[i]
            if nd < dist[v]:
                dist[v] = nd; push(pq, nd * n + v)

    return -1
