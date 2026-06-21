class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}

    def get(self, key):
        if key in self.cache:
            self.cache[key] = self.cache.pop(key)
        return self.cache.get(key, -1)

    def put(self, key, value):
        self.cache.pop(key, None)
        if len(self.cache) >= self.capacity:
            self.cache.pop(next(iter(self.cache)))
        self.cache[key] = value
