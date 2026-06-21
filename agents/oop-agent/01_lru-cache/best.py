from collections import OrderedDict


class LRUCache:
    """Fixed-capacity least-recently-used cache.

    Recency is delegated to an OrderedDict: the leftmost item is the
    least recently used, the rightmost the most recently used. Every
    access moves its key to the right end; eviction pops the left end.
    """

    def __init__(self, capacity):
        self._capacity = capacity
        self._store = OrderedDict()

    def get(self, key):
        store = self._store
        if key not in store:
            return -1
        store.move_to_end(key)
        return store[key]

    def put(self, key, value):
        store = self._store
        if key in store:
            store.move_to_end(key)
        elif len(store) >= self._capacity:
            store.popitem(last=False)
        store[key] = value
