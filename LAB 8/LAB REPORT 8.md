# Laboratory Activity No. 8 — Binary Search Tree Insertion and Traversals

**Course Code:** CPEPRO8L
**Course Title:** Data Structures and Algorithms
**Term:** First Semester, AY 2026–2027

## 1. Objectives

1. Implement dynamic tree nodes with left and right child references.
2. Build insertion and lookup functions in a Binary Search Tree (BST).
3. Implement Inorder, Preorder, and Postorder recursive tree traversals.

## 2. Implementation Summary

The `BST` class stores keys in nodes such that, for every node, all keys in
its left subtree are smaller and all keys in its right subtree are greater
than or equal to the node's key. Three recursive methods were implemented:

- **`_insert_recursive(node, key)`** — compares `key` against `node.key`.
  If `key` is smaller, it descends into (or creates) the left child;
  otherwise it descends into (or creates) the right child. Recursion
  terminates once an empty (`None`) child slot is found, which becomes the
  insertion point.
- **`inorder(node)`** — recursively visits Left → Node → Right.
- **`preorder(node)`** — recursively visits Node → Left → Right.
- **`postorder(node)`** — recursively visits Left → Right → Node.

All three traversals use `if node:` as the base case, so recursion stops
naturally at empty subtrees without extra checks.

## 3. Execution & Output

**Test data (insertion order):** `50, 30, 70, 20, 40, 60, 80`

Resulting tree structure:

```
                50
              /    \
            30      70
           /  \    /  \
         20   40  60   80
```

**Console capture:**

```
— python3 lab8_bst.py
Inorder Traversal:
20 30 40 50 60 70 80 
Preorder Traversal:
50 30 20 40 70 60 80 
Postorder Traversal:
20 40 30 60 80 70 50 
```

| Traversal | Order Rule        | Output                        |
|-----------|--------------------|--------------------------------|
| Inorder   | Left → Node → Right | 20 30 40 50 60 70 80          |
| Preorder  | Node → Left → Right | 50 30 20 40 70 60 80          |
| Postorder | Left → Right → Node | 20 40 30 60 80 70 50          |

The inorder result matches the expected sorted sequence, confirming the
insertion logic is correct.

## 4. Report Analysis Questions

### 4.1 Preorder and Postorder outputs for the test tree

- **Preorder:** `50 30 20 40 70 60 80`
- **Postorder:** `20 40 30 60 80 70 50`

### 4.2 Why does the inorder traversal of a BST output items in sorted order?

Inorder traversal visits nodes in the sequence **Left subtree → Node →
Right subtree**. This matches the structural invariant that defines a BST:
for every node, all keys in its left subtree are smaller than the node's
key, and all keys in its right subtree are greater than (or equal to) it.

Because this invariant holds recursively at every node in the tree, the
traversal produces sorted output at every level:

1. At the root, inorder first fully traverses the left subtree — which by
   the BST property contains only smaller keys — before visiting the root
   itself.
2. It then visits the root's key.
3. Finally, it traverses the right subtree, which by the BST property
   contains only larger keys.

Since this same left-smaller / right-larger relationship applies
recursively to every subtree (each subtree is itself a valid BST), the
"smaller keys, then current key, then larger keys" pattern repeats at
every level of recursion. The cumulative effect across the whole tree is
that keys are emitted in strictly non-decreasing order — i.e., sorted
order — with no additional comparison or sorting step required. This is
precisely what the test run demonstrates: `20 30 40 50 60 70 80`.
