# Randomised Quicksort and Analysis

!!! abstract "At a glance"

    - **Problem:** deterministic quicksort has inputs (sorted, reverse-sorted, crafted) that force $\Theta(n^2)$ time.
    - **Key idea:** choose the pivot uniformly at random. Bad behaviour now depends on unlucky coin flips, not on the input, so no input is bad.
    - **Result:** for **every** input, the expected number of comparisons is $2(n+1)H_n - 4n \approx 1.39\, n \lg n$, proved with indicator random variables and linearity of expectation; the running time is $O(n \log n)$ with high probability.
    - **Classification:** a Las Vegas algorithm: always correct, running time is random.
    - **In practice:** production sorts combine randomness or pattern detection with a worst-case fallback (introsort, pdqsort).

## Motivation and Problem Context

[Quicksort](topic3.md) is fast on random data, but real data is not random: logs arrive in timestamp order, spreadsheets are re-sorted after small edits, and an attacker can submit input designed to hit the worst case. With a fixed pivot rule, the algorithm's behaviour is a deterministic function of the input, so somebody can always find an input of size $n$ that costs $\Theta(n^2)$. Published attacks of this kind exist: M. D. McIlroy's "A Killer Adversary for Quicksort" (1999) shows how to generate quadratic inputs for essentially any deterministic quicksort by observing its comparisons, and "algorithmic complexity attacks" on web services (sending inputs that trigger worst-case behaviour in hash tables or sorts) are a recognised denial-of-service technique.

Randomisation moves the source of uncertainty from the **input** (which we do not control) to the **algorithm** (which we do). This page proves that the move works, and explains how production libraries go one step further to guarantee $O(n \log n)$ outright.

## Problem Formulation

- **Input:** an arbitrary (possibly adversarial) array $A[1..n]$; for the analysis we assume distinct keys (duplicates are handled by [3-way partition](topic3.md)).
- **Algorithm:** quicksort in which each partition chooses its pivot uniformly at random from the current subarray, independently of all earlier choices.
- **Quantity of interest:** $X$ = total number of key comparisons, a random variable whose distribution depends on the algorithm's coin flips.
- **Goal:** bound $E[X]$ for **the worst input**, i.e. show $\max_{A} E[X \mid A] = O(n \log n)$.

!!! warning "Important"

    **Average-case** analysis averages over a distribution of **inputs** (random permutations) for a deterministic algorithm. **Expected** running time of a randomised algorithm averages over the algorithm's **own random choices** for a fixed, worst-case input. Both give about $1.39\, n \lg n$ for quicksort, but only the second is a guarantee you can rely on without assumptions about the data. Do not use the terms interchangeably in exams.

## Intuition

A pivot is "good" if it lands in the middle half of the current subarray (rank between $m/4$ and $3m/4$). Then both sides have at most $3m/4$ elements. A random pivot is good with probability $1/2$, like a fair coin. Any particular element needs only about $\log_{4/3} n$ good pivots on its path before its subarray shrinks to size 1, and with a fair coin you expect to wait about 2 flips per success. So every element participates in $O(\log n)$ partitions on expectation and, as it turns out, with high probability. Each partition charges $O(1)$ comparisons to each element in it, giving $O(n \log n)$ total.

The cleaner exact analysis below counts comparisons **pair by pair** instead of level by level.

## Baseline Approach

Two "obvious" fixes do not fully solve the problem:

1. **Shuffle the input once, then run deterministic quicksort.** This works: after a uniformly random shuffle, the input is a random permutation and the average-case analysis applies. It costs an extra $O(n)$ pass and is exactly how Sedgewick's textbook implementations protect quicksort. It is equivalent in expectation to choosing random pivots.
2. **Median-of-three pivot.** Fixes sorted and reverse-sorted input, but it is still deterministic, so adversarial "median-of-3 killer" sequences exist.

The bottleneck in both deterministic designs is the same: a fixed rule can be predicted. Random pivots make every choice unpredictable.

## Algorithm Design

