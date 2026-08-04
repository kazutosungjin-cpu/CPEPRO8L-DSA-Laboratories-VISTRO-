# Laboratory Activity No. 6 — Circular Queue Buffer Implementation

**Course Code:** CPEPRO8L
**Course Title:** Data Structures and Algorithms
**Term:** First Semester, AY 2026–2027

---

## 1. Objectives

1. Implement a fixed-capacity Circular Queue from scratch.
2. Understand index wrapping mathematical calculations (`(tail + 1) % capacity`).
3. Solve buffer overflow and underflow conditions.

---

## 2. Files

| File | Description |
|---|---|
| `lab6_circular_queue.py` | Completed implementation of the `CircularQueue` class (`enqueue`, `dequeue`) plus the required sample run and a 10-operation demonstration trace. |
| `README.md` | This documentation file. |

---

## 3. Methodology

`CircularQueue` is built on a fixed-size Python list (`self.queue`) with three pointers/counters: `head` (index of the front item), `tail` (index where the next item will be inserted), and `size` (current element count).

- **`enqueue(item)`** — if `is_full()` (`size == capacity`), it prints an overflow warning and returns `False`. Otherwise it stores `item` at `queue[tail]`, increments `size`, and advances `tail` with `tail = (tail + 1) % capacity`.
- **`dequeue()`** — if `is_empty()` (`size == 0`), it prints an underflow warning and returns `None`. Otherwise it reads `queue[head]`, clears that slot to `None`, decrements `size`, and advances `head` with `head = (head + 1) % capacity`.
- **`display()`** — prints the raw backing array along with the current `head` and `tail` indices, which is what makes the wraparound behavior visible in the traces below.

Because `head` and `tail` are always taken modulo `capacity`, both pointers cycle back to index `0` after reaching the end of the array instead of needing to shift all the remaining elements — this is what distinguishes a **circular** queue from a naive array-based queue.

---

## 4. Execution & Output

Console capture from running `python3 lab6_circular_queue.py`:

```
Dequeued: 1
Queue array: [None, 2, 3, 4, None] | Head: 1 | Tail: 4

--- 10-operation enqueue/dequeue trace (capacity = 5) ---
Step 1: enqueue(10)
Queue array: [10, None, None, None, None] | Head: 0 | Tail: 1
Step 2: enqueue(20)
Queue array: [10, 20, None, None, None] | Head: 0 | Tail: 2
Step 3: enqueue(30)
Queue array: [10, 20, 30, None, None] | Head: 0 | Tail: 3
Step 4: dequeue() -> 10
Queue array: [None, 20, 30, None, None] | Head: 1 | Tail: 3
Step 5: enqueue(40)
Queue array: [None, 20, 30, 40, None] | Head: 1 | Tail: 4
Step 6: enqueue(50)
Queue array: [None, 20, 30, 40, 50] | Head: 1 | Tail: 0
Step 7: enqueue(60)
Queue array: [60, 20, 30, 40, 50] | Head: 1 | Tail: 1
Step 8: enqueue(70)
Overflow! Queue is full.
Queue array: [60, 20, 30, 40, 50] | Head: 1 | Tail: 1
Step 9: dequeue() -> 20
Queue array: [60, None, 30, 40, 50] | Head: 2 | Tail: 1
Step 10: dequeue() -> 30
Queue array: [60, None, None, 40, 50] | Head: 3 | Tail: 1
```

---

## 5. Report Analysis Questions

### 5.1 Queue states during a series of 10 enqueues and dequeues

A `CircularQueue(5)` was driven through 10 operations: `enqueue(10, 20, 30)`, `dequeue()`, `enqueue(40, 50, 60, 70)`, `dequeue(), dequeue()`.

| Step | Operation | Result | Queue array | Head | Tail | Size |
|---|---|---|---|---|---|---|
| 0 | — (initial) | — | `[None, None, None, None, None]` | 0 | 0 | 0 |
| 1 | `enqueue(10)` | inserted | `[10, None, None, None, None]` | 0 | 1 | 1 |
| 2 | `enqueue(20)` | inserted | `[10, 20, None, None, None]` | 0 | 2 | 2 |
| 3 | `enqueue(30)` | inserted | `[10, 20, 30, None, None]` | 0 | 3 | 3 |
| 4 | `dequeue()` | returns `10` | `[None, 20, 30, None, None]` | 1 | 3 | 2 |
| 5 | `enqueue(40)` | inserted | `[None, 20, 30, 40, None]` | 1 | 4 | 3 |
| 6 | `enqueue(50)` | inserted (**tail wraps 4→0**) | `[None, 20, 30, 40, 50]` | 1 | 0 | 4 |
| 7 | `enqueue(60)` | inserted, queue now **full** | `[60, 20, 30, 40, 50]` | 1 | 1 | 5 |
| 8 | `enqueue(70)` | **rejected — overflow** | `[60, 20, 30, 40, 50]` | 1 | 1 | 5 |
| 9 | `dequeue()` | returns `20` | `[60, None, 30, 40, 50]` | 2 | 1 | 4 |
| 10 | `dequeue()` | returns `30` | `[60, None, None, 40, 50]` | 3 | 1 | 3 |

Key observations:
- At **step 6**, `tail` was at index 4 (the last slot). Adding `50` fills that slot, then `(4 + 1) % 5 = 0` wraps `tail` back to the front of the array instead of running out of bounds — even though physical slot `0` (originally holding `10`) had already been freed by the earlier `dequeue()` in step 4.
- At **step 7**, the queue reaches `size == capacity` (full), with `head == tail == 1` — a state that means "full," not "empty," because `size` (tracked separately) resolves the ambiguity.
- At **step 8**, `enqueue(70)` is correctly rejected with an overflow warning, and the array is left unchanged.
- At **steps 9–10**, `dequeue()` correctly frees slots `1` and `2` and advances `head` circularly, making room for future enqueues to reuse those slots.

### 5.2 Purpose of the `%` (modulo) operator in index calculations

The array backing the queue has a fixed length (`capacity`), with valid indices `0` to `capacity - 1`. As items are continuously enqueued and dequeued, `head` and `tail` must keep advancing forward — but without modulo, they would just increase indefinitely and eventually index outside the bounds of the array (`IndexError`), even though earlier slots have already been freed by prior dequeues.

The modulo operator solves this by wrapping the index back to `0` the moment it reaches `capacity`:

```python
self.tail = (self.tail + 1) % self.capacity
self.head = (self.head + 1) % self.capacity
```

For example, with `capacity = 5`, once `tail` reaches `5`, `5 % 5 = 0`, so the next item is written back into index `0` — reusing a slot instead of the queue reporting "full" prematurely just because the raw pointer ran past the end of the array. This is exactly what happens at **step 6** above, where `tail` moves from `4` to `0`.

In short, `%` turns a linear array into a **circular buffer**: it lets `head` and `tail` chase each other endlessly around the same fixed block of memory, so the queue's capacity is determined by `size` versus `capacity`, not by how far the raw index counters have climbed — giving O(1) enqueue/dequeue without ever needing to shift elements or reallocate the array.

---

## 6. Conclusion

The `CircularQueue` implementation correctly performs FIFO insertion and removal, wraps `head` and `tail` around the fixed-size array via the modulo operator, and correctly detects and rejects overflow and underflow conditions. The 10-operation trace confirms that freed slots at the front of the array (from earlier dequeues) are properly reused once `tail` wraps around, which is the defining advantage of a circular queue over a plain array-based queue.
