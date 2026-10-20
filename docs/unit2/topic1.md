# Asymptotic Analysis

!!! abstract "At a glance"

    - **Problem:** compare algorithms in a way that does not depend on the machine, language, compiler, or the particular test data.
    - **Key idea:** express cost as a function $T(n)$ of the input size $n$, count basic operations instead of seconds, and keep only the dominant growth term.
    - **Cases:** best, worst, and average case are three *different functions* of $n$; worst case is the usual guarantee.
    - **Check:** doubling experiments ($T(2n)/T(n)$) let you confirm a theoretical growth rate empirically.
    - **Formal notation** ($O$, $\Omega$, $\Theta$) is defined precisely in [2.5 O, Ω, Θ Notation](topic5.md); this page builds the intuition it formalises.

## Motivation and Problem Context

Suppose two teams submit solutions for de-duplicating customer records. Team A's code takes 0.8 s on the test file; Team B's takes 1.1 s. Which is better? You cannot tell:

- the runs may have been on different laptops, with different Python versions, under different load;
- the test file has 10,000 records, but production has 50 million;
- Team A's code might be fast only because the test file happened to be almost sorted.

A stopwatch measures *one program, on one machine, on one input*. Algorithm design needs a statement about *the algorithm, on any reasonable machine, for every input of a given size, as that size grows*. That is exactly what asymptotic analysis provides. It answers: **"If the input grows by a factor of 10, what happens to the cost?"** An algorithm whose cost grows like $n^2$ becomes 100 times slower; one that grows like $n \log n$ becomes only about 10–13 times slower. No amount of hardware tuning changes that ratio.

!!! note "What an algorithm is"

    An algorithm is a finite sequence of unambiguous instructions that transforms an input into an output. Knuth's classic criteria still frame what we analyse:

    | Property | Meaning |
    |---|---|
    | Input | zero or more quantities supplied externally |
    | Output | at least one quantity is produced |
    | Definiteness | each step is precisely and unambiguously specified |
    | Finiteness | it terminates after a finite number of steps on every valid input |
    | Effectiveness | each step is basic enough to be carried out exactly in finite time |

    Asymptotic analysis studies how many of those basic steps are needed, as a function of input size.

## Problem Formulation

Analysing an algorithm $A$ means producing a function, not a number.

- **Input:** an algorithm $A$ and a family of inputs, grouped by size $n$.
- **Output:** a function $T_A(n)$ (time) or $S_A(n)$ (extra space), usually simplified to its order of growth.
- **Assumptions:** a fixed [model of computation](topic2.md) that says which operations cost one unit; a precise definition of input size; a stated case (best, worst, average, or amortized).

### Choosing the input size $n$

The measure of "size" must reflect what actually drives the work. Choosing it badly gives meaningless results.

| Problem | Natural size measure | Why |
|---|---|---|
| Sorting / searching an array | number of elements $n$ | each element is touched or compared |
| Graph algorithms | vertices $V$ **and** edges $E$ (two parameters) | sparse and dense graphs behave very differently |
| Matrix multiplication | dimension $n$ of an $n \times n$ matrix (input has $n^2$ entries) | state which one you use |
| String matching | text length $n$ and pattern length $m$ | both matter |
| Primality / arithmetic on a number $N$ | number of bits $b = \lceil \log_2(N+1) \rceil$ | the input is written in $b$ bits, not $N$ symbols |

!!! warning "Important"

    For numeric inputs, the input size is the number of **bits**, not the value. Trial division up to $\sqrt{N}$ takes about $\sqrt{N} = 2^{b/2}$ steps, which is **exponential** in the input size $b$, even though it "looks" sublinear in $N$. This distinction (pseudo-polynomial vs polynomial) is revisited in [2.2 Model of Computation](topic2.md).

## Intuition

Think of an algorithm's cost as a sum of many terms, for example $T(n) = 3n^2 + 20n + 500$. For small $n$ the constant 500 dominates; for moderate $n$ the $20n$ term matters; but once $n$ passes a few hundred, $3n^2$ accounts for almost all of the cost, and its share only increases. The constant 3 depends on the machine and compiler; the exponent 2 depends on the algorithm. **Asymptotic analysis keeps the part that the algorithm controls (the shape of the growth) and discards the parts that the environment controls (constants and small terms).**

