# Task 1: Mutable references tracing
print("--- TASK 1: OBJECT ID COMPARISON ---")

list_a = [10, 20, 30]
list_b = list_a  # Copying the reference 

print(f"Address of list_a (id): {id(list_a)}")
print(f"Address of list_b (id): {id(list_b)}")
print(f"Are list_a and list_b pointing to the same object? {list_a is list_b}")

# Mutating list_b
list_b = [100, 200]
print(f"\nAfter appending 40 to list_b:")
print(f"list_a: {list_a}")
print(f"list_b: {list_b}")

# 2.   What happens to the memory reference if you assign a new list to list_b using list_b = [100, 200]? Explain using the output of id(). 
# When you change the list of list_b using list_b = [100, 200] it changes it becoming list_b = [100,200, 40], This means that list_b now points to a completely new list object in memory, while list_a still the same list_a = [10, 20, 30, 40].