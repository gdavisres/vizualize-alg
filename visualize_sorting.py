"""visualize_sorting.py - interactive sorting visualizer.

Usage:
  python visualize_sorting.py --alg {bubble,insertion,selection,merge,quick} [--n N] [--save]

Steps format:
  A list of tuples (array_snapshot, highlight_indices)
  - array_snapshot: list[int] snapshot of the array at that step
  - highlight_indices: list[int] indices to highlight for that frame (comparisons/swaps)

The instrumented "*_steps" functions return (final_sorted_list, steps).

Note:
  Output animation files are written to the "output/" directory by default when --save
  is used (the directory will be created if necessary).
"""
from __future__ import annotations
import argparse
import random
import os
from typing import List, Tuple, Optional
import matplotlib.pyplot as plt
import matplotlib.animation as animation
try:
    from matplotlib.animation import PillowWriter
    _HAS_PILLOW = True
except Exception:
    PillowWriter = None
    _HAS_PILLOW = False

StepsType = List[Tuple[List[int], List[int]]]  # list of (array_snapshot, highlight_indices)

def _record(steps: StepsType, arr: List[int], highlights: List[int]):
    steps.append((arr.copy(), highlights.copy()))

def bubble_sort_steps(arr: list) -> tuple[list, list]:
    """Instrumented bubble sort.

    Returns (sorted_list, steps) where steps is a list of (array_snapshot, highlight_indices).
    """
    a = arr.copy()
    n = len(a)
    steps: StepsType = []
    _record(steps, a, [])
    for i in range(n):
        for j in range(0, n - i - 1):
            _record(steps, a, [j, j+1])
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
                _record(steps, a, [j, j+1])
    _record(steps, a, [])
    return a, steps

def insertion_sort_steps(arr: list) -> tuple[list, list]:
    """Instrumented insertion sort."""
    a = arr.copy()
    steps: StepsType = []
    _record(steps, a, [])
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        _record(steps, a, [i])
        while j >= 0 and a[j] > key:
            _record(steps, a, [j, j+1])
            a[j+1] = a[j]
            _record(steps, a, [j, j+1])
            j -= 1
        a[j+1] = key
        _record(steps, a, [j+1])
    _record(steps, a, [])
    return a, steps

def selection_sort_steps(arr: list) -> tuple[list, list]:
    """Instrumented selection sort."""
    a = arr.copy()
    steps: StepsType = []
    _record(steps, a, [])
    n = len(a)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            _record(steps, a, [min_idx, j])
            if a[j] < a[min_idx]:
                min_idx = j
                _record(steps, a, [min_idx])
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            _record(steps, a, [i, min_idx])
    _record(steps, a, [])
    return a, steps

def merge_sort_steps(arr: list) -> tuple[list, list]:
    """Instrumented merge sort."""
    a = arr.copy()
    steps: StepsType = []
    _record(steps, a, [])
    def _merge_sort(a, left, right):
        if right - left <= 1:
            return
        mid = (left + right) // 2
        _merge_sort(a, left, mid)
        _merge_sort(a, mid, right)
        merged = []
        i, j = left, mid
        while i < mid and j < right:
            _record(steps, a, [i, j])
            if a[i] <= a[j]:
                merged.append(a[i])
                i += 1
            else:
                merged.append(a[j])
                j += 1
        while i < mid:
            merged.append(a[i])
            i += 1
        while j < right:
            merged.append(a[j])
            j += 1
        for k, val in enumerate(merged, start=left):
            a[k] = val
            _record(steps, a, [k])
    _merge_sort(a, 0, len(a))
    _record(steps, a, [])
    return a, steps

def quick_sort_steps(arr: list) -> tuple[list, list]:
    """Instrumented quick sort (Lomuto partition)."""
    a = arr.copy()
    steps: StepsType = []
    _record(steps, a, [])
    def _quick(l, r):
        if l >= r:
            return
        pivot = a[r]
        i = l
        for j in range(l, r):
            _record(steps, a, [j, r])
            if a[j] < pivot:
                a[i], a[j] = a[j], a[i]
                _record(steps, a, [i, j])
                i += 1
        a[i], a[r] = a[r], a[i]
        _record(steps, a, [i, r])
        _quick(l, i-1)
        _quick(i+1, r)
    _quick(0, len(a)-1)
    _record(steps, a, [])
    return a, steps

