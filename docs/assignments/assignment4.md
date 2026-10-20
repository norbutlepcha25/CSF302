# Assignment 4: Booking the Hall (Greedy vs Dynamic Programming)

!!! abstract "At a glance"
    - **Units:** 6 and 7 (dynamic programming, greedy algorithms; randomised testing optional from 7.7).
    - **Marks:** 15, assessed with the module-descriptor rubric [below](#marking-rubric).
    - **You build:** four greedy rules, an exact dynamic-programming solution, a brute-force checker and a random counterexample finder.
    - **You prove:** when a greedy rule is optimal, and show with counterexamples when it is not.
    - **You reflect:** 400 to 600 words on the cost of choosing a fast but wrong algorithm.

## Context

A community hall in Paro is rented out for weddings, training workshops, archery-tournament dinners and Losar gatherings. Each booking request has a start time, an end time and a fee. The hall can host only one event at a time. Each month the manager must accept some requests and turn the rest away, and wants to earn as much as possible.

The manager has been using a simple rule: "always accept the request that ends earliest, if it fits". It is quick and easy to explain. Your job is to find out whether it, or any other simple rule, gives the best revenue; to build a method that is always optimal; and to tell the manager what the simple rule is costing them.

## Learning Outcomes

By completing this assignment you will be able to:

1. Formulate a scheduling problem precisely, including the meaning of "compatible" ([6.1 Dynamic Programming Design](../unit6/topic1.md)).
2. Design a dynamic-programming recurrence, justify it with optimal substructure, and reconstruct the solution ([6.1](../unit6/topic1.md), [6.2 Rod Cutting](../unit6/topic2.md)).
3. Prove a greedy rule correct with an exchange argument, and disprove one with a counterexample ([7.1 Greedy Design Principles](../unit7/topic1.md), [7.4 Activity Selection](../unit7/topic4.md)).
4. Use brute force and randomised testing to validate an algorithm and to search for counterexamples ([7.7 Randomized Algorithms](../unit7/topic7.md)).
5. Measure both the running-time cost and the quality cost of an algorithmic choice.

## Problem Statement

**Input.** A list `requests` of $n$ tuples `(start, finish, fee)` with integers $0 \le \text{start} < \text{finish} \le 10^9$ and $1 \le \text{fee} \le 10^6$. Times are in minutes from the start of the month.

**Compatibility.** Intervals are half-open, $[\text{start}, \text{finish})$. Two requests are compatible if one finishes no later than the other starts. So `(9, 12, ...)` and `(12, 14, ...)` are compatible: one event can end at 12 and the next start at 12.

**Output.** A tuple `(total_fee, chosen)` where `chosen` is a list of indices into `requests`, in increasing order, of pairwise compatible requests, and `total_fee` is the sum of their fees. For `best_schedule`, `total_fee` must be the maximum possible. If several selections tie, any one is accepted.

**Constraints.** $0 \le n \le 2 \times 10^5$ for `best_schedule` and the earliest-finish greedy rule, which must run in $O(n \log n)$. Brute force is only for $n \le 15$.

**Example.** (Times shown in hours for readability.)

```text
requests = [(9, 12, 3000), (10, 16, 8000), (13, 17, 4000), (12, 14, 2500), (16, 18, 2000)]

best_schedule(requests)                       -> (10000, [1, 4])
greedy_schedule(requests, "earliest_finish")  -> (7500, [0, 3, 4])
```

The earliest-finish rule earns Nu 2,500 less than the best schedule on this input.

## Requirements

### Functional requirements

| ID | Function | Requirement |
|---|---|---|
| F1 | `greedy_schedule(requests, rule)` | Consider requests in the order given by `rule`, accepting each one that is compatible with all requests accepted so far. Rules: `"earliest_finish"`, `"highest_fee"`, `"fee_per_hour"` (fee divided by duration), `"shortest"`. Break ties by earlier finish, then by lower index. The `"earliest_finish"` rule must run in $O(n \log n)$; the others may use a simple $O(n^2)$ compatibility check. |
| F2 | `best_schedule(requests)` | Dynamic programming in $O(n \log n)$: sort by finish time, compute $p(j)$ (the last request compatible with $j$) by binary search, fill the table, then reconstruct the chosen requests. You may use `bisect`. |
| F3 | `brute_force(requests)` | Try every subset. For $n \le 15$ only. This is your reference. |
| F4 | `find_counterexample(rule, rng, max_n=6, trials=10_000)` | Generate random small instances and return the **smallest** one (fewest requests) on which `rule` earns less than `best_schedule`, or `None` if none is found. |

### Testing requirements

| ID | Requirement |
|---|---|
| T1 | Cross-check F2 against F3 on at least 1,000 random instances with $0 \le n \le 10$. Compare totals, and check that the returned selection is valid and adds up to the returned total. |
| T2 | Check that every greedy result is a valid selection, and never exceeds the optimum. |
| T3 | Edge cases: no requests; one request; all requests overlapping; no requests overlapping; back-to-back requests (finish equals the next start); identical requests; equal fees. |
| T4 | With all fees equal, check that `"earliest_finish"` always matches `best_schedule` (on random instances). |

### Analysis and experimental requirements

| ID | Requirement |
|---|---|
| A1 | **Recurrence.** State the DP recurrence for $\text{OPT}(j)$ with its base case. Justify it with optimal substructure in your own words. |
| A2 | **Proof.** Prove, using an exchange argument, that `"earliest_finish"` is optimal when all fees are equal. |
| A3 | **Counterexamples.** Give a smallest counterexample for each of the four rules (use F4), and explain in one or two sentences why the rule fails on it. |
| E1 | **Running time.** Time F2 and the earliest-finish greedy for $n = 2^{12}, \dots, 2^{18}$ random requests. Report log-log slopes. |
| E2 | **Quality cost.** For $n = 50$, generate 1,000 random instances. For each rule, report the average and worst ratio (greedy revenue / optimal revenue), and how often the rule is optimal. |

## Starter Code

Time your code with `time.perf_counter()` following the [Lab Overview rules](../lab/overview.md#rules). Write your code where you see `# TODO`.

```python
# scheduling.py
"""CSF302 Assignment 4: weighted interval scheduling, greedy vs DP."""
import bisect
import itertools

RULES = ["earliest_finish", "highest_fee", "fee_per_hour", "shortest"]


def compatible(r1, r2):
    """Half-open intervals [start, finish): True if r1 and r2 do not overlap."""
    return r1[1] <= r2[0] or r2[1] <= r1[0]


def is_valid(requests, chosen):
    return all(compatible(requests[i], requests[j]) for i, j in itertools.combinations(chosen, 2))


def total(requests, chosen):
    return sum(requests[i][2] for i in chosen)


def greedy_schedule(requests, rule):
    """F1. Return (total_fee, sorted list of chosen indices)."""
    order_key = {
        "earliest_finish": lambda i: (requests[i][1], i),
        # TODO: "highest_fee", "fee_per_hour", "shortest"
        #       (ties: earlier finish, then lower index)
    }[rule]
    order = sorted(range(len(requests)), key=order_key)
    chosen = []
    # TODO: accept requests[i] if it is compatible with everything chosen so far
    #       (for earliest_finish, comparing with the last accepted finish is enough: why?)
    raise NotImplementedError


def best_schedule(requests):
    """F2. Return (maximum total fee, sorted list of chosen indices) in O(n log n)."""
    order = sorted(range(len(requests)), key=lambda i: requests[i][1])
    finishes = [requests[i][1] for i in order]
    # p[k] = number of requests (in finish order) that end no later than order[k] starts
    p = [bisect.bisect_right(finishes, requests[i][0]) for i in order]
    # TODO: opt[k] = best total using only the first k requests in finish order
    # TODO: walk back through opt to reconstruct which requests were taken
    raise NotImplementedError


def brute_force(requests):
    """F3. Try every subset (n <= 15). Return (maximum total fee, chosen indices)."""
    # TODO
    raise NotImplementedError


def find_counterexample(rule, rng, max_n=6, trials=10_000):
    """F4. Smallest random instance where `rule` is not optimal, or None."""
    # TODO: for n = 1 .. max_n, try `trials` random instances of size n
    #       (small integer times and fees make counterexamples easy to read)
    raise NotImplementedError
```

```python
# test_scheduling.py
import random

from scheduling import (RULES, best_schedule, brute_force, greedy_schedule, is_valid,
                        total)

EXAMPLE = [(9, 12, 3000), (10, 16, 8000), (13, 17, 4000), (12, 14, 2500), (16, 18, 2000)]


def random_requests(rng, n, horizon=20, max_len=8, max_fee=10):
    out = []
    for _ in range(n):
        s = rng.randint(0, horizon)
        out.append((s, s + rng.randint(1, max_len), rng.randint(1, max_fee)))
    return out


def test_example():
    assert best_schedule(EXAMPLE) == (10000, [1, 4])
    assert greedy_schedule(EXAMPLE, "earliest_finish") == (7500, [0, 3, 4])


def test_dp_against_brute_force():
    rng = random.Random(1)
    for _ in range(1000):
        reqs = random_requests(rng, rng.randint(0, 10))
        value, chosen = best_schedule(reqs)
        assert value == brute_force(reqs)[0]
        assert is_valid(reqs, chosen) and total(reqs, chosen) == value


def test_greedy_is_valid_and_never_better():
    rng = random.Random(2)
    for _ in range(300):
        reqs = random_requests(rng, rng.randint(0, 10))
        best = best_schedule(reqs)[0]
        for rule in RULES:
            value, chosen = greedy_schedule(reqs, rule)
            assert is_valid(reqs, chosen) and total(reqs, chosen) == value <= best

# TODO: edge cases (T3) and the equal-fees test (T4)
```

## Deliverables

- [ ] `scheduling.py` with F1 to F4 implemented.
- [ ] `test_scheduling.py` covering T1 to T4, all passing (include the `pytest` summary line).
- [ ] `experiments.py` that reproduces every table and plot from a fixed seed.
- [ ] Report (PDF or Markdown, at most 6 pages excluding code) containing:
    - [ ] A1 to A3: recurrence, exchange-argument proof, and four counterexamples (as small tables or timeline sketches);
    - [ ] E1 and E2 tables and plots, with your machine details;
    - [ ] a one-paragraph recommendation to the hall manager, in plain language;
    - [ ] the critical reflection (400 to 600 words);
    - [ ] an AI-use and help statement.

## Critical Reflection

Write 400 to 600 words. Answer **at least four** of the prompts below, using your own results as evidence.

1. **Proof vs testing.** Your greedy rules passed some tests before you found counterexamples. What does this tell you about using tests to show that a greedy algorithm is correct? Where exactly does your exchange-argument proof (A2) break when fees differ?
2. **Cost of being wrong.** From E2, how much revenue does each rule lose on average and in the worst case? Is "usually optimal" good enough for the manager? Would your answer change if the fees were salaries in a hospital rota?
3. **Time vs quality.** E1 shows both F2 and the greedy rule are $O(n \log n)$. So what does the greedy rule actually save? When would a faster-but-approximate method be the right engineering choice?
4. **Model assumptions.** The model assumes one hall, fixed times, and that every request is known in advance. Which assumption would break first in real life (for example, late bookings, setup time between events, two halls)? How would your algorithm need to change?
5. **Randomised search.** How quickly did `find_counterexample` succeed for each rule? Were the smallest counterexamples it found the same as the ones you would have constructed by hand? What are the limits of random search as evidence?
6. **AI assistance and hindsight.** If you used an AI tool, did it suggest a greedy rule as "optimal"? How did you check it? What would you do differently next time?

## Marking Rubric

Each assignment is marked out of 15 using the module-descriptor criteria. The instructor may move marks between sub-components; the table below is the default split.

| Criterion | Sub-component | Marks |
|---|---|---|
| Analysis and problem-solving | recurrence (A1), exchange-argument proof (A2), counterexamples (A3) | 1 |
| | experimental analysis (E1, E2) interpreted against theory | 1 |
| | **critical reflection** | 3 |
| Application of concepts | F1 to F4 correct; DP in $O(n \log n)$ with reconstruction | 3 |
| | tests T1 to T4, including brute-force cross-check and edge cases | 2 |
| Presentation and explanation | report clarity, code readability, labelled tables and figures; clear advice to the manager | 3 |
| Timely submission and correctness | on time; code runs as submitted and passes the given tests | 2 |
| **Total** | | **15** |

| Criterion (marks) | Excellent | Good | Satisfactory | Poor |
|---|---|---|---|---|
| **Analysis: technical (2)** | (2) Correct recurrence with justification; rigorous exchange argument; minimal, explained counterexamples for all four rules; experiments interpreted | (1.5) Mostly correct; proof has a small gap | (1) Recurrence stated without justification, or proof is only an example | (0 to 0.5) Missing or incorrect |
| **Analysis: critical reflection (3)** | (3) Four or more prompts answered with specific evidence from own results; identifies what assumptions break and the real cost of greedy; honest about limitations | (2) Three or four prompts with some evidence | (1) Generic, little use of own data | (0) Missing, off-topic or far outside the word limit |
| **Application of concepts (5)** | (5) All functions correct and efficient; full tests | (4) Correct; one test category thin | (2 to 3) DP value correct but reconstruction wrong, or greedy not $O(n \log n)$, or F4 missing | (0 to 1) Incorrect or no cross-check |
| **Presentation and explanation (3)** | (3) Clear structure; readable code; labelled tables and plots; manager-friendly recommendation | (2) Mostly clear | (1) Hard to follow | (0) Unreadable or missing |
| **Timely submission and correctness (2)** | (2) On time, and code runs from a clean folder and passes the given tests | | (1) One of the two | (0) Neither |

## Academic Integrity and AI Use

- This is individual work. You may discuss ideas, but the code and the report must be your own. You may be asked to explain or modify your code in a short viva.
- AI tools are allowed under the rules in the [Lab Overview](../lab/overview.md#rules). Include a **disclosure statement**: which tool, for what, and what you changed or rejected. Undisclosed use is treated as academic misconduct.
- A greedy algorithm is not correct because an AI tool, or a passing test, says so. Only a proof or a brute-force check counts as evidence.
- Cite any website, book or classmate that helped you.
