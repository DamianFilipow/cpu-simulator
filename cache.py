from collections import deque

class Cache:

    def __init__(self, size = 16):
        self.cache = deque(maxlen=size)
    
    def search_cache(self, address):
        for entry in self.cache:
            if entry[0] == address:
                print("Cache hit")
                return entry[1]
        print("Cache miss")
        return None
    
    def write_cache(self, address, data):
        for idx, (addr, _) in enumerate(self.cache):
            if addr == address:
                self.cache.pop(idx)
                self.cache.append((address, data))
                print("Cache updated")
                return
        self.cache.append((address, data))
        print("Data saved into cache")
        
    def flush_cache(self):
        self.cache.clear()
        print("Cache cleared")