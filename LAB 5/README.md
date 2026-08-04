# Laboratory Activity No. 5 — Stack-Based Parenthesis & Arithmetic Parser

**Course Code:** CPEPRO8L
**Course Title:** Data Structures and Algorithms
**Term:** First Semester, AY 2026–2027

---

## 1. Objectives

1. Build a custom `Stack` class using a dynamic list.
2. Design an algorithm to check for balanced bracket pairs `()`, `[]`, `{}`.
3. Understand stack push/pop tracking in expression parsers.

---

## 2. Files

| File | Description |
|---|---|
| `lab5_bracket_parser.py` | Completed implementation of the `Stack` class and the `is_balanced()` bracket-matching function. |
| `README.md` | This documentation file. |

---

## 3. Methodology

The `Stack` class is implemented on top of a Python `list`:

- `push(item)` appends `item` to the end of the list (top of stack).
- `pop()` raises `IndexError("pop from empty stack")` if the stack is empty; otherwise it removes and returns the last item.
- `is_empty()` / `peek()` are used as helper/read-only operations.

`is_balanced(expression)` scans the expression left to right:

- Every **opening** bracket (`(`, `{`, `[`) is pushed onto the stack.
- Every **closing** bracket (`)`, `}`, `]`) triggers a pop:
  - If the stack is empty at that point, there is nothing to match → **unbalanced**.
  - If the popped symbol does not correspond to the closing bracket (via `bracket_map`), the pair is mismatched → **unbalanced**.
- After the scan, the expression is balanced **only if** the stack is empty (every opened bracket was eventually closed).

---

## 4. Execution & Output

Console capture from running `python3 lab5_bracket_parser.py`:

```
Is {[()()]} balanced? True
Is {[(])} balanced? False

--- Verification with 5 customized mathematical expressions ---
Test 1: '(a + b) * (c - d)'                 -> Balanced? True
Test 2: '[(x + y) * {z - 1}]'               -> Balanced? True
Test 3: '((a + b) * (c + d)'                -> Balanced? False
Test 4: '{[a + (b * c)] - d}'               -> Balanced? True
Test 5: '(a + [b * (c - d)])]'              -> Balanced? False
```

---

## 5. Report Analysis Questions

### 5.1 Verification against 5 customized mathematical expressions

| # | Expression | Expected | Result | Explanation |
|---|---|---|---|---|
| 1 | `(a + b) * (c - d)` | Balanced | **True** | Two independent, correctly closed `()` groups. |
| 2 | `[(x + y) * {z - 1}]` | Balanced | **True** | `(...)` and `{...}` are properly nested inside a single outer `[...]`. |
| 3 | `((a + b) * (c + d)` | Unbalanced | **False** | The outermost `(` is never closed — stack still holds `(` at the end. |
| 4 | `{[a + (b * c)] - d}` | Balanced | **True** | Three-level nesting `{ [ ( ) ] }`, each bracket closes in the correct order. |
| 5 | `(a + [b * (c - d)])]` | Unbalanced | **False** | An extra, unmatched `]` appears after the expression is already fully closed — the stack is empty when `]` is scanned, so it fails immediately. |

All five results match the expected outcomes, confirming that the algorithm correctly handles nested brackets, unmatched opening brackets, and unmatched/extra closing brackets.

### 5.2 Stack state trace for `"{[()]}"`

| Step | Char read | Action | Stack (bottom → top) | Notes |
|---|---|---|---|---|
| 0 | — | initial | `[ ]` | Stack starts empty. |
| 1 | `{` | push `{` | `[ { ]` | Opening bracket → pushed. |
| 2 | `[` | push `[` | `[ {, [ ]` | Opening bracket → pushed. |
| 3 | `(` | push `(` | `[ {, [, ( ]` | Opening bracket → pushed. |
| 4 | `)` | pop → `(` | `[ {, [ ]` | Closing bracket; popped `(` matches `)` via `bracket_map`. |
| 5 | `]` | pop → `[` | `[ { ]` | Closing bracket; popped `[` matches `]`. |
| 6 | `}` | pop → `{` | `[ ]` | Closing bracket; popped `{` matches `}`. |
| — | — | end of string | `[ ]` (empty) | `stack.is_empty()` is `True` → **`is_balanced("{[()]}")` returns `True`**. |

Visual push/pop trace (top of stack on the right):

```
Step 1 (push {):  [ { ]
Step 2 (push [):  [ {  [ ]
Step 3 (push ():  [ {  [  ( ]
Step 4 (pop  )):  [ {  [ ]        <- ( removed, matched with )
Step 5 (pop  ]):  [ { ]           <- [ removed, matched with ]
Step 6 (pop  }):  [ ]             <- { removed, matched with }
```

The stack grows by one element for every opening bracket and shrinks by one for every matching closing bracket, ending empty exactly when the expression is fully balanced — demonstrating the Last-In-First-Out (LIFO) property that makes stacks well-suited for this kind of nested-structure validation.

---

## 6. Conclusion

The `Stack` class and `is_balanced()` function correctly identify balanced and unbalanced bracket sequences, including mismatched pairs, unclosed openings, and extra unmatched closings. Testing against the two provided samples plus five additional customized mathematical expressions confirms the implementation behaves as expected in all cases.
