# Task 1: Mutable references tracing
print("\n--- TASK 1 (Q1): OBJECT ID COMPARISON ---")
print("\n")
list_a = [10, 20, 30]
list_b = list_a  # Copying the reference

print(f"Address of list_a (id): {id(list_a)}")
print(f"Address of list_b (id): {id(list_b)}")
print(f"Are list_a and list_b pointing to the same object? {list_a is list_b}")

# Mutating list_b
list_b.append(40)
print(f"\nAfter appending 40 to list_b:")
print(f"list_a: {list_a}")
print(f"list_b: {list_b}")

# 1.   Why did the value of list_a change when you appended a number to list_b?

# list_a changed because list_b = list_a does not create a new, separate list — it just makes list_b point to the same list object in memory that list_a already points to.


print("\n--- TASK 1( Q2): OBJECT ID COMPARISON ---")
print("\n")
list_a = [10, 20, 30]
list_b = list_a  # Copying the reference

# Reassigning list_b to a brand new list
list_b = [100, 200]

print(f"Address of list_a (id): {id(list_a)}")
print(f"Address of list_b (id): {id(list_b)}")
print(f"list_a: {list_a}")
print(f"list_b: {list_b}")
print(f"Are list_a and list_b pointing to the same object? {list_a is list_b}")

# 2.   What happens to the memory reference if you assign a new list to list_b using list_b = [100, 200]? Explain using the output of id(). 

# When list_b = [100, 200] runs, list_b now points to a new object in memory, while list_a still points to the original [10, 20, 30]. The id() output confirms this — list_a and list_b now have different addresses, meaning they are separate objects.