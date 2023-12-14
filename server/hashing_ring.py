import hashlib

class HashingRing:
    def __init__(self, nodes=None):
        self.nodes = set(nodes or [])
        self.ring = dict()
        self.sorted_keys = []

        for node in self.nodes:
            self.add_node(node)

    def add_node(self, node):
        key = self.gen_key(str(node))
        self.ring[key] = node
        self.sorted_keys.append(key)
        self.sorted_keys.sort()

    def remove_node(self, node):
        key = self.gen_key(node)
        del self.ring[key]
        self.sorted_keys.remove(key)

    def get_node(self, string_key):
        if not self.ring:
            return None

        key = self.gen_key(str(string_key))
        nodes = self.sorted_keys
        for i, node_key in enumerate(nodes):
            if key <= node_key:
                return self.ring[node_key]
        return self.ring[nodes[0]]

    @staticmethod
    def gen_key(key):
        m = hashlib.md5()
        m.update(key.encode('utf-8'))
        return int(m.hexdigest(), 16)
