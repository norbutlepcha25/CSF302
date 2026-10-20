# Probability for Algorithm Analysis

!!! abstract "At a glance"

    - **Problem space:** predicting the *typical* cost of an algorithm when its input is random or when the algorithm itself makes random choices.
    - **Key ideas:** random variables and expectation; **linearity of expectation** (needs no independence); **indicator random variables** turn "how many times does X happen?" into a sum of probabilities.
    - **Signature results:** hiring problem $E[\text{hires}] = H_n \approx \ln n$; expected inversions of a random permutation $n(n-1)/4$; geometric distribution $E[\text{trials}] = 1/p$; birthday bound — collisions appear after about $\sqrt{m}$ keys in $m$ buckets.
    - **Where it is used:** randomized quicksort ([Unit 5.4](../unit5/topic4.md)), hashing and load balancing, Bloom filters, Miller–Rabin primality testing, Monte Carlo simulation, A/B testing, ML (stochastic gradient descent).

## Motivation and Problem Context

Worst-case analysis is safe but sometimes misleading. Quicksort is $\Theta(n^2)$ in the worst case, yet it is one of the fastest sorts in practice. A hash table can degrade to $\Theta(n)$ per lookup, yet billions of lookups per second run in expected $O(1)$. To explain — and to *engineer* — this behaviour we need probability.

Two distinct situations appear throughout the course:

1. **Probabilistic analysis of a deterministic algorithm.** We assume a distribution over inputs (e.g. "every ordering of the input is equally likely") and compute the *average-case* cost. Its weakness: real inputs may not follow the assumed distribution (sorted data is common).
2. **Analysis of a randomized algorithm.** The algorithm flips coins (random pivot, random hash function). Now the expectation is over the algorithm's own random choices and holds **for every input** — an adversary cannot force the bad case by choosing the input.

!!! warning "Important: average-case vs expected running time"

    *Average-case* running time averages over a **distribution of inputs** for a deterministic algorithm. *Expected* running time of a randomized algorithm averages over the **algorithm's coin flips** for a fixed, worst-case input. Randomized quicksort has expected $O(n \log n)$ time on **every** input; deterministic quicksort only has average-case $O(n \log n)$ if inputs are random. Do not use the two terms interchangeably in exams.

## Problem Formulation

Given an algorithm whose cost $T$ depends on random choices (of the input or of the algorithm):

- **Input:** the algorithm, the input size $n$, and a precise probability model (what is random and how it is distributed).
- **Output:** $E[T]$ as a function of $n$ (and sometimes $\Pr[T > t]$ — a tail bound).
- **Assumptions:** must be stated explicitly: e.g. "candidates arrive in uniformly random order", "each key hashes independently and uniformly to one of $m$ buckets" (simple uniform hashing), "the pivot is chosen uniformly at random".

## Intuition

Most costs are **counts**: number of comparisons, number of hires, number of collisions. Write the count as a sum of 0/1 variables, one per "thing that might happen". The expected count is then just the **sum of the probabilities** of those things, no matter how they depend on each other. Mental model: *don't try to find the distribution of the total — break it into yes/no events and add their probabilities.*

## Definitions

| Term | Definition | Example |
| --- | --- | --- |
| Sample space $\Omega$ | Set of all possible outcomes | Orderings of $n$ candidates: $\lvert\Omega\rvert = n!$ |
| Event $A \subseteq \Omega$ | A set of outcomes | "The best candidate comes first" |
| Probability (uniform, finite) | $\Pr[A] = \lvert A \rvert / \lvert \Omega \rvert$ | $\Pr[\text{best first}] = (n-1)!/n! = 1/n$ |
| Axioms | $\Pr[A] \ge 0$, $\Pr[\Omega] = 1$, additivity for disjoint events | |
| Conditional probability | $\Pr[A \mid B] = \Pr[A \cap B]/\Pr[B]$ for $\Pr[B] > 0$ | |
| Independence | $\Pr[A \cap B] = \Pr[A]\Pr[B]$ | Two fair coin flips |
| Random variable $X$ | A function $\Omega \to \mathbb{R}$ | Number of hires, comparisons, collisions |
| Expectation | $E[X] = \sum_x x \Pr[X = x]$ | Fair die: $E = 3.5$ |
| Variance | $\operatorname{Var}[X] = E[X^2] - E[X]^2$ | Spread around the mean |
| Indicator $I\{A\}$ | $1$ if $A$ occurs, else $0$ | $I\{\text{candidate } i \text{ is hired}\}$ |