<figure markdown="span">
    ![Common growth rates](../img/u2/algoGrowthRate.jpg){width="80%"}
    <figcaption>Number of computations versus input size for the common growth classes, from constant and logarithmic up to exponential and factorial.</figcaption>
</figure>

## Definitions

**Basic (primitive) operation.** An operation that the model of computation charges one unit for: an arithmetic operation on a machine word, a comparison, an assignment, an array access, a function call/return. See [2.2](topic2.md) for what is and is not unit cost.

**Running time $T(n)$.** The number of basic operations executed on an input of size $n$. Because different inputs of the same size can take different time, $T$ is not yet well defined until we pick a *case*.

**Cost model shortcut: the dominant (key) operation.** Instead of counting every operation, pick the operation executed most often (or the one whose count is proportional to the total), e.g. *key comparisons* in sorting. The total work is within a constant factor of that count, which is all asymptotic analysis needs.

### Best, worst, and average case

Let $I_n$ be the set of all inputs of size $n$ and $t(x)$ the cost on input $x$.

| Case | Definition | What it tells you |
|---|---|---|
| Worst case | $T_{\text{worst}}(n) = \max_{x \in I_n} t(x)$ | a **guarantee**: no input of size $n$ is slower |
| Best case | $T_{\text{best}}(n) = \min_{x \in I_n} t(x)$ | the floor; rarely useful alone, but shows adaptivity |
| Average case | $T_{\text{avg}}(n) = \sum_{x \in I_n} \Pr[x]\, t(x)$ | expected cost **under a stated input distribution** |
| Amortized | total cost of a sequence of $m$ operations divided by $m$, worst case over sequences | per-operation cost of data structures like dynamic arrays |
| Expected (randomized) | expectation over the algorithm's own coin flips, for the **worst** input | used for randomized quicksort, hashing ([5.4](../unit5/topic4.md)) |

!!! warning "Important"

    Best/worst/average case describe **which inputs** you analyse. $O$/$\Omega$/$\Theta$ describe **how a function is bounded**. They are independent: you can give an $O$, $\Omega$ or $\Theta$ bound for *any* of the cases. "Big-O means worst case" is a classic exam error; see [2.5](topic5.md).

### Order of growth

The **order of growth** of $T(n)$ is its leading term with the constant coefficient dropped: $3n^2 + 20n + 500$ has order of growth $n^2$, written $\Theta(n^2)$. The formal justification is in [2.5](topic5.md); the full catalogue of growth functions is in [2.6](topic6.md).

## Key Results

1. **Constant factors do not change the order of growth.** $T(n)$ and $c \cdot T(n)$ for a constant $c > 0$ scale identically: doubling $n$ multiplies both by the same factor.
2. **Lower-order terms vanish.** If $T(n) = a_k n^k + \dots + a_0$ with $a_k > 0$, then $T(n)/(a_k n^k) \to 1$, so the leading term governs.
3. **A higher order of growth always loses eventually.** For any constants $a, b > 0$, $a n^2 > b\, n \log_2 n$ for all sufficiently large $n$, no matter how much larger $b$ is than $a$.
4. **Scaling behaviour identifies the class.** If $T(n) \approx c\, n^k$, then $T(2n)/T(n) \to 2^k$. This is the basis of the doubling experiment below.

!!! warning "Important"

    "Eventually" can be large. Insertion sort ($\approx n^2/4$ comparisons on average) beats merge sort ($\approx n \log_2 n$ comparisons plus copying overhead) on small arrays, which is why production sorts switch to insertion sort for short runs (typically a few dozen elements). Asymptotics decides which algorithm wins **at scale**; constants decide which wins **at small $n$**.

### Growth-rate table

Approximate values (logarithms base 2):

| $n$ | $\log_2 n$ | $n$ | $n \log_2 n$ | $n^2$ | $n^3$ | $2^n$ |
|---|---|---|---|---|---|---|
| 10 | 3.3 | 10 | 33 | 100 | 1,000 | 1,024 |
| 100 | 6.6 | 100 | 664 | $10^4$ | $10^6$ | $1.3 \times 10^{30}$ |
| 1,000 | 10.0 | 1,000 | 9,966 | $10^6$ | $10^9$ | $1.1 \times 10^{301}$ |
| $10^6$ | 19.9 | $10^6$ | $2.0 \times 10^7$ | $10^{12}$ | $10^{18}$ | (astronomical) |

