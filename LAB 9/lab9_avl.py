class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

    def rotate_right(self, y):
        x = y.left
        t2 = x.right

        # Perform rotation
        x.right = y
        y.left = t2

        # Update heights (y first, since it's now lower in the tree)
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))

        # x is the new root of this subtree
        return x

    def rotate_left(self, x):
        y = x.right
        t2 = y.left

        # Perform rotation
        y.left = x
        x.right = t2

        # Update heights (x first, since it's now lower in the tree)
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        # y is the new root of this subtree
        return y

    def insert(self, root, key):
        # 1. Standard BST insertion
        if root is None:
            return AVLNode(key)
        if key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        # 2. Update height of this ancestor node
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        # 3. Get the balance factor to check whether this node became unbalanced
        balance = self.get_balance(root)

        # 4. Balancing cases

        # Left Left Case
        if balance > 1 and key < root.left.key:
            return self.rotate_right(root)

        # Right Right Case
        if balance < -1 and key >= root.right.key:
            return self.rotate_left(root)

        # Left Right Case
        if balance > 1 and key >= root.left.key:
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)

        # Right Left Case
        if balance < -1 and key < root.right.key:
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)

        # No rotation needed, return unchanged node pointer
        return root

    def inorder(self, node, result=None):
        if result is None:
            result = []
        if node:
            self.inorder(node.left, result)
            result.append(node.key)
            self.inorder(node.right, result)
        return result

    def preorder(self, node, result=None):
        if result is None:
            result = []
        if node:
            result.append(node.key)
            self.preorder(node.left, result)
            self.preorder(node.right, result)
        return result


if __name__ == "__main__":
    tree = AVLTree()
    root = None

    print("=== Trace: inserting [10, 20, 30] sequentially ===")
    keys = [10, 20, 30]
    for k in keys:
        root = tree.insert(root, k)
        print(f"After inserting {k}: preorder = {tree.preorder(root)}, "
              f"root = {root.key}, root height = {root.height}, "
              f"root balance = {tree.get_balance(root)}")

    print()
    print("Final inorder traversal:", tree.inorder(root))
    print("Final preorder traversal (shows structure):", tree.preorder(root))
    print(f"Final root: {root.key} | left: "
          f"{root.left.key if root.left else None} | right: "
          f"{root.right.key if root.right else None}")

    print()
    print("=== Larger demonstration: inserting [50, 30, 70, 20, 40, 60, 80, 10, 25] ===")
    root2 = None
    for k in [50, 30, 70, 20, 40, 60, 80, 10, 25]:
        root2 = tree.insert(root2, k)
    print("Inorder:", tree.inorder(root2))
    print("Preorder:", tree.preorder(root2))
    print(f"Root: {root2.key}, height: {root2.height}, balance: {tree.get_balance(root2)}")
