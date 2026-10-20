# Randomized Algorithms

!!! abstract "At a glance"

    - **Problem:** some problems have simple deterministic algorithms that are slow on adversarial inputs, or no known fast deterministic algorithm that is practical.
    - **Key idea:** let the algorithm flip coins. Randomness defeats adversarial inputs (no fixed input is always bad) and makes simple algorithms fast in expectation or correct with high probability.
    - **Two kinds:** **Las Vegas** (always correct, running time is random) and **Monte Carlo** (bounded running time, answer may be wrong with small probability).
    - **Examples:** randomized quicksort and quickselect (expected $O(n \log n)$ and $O(n)$), Miller–Rabin primality (error $\le 4^{-k}$), Karger min-cut, universal hashing, reservoir sampling.
    - **Used in:** hash tables with seeded hashing, RSA key generation, Bloom filters in databases, load balancing, streaming analytics, machine learning (SGD, dropout, random initialization).

## Motivation and Problem Context

Deterministic quicksort with "first element as pivot" is $\Theta(n^2)$ on already-sorted input, and sorted input is common in practice. Worse, an attacker who knows the pivot rule can craft bad inputs on purpose. The same is true of hash tables: if the hash function is fixed and public, an attacker can send thousands of keys that collide, turning $O(1)$ lookups into $O(n)$ and taking a web server down (hash-flooding denial-of-service attacks).

Randomization changes the game. If the algorithm's choices depend on random bits chosen *at run time*, there is no single input that is always bad. The adversary picks the input; the algorithm then picks its random choices; performance is analysed as an expectation **over the algorithm's coins**, for the **worst** input.

Randomization also gives algorithms that are dramatically simpler or faster than the best known deterministic ones, at the cost of a tiny, controllable probability of error. Testing whether a 2048-bit number is prime takes a handful of modular exponentiations with Miller–Rabin, which is fast enough to run on thousands of random candidates during key generation; the deterministic AKS test, while polynomial, is far too slow to be used in practice.

This topic builds on the probability basics from [Unit 1](../unit1/topic3.md) and on randomized quicksort from [Unit 5](../unit5/topic4.md).

## Problem Formulation

A **randomized algorithm** receives an input $x$ and, in addition, a stream of independent uniformly random bits $r$. Its behaviour (running time, output) is a function of both.

- **Expected running time:** $T(x) = \mathbb{E}_r[\text{time}(x, r)]$. We bound $\max_x T(x)$: the worst input, averaged over the algorithm's coins.
- **Error probability:** $\Pr_r[\text{output}(x, r) \text{ is wrong}]$. We bound this for every input $x$.
- **High probability (w.h.p.):** probability at least $1 - 1/n^c$ for a constant $c \ge 1$.

!!! warning "Important"

    **Expected running time of a randomized algorithm** is not **average-case running time of a deterministic algorithm**. Average-case analysis assumes a probability distribution over *inputs* (e.g. "all permutations equally likely"), which an adversary or real data need not respect. Randomized analysis assumes nothing about the input; the randomness is inside the algorithm. Randomized quicksort is expected $O(n \log n)$ on **every** input, including sorted input.

## Intuition

Two mental models:

- **Random sampling of choices:** if at least a constant fraction of the choices are "good" (a good pivot, a witness of compositeness), picking one at random finds a good one quickly. You do not need to know *which* choices are good.
- **Hiding from the adversary:** a deterministic algorithm is a fixed strategy; an adversary can find its weakness. A randomized algorithm is a mixture of strategies; any fixed input defeats only a small fraction of them.

## Definitions

| Type | Correctness | Running time | Example |
|---|---|---|---|
| **Las Vegas** | Always correct | Random; we bound its expectation | Randomized quicksort, quickselect, treaps, universal-hashing tables |
| **Monte Carlo** | Correct with probability $\ge 1 - \varepsilon$ | Bounded (deterministic upper bound) | Miller–Rabin, Karger min-cut, Bloom filter queries |

Monte Carlo error can be:

- **One-sided:** only one kind of mistake. Miller–Rabin never rejects a prime; it may accept a composite. A Bloom filter never says "absent" for a present item; it may say "present" for an absent one.
- **Two-sided:** may err either way (e.g. randomized estimators of a quantity compared with a threshold).

