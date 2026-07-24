# Lab Report: Singly Linked List CRUD Operations

## Objectives

1. Construct custom `Node` and `SinglyLinkedList` classes.
2. Implement insertion at the head, tail, and specific values.
3. Manage list nodes and pointers cleanly without losing references.

## Files

| File | Description |
|---|---|
| `lab3_singly_linked_list.py` | `Node` and `SinglyLinkedList` classes with `insert_head`, `insert_tail`, `delete_value`, `search`, and `display` operations, plus a test run. |

The file was run successfully with no errors.

---

## Execution & Output

```
20 -> 10 -> 30 -> None
20 -> 30 -> None
Is 30 in list? True
```

The output matches the expected results defined in the test script:
- After `insert_head(10)`, `insert_head(20)`, and `insert_tail(30)`, the
  list correctly reads `20 -> 10 -> 30 -> None`.
- After `delete_value(10)`, the list correctly reads `20 -> 30 -> None`.
- `search(30)` correctly returns `True`.

---

## Report Analysis Questions

### 1. Source Code

`lab3_singly_linked_list.py` is included with this submission and was
verified to run without errors (see Execution & Output above for the
actual console capture, which matches the expected output noted in the
test script's comments).

### 2. Console Output — Insertion, Search, and Deletion

See the **Execution & Output** section above for the full console
capture covering insertion (`insert_head`, `insert_tail`), deletion
(`delete_value`), and search (`search`).

### 3. Pointer Trace — Deleting the Middle Node

Before deletion, the list is: `head -> [20] -> [10] -> [30] -> None`

Calling `delete_value(10)` walks the list as follows:

1. `current` starts at `head`, which points to the node containing `20`.
   `head.data` (`20`) is not the target (`10`), so the head-removal
   shortcut is skipped.
2. The loop checks `current.next.data`: `current` is the `20` node, and
   `current.next` is the `10` node — `current.next.data == 10` matches
   the target.
3. The deletion rewires the pointer: `current.next = current.next.next`.
   This sets the `20` node's `next` pointer to skip directly over the
   `10` node and point to the `30` node instead.
4. The `10` node is now unreferenced by the list — nothing points to it
   anymore — so it is effectively removed, even though its own `.next`
   pointer still (harmlessly) points to the `30` node.
5. The list is now: `head -> [20] -> [30] -> None`, matching the actual
   output `20 -> 30 -> None`.

### 4. Conclusions

Deleting a node from a singly linked list is O(1) once you've found it — you just re-point the previous node's next to skip over it, no shifting needed (unlike arrays, which require moving every subsequent element). But finding that node takes O(n), since linked lists only allow sequential traversal, not direct indexing. So overall delete-by-value is still O(n), just with cheaper removal once located. The takeaway: arrays favor random access, linked lists favor cheap insertion/deletion — pick based on your workload.
