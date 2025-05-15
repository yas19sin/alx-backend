#!/usr/bin/env python3
""" LIFOCache module
"""
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """ LIFOCache defines:
      - a LIFO caching system
    """

    def __init__(self):
        """ Initialize
        """
        super().__init__()
        self.stack = []

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data[key] = item
            self.stack.remove(key)
            self.stack.append(key)
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                last_key = self.stack.pop()
                del self.cache_data[last_key]
                print("DISCARD: {}".format(last_key))

            self.cache_data[key] = item
            self.stack.append(key)

    def get(self, key):
        """ Get an item by key
        """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