Counting the sizes of $\Omega$ and $A$ is exactly the combinatorics of [Topic 1.2](topic2.md); this topic builds on it.

## Key Results

### Basic rules

| Rule | Statement | Note |
| --- | --- | --- |
| Complement | $\Pr[\overline A] = 1 - \Pr[A]$ | "At least one" problems |
| Inclusion–exclusion | $\Pr[A \cup B] = \Pr[A] + \Pr[B] - \Pr[A \cap B]$ | Generalizes as in [Topic 1.2](topic2.md) |
| Union bound | $\Pr[A_1 \cup \dots \cup A_k] \le \sum_i \Pr[A_i]$ | Holds always; used to bound failure probabilities |
| Product rule (independent) | $\Pr[A \cap B] = \Pr[A]\Pr[B]$ | **Only** under independence |
| Chain rule | $\Pr[A \cap B] = \Pr[A]\Pr[B \mid A]$ | Always holds |
| Bayes | $\Pr[A \mid B] = \Pr[B \mid A]\Pr[A]/\Pr[B]$ | Spam filters, diagnostics |

### Linearity of expectation

**Theorem.** For any random variables $X, Y$ (on the same sample space) and constants $a, b$:

$$
E[aX + bY] = aE[X] + bE[Y],
$$

**whether or not $X$ and $Y$ are independent.**

*Proof (finite $\Omega$).* $E[aX + bY] = \sum_{\omega} (aX(\omega) + bY(\omega))\Pr[\omega] = a\sum_\omega X(\omega)\Pr[\omega] + b\sum_\omega Y(\omega)\Pr[\omega] = aE[X] + bE[Y]$. The proof never uses independence. $\square$

By induction it extends to any finite sum: $E\big[\sum_i X_i\big] = \sum_i E[X_i]$.

By contrast, $E[XY] = E[X]E[Y]$ **requires** independence, and $E[f(X)] \ne f(E[X])$ for non-linear $f$ in general (e.g. $E[X^2] \ge E[X]^2$, with equality only when $X$ is constant).

### Indicator random variables

**Lemma.** For an event $A$, $E[I\{A\}] = \Pr[A]$.
*Proof.* $E[I\{A\}] = 1 \cdot \Pr[A] + 0 \cdot \Pr[\overline A] = \Pr[A]$. $\square$

**Combined with linearity:** if $X = \sum_{i} X_i$ where $X_i = I\{A_i\}$, then

$$
E[X] = \sum_i \Pr[A_i].
$$

This is the single most useful technique in the analysis of randomized algorithms.

### Standard distributions

| Distribution | Models | $\Pr[X = k]$ | $E[X]$ | $\operatorname{Var}[X]$ |
| --- | --- | --- | --- | --- |
| Bernoulli($p$) | One trial succeeds or not | $p$ for $k=1$, $1-p$ for $k = 0$ | $p$ | $p(1-p)$ |
| Binomial($n, p$) | Successes in $n$ independent trials | $\binom{n}{k}p^k(1-p)^{n-k}$ | $np$ | $np(1-p)$ |
| Geometric($p$) | Trials up to and including the first success | $(1-p)^{k-1}p$, $k \ge 1$ | $1/p$ | $(1-p)/p^2$ |
| Uniform on $\{1..n\}$ | Random index, random pivot | $1/n$ | $(n+1)/2$ | $(n^2 - 1)/12$ |

*Binomial mean via linearity:* $X = \sum_{i=1}^n X_i$ with $X_i$ Bernoulli($p$), so $E[X] = np$ — no need to evaluate the sum over $k$.

*Geometric mean.* Condition on the first trial: with probability $p$ we stop after 1 trial; otherwise we have used 1 trial and the process restarts. So $E[X] = 1 + (1-p)E[X]$, giving $E[X] = 1/p$.