Read the table column-wise: going from $n = 1{,}000$ to $n = 10^6$ (1000 times larger) multiplies $\log_2 n$ by 2, $n$ by $10^3$, $n^2$ by $10^6$. Topic [2.3](topic3.md) turns this into wall-clock time.

## Method: Step Counting

A repeatable procedure for any iterative algorithm:

1. **Fix $n$** and the case (usually worst).
2. **Assign a cost to each line** (constant for simple statements; a function call costs whatever the callee costs).
3. **Count how many times each line executes**, as a function of $n$. Loops become sums.
4. **Add up** cost × count to get $T(n)$.
5. **Simplify** to the order of growth using the sums below.

Sums that appear constantly:

$$
\sum_{i=1}^{n} 1 = n, \qquad \sum_{i=1}^{n} i = \frac{n(n+1)}{2}, \qquad \sum_{i=1}^{n} i^2 = \frac{n(n+1)(2n+1)}{6}, \qquad \sum_{i=0}^{k} 2^i = 2^{k+1}-1.
$$

For recursive algorithms step 3 produces a **recurrence** instead of a sum; solving recurrences is the subject of [Unit 3](../unit3/overview.md).

## Worked Examples

### Example 1: single loop

```text
total ← 0
for i ← 1 to n
    total ← total + A[i]
```

The body runs $n$ times, the loop header $n+1$ times, the initialisation once: $T(n) = c_1 + c_2(n+1) + c_3 n = \Theta(n)$. Best = worst = average, since no branch depends on the data.

### Example 2: independent nested loops

```text
for i ← 1 to n
    for j ← 1 to n
        count ← count + 1
```

Inner body: $n \cdot n = n^2$ executions, so $\Theta(n^2)$.

### Example 3: dependent nested loops

```text
for i ← 1 to n
    for j ← i + 1 to n
        if A[i] = A[j] then duplicates ← duplicates + 1
```

For a given $i$ the inner loop runs $n - i$ times, so the comparison executes

$$
\sum_{i=1}^{n} (n - i) = \sum_{k=0}^{n-1} k = \frac{n(n-1)}{2}
$$

times. This is still $\Theta(n^2)$; the triangle shape halves the constant but does not change the growth.

### Example 4: halving loop

```text
k ← 0
while n > 1
    n ← ⌊n / 2⌋
    k ← k + 1
```

After $t$ iterations $n$ has become at most $n_0 / 2^t$; the loop stops once this is $\le 1$, i.e. after exactly $\lfloor \log_2 n_0 \rfloor$ iterations. Any loop that divides the problem by a constant factor each step runs $\Theta(\log n)$ times; this is the engine behind binary search ([4.5](../unit4/topic5.md)).

### Example 5: linear search, three cases

```text
LINEAR-SEARCH(A[1..n], x)
    for i ← 1 to n
        if A[i] = x then return i
    return NOT-FOUND
```

Counting key comparisons:

| Case | Input that causes it | Comparisons | Order |
|---|---|---|---|
| Best | $x = A[1]$ | 1 | $\Theta(1)$ |
| Worst | $x$ is last, or absent | $n$ | $\Theta(n)$ |
| Average (present, each position equally likely) | $\Pr[x = A[i]] = 1/n$ | $\frac{1}{n}\sum_{i=1}^{n} i = \frac{n+1}{2}$ | $\Theta(n)$ |
| Average (present with probability $p$) | as above, absent with prob. $1-p$ | $p\frac{n+1}{2} + (1-p)n$ | $\Theta(n)$ |

The average-case result depends on the assumed distribution; change the assumption and the formula changes. That is why an average-case claim must always state its distribution.

### Example 6: insertion sort, three cases

```text
INSERTION-SORT(A[1..n])
    for j ← 2 to n
        key ← A[j]
        i ← j − 1
        while i ≥ 1 and A[i] > key
            A[i + 1] ← A[i]
            i ← i − 1
        A[i + 1] ← key
```

Let $t_j$ be the number of times the `while` test runs for a given $j$. The shifts executed equal $t_j - 1$.

