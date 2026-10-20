# Assignment 2: Closest Camera Traps

!!! abstract "At a glance"
    - **Units:** 2 to 4 (asymptotic analysis, recurrences, divide and conquer)
    - **Marks:** 15
    - **Hand in:** `closest.py`, `test_closest.py`, and a short report (maximum 4 pages, including a reflection of at most 400 words)

## Scenario

Camera traps in Jigme Dorji National Park are placed on a map grid. Two traps placed very close together record the same animals and waste batteries. The field team wants the **closest pair of traps** so it can move one of them. With tens of thousands of traps, checking every pair is too slow.

## What You Will Use

- Closest pair by divide and conquer: [4.1 Divide and Conquer](../unit4/topic1.md)
- Writing and solving recurrences: [3.1 Recurrence Relations](../unit3/topic1.md), [3.5 Master Method](../unit3/topic5.md)
- Measuring growth rates: [2.1 Asymptotic Analysis](../unit2/topic1.md)

## Problem

**Input:** a list of `n ≥ 2` points `(x, y)`.
**Output:** `(d, i, j)`: the smallest distance `d` and the indices `i < j` of the two points.

```text
points = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
output = (1.414..., 0, 5)        # (2, 3) and (3, 4)
```

```python
def closest_pair_brute(points): ...   # check every pair
def closest_pair(points): ...         # divide and conquer
```

## Tasks

### Part A: Implement

1. `closest_pair_brute(points)`: compare every pair, Θ(n²).
2. `closest_pair(points)`: divide and conquer. Sort by x, split at the middle, solve both halves, then check the strip of width 2δ around the dividing line.

### Part B: Test

1. Check `closest_pair` against `closest_pair_brute` on at least 500 random inputs of 2 to 50 points.
2. Test these cases: exactly 2 points, duplicate points (answer 0), all points on one vertical line, and the closest pair lying on opposite sides of the dividing line.

### Part C: Analyse

1. Write the recurrence for your divide-and-conquer version and solve it with the Master Method.
2. Time both functions for n = 1,000, 2,000, 4,000, ..., 64,000 (stop brute force after 60 seconds). Show a table and a log-log graph.
3. Find the smallest n at which divide and conquer becomes faster than brute force on your machine.

### Part D: Critical Reflection (maximum 400 words)

Answer **three** of the following, using your own results:

1. Did your measured growth match your recurrence? If not, why not?
2. Why is brute force faster for small n even though it is Θ(n²)?
3. Which edge case was hardest to get right, and how did testing help?
4. If you used an AI tool, what did it get right or wrong, and how did you check it?

## Deliverables

- [ ] `closest.py` (Part A)
- [ ] `test_closest.py` (Part B), all tests passing
- [ ] Report: recurrence and solution, timing table and graph, crossover point, reflection
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
