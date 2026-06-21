class LRUCache(dict):
    def __init__(self, capacity):
        super().__init__()
        self.capacity = capacity

    def get(self, key):
        if key not in self: return -1
        self[key] = self.pop(key)
        return self[key]

    def put(self, key, value):
        if key in self: del self[key]
        elif len(self) >= self.capacity: del self[next(iter(self))]
        self[key] = value