def animate_sort(steps: list, title: str = "", save_path: str | None = None):
    """Animate steps using matplotlib.FuncAnimation.

    Steps format: list of tuples (array_snapshot: List[int], highlight_indices: List[int]).
    Each frame will draw the array as a bar chart and color highlight_indices in red.

    Returns the path to the saved animation if saving succeeded, otherwise None.
    """
    if not steps:
        print("No steps to animate.")
        return None
    arr0, _ = steps[0]
    fig, ax = plt.subplots()
    ax.set_title(title)
    bars = ax.bar(range(len(arr0)), arr0, align='center')
    ax.set_xlim(-0.5, len(arr0) - 0.5)
    ax.set_ylim(0, max(max(s[0]) for s in steps) * 1.05 if steps else 1)
    ax.set_xlabel("Index")
    ax.set_ylabel("Value")
    from matplotlib.patches import Patch
    legend_patches = [Patch(color='tab:blue', label='Idle'),
                      Patch(color='tab:red', label='Active')]
    ax.legend(handles=legend_patches, loc='upper right')

    fps = 20
    interval = int(1000 / fps)

    def update(frame):
        arr, highlights = steps[frame]
        for rect, h in zip(bars, arr):
            rect.set_height(h)
            rect.set_color('tab:blue')
        for idx in highlights:
            if 0 <= idx < len(bars):
                bars[idx].set_color('tab:red')
        ax.set_title(f"{title} — Step {frame+1}/{len(steps)}")
        return bars

    anim = animation.FuncAnimation(fig, update, frames=len(steps), interval=interval, blit=False, repeat=False)

    saved = None
    if save_path:
        try:
            # Ensure default output directory exists when using simple filenames or the default naming pattern.
            # If caller provided a path with directories, respect it but make parent dirs.
            basename = os.path.basename(save_path)
            dirname = os.path.dirname(save_path)
            use_output_dir = False
            if dirname == '' or basename.startswith('sorting_animation_'):
                # Treat as simple filename or default naming -> place in output/
                os.makedirs("output", exist_ok=True)
                save_path = os.path.join("output", basename)
                dirname = os.path.dirname(save_path)
                use_output_dir = True
            # Ensure parent directories exist for provided paths (absolute or relative with folders).
            if dirname:
                os.makedirs(dirname, exist_ok=True)

            if save_path.lower().endswith('.gif') and _HAS_PILLOW and PillowWriter is not None:
                writer = PillowWriter(fps=fps)
                anim.save(save_path, writer=writer)
                print(f"Saved animation to: {save_path}")
                saved = save_path
            else:
                Writer = animation.writers.get('ffmpeg')
                if Writer:
                    writer = Writer(fps=fps, metadata=dict(artist='visualize_sorting'), bitrate=1800)
                    anim.save(save_path, writer=writer)
                    print(f"Saved animation to: {save_path}")
                    saved = save_path
                else:
                    # No suitable writer available; instruct user.
                    print("No suitable writer available to save animation. Install 'pillow' for GIF or ensure ffmpeg is available for mp4.")
                    # Even if save failed due to missing writer, ensure output dir was created (above).
        except Exception as e:
            print("Failed to save animation:", e)

    try:
        plt.show()
    except Exception:
        print("Unable to show animation in this environment. If running headless, save to a file with --save.")

    return saved

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Visualize sorting algorithms.")
    parser.add_argument('--alg', choices=['bubble', 'insertion', 'selection', 'merge', 'quick'], default='bubble')
    parser.add_argument('--n', type=int, default=30, help='Number of elements (default 30)')
    parser.add_argument('--save', action='store_true', help='Save animation to output/sorting_animation_{alg}.gif if possible')
    args = parser.parse_args()
    random.seed(42)
    arr = list(range(1, args.n + 1))
    random.shuffle(arr)
    alg_map = {
        'bubble': bubble_sort_steps,
        'insertion': insertion_sort_steps,
        'selection': selection_sort_steps,
        'merge': merge_sort_steps,
        'quick': quick_sort_steps,
    }
    func = alg_map[args.alg]
    final, steps = func(arr)
    save_path = f"output/sorting_animation_{args.alg}.gif" if args.save else None
    saved = animate_sort(steps, title=f"{args.alg.capitalize()} Sort", save_path=save_path)
    if args.save:
        if saved:
            print(f"Saved animation to: {saved}")
        else:
            print("Animation was not saved. See messages above for details.")