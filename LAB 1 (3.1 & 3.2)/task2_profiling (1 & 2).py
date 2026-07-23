import time

# O(1) Constant Time Function
def constant_time_check(arr):
    # Returns the first element of the array
    return arr[0] if len(arr) > 0 else None

# O(n) Linear Time Function
def linear_time_sum(arr):
    total = 0
    for value in arr:
        total += value
    return total

# O(n^2) Quadratic Time Function
def quadratic_time_pairs(arr):
    pair_sum = 0
    n = len(arr)
    for i in range(n):
        for j in range(n):
            pair_sum += (arr[i] * arr[j])
    return pair_sum

# Benchmarking Logic
N_values = [100, 500, 1000, 5000, 10000]
results = []

for n in N_values:
    test_list = list(range(n))
    print(f"\n--- Benchmarking N = {n} ---")

    # 1. Profile O(1)
    start = time.perf_counter()
    constant_time_check(test_list)
    t_constant = (time.perf_counter() - start) * 1_000_000  # microseconds

    # 2. Profile O(n)
    start = time.perf_counter()
    linear_time_sum(test_list)
    t_linear = (time.perf_counter() - start) * 1_000_000

    # 3. Profile O(n^2)
    # Hint: Skip N = 10000 for O(n^2) if it runs too slowly on your system!
    if n <= 5000:
        start = time.perf_counter()
        quadratic_time_pairs(test_list)
        t_quadratic = (time.perf_counter() - start) * 1_000_000
        q_text = f"{t_quadratic:.2f} us"
    else:
        q_text = "SKIPPED (too slow)"

    print(f"Constant time: {t_constant:.2f} us")
    print(f"Linear time:   {t_linear:.2f} us")
    print(f"Quadratic time: {q_text}")

    results.append((n, t_constant, t_linear, q_text))

print("\n1.")
print("\nComparative Benchmark Table")
print(f"{'N':<10} {'Constant (O(1))':<18} {'Linear (O(n))':<18} {'Quadratic (O(n²))':<20}")
print("-" * 70)
for n, t_constant, t_linear, q_text in results:
    print(f"{n:<10} {f'{t_constant:.2f} us':<18} {f'{t_linear:.2f} us':<18} {q_text:<20}")

print("\n2.")
print("\nRuntime Comparison Summary")
print(f"{'N':<10} {'Linear vs Quadratic':<25} {'Observation':<30}")
print("-" * 70)
for n, _, t_linear, q_text in results:
    if q_text != "SKIPPED (too slow)":
        q_value = float(q_text.replace(" us", ""))
        if t_linear > 0:
            ratio = q_value / t_linear
        else:
            ratio = float("inf")
        print(f"{n:<10} {ratio:>10.2f}x            {'Quadratic grows much faster'}")
    else:
        print(f"{n:<10} {'N/A':>10}            {'Quadratic test skipped'}")

print("\nObservation:")
print("As N increases, the quadratic function grows much faster than the linear function.")
print("This is because the quadratic algorithm performs roughly N² operations, while the linear one performs about N operations.")