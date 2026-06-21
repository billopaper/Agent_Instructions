import heapq


def shortest_path(n, edges, src, dst):
    if src == dst:
        return 0
    deg = [0] * n
    for u, v, w in edges:
        if u != v: deg[u] += 1; deg[v] += 1
    head = [0] * (n + 1)
    for i in range(n): head[i + 1] = head[i] + deg[i]
    to = [0] * head[n]; wt = [0] * head[n]
    for i in range(n): deg[i] = head[i]
    for u, v, w in edges:
        if u == v: continue
        p = deg[u]; to[p] = v; wt[p] = w; deg[u] = p + 1
        p = deg[v]; to[p] = u; wt[p] = w; deg[v] = p + 1
    INF = float('inf')
    dF = [INF] * n; dB = [INF] * n
    dF[src] = 0; dB[dst] = 0
    hF = [(0, src)]; hB = [(0, dst)]
    best = INF
    push = heapq.heappush; pop = heapq.heappop
    while hF and hB:
        if hF[0][0] + hB[0][0] >= best: break
        d, u = pop(hF)
        if d <= dF[u]:
            for i in range(head[u], head[u + 1]):
                v = to[i]; nd = d + wt[i]
                if nd < dF[v]:
                    dF[v] = nd; push(hF, (nd, v))
                    if dB[v] + nd < best: best = dB[v] + nd
        d, u = pop(hB)
        if d <= dB[u]:
            for i in range(head[u], head[u + 1]):
                v = to[i]; nd = d + wt[i]
                if nd < dB[v]:
                    dB[v] = nd; push(hB, (nd, v))
                    if dF[v] + nd < best: best = dF[v] + nd
    return best if best < INF else -1
