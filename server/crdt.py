from handlers import *
from typing import TypeVar, Generic

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

class Context:
    def __init__(self):
        self.clock_map = {}
        self.dot_cloud = set()

    def contain(self, resource, number):
        cloud = (resource, number) in self.dot_cloud
        clock = self.clock_map.get(resource, 0) >= number
        return cloud or clock

    def compact(self):
        dots_to_rmv = set()

        for r, n in self.dot_cloud:
            n2 = self.clock_map.get(r, 0)

            if n == n2 + 1:
                self.clock_map[r] = n
                dots_to_rmv.add((r, n))
            elif n <= n2:
                dots_to_rmv.add((r, n))

        self.dot_cloud.difference_update(dots_to_rmv)

    def next_dot(self, r):
        current_count = self.clock_map.setdefault(r, 0)
        self.clock_map[r] = current_count + 1
        return (r, self.clock_map[r])

    def add(self, dot):
        self.dot_cloud.add(dot)

    def join(self, other):
        for key, value in other.clock_map.items():
            handle_update_or_insert(key, value, max, self.clock_map)

        self.dot_cloud.update(other.dot_cloud)
        self.compact()
        
    def get_clock(self, resource):
        return self.clock_map.get(resource, 0)

    def add_multiple(self, dots):
        self.dot_cloud.update(dots)

class Kernel(Generic[T]):
    def __init__(self):
        self.context = Context()
        self.entries = {}

    def values(self):
        return list(self.entries.values())

    def add(self, rep, v):
        dot = self.context.next_dot(rep)
        self.entries[dot] = v
        self.context.add(dot)

    def rmv(self, rep, v):
        entries_to_rmv = [(dot, v2) for dot, v2 in self.entries.items() if v2 == v]

        for dot, _ in entries_to_rmv:
            del self.entries[dot]
            self.context.add(dot)

        self.context.compact()

    def rmv_all(self):
        dots_to_add = list(self.entries.keys())
        self.context.add_multiple(dots_to_add)
        self.entries.clear()
        self.context.compact()

    def join(self, other):
        entries_to_add = [(dot, v) for dot, v in other.entries.items() if dot not in self.entries and not self.context.contain(*dot)]
        entries_to_rmv = [dot for dot in self.entries.keys() if self.context.contain(*dot) and dot not in other.entries]

        self.entries.update(entries_to_add)
        for dot in entries_to_rmv:
            del self.entries[dot]

        self.context.join(other.context)
    
    def get_entry(self, dot):
        return self.entries.get(dot, None)

    def get_all_entries(self):
        return self.entries.copy()

class AWORSet(Generic[T]):
    def __init__(self):
        self.core = Kernel[T]()
        self.delta = None

    def value(self):
        return set(self.core.values())

    def add(self, r, v):
        self.core.rmv(r, v)
        self.core.add(r, v)

    def rmv(self, r, v):
        self.core.rmv(r, v)

    def add_and_rmv(self, r, v):
        entries_to_rmv = [(dot, v2) for dot, v2 in self.core.entries.items() if v2 == v]

        for dot, _ in entries_to_rmv:
            del self.core.entries[dot]
            self.core.context.add(dot)

        dots_to_add = list(self.core.entries.keys())
        self.core.context.add_multiple(dots_to_add)

        self.core.context.compact()

    def join(self, other):
        self.delta = handle_join(self.delta, other.delta)
        self.core.join(other.core)

    def join_delta(self, delta):
        self.delta = handle_join(self.delta, delta)
        self.core.join(delta)

    def split(self):
        return self, self.delta
    
    def get_entry_value(self, key):
        return self.entries.get(key, None)

    def get_all_entries(self):
        return self.entries.copy()

class AWORMap(Generic[K, V]):
    def __init__(self):
        self.keys = AWORSet[K]()
        self.entries = dict()

    def value(self):
        return self.entries

    def add(self, r, key: K, value: V):
        self.rmv(r, key)
        self.keys.add(r, key)
        self.entries[key] = max(self.entries.get(key, 0) + value, 0)

    def rmv(self, r, key: K):
        self.keys.rmv(r, key)
        self.rmv(r, key)

    def join(self, r1, other, r2):
        self.keys.join(other.keys)
        entries = {}

        for key in self.keys.value():
            entries[key] = self._join_entry(r1, self.entries.get(key, 0), r2, other.entries.get(key, 0))

        self.entries = entries

    def rmv(self, r, key: K):
        if key in self.entries:
            del self.entries[key]

    def _join_entry(self, r1, value1, r2, value2):
        return value1 if r1 > r2 else value2
    
    def get_entry_value(self, key):
        return self.entries.get(key, None)

    def get_all_entries(self):
        return self.entries.copy()

class CRDT:
    def __init__(self, id, name, items: AWORMap, replica_id=0):
        self.id = id
        self.replica_id = replica_id
        self.name = name
        self.items = items
        self.item_names = dict()

    def add_item(self, item_id, item_name, item_quantity):
        self._update_items(item_id, item_quantity)
        self._update_item_names(item_id, item_name)

    def rmv_item(self, item_id):
        self.items.rmv(self.replica_id, item_id)

    def join(self, other):
        if self._is_same_shopping_list(other):
            self._join_items(other)
            self._update_replica_id(other)
            self._update_item_names(other)

    def _update_items(self, item_id, item_quantity):
        self.items.add(self.replica_id, item_id, item_quantity)

    def _update_item_names(self, item_id, item_name):
        if item_name is not None:
            self.item_names[item_id] = item_name

    def _is_same_shopping_list(self, other):
        return self.id == other.id

    def _join_items(self, other):
        self.items.join(self.replica_id, other.items, other.replica_id)

    def _update_replica_id(self, other):
        self.replica_id = max(self.replica_id, other.replica_id) + 1

    def _update_item_names(self, other):
        self.item_names.update(other.item_names)
        
    def get_item_name(self, item_id):
        return self.item_names.get(item_id, None)

    def get_all_item_names(self):
        return self.item_names.copy()