"""Controlled benchmark. Run: python benchmark_sorts.py

Fairness controls
  * One source dataset per (size, condition), generated once with a fixed seed.
  * Every algorithm and every trial receives a fresh copy of that same data
    (the copy happens inside the sort function, outside the timed region's
    setup of the data itself; generation is never timed).
  * 5 timed trials per (algorithm, condition, size); the MEDIAN is reported.
  * time.perf_counter() around the sort call only.
  * Counters are active in every run (same small overhead for all algorithms).
  * Quadratic algorithms are skipped for a larger size if the previous size's
    median exceeded TIME_LIMIT seconds; the skip is recorded in the CSV.
"""
import csv
import random
import statistics
import time

from sorting_algorithms import ALGORITHMS

SIZES = [500, 1000, 2000, 4000]
TRIALS = 5
SEED = 11
TIME_LIMIT = 5.0            # seconds per run (approved limit assumed)
QUADRATIC = {"Bubble Sort", "Selection Sort", "Insertion Sort"}
CONDITIONS = ["random", "sorted", "reverse", "duplicate-heavy"]


def make_data(condition, n, rng):
    if condition == "random":
        return [rng.randint(0, n * 10) for _ in range(n)]
    if condition == "sorted":
        return list(range(n))
    if condition == "reverse":
        return list(range(n, 0, -1))
    if condition == "duplicate-heavy":
        return [rng.randint(0, 9) for _ in range(n)]
    raise ValueError(condition)


def main():
    rng = random.Random(SEED)
    rows = []
    last_median = {}
    for n in SIZES:
        for cond in CONDITIONS:
            source = make_data(cond, n, rng)
            expected = sorted(source)            # reference, not timed
            for name, fn in ALGORITHMS.items():
                key = (name, cond)
                if name in QUADRATIC and last_median.get(key, 0) > TIME_LIMIT:
                    rows.append([name, cond, n, "", "", "", "SKIPPED",
                                 f"previous median > {TIME_LIMIT}s limit"])
                    print(f"{name:15} {cond:16} n={n:<6} SKIPPED")
                    continue
                times = []
                for _ in range(TRIALS):
                    t0 = time.perf_counter()
                    out, stats = fn(source)
                    times.append(time.perf_counter() - t0)
                    assert out == expected, f"{name} wrong on {cond} n={n}"
                med = statistics.median(times)
                last_median[key] = med
                rows.append([name, cond, n, f"{med:.6f}", stats.comparisons,
                             stats.moves, "OK", ""])
                print(f"{name:15} {cond:16} n={n:<6} {med*1000:10.2f} ms "
                      f"cmp={stats.comparisons} mov={stats.moves}")
    with open("benchmark_results.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["algorithm", "condition", "n", "median_seconds",
                    "comparisons", "moves", "status", "note"])
        w.writerows(rows)
    print("Wrote benchmark_results.csv")


if __name__ == "__main__":
    main()
