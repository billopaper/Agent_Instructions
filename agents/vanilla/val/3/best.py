import heapq


def shortest_path(n, edges, src, dst):
    if src == dst:
        return 0
    best_e = [None] * n
    for u, v, w in edges:
        if u != v:
            du = best_e[u]
            if du is None:
                du = best_e[u] = {}
            if v not in du or w < du[v]:
                du[v] = w
            dv = best_e[v]
            if dv is None:
                dv = best_e[v] = {}
            if u not in dv or w < dv[u]:
                dv[u] = w
    INF = float('inf')
    dist = [INF] * n
    dist[src] = 0
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        if u == dst:
            return d
        nbrs = best_e[u]
        if nbrs:
            for v, w in nbrs.items():
                nd = d + w
                if nd < dist[v]:
                    dist[v] = nd
                    heapq.heappush(pq, (nd, v))
    return -1