**Consequence for algorithms:** if each attempt of a "retry until success" loop succeeds with probability $p$ independently, the expected number of attempts is $1/p$. Examples: generating a random prime by sampling (about $\ln N / 2$ odd samples), rejection sampling, randomized selection of a "good" pivot (probability $1/2$ that a random pivot lies in the middle half, so 2 tries on average).

### Harmonic numbers

$H_n = \sum_{k=1}^n \frac{1}{k}$ appears whenever "the $k$-th item matters with probability $1/k$". By comparing with $\int \frac{dx}{x}$:

$$
\ln(n+1) \le H_n \le \ln n + 1, \qquad H_n = \ln n + \gamma + O(1/n),\quad \gamma \approx 0.5772 .
$$

### Markov's inequality (tail bound)

For $X \ge 0$ and $t > 0$: $\Pr[X \ge t] \le E[X]/t$. For example, if an algorithm's expected time is $T$, it runs longer than $10T$ with probability at most $1/10$. Restarting it after $2T$ steps and repeating turns a Las Vegas expected-time algorithm into one that rarely runs long.

## Method: The Indicator Recipe

1. **State the probability model** precisely (what is random, what is uniform, what is independent).
2. **Identify the cost** $X$ as a count of events.
3. **Decompose** $X = \sum_i X_i$ with $X_i = I\{A_i\}$ — one indicator per item, pair, or position.
4. **Compute** $\Pr[A_i]$ for a single generic $i$, usually by a symmetry argument.
5. **Sum** using linearity: $E[X] = \sum_i \Pr[A_i]$; simplify with $H_n$, $\binom{n}{2}$, geometric series.
6. **Sanity-check** with tiny $n$ by brute force over all outcomes, or by simulation.

## Worked Examples

!!! example "Example 1 (basic): expected sum of dice"

    Roll $n$ fair dice. Let $X_i$ be the value of die $i$, so $E[X_i] = (1+2+\dots+6)/6 = 3.5$. By linearity, $E[\text{sum}] = 3.5n$. Computing the distribution of the sum would require convolutions; linearity skips that entirely.

!!! example "Example 2 (basic): expected fixed points of a random permutation"

    Shuffle $n$ labelled cards. How many cards are expected to stay in their original position? Let $X_i = I\{\text{card } i \text{ stays}\}$; by symmetry $\Pr[X_i = 1] = 1/n$. So $E[X] = n \cdot \frac{1}{n} = 1$ for **every** $n$. The events are dependent (if $n-1$ cards stay, the last must too), but linearity does not care. Compare with [Topic 1.2](topic2.md): the probability of **zero** fixed points is about $1/e$.

### The hiring problem

!!! example "Example 3 (intermediate): the hiring problem"

    An agency sends $n$ candidates one per day. You interview each (cost $c_i$, small) and **hire** them if they are better than everyone seen so far (cost $c_h$, large — firing and hiring). What is the expected hiring cost if candidates arrive in uniformly random order?

    ```text
    HIRE-ASSISTANT(candidates[1..n])
        best <- a dummy candidate worse than everyone
        hires <- 0
        for i <- 1 to n
            interview candidate i
            if candidate i is better than best
                best <- candidate i
                hire candidate i
                hires <- hires + 1
        return hires
    ```

    - **Worst case:** candidates arrive in increasing quality; all $n$ are hired, cost $\Theta(n\,c_h)$.
    - **Indicator decomposition:** $X = \sum_{i=1}^n X_i$, $X_i = I\{\text{candidate } i \text{ is hired}\}$.
    - **Probability:** candidate $i$ is hired iff it is the best among the first $i$. In a uniformly random order each of the first $i$ is equally likely to be the best, so $\Pr[X_i = 1] = 1/i$.
    - **Sum:** $E[X] = \sum_{i=1}^n \frac{1}{i} = H_n = \ln n + O(1)$.

    Expected hiring cost: $O(c_h \ln n)$ versus $O(c_h n)$ in the worst case. With $n = 100$ candidates, $H_{100} \approx 5.19$ hires on average instead of 100.

    **Making it robust (randomized version):** the analysis assumed random arrival order. If the agency might send candidates in a bad order, **shuffle the list first** (e.g. Fisher–Yates). The expectation $H_n$ then holds for every input — this is the step from probabilistic analysis to a randomized algorithm, exactly the idea behind randomized quicksort.

    Trace on one ordering of qualities $[3, 1, 4, 2, 5, 9, 7, 6]$:

    | $i$ | quality | best before | hired? | hires |
    | --- | --- | --- | --- | --- |
    | 1 | 3 | $-\infty$ | yes | 1 |
    | 2 | 1 | 3 | no | 1 |
    | 3 | 4 | 3 | yes | 2 |
    | 4 | 2 | 4 | no | 2 |
    | 5 | 5 | 4 | yes | 3 |
    | 6 | 9 | 5 | yes | 4 |
    | 7 | 7 | 9 | no | 4 |
    | 8 | 6 | 9 | no | 4 |

    The hires are exactly the **left-to-right maxima** ("records") of the sequence.

