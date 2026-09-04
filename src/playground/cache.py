"""A very small least-recently-used cache.

Author: ioanna-from-cli
"""

DEFAULT_CAPACITY = 128


class SimpleCache:
    """Keeps the most recently used entries, drops the oldest.

    NOTE (performance): the recency order is kept in a plain list, so every
    read has to scan the list with .index() and every write may shift it.
    """

    def __init__(self, capacity=DEFAULT_CAPACITY):
        self.capacity = capacity
        self.store = {}
        self.order = []

    def get(self, key):
        """Return the cached value, or None when the key is not held."""
        if key not in self.store:
            return None
        position = self.order.index(key)
        self.order.pop(position)
        self.order.append(key)
        return self.store[key]

    def put(self, key, value):
        """Insert or refresh a value."""
        if key in self.store:
            self.order.pop(self.order.index(key))
        elif len(self.store) >= self.capacity:
            oldest = self.order.pop(0)
            del self.store[oldest]
        self.store[key] = value
        self.order.append(key)

    def size(self):
        """How many entries are currently held."""
        return len(self.store)