Choosing the pivot uniformly at random from $A[lo..hi]$ and swapping it into the position the partition routine expects (here $A[hi]$ for Lomuto) changes nothing else in the algorithm. Correctness is unaffected because [quicksort is correct for any pivot choice](topic3.md); only the running time distribution changes.

The analysis tool is the **indicator random variable**: for an event $E$, $I\{E\} = 1$ if $E$ happens and $0$ otherwise, so $E[I\{E\}] = \Pr[E]$. Combined with **linearity of expectation** ($E[\sum X_k] = \sum E[X_k]$, valid even for dependent variables), it lets us compute $E[X]$ without understanding the joint behaviour of all comparisons. See [Probability and Expectation](../unit1/topic3.md) for the background.

## Pseudocode

```text
RANDOMIZED-QUICKSORT(A, lo, hi)
    if lo < hi
        p = RANDOMIZED-PARTITION(A, lo, hi)
        RANDOMIZED-QUICKSORT(A, lo, p - 1)
        RANDOMIZED-QUICKSORT(A, p + 1, hi)

RANDOMIZED-PARTITION(A, lo, hi)
    k = RANDOM(lo, hi)                    // uniform, inclusive
    swap A[k], A[hi]                      // random pivot moves to the end
    return LOMUTO-PARTITION(A, lo, hi)    // see Topic 5.3
```

## Worked Example

Let the sorted order of the keys be $z_1 < z_2 < z_3 < z_4 < z_5$, and define $Z_{ij} = \{z_i, z_{i+1}, \dots, z_j\}$.

**Will $z_2$ and $z_4$ be compared?** Consider $Z_{24} = \{z_2, z_3, z_4\}$. Until some element of $Z_{24}$ is chosen as a pivot, all three stay together in the same subarray (any pivot outside $Z_{24}$ is either smaller than all of them or larger than all of them). At the moment the first pivot from $Z_{24}$ is chosen, each of its three elements is equally likely to be that pivot:

| First pivot chosen from $Z_{24}$ | Probability | Are $z_2$ and $z_4$ compared? |
| --- | --- | --- |
| $z_2$ | $1/3$ | Yes: the pivot is compared with every element in its subarray, including $z_4$ |
| $z_3$ | $1/3$ | No: $z_2$ goes left, $z_4$ goes right, never meet again |
| $z_4$ | $1/3$ | Yes |

So $\Pr[z_2 \text{ compared with } z_4] = 2/3 = \frac{2}{4 - 2 + 1}$.

**Small exact case, $n = 3$.** Pairs $(z_1, z_2)$ and $(z_2, z_3)$ are adjacent, so $Z_{ij}$ has two elements and they are compared with probability $1$. Pair $(z_1, z_3)$ is compared with probability $2/3$. Hence $E[X] = 1 + 1 + 2/3 = 8/3$, which matches the formula $2(n+1)H_n - 4n = 8 \cdot \frac{11}{6} - 12 = \frac{8}{3}$.

**Experiment.** Running the implementation below on sorted input (the worst case for deterministic last-element quicksort):

| $n$ | mean comparisons (measured) | $2(n+1)H_n - 4n$ | max over runs | $\binom{n}{2}$ (deterministic worst) |
| --- | --- | --- | --- | --- |
| 10 | 24.3 | 24.4 | 38 | 45 |
| 100 | 647.6 | 647.9 | 848 | 4950 |
| 1000 | 11043 | 10986 | 13098 | 499500 |
| 10000 | 154468 | 155772 | 173086 | 49995000 |

Measured means agree with the formula, and even the worst observed run is far below the quadratic count.

## Correctness

### Correctness of the output

Randomised quicksort always returns a sorted array: the inductive proof for quicksort in [Topic 5.3](topic3.md) holds for every pivot choice. Randomness affects only the running time. This is what makes it a **Las Vegas** algorithm.

### Expected number of comparisons (the main theorem)

**Theorem.** For any input of $n$ distinct keys, the expected number of comparisons made by randomised quicksort is

$$
E[X] = \sum_{i=1}^{n-1}\sum_{j=i+1}^{n} \frac{2}{j - i + 1} = 2(n+1)H_n - 4n = O(n \log n),
$$

