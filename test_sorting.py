import random
import sorting_demo

ALGORITHMS = [
    "bubble_sort",
    "insertion_sort",
    "selection_sort",
    "merge_sort",
    "quick_sort",
    "heap_sort",
]

SAMPLES = [
    [],
    [1],
    [1, 2, 3],
    [3, 2, 1],
    [2, 1, 2, 1, 3],
]

# deterministic random samples
random.seed(42)
for _ in range(5):
    SAMPLES.append([random.randint(-10, 10) for _ in range(10)])


def test_sorting_algorithms_correctness():
    """Pytest-discoverable test that iterates algorithms and samples.

    This avoids importing pytest (which some editors/linters may flag as missing)
    while remaining compatible with pytest test discovery.
    """
    for alg_name in ALGORITHMS:
        func = getattr(sorting_demo, alg_name)
        for arr in SAMPLES:
            original = list(arr)
            sorted_arr, metrics = func(original)
            # correctness
            assert sorted_arr == sorted(original)
            # metrics checks
            assert isinstance(metrics, dict)
            for key in ("comparisons", "swaps", "time_seconds"):
                assert key in metrics
            assert isinstance(metrics["comparisons"], int) and metrics["comparisons"] >= 0
            assert isinstance(metrics["swaps"], int) and metrics["swaps"] >= 0
            assert isinstance(metrics["time_seconds"], float) and metrics["time_seconds"] >= 0.0
            # ensure original input was not mutated
            assert original == list(arr)