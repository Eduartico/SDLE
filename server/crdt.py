from collections import Counter

class PNCounter:
    def __init__(self):
        self.positive_counter = Counter()
        self.negative_counter = Counter()

    def increment(self, replica_id, value=1):
        self.positive_counter[replica_id] += value

    def decrement(self, replica_id, value=1):
        self.negative_counter[replica_id] += value

    def value(self):
        return sum((self.positive_counter - self.negative_counter).values())

    def merge(self, other):
        self.positive_counter.update(other.positive_counter)
        self.negative_counter.update(other.negative_counter)

class ShoppingListCRDT:
    def __init__(self):
        self.added_items = set()
        self.removed_items = set()
        self.quantities = {}

    def add_item(self, item, quantity=1):
        self.added_items.add(item)
        if item not in self.quantities:
            self.quantities[item] = PNCounter()
        self.quantities[item].increment('add', quantity)

    def remove_item(self, item, quantity=1):
        if item in self.added_items:
            self.removed_items.add(item)
            if item not in self.quantities:
                self.quantities[item] = PNCounter()
            self.quantities[item].increment('remove', quantity)

    def buy_item(self, item, quantity=1):
        if item in self.added_items and item not in self.removed_items:
            if item not in self.quantities:
                self.quantities[item] = PNCounter()
            self.quantities[item].decrement('add', quantity)

    def get_state(self):
        return {
            'added_items': list(self.added_items),
            'removed_items': list(self.removed_items),
            'quantities': {item: self.quantities[item].value() for item in self.quantities}
        }
    
    def get_list(self):
        final_list = [(item, self.quantities[item].value()) for item in self.added_items if item not in self.removed_items]
        return final_list

    def merge(self, other):
        self.added_items.update(other.added_items)
        self.removed_items.update(other.removed_items)

        for item in other.quantities:
            if item not in self.quantities:
                self.quantities[item] = PNCounter()
            self.quantities[item].merge(other.quantities[item])

    def copy(self):
        replica = ShoppingListCRDT()
        replica.added_items = self.added_items.copy()
        replica.removed_items = self.removed_items.copy()
        replica.quantities = self.quantities.copy()
        return replica

# Example usage
replica1 = ShoppingListCRDT()
replica2 = ShoppingListCRDT()

replica1.add_item("Apple", quantity=3)
replica2.remove_item("Apple", quantity=1)
replica1.buy_item("Apple", quantity=2)

# Print the final state
print()
print("Replica 1 state:", replica1.get_state())
print("Replica 1 list:", replica2.get_list())
print("Replica 2 state:", replica2.get_state())
print("Replica 2 list:", replica2.get_list())

# Merge replicas to synchronize state
replica1.merge(replica2)
replica2.merge(replica1)

# Print the final state
print()
print("Replica 1 state:", replica1.get_state())
print("Replica 1 list:", replica2.get_list())
print("Replica 2 state:", replica2.get_state())
print("Replica 2 list:", replica2.get_list())