!!! example "Example 4 (intermediate): expected inversions and insertion sort"

    An inversion is a pair $i < j$ with $a_i > a_j$. For a uniformly random permutation of distinct values, let $X_{ij} = I\{a_i > a_j\}$. By symmetry $\Pr[a_i > a_j] = 1/2$. Hence

    $$
    E[\text{inversions}] = \binom{n}{2} \cdot \frac12 = \frac{n(n-1)}{4}.
    $$

    Insertion sort performs one swap per inversion, so its **average-case** time is $\Theta(n^2)$ — the same order as its worst case. Inversions are studied algorithmically in [Unit 5.7](../unit5/topic7.md).

!!! example "Example 5 (advanced): hashing, collisions and the birthday bound"

    Insert $n$ keys into $m$ buckets, each key independently uniform (simple uniform hashing).

    - **Expected chain length** of a given bucket: $X = \sum_{k} I\{\text{key } k \text{ lands there}\}$, so $E[X] = n/m = \alpha$, the load factor. An unsuccessful search in chaining costs expected $\Theta(1 + \alpha)$.
    - **Expected colliding pairs:** $E\big[\sum_{k < l} I\{h(k) = h(l)\}\big] = \binom{n}{2}\frac{1}{m}$. With $n = 100$ keys and $m = 1000$ buckets this is $4.95$ — collisions are routine, not exceptional.
    - **Probability of at least one collision** (exact): $1 - \prod_{i=0}^{n-1}\frac{m - i}{m}$. Using $1 - x \le e^{-x}$, this is at least $1 - e^{-n(n-1)/(2m)}$, which passes $1/2$ once $n \approx \sqrt{2m \ln 2} \approx 1.18\sqrt m$.
    - **Birthday paradox:** with $m = 365$, the exact probability is $0.507$ for $n = 23$ people (and $0.476$ for $n = 22$).

    Engineering consequence: a 32-bit hash or checksum ($m = 2^{32}$) is expected to see a collision after only about $2^{16} \approx 65{,}000$ items; content-addressed storage and deduplication therefore use hashes of 128 bits or more.

!!! example "Example 6 (advanced): coupon collector"

    How many uniformly random draws from $n$ types until every type is seen? After $i$ types have been seen, a new type appears with probability $(n - i)/n$, so the wait is geometric with mean $n/(n-i)$. By linearity:

    $$
    E[\text{draws}] = \sum_{i=0}^{n-1}\frac{n}{n-i} = n H_n = \Theta(n \log n).
    $$

    Uses: how many random probes to hit every server; why random testing needs $\Theta(n \log n)$ trials to cover $n$ equally likely cases; expected number of keys before every bucket in a hash table is non-empty.

### Preview: randomized quicksort

The same recipe drives the analysis in [Unit 5.4](../unit5/topic4.md). Let $z_1 < z_2 < \dots < z_n$ be the sorted elements and $X_{ij} = I\{z_i \text{ is compared with } z_j\}$. Two elements are compared iff one of them is the **first pivot chosen** from $\{z_i, \dots, z_j\}$, which happens with probability $\frac{2}{j - i + 1}$. Summing over all pairs gives $E[\text{comparisons}] = \sum_{i<j}\frac{2}{j-i+1} = O(n \log n)$ (exactly $2(n+1)H_n - 4n$). The full derivation belongs to Unit 5.4; what matters here is that **no independence was needed** — only indicators and linearity.

