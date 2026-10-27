"""Six sorting algorithms with comparison and data-movement counters.

Every function takes a list, leaves the input untouched (works on a copy),
and returns ``(sorted_list, stats)`` where ``stats`` is a ``Stats`` object.

Counting convention
    comparisons: every comparison between two data items.
    moves:       every write of a data item into a list slot
                 (a swap counts as 2 moves).

Python's built-in sorted()/list.sort() are NOT used anywhere in this module.
"""


class Stats:
    """Counts comparisons and data movements."""

    __slots__ = ("comparisons", "moves")

    def __init__(self):
        self.comparisons = 0
        self.moves = 0


def bubble_sort(data):
    """Bubble Sort with early exit. Stable, in place (O(1) extra space)."""
    a, s = list(data), Stats()
    n = len(a)
    for end in range(n - 1, 0, -1):
        swapped = False
        for i in range(end):
            s.comparisons += 1
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                s.moves += 2
                swapped = True
        if not swapped:          # already sorted -> O(n) best case
            break
    return a, s


def selection_sort(data):
    """Selection Sort. Not stable, in place. Always ~n^2/2 comparisons."""
    a, s = list(data), Stats()
    n = len(a)
    for i in range(n - 1):
        m = i
        for j in range(i + 1, n):
            s.comparisons += 1
            if a[j] < a[m]:
                m = j
        if m != i:
            a[i], a[m] = a[m], a[i]
            s.moves += 2
    return a, s


def insertion_sort(data):
    """Insertion Sort. Stable, in place, O(n) on already sorted input."""
    a, s = list(data), Stats()
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0:
            s.comparisons += 1
            if a[j] > key:
                a[j + 1] = a[j]
                s.moves += 1
                j -= 1
            else:
                break
        a[j + 1] = key
        s.moves += 1
    return a, s


def merge_sort(data):
    """Top-down Merge Sort. Stable. O(n) auxiliary space (one buffer)."""
    a, s = list(data), Stats()
    buf = a[:]                   # single reusable auxiliary buffer

    def sort(lo, hi):            # sorts a[lo:hi]
        if hi - lo < 2:
            return
        mid = (lo + hi) // 2
        sort(lo, mid)
        sort(mid, hi)
        i, j, k = lo, mid, lo
        while i < mid and j < hi:
            s.comparisons += 1
            if a[j] < a[i]:
                buf[k] = a[j]
                j += 1
            else:                # ties take the left item -> stable
                buf[k] = a[i]
                i += 1
            k += 1
            s.moves += 1
        while i < mid:
            buf[k] = a[i]; i += 1; k += 1; s.moves += 1
        while j < hi:
            buf[k] = a[j]; j += 1; k += 1; s.moves += 1
        for k in range(lo, hi):  # copy back
            a[k] = buf[k]
            s.moves += 1

    sort(0, len(a))
    return a, s


def quick_sort(data):
    """Quick Sort: median-of-three pivot + three-way (Dutch flag) partition.

    Pivot strategy: median of first, middle and last item. This avoids the
    O(n^2) behaviour a first/last-element pivot has on sorted and reverse
    sorted data. Three-way partitioning groups all items equal to the pivot,
    so duplicate-heavy data does not degrade.
    Space: in place; recursion goes into the smaller side and loops on the
    larger side, so stack depth is O(log n). Not stable.
    """
    a, s = list(data), Stats()

    def median_of_three(lo, hi):
        mid = (lo + hi) // 2
        x, y, z = a[lo], a[mid], a[hi]
        s.comparisons += 3
        if x < y:
            if y < z: return y
            return z if x < z else x
        if x < z: return x
        return z if y < z else y

    def sort(lo, hi):            # inclusive bounds
        while lo < hi:
            p = median_of_three(lo, hi)
            lt, i, gt = lo, lo, hi
            while i <= gt:
                s.comparisons += 1
                if a[i] < p:
                    a[lt], a[i] = a[i], a[lt]
                    s.moves += 2
                    lt += 1; i += 1
                else:
                    s.comparisons += 1
                    if a[i] > p:
                        a[i], a[gt] = a[gt], a[i]
                        s.moves += 2
                        gt -= 1
                    else:
                        i += 1
            # a[lo:lt] < p, a[lt:gt+1] == p, a[gt+1:hi+1] > p
            if lt - lo < hi - gt:
                sort(lo, lt - 1)
                lo = gt + 1
            else:
                sort(gt + 1, hi)
                hi = lt - 1

    sort(0, len(a) - 1)
    return a, s


def heap_sort(data):
    """Heap Sort with a max-heap. In place, not stable, O(n log n) worst case."""
    a, s = list(data), Stats()
    n = len(a)

    def sift_down(root, size):
        while True:
            child = 2 * root + 1
            if child >= size:
                return
            if child + 1 < size:
                s.comparisons += 1
                if a[child + 1] > a[child]:
                    child += 1
            s.comparisons += 1
            if a[child] > a[root]:
                a[root], a[child] = a[child], a[root]
                s.moves += 2
                root = child
            else:
                return

    for i in range(n // 2 - 1, -1, -1):      # build heap
        sift_down(i, n)
    for end in range(n - 1, 0, -1):          # extract max
        a[0], a[end] = a[end], a[0]
        s.moves += 2
        sift_down(0, end)
    return a, s


ALGORITHMS = {
    "Bubble Sort": bubble_sort,
    "Selection Sort": selection_sort,
    "Insertion Sort": insertion_sort,
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort,
    "Heap Sort": heap_sort,
}

# Extra (auxiliary) space, for the README / analysis.
AUX_SPACE = {
    "Bubble Sort": "O(1)", "Selection Sort": "O(1)", "Insertion Sort": "O(1)",
    "Merge Sort": "O(n)", "Quick Sort": "O(log n) stack", "Heap Sort": "O(1)",
}