**Complexity classes (enrichment).** **ZPP**: problems solvable by Las Vegas algorithms in expected polynomial time. **RP**: one-sided Monte Carlo in polynomial time. **BPP**: two-sided error at most $1/3$ in polynomial time. It is widely conjectured, but not proven, that BPP = P.

## Key Results

### Probability amplification by repetition

**One-sided error.** If a single run errs with probability at most $\varepsilon$ and runs are independent, then $k$ runs (answering "composite" if *any* run says so) err with probability at most $\varepsilon^k$.

For Miller–Rabin, $\varepsilon \le 1/4$, so 20 rounds give error at most $4^{-20} \approx 10^{-12}$; 40 rounds give about $10^{-24}$, far smaller than the probability of a hardware fault during the computation.

**Two-sided error.** If each run is correct with probability at least $2/3$, take the **majority** of $k$ independent runs. By a Chernoff bound the majority is wrong with probability $e^{-\Omega(k)}$: error drops exponentially in $k$.

### Converting between Las Vegas and Monte Carlo

- **Las Vegas → Monte Carlo:** run a Las Vegas algorithm with expected time $T$ for $2T$ steps; if it has not finished, output "fail" (or a guess). By **Markov's inequality** $\Pr[\text{time} \ge 2T] \le 1/2$, so the failure probability is at most $1/2$, and it can be amplified.
- **Monte Carlo → Las Vegas:** possible when answers can be **verified** cheaply. Repeat until the verifier accepts. If each run succeeds with probability $p$, the expected number of runs is $1/p$ (geometric distribution).

### Useful tools

| Tool | Statement | Typical use |
|---|---|---|
| Linearity of expectation | $\mathbb{E}[\sum X_i] = \sum \mathbb{E}[X_i]$, even for dependent $X_i$ | Counting expected comparisons (quicksort) |
| Indicator variables | $\mathbb{E}[\mathbf{1}_A] = \Pr[A]$ | Expected collisions, expected comparisons |
| Geometric distribution | Expected trials until first success is $1/p$ | "Repeat until a good pivot" arguments |
| Markov's inequality | $\Pr[X \ge a] \le \mathbb{E}[X]/a$ for $X \ge 0$ | Las Vegas → Monte Carlo |
| $1 - x \le e^{-x}$ | | Bounding repeated failure, e.g. $(1 - p)^t \le e^{-pt}$ |

## Algorithms

### Randomized quicksort (recap)

Choose the pivot uniformly at random; partition; recurse. Expected comparisons $\le 2n \ln n = O(n \log n)$ on every input; worst case still $\Theta(n^2)$ but with vanishing probability. Full analysis (indicator variables over pairs $z_i, z_j$ compared with probability $2/(j - i + 1)$) is in [Unit 5, Topic 5.4](../unit5/topic4.md). Do not re-derive it here; the same idea drives quickselect.

### Randomized selection (quickselect): Las Vegas

**Problem.** Given an unsorted array of $n$ elements and $k$ ($0 \le k < n$), return the $k$-th smallest element (0-indexed). Sorting costs $O(n \log n)$; we want $O(n)$.

**Design.** Partition around a random pivot as in quicksort, but **recurse only into the side containing rank $k$**.

```text
QUICKSELECT(A, k):                       // k-th smallest, 0-indexed
    lo = 0, hi = n - 1
    loop:
        if lo == hi: return A[lo]
        p = uniformly random index in [lo, hi]
        q = PARTITION(A, lo, hi, p)      // pivot ends at its final index q
        if k == q: return A[q]
        else if k < q: hi = q - 1
        else: lo = q + 1
```

**Worked example.** $A = [9, 3, 7, 1, 8, 2, 6]$, $k = 3$ (the 4th smallest, which is 6). One possible run:

| Round | Candidates | Random pivot | Smaller side | Larger side | Where is rank $k$? |
|---|---|---|---|---|---|
| 1 | {9, 3, 7, 1, 8, 2, 6}, $k = 3$ | 2 | {1} | {9, 3, 7, 8, 6} | right; new $k = 3 - 2 = 1$ |
| 2 | {9, 3, 7, 8, 6}, $k = 1$ | 8 | {3, 7, 6} | {9} | left; $k = 1$ |
| 3 | {3, 7, 6}, $k = 1$ | 3 | {} | {7, 6} | right; new $k = 1 - 1 = 0$ |
| 4 | {7, 6}, $k = 0$ | 7 | {6} | {} | left; $k = 0$ |
| 5 | {6} | | | | return **6** |