## Python Implementation

```python
import itertools
import math
import random
from fractions import Fraction


def hire_assistant(candidates):
    """Number of hires when we hire every candidate better than all before."""
    best = float("-inf")
    hires = 0
    for quality in candidates:
        if quality > best:
            best = quality
            hires += 1
    return hires


def harmonic(n):
    return sum(Fraction(1, i) for i in range(1, n + 1))


def expected_hires_exact(n):
    """Average number of hires over all n! orderings (brute force, small n)."""
    total = sum(hire_assistant(p) for p in itertools.permutations(range(n)))
    return Fraction(total, math.factorial(n))


def collision_probability(n, m):
    """P(at least two of n uniformly random keys share one of m buckets)."""
    if n > m:
        return 1.0                       # pigeonhole
    p_distinct = 1.0
    for i in range(n):
        p_distinct *= (m - i) / m
    return 1.0 - p_distinct


def simulate(trial, runs=100_000, seed=1):
    """Monte Carlo estimate of E[trial(rng)]."""
    rng = random.Random(seed)
    return sum(trial(rng) for _ in range(runs)) / runs


def flips_until_head(rng, p=0.5):
    flips = 1
    while rng.random() >= p:             # failure with probability 1 - p
        flips += 1
    return flips


assert all(expected_hires_exact(n) == harmonic(n) for n in range(1, 8))
print(round(collision_probability(23, 365), 3))                     # 0.507
print(round(simulate(lambda rng: flips_until_head(rng, 0.2)), 2))   # close to 5
```

**Walkthrough of the non-obvious lines**

- `expected_hires_exact` averages over all $n!$ orderings with exact `Fraction` arithmetic, so the assertion `== harmonic(n)` checks the theorem exactly for small $n$ rather than approximately.
- `collision_probability` multiplies the probabilities that the $i$-th key avoids the $i$ occupied buckets; it returns 1 immediately when $n > m$ (pigeonhole).
- `simulate` takes a seeded `random.Random` so experiments are reproducible; Monte Carlo estimates converge at rate $O(1/\sqrt{\text{runs}})$, so compare with tolerances, not equality.
- The code was also used to confirm $E[\text{inversions}] = n(n-1)/4$, $E[\text{fixed points}] = 1$, the colliding-pairs formula, and the coupon-collector mean $nH_n$.

## Edge Cases and Pitfalls

| Case / pitfall | What goes wrong | Fix |
| --- | --- | --- |
| Unstated probability model | "Expected time" is meaningless without saying what is random | Always write the assumption (uniform order, uniform hashing, random pivot) |
| Multiplying probabilities of dependent events | $\Pr[A \cap B] \ne \Pr[A]\Pr[B]$; answer wrong | Use the chain rule $\Pr[A]\Pr[B \mid A]$ |
| Assuming $E[XY] = E[X]E[Y]$ | False without independence | Use only linearity, or prove independence |
| Assuming $E[1/X] = 1/E[X]$ or $E[X^2] = E[X]^2$ | Jensen: non-linear functions do not commute with $E$ | Compute the distribution, or bound with Jensen/Markov |
| Ties in the hiring problem | "Better than" with equal qualities changes the count | State distinctness (random permutation of distinct values) |
| Floating-point product of many probabilities | Underflow toward 0 for long products | Sum logarithms, or use `math.prod` with care |
| Non-seeded simulations in tests | Flaky tests | Seed the RNG; assert with tolerances |
| Using `random` for security | Predictable outputs (Mersenne Twister) | Use the `secrets` module for tokens and keys |
| Modular probabilities in CP ($P/Q \bmod p$) | Floating-point answer rejected | Output $P \cdot Q^{-1} \bmod p$ using a modular inverse ([Topic 1.1](topic1.md)) |

## Common Misconceptions

