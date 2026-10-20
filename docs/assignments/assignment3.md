# Assignment 3: Engineering a Hybrid Quicksort

!!! abstract "At a glance"
    - **Unit:** 5 (sorting).
    - **Marks:** 15, assessed with the module-descriptor rubric [below](#marking-rubric).
    - **You build:** a textbook quicksort and a production-style hybrid (introsort-like) quicksort, with tests.
    - **You measure:** the best insertion-sort cutoff, behaviour on hostile inputs, and the gap to Python's built-in `sorted()`.
    - **You reflect:** 400 to 600 words on why "$O(n \log n)$ on average" is not the whole story.

## Context

A bank in Thimphu settles its mobile-payment transactions every night. The settlement job sorts the day's transactions by amount to detect duplicates and build reports. The data is not random: it often arrives already sorted by time (and so nearly sorted by some fields), and many amounts repeat (Nu 100 and Nu 500 top-ups are very common).

A junior developer wrote a textbook quicksort for this job. It worked in testing on random data. On the first real night it either ran for a very long time or crashed with `RecursionError`. Your task is to explain why, and to engineer a sort that stays fast on every kind of input the bank sees.

## Learning Outcomes

By completing this assignment you will be able to:

1. Explain why quicksort's worst case is $\Theta(n^2)$ and which inputs trigger it ([5.3 Quicksort Analysis](../unit5/topic3.md)).
2. Apply pivot rules (median-of-three, random) and the depth-limit fallback used by introsort ([5.4 Randomised Quicksort](../unit5/topic4.md)).
3. Handle duplicate keys with three-way partitioning ([5.3](../unit5/topic3.md)).
4. Tune an algorithmic parameter (the cutoff) by experiment, and explain the result with constant factors ([5.1 Comparison-based Sorting](../unit5/topic1.md)).
5. Define and test **stability**, and relate it to real requirements ([5.1](../unit5/topic1.md)).

## Problem Statement

**Input.** A Python list `a` of $n$ elements, $0 \le n \le 10^6$. Elements can be compared with `<`. They may contain many duplicates.

**Output.** Sort `a` **in place** into non-decreasing order and return `None`.

**Rules.**

- Compare elements **only** with `<`. (This lets your sort work on any object that defines `__lt__`.)
- Do not call `sorted()`, `list.sort()` or `heapq` inside your sorting functions. They are allowed in tests and experiments as the reference.

**Example.**

```text
a = [5, 3, 8, 1, 9, 2, 7]
hybrid_sort(a, cutoff=2)
a == [1, 2, 3, 5, 7, 8, 9]
```

## Requirements

### Functional requirements

| ID | Function | Requirement |
|---|---|---|
| F1 | `quicksort_basic(a)` | Textbook baseline: last element as pivot, Lomuto partition, recurse on both sides, no cutoff. Do **not** raise the recursion limit. |
| F2 | `insertion_sort(a, lo, hi)` | Sort `a[lo..hi]` (inclusive) in place. |
| F3 | `median_of_three(a, lo, hi)` | Return the median of `a[lo]`, `a[mid]`, `a[hi]` as the pivot value. |
| F4 | `partition3(a, lo, hi, pivot)` | Three-way partition. Return `(lt, gt)` so that `a[lo..lt-1] < pivot`, `a[lt..gt]` equal to pivot, `a[gt+1..hi] > pivot`. |
| F5 | `hybrid_sort(a, cutoff=16, pivot="median3")` | Quicksort that (a) uses insertion sort for ranges of size $\le$ `cutoff`; (b) chooses the pivot by `"median3"` or `"random"`; (c) partitions three ways; (d) recurses on the **smaller** part and loops on the larger; (e) switches to the given `heapsort_range` when the depth exceeds $2\lfloor\log_2 n\rfloor$. |
| F6 | `STATS["heapsort_fallbacks"]` | Count how many times F5 falls back to heapsort. |

### Testing requirements

| ID | Requirement |
|---|---|
| T1 | Cross-check F1 (for $n \le 500$) and F5 against `sorted()` on at least 1,000 random lists, for several cutoffs and both pivot rules. |
| T2 | Edge cases: empty list; one element; two elements in both orders; all equal; already sorted; reverse sorted; only two distinct values; negative numbers; floats. |
| T3 | A `hypothesis` property test: the output is sorted **and** is a permutation of the input. |
| T4 | A **stability** test using the `Txn` class in the starter code. Record whether your sort is stable, and whether `sorted()` is. |

### Experimental requirements

Use the generators in `inputs.py`. Fix the seed. Report medians of at least 5 runs.

| ID | Requirement |
|---|---|
| E1 | **Cutoff tuning.** For $n = 100{,}000$ random integers, time F5 with cutoff $\in \{1, 2, 4, 8, 16, 32, 64, 128\}$. Plot time against cutoff. Repeat for one other input kind. Choose a cutoff and justify it. |
| E2 | **Robustness.** For every input kind in `inputs.py`, time F5 (your chosen cutoff, both pivot rules) for $n = 2^{12}, 2^{13}, \dots, 2^{17}$, and report log-log slopes. Time F1 too, for as long as it runs; record crashes and time-outs as results. |
| E3 | **Built-in comparison.** Time `sorted()` on the same inputs. Report the ratio (your time / built-in time) for each input kind. |
| E4 | **Fallbacks.** Report `STATS["heapsort_fallbacks"]` for each input kind and pivot rule at $n = 2^{17}$. |

## Starter Code

Time your code with `time.perf_counter()` following the [Lab Overview rules](../lab/overview.md#rules). Write your code where you see `# TODO`.

```python
# hybrid.py
"""CSF302 Assignment 3: hybrid quicksort. Compare elements with < only."""
import math
import random

STATS = {"heapsort_fallbacks": 0}


def quicksort_basic(a, lo=0, hi=None):
    """F1. Textbook quicksort: last-element pivot, Lomuto partition, no cutoff."""
    if hi is None:
        hi = len(a) - 1
    # TODO
    raise NotImplementedError


def insertion_sort(a, lo, hi):
    """F2. Sort a[lo..hi] inclusive, in place."""
    # TODO
    raise NotImplementedError


def median_of_three(a, lo, hi):
    """F3. Return the median value of a[lo], a[mid], a[hi]."""
    # TODO
    raise NotImplementedError


def partition3(a, lo, hi, pivot):
    """F4. Three-way partition of a[lo..hi] around the value pivot. Return (lt, gt)."""
    # TODO: keep three regions: < pivot, == pivot, > pivot (test 'pivot < x' for '>')
    raise NotImplementedError


def heapsort_range(a, lo, hi):
    """GIVEN. Heapsort a[lo..hi] inclusive, in place, using only <."""
    n = hi - lo + 1

    def sift_down(root, end):
        while 2 * root + 1 <= end:
            child = 2 * root + 1
            if child + 1 <= end and a[lo + child] < a[lo + child + 1]:
                child += 1
            if a[lo + root] < a[lo + child]:
                a[lo + root], a[lo + child] = a[lo + child], a[lo + root]
                root = child
            else:
                return

    for start in range(n // 2 - 1, -1, -1):
        sift_down(start, n - 1)
    for end in range(n - 1, 0, -1):
        a[lo], a[lo + end] = a[lo + end], a[lo]
        sift_down(0, end - 1)


def hybrid_sort(a, cutoff=16, pivot="median3", rng=None):
    """F5. Sort a in place. pivot is "median3" or "random"."""
    if len(a) < 2:
        return
    rng = rng or random.Random(0)
    depth_limit = 2 * int(math.log2(len(a)))
    _hybrid(a, 0, len(a) - 1, cutoff, pivot, depth_limit, rng)


def _hybrid(a, lo, hi, cutoff, pivot, depth, rng):
    while hi - lo + 1 > cutoff:
        if depth == 0:
            STATS["heapsort_fallbacks"] += 1
            heapsort_range(a, lo, hi)
            return
        depth -= 1
        # TODO: choose the pivot value (median_of_three or a random element)
        # TODO: lt, gt = partition3(...)
        # TODO: recurse on the SMALLER of a[lo..lt-1] and a[gt+1..hi];
        #       then update lo or hi so the loop handles the larger one
        raise NotImplementedError
    insertion_sort(a, lo, hi)
```

```python
# inputs.py
"""GIVEN. Input generators for the experiments, and a record type for the stability test."""
from dataclasses import dataclass


def make_input(kind, n, rng):
    if kind == "random":
        return [rng.randint(0, 10 ** 9) for _ in range(n)]
    if kind == "sorted":
        return sorted(rng.randint(0, 10 ** 9) for _ in range(n))
    if kind == "reversed":
        return sorted((rng.randint(0, 10 ** 9) for _ in range(n)), reverse=True)
    if kind == "nearly sorted":                         # sorted, then 1% random swaps
        a = sorted(rng.randint(0, 10 ** 9) for _ in range(n))
        for _ in range(max(1, n // 100)):
            i, j = rng.randrange(n), rng.randrange(n)
            a[i], a[j] = a[j], a[i]
        return a
    if kind == "few distinct":                          # like repeated top-up amounts
        return [rng.choice([50, 100, 200, 500, 1000]) for _ in range(n)]
    if kind == "all equal":
        return [500] * n
    if kind == "organ pipe":                            # up, then down
        return list(range(n // 2)) + list(range(n - n // 2, 0, -1))
    raise ValueError(kind)


KINDS = ["random", "sorted", "reversed", "nearly sorted", "few distinct", "all equal", "organ pipe"]


@dataclass
class Txn:
    amount: int        # the sort key
    txn_id: int        # original arrival order

    def __lt__(self, other):
        return self.amount < other.amount
```

```python
# test_hybrid.py
import random

from hybrid import hybrid_sort, quicksort_basic
from inputs import KINDS, Txn, make_input


def test_example():
    a = [5, 3, 8, 1, 9, 2, 7]
    hybrid_sort(a, cutoff=2)
    assert a == [1, 2, 3, 5, 7, 8, 9]


def test_random_against_builtin():
    rng = random.Random(1)
    for _ in range(1000):
        a = [rng.randint(0, rng.choice([1, 5, 1000])) for _ in range(rng.randint(0, 120))]
        for cutoff in (1, 4, 16):
            for pivot in ("median3", "random"):
                b = a.copy()
                hybrid_sort(b, cutoff, pivot)
                assert b == sorted(a)
        b = a.copy()
        quicksort_basic(b)
        assert b == sorted(a)


def test_every_input_kind():
    rng = random.Random(2)
    for kind in KINDS:
        a = make_input(kind, 3000, rng)
        b = a.copy()
        hybrid_sort(b)
        assert b == sorted(a)


def test_stability_report():
    txns = [Txn(amount, i) for i, amount in enumerate([500, 100, 500, 100, 50, 500])]
    mine = txns.copy()
    hybrid_sort(mine, cutoff=1)
    assert [t.amount for t in mine] == [50, 100, 100, 500, 500, 500]
    print("stable?", [t.txn_id for t in mine] == [t.txn_id for t in sorted(txns)])

# TODO: add the edge cases (T2) and a hypothesis property test (T3)
```

## Deliverables

- [ ] `hybrid.py` with F1 to F6 implemented; `inputs.py` unchanged.
- [ ] `test_hybrid.py` covering T1 to T4, all passing (include the `pytest` summary line).
- [ ] `experiments.py` that reproduces every table and plot from a fixed seed.
- [ ] Report (PDF or Markdown, at most 6 pages excluding code) containing:
    - [ ] the recurrences for quicksort's worst case and for a perfectly balanced split, solved, and how the depth limit bounds hybrid sort's worst case;
    - [ ] the tables and plots for E1 to E4, with your machine details;
    - [ ] your chosen cutoff, with evidence;
    - [ ] a stability statement: is your sort stable, and does it matter for the bank?
    - [ ] the critical reflection (400 to 600 words);
    - [ ] an AI-use and help statement.

## Critical Reflection

Write 400 to 600 words. Answer **at least four** of the prompts below, using your own measurements as evidence.

1. **The baseline's failure.** What exactly happened when `quicksort_basic` met sorted input: slow, crash, or both? Connect it to the recurrence $T(n) = T(n-1) + \Theta(n)$ and to Python's recursion limit. Which assumption of the "average case" analysis did real data break?
2. **Your best cutoff.** Insertion sort is $\Theta(n^2)$, yet a cutoff helps. Why? Did the best cutoff depend on the input kind? Would it be the same in C?
3. **Pivot rules under attack.** Median-of-three is often said to "fix" sorted input. Did it, in your implementation? Use your fallback counts (E4). How does the random pivot change who can make your sort slow?
4. **The built-in gap.** By what factor was `sorted()` faster, and was the factor the same for every input kind? Which part is the language (C vs Python) and which part is the algorithm (Timsort detects existing runs)?
5. **Stability.** Give a concrete bank-report scenario where an unstable sort produces a wrong or confusing result. How would you fix it without changing your algorithm?
6. **AI assistance and hindsight.** If you used an AI tool, what did it get wrong or leave out (for example the depth limit, or recursion on the smaller side)? What would you do differently next time?

## Marking Rubric

Each assignment is marked out of 15 using the module-descriptor criteria. The instructor may move marks between sub-components; the table below is the default split.

| Criterion | Sub-component | Marks |
|---|---|---|
| Analysis and problem-solving | recurrences and worst-case bound derived; cutoff choice justified | 1 |
| | experimental analysis (E1 to E4) interpreted against theory | 1 |
| | **critical reflection** | 3 |
| Application of concepts | F1 to F6 correct; pivot rules, three-way partition, depth limit working | 3 |
| | tests T1 to T4, including brute-force/built-in cross-check, edge cases and stability | 2 |
| Presentation and explanation | report clarity, code readability, labelled tables and figures | 3 |
| Timely submission and correctness | on time; code runs as submitted and passes the given tests | 2 |
| **Total** | | **15** |

| Criterion (marks) | Excellent | Good | Satisfactory | Poor |
|---|---|---|---|---|
| **Analysis: technical (2)** | (2) Worst and balanced recurrences solved; depth-limit bound explained; every experiment interpreted, including anomalies | (1.5) Mostly complete; minor gaps | (1) Results reported with little interpretation | (0 to 0.5) Missing or incorrect |
| **Analysis: critical reflection (3)** | (3) Four or more prompts answered with specific evidence from own data; identifies which assumption broke and why; honest about limitations | (2) Three or four prompts with some evidence | (1) Generic, little use of own data | (0) Missing, off-topic or far outside the word limit |
| **Application of concepts (5)** | (5) All functions correct; fast on every input kind; full tests including stability | (4) Correct; one test category thin | (2 to 3) Sorts correctly but slow or crashing on some input kind, or depth limit missing | (0 to 1) Incorrect or no cross-check |
| **Presentation and explanation (3)** | (3) Clear structure; readable code; all plots labelled | (2) Mostly clear | (1) Hard to follow or plots unlabelled | (0) Unreadable or missing |
| **Timely submission and correctness (2)** | (2) On time, and code runs from a clean folder and passes the given tests | | (1) One of the two | (0) Neither |

## Academic Integrity and AI Use

- This is individual work. You may discuss ideas, but the code and the report must be your own. You may be asked to explain or modify your code in a short viva.
- AI tools are allowed under the rules in the [Lab Overview](../lab/overview.md#rules). Include a **disclosure statement**: which tool, for what, and what you changed or rejected. Undisclosed use is treated as academic misconduct.
- Any AI-generated code must pass your cross-check against `sorted()`. Claims about speed must be backed by your own measurements.
- Cite any website, book or classmate that helped you.
