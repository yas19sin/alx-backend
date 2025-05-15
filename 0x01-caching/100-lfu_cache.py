#!/usr/bin/env python3
""" LFUCache module
"""
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """ LFUCache defines:
      - a LFU caching system with LRU for tie-breaking
    """

    def __init__(self):
        """ Initialize
        """
        super().__init__()
        self.frequencies = {}
        self.frequency_lists = {}
        self.min_frequency = 0

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data[key] = item
            self._increment_frequency(key)
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                lfu_key = self.frequency_lists[self.min_frequency][0]
                self.frequency_lists[self.min_frequency].pop(0)

                if not self.frequency_lists[self.min_frequency]:
                    del self.frequency_lists[self.min_frequency]

                del self.cache_data[lfu_key]
                del self.frequencies[lfu_key]
                print("DISCARD: {}".format(lfu_key))

            self.cache_data[key] = item
            self.frequencies[key] = 1
            self.min_frequency = 1

            if 1 not in self.frequency_lists:
                self.frequency_lists[1] = []
            self.frequency_lists[1].append(key)

    def get(self, key):
        """ Get an item by key
        """
        if key is None or key not in self.cache_data:
            return None

        self._increment_frequency(key)

        return self.cache_data[key]

    def _increment_frequency(self, key):
        """Increment frequency of a key and adjust data structures"""
        current_freq = self.frequencies[key]

        self.frequency_lists[current_freq].remove(key)

        if not self.frequency_lists[current_freq]:
            del self.frequency_lists[current_freq]
            if self.min_frequency == current_freq:
                self.min_frequency += 1

        new_freq = current_freq + 1
        self.frequencies[key] = new_freq

        if new_freq not in self.frequency_lists:
            self.frequency_lists[new_freq] = []
        self.frequency_lists[new_freq].append(key)