- **Best case (already sorted):** the test fails immediately, $t_j = 1$, giving $n-1$ comparisons: $\Theta(n)$.
- **Worst case (reverse sorted):** every earlier element is shifted, $t_j = j$, so the test runs $\sum_{j=2}^{n} j = \frac{n(n+1)}{2} - 1$ times: $\Theta(n^2)$.
- **Average case (all permutations equally likely):** each shift removes exactly one *inversion* (a pair $i<j$ with $A[i]>A[j]$). A random permutation has $\binom{n}{2}/2 = n(n-1)/4$ inversions in expectation (each pair is inverted with probability $1/2$), so the expected number of shifts is $n(n-1)/4$: $\Theta(n^2)$.

Insertion sort's correctness proof (loop invariant) is in [2.4](topic4.md); its place among sorting algorithms is in [5.1](../unit5/topic1.md).

## Empirical Analysis: Doubling Experiments

Theory predicts growth; measurement checks it (and catches analysis mistakes or hidden costs such as a list slice inside a loop). The **doubling experiment**:

1. Run the program on inputs of size $n, 2n, 4n, 8n, \dots$, keeping the input distribution fixed.
2. Record the best of a few repetitions to reduce noise.
3. Compute $r = T(2n)/T(n)$. If $T(n) \approx c n^k$, then $r \to 2^k$, so $k \approx \log_2 r$.

| Observed ratio $r$ | Suggests |
|---|---|
| $\approx 1$ | $\Theta(1)$ or $\Theta(\log n)$ (log adds a constant per doubling) |
| $\approx 2$ | $\Theta(n)$; slightly above 2 suggests $\Theta(n \log n)$ |
| $\approx 4$ | $\Theta(n^2)$ |
| $\approx 8$ | $\Theta(n^3)$ |
| itself growing with $n$ | exponential, or the data no longer fits in cache/RAM |

| | Theoretical analysis | Empirical analysis |
|---|---|---|
| Result | a function valid for all $n$ and all machines | numbers valid for this machine, this input set |
| Covers worst case | yes, by argument | only if you know how to generate worst inputs |
| Sees constants, caches, interpreters | no | yes |
| Cost | thinking time | implementation and test-harness time |
| Best use | choosing an algorithm; guarantees | validating an implementation; tuning |

Use both: theory to choose, experiment to confirm.

## Python Implementation

Operation counters for the two worked examples, plus a reusable doubling-experiment harness.

```python
import math
import time


def linear_search_count(items, target):
    """Return (index of target or -1, number of key comparisons)."""
    comparisons = 0
    for index, value in enumerate(items):
        comparisons += 1
        if value == target:
            return index, comparisons
    return -1, comparisons


def insertion_sort_count(items):
    """Sort a copy of items; return (sorted list, comparisons, shifts)."""
    a = list(items)
    comparisons = 0
    shifts = 0
    for j in range(1, len(a)):
        key = a[j]
        i = j - 1
        while i >= 0:
            comparisons += 1
            if a[i] <= key:
                break
            a[i + 1] = a[i]
            shifts += 1
            i -= 1
        a[i + 1] = key
    return a, comparisons, shifts


def doubling_experiment(func, make_input, start=1000, rounds=5, repeats=3):
    """Time func on sizes start, 2*start, 4*start, ... and print growth ratios."""
    previous = None
    for r in range(rounds):
        n = start * (2 ** r)
        data = make_input(n)
        best = float("inf")
        for _ in range(repeats):
            copy = list(data)
            t0 = time.perf_counter()
            func(copy)
            best = min(best, time.perf_counter() - t0)
        if previous is None:
            print(f"{n:>8} {best:10.4f}s")
        else:
            ratio = best / previous
            print(f"{n:>8} {best:10.4f}s  ratio={ratio:5.2f}  exponent~{math.log2(ratio):4.2f}")
        previous = best
```

Walkthrough:

- The counters count **comparisons**, the dominant operation, not seconds; on a sorted input `insertion_sort_count` reports $n-1$ comparisons and on a reversed input $n(n-1)/2$, matching the analysis. `shifts` always equals the number of inversions.
- `doubling_experiment` copies the input before each run so an in-place sort does not receive already-sorted data on the second repetition (a classic measurement bug).
- Taking the **minimum** of repeats filters out interference from other processes; the minimum is the run with the least noise.
- On a typical laptop, `insertion_sort_count` shows ratios near 4 (exponent about 2) and Python's built-in `sorted` on random floats shows ratios slightly above 2 (exponent about 1.1), consistent with $\Theta(n^2)$ and $\Theta(n \log n)$.

## Edge Cases and Pitfalls

