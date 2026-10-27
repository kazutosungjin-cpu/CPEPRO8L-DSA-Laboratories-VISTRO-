"""Correctness tests. Run: python test_sorts.py   (or python -m unittest -v)"""
import random
import unittest

from sorting_algorithms import ALGORITHMS


def reference_sorted(data):
    """Independent reference: simple counting-free check using the built-in
    sorted(). Used ONLY here, never inside the algorithms."""
    return sorted(data)


def make_datasets():
    rng = random.Random(11)
    return {
        "empty": [],
        "one item": [42],
        "two items": [2, 1],
        "all duplicates": [7] * 50,
        "many duplicates": [rng.randint(0, 4) for _ in range(200)],
        "already sorted": list(range(100)),
        "reverse sorted": list(range(100, 0, -1)),
        "random": [rng.randint(-1000, 1000) for _ in range(300)],
        "negatives": [-5, 3, -1, 0, -5, 9, 3],
    }


class TestSorts(unittest.TestCase):
    def test_all(self):
        for name, fn in ALGORITHMS.items():
            for dname, data in make_datasets().items():
                with self.subTest(algorithm=name, dataset=dname):
                    original = list(data)
                    result, stats = fn(data)
                    self.assertEqual(result, reference_sorted(original))
                    self.assertEqual(data, original, "input was modified")
                    self.assertGreaterEqual(stats.comparisons, 0)

    def test_random_fuzz(self):
        rng = random.Random(2026)
        for name, fn in ALGORITHMS.items():
            for _ in range(100):
                data = [rng.randint(0, 20) for _ in range(rng.randint(0, 60))]
                with self.subTest(algorithm=name):
                    self.assertEqual(fn(data)[0], reference_sorted(data))

    def test_stability_of_stable_sorts(self):
        class Item:
            def __init__(self, k, tag): self.k, self.tag = k, tag
            def __lt__(self, o): return self.k < o.k
            def __gt__(self, o): return self.k > o.k
        data = [Item(k, i) for i, k in enumerate([3, 1, 3, 1, 2, 3, 1])]
        for name in ("Bubble Sort", "Insertion Sort", "Merge Sort"):
            out, _ = ALGORITHMS[name](data)
            for x, y in zip(out, out[1:]):
                if x.k == y.k:
                    self.assertLess(x.tag, y.tag, f"{name} not stable")


if __name__ == "__main__":
    unittest.main(verbosity=2)