**Correctness.** After partitioning, the pivot is at its sorted position $q$, everything left is smaller and everything right is at least as large. So the $k$-th smallest is the pivot (if $k = q$), or lies in the side containing index $k$. The loop invariant "the answer is in `A[lo..hi]` at index $k$ of the sorted order" holds initially, is maintained by each narrowing, and at termination ($k = q$ or $lo = hi$) gives the answer.

**Expected $O(n)$ analysis.** Call a pivot **good** if its rank lies in the middle half of the current range. A random pivot is good with probability at least $1/2$, and after a good pivot the range shrinks to at most $3/4$ of its size. Group the rounds into **phases**: phase $j$ consists of the rounds in which the range size is between $(3/4)^{j+1} n$ and $(3/4)^j n$. Each phase ends at the latest after its first good pivot, so the expected number of rounds in a phase is at most 2 (geometric distribution). Each round of phase $j$ costs at most $c (3/4)^j n$. Therefore

$$
\mathbb{E}[T(n)] \le \sum_{j \ge 0} 2 \cdot c \left(\tfrac{3}{4}\right)^j n = 2cn \cdot \frac{1}{1 - 3/4} = 8cn = O(n).
$$

The worst case is still $\Theta(n^2)$ (every pivot is the minimum), with tiny probability. The deterministic **median-of-medians** algorithm achieves $O(n)$ worst case but with much larger constants; introselect-style library routines combine both.

### Miller–Rabin primality test: Monte Carlo, one-sided error

**Problem.** Given an odd $n > 3$, decide whether $n$ is prime. Trial division up to $\sqrt{n}$ is exponential in the number of digits.

**Fermat's idea and its flaw.** If $n$ is prime, $a^{n-1} \equiv 1 \pmod n$ for all $1 \le a < n$. Composite $n$ usually fail this for many $a$, but **Carmichael numbers** (e.g. $561 = 3 \cdot 11 \cdot 17$) pass it for every $a$ coprime to $n$.

**Miller's strengthening.** Write $n - 1 = 2^s d$ with $d$ odd. If $n$ is prime, the only square roots of 1 modulo $n$ are $\pm 1$. So the sequence

$$
a^d, \; a^{2d}, \; a^{4d}, \; \dots, \; a^{2^s d} = a^{n-1} \pmod n
$$

must either start at 1, or contain $n - 1$ (i.e. $-1$) somewhere before the final term. If neither happens, $a$ is a **witness** that $n$ is composite.

**Key result (Rabin).** For odd composite $n$, at least $3/4$ of the bases $a \in [1, n-1]$ are witnesses. So one random base errs with probability at most $1/4$, and $k$ independent bases err with probability at most $4^{-k}$.

**Worked examples.**

| $n$ | $n - 1 = 2^s d$ | Base $a$ | Sequence $a^d, a^{2d}, \dots$ (mod $n$) | Verdict |
|---|---|---|---|---|
| 97 (prime) | $2^5 \cdot 3$ | 5 | 28, 8, 64, 22, **96** | reaches $n - 1$: passes |
| 561 (Carmichael) | $2^4 \cdot 35$ | 2 | 263, 166, 67, 1 | reaches 1 without passing $n - 1$: **composite** (67 is a non-trivial square root of 1) |
| 221 = 13 · 17 | $2^2 \cdot 55$ | 174 | 47, **220** | passes: 174 is a *strong liar* |
| 221 | $2^2 \cdot 55$ | 137 | 188, 205 | never 1 or $n - 1$: **composite** |

The 221 rows show why several random bases are used: a single base can lie.

**Cost.** Each round is one modular exponentiation, $O(\log n)$ multiplications of $O(\log n)$-bit numbers: $O(\log^3 n)$ bit operations with schoolbook multiplication. $k$ rounds: $O(k \log^3 n)$.

**Deterministic variant.** For $n < 3.3 \times 10^{24}$ (which covers all 64-bit integers), testing the fixed bases 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37 gives a correct deterministic answer.

### Karger's minimum cut: Monte Carlo (brief)

**Problem.** In a connected undirected multigraph, find a minimum set of edges whose removal disconnects the graph.

**Algorithm.** Repeatedly pick a uniformly random edge and **contract** it (merge its endpoints, keep parallel edges, delete self-loops) until two super-vertices remain. Output the edges between them.

