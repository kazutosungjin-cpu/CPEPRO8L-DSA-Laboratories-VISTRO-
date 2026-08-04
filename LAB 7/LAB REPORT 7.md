# Laboratory Activity No. 7 — Recursion Tracing & Binary Search

**Course Code:** CPEPRO8L
**Course Title:** Data Structures and Algorithms
**Term:** First Semester, AY 2026–2027

---

## 1. Objectives

1. Understand recursive execution, base cases, and call nesting.
2. Code and test recursive Binary Search.
3. Compare iterative and recursive space complexities.

---

## 2. Files

| File | Description |
|---|---|
| `lab7_recursive_search.py` | Completed `recursive_binary_search()` implementation, run against three targets: `23` (found), `56` (found), and `99` (not present). |
| `README.md` | This documentation file. |

---

## 3. Methodology

`recursive_binary_search(arr, low, high, target)` operates on the sorted array `data = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]` (indices `0`–`9`):

1. **Base case:** if `low > high`, the search space is empty — the target cannot be in the array, so the function returns `-1`.
2. It computes `mid = (low + high) // 2` and checks `arr[mid]`:
   - If `arr[mid] == target`, that index is the answer — return `mid`.
   - If `arr[mid] > target`, the target (if present) must be to the left, so the function calls itself on `(low, mid - 1)`.
   - Otherwise, the target must be to the right, so it calls itself on `(mid + 1, high)`.

Each recursive call halves the remaining search space, giving `O(log n)` time complexity. Because each call also adds a new frame to the call stack, it uses `O(log n)` **stack space** as well (see Section 5.2).

---

## 4. Execution & Output

Console capture from running `python3 lab7_recursive_search.py`:

```
Element found at index: 5
Element found at index: 7
Element found at index: -1
```

- `target_val = 23` → found at index `5`.
- `target_val_2 = 56` → found at index `7`.
- `target_val_3 = 99` → not in the array → base case returns `-1`.

---

## 5. Report Analysis Questions

### 5.1 Execution stack trace diagram — searching for `56`

Array: `data = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]` (10 elements, indices `0`–`9`).

**Call-by-call trace:**

| Call | Arguments `(low, high, target)` | `mid` | `arr[mid]` | Decision |
|---|---|---|---|---|
| 1 (initial) | `(0, 9, 56)` | 4 | 16 | `16 < 56` → recurse right: `(5, 9, 56)` |
| 2 | `(5, 9, 56)` | 7 | 56 | `56 == 56` → match, return `7` |

**Stack diagram** (frames pushed top-to-bottom as calls are made, then popped/returned bottom-to-top with their return values):

```
Call stack grows downward as recursion goes deeper:

┌────────────────────────────────────────────┐
│ Call 1: recursive_binary_search(arr,0,9,56) │   <- pushed first (outermost)
│   mid = 4, arr[4] = 16  (16 < 56 -> go right)
└──────────────────┬───────────────────────────┘
                    │ calls
                    ▼
┌────────────────────────────────────────────┐
│ Call 2: recursive_binary_search(arr,5,9,56) │   <- pushed second (innermost)
│   mid = 7, arr[7] = 56  (match!) -> return 7
└────────────────────────────────────────────┘

Unwinding (stack pops back up, return value flows back):

Call 2 returns 7  ─────►  Call 1 returns 7 (passes value straight through)  ─────►  result = 7
```

Since the target is found on only the second call, the recursion is shallow: the stack never grows beyond 2 frames deep for this particular search. Contrast this with searching for `23`, which needs 3 calls (`(0,9)` → `(5,9)` → `(5,6)`), or a worst-case search on a larger array, which would need up to `⌈log₂ n⌉` frames.

### 5.2 Why missing base cases lead to stack overflow errors

The base case (`if low > high: return -1`) is what tells the recursion **when to stop**. It's the only branch of the function that does *not* call `recursive_binary_search()` again — every other branch calls the function once more, just with a narrower `(low, high)` range.

If the base case were removed (or written incorrectly, e.g. checking the wrong condition so it never triggers), then:

- Every call would still compute `mid` and, if `arr[mid]` isn't the target, would call itself again — with no case that returns without recursing further.
- Even after `low` has already crossed past `high` (meaning the search space is logically empty), the function would keep calling itself with an ever-shrinking, invalid, or even out-of-bounds range, since nothing stops it from doing so.
- Each of those recursive calls pushes a **new stack frame** onto the call stack (holding its own copies of `arr`, `low`, `high`, `target`, and the return address). Because the recursion never terminates, frames keep being pushed and are never popped off.
- The call stack has a fixed, finite size (allocated by the operating system/interpreter for the program's execution). Once the number of nested, unreturned calls exceeds that limit, the program raises a **`RecursionError: maximum recursion depth exceeded`** in Python (equivalent to a **stack overflow** at the OS/runtime level in languages like C or Java).

In short: the base case is the exit condition that guarantees the recursion depth stays bounded (here, bounded by `O(log n)`, since the search space is halved each call). Without it, recursive calls accumulate stack frames indefinitely instead of unwinding, exhausting the available stack memory and crashing the program — which is exactly why every correct recursive function must have at least one reachable base case that does not recurse further.

---

## 6. Conclusion

The recursive Binary Search implementation correctly locates target elements (or reports their absence) in `O(log n)` time by repeatedly halving the search space, matching the behavior of its iterative counterpart while trading a small amount of stack space for simpler, more declarative code. The stack trace for searching `56` shows the recursion terminating quickly once a match is found, while the discussion of missing base cases illustrates why every recursive function must guarantee it reaches a non-recursive stopping condition.
