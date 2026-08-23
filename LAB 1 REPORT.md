# Lab Report: Object References & Performance Profiling in Python

## Objectives

- **Task 1 — Object References:** Understand how Python variables work as
  references (names bound to objects, not containers), and use `id()` and
  the `is` operator to trace what happens in memory when references are
  copied versus when a variable is reassigned to a new object.
- **Task 2 — Profiling:** Measure and compare the execution time of three
  functions with different time complexities — O(1), O(n), and O(n²) — for
  increasing values of *N*, and connect the measured timings back to
  Big-O notation.

## Files

| File | Description |
|---|---|
| `task1_references.py` | Demonstrates reference aliasing vs. reassignment using `id()` and `is`. |
| `task2_profiling.py` | Benchmarks constant, linear, and quadratic functions across five values of N. |

Both files were run successfully with no errors.

---

## Execution & Output

### Task 1: `task1_references.py`

```
--- TASK 1 (Q1): OBJECT ID COMPARISON ---

Address of list_a (id): 140099179055936
Address of list_b (id): 140099179055936
Are list_a and list_b pointing to the same object? True

After appending 40 to list_b:
list_a: [10, 20, 30, 40]
list_b: [10, 20, 30, 40]

--- TASK 1 (Q2): OBJECT ID COMPARISON ---

Address of list_a (id): 140099174703744
Address of list_b (id): 140099179055936
list_a: [10, 20, 30]
list_b: [100, 200]
Are list_a and list_b pointing to the same object? False
```

### Task 2: `task2_profiling.py`

```
--- Benchmarking N = 100 ---
Constant time: 4.31 us
Linear time:   7.87 us
Quadratic time: 780.05 us

--- Benchmarking N = 500 ---
Constant time: 2.33 us
Linear time:   17.07 us
Quadratic time: 34302.11 us

--- Benchmarking N = 1000 ---
Constant time: 4.52 us
Linear time:   34.00 us
Quadratic time: 107723.99 us

--- Benchmarking N = 5000 ---
Constant time: 4.15 us
Linear time:   176.68 us
Quadratic time: 2249498.96 us

--- Benchmarking N = 10000 ---
Constant time: 3.85 us
Linear time:   416.40 us
Quadratic time: SKIPPED (too slow)
```

---

## Report Analysis Questions

### 1. Source Code

Both `task1_references.py` and `task2_profiling.py` are included with this
submission and were verified to run without errors (see Execution & Output
above for the actual console captures).

### 2. Analysis — Execution Time Table

**Comparative Benchmark Table (Task 2, TR1)**

| N | Constant O(1) | Linear O(n) | Quadratic O(n²) |
|---|---|---|---|
| 100 | 4.31 µs | 7.87 µs | 780.05 µs |
| 500 | 2.33 µs | 17.07 µs | 34,302.11 µs |
| 1,000 | 4.52 µs | 34.00 µs | 107,723.99 µs |
| 5,000 | 4.15 µs | 176.68 µs | 2,249,498.96 µs |
| 10,000 | 3.85 µs | 416.40 µs | *skipped (too slow)* |

**Runtime Comparison Summary (Task 2, TR2)**

| N | Quadratic ÷ Linear | Observation |
|---|---|---|
| 100 | 99.13× | Quadratic grows much faster |
| 500 | 2,008.91× | Quadratic grows much faster |
| 1,000 | 3,168.35× | Quadratic grows much faster |
| 5,000 | 12,732.41× | Quadratic grows much faster |
| 10,000 | N/A | Quadratic test skipped |

### 3. Conclusions

**Object references**

In Python, variables point to objects rather than storing data directly.
Assigning one variable to another (`list_b = list_a`) makes both point to
the same object, so changes through one affect the other. Understanding
this prevents accidental data mutation bugs, especially in complex
structures like linked lists or trees.

**Big-O and real speed**

The profiling results confirm Big-O predictions hold in practice —
Constant time stayed flat, Linear time grew proportionally with N, and
Quadratic time grew proportionally with N² (e.g., a 5x increase in N
caused a ~25x increase in Quadratic time). This shows why complexity
analysis matters: as data grows, O(n²) algorithms become impractically
slow while O(n) or O(1) ones stay efficient.