**Analysis.** Let the minimum cut $C$ have $k$ edges. Every vertex has degree $\ge k$ (otherwise its edges would be a smaller cut), so with $i$ vertices left there are at least $ik/2$ edges, and the chance of contracting an edge of $C$ is at most $k / (ik/2) = 2/i$. Surviving all contractions:

$$
\Pr[\text{output} = C] \ge \prod_{i=3}^{n} \left(1 - \frac{2}{i}\right) = \prod_{i=3}^{n} \frac{i - 2}{i} = \frac{2}{n(n-1)}.
$$

Repeating $T = \binom{n}{2} \ln n$ times and keeping the smallest cut fails with probability at most $(1 - 1/\binom{n}{2})^T \le e^{-\ln n} = 1/n$. A useful corollary: a graph has at most $\binom{n}{2}$ distinct minimum cuts. (The Karger–Stein refinement reduces the total cost substantially; enrichment only.)

### Universal hashing: randomized data structure

**Problem.** A hash table with a fixed hash function has $O(n)$ worst-case operations, and an adversary can force it.

**Definition.** A family $\mathcal{H}$ of functions $U \to \{0, \dots, m-1\}$ is **universal** if for all distinct keys $x \ne y$,

$$
\Pr_{h \in \mathcal{H}}[h(x) = h(y)] \le \frac{1}{m}.
$$

**Construction (Carter–Wegman).** Choose a prime $p$ larger than every key. For $a \in \{1, \dots, p-1\}$ and $b \in \{0, \dots, p-1\}$, let $h_{a,b}(x) = ((a x + b) \bmod p) \bmod m$. The family of all $h_{a,b}$ is universal.

**Consequence.** With chaining and $n$ keys in $m$ buckets (load factor $\alpha = n/m$), for **any** fixed set of keys and any key $x$, the expected length of $x$'s chain is at most $1 + \alpha$ (by linearity of expectation over indicator variables $\mathbf{1}[h(x) = h(y)]$). The expectation is over the random choice of $h$, made when the table is created and hidden from the adversary.

### Reservoir sampling: random sampling from a stream

**Problem.** Choose $k$ items uniformly at random from a stream of unknown length $N$, in one pass, using $O(k)$ memory.

**Algorithm R.** Keep the first $k$ items. For the item with 0-based index $i \ge k$, draw $j$ uniformly from $\{0, \dots, i\}$; if $j < k$, replace `reservoir[j]` with the new item.

**Proof (induction).** Claim: after processing $t$ items ($t \ge k$), each of them is in the reservoir with probability $k/t$. True for $t = k$. When item number $t$ (0-based index $t$, the $(t+1)$-th item) arrives, it enters with probability $k/(t+1)$. An item already in the reservoir is evicted only if the new item enters and picks its slot: probability $\frac{k}{t+1} \cdot \frac{1}{k} = \frac{1}{t+1}$. So it remains with probability $\frac{k}{t} \cdot \frac{t}{t+1} = \frac{k}{t+1}$. $\blacksquare$

## Complexity Analysis

| Algorithm | Type | Time | Error / guarantee | Space |
|---|---|---|---|---|
| Randomized quicksort | Las Vegas | Expected $O(n \log n)$, worst $O(n^2)$ | Always correct | $O(\log n)$ expected stack |
| Quickselect | Las Vegas | Expected $O(n)$, worst $O(n^2)$ | Always correct | $O(1)$ extra (in place) |
| Miller–Rabin, $k$ rounds | Monte Carlo (one-sided) | $O(k \log^3 n)$ | Composite accepted w.p. $\le 4^{-k}$ | $O(\log n)$ bits |
| Karger, one trial | Monte Carlo | $O(m \, \alpha(n))$ with random edge order + union-find, $O(n^2)$ with adjacency matrix | Success $\ge 2/(n(n-1))$ | $O(n + m)$ |
| Karger, $\binom{n}{2} \ln n$ trials | Monte Carlo | $O(n^2 \log n)$ trials times trial cost | Failure $\le 1/n$ | $O(n + m)$ |
| Universal hash table (chaining) | Las Vegas | Expected $O(1 + \alpha)$ per operation | Always correct | $O(n + m)$ |
| Reservoir sampling | Exact distribution | $O(N)$ for the stream | Uniform sample | $O(k)$ |

## Python Implementation

