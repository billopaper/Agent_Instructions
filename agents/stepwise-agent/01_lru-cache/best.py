class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.store = {}  # insertion-ordered: first key is least-recently-used

    def get(self, key):
        if key not in self.store:
            return -1
        self.store[key] = value = self.store.pop(key)
        return value

    def put(self, key, value):
        if key in self.store:
            self.store.pop(key)
        elif len(self.store) >= self.capacity:
            del self.store[next(iter(self.store))]
        self.store[key] = value
