#!/usr/bin/env python3
"""Benchmarking and plotting utilities for sorting algorithms provided in sorting_demo.py.

This script provides:
- run_benchmarks(...)
- plot_results(...)
- __main__ entrypoint to run a small benchmark and generate a plot.
"""
from __future__ import annotations
import time
import math
import random
from typing import Callable, Dict, List, Any, Optional
import csv
import os

try:
    import matplotlib.pyplot as plt
except Exception:
    plt = None  # type: ignore

import sorting_demo


def run_benchmarks(algorithms: Dict[str, Callable[[List[int]], Any]],
                   sizes: List[int],
                   trials: int,
                   seed: int = 42) -> Dict[str, List[Dict[str, Optional[float]]]]:
    """Run benchmarks for provided sorting algorithms.

    Parameters
    ----------
    algorithms:
        Mapping name -> callable that accepts a list and returns (sorted_list, metrics_dict).
    sizes:
        List of input sizes to benchmark.
    trials:
        Number of trials per size (averaged).
    seed:
        Base RNG seed for reproducible inputs.

    Returns
    -------
    Dict mapping algorithm name -> list of result dicts (one per size).
    Each result dict contains keys: 'n', 'time_seconds', 'comparisons', 'swaps'.
    Values that are not provided by an algorithm are set to None.
    """
    rng = random.Random(seed)
    results: Dict[str, List[Dict[str, Optional[float]]]] = {}

    # Pre-generate inputs so the same inputs are used across algorithms for each trial.
    inputs_by_size: Dict[int, List[List[int]]] = {}
    for n in sizes:
        trials_inputs: List[List[int]] = []
        for t in range(trials):
            # Use the same RNG stream; inputs are reproducible given seed.
            trials_inputs.append([rng.randint(-10000, 10000) for _ in range(n)])
        inputs_by_size[n] = trials_inputs

    for name, func in algorithms.items():
        alg_results: List[Dict[str, Optional[float]]] = []
        for n in sizes:
            times: List[float] = []
            comps: List[int] = []
            swaps: List[int] = []
            has_comps = False
            has_swaps = False
            for trial_input in inputs_by_size[n]:
                arr = list(trial_input)  # fresh copy per run
                # Attempt to use algorithm-provided timing if available.
                start = time.perf_counter()
                try:
                    out = func(arr)
                except Exception:
                    # If algorithm raises, skip this trial.
                    continue
                elapsed = time.perf_counter() - start
                # Unpack expected return form (sorted_list, metrics_dict)
                if isinstance(out, tuple) and len(out) == 2:
                    _, metrics = out
                    if isinstance(metrics, dict):
                        tval = metrics.get("time_seconds", None)
                        if isinstance(tval, (int, float)):
                            times.append(float(tval))
                        else:
                            times.append(elapsed)
                        comp = metrics.get("comparisons", None)
                        if isinstance(comp, int):
                            comps.append(comp)
                            has_comps = True
                        swapv = metrics.get("swaps", None)
                        if isinstance(swapv, int):
                            swaps.append(swapv)
                            has_swaps = True
                    else:
                        times.append(elapsed)
                else:
                    # unexpected return form
                    times.append(elapsed)

            # Compute averages; use None when no data available.
            avg_time = float(sum(times) / len(times)) if times else None
            avg_comps = float(sum(comps) / len(comps)) if comps else None
            avg_swaps = float(sum(swaps) / len(swaps)) if swaps else None

            alg_results.append({
                "n": n,
                "time_seconds": avg_time,
                "comparisons": avg_comps,
                "swaps": avg_swaps,
            })
        results[name] = alg_results
    return results


def save_results_table(results: Dict[str, List[Dict[str, Optional[float]]]],
                       sizes: List[int],
                       out_csv: str = "output/benchmark_table.csv",
                       out_image: str = "output/sorting_performance_table.png") -> None:
    """Save benchmark results to a CSV and optionally create a PNG table image.

    CSV format:
      algorithm, n, time_seconds, comparisons, swaps

    One row per algorithm per input size. Missing values are written as empty
    cells in the CSV. The PNG image (if matplotlib available) contains a
    compact table with algorithms as rows and input sizes as columns showing
    formatted time_seconds (3 decimal places). Missing times are shown as '-'.
    """
    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)

    # Write CSV
    fieldnames = ["algorithm", "n", "time_seconds", "comparisons", "swaps"]
    try:
        with open(out_csv, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames)
            writer.writeheader()
            for alg, rows in results.items():
                for r in rows:
                    # Use empty strings for None values per requirement
                    writer.writerow({
                        "algorithm": alg,
                        "n": r.get("n", ""),
                        "time_seconds": "" if r.get("time_seconds") is None else f"{r.get('time_seconds')}",
                        "comparisons": "" if r.get("comparisons") is None else f"{r.get('comparisons')}",
                        "swaps": "" if r.get("swaps") is None else f"{r.get('swaps')}",
                    })
    except Exception as exc:
        print(f"Failed to write CSV {out_csv}: {exc}")

    # Attempt to create a PNG table image using matplotlib if available.
    if plt is None:
        print("matplotlib is not available; skipping table image generation.")
        return

    try:
        row_labels = list(results.keys())
        col_labels = [str(n) for n in sizes]
        cell_text: List[List[str]] = []
        for alg in row_labels:
            # build mapping n -> time_seconds for this algorithm
            n_to_time = {int(r.get("n")): r.get("time_seconds") for r in results.get(alg, [])}
            row: List[str] = []
            for n in sizes:
                t = n_to_time.get(n)
                if t is None:
                    row.append("-")
                else:
                    try:
                        row.append(f"{float(t):.3f}")
                    except Exception:
                        row.append(str(t))
            cell_text.append(row)

        # Create figure sized according to table dimensions
        fig_w = max(6, len(col_labels) * 1.2)
        fig_h = max(1.5, len(row_labels) * 0.5 + 0.8)
        fig, ax = plt.subplots(figsize=(fig_w, fig_h))
        ax.axis("off")
        table = ax.table(cellText=cell_text,
                         rowLabels=row_labels,
                         colLabels=col_labels,
                         cellLoc="center",
                         loc="center")
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.5)
        fig.tight_layout()
        fig.savefig(out_image, dpi=150)
    except Exception as exc:
        print(f"Failed to create table image {out_image}: {exc}")