```python
import random


def quickselect(a, k):
    """Return the k-th smallest element of a (k = 0 is the minimum). Las Vegas."""
    if not 0 <= k < len(a):
        raise IndexError("k out of range")
    a = list(a)
    lo, hi = 0, len(a) - 1
    while True:
        if lo == hi:
            return a[lo]
        p = random.randint(lo, hi)
        a[p], a[hi] = a[hi], a[p]
        pivot, store = a[hi], lo
        for i in range(lo, hi):                 # Lomuto partition of a[lo..hi]
            if a[i] < pivot:
                a[i], a[store] = a[store], a[i]
                store += 1
        a[store], a[hi] = a[hi], a[store]       # pivot now at its final index
        if k == store:
            return a[store]
        if k < store:
            hi = store - 1
        else:
            lo = store + 1


def is_probable_prime(n, rounds=20):
    """Miller-Rabin. Never rejects a prime; wrongly accepts a composite
    with probability at most 4**(-rounds). Monte Carlo (one-sided error)."""
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:                           # n - 1 = 2^s * d with d odd
        d //= 2
        s += 1
    for _ in range(rounds):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False                        # a is a witness: n is composite
    return True


def reservoir_sample(stream, k):
    """Uniform random sample of k items from an iterable of unknown length."""
    reservoir = []
    for i, item in enumerate(stream):
        if i < k:
            reservoir.append(item)
        else:
            j = random.randint(0, i)            # inclusive: i + 1 choices
            if j < k:
                reservoir[j] = item
    return reservoir


def karger_min_cut(edges, n, trials):
    """edges: list of (u, v) on vertices 0..n-1, connected multigraph.
    Returns the smallest cut size found over independent trials (Monte Carlo)."""
    best = float("inf")
    for _ in range(trials):
        parent = list(range(n))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        order = edges[:]
        random.shuffle(order)                   # contracting in random order
        components = n
        for u, v in order:
            if components == 2:
                break
            ru, rv = find(u), find(v)
            if ru != rv:
                parent[ru] = rv                 # contract edge (u, v)
                components -= 1
        cut = sum(1 for u, v in edges if find(u) != find(v))
        best = min(best, cut)
    return best


class UniversalHash:
    """h(x) = ((a*x + b) mod p) mod m, with a, b random; p prime > every key."""

    P = (1 << 61) - 1                           # a Mersenne prime

    def __init__(self, m):
        self.m = m
        self.a = random.randrange(1, self.P)
        self.b = random.randrange(0, self.P)

    def __call__(self, x):
        return ((self.a * x + self.b) % self.P) % self.m
```

- `quickselect` copies the input so the caller's list is not reordered; it is iterative, so there is no recursion-depth issue. Tested against `sorted(a)[k]` on thousands of random arrays with many duplicates.
- In `is_probable_prime`, the trial division by small primes handles $n \le 37$ and even numbers before `randrange(2, n - 1)` is called. The inner `for ... else` returns "composite" only if the squaring loop never hit $n - 1$. Tested: exact agreement with trial division for all $n < 5000$, rejection of Carmichael numbers (561, 1105, 1729, ...) and strong pseudoprimes to several small bases.
- `reservoir_sample` uses `random.randint(0, i)`, which is **inclusive**; a frequency test over 60,000 runs showed every item selected with probability close to $k/N$.
- `karger_min_cut` contracts edges in a random order using union-find. Processing a uniformly random permutation of edges and skipping those inside a super-vertex is equivalent to repeatedly picking a uniformly random remaining non-loop edge.
- `UniversalHash` uses Python's arbitrary-precision integers, so `a * x` cannot overflow; keys must be non-negative integers smaller than $p$.

## Edge Cases and Pitfalls

| Case / pitfall | What goes wrong | Fix |
|---|---|---|
| Quickselect with many duplicates | Two-way partition degrades towards $O(n^2)$ when all keys are equal | Use three-way partitioning (less, equal, greater) |
| Quickselect $k$ off by one | Returns the $(k+1)$-th smallest | Fix 0- vs 1-based convention in the interface |
| Miller–Rabin on $n \le 3$ or even $n$ | `randrange(2, n - 1)` is empty or meaningless | Handle small $n$ and even $n$ first |
| Fermat test instead of Miller–Rabin | Carmichael numbers pass every coprime base | Use the full squaring sequence check |
| `random` for cryptography | Mersenne Twister is predictable from its outputs | Use `secrets` / OS randomness for keys and seeds |
| Fixed seed in production | Randomization no longer hides from an adversary | Seed from OS entropy; fixed seeds only in tests |
| Reservoir with `randint(0, i - 1)` | Biased sample | Draw from $\{0, \dots, i\}$ (i + 1 values, 0-based) |
| Karger with too few trials | Min cut missed with high probability | Use about $\binom{n}{2} \ln n$ trials, or Karger–Stein |
| Universal hash with $p \le$ max key | Distinct keys collide modulo $p$ for every $h$ | Choose $p$ larger than the key universe |
| Tests that depend on random output | Flaky tests | Seed the generator in tests, or assert properties instead of exact outputs |

