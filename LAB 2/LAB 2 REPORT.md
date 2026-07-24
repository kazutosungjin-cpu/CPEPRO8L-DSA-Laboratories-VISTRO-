# Lab Report: Dynamic Array Builder & Capacity Allocation

## Objectives

1. Implement a custom dynamic array class from scratch using Python's
   `ctypes` module.
2. Understand capacity scaling, memory doubling, and the cost of element
   copying.
3. Observe how index search works in O(1) constant time complexity.

## Files

| File | Description |
|---|---|
| `lab2_dynamic_array.py` | Custom `DynamicArray` class backed by a `ctypes` array, with resize-on-append logic and a 10-element test run. |

The file was run successfully with no errors.

---

## Execution & Output

```
1.
Appending 0 | Size: 1 | Capacity: 1 | Element at index 0: 0
Resizing from 1 to 2
Appending 1 | Size: 2 | Capacity: 2 | Element at index 1: 1
Resizing from 2 to 4
Appending 2 | Size: 3 | Capacity: 4 | Element at index 2: 2
Appending 3 | Size: 4 | Capacity: 4 | Element at index 3: 3
Resizing from 4 to 8
Appending 4 | Size: 5 | Capacity: 8 | Element at index 4: 4
Appending 5 | Size: 6 | Capacity: 8 | Element at index 5: 5
Appending 6 | Size: 7 | Capacity: 8 | Element at index 6: 6
Appending 7 | Size: 8 | Capacity: 8 | Element at index 7: 7
Resizing from 8 to 16
Appending 8 | Size: 9 | Capacity: 16 | Element at index 8: 8
Appending 9 | Size: 10 | Capacity: 16 | Element at index 9: 9
```

---

## Report Analysis Questions

### 1. Source Code

`lab2_dynamic_array.py` is included with this submission and was verified
to run without errors (see Execution & Output above for the actual
console capture).

### 2. Resize Trace — Exact Sizes Where Capacity Resizes Occur

Running the script with 10 appends (elements 0–9), resizing (capacity
doubling) occurred at these exact sizes:

| Size at resize | Capacity change |
|---|---|
| Size 1 | Capacity resized from 1 to 2 |
| Size 2 | Capacity resized from 2 to 4 |
| Size 4 | Capacity resized from 4 to 8 |
| Size 8 | Capacity resized from 8 to 16 |

### 3. Conclusions

Because the dynamic array needs to allocate a new block of memory with
double the capacity, it must copy all existing elements from the old
array to the new one. This ensures that the elements are preserved and
accessible in the new array. The time complexity of a single resize
operation is O(n), where n is the number of elements in the array at the
time of resizing, because each element must be copied to the new array.
