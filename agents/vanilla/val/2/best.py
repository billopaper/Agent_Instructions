from heapq import heappush, heappop


def shortest_path(n, edges, src, dst):
    if src == dst:
        return 0
    deg = [0] * (n + 1)
    for u, v, w in edges:
        if u != v:
            deg[u + 1] += 1; deg[v + 1] += 1
    for i in range(n):
        deg[i + 1] += deg[i]
    head = deg[:]; nbr = [0] * deg[n]; wgt = [0] * deg[n]
    for u, v, w in edges:
        if u != v:
            p = head[u]; nbr[p] = v; wgt[p] = w; head[u] = p + 1
            q = head[v]; nbr[q] = u; wgt[q] = w; head[v] = q + 1
    INF = float('inf')
    dF = [INF] * n; dB = [INF] * n
    dF[src] = 0; dB[dst] = 0
    hF = [src]; hB = [dst]
    doneF = bytearray(n); doneB = bytearray(n)
    best = INF
    while hF and hB:
        if hF[0] // n + hB[0] // n >= best:
            break
        c = heappop(hF); u = c % n; d = c // n
        if not doneF[u]:
            doneF[u] = 1
            for i in range(deg[u], deg[u + 1]):
                v = nbr[i]; nd = d + wgt[i]
                if nd < dF[v]:
                    dF[v] = nd; heappush(hF, nd * n + v)
                    if dB[v] + nd < best:
                        best = dB[v] + nd
        c = heappop(hB); u = c % n; d = c // n
        if not doneB[u]:
            doneB[u] = 1
            for i in range(deg[u], deg[u + 1]):
                v = nbr[i]; nd = d + wgt[i]
                if nd < dB[v]:
                    dB[v] = nd; heappush(hB, nd * n + v)
                    if dF[v] + nd < best:
                        best = dF[v] + nd
    return best if best < INF else -1
