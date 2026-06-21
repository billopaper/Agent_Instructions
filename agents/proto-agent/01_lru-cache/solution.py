class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity; self.cache = {}
    def get(self, key):
        if key not in self.cache: return -1
        self.cache[key] = self.cache.pop(key); return self.cache[key]
    def put(self, key, value):
        self.cache.pop(key, None); self.cache[key] = value
        if len(self.cache) > self.capacity: del self.cache[next(iter(self.cache))]
