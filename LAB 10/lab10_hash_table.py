class HashNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.buckets = [None] * capacity

    def _hash(self, key):
        # Simple hash function: sum of ASCII values of the key's characters,
        # modulo the table's capacity.
        return sum(ord(ch) for ch in str(key)) % self.capacity

    def put(self, key, value):
        index = self._hash(key)

        # Empty bucket: place the new node directly.
        if self.buckets[index] is None:
            self.buckets[index] = HashNode(key, value)
            return

        # Bucket occupied: walk the chain.
        current = self.buckets[index]
        while True:
            if current.key == key:
                # Key already exists in the chain: update its value.
                current.value = value
                return
            if current.next is None:
                break
            current = current.next

        # Reached the end of the chain without finding the key: append (collision).
        current.next = HashNode(key, value)

    def get(self, key):
        index = self._hash(key)
        current = self.buckets[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next
        raise KeyError(key)

    def display(self):
        for idx in range(self.capacity):
            chain = []
            temp = self.buckets[idx]
            while temp:
                chain.append(f"[{temp.key}: {temp.value}]")
                temp = temp.next
            print(f"Bucket {idx}: " + " -> ".join(chain))


if __name__ == "__main__":
    ht = HashTable(5)
    ht.put("Alice", 25)
    ht.put("Bob", 30)
    ht.put("Charlie", 35)
    ht.display()

    print()
    print("Hash values:")
    for name in ["Alice", "Bob", "Charlie"]:
        print(f"  hash('{name}') = {ht._hash(name)}")

    print()
    print("=== Collision demonstration ===")
    print(f"hash('Alice') = {ht._hash('Alice')}")
    print(f"hash('David') = {ht._hash('David')}")
    print("Both hash to the same bucket -> David will be chained onto Alice's node.")
    ht.put("David", 40)
    ht.display()

    print()
    print("Lookup check after collision:")
    print(f"  get('Alice') = {ht.get('Alice')}")
    print(f"  get('David') = {ht.get('David')}")
