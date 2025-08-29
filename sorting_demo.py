import time
from typing import List, Tuple, Dict


def _now():
    return time.perf_counter()


def _make_metrics():
    return {"comparisons": 0, "swaps": 0, "time_seconds": 0.0}


def bubble_sort(arr: list) -> tuple[list, dict]:
    """Bubble sort (stable). Operates on a shallow copy of the input.

    Design choices:
    - Stable: yes (bubble sort preserves order of equal elements).
    - Operates on a copy of the input list to avoid side-effects.
    - 'comparisons' increments for each element comparison.
    - 'swaps' increments for each element exchange.
    """
    start = _now()
    metrics = _make_metrics()
    a = list(arr)
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            metrics["comparisons"] += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                metrics["swaps"] += 1
                swapped = True
        if not swapped:
            break
    metrics["time_seconds"] = _now() - start
    return a, metrics


def insertion_sort(arr: list) -> tuple[list, dict]:
    """Insertion sort (stable). Operates on a shallow copy of the input.

    Design choices:
    - Stable: yes.
    - Works on a copy to avoid mutating the caller's list.
    - 'swaps' counts element moves (assignments during shifting).
    """
    start = _now()
    metrics = _make_metrics()
    a = list(arr)
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0:
            metrics["comparisons"] += 1
            if a[j] > key:
                a[j + 1] = a[j]
                metrics["swaps"] += 1
                j -= 1
            else:
                break
        a[j + 1] = key
    metrics["time_seconds"] = _now() - start
    return a, metrics


def selection_sort(arr: list) -> tuple[list, dict]:
    """Selection sort (not stable by default). Operates on a shallow copy.

    Design choices:
    - Not stable: selection sort swaps the minimum into position.
    - Works on a copy to avoid mutating input.
    - 'comparisons' for each comparison, 'swaps' for actual exchanges.
    """
    start = _now()
    metrics = _make_metrics()
    a = list(arr)
    n = len(a)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            metrics["comparisons"] += 1
            if a[j] < a[min_idx]:
                min_idx = j
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            metrics["swaps"] += 1
    metrics["time_seconds"] = _now() - start
    return a, metrics


def merge_sort(arr: list) -> tuple[list, dict]:
    """Merge sort (stable). Returns a new sorted list.

    Design choices:
    - Stable: yes, merge preserves order of equal elements.
    - Returns a new list rather than sorting in-place.
    - 'comparisons' counted when elements are compared.
    - 'swaps' counted as assignments into the merged output (i.e., moves).
    """
    start = _now()
    metrics = _make_metrics()

    def _merge(left: List, right: List) -> List:
        merged: List = []
        i = j = 0
        while i < len(left) and j < len(right):
            metrics["comparisons"] += 1
            if left[i] <= right[j]:
                merged.append(left[i])
                metrics["swaps"] += 1
                i += 1
            else:
                merged.append(right[j])
                metrics["swaps"] += 1
                j += 1
        while i < len(left):
            merged.append(left[i])
            metrics["swaps"] += 1
            i += 1
        while j < len(right):
            merged.append(right[j])
            metrics["swaps"] += 1
            j += 1
        return merged

    def _merge_sort(a: List) -> List:
        if len(a) <= 1:
            return list(a)
        mid = len(a) // 2
        left = _merge_sort(a[:mid])
        right = _merge_sort(a[mid:])
        return _merge(left, right)

    sorted_list = _merge_sort(list(arr))
    metrics["time_seconds"] = _now() - start
    return sorted_list, metrics


def quick_sort(arr: list) -> tuple[list, dict]:
    """Quick sort using the Lomuto partition scheme (not stable).

    Design choices:
    - Lomuto partition chosen for simplicity and clarity.
    - Operates on a copy of the input and sorts that copy in-place.
    - Not stable: equal elements may be reordered.
    - 'comparisons' counted for element-to-pivot comparisons.
    - 'swaps' counted for element exchanges.
    """
    start = _now()
    metrics = _make_metrics()
    a = list(arr)

    def _partition(lo: int, hi: int) -> int:
        pivot = a[hi]
        i = lo
        for j in range(lo, hi):
            metrics["comparisons"] += 1
            if a[j] < pivot:
                a[i], a[j] = a[j], a[i]
                metrics["swaps"] += 1
                i += 1
        a[i], a[hi] = a[hi], a[i]
        metrics["swaps"] += 1
        return i

    def _quick(lo: int, hi: int) -> None:
        if lo < hi:
            p = _partition(lo, hi)
            _quick(lo, p - 1)
            _quick(p + 1, hi)

    _quick(0, len(a) - 1)
    metrics["time_seconds"] = _now() - start
    return a, metrics


def heap_sort(arr: list) -> tuple[list, dict]:
    """Heap sort (not stable). Operates on a copy and sorts in-place on that copy.

    Design choices:
    - Uses a max-heap with zero-based indexing.
    - Not stable: heap operations can reorder equal elements.
    - 'comparisons' counted during sift-down, 'swaps' for exchanges.
    """
    start = _now()
    metrics = _make_metrics()
    a = list(arr)
    n = len(a)

    def _sift_down(start_idx: int, end_idx: int) -> None:
        root = start_idx
        while True:
            child = 2 * root + 1
            if child > end_idx:
                break
            swap_idx = root
            metrics["comparisons"] += 1
            if a[swap_idx] < a[child]:
                swap_idx = child
            if child + 1 <= end_idx:
                metrics["comparisons"] += 1
                if a[swap_idx] < a[child + 1]:
                    swap_idx = child + 1
            if swap_idx == root:
                return
            a[root], a[swap_idx] = a[swap_idx], a[root]
            metrics["swaps"] += 1
            root = swap_idx

    # Build max-heap
    for start_idx in range((n - 2) // 2, -1, -1):
        _sift_down(start_idx, n - 1)

    # Extract elements from heap
    for end_idx in range(n - 1, 0, -1):
        a[0], a[end_idx] = a[end_idx], a[0]
        metrics["swaps"] += 1
        _sift_down(0, end_idx - 1)

    metrics["time_seconds"] = _now() - start
    return a, metrics


__all__ = [
    "bubble_sort",
    "insertion_sort",
    "selection_sort",
    "merge_sort",
    "quick_sort",
    "heap_sort",
]