def plot_results(results: Dict[str, List[Dict[str, Optional[float]]]],
                 sizes: List[int],
                 out_path: str = "output/sorting_performance.png") -> None:
    """Plot timing results and theoretical complexity reference lines.

    The plot shows averaged time vs input size for each algorithm and three
    reference complexity curves: O(n), O(n log n), and O(n^2).
    After saving the plot it calls save_results_table(...) to persist a CSV
    summary and optionally a table-image PNG.
    """
    if plt is None:
        print(
            "matplotlib is not available. Install matplotlib to generate plots."
        )
        # Even if matplotlib not available for plotting, attempt to write CSV.
        try:
            save_results_table(
                results,
                sizes,
                out_csv="output/benchmark_table.csv",
                out_image="output/sorting_performance_table.png",
            )
        except Exception:
            pass
        return

    n_vals = list(sizes)
    n_max = max(n_vals) if n_vals else 1

    fig, ax = plt.subplots(figsize=(8, 6))

    # Prepare colors and markers
    markers = ["o", "s", "D", "^", "v", "P", "X", "*"]

    # Collect times for scaling heuristics
    times_at_max = []
    alg_names = list(results.keys())
    for name in alg_names:
        # get time list aligned with sizes
        times = []
        for r in results[name]:
            times.append(r.get("time_seconds"))
        # pick the last element as time at n_max
        last_time = times[-1] if times else None
        if last_time is not None:
            times_at_max.append(float(last_time))

    # Choose reference time: fastest algorithm at largest n, if available.
    ref_time = min(times_at_max) if times_at_max else 1.0
    if ref_time <= 0:
        ref_time = 1.0

    # Plot each algorithm's averaged times
    for idx, name in enumerate(alg_names):
        times = [r.get("time_seconds") for r in results[name]]
        # Replace None with NaN for plotting
        plot_times = [float(t) if t is not None else float("nan") for t in times]
        ax.plot(n_vals, plot_times, marker=markers[idx % len(markers)],
                label=name, linewidth=1.5)

    # Theoretical curves (unscaled)
    n_array = [float(n) for n in n_vals]
    nlogn = [n * math.log2(n) if n > 0 else 0.0 for n in n_array]
    linear = [n for n in n_array]
    quad = [n * n for n in n_array]

    # Scale so that at n_max the n log n curve matches ref_time.
    nlogn_max = nlogn[-1] if nlogn else 1.0
    scale = ref_time / nlogn_max if nlogn_max > 0 else 1.0
    linear_scaled = [scale * v for v in linear]
    nlogn_scaled = [scale * v for v in nlogn]
    quad_scaled = [scale * v for v in quad]

    ax.plot(n_vals, linear_scaled, linestyle="--", color="gray", label="O(n)")
    ax.plot(n_vals, nlogn_scaled, linestyle="--", color="black", label="O(n log n)")
    ax.plot(n_vals, quad_scaled, linestyle="--", color="lightgray", label="O(n^2)")

    ax.set_xlabel("Input size n")
    ax.set_ylabel("Average time (seconds)")
    ax.set_title("Sorting algorithms: time vs input size")
    ax.grid(True, which="both", linestyle=":", linewidth=0.5)
    ax.legend()
    # Use linear scale but make sure small values are visible.
    ax.set_xscale("linear")
    ax.set_yscale("linear")

    fig.tight_layout()
    try:
        # Ensure output directory exists before saving the main plot
        os.makedirs("output", exist_ok=True)
        fig.savefig(out_path, dpi=150)
        print(f"Saved plot to: {out_path}")
    except Exception as exc:
        print(f"Failed to save figure to {out_path}: {exc}")

    # After saving the main plot, also save summary CSV and table image.
    try:
        save_results_table(
            results,
            sizes,
            out_csv="output/benchmark_table.csv",
            out_image="output/sorting_performance_table.png",
        )
    except Exception as exc:
        print(f"Failed to save results table: {exc}")

    # Show interactively if possible
    try:
        plt.show()
    except Exception:
        pass


if __name__ == "__main__":
    # Build algorithms mapping from sorting_demo
    alg_names = [
        "bubble_sort",
        "insertion_sort",
        "selection_sort",
        "merge_sort",
        "quick_sort",
        "heap_sort",
    ]
    algorithms: Dict[str, Callable[[List[int]], Any]] = {}
    for name in alg_names:
        func = getattr(sorting_demo, name, None)
        if callable(func):
            algorithms[name] = func

    # Reasonable sizes for a mixed set of algorithms; adjust if runs are too slow.
    sizes = [100, 200, 500, 1000, 2000]
    trials = 3
    print("Running benchmarks (this may take a moment)...")
    results = run_benchmarks(algorithms, sizes, trials, seed=42)
    plot_results(results, sizes, out_path="output/sorting_performance.png")
    
    # Inform where the summary table and image were saved.
    csv_path = "output/benchmark_table.csv"
    img_path = "output/sorting_performance_table.png"
    print(f"Saved table to: {csv_path}")
    if plt is not None:
        print(f"Saved table image to: {img_path}")
    print("Done.")