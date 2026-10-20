# Assignment 2: Closest Camera Traps (Divide and Conquer)

!!! abstract "At a glance"
    - **Units:** 2 to 4 (asymptotic analysis, recurrences, divide and conquer).
    - **Marks:** 15, assessed with the module-descriptor rubric [below](#marking-rubric).
    - **You build:** a brute-force and two divide-and-conquer solutions to the closest-pair problem, with tests.
    - **You measure:** whether the running time really grows like $n \log n$, and where divide and conquer starts to beat brute force.
    - **You reflect:** 400 to 600 words on where theory and measurement agreed, where they did not, and why.

## Context

The Department of Forests and Park Services places camera traps across Jigme Dorji National Park to monitor snow leopards and takins. Each trap has a position in metres on a map grid. Two traps placed very close together record the same animals, which wastes batteries and memory cards. Before each season, the field team wants the pair of traps that are closest together, so it can move one of them.

There may be tens of thousands of trap positions once several seasons of data are merged. Comparing every pair is simple, but the number of pairs grows like $n^2$. Your job is to build a faster method, prove to yourself that it is correct, and show with measurements when it is worth using.

## Learning Outcomes

By completing this assignment you will be able to:

1. Design a divide-and-conquer algorithm with a non-trivial combine step ([4.1 Divide and Conquer](../unit4/topic1.md)).
2. Write and solve the recurrence for your algorithm ([3.1 Recurrence Relations](../unit3/topic1.md), [3.5 Master Method](../unit3/topic5.md)).
3. Explain why two algorithms with recurrences $2T(n/2) + \Theta(n)$ and $2T(n/2) + \Theta(n \log n)$ differ ([3.3 Recursion Tree](../unit3/topic3.md)).
4. Test an efficient algorithm against a brute-force reference, including edge cases.
5. Run a doubling experiment and read the growth rate from a log-log plot ([2.1 Asymptotic Analysis](../unit2/topic1.md), [Lab Overview rules](../lab/overview.md#rules)).

## Problem Statement

**Input.** A list `points` of $n \ge 2$ points. Each point is a tuple `(x, y)` of integers or floats with $0 \le x, y \le 10^6$. Two points may have the same coordinates.

**Output.** A tuple `(d, i, j)` where `i < j` are indices into `points` and `d` is the Euclidean distance between `points[i]` and `points[j]`, and no other pair is closer. If several pairs tie, any one of them is accepted.

**Errors.** Raise `ValueError` if $n < 2$.

**Constraints.** $2 \le n \le 2 \times 10^5$. Your divide-and-conquer version should handle $n = 10^5$ in a few seconds of pure Python.

**Example.**

```text
points = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
output = (1.4142135623730951, 0, 5)      # (2, 3) and (3, 4) are sqrt(2) apart
```

## Requirements

### Functional requirements

| ID | Function | Requirement |
|---|---|---|
| F1 | `closest_pair_brute(points)` | Check every pair. $\Theta(n^2)$. This is your reference. |
| F2 | `closest_pair(points)` | Divide and conquer in $O(n \log n)$: sort by $x$ and by $y$ **once**, split at the median $x$, recurse on both halves, then check the strip of width $2\delta$ around the dividing line in $y$ order. |
| F3 | `closest_pair_resort(points)` | The same algorithm, but presort by $x$ only. Inside **every** call, sort that call's points by $y$ with `sorted()` instead of receiving the $y$-order from the parent. This is the $O(n \log^2 n)$ version. |
| F4 | all | Return indices into the **original** list, with `i < j`. Do not modify `points`. |

You may use `sorted()` and `math.hypot` in all three functions. The algorithm under study is the recursion and the strip check, not sorting.

### Testing requirements

| ID | Requirement |
|---|---|
| T1 | Cross-check F2 and F3 against F1 on at least 1,000 random inputs of size 2 to 50. Compare distances, not indices (ties may give different pairs). |
| T2 | Check that the returned indices really are at the returned distance, and that `i < j`. |
| T3 | Edge cases, at least: exactly 2 points; 3 points; duplicate points (answer 0); all points on one vertical line (same $x$); all points on one horizontal line; the closest pair straddling the dividing line; $n < 2$ raises `ValueError`. |
| T4 | One property-based test with `hypothesis`. |

### Experimental requirements

| ID | Requirement |
|---|---|
| E1 | **Doubling experiment.** Time F2 and F3 for $n = 2^{10}, 2^{11}, \dots, 2^{17}$ on uniform random points. Report the median of at least 3 runs, the local exponents and the fitted log-log slope. |
| E2 | **Normalised time.** For both F2 and F3, tabulate $t / (n \log_2 n)$ and $t / (n \log_2^2 n)$. For each algorithm, which ratio settles to a constant, and which keeps rising or falling? |
| E3 | **Crossover.** Time F1 and F2 for $n = 4, 8, 16, \dots, 1024$. Find the smallest $n$ at which F2 is faster on your machine. |
| E4 | **Strip work.** Count the distance computations made in the strip for each $n$ in E1. Divide by $n$ and compare with the constant bound from the packing lemma in [4.1](../unit4/topic1.md). |

## Starter Code

Time your code with `time.perf_counter()` following the [Lab Overview rules](../lab/overview.md#rules). Write your code where you see `# TODO`.

```python
# closest.py
"""CSF302 Assignment 2: closest pair of points."""
import math


def dist(p, q):
    return math.hypot(p[0] - q[0], p[1] - q[1])


def _ordered(d, i, j):
    """Return (d, i, j) with i < j."""
    return (d, i, j) if i < j else (d, j, i)


def closest_pair_brute(points):
    """F1. Return (d, i, j) by checking every pair."""
    if len(points) < 2:
        raise ValueError("need at least two points")
    # TODO
    raise NotImplementedError


def closest_pair(points):
    """F2. O(n log n) divide and conquer."""
    if len(points) < 2:
        raise ValueError("need at least two points")
    idx = range(len(points))
    by_x = sorted(idx, key=lambda i: points[i])                    # indices in x order
    by_y = sorted(idx, key=lambda i: (points[i][1], points[i][0]))  # indices in y order
    d, i, j = _solve(points, by_x, by_y)
    return _ordered(d, i, j)


def _solve(points, by_x, by_y):
    """Closest pair among the indices in by_x; by_y holds the SAME indices in y order."""
    n = len(by_x)
    # TODO: base case (n <= 3): brute force on these indices
    # TODO: split by_x into left and right halves at mid = n // 2
    # TODO: split by_y into left_y and right_y in O(n), keeping y order
    #       (hint: put the left indices in a set first)
    # TODO: recurse on both halves; delta = the smaller answer
    # TODO: strip = indices in by_y whose x is within delta of the dividing x
    # TODO: compare each strip point with the next few strip points while
    #       their y difference is less than the best distance so far
    raise NotImplementedError


def closest_pair_resort(points):
    """F3. Same idea, but every call sorts its own points by y: O(n log^2 n)."""
    if len(points) < 2:
        raise ValueError("need at least two points")
    # TODO
    raise NotImplementedError
```

```python
# test_closest.py
import random

import pytest

from closest import closest_pair, closest_pair_brute, closest_pair_resort, dist

FAST = [closest_pair, closest_pair_resort]


def test_example():
    pts = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
    for f in [closest_pair_brute] + FAST:
        d, i, j = f(pts)
        assert (i, j) == (0, 5) and d == pytest.approx(2 ** 0.5)


def test_random_against_brute():
    rng = random.Random(1)
    for _ in range(1000):
        n = rng.randint(2, 50)
        pts = [(rng.randint(0, 100), rng.randint(0, 100)) for _ in range(n)]
        expected = closest_pair_brute(pts)[0]
        for f in FAST:
            d, i, j = f(pts)
            assert i < j and d == pytest.approx(expected)
            assert dist(pts[i], pts[j]) == pytest.approx(d)


def test_too_few_points():
    with pytest.raises(ValueError):
        closest_pair([(0, 0)])

# TODO: add the edge cases listed in T3 and a hypothesis test (T4)
```

## Deliverables

- [ ] `closest.py` with F1, F2 and F3 implemented.
- [ ] `test_closest.py` covering T1 to T4, all passing (include the `pytest` summary line in your report).
- [ ] `experiments.py` that reproduces every table and plot in your report from a fixed seed.
- [ ] Report (PDF or Markdown, at most 6 pages excluding code) containing:
    - [ ] the recurrence for F2 and for F3, each solved with a named method (recursion tree, substitution or Master Theorem), with all steps shown;
    - [ ] a short correctness argument for the strip step, in your own words;
    - [ ] the tables and log-log plots for E1 to E4, with your machine details;
    - [ ] the critical reflection (400 to 600 words);
    - [ ] an AI-use and help statement.

## Critical Reflection

Write 400 to 600 words. Answer **at least four** of the prompts below. Use your own numbers as evidence. A reflection that only repeats the theory scores low.

1. **Theory vs measurement.** Your fitted slope for F2 is probably a little above 1, and F3's is probably only slightly higher. Can your data actually tell $n \log n$ from $n \log^2 n$? What would you need to change (range of $n$, number of runs, normalisation) to be confident?
2. **The model's assumptions.** The analysis counts distance computations and treats every operation as costing the same. Which part of your Python program does that model ignore (sorting with `key=`, building lists and sets, recursion overhead, memory)? Which of these dominates your measured time?
3. **The crossover.** Why is brute force faster for small $n$, even though it is $\Theta(n^2)$? Would a base case larger than 3 help? Give the evidence.
4. **Worst-case inputs.** Did any input make your implementation slower than random points (for example many points with the same $x$, or many duplicates)? Was that a property of the algorithm or of your implementation?
5. **AI assistance.** If you used an AI tool, give one specific suggestion it made and how you checked it. Did it make any claim (about correctness or complexity) that turned out to be wrong or unsupported?
6. **Hindsight.** If you started again, what would you design or test differently, and why?

## Marking Rubric

Each assignment is marked out of 15 using the module-descriptor criteria. The instructor may move marks between sub-components; the table below is the default split.

| Criterion | Sub-component | Marks |
|---|---|---|
| Analysis and problem-solving | recurrences derived and solved; correctness of the strip step argued | 1 |
| | experimental analysis (E1 to E4) interpreted against theory | 1 |
| | **critical reflection** | 3 |
| Application of concepts | F1 to F4 correct and efficient | 3 |
| | tests T1 to T4, including brute-force cross-check and edge cases | 2 |
| Presentation and explanation | report clarity, code readability, labelled tables and figures | 3 |
| Timely submission and correctness | on time; code runs as submitted and passes the given tests | 2 |
| **Total** | | **15** |

| Criterion (marks) | Excellent | Good | Satisfactory | Poor |
|---|---|---|---|---|
| **Analysis: technical (2)** | (2) Both recurrences set up from the code and solved correctly with steps; strip argument correct; every experiment interpreted against theory | (1.5) Recurrences correct; minor gaps in argument or interpretation | (1) Recurrences stated but not derived, or experiments described without interpretation | (0 to 0.5) Missing or incorrect |
| **Analysis: critical reflection (3)** | (3) Four or more prompts answered with specific evidence from own data; identifies which model assumption broke and why; honest about limitations | (2) Three or four prompts with some evidence; mostly specific | (1) Generic statements, little use of own data | (0) Missing, off-topic or outside the word limit by a wide margin |
| **Application of concepts (5)** | (5) All functions correct, $O(n \log n)$ achieved, all tests present and passing | (4) Correct; one test category thin | (2 to 3) Works on random data but fails an edge case, or F3 missing | (0 to 1) Incorrect or no cross-check |
| **Presentation and explanation (3)** | (3) Clear structure; readable code; all plots labelled with units and slopes | (2) Mostly clear; small presentation gaps | (1) Hard to follow or plots unlabelled | (0) Unreadable or missing |
| **Timely submission and correctness (2)** | (2) On time, and code runs from a clean folder and passes the given tests | | (1) One of the two | (0) Neither |

## Academic Integrity and AI Use

- This is individual work. You may discuss ideas, but the code and the report must be your own. You may be asked to explain or modify your code in a short viva.
- AI tools are allowed under the rules in the [Lab Overview](../lab/overview.md#rules). You must include a **disclosure statement**: which tool, for what, and what you changed or rejected. Undisclosed use is treated as academic misconduct.
- Any AI-generated code must pass your brute-force cross-check. "The AI said it is $O(n \log n)$" is not evidence; your recurrence and your measurements are.
- Cite any website, book or classmate that helped you.