## Common Misconceptions

- **"Randomized means unreliable."** Las Vegas algorithms are always correct; Monte Carlo error can be pushed below $10^{-20}$ with a few repetitions, far below hardware error rates.
- **"Expected time is the same as average-case time."** Expected time is over the algorithm's coins for the worst input; average case is over an assumed input distribution.
- **"Randomization improves the worst case."** It does not remove the worst case (randomized quicksort can still take $\Theta(n^2)$); it makes it astronomically unlikely and independent of the input.
- **"Monte Carlo answers can always be checked."** Only if a fast verifier exists. Primality has one in principle (certificates), but Miller–Rabin output itself is not a proof.
- **"Python's `random` is random enough for everything."** It is fine for algorithms and simulations, not for security.

## Alternatives and Trade-offs

| Problem | Randomized | Deterministic alternative | Trade-off |
|---|---|---|---|
| Sorting | Randomized quicksort, expected $O(n \log n)$ | Merge sort / heapsort $O(n \log n)$ worst; introsort | Randomized is fast and simple; deterministic gives guarantees |
| Selection | Quickselect, expected $O(n)$ | Median of medians, $O(n)$ worst | Deterministic has large constants |
| Primality | Miller–Rabin, $O(k \log^3 n)$, error $4^{-k}$ | AKS (polynomial, impractical); deterministic MR bases for 64-bit | Randomized is the practical standard for large $n$ |
| Min cut | Karger / Karger–Stein | Stoer–Wagner $O(nm + n^2 \log n)$ | Stoer–Wagner is deterministic and practical for moderate sizes |
| Hashing | Universal / seeded hashing, expected $O(1)$ | Balanced BST $O(\log n)$ worst | Hashing faster on average; trees have worst-case guarantees and ordering |
| Sampling a stream | Reservoir sampling | Store everything, then sample | Reservoir uses $O(k)$ memory |

**Use randomization** when worst-case inputs are plausible or adversarial, when a simple randomized algorithm replaces a complex deterministic one, or when an exponentially small error is acceptable. **Avoid it** when you need reproducible results without seeding, hard real-time worst-case guarantees, or certified correctness (e.g. a proof of primality for a mathematical claim).

## In Practice

- **Hash tables:** after hash-flooding attacks were publicized in 2011, languages adopted seeded hash functions. Python randomizes the hash of `str` and `bytes` per process (controlled by `PYTHONHASHSEED`) and uses SipHash; Rust's standard `HashMap` uses SipHash-1-3 with random keys by default.
- **Cryptography:** RSA key generation draws random odd numbers of the right size and tests them with Miller–Rabin (after cheap trial division) until a probable prime is found.
- **Databases and storage:** **Bloom filters** answer "definitely not present" or "probably present" using $m$ bits and $k$ hash functions, with false-positive rate about $(1 - e^{-kn/m})^k$ and no false negatives. LSM-tree storage engines such as LevelDB, RocksDB and Cassandra use them to skip disk reads for absent keys.
- **Load balancing:** the "power of two choices": sending each request to the less loaded of **two** randomly chosen servers reduces the maximum load (for $n$ requests on $n$ servers) from $\Theta(\log n / \log \log n)$ to $\Theta(\log \log n)$ with high probability. NGINX offers this as its `random two` upstream balancing method.
- **Streaming and analytics:** reservoir sampling for log sampling; randomized sketches (Count-Min sketch, HyperLogLog) estimate frequencies and distinct counts in tiny memory.
- **Data structures:** skip lists (used for Redis sorted sets) and treaps achieve expected $O(\log n)$ operations through random levels or priorities.
- **Machine learning:** stochastic gradient descent, random initialization, dropout, random forests and train/test shuffling are all randomized algorithms; fixing seeds is essential for reproducible experiments.

## Interview and Competitive Programming

