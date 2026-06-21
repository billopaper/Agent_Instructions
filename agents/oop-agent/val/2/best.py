import heapq
from array import array


class WeightedGraph:
    """Undirected weighted CSR graph with bidirectional Dijkstra."""

    def __init__(self, n, edges):
        self.n = n
        deg = [0] * n
        for u, v, w in edges:
            if u != v:  # self-loops never help
                deg[u] += 1; deg[v] += 1
        off = array('i', [0]) * (n + 1)
        for i in range(n):
            off[i + 1] = off[i] + deg[i]
        to = array('i', [0]) * off[n]
        wt = array('i', [0]) * off[n]
        cur = list(off[:n])
        for u, v, w in edges:
            if u == v:
                continue
            to[cur[u]] = v; wt[cur[u]] = w; cur[u] += 1
            to[cur[v]] = u; wt[cur[v]] = w; cur[v] += 1
        self.off, self.to, self.wt = off, to, wt

    def shortest(self, src, dst):
        if src == dst:
            return 0
        n, off, to, wt = self.n, self.off, self.to, self.wt
        df = [-1] * n; db = [-1] * n
        df[src] = 0; db[dst] = 0
        hf = [src]; hb = [dst]
        push, pop = heapq.heappush, heapq.heappop
        best = float("inf")
        while hf and hb:
            if hf[0] // n + hb[0] // n >= best:
                break
            heap, dist, other = (hf, df, db) if hf[0] <= hb[0] else (hb, db, df)
            key = pop(heap); u = key % n; d = key // n
            if d > dist[u]:
                continue
            for i in range(off[u], off[u + 1]):
                nd = d + wt[i]; v = to[i]; dv = dist[v]
                if dv < 0 or nd < dv:
                    dist[v] = nd; push(heap, nd * n + v)
                    ov = other[v]
                    if ov >= 0 and nd + ov < best:
                        best = nd + ov
        return -1 if best == float("inf") else best


def shortest_path(n, edges, src, dst):
    return WeightedGraph(n, edges).shortest(src, dst)
