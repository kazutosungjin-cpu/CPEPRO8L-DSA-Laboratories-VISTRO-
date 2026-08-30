# Laboratory Activity No. 10 — Hash Tables and Collision Resolution

**Course Code:** CPEPRO8L
**Course Title:** Data Structures and Algorithms
**Term:** First Semester, AY 2026–2027

## 1. Objectives

1. Implement a custom hash mapping function.
2. Design a collision resolution mechanism using linked-list buckets
   (chaining).
3. Observe how load factor balances search efficiency.

## 2. Implementation Summary

**`_hash(key)`** — converts the key to a string, sums the ASCII value
(`ord`) of each character, and takes the result modulo `capacity`. This
maps any string key to a valid bucket index in `[0, capacity - 1]`.

**`put(key, value)`** — hashes the key to find its bucket:
- If the bucket is empty (`None`), a new `HashNode` is placed there
  directly.
- If the bucket is occupied, the chain (singly linked list) is walked:
  - If a node with a matching key is found, its value is updated in
    place (no duplicate is created).
  - Otherwise, the new key-value pair is appended as a new node at the
    end of the chain — this is the **collision resolution step**.

**`get(key)`** *(added for verification)* — hashes the key and walks the
resulting bucket's chain to find and return the matching value, raising
`KeyError` if the key isn't present. This isn't required by the
template but was added to confirm that chained entries remain correctly
retrievable after a collision.

**`display()`** — prints every bucket's index and its chain contents, so
the internal state of the table is directly observable.

## 3. Execution & Output

**Capacity:** 5 buckets. **Hash function:** sum of ASCII values mod 5.

### Initial insertions

```
$ python3 lab10_hash_table.py
Bucket 0: [Bob: 30]
Bucket 1: [Charlie: 35]
Bucket 2: 
Bucket 3: [Alice: 25]
Bucket 4: 

Hash values:
  hash('Alice') = 3
  hash('Bob') = 0
  hash('Charlie') = 1
```

With `capacity=5`, `"Alice"`, `"Bob"`, and `"Charlie"` happen to hash to
three different buckets (3, 0, and 1), so no collision occurs among the
template's original three entries.

### Collision demonstration

To satisfy the requirement of recording an actual collision event, the
key `"David"` was inserted next. Its ASCII sum also reduces to `3` modulo
5 — the same bucket as `"Alice"`:

```
=== Collision demonstration ===
hash('Alice') = 3
hash('David') = 3
Both hash to the same bucket -> David will be chained onto Alice's node.
Bucket 0: [Bob: 30]
Bucket 1: [Charlie: 35]
Bucket 2: 
Bucket 3: [Alice: 25] -> [David: 40]
Bucket 4: 
```

Bucket 3 now holds a chain of two nodes — `Alice` followed by `David` —
confirming the collision was resolved by appending to the linked list
rather than overwriting the existing entry.

A lookup on both keys afterward confirms neither value was lost or
corrupted by the collision:

```
Lookup check after collision:
  get('Alice') = 25
  get('David') = 40
```

## 4. Report Analysis Questions

### 4.1 Hash table entries demonstrating a collision event

| Key | Hash value (ASCII sum mod 5) | Bucket | Chain after insertion |
|-------|:---:|:---:|---|
| Alice | 3 | 3 | `[Alice: 25]` |
| David | 3 | 3 | `[Alice: 25] -> [David: 40]` |

Both `"Alice"` and `"David"` hash to bucket 3, producing a collision.
Since `"Alice"` was inserted first and occupies the bucket, `"David"` is
appended to the end of that bucket's chain rather than overwriting
`"Alice"`'s entry. Both keys remain independently retrievable afterward,
as shown by the `get()` calls above.

### 4.2 Chaining vs. linear probing: search efficiency

**Chaining** (used in this implementation) resolves a collision by
storing all keys that hash to the same index in a linked list attached
to that bucket. Searching for a key means hashing to the bucket, then
walking that bucket's chain until the key is found.

**Linear probing** is an open-addressing scheme: on a collision, it
scans forward through the array (index + 1, index + 2, …, wrapping
around) until it finds an empty slot, and stores the key there instead.
Searching means hashing to the initial index, then scanning forward the
same way until the key is found or an empty slot is hit.

| Aspect | Chaining | Linear probing |
|---|---|---|
| Storage | Extra nodes/pointers per bucket | All keys live in the fixed-size array itself |
| Worst-case search | O(n) if all keys hash to one bucket, but only that bucket's chain is searched | O(n) if the table is full/clustered, and a long probe sequence can span most of the table |
| Load factor > 1 | Still works — chains simply grow longer | Impossible — the array cannot hold more entries than its capacity |
| Clustering | Not affected by clustering; a full bucket doesn't slow down lookups elsewhere in the table | Prone to **primary clustering**, where consecutive filled slots merge into long runs, degrading search times across the *whole* table, not just one bucket |
| Deletion | Straightforward — just unlink the node from its chain | Harder — naively deleting a slot can break the probe sequence for later keys, usually requiring a special "deleted" marker (tombstone) |
| Cache performance | Chain nodes may be scattered in memory (pointer chasing) | Better cache locality — probing walks a contiguous array |

**In practice:** chaining degrades gracefully as the load factor grows
past 1, since a bucket's chain can grow indefinitely — average search
time stays close to O(1 + load factor). Linear probing is faster when
the load factor is kept low (roughly below 0.7) because it benefits from
array cache locality, but its performance deteriorates sharply as the
table fills up, since clustering causes probe sequences to grow much
longer than the load factor alone would suggest. Chaining is generally
the simpler and more forgiving choice when the number of entries is
unpredictable; linear probing can outperform it in tightly
capacity-managed tables with good hash distribution and low load
factors.
