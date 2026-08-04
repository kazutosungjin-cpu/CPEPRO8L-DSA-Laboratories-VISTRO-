class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self.items.pop()

    def peek(self):
        return self.items[-1] if not self.is_empty() else None

def is_balanced(expression):
    stack = Stack()
    bracket_map = {')': '(', '}': '{', ']': '['}
    
    for char in expression:
        if char in "({[":
            stack.push(char)
        elif char in ")}]":
            if stack.is_empty():
                return False
            if stack.pop() != bracket_map[char]:
                return False
                
    return stack.is_empty()

if __name__ == "__main__":
    expr1 = "{[()()]}"
    expr2 = "{[(])}"
    print(f"Is {expr1} balanced? {is_balanced(expr1)}") # Expected: True
    print(f"Is {expr2} balanced? {is_balanced(expr2)}") # Expected: False
