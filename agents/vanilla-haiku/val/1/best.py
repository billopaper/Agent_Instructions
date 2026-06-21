import heapq


def shortest_path(n, edges, src, dst):
    if src == dst:
        return 0
    head = [0] * (n + 1)
    for u, v, w in edges:
        if u != v:
            head[u + 1] += 1
            head[v + 1] += 1
    for i in range(1, n + 1):
        head[i] += head[i - 1]
    pos = head[:n]
    nbr = [0] * head[n]
    wgt = [0] * head[n]
    for u, v, w in edges:
        if u == v:
            continue
        p = pos[u]; nbr[p] = v; wgt[p] = w; pos[u] = p + 1
        q = pos[v]; nbr[q] = u; wgt[q] = w; pos[v] = q + 1
    dist = [float('inf')] * n
    dist[src] = 0
    pq = [(0, src)]
    push = heapq.heappush; pop = heapq.heappop
    while pq:
        d, u = pop(pq)
        if d > dist[u]:
            continue
        if u == dst:
            return d
        for i in range(head[u], head[u + 1]):
            v = nbr[i]
            nd = d + wgt[i]
            if nd < dist[v]:
                dist[v] = nd
                push(pq, (nd, v))
    return -1