| Wrong belief | Correct mental model |
| --- | --- |
| "Linearity of expectation needs independent variables." | It holds for **any** random variables. Independence is needed for products and variances of sums. |
| "Expected $O(n \log n)$ means it always runs in $O(n \log n)$." | It is an average over coin flips; individual runs can be slower, though for randomized quicksort large deviations are very unlikely. |
| "Average-case and expected running time are the same thing." | Average-case: random **input**, fixed algorithm. Expected: random **algorithm**, any input. |
| "If an event has probability $1/2$, two tries guarantee it." | Two independent tries succeed with probability $3/4$; the **expected** number of tries is 2. |
| "Collisions are rare until the table is nearly full." | Birthday bound: collisions are likely after about $\sqrt m$ keys. |
| "A random-looking input distribution justifies average-case analysis." | Real inputs are often sorted, adversarial or skewed; randomize inside the algorithm instead. |

## Alternatives and Trade-offs

| Analysis type | Averages over | Guarantee | Typical example | Weakness |
| --- | --- | --- | --- | --- |
| Worst case | Nothing | Bound for every input and run | Merge sort $O(n \log n)$ | Can be pessimistic |
| Average case | Assumed input distribution | Mean over inputs | Deterministic quicksort on random data | Breaks if inputs are not random |
| Expected (randomized) | Algorithm's coin flips | Mean for **every** input | Randomized quicksort, universal hashing | Individual runs can be slow |
| High probability | Coin flips | Bound holds with probability $\ge 1 - 1/n^c$ | Skip lists, randomized quicksort tail bounds | Harder proofs |
| Amortized | Sequence of operations | Total over any sequence | Dynamic array append | Single operation may be slow |

**Randomized algorithm types.** *Las Vegas*: always correct, running time random (randomized quicksort). *Monte Carlo*: running time bounded, answer correct with high probability (Miller–Rabin: a composite passes $k$ random rounds with probability at most $4^{-k}$). Use Las Vegas when wrong answers are unacceptable; Monte Carlo when a tiny, controllable error probability buys a large speedup.

**When NOT to rely on expected bounds:** hard real-time systems (avionics, audio callbacks) need worst-case guarantees; security-sensitive data structures exposed to adversaries need randomization the adversary cannot predict, not just "inputs are probably random".

## In Practice

- **Hash flooding defence.** Python randomizes string hashing per process (since 3.3; controlled by `PYTHONHASHSEED`) and uses SipHash for `str`/`bytes` (PEP 456). Rust's default `HashMap` hasher is also a keyed SipHash variant. The goal: an attacker cannot precompute keys that all collide, so the expected-$O(1)$ analysis applies.
- **Randomization in sorting and selection.** Pivot randomization (or pseudo-random shuffling of candidate pivots) is used to defeat adversarial inputs; introsort-style hybrids additionally fall back to heapsort to cap the worst case.
- **Probabilistic data structures.** Bloom filters (false-positive rate $\approx (1 - e^{-kn/m})^k$), HyperLogLog cardinality estimation, Count-Min sketch and skip lists are all analyzed with indicators, linearity and tail bounds. They are used in databases (e.g. LSM-tree storage engines use Bloom filters to skip disk reads), networking and analytics.
- **Load balancing.** Sending each request to a random server gives a maximum load of $\Theta(\log n / \log\log n)$ for $n$ requests on $n$ servers; sampling **two** servers and choosing the less loaded ("power of two choices") reduces it to $\Theta(\log\log n)$.
- **Testing and simulation.** Monte Carlo estimates converge like $1/\sqrt{N}$: halving the error needs four times the samples. Property-based testing (`hypothesis`) draws random inputs to search for counterexamples.
- **Machine learning.** Stochastic gradient descent uses an unbiased random estimate of the gradient — linearity of expectation over the minibatch is what makes it unbiased.

## Interview and Competitive Programming

**Recognition cues**

| If you see... | Think... |
| --- | --- |
| "Expected number of ..." | Indicators + linearity; avoid computing the full distribution |
| "Expected number of steps until ..." | Geometric distribution or expected-value DP: $E[s] = 1 + \sum_{t} \Pr[s \to t] E[t]$ |
| "Random permutation" | Symmetry: each position/element/pair is equally likely |
| "Output the probability as $P \cdot Q^{-1} \bmod 998244353$" | Do all arithmetic modulo $p$; replace division by inverses |
| "Shuffle uniformly" | Fisher–Yates; naive "swap with any index" shuffles are biased |
| "Pick a random element from a stream of unknown length" | Reservoir sampling: keep item $i$ with probability $1/i$ (same $1/i$ as the hiring problem) |

