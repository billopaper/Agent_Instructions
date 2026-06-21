import heapq
from array import array
from itertools import accumulate


class Graph:
    """Undirected weighted graph in CSR form (self-loops dropped)."""

    def __init__(self, n, edges):
        deg = [0] * n
        for u, v, w in edges:
            if u != v:
                deg[u] += 1; deg[v] += 1
        head = [0] + list(accumulate(deg))
        to = array('i', bytes(4 * head[n]))
        wt = array('i', bytes(4 * head[n]))
        cur = head[:n]
        for u, v, w in edges:
            if u != v:
                p = cur[u]; to[p] = v; wt[p] = w; cur[u] = p + 1
                q = cur[v]; to[q] = u; wt[q] = w; cur[v] = q + 1
        self.head, self.to, self.wt, self.n = head, to, wt, n

    def shortest_path(self, src, dst):
        if src == dst:
            return 0
        head, to, wt, n = self.head, self.to, self.wt, self.n
        dist = array('q', [-1]) * n  # -1 = unvisited; real distances are >= 0
        dist[src] = 0
        heap = [src]  # heap of packed keys: key = d * n + node
        push, pop = heapq.heappush, heapq.heappop
        while heap:
            d, node = divmod(pop(heap), n)
            if node == dst:
                return d
            if d > dist[node]:
                continue
            for i in range(head[node], head[node + 1]):
                nxt = to[i]
                nd = d + wt[i]
                if dist[nxt] < 0 or nd < dist[nxt]:
                    dist[nxt] = nd
                    push(heap, nd * n + nxt)
        return -1


def shortest_path(n, edges, src, dst):
    return Graph(n, edges).shortest_path(src, dst)
