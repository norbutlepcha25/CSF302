# Lab Overview

| Lab | Topic | Notes |
|---|---|---|
| [Lab 1](lab1.md) | Empirical growth rates: searching, sorting, primes | [Unit 2](../unit2/overview.md) |
| [Lab 2](lab-02.md) | Step counting: primality, merge sort, matrix multiplication | [Unit 2](../unit2/overview.md), [3.6](../unit3/topic6.md) |
| [Lab 3](lab-03.md) | Divide and conquer: Strassen, Karatsuba, binary vs ternary search | [Unit 4](../unit4/overview.md) |
| [Lab 4](lab-04.md) | Modular and matrix exponentiation | [4.6](../unit4/topic6.md), [4.7](../unit4/topic7.md) |
| [Lab 5](lab-05.md) | Sorting: quicksort variants, linear-time sorts, inversions | [Unit 5](../unit5/overview.md) |
| [Lab 6](lab-06.md) | Dynamic programming: rod cutting, matrix chain, LCS, optimal BST | [Unit 6](../unit6/overview.md) |
| [Lab 7](lab-07.md) | Greedy and randomized algorithms | [Unit 7](../unit7/overview.md) |

## Setup

Python 3.11 or later. Install the libraries once:

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install matplotlib pytest
```

## Rules

- Implement every algorithm yourself. Library calls (`sorted`, `pow`, `heapq`, `math.comb` and so on) may be used only to **check** your answers, unless the question allows them.
- Verify every fast algorithm against a simple brute-force version on small inputs before timing it.
- For timing, use `time.perf_counter()`, keep input generation outside the timed region, repeat each measurement at least 3 times and report the average or median. Fix the random seed.
- Plot growth on a log-log scale where asked.
- AI tools may be used for help, but you must understand and be able to explain every line you submit. State which tool you used and for what at the top of your source file.

## Submission

For every lab submit:

1. Source code files (one per question).
2. Step/frequency count or timing tables for all experiments.
3. Graphs where the question asks for them.
4. A brief analysis/conclusion written as a comment at the end of each source file: does the measurement match the theoretical complexity? If not, why not?
