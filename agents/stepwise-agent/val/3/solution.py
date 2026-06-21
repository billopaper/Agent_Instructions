import heapq


def shortest_path(n, edges, src, dst):
    if src == dst:
        return 0
    deg = [0] * n
    for u, v, w in edges:
        if u != v:
            deg[u] += 1
            deg[v] += 1
    head = [0] * (n + 1)
    for i in range(n):
        head[i + 1] = head[i] + deg[i]
    to = [0] * head[n]
    wt = [0] * head[n]
    pos = head[:n]
    for u, v, w in edges:
        if u == v:
            continue
        pu = pos[u]; to[pu] = v; wt[pu] = w; pos[u] = pu + 1
        pv = pos[v]; to[pv] = u; wt[pv] = w; pos[v] = pv + 1
    del deg, pos
    shift = n.bit_length(); mask = (1 << shift) - 1
    dist = [float("inf")] * n; dist[src] = 0
    pq = [src]
    while pq:
        key = heapq.heappop(pq)
        d = key >> shift; u = key & mask
        if d > dist[u]:
            continue
        if u == dst:
            return d
        for i in range(head[u], head[u + 1]):
            v = to[i]; nd = d + wt[i]
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd << shift) | v)
    return -1
