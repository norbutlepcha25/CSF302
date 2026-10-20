# Assignment 3: Fixing a Slow Quicksort

!!! abstract "At a glance"
    - **Unit:** 5 (sorting)
    - **Marks:** 15
    - **Hand in:** `sorts.py`, `test_sorts.py`, and a short report (maximum 4 pages, including a reflection of at most 400 words)

## Scenario

A bank in Thimphu sorts its daily mobile-payment transactions by amount every night. The data often arrives **already sorted** and has **many repeated amounts** (Nu 100 and Nu 500 top-ups). A textbook quicksort worked on random test data, but on real data it ran very slowly or crashed with `RecursionError`. Your job is to explain why and fix it.

## What You Will Use

- Quicksort and its worst case: [5.3 Quicksort Analysis](../unit5/topic3.md)
- Random pivots: [5.4 Randomised Quicksort](../unit5/topic4.md)
- Insertion sort: [5.1 Comparison-based Sorting](../unit5/topic1.md)

## Problem

Sort a list of integers in place into ascending order. Do not use `sorted()` or `list.sort()` inside your functions; use them only to check your answers.

```python
def quicksort_basic(a): ...                 # last element as pivot
def quicksort_improved(a, cutoff=16): ...   # random pivot + insertion sort for small parts
```

## Tasks

### Part A: Implement

1. `quicksort_basic(a)`: Lomuto partition with the last element as pivot.
2. `quicksort_improved(a, cutoff)`:
    - choose a **random pivot**;
    - use **insertion sort** for parts of size ≤ `cutoff`;
    - recurse on the **smaller** part and loop on the larger one, so that the recursion depth stays O(log n).

### Part B: Test

1. Check both sorts against `sorted()` on at least 500 random lists.
2. Test these cases: an empty list, one element, all equal, already sorted, reverse sorted, and negative numbers.

### Part C: Analyse

1. Time both sorts for n = 1,000, 2,000, 4,000, ..., 64,000 on three input types: random, already sorted, and many duplicates (values 0 to 9). Record any crash as a result. Show tables and graphs.
2. Explain the slow case of `quicksort_basic` using the recurrence T(n) = T(n − 1) + Θ(n).
3. For n = 100,000 random values, time `quicksort_improved` with cutoff = 1, 4, 8, 16, 32 and 64. Choose the best cutoff.
4. Compare your best version with Python's `sorted()`.

### Part D: Critical Reflection (maximum 400 words)

Answer **three** of the following, using your own results:

1. Why did the basic quicksort fail on sorted data, and which assumption of the average-case analysis did real data break?
2. Insertion sort is Θ(n²). Why does using it for small parts make quicksort faster?
3. Why is `sorted()` still faster than your best version? How much of the difference comes from the algorithm and how much from the language?
4. If you used an AI tool, what did it get right or wrong, and how did you check it?

## Deliverables

- [ ] `sorts.py` (Part A)
- [ ] `test_sorts.py` (Part B), all tests passing
- [ ] Report: timing tables and graphs, recurrence explanation, chosen cutoff, comparison with `sorted()`, reflection
## Marking (15 marks)

| Criterion (module descriptor) | What is assessed | Marks |
|---|---|---|
| Analysis and problem-solving | Part C analysis (2) and critical reflection (3) | 5 |
| Application of concepts | Part A implementation (3) and Part B testing (2) | 5 |
| Presentation and explanation | Clear report, readable code, labelled tables and graphs | 3 |
| Timely submission and correctness | Submitted on time; code runs and gives correct results | 2 |
| **Total** | | **15** |

## Academic Integrity

- Individual work. You may be asked to explain your code in a short viva.
- AI tools are allowed, but state at the top of your report which tool you used and for what. All submitted code must pass your brute-force check.