where $H_n = \sum_{k=1}^{n} 1/k$ is the $n$-th harmonic number.

**Step 1: decompose $X$ into indicators.** Every comparison is between the pivot and some other element of the subarray. After a partition, the pivot is excluded from both recursive calls, so **each pair is compared at most once**. Define

$$
X_{ij} = I\{z_i \text{ is compared with } z_j\}, \qquad X = \sum_{i=1}^{n-1}\sum_{j=i+1}^{n} X_{ij}.
$$

**Step 2: linearity of expectation.**

$$
E[X] = \sum_{i=1}^{n-1}\sum_{j=i+1}^{n} E[X_{ij}] = \sum_{i=1}^{n-1}\sum_{j=i+1}^{n} \Pr[z_i \text{ is compared with } z_j].
$$

**Step 3: the key lemma.** $z_i$ and $z_j$ are compared **if and only if** the first element of $Z_{ij} = \{z_i, \dots, z_j\}$ chosen as a pivot is $z_i$ or $z_j$.

- While no element of $Z_{ij}$ has been a pivot, every pivot $x$ satisfies $x < z_i$ or $x > z_j$, so all of $Z_{ij}$ goes to the same side; $Z_{ij}$ stays inside one subarray.
- If the first pivot from $Z_{ij}$ is $z_i$ (or $z_j$), it is compared with every element of its subarray, including the other endpoint.
- If the first pivot is some $z_k$ with $i < k < j$, then $z_i$ goes left and $z_j$ goes right; they are in different subarrays forever and are never compared.

**Step 4: the probability.** At the moment the first pivot from $Z_{ij}$ is chosen, all $j - i + 1$ elements of $Z_{ij}$ are in the current subarray and the pivot is uniform over that subarray, so conditioned on it falling in $Z_{ij}$ it is uniform over $Z_{ij}$. The two outcomes $z_i$ and $z_j$ are disjoint events, so

$$
\Pr[z_i \text{ compared with } z_j] = \frac{1}{j-i+1} + \frac{1}{j-i+1} = \frac{2}{j-i+1}.
$$

**Step 5: evaluate the sum (upper bound).** Substitute $k = j - i$ (so $k$ runs from $1$ to $n - i$):

$$
E[X] = \sum_{i=1}^{n-1}\sum_{k=1}^{n-i}\frac{2}{k+1}
< \sum_{i=1}^{n-1}\sum_{k=1}^{n}\frac{2}{k}
= 2(n-1)H_n
\le 2n(\ln n + 1) = O(n \log n).
$$

using $H_n \le \ln n + 1$.

**Step 6 (exact value, optional).** Group the terms by $d = j - i + 1$, which takes value $d$ for exactly $n - d + 1$ pairs:

$$
E[X] = \sum_{d=2}^{n} (n - d + 1)\frac{2}{d} = 2(n+1)\sum_{d=2}^{n}\frac{1}{d} - 2(n-1) = 2(n+1)(H_n - 1) - 2(n - 1) = 2(n+1)H_n - 4n.
$$

Since $H_n = \ln n + \gamma + O(1/n)$ with $\gamma \approx 0.5772$, this is $2n\ln n - (4 - 2\gamma)n + O(\log n) \approx 1.386\, n\lg n - 2.85\,n$.

**Lower bound.** $E[X] \ge \sum_{i \le n/2} \sum_{k=1}^{n/2} \frac{2}{k+1} = \Omega(n \log n)$, so $E[X] = \Theta(n \log n)$. This is also forced by the comparison lower bound for randomised algorithms ([Topic 5.2](topic2.md)).

!!! warning "Important"

    The exam-critical steps are: (1) each pair is compared at most once, so $X = \sum X_{ij}$; (2) linearity of expectation; (3) **$z_i, z_j$ compared iff the first pivot from $Z_{ij}$ is $z_i$ or $z_j$**, with the reason; (4) probability $2/(j-i+1)$; (5) harmonic sum $\Rightarrow O(n \log n)$. A common error is writing the probability as $2/n$ or $1/(j-i)$.

