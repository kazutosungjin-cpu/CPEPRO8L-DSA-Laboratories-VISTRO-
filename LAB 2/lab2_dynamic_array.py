print("\n1.")

import ctypes

class DynamicArray:
    def __init__(self):
        self.size = 0  # number of elements
        self.capacity = 1  # initial capacity
        self.array = self._make_array(self.capacity)

    def __len__(self):
        return self.size

    def __getitem__(self, index):
        
        if not 0 <= index < self.size:
            raise IndexError("Index out of bounds")
        return self.array[index]

    def append(self, element):
       
        if self.size == self.capacity:
            self._resize(2 * self.capacity)
        self.array[self.size] = element
        self.size += 1

    def _resize(self, new_capacity):
        
        print(f"Resizing from {self.capacity} to {new_capacity}")
        new_array = self._make_array(new_capacity)
        for i in range(self.size):
            new_array[i] = self.array[i]
        self.array = new_array
        self.capacity = new_capacity

    def _make_array(self, new_capacity):
        return (new_capacity * ctypes.py_object)()

# Testing script
if __name__ == "__main__":
    arr = DynamicArray()
    for i in range(10):
        arr.append(i)
        print(f"Appending {i} | Size: {len(arr)} | Capacity: {arr.capacity} | Element at index {i}: {arr[i]}")




