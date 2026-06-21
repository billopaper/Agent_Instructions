import heapq


def shortest_path(n, edges, src, dst):
    if src == dst:
        return 0
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    INF = float('inf')
    df = [INF] * n; db = [INF] * n
    df[src] = 0; db[dst] = 0
    fwd = [(0, src)]; bwd = [(0, dst)]
    push = heapq.heappush; pop = heapq.heappop
    mu = INF
    while fwd and bwd:
        if fwd[0][0] + bwd[0][0] >= mu:
            break
        if fwd[0][0] <= bwd[0][0]:
            heap, dn, dfar = fwd, df, db
        else:
            heap, dn, dfar = bwd, db, df
        d, u = pop(heap)
        if d == dn[u]:
            for v, w in adj[u]:
                nd = d + w
                if nd < dn[v]:
                    dn[v] = nd
                    push(heap, (nd, v))
                if nd + dfar[v] < mu:
                    mu = nd + dfar[v]
    return mu if mu < INF else -1