## Complexity Analysis

### From comparisons to running time

Each call to `RANDOMIZED-PARTITION` does $O(1)$ work plus work proportional to its comparisons, and there are at most $n$ such calls (each fixes one pivot). Hence the running time is $O(n + X)$ and the expected running time is $O(n + E[X]) = O(n \log n)$ for **every** input.

### High-probability bound (intuition)

The expectation alone does not say how often a run is slow. A stronger statement holds: **randomised quicksort runs in $O(n \log n)$ time with probability at least $1 - 1/n^c$** for a constant $c$ that can be made as large as desired by enlarging the hidden constant. Sketch:

1. Fix one element $e$. Call a partition of $e$'s subarray "good" if the pivot's rank lies in the middle half; this happens with probability $1/2$, independently across partitions.
2. After $\log_{4/3} n$ good partitions, $e$'s subarray has size at most $1$.
3. Among $L = a \lg n$ partitions on $e$'s path (for a suitable constant $a$), the number of good ones is a sum of independent fair coin flips with mean $L/2$. A Chernoff bound shows that fewer than $\log_{4/3} n$ good ones occurs with probability at most $1/n^{c+1}$.
4. A union bound over the $n$ elements: with probability $\ge 1 - 1/n^c$, every element is involved in $O(\log n)$ partitions, so the recursion depth is $O(\log n)$ and total work is $O(n \log n)$.

### How unlikely is the quadratic worst case?

For the run to make all $\binom{n}{2}$ comparisons, every pivot must be the minimum or maximum of its subarray. For a subarray of size $m \ge 2$ that has probability $2/m$, so the whole run is maximally bad with probability

$$
\prod_{m=2}^{n}\frac{2}{m} = \frac{2^{n-1}}{n!},
$$

which for $n = 20$ is about $2 \times 10^{-13}$ and for $n = 100$ is below $10^{-127}$.

### Space

Expected recursion depth is $O(\log n)$ (and $O(\log n)$ with high probability). Recursing on the smaller side makes the bound deterministic.

## Python Implementation

=== "Randomised quicksort"

    ```python
    import random


    def randomized_partition(a, lo, hi, rng):
        k = rng.randint(lo, hi)              # inclusive on both ends
        a[k], a[hi] = a[hi], a[k]
        pivot = a[hi]
        i = lo - 1
        comparisons = 0
        for j in range(lo, hi):
            comparisons += 1
            if a[j] <= pivot:
                i += 1
                a[i], a[j] = a[j], a[i]
        a[i + 1], a[hi] = a[hi], a[i + 1]
        return i + 1, comparisons


    def randomized_quicksort(a, rng=None):
        """Sort a in place; return the number of element comparisons made."""
        rng = rng or random.Random()
        total = 0
        stack = [(0, len(a) - 1)]
        while stack:
            lo, hi = stack.pop()
            if lo >= hi:
                continue
            p, c = randomized_partition(a, lo, hi, rng)
            total += c
            stack.append((lo, p - 1))
            stack.append((p + 1, hi))
        return total


    def expected_comparisons(n):
        """Exact E[X] = 2(n+1)H_n - 4n for distinct keys."""
        harmonic = sum(1 / k for k in range(1, n + 1))
        return 2 * (n + 1) * harmonic - 4 * n
    ```

