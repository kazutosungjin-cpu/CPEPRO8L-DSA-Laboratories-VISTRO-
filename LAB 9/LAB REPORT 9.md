# Laboratory Activity No. 9 — Height Balancing in AVL Trees

**Course Code:** CPEPRO8L
**Course Title:** Data Structures and Algorithms
**Term:** First Semester, AY 2026–2027

## 1. Objectives

1. Calculate height metrics and balance factors dynamically.
2. Implement Single and Double Rotations (LL, RR, LR, RL cases).
3. Demonstrate self-balancing tree insertions.

## 2. Implementation Summary

An **AVL Tree** is a self-balancing BST that keeps the balance factor of
every node — `height(left subtree) - height(right subtree)` — within
`[-1, 1]`. Whenever an insertion pushes a node's balance factor outside
that range, one of four rotation cases restores balance:

| Case | Condition | Fix |
|------|-----------|-----|
| Left-Left (LL) | balance > 1, new key < left child's key | single right rotation |
| Right-Right (RR) | balance < -1, new key ≥ right child's key | single left rotation |
| Left-Right (LR) | balance > 1, new key ≥ left child's key | left rotation on left child, then right rotation |
| Right-Left (RL) | balance < -1, new key < right child's key | right rotation on right child, then left rotation |

**`rotate_right(y)`** — promotes `y`'s left child (`x`) to take `y`'s
place. `x`'s original right subtree (`T2`) is reattached as `y`'s new
left subtree, since every key in `T2` is still greater than `x` and less
than `y`. Heights are recalculated bottom-up (`y` first, then `x`, since
`y` is now the lower node).

**`rotate_left(x)`** — the mirror image: promotes `x`'s right child (`y`)
to take `x`'s place, reattaching `y`'s original left subtree (`T2`) as
`x`'s new right subtree.

**`insert(root, key)`** — performs a standard recursive BST insertion,
then on the way back up the recursion: updates the current node's
height, computes its balance factor, and applies the matching rotation
case from the table above if the node is unbalanced.

### Sequence diagram of a right rotation

```
Before rotate_right(y):              After rotate_right(y):

        y                                     x
       / \                                   / \
      x   T3                               T1    y
     / \          -- rotate_right(y) -->        / \
   T1   T2                                     T2   T3

Step-by-step:
1. x = y.left                  (x becomes the pivot)
2. T2 = x.right                (save x's right subtree)
3. x.right = y                 (y drops down to become x's right child)
4. y.left = T2                 (T2 reattaches as y's new left subtree)
5. recompute height(y), then height(x)
6. return x                    (x is the new subtree root)
```

`rotate_left` is the exact mirror: pivot on `x.right`, save its left
subtree, and swing `x` down to the left.

## 3. Execution & Output

### Trace: inserting [10, 20, 30] sequentially

Inserting keys in strictly ascending order is the classic case that
triggers a **left rotation** (RR case), since every new key lands in the
rightmost position and the tree grows into a right-leaning chain.

```
$ python3 lab9_avl.py
=== Trace: inserting [10, 20, 30] sequentially ===
After inserting 10: preorder = [10], root = 10, root height = 1, root balance = 0
After inserting 20: preorder = [10, 20], root = 10, root height = 2, root balance = -1
After inserting 30: preorder = [20, 10, 30], root = 20, root height = 2, root balance = 0
```

**Step-by-step trace:**

1. **Insert 10** → tree is just `10`. Balanced (balance factor 0).
   ```
   10
   ```
2. **Insert 20** → 20 attaches as `10`'s right child. Root `10` now has
   height 2 and balance factor `0 - 1 = -1`. Still within `[-1, 1]`, so
   no rotation yet.
   ```
   10
     \
      20
   ```
3. **Insert 30** → 30 attaches as `20`'s right child. Walking back up to
   root `10`: its balance factor becomes `0 - 2 = -2`, which is outside
   `[-1, 1]` → **unbalanced**. Since `30 ≥ 20` (the right child's key),
   this is the **Right-Right (RR) case**, corrected with a single
   **left rotation** on `10`.

   ```
   Before rotate_left(10):        After rotate_left(10):

    10                                    20
      \                                  /  \
       20        -- rotate_left -->   10    30
         \
          30
   ```

   `20` becomes the new subtree root, with `10` as its left child and
   `30` as its right child — a perfectly balanced tree of height 2.

Final structure confirmed by the program:

```
Final inorder traversal: [10, 20, 30]
Final preorder traversal (shows structure): [20, 10, 30]
Final root: 20 | left: 10 | right: 30
```

### Larger demonstration

To confirm the implementation generalizes beyond the 3-key trace, the
same tree was built from `[50, 30, 70, 20, 40, 60, 80, 10, 25]`:

```
=== Larger demonstration: inserting [50, 30, 70, 20, 40, 60, 80, 10, 25] ===
Inorder: [10, 20, 25, 30, 40, 50, 60, 70, 80]
Preorder: [50, 30, 20, 10, 25, 40, 70, 60, 80]
Root: 50, height: 4, balance: 1
```

The inorder traversal is correctly sorted, and the tree's height (4) is
close to the theoretical minimum for 9 nodes (`⌈log₂(9+1)⌉ = 4`),
confirming the AVL property is being maintained as more keys are
inserted.

## 4. Report Analysis Questions

### 4.1 AVL insertion and rotation routines, with a right-rotation sequence diagram

The insertion and rotation routines are implemented in `lab9_avl.py`
(see Section 2 above for the algorithm and the sequence diagram of
`rotate_right`).

### 4.2 Trace of inserting [10, 20, 30] and the automatic left rotation

See the full step-by-step trace in Section 3. In summary: inserting
`10`, then `20`, then `30` in ascending order makes every new node
attach to the right, degrading the tree toward a linked list. After
inserting `30`, the root (`10`)'s balance factor drops to `-2`, which
violates the AVL invariant. Because the new key (`30`) is greater than
or equal to the unbalanced node's right child's key (`20`), this is
classified as the **Right-Right case**, and a single **left rotation**
on the root automatically restores balance — producing the balanced
tree `20` (root) with `10` and `30` as its children.
