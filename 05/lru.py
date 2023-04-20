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

    def get(self, key):
        if key in self.dct:
            node = self.dct[key]
            self.rm_from_list(node)
            self.put_head(node)
            return node.value
        return None

    def set(self, key, value):
        if key in self.dct:
            node = self.dct[key]
            self.rm_from_list(node)
            self.put_head(node)
            node.value = value
        else:
            if len(self.dct) == self.limit:
                self.rm_tail()
            node = Node(key, value)
            self.dct[key] = node
            self.put_head(node)

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