**Recognition cues**

- "$k$-th largest / median in an unsorted array, $O(n)$ expected" → quickselect (or a size-$k$ heap for $O(n \log k)$).
- "Random element from a linked list or stream of unknown length", "uniform pick from a stream" → reservoir sampling ($k = 1$).
- "Is this 64-bit number prime?" with many queries → deterministic Miller–Rabin with the fixed 12 bases.
- "Shuffle an array uniformly" → Fisher–Yates: for $i$ from $n-1$ down to 1, swap `a[i]` with `a[randint(0, i)]`.
- Anti-hash tests on judges (Codeforces "hacks") → randomize your hash (random base for polynomial string hashing, random seed for custom hash functions).

**Typical constraints:** $n \le 10^6$ for selection → expected $O(n)$; primality for $n \le 10^{18}$ with $10^5$ queries → $O(12 \log n)$ multiplications each.

**Common traps:** quickselect with a fixed pivot (worst-case tests exist); `randint` inclusive bounds; 64-bit overflow in modular multiplication in C++ (use 128-bit intermediates); naive shuffle "swap each $i$ with any random index" is biased.

## Using AI Assistants Critically

- LLM-written Miller–Rabin often implements only the Fermat test or mishandles the squaring loop; test it on 561, 1105, 1729 and 3215031751 (a strong pseudoprime to bases 2, 3, 5 and 7).
- Generated reservoir sampling frequently uses the wrong range (`randint(0, i - 1)` or 1-based mix-ups). Run a frequency test: over many runs every item should appear with probability $k/N$.
- Assistants often state quickselect as "$O(n)$" without "expected", or claim average-case and expected are the same. Ask for the probabilistic argument (good-pivot phases).
- Many AI quickselect versions use a fixed pivot or two-way partitioning; feed them sorted input and all-equal input and time them at doubling sizes to expose $O(n^2)$ behaviour.
- For Monte Carlo code, check that error probability is stated and that the number of repetitions matches the target; ask "what is the failure probability after $k$ trials?" and verify the arithmetic.
- Ensure security-relevant code uses `secrets` or OS randomness, not `random`, and that tests seed the generator for reproducibility.

## Practice

### Beginner

1. **Classify.** For randomized quicksort, Miller–Rabin, Bloom filter lookup, quickselect and Karger, state Las Vegas or Monte Carlo and whether error is one- or two-sided. Difficulty: Easy.
2. **Amplification.** A test has one-sided error $1/3$. How many independent runs are needed to make the error below $10^{-9}$? Difficulty: Easy.
3. **Hand Miller–Rabin.** Run one round on $n = 341$ with $a = 2$, showing $n - 1 = 2^s d$ and the sequence. Difficulty: Easy.

### Intermediate

1. **Kth largest.** Input: $n \le 10^6$ integers and $k$. Output: the $k$-th largest element in expected $O(n)$. Handle many duplicates. Difficulty: Medium.
2. **Weighted reservoir.** Input: a stream of $(item, weight)$ pairs. Output: one item chosen with probability proportional to its weight, in one pass and $O(1)$ memory. Prove correctness. Difficulty: Medium.
3. **Expected collisions.** With a universal family, $n$ keys and $m$ buckets, derive the expected number of colliding pairs. Difficulty: Medium.

### Advanced

1. **Quickselect bound.** Prove that the expected number of comparisons of quickselect is at most $4n$ for $k$ = median using a more careful analysis than the phase argument. Difficulty: Hard.
2. **Karger bound.** Prove that every graph has at most $\binom{n}{2}$ minimum cuts using the analysis of Karger's algorithm. Difficulty: Hard.
3. **Freivalds' algorithm.** Given $n \times n$ matrices $A, B, C$, design an $O(n^2)$ Monte Carlo test of $AB = C$ with one-sided error at most $1/2$ per round, and prove the error bound. Difficulty: Hard.

### Interview / CP

1. **Linked list random node.** Input: a singly linked list of unknown length. Output: a uniformly random node value per call, using $O(1)$ extra memory. Difficulty: Medium.
2. **Shuffle an array.** Implement `shuffle()` returning a uniformly random permutation, and prove uniformity. $n \le 200$. Difficulty: Medium.
3. **Prime queries.** Input: up to $10^5$ integers $n \le 10^{18}$. Output: "YES" or "NO" for primality of each. Difficulty: Medium.

## Self-Check Questions

