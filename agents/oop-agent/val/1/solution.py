import heapq
from array import array


class WeightedGraph:
    def __init__(self, n, edges):
        self._n = n
        deg = [0] * n
        for u, v, w in edges:
            if u != v:
                deg[u] += 1; deg[v] += 1
        start = array('i', bytes(4 * (n + 1)))
        s = 0
        for i in range(n):
            start[i] = s; s += deg[i]
        start[n] = s
        to = array('i', bytes(4 * s))
        wt = array('i', bytes(4 * s))
        cur = list(start[:n])
        for u, v, w in edges:
            if u == v:
                continue
            i = cur[u]; to[i] = v; wt[i] = w; cur[u] = i + 1
            j = cur[v]; to[j] = u; wt[j] = w; cur[v] = j + 1
        self._start, self._to, self._wt = start, to, wt

    def shortest_distance(self, src, dst):
        if src == dst:
            return 0
        start, to, wt = self._start, self._to, self._wt
        dist = [None] * self._n
        dist[src] = 0
        heap = [(0, src)]
        push, pop = heapq.heappush, heapq.heappop
        while heap:
            d, u = pop(heap)
            if u == dst:
                return d
            if d > dist[u]:
                continue
            for i in range(start[u], start[u + 1]):
                v = to[i]; nd = d + wt[i]; dv = dist[v]
                if dv is None or nd < dv:
                    dist[v] = nd; push(heap, (nd, v))
        return -1


def shortest_path(n, edges, src, dst):
    return WeightedGraph(n, edges).shortest_distance(src, dst)