| Case / pitfall | What goes wrong | Fix |
|---|---|---|
| Measuring $n$ in values, not bits, for numeric problems | "$O(\sqrt{N})$" primality looks fast but is exponential in input length | state size as $b = \log_2 N$ bits |
| Hidden loops in library calls (`x in list`, `list.pop(0)`, slicing, string `+=`) | a "single loop" is actually $\Theta(n^2)$ | know the cost of each built-in operation; count it |
| Ignoring a second size parameter | "$O(n)$" for a graph algorithm that is really $O(V + E)$ | keep all independent parameters |
| Average case with no stated distribution | the claim is unfalsifiable | state the distribution (e.g. uniform random permutation) |
| Doubling experiment with too small $n$ | timer resolution and start-up costs dominate; ratios near 1 | start where one run takes at least a few milliseconds |
| Reusing a mutated input across timing repeats | sorted input on later runs hides the true cost | copy input per run |
| Treating $\log n$ base as significant | confusion between $\log_2 n$ and $\ln n$ | bases differ only by a constant factor ([2.6](topic6.md)) |

## Common Misconceptions

- **"Asymptotic analysis says which program is faster."** It says which one *scales* better. For small $n$, a $\Theta(n^2)$ algorithm with tiny constants can win. Correct model: asymptotics ranks growth; benchmarks rank actual speed at a given size.
- **"Worst case is pessimistic and therefore useless."** Worst case is the only bound that holds for adversarial or unlucky inputs, which is exactly what latency SLAs, security (algorithmic-complexity attacks on hash tables), and real-time systems need.
- **"Average case = typical case."** Average case is an expectation under an assumed distribution; real data (nearly sorted logs, duplicate-heavy keys) may follow a very different distribution.
- **"Best case is the lower bound of the problem."** Best case is a property of *one algorithm on its luckiest input*. A lower bound for a *problem* (e.g. $\Omega(n \log n)$ comparisons for sorting, [5.2](../unit5/topic2.md)) constrains every algorithm.
- **"Two nested loops always mean $n^2$."** Only if both loops run $\Theta(n)$ times. A loop over `j` that halves each time inside a loop over `i` gives $\Theta(n \log n)$; loops whose total work is bounded by a shared pointer (two-pointer technique) give $\Theta(n)$.

## Alternatives and Trade-offs

| Way to assess an algorithm | Strength | Weakness | Use when |
|---|---|---|---|
| Exact step count $T(n)$ | precise, compares constants | tedious, model-dependent | comparing two algorithms of the same order |
| Asymptotic order of growth | machine-independent, quick | hides constants and small-$n$ behaviour | choosing between designs; reasoning about scale |
| Worst-case analysis | guarantee | may be overly pessimistic | latency bounds, adversarial inputs |
| Average-case analysis | reflects typical behaviour | depends on distribution assumption | inputs truly random, or randomised algorithms |
| Amortized analysis | tight for operation sequences | says nothing about a single operation's latency | data structures (dynamic arrays, union-find) |
| Benchmarking | captures real hardware effects | specific to machine and data | final tuning, validating theory |

Do **not** rely on asymptotics alone when $n$ is bounded and small (an embedded table with 20 entries), or when constants differ by orders of magnitude (disk I/O vs in-memory work).

## In Practice

- **Hybrid algorithms exist because of constants.** CPython's `list.sort` (Timsort, with the Powersort merge policy since Python 3.11) uses binary insertion sort to build short runs; C++ `std::sort` implementations are typically introsort with an insertion-sort pass for small partitions. Asymptotically better is combined with practically better at small $n$.
- **Complexity bugs are production bugs.** A common real-world pattern is code that is fine on a developer's 1,000-row test database and times out on a 10-million-row production table because a query or loop is quadratic. Asking "what is $n$ in production?" during code review catches this.
- **Algorithmic-complexity attacks.** If an attacker can force the worst case (for example, many keys that collide in a hash table), an $O(1)$-average operation becomes $O(n)$. This is why many language runtimes randomise their string hashing.
- **Profilers measure, they do not predict.** A profile on small data shows where time goes now; a doubling experiment shows how it will grow.

## Interview and Competitive Programming

Recognition cues:

- "Single pass", "running total" → $\Theta(n)$.
- "Halve the search space", "sorted array", "monotone predicate" → $\Theta(\log n)$ per query.
- "All pairs" → $\Theta(n^2)$; "all triples" → $\Theta(n^3)$; "all subsets" → $\Theta(2^n)$; "all orderings" → $\Theta(n!)$.