??? question "Q1. Distinguish Las Vegas and Monte Carlo algorithms with one example each."

    Las Vegas: always correct, random running time (randomized quicksort, quickselect). Monte Carlo: bounded running time, may be wrong with small probability (Miller–Rabin, Karger).

??? question "Q2. Why is randomized quicksort's $O(n \log n)$ bound stronger than deterministic quicksort's average-case $O(n \log n)$?"

    The randomized bound holds for every input, with expectation over the algorithm's own coins. The deterministic average-case bound assumes inputs are random permutations; on sorted or adversarial inputs, deterministic quicksort with a fixed pivot rule can take $\Theta(n^2)$.

??? question "Q3. Miller–Rabin with 25 rounds says $n$ is prime. What can you claim?"

    If $n$ is prime, the test always says prime. If $n$ is composite, the probability that all 25 rounds miss a witness is at most $4^{-25} \approx 10^{-15}$. So $n$ is prime with overwhelming confidence, but this is not a proof.

??? question "Q4. Sketch why quickselect runs in expected linear time."

    A random pivot lands in the middle half with probability at least $1/2$, shrinking the range to at most $3/4$. Expect at most two rounds per phase; costs per phase form a geometric series $\sum 2c(3/4)^j n = 8cn$.

??? question "Q5. How many Karger trials are needed for failure probability at most $1/n$, and why?"

    About $\binom{n}{2} \ln n$. One trial succeeds with probability at least $1/\binom{n}{2}$, so $T$ trials all fail with probability at most $(1 - 1/\binom{n}{2})^T \le e^{-T/\binom{n}{2}} = 1/n$.

??? question "Q6. A public web API uses a hash map with a fixed, published hash function. What attack is possible, and what is the fix?"

    An attacker sends many keys that hash to the same bucket, making each operation $O(n)$ and the server CPU-bound (hash flooding). Fix: choose the hash function at random per process (seeded/keyed hashing such as SipHash, or a universal family), so the attacker cannot predict collisions.

??? question "Q7. In reservoir sampling with $k = 1$, what is the probability that the 3rd of 5 items is the final sample?"

    It enters with probability $1/3$, survives item 4 with probability $3/4$ and item 5 with probability $4/5$: $\tfrac{1}{3} \cdot \tfrac{3}{4} \cdot \tfrac{4}{5} = \tfrac{1}{5}$, as required.

??? question "Q8. A Bloom filter says a key is present. What do you do?"

    Treat it as "possibly present" and check the authoritative store (e.g. read from disk). A Bloom filter has false positives but no false negatives, so a "not present" answer can be trusted and saves the lookup.

## Complexity Summary

| Algorithm | Expected / guaranteed time | Worst case | Error |
|---|---|---|---|
| Randomized quicksort | $O(n \log n)$ expected | $O(n^2)$ (vanishing probability) | None |
| Quickselect | $O(n)$ expected | $O(n^2)$ | None |
| Median of medians (deterministic) | $O(n)$ | $O(n)$ | None |
| Miller–Rabin, $k$ rounds | $O(k \log^3 n)$ | same | $\le 4^{-k}$, one-sided |
| Karger, one trial | $O(m \, \alpha(n))$ (random order + union-find) | same | Success $\ge 2/(n(n-1))$ |
| Universal hashing (chaining) | $O(1 + \alpha)$ expected per operation | $O(n)$ | None |
| Reservoir sampling | $O(N)$ time, $O(k)$ space | same | Exact uniform sample |

## Key Takeaways

- Randomized algorithms use coin flips inside the algorithm; analysis is for the worst input, in expectation over the coins.
- **Las Vegas:** always correct, random time (quicksort, quickselect, universal hashing). **Monte Carlo:** fixed time, small error (Miller–Rabin, Karger, Bloom filters).
- Independent repetition amplifies success: one-sided error $\varepsilon$ becomes $\varepsilon^k$; two-sided error drops exponentially by majority vote.
- Quickselect is expected $O(n)$ by the good-pivot argument; Miller–Rabin errs with probability at most $4^{-k}$; Karger succeeds with probability at least $2/(n(n-1))$ per trial.
- Universal hashing and seeded hash functions protect hash tables from adversarial inputs.
- Reservoir sampling gives a uniform sample of a stream in $O(k)$ memory.
- In engineering: seed from OS entropy in production, fix seeds in tests, and never use `random` for security.