=== "Introsort"

    ```python
    import math

    SMALL = 16


    def introsort(a):
        depth_limit = 2 * math.floor(math.log2(len(a))) if a else 0
        _introsort(a, 0, len(a) - 1, depth_limit)
        return a


    def _introsort(a, lo, hi, depth_limit):
        while hi - lo + 1 > SMALL:
            if depth_limit == 0:
                heapsort_range(a, lo, hi)        # quicksort is misbehaving: bail out
                return
            depth_limit -= 1
            m = median_of_three(a, lo, hi)
            a[m], a[hi] = a[hi], a[m]
            p = lomuto(a, lo, hi)
            if p - lo < hi - p:                  # recurse on smaller side
                _introsort(a, lo, p - 1, depth_limit)
                lo = p + 1
            else:
                _introsort(a, p + 1, hi, depth_limit)
                hi = p - 1
        insertion_sort_range(a, lo, hi)


    def median_of_three(a, lo, hi):
        mid = (lo + hi) // 2
        trio = sorted([(a[lo], lo), (a[mid], mid), (a[hi], hi)])
        return trio[1][1]


    def lomuto(a, lo, hi):
        pivot = a[hi]
        i = lo - 1
        for j in range(lo, hi):
            if a[j] <= pivot:
                i += 1
                a[i], a[j] = a[j], a[i]
        a[i + 1], a[hi] = a[hi], a[i + 1]
        return i + 1


    def insertion_sort_range(a, lo, hi):
        for i in range(lo + 1, hi + 1):
            key = a[i]
            j = i - 1
            while j >= lo and a[j] > key:
                a[j + 1] = a[j]
                j -= 1
            a[j + 1] = key


    def heapsort_range(a, lo, hi):
        n = hi - lo + 1

        def sift_down(i, size):
            while True:
                left, right, largest = 2 * i + 1, 2 * i + 2, i
                if left < size and a[lo + left] > a[lo + largest]:
                    largest = left
                if right < size and a[lo + right] > a[lo + largest]:
                    largest = right
                if largest == i:
                    return
                a[lo + i], a[lo + largest] = a[lo + largest], a[lo + i]
                i = largest

        for i in range(n // 2 - 1, -1, -1):
            sift_down(i, n)
        for end in range(n - 1, 0, -1):
            a[lo], a[lo + end] = a[lo + end], a[lo]
            sift_down(0, end)
    ```

**Walkthrough of the non-obvious lines**

- `rng.randint(lo, hi)` is inclusive at both ends in Python; `random.randrange(lo, hi)` would never pick `hi`, a subtle bias that excludes one candidate per call.
- Passing an explicit `random.Random` object makes experiments reproducible (seed it in tests) and avoids sharing global RNG state.
- The explicit stack in `randomized_quicksort` avoids Python's recursion limit; the comparison counter is returned so the formula can be checked empirically.
- In `introsort`, the depth budget $2\lfloor \lg n \rfloor$ is shared down each recursion path; when it reaches 0 on a path, that subarray is finished by heapsort, guaranteeing $O(n \log n)$ overall.
- With all-equal keys, Lomuto inside introsort produces maximally unbalanced splits; the depth limit catches this and heapsort completes the job (tested on 5000 equal keys).
- Both implementations were tested against `sorted()` on random arrays with duplicates, sorted, reversed and all-equal inputs.

## Edge Cases and Pitfalls

| Case / pitfall | What goes wrong | Fix |
| --- | --- | --- |
| Off-by-one in random range (`randrange(lo, hi)`) | Last element never chosen; distribution not uniform; the proof's assumption fails | Use inclusive `randint(lo, hi)` or `randrange(lo, hi + 1)` |
| Random index from the whole array instead of the subarray | Pivot may not belong to the range: wrong output or crashes | Choose in $[lo, hi]$ |
| Many duplicate keys | Random pivot does not help Lomuto: all-equal input still $\Theta(n^2)$ | 3-way partition or Hoare partition |
| Fixed, public RNG seed in a server | Attacker reproduces your pivots and crafts a bad input | Seed from the OS per process, or use introsort/pdqsort with a worst-case fallback |
| Expensive RNG call per partition | Noticeable constant-factor slowdown on small subarrays | Switch to insertion sort below a threshold; or shuffle once up front |
| Assuming "expected" means "always" | Rare slow runs in latency-critical systems | Use introsort when worst-case bounds matter |

## Common Misconceptions