Typical constraint-to-complexity mapping (about $10^8$ simple operations per second in C++, noticeably fewer in Python):

| Constraint on $n$ | Target complexity |
|---|---|
| $n \le 10$–$12$ | $O(n!)$, $O(n \cdot n!)$ |
| $n \le 20$–$25$ | $O(2^n)$, $O(n 2^n)$ |
| $n \le 500$ | $O(n^3)$ |
| $n \le 5000$ | $O(n^2)$ |
| $n \le 10^5$–$10^6$ | $O(n \log n)$ or $O(n)$ |
| $n \le 10^{18}$ | $O(\log n)$ or $O(1)$ (math, binary search, fast exponentiation) |

Traps: hidden $O(n)$ operations in Python (`list.insert(0, x)`, `in` on a list, slicing inside a loop); string concatenation in a loop; forgetting that a recursive solution without memoisation may be exponential.

## Using AI Assistants Critically

- LLM-generated code frequently claims "$O(n)$" while containing `x in some_list` or `list.pop(0)` inside a loop; re-derive the cost line by line yourself.
- Ask the assistant **which case** (best/worst/average) and **which distribution** a claimed bound refers to; vague answers usually mean the claim is not justified.
- Watch for confusion between $O$ and worst case in explanations ("Big-O is the worst case"); correct it using [2.5](topic5.md).
- Verify any claimed complexity with a doubling experiment like the harness above: a claimed $O(n \log n)$ that shows ratios near 4 is wrong.
- Generated operation counters often count the wrong thing (e.g. counting loop iterations instead of comparisons, or missing the final failed comparison); check against hand-computed values for $n = 0, 1, 2$ and for sorted and reversed inputs.
- For average-case claims, ask for the derivation, then check it with a quick simulation (as done above for the $n(n-1)/4$ inversions).

## Practice

### Beginner

1. **Count a loop.** Given `for i in range(n): for j in range(5): work()`, state the exact number of `work()` calls and the order of growth. Input: $n \ge 0$. Difficulty: easy.
2. **Best/worst case of max.** For finding the maximum of an unsorted array of $n \ge 1$ integers, give the number of comparisons in best and worst case. Difficulty: easy.
3. **Read a growth table.** If an algorithm takes 2 s at $n = 10^4$ and is $\Theta(n^2)$, estimate the time at $n = 4 \times 10^4$. Difficulty: easy.

### Intermediate

1. **Triangular loop.** Count the exact number of times the innermost statement runs in `for i in 1..n: for j in 1..i: for k in 1..j: work()`. Output: closed form and order. Difficulty: medium.
2. **Average case with probability.** Linear search where the key is present with probability $p$ and, if present, is at position $i$ with probability proportional to $1/i$. Derive the expected comparisons. Difficulty: medium.
3. **Doubling data.** Timings for $n = 1000, 2000, 4000, 8000$ are 0.5, 2.1, 8.3, 33.0 ms. Estimate the exponent and predict $n = 64{,}000$. Difficulty: medium.

### Advanced

1. **Hidden quadratic.** A Python function builds a string by `s += word` for $n$ words of length $L$. Analyse the worst-case time in a model where strings are immutable, and explain why CPython often runs faster than this bound. Difficulty: hard.
2. **Two-parameter analysis.** An algorithm scans every vertex and, for each, all of its outgoing edges. Show the total work is $\Theta(V + E)$, not $\Theta(V \cdot E)$. Difficulty: medium-hard.
3. **Adversarial input.** Design an input family on which insertion sort makes exactly $k$ shifts for any given $0 \le k \le n(n-1)/2$. Difficulty: hard.

### Interview / Competitive Programming

1. **Constraint reading.** $n \le 2 \times 10^5$, $q \le 2 \times 10^5$ queries on an array. Which per-query complexities are acceptable? Difficulty: medium.
2. **Two-sum complexity.** Give the time and space of the brute-force and hash-set solutions to "find two numbers summing to $t$" (LeetCode 1 Two Sum). Difficulty: easy.
3. **Spot the trap.** A solution uses `bisect.insort` to keep a list sorted while inserting $n$ elements. Is it $O(n \log n)$? Justify. Difficulty: medium.

## Self-Check Questions