**Expected-value DP template**

```text
E[terminal] <- 0
for states s in reverse topological order
    E[s] <- cost(s) + sum over transitions s -> t of Pr[s -> t] * E[t]
```

If a state can transition to itself with probability $q$, solve $E[s] = c + qE[s] + \dots$ algebraically: $E[s] = (c + \dots)/(1 - q)$.

**Common traps:** using floating-point when a modular answer is required; summing dependent probabilities with the product rule; forgetting that "uniform random pair" may be ordered or unordered.

## Using AI Assistants Critically

- LLMs often "prove" results by multiplying probabilities of dependent events; check every product for an independence justification.
- They sometimes conflate average-case and expected running time, or claim randomized quicksort is "$O(n \log n)$ guaranteed". Ask what is random and what the guarantee is over.
- Generated shuffles are frequently biased (`j = random.randint(0, n - 1)` for every `i`). A Fisher–Yates loop must pick `j` in `[i, n - 1]` (or `[0, i]` when iterating downward). Verify with a chi-square-style frequency count over all $n!$ outcomes for $n = 3$.
- Verify any claimed expectation two ways: exact enumeration for tiny $n$ (with `Fraction`) and a seeded Monte Carlo simulation for moderate $n$.
- Watch for code using `random` for tokens or keys; security needs `secrets`.
- For CP-style probability answers, check that generated code applies modular inverses rather than floating-point division.

## Practice

**Beginner**

1. *Expected heads.* Input: $n \le 10^6$ biased coins with probabilities $p_i$. Output: expected number of heads. Difficulty: easy.
2. *Dice until six.* Input: none. Output: expected number of rolls of a fair die until the first 6, with a derivation. Difficulty: easy.
3. *Same bucket.* Input: $n$ keys, $m$ buckets, uniform hashing. Output: probability that two specific keys collide, and expected number of colliding pairs. Difficulty: easy.

**Intermediate**

1. *Records.* Input: $n \le 10^6$. Output: expected number of left-to-right maxima **and** left-to-right minima of a random permutation, as an exact fraction modulo $998\,244\,353$. Difficulty: medium.
2. *Expected empty buckets.* Input: $n$ keys and $m$ buckets ($n, m \le 10^9$). Output: expected number of empty buckets (a formula and its limit when $n = m$). Difficulty: medium.
3. *Biased shuffle detector.* Input: a shuffle procedure as code. Output: decide whether all $n!$ permutations are equally likely for $n = 3$, by counting. Difficulty: medium.

**Advanced**

1. *Hiring with a budget.* Input: $n$ candidates in random order; you may hire at most once and must decide immediately. Output: a strategy maximizing the probability of hiring the best (the secretary problem) and that probability's limit. Difficulty: hard.
2. *Random walk to the end.* Input: positions $0..n$ ($n \le 10^5$); from $i$ you move to $i+1$ with probability $p$ and stay with probability $1-p$, with cost 1 per step. Output: expected number of steps to reach $n$. Difficulty: medium–hard.
3. *Comparison count.* Input: $n \le 10^6$. Output: the exact expected number of comparisons of randomized quicksort, $2(n+1)H_n - 4n$, modulo $998\,244\,353$. Difficulty: hard.

**Interview / CP**

1. *Linked List Random Node* (LeetCode 382). Input: a linked list of unknown length. Output: a uniformly random node using $O(1)$ extra space. Difficulty: medium.
2. *Shuffle an Array* (LeetCode 384). Input: an array. Output: an unbiased random permutation in $O(n)$. Difficulty: medium.
3. *Expected dice game.* Input: a board with $n \le 10^5$ cells and ladders; each turn roll a fair die. Output: expected number of turns to finish. Difficulty: hard.

## Self-Check Questions

??? question "Q1. State linearity of expectation. Why is it so useful when analyzing algorithms?"

    $E[\sum_i X_i] = \sum_i E[X_i]$ for any random variables, independent or not. Algorithm costs are sums of many dependent events (comparisons, hires, collisions); linearity lets us add their individual probabilities without understanding their joint distribution.