- **"Randomised quicksort's worst case is $O(n \log n)$."** The worst case over coin flips is still $\Theta(n^2)$; what is $O(n \log n)$ is the **expected** time for every input, and the time with high probability.
- **"Randomisation assumes the input is random."** It assumes nothing about the input; the probability is over the algorithm's own choices.
- **"Linearity of expectation needs independence."** It does not; the indicators $X_{ij}$ are dependent and the proof is still valid.
- **"Each pair has probability $2/n$ of being compared."** Neighbours in sorted order ($j = i + 1$) are always compared; far-apart pairs rarely. The probability $2/(j-i+1)$ depends on rank distance.
- **"Random pivots fix duplicates."** No, duplicates are a partition-scheme problem, not a pivot-choice problem.
- **"Monte Carlo and Las Vegas are the same thing."** Las Vegas is always correct with random time; Monte Carlo has bounded time but may be wrong with small probability.

## Alternatives and Trade-offs

### Las Vegas vs Monte Carlo

| | Las Vegas | Monte Carlo |
| --- | --- | --- |
| Output | Always correct | Correct with high probability |
| Running time | Random; bound holds in expectation or w.h.p. | Deterministically bounded |
| Examples | Randomised quicksort, quickselect, hash tables with random hash functions | Miller-Rabin primality test, Freivalds' matrix product check, Karger's min-cut |
| Converting | Stop after $c \cdot E[T]$ steps: becomes Monte Carlo with failure probability $\le 1/c$ (Markov's inequality) | If answers can be verified cheaply, repeat until verified: becomes Las Vegas |

### Ways to protect quicksort

| Strategy | Expected time | Worst-case time | Deterministic? | Notes |
| --- | --- | --- | --- | --- |
| Fixed pivot (first/last) | $\Theta(n \log n)$ on random inputs only | $\Theta(n^2)$, common inputs | Yes | Do not use |
| Median-of-three | Better constants | $\Theta(n^2)$ on crafted inputs | Yes | Good default component |
| Random pivot / initial shuffle | $\Theta(n \log n)$ for every input | $\Theta(n^2)$ with negligible probability | No | Simple, provable |
| Median of medians pivot | $\Theta(n \log n)$ | $\Theta(n \log n)$ | Yes | Large constants |
| Introsort | $\Theta(n \log n)$ | $\Theta(n \log n)$ | Yes | Industry standard |
| pdqsort | $\Theta(n \log n)$, $O(n)$ on some patterns | $\Theta(n \log n)$ | Yes (uses deterministic shuffles) | Fast on sorted, reversed and many-duplicate inputs |

**When to use randomised quicksort:** you need a simple sort with a provable expected bound on arbitrary input, or you are writing quickselect; teaching and contest code.

**When NOT to use it:** hard real-time systems that need a deterministic worst-case bound (use introsort or heapsort); when stability is required; when reproducibility of exact execution traces matters and you cannot control seeds.

## In Practice

- **Introsort** (David Musser, 1997) starts as median-of-three quicksort, switches to heapsort if the recursion depth exceeds a limit proportional to $\lg n$, and finishes small ranges with insertion sort. libstdc++ uses it for `std::sort`, giving the $O(n \log n)$ worst case the C++ standard requires.
- **pdqsort** (Orson Peters) extends introsort: it detects badly unbalanced partitions and responds by swapping a few elements to break patterns, falls back to heapsort if this keeps happening, and handles many equal keys efficiently. Rust's `sort_unstable` (ipnsort since Rust 1.81) and Go's `sort` (since Go 1.19) descend from it.
- **Shuffle first.** Sedgewick and Wayne's *Algorithms* textbook implementation of quicksort shuffles the array once at the start, the same probabilistic guarantee with one RNG pass.
- **Security.** Any service that sorts user-controlled data (search APIs, JSON processing, spreadsheet engines) is a target for algorithmic complexity attacks. A worst-case guarantee (introsort/pdqsort) is a stronger defence than randomness with a predictable seed.
- **Randomised algorithms elsewhere.** Hash tables with random hash functions (Python randomises string hashing per process by default, controlled by `PYTHONHASHSEED`), randomised load balancing, skip lists, and sampling-based partitioners in distributed sorting (e.g. Spark's range partitioner samples keys to choose split points) all use the same "randomness defeats the adversary" idea.

## Interview and Competitive Programming

**Recognition cues**

- "Expected $O(n)$ selection", "$k$-th smallest without sorting" → randomised quickselect.
- "Your quicksort got TLE on a sorted test" → randomise the pivot (and use 3-way partition if values repeat).
- "Prove the expected number of X" → indicator random variables plus linearity of expectation (also used for expected number of fixed points of a random permutation, hiring problem, birthday problem).

**Template (indicator-variable proof)**

1. Write the quantity as a sum of indicators $X = \sum_k X_k$.
2. $E[X] = \sum_k \Pr[X_k = 1]$ (no independence needed).
3. Compute each probability with a symmetry argument ("each of the $m$ candidates is equally likely to be first").
4. Simplify the sum (often harmonic: $H_n = \Theta(\log n)$).

**Traps**

- Hack-based contests (e.g. Codeforces) let other contestants submit inputs against your code; deterministic quicksort or a fixed-seed shuffle can be broken. Seed from time or a hardware source, or use the library sort.
- In C++, `std::sort` is safe ($O(n \log n)$ worst case), but a hand-written quicksort is not.

## Using AI Assistants Critically

- LLM-generated randomised quicksort often draws the pivot with `random.randint(0, len(a) - 1)` instead of the current range, or with `randrange(lo, hi)` (excluding `hi`); check the range against the subarray bounds.
- Generated proofs frequently state $\Pr[z_i, z_j \text{ compared}] = 2/n$ or skip the "iff the first pivot from $Z_{ij}$" argument. Insist on the lemma and its justification.
- Watch for confusion of "expected" with "average-case" and claims that randomised quicksort has an $O(n \log n)$ **worst case**.
- Assistants often assert that random pivots handle duplicates; test with an all-equal array of size $10^4$ and observe the quadratic time or recursion error.
- Verify formulas empirically as on this page: average comparison counts over many seeds should match $2(n+1)H_n - 4n$ within a few percent.
- Use a fixed seed in unit tests for reproducibility, but test with many seeds and adversarial inputs (sorted, reversed, all-equal, organ-pipe) for robustness.

## Practice

**Beginner**

1. *Probability.* Input: keys $z_1 < \dots < z_{10}$. Output: probability that $z_3$ and $z_7$ are compared, and that $z_5$ and $z_6$ are compared. Difficulty: easy.
2. *Small case.* Input: $n = 4$. Output: $E[X]$ by summing $2/(j-i+1)$ over all pairs; check against $2(n+1)H_n - 4n$. Difficulty: easy.
3. *Classify.* Input: randomised quicksort, Miller-Rabin, quickselect, Freivalds' algorithm. Output: Las Vegas or Monte Carlo, with reasons. Difficulty: easy.

**Intermediate**

1. *Comparisons with the minimum.* Output: the expected number of comparisons involving $z_1$ in randomised quicksort, as a function of $n$. Difficulty: medium.
2. *Quickselect.* Prove that randomised quickselect makes an expected $O(n)$ comparisons. Difficulty: medium.
3. *Worst-case probability.* Prove that the probability that randomised quicksort makes all $\binom{n}{2}$ comparisons is $2^{n-1}/n!$. Difficulty: medium.

**Advanced**

1. *Median-of-3 random.* Choose the pivot as the median of three randomly chosen elements. Show the expected comparisons are about $\frac{12}{7} n \ln n$ (set up the recurrence and solve or simulate). Difficulty: hard.
2. *Depth tail bound.* Using the good-pivot argument and a Chernoff bound, prove the recursion depth is $O(\log n)$ with probability $1 - 1/n$. Difficulty: hard.
3. *Adversary.* Implement McIlroy-style adversarial input generation against a deterministic median-of-three quicksort and show quadratic behaviour. Difficulty: hard.

**Interview / CP**

1. *LeetCode 912 Sort an Array.* Input: up to $5 \cdot 10^4$ integers, many repeated. Output: sorted array; your quicksort must pass sorted and all-equal tests. Difficulty: medium.
2. *LeetCode 215 Kth Largest Element in an Array.* Input: $n \le 10^5$. Output: $k$-th largest in expected $O(n)$. Difficulty: medium.
3. *Random shuffle.* Input: an array. Output: a uniformly random permutation in $O(n)$ (Fisher-Yates); prove each permutation has probability $1/n!$. Difficulty: medium.

## Self-Check Questions

??? question "Q1. Why is each pair of elements compared at most once?"

    Every comparison involves the current pivot, and after the partition the pivot is in its final position and excluded from both recursive calls, so it is never compared again.

??? question "Q2. Prove that $z_i$ and $z_j$ are compared iff the first pivot chosen from $Z_{ij}$ is $z_i$ or $z_j$."

    Before any element of $Z_{ij}$ is a pivot, all of $Z_{ij}$ stays in one subarray. If the first such pivot is an endpoint, it is compared with the other endpoint. If it is a middle element, the endpoints are separated into different subarrays and never meet.

??? question "Q3. Where in the proof is linearity of expectation used, and why is independence not needed?"

    In $E[\sum X_{ij}] = \sum E[X_{ij}]$. Linearity holds for any random variables, dependent or not; the $X_{ij}$ are in fact dependent.

??? question "Q4. Show $E[X] = O(n \log n)$ from $\sum_{i<j} 2/(j-i+1)$."

    Substitute $k = j - i$: $E[X] = \sum_{i=1}^{n-1}\sum_{k=1}^{n-i}\frac{2}{k+1} < \sum_{i=1}^{n-1} 2H_n \le 2n(\ln n + 1)$.

??? question "Q5. Compare average-case analysis of deterministic quicksort with expected-time analysis of randomised quicksort."

    The first averages over random inputs and gives no guarantee for a particular (e.g. sorted) input. The second averages over the algorithm's coin flips and holds for every input. Both yield $2(n+1)H_n - 4n$ comparisons.

??? question "Q6. Is randomised quicksort Las Vegas or Monte Carlo? How could you turn it into the other type?"

    Las Vegas. Stop it after $c$ times its expected running time and output "fail": by Markov's inequality it fails with probability at most $1/c$, which is a Monte Carlo algorithm.

??? question "Q7. Why do production libraries prefer introsort or pdqsort over plain randomised quicksort?"

    They give a deterministic $O(n \log n)$ worst case (via heapsort fallback), need no RNG, handle common patterns (sorted, many duplicates) quickly, and cannot be attacked by predicting random seeds.

??? question "Q8. An all-equal array of size $10^5$ makes your randomised Lomuto quicksort crash. Why, and how do you fix it?"

    Every element is $\le$ the pivot, so each split is $n-1$ / $0$ regardless of which element is chosen: $\Theta(n^2)$ time and $\Theta(n)$ depth. Use 3-way partition (or Hoare partition) and recurse on the smaller side.

## Complexity Summary

| Measure | Randomised quicksort |
| --- | --- |
| Expected comparisons (every input, distinct keys) | $2(n+1)H_n - 4n \approx 1.39\, n\lg n$ |
| Expected time | $\Theta(n \log n)$ |
| Time with high probability | $O(n \log n)$ |
| Worst-case time (over coin flips) | $\Theta(n^2)$, probability $2^{n-1}/n!$ of the maximal run |
| Expected stack depth | $O(\log n)$; $O(\log n)$ worst case with smaller-side recursion |
| Introsort worst case | $\Theta(n \log n)$ time, $O(\log n)$ stack |

## Key Takeaways

- Random pivots make quicksort's performance independent of the input order; no input is bad, only coin flips can be unlucky.
- Expected comparisons for every input: $E[X] = \sum_{i<j} \frac{2}{j-i+1} = 2(n+1)H_n - 4n = \Theta(n \log n)$.
- The proof pattern (indicators, linearity, symmetry, harmonic sum) is reusable for many randomised algorithms.
- "Expected over coin flips" is a guarantee; "average over inputs" is an assumption about the data.
- Randomised quicksort is Las Vegas: always correct, random time; the quadratic run has probability $2^{n-1}/n!$.
- Randomisation does not fix duplicates; combine it with 3-way partitioning.
- Industry sorts use introsort/pdqsort to get quicksort's speed with a deterministic $O(n \log n)$ worst case.
