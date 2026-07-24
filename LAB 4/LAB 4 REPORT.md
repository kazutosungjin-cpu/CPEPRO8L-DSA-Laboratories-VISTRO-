# Lab Report: Doubly and Circular Linked Lists

## Objectives

1. Implement a Doubly Linked List with `next` and `prev` pointers.
2. Build a Circular Singly Linked List verifying tail link wrapping.
3. Differentiate traversal termination strategies across linear and
   circular lists.

## Files

| File | Description |
|---|---|
| `lab4_doubly_circular.py` | `DoubleNode`, `DoublyLinkedList` (head insertion with `next`/`prev` links), and `CircularSinglyLinkedList` (tail insertion with tail-to-head wraparound), plus a test run. |

The file was run successfully with no errors.

---

## Execution & Output

```
--- Testing Doubly Linked List ---
None <-> 10 <-> 5 <-> None

--- Testing Circular Linked List ---
100 -> 200 -> 300 -> (loops to 100)
```

The output matches the expected results defined in the test script:
- After `insert_head(5)` and `insert_head(10)`, the doubly linked list
  correctly reads `None <-> 10 <-> 5 <-> None`, confirming both `next`
  and `prev` pointers were wired correctly.
- After `insert_tail(100)`, `insert_tail(200)`, and `insert_tail(300)`,
  the circular list correctly reads `100 -> 200 -> 300 -> (loops to 100)`.

---

## Report Analysis Questions

### 1. Source Code

`lab4_doubly_circular.py` is included with this submission and was
verified to execute without compile or runtime errors (see Execution &
Output above for the actual console capture, which matches the expected
output noted in the test script's comments).

### 2. Termination Condition — Traversing a Circular Linked List

Unlike a linear linked list, a circular list has no node whose `next`
pointer is `None`  the tail's `next` always points back to the `head`,
so a `while temp:` style loop would never stop and would traverse the
list forever. To avoid this, the traversal instead checks whether the
current pointer has looped back to the starting node.

In `CircularSinglyLinkedList.display()`, this is done by first visiting
`self.head`, then repeatedly moving `temp = temp.next` and checking
`if temp == self.head: break`. Because the check happens *after* moving
to the next node, the loop still visits every node exactly once
(including the head itself, added before the loop starts) before it
detects the wraparound and stops  rather than comparing against `None`,
which would never occur in a circular structure.

### 3. Conclusions

The extra prev pointer in a doubly linked list costs more memory but enables two-way traversal and O(1) node removal without needing to search for the predecessor. A circular list has no true "end"  the tail loops back to the head  which is great for things like round-robin scheduling, but it means traversal must stop by checking if you've returned to the starting node, since a None-based loop condition would run forever
