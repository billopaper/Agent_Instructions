import heapq


def shortest_path(n, edges, src, dst):
    if src == dst:
        return 0

    head = [0] * (n + 1)
    for u, v, w in edges:
        if u != v:
            head[u + 1] += 1
            head[v + 1] += 1
    for i in range(n):
        head[i + 1] += head[i]

    nbr = [0] * head[n]
    wgt = [0] * head[n]
    fill = head[:n]
    for u, v, w in edges:
        if u == v:
            continue
        p = fill[u]; nbr[p] = v; wgt[p] = w; fill[u] = p + 1
        p = fill[v]; nbr[p] = u; wgt[p] = w; fill[v] = p + 1

    INF = float("inf")
    df = {src: 0}
    db = {dst: 0}
    pf = [(0, src)]
    pb = [(0, dst)]
    best = INF
    push = heapq.heappush
    pop = heapq.heappop
    while pf and pb:
        if pf[0][0] + pb[0][0] >= best:
            break
        if pf[0][0] <= pb[0][0]:
            pq, dcur, doth = pf, df, db
        else:
            pq, dcur, doth = pb, db, df
        d, u = pop(pq)
        if d > dcur[u]:
            continue
        for i in range(head[u], head[u + 1]):
            v = nbr[i]
            nd = d + wgt[i]
            cur = dcur.get(v)
            if cur is None or nd < cur:
                dcur[v] = nd
                push(pq, (nd, v))
                o = doth.get(v)
                if o is not None and nd + o < best:
                    best = nd + o

    return best if best < INF else -1