??? question "Q2. In the hiring problem, why is $\Pr[\text{candidate } i \text{ is hired}] = 1/i$, and what assumption is needed?"

    Candidate $i$ is hired iff it is the best of the first $i$ candidates. If the order is a uniformly random permutation of distinct qualities, each of those $i$ candidates is equally likely to be the best, so the probability is $1/i$. Without the random-order assumption (or an explicit shuffle), the probability can be anything.

??? question "Q3. Why is the expected number of hires $\Theta(\log n)$ and not $\Theta(n)$?"

    $E[\text{hires}] = H_n$, and $\ln(n+1) \le H_n \le \ln n + 1$. Later candidates are increasingly unlikely to beat everyone before them.

??? question "Q4. Compute the expected number of inversions of a random permutation. What does it imply about insertion sort?"

    Each of the $\binom{n}{2}$ pairs is inverted with probability $1/2$, so $E = n(n-1)/4$. Insertion sort does one shift per inversion, so its average case is $\Theta(n^2)$, not better than its worst case in order of growth.

??? question "Q5. Explain the difference between average-case analysis of quicksort and the expected running time of randomized quicksort."

    Average-case assumes the input order is uniformly random and averages over inputs for a deterministic pivot rule; sorted or adversarial inputs still give $\Theta(n^2)$. Randomized quicksort picks pivots at random, so for **every fixed input** the expected time over its own coin flips is $O(n \log n)$.

??? question "Q6. A system assigns 64-bit random IDs. Roughly how many IDs can be generated before a collision becomes likely? What if IDs were 32-bit?"

    Birthday bound: collisions become likely after about $\sqrt{m}$ IDs. For $m = 2^{64}$ that is about $2^{32} \approx 4.3 \times 10^9$ IDs; for $m = 2^{32}$ only about $2^{16} \approx 65{,}536$. This is why UUIDv4 uses 122 random bits.

??? question "Q7. Each attempt of a randomized algorithm succeeds independently with probability $1/4$. What is the expected number of attempts, and what is the probability that more than 10 attempts are needed?"

    Geometric: $E = 1/p = 4$. More than 10 attempts means 10 failures: $(3/4)^{10} \approx 0.056$.

??? question "Q8. Is $E[X^2] = (E[X])^2$ for the number of heads $X$ in $n$ fair coin flips? Justify."

    No. $E[X^2] = \operatorname{Var}[X] + E[X]^2 = n/4 + n^2/4$, which exceeds $(n/2)^2$ by the variance $n/4$. Expectation is linear, but squaring is not.

## Complexity Summary

| Quantity | Model | Expected value |
| --- | --- | --- |
| Hires in the hiring problem | Random order | $H_n = \ln n + O(1)$ |
| Fixed points of a permutation | Uniform permutation | $1$ |
| Inversions | Uniform permutation | $n(n-1)/4$ |
| Trials until first success | Independent, probability $p$ | $1/p$ |
| Chain length / unsuccessful search in chaining | Simple uniform hashing | $\alpha = n/m$; search $\Theta(1 + \alpha)$ |
| Colliding pairs | $n$ keys, $m$ buckets | $\binom{n}{2}/m$ |
| Keys until first likely collision | $m$ buckets | $\approx 1.18\sqrt{m}$ for probability $1/2$ |
| Draws to see all $n$ types | Coupon collector | $n H_n = \Theta(n \log n)$ |
| Randomized quicksort comparisons | Uniform random pivots | $2(n+1)H_n - 4n = O(n \log n)$ |

## Key Takeaways

- Always state the probability model: what is random, with what distribution, and what is independent.
- Linearity of expectation holds without independence; combined with indicators, $E[\text{count}] = \sum \Pr[\text{event}]$.
- The hiring problem shows the pattern: worst case $n$ hires, expected $H_n \approx \ln n$; shuffling first makes the bound hold for every input.
- Average-case analysis averages over inputs; expected running time of a randomized algorithm averages over coin flips and is robust to adversarial inputs.
- Geometric waits have mean $1/p$; harmonic sums $H_n \approx \ln n$ appear whenever item $k$ matters with probability $1/k$.
- Collisions arrive early: about $\sqrt m$ keys suffice in $m$ buckets, so hash sizes and table designs must plan for them.
- These tools are the foundation for randomized quicksort, hashing and probabilistic data structures later in the course.
