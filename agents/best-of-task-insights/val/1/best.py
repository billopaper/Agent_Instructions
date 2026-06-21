import heapq
from array import array

def shortest_path(n, edges, src, dst):
    if src == dst: return 0
    off = [0] * (n + 1)
    for u, v, w in edges:
        if u != v: off[u + 1] += 1; off[v + 1] += 1
    for i in range(n): off[i + 1] += off[i]
    m = off[n]; nbr = array('i', bytes(4 * m)); wt = array('i', bytes(4 * m)); pos = off[:n]
    for u, v, w in edges:
        if u != v:
            p = pos[u]; nbr[p] = v; wt[p] = w; pos[u] = p + 1
            q = pos[v]; nbr[q] = u; wt[q] = w; pos[v] = q + 1
    del pos
    D = [[-1] * n, [-1] * n]; D[0][src] = 0; D[1][dst] = 0
    Q = [[(0, src)], [(0, dst)]]; push = heapq.heappush; pop = heapq.heappop; best = -1
    while Q[0] and Q[1]:
        tf = Q[0][0][0]; tb = Q[1][0][0]
        if best >= 0 and tf + tb >= best: break
        s = 0 if tf <= tb else 1; dd = D[s]; od = D[1 - s]; pq = Q[s]
        d, u = pop(pq)
        if d > dd[u]: continue
        for i in range(off[u], off[u + 1]):
            v = nbr[i]; nd = d + wt[i]; dv = dd[v]
            if dv < 0 or nd < dv:
                dd[v] = nd; push(pq, (nd, v)); ov = od[v]
                if ov >= 0 and (best < 0 or nd + ov < best): best = nd + ov
    return best
