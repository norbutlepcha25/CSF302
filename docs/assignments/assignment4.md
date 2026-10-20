# Assignment 4: Booking the Hall

!!! abstract "At a glance"
    - **Units:** 6 and 7 (dynamic programming, greedy algorithms)
    - **Marks:** 15
    - **Hand in:** `booking.py`, `test_booking.py`, and a short report (maximum 4 pages, including a reflection of at most 400 words)

## Scenario

A community hall in Paro is rented out for weddings, workshops and Losar gatherings. Each booking request has a start time, an end time and a fee. Only one event can use the hall at a time. The manager accepts the request that **ends earliest** if it fits, and wants to know whether this earns the most money.

## What You Will Use

- Activity selection (greedy, earliest finish): [7.4 Activity Selection](../unit7/topic4.md)
- Greedy versus dynamic programming: [7.1 Greedy Design Principles](../unit7/topic1.md)
- Designing a DP recurrence: [6.1 DP Design Principles](../unit6/topic1.md)

## Problem

**Input:** a list of requests `(start, finish, fee)`. Two requests fit together if one finishes no later than the other starts (an event ending at 12 and one starting at 12 both fit).
**Output:** `(total_fee, chosen)`: the total fee and the list of indices of the accepted requests.

```text
requests = [(9, 12, 3000), (10, 16, 8000), (13, 17, 4000), (12, 14, 2500), (16, 18, 2000)]

greedy_earliest_finish(requests) -> (7500,  [0, 3, 4])
best_schedule(requests)          -> (10000, [1, 4])
```

```python
def greedy_earliest_finish(requests): ...
def greedy_highest_fee(requests): ...
def best_schedule(requests): ...      # dynamic programming
def brute_force(requests): ...        # try every subset, n <= 15
```

## Tasks

### Part A: Implement

1. `greedy_earliest_finish`: sort by finish time and accept each request that fits.
2. `greedy_highest_fee`: sort by fee, highest first, and accept each request that fits.
3. `best_schedule`: dynamic programming. Sort by finish time and let `p(j)` be the last request that fits before request `j`. Then `OPT(j) = max(OPT(j−1), fee_j + OPT(p(j)))`. Reconstruct the chosen requests.
4. `brute_force`: try every subset (for checking only).

### Part B: Test

1. Check `best_schedule` against `brute_force` on at least 500 random inputs of 0 to 10 requests.
2. Test these cases: no requests, one request, all overlapping, none overlapping, and back-to-back requests.
3. Check that when **all fees are equal**, `greedy_earliest_finish` always gives the optimal total.

### Part C: Analyse

1. Find a small counterexample (2 to 4 requests) where each greedy rule earns less than the optimum. Explain why each rule fails.
2. Explain in your own words why the DP recurrence is correct (optimal substructure).
3. For 1,000 random inputs of 50 requests, report the average and worst ratio of greedy revenue to optimal revenue for each rule.
4. State the time complexity of each function.

### Part D: Critical Reflection (maximum 400 words)

Answer **three** of the following, using your own results:

1. Your greedy rules passed some tests before you found a counterexample. What does this say about using testing to prove correctness?
2. Should the manager keep the simple rule? Use your revenue ratios from Part C.
3. Why does greedy work when all fees are equal but fail when fees differ?
4. If you used an AI tool, did it claim a greedy rule was optimal? How did you check it?

## Deliverables

- [ ] `booking.py` (Part A)
- [ ] `test_booking.py` (Part B), all tests passing
- [ ] Report: counterexamples, DP explanation, ratio table, complexities, reflection
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