??? question "Q1. Why do we count basic operations instead of measuring time in seconds?"

    Seconds depend on hardware, language, compiler, and system load; the number of basic operations depends only on the algorithm and the input. Under a fixed model of computation each basic operation takes bounded time, so seconds are proportional to the operation count, and the *growth* of that count is a machine-independent property.

??? question "Q2. Insertion sort is $\Theta(n)$ in the best case and $\Theta(n^2)$ in the worst case. What is its running time?"

    There is no single function: the running time depends on the input. You can say the running time is $O(n^2)$ and $\Omega(n)$ over all inputs. Its worst-case running time is $\Theta(n^2)$ and its best-case running time is $\Theta(n)$. Saying "insertion sort is $\Theta(n^2)$" without naming a case is imprecise.

??? question "Q3. A doubling experiment shows ratios of 2.0, 2.1, 2.1, 2.2. What do you conclude?"

    Roughly linear growth with a slowly increasing ratio, consistent with $\Theta(n \log n)$: for $n \log n$, $T(2n)/T(n) = 2 \cdot \frac{\log 2n}{\log n} = 2(1 + 1/\log_2 n)$, which is slightly above 2. A rising ratio can also indicate data spilling out of cache, so confirm with the analysis.

??? question "Q4. Why must an average-case analysis state a distribution?"

    The average is $\sum_x \Pr[x] t(x)$; different distributions give different averages. Quicksort with a first-element pivot averages $\Theta(n \log n)$ over random permutations but is $\Theta(n^2)$ on the sorted inputs that real systems often see.

??? question "Q5. A loop runs `while n > 0: n = n // 3`. How many iterations, in terms of the initial $n$?"

    $\lfloor \log_3 n \rfloor + 1$ for $n \ge 1$: the loop strips one base-3 digit per iteration, so it runs once per digit of $n$ in base 3. The order is $\Theta(\log n)$; the base only changes the constant.

??? question "Q6. Algorithm A takes $100 n \log_2 n$ steps and B takes $n^2$ steps. For which $n$ is A faster?"

    A is faster when $100 \log_2 n < n$. At $n = 1000$, $100 \log_2 n \approx 997 < 1000$, and the crossover is at $n = 997$ (for all $2 \le n \le 996$, B is faster). B wins below the crossover despite its worse growth rate.

??? question "Q7. Your code passes all tests on 1,000 records but times out on 1,000,000. What is the first thing to check?"

    The order of growth. Growing $n$ by 1000× multiplies $\Theta(n^2)$ work by $10^6$; look for nested iteration over the data, hidden linear operations inside loops (membership tests on lists, repeated slicing, repeated string concatenation), or a database query issued once per row.

## Complexity Summary

| Pattern | Count | Order |
|---|---|---|
| Single loop over $n$ | $n$ | $\Theta(n)$ |
| Loop dividing $n$ by a constant | $\approx \log_b n$ | $\Theta(\log n)$ |
| Two independent nested loops | $n^2$ | $\Theta(n^2)$ |
| Triangular nested loops ($j > i$) | $n(n-1)/2$ | $\Theta(n^2)$ |
| Outer $n$, inner halving | $n \log n$ | $\Theta(n \log n)$ |
| Linear search best / worst / avg | $1$ / $n$ / $(n+1)/2$ | $\Theta(1)$ / $\Theta(n)$ / $\Theta(n)$ |
| Insertion sort best / worst / avg | $n-1$ / $\approx n^2/2$ / $\approx n^2/4$ | $\Theta(n)$ / $\Theta(n^2)$ / $\Theta(n^2)$ |

## Key Takeaways

- Analyse algorithms as functions of input size $n$, counting basic operations under a fixed model of computation.
- Choose $n$ carefully: number of elements for collections, $V$ and $E$ for graphs, number of bits for numbers.
- Best, worst, and average case are different functions; worst case is the standard guarantee, and average case needs a stated distribution.
- Keep the dominant term and drop constants: the order of growth is what the algorithm controls.
- Asymptotic superiority wins at scale; constants win at small $n$, which is why practical libraries use hybrid algorithms.
- Confirm theoretical growth with doubling experiments: a ratio of $2^k$ indicates $\Theta(n^k)$.
- The formal tools, $O$, $\Omega$, $\Theta$, are defined in [2.5](topic5.md); the functions you will meet are catalogued in [2.6](topic6.md).
