import logging
import argparse


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:

    def __init__(self, limit=42):
        self.limit = limit
        self.dct = {}
        self.head = Node('k0', 'val0')
        self.tail = Node('k-1', 'val-1')
        self.head.next = self.tail
        self.tail.prev = self.head
        self.logger = logging.getLogger()

    def get(self, key):
        if key in self.dct:
            node = self.dct[key]
            self.rm_from_list(node)
            self.put_head(node)
            self.logger.debug("LRUCache: Got value from cache for key %s", key)
            return node.value
        # logging.info(f"LRUCache: Key {key} not found in cache")
        self.logger.error("LRUCache: Key %s not found in cache", key)
        return None

    def set(self, key, value):
        if key in self.dct:
            node = self.dct[key]
            self.rm_from_list(node)
            self.put_head(node)
            node.value = value
            # logging.info(f"LRUCache: Updated value in cache for key {key}")
            self.logger.info(
                "LRUCache: Updated value in cache for key %s", key)
        else:
            if len(self.dct) == self.limit:
                self.rm_tail()
                self.logger.info(
                    "LRUCache: Removed least recently used item from cache"
                    )
            node = Node(key, value)
            self.dct[key] = node
            self.put_head(node)
            # logging.info(f"LRUCache: Added new item to cache for key {key}")
            self.logger.info(
                "LRUCache: Added new item to cache for key %s", key)

    def rm_from_list(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def put_head(self, node):
        pointer = self.head.next
        self.head.next = node
        node.next = pointer
        node.prev = self.head
        pointer.prev = node

    def rm_tail(self):
        if self.dct:
            pointer = self.tail.prev
            del self.dct[pointer.key]
            self.rm_from_list(pointer)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='LRU Cache with logging')
    parser.add_argument('-f', '--filter', action='store_true',
                        help='Custom filter for logging')
    parser.add_argument('-s', '--stdout', action='store_true',
                        help='Enable logging to stdout')
    args = parser.parse_args()

    FILENAME = 'cache.log'

    if args.filter:
        class CustomFilter(logging.Filter):
            def filter(self, record):
                return len(record.getMessage().split()) % 2 != 0
        logging.getLogger().addFilter(CustomFilter())
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                        filename=FILENAME, level=logging.DEBUG)
    if args.stdout:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(levelname)s:%(message)s')
        console_handler.setFormatter(formatter)
        logging.getLogger().addHandler(console_handler)

    cache = LRUCache(limit=3)
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.set("key3", "value3")
    cache.get("key1")
    cache.set("key4", "value4")
    cache.set("key5", "value5")
    cache.get("key2")
    cache.set("key6", "value6")
