import unittest
from lru import LRUCache


class TestLRUCache(unittest.TestCase):
    def test_cache_set_get(self):
        cache = LRUCache(2)

        cache.set("k1", "val1")
        cache.set("k2", "val2")

        self.assertEqual(cache.get("k3"), None)
        self.assertEqual(cache.get("k2"), "val2")
        self.assertEqual(cache.get("k1"), "val1")

        cache.set("k3", "val3")

        self.assertEqual(cache.get("k3"), "val3")
        self.assertEqual(cache.get("k2"), None)
        self.assertEqual(cache.get("k1"), "val1")

    def test_cache_overwrite_key(self):
        cache = LRUCache(2)

        cache.set("k1", "val1")
        cache.set("k2", "val2")
        cache.set("k1", "new_val1")

        self.assertEqual(cache.get("k1"), "new_val1")
        self.assertEqual(cache.get("k2"), "val2")

    def test_cache_exceed_limit(self):
        cache = LRUCache(2)

        cache.set("k1", "val1")
        cache.set("k2", "val2")
        cache.set("k3", "val3")

        self.assertEqual(cache.get("k1"), None)
        self.assertEqual(cache.get("k2"), "val2")
        self.assertEqual(cache.get("k3"), "val3")

    def test_cache_empty(self):
        cache = LRUCache(2)

        self.assertEqual(cache.get("k1"), None)
        self.assertEqual(cache.get("k2"), None)


if __name__ == '__main__':
    unittest.main()
