# Combinatorics

!!! abstract "At a glance"

    - **Problem space:** counting the objects an algorithm might have to examine (subsets, orderings, paths, assignments) without listing them.
    - **Key ideas:** sum and product rules, bijections, binomial coefficients, pigeonhole, inclusion–exclusion, and counting recurrences (Fibonacci, Catalan).
    - **Core complexities:** $\binom{n}{r} \bmod p$ in $O(1)$ per query after $O(n)$ precomputation; Pascal's triangle $O(n^2)$; inclusion–exclusion over $k$ sets $O(2^k)$.
    - **Where it is used:** estimating brute-force cost ($2^n$ subsets, $n!$ orderings), lower-bound proofs (sorting needs $\log_2 n!$ comparisons), probability of collisions, DP state counting, and "count the ways modulo $10^9+7$" problems.

## Motivation and Problem Context

Before writing any algorithm, an engineer should be able to answer: **how many candidate solutions are there?** A route planner choosing an order for 15 delivery stops faces $15! \approx 1.3 \times 10^{12}$ orderings — trying them all is hopeless. A feature-flag system with 30 independent flags has $2^{30} \approx 10^9$ configurations — exhaustive testing is impossible, so you need pairwise or sampling strategies. A password policy of 8 characters from 62 symbols allows $62^8 \approx 2.2 \times 10^{14}$ passwords — that number decides whether brute-force attacks are feasible.

Combinatorics turns these questions into formulas. In this course it plays three roles:

1. **Cost estimation** — the size of the search space is the running time of brute force.
2. **Proof tool** — pigeonhole and counting arguments prove lower bounds and the existence of collisions and cycles.
3. **Computation** — many problems ask *for* a count, which must be computed exactly or modulo a prime.

## Problem Formulation

A counting problem specifies a finite set $S$ of objects described by rules, and asks for $|S|$ (often modulo a prime $p$). The input is usually a few integers ($n$, $k$, constraints), so enumerating $S$ — which may have exponentially many elements — is the baseline we want to avoid.

| Question | Formal answer |
| --- | --- |
| Ordered selections of $r$ from $n$, no repetition | $P(n, r) = n!/(n-r)!$ |
| Unordered selections of $r$ from $n$, no repetition | $\binom{n}{r} = \dfrac{n!}{r!(n-r)!}$ |
| Ordered selections with repetition | $n^r$ |
| Unordered selections with repetition (multisets) | $\binom{n + r - 1}{r}$ |
| Arrangements of a multiset with counts $k_1, \dots, k_m$ | $\dfrac{n!}{k_1! \cdots k_m!}$ |

**Assumption:** "objects" are distinguishable unless stated otherwise. Misreading this (distinguishable vs identical, ordered vs unordered) is the most common source of wrong counts.

## Intuition

Counting is **structured decomposition**. Break a complicated object into a sequence of independent choices (multiply), or split the set into disjoint cases (add). When that is hard, find a **bijection** to something easy to count, or count the complement, or overcount and correct (inclusion–exclusion). Mental model: *describe one object as a sequence of decisions; the count is the number of distinct decision sequences, provided each object corresponds to exactly one sequence.*

## Definitions and Basic Principles

| Principle | Statement | Example |
| --- | --- | --- |
| Sum rule | If $S = A \cup B$ with $A \cap B = \emptyset$, then $\lvert S \rvert = \lvert A \rvert + \lvert B \rvert$ | Choose a dessert from 3 cakes **or** 4 ice creams: 7 |
| Product rule | If an object is built by a choice with $a$ options followed by an independent choice with $b$ options: $ab$ | 3 shirts **and** 4 trousers: 12 outfits |
| Bijection rule | If there is a one-to-one correspondence $A \leftrightarrow B$, then $\lvert A \rvert = \lvert B \rvert$ | Subsets of $\{1..n\}$ $\leftrightarrow$ $n$-bit strings, so $2^n$ |
| Complement rule | $\lvert \overline{A} \rvert = \lvert U \rvert - \lvert A \rvert$ | Bit strings of length 8 with at least one 1: $2^8 - 1$ |
| Division rule | If every object is counted exactly $k$ times, divide by $k$ | Circular seatings of $n$ people: $n!/n = (n-1)!$ |

$n!$ (factorial) counts orderings of $n$ distinct items; $0! = 1$ because there is exactly one way to arrange nothing.

!!! warning "Important: ordered vs unordered, distinct vs identical"

    Before applying any formula, decide two things: (1) does order matter? (2) are the items/boxes distinguishable? Choosing a committee of 3 from 10 is $\binom{10}{3} = 120$; choosing a president, secretary and treasurer is $P(10,3) = 720$. Most wrong exam answers use the right formula for the wrong question.

## Key Results

### Binomial coefficients

$\binom{n}{k}$ counts $k$-element subsets of an $n$-element set.

**Pascal's rule.** $\binom{n}{k} = \binom{n-1}{k-1} + \binom{n-1}{k}$, with $\binom{n}{0} = \binom{n}{n} = 1$.
*Combinatorial proof.* Fix element $n$. A $k$-subset either contains it (choose the other $k-1$ from $n-1$) or does not (choose all $k$ from $n-1$). The cases are disjoint, so add. $\square$

This is exactly a **dynamic programming recurrence** with overlapping subproblems ([Unit 6.1](../unit6/topic1.md)): computing it recursively without memoization is exponential, while the table is $O(n^2)$.

**Binomial theorem.** $(x + y)^n = \sum_{k=0}^{n} \binom{n}{k} x^k y^{n-k}$. Each of the $n$ factors contributes either $x$ or $y$; terms with exactly $k$ copies of $x$ correspond to $k$-subsets of factors.

| Identity | Meaning / use |
| --- | --- |
| $\binom{n}{k} = \binom{n}{n-k}$ | Choosing what to include = choosing what to exclude; compute with the smaller $k$ |
| $\sum_{k=0}^{n} \binom{n}{k} = 2^n$ | Total number of subsets ($x = y = 1$ in the binomial theorem) |
| $\sum_{k=0}^{n} (-1)^k \binom{n}{k} = 0$ for $n \ge 1$ | Even-size and odd-size subsets are equinumerous; the engine of inclusion–exclusion |
| $\sum_{i=r}^{n} \binom{i}{r} = \binom{n+1}{r+1}$ | Hockey stick; e.g. counting triples $i < j < k$ by the largest element |
| $\binom{n}{k} = \frac{n}{k}\binom{n-1}{k-1}$ | Gives an $O(k)$ multiplicative formula |
| $\binom{n}{k} \le \left(\frac{en}{k}\right)^k$ | Upper bound used in complexity estimates |

**Stars and bars.** The number of solutions of $x_1 + \dots + x_k = n$ in non-negative integers is $\binom{n + k - 1}{k - 1}$.
*Proof.* Encode a solution as a row of $n$ stars and $k - 1$ bars (bars separate the groups). Every arrangement of $n + k - 1$ symbols with $k-1$ bars is exactly one solution: choose the bar positions. For positive integers ($x_i \ge 1$), substitute $y_i = x_i - 1$ to get $\binom{n-1}{k-1}$.

### Computing $\binom{n}{r}$ exactly and modulo a prime

| Method | Precompute | Query | Works when |
| --- | --- | --- | --- |
| Pascal's table | $O(n^2)$ time and space | $O(1)$ | $n \le$ a few thousand; any modulus (only additions) |
| Multiplicative formula with big integers | — | $O(r)$ big-integer ops | Exact values, moderate $n$ (`math.comb`) |
| Factorials + inverse factorials mod $p$ | $O(n)$ | $O(1)$ | $p$ prime and $n < p$ (typical: $n \le 10^6$, $p = 10^9+7$) |
| Lucas' theorem | $O(p)$ or none | $O(\log_p n)$ small binomials | $p$ is a **small** prime, $n$ huge |

**Factorial method.** $\binom{n}{r} \equiv n! \cdot (r!)^{-1} \cdot ((n-r)!)^{-1} \pmod p$. The inverses exist because $p$ is prime and $p \nmid k!$ for $k < p$ ([Topic 1.1](topic1.md)). Compute all inverse factorials with **one** modular exponentiation using $\big((i-1)!\big)^{-1} = (i!)^{-1} \cdot i$.

**Lucas' theorem.** For prime $p$, write $n$ and $r$ in base $p$: $n = (n_t \dots n_0)_p$, $r = (r_t \dots r_0)_p$. Then $\binom{n}{r} \equiv \prod_i \binom{n_i}{r_i} \pmod p$, with $\binom{n_i}{r_i} = 0$ when $r_i > n_i$.

!!! warning "Important: the factorial method needs $n < p$"

    If $n \ge p$ then $n!$ contains the factor $p$, so $n! \equiv 0 \pmod p$ and its "inverse" does not exist. With $p = 10^9+7$ and $n \le 10^6$ this never happens, but with a small prime (e.g. $p = 13$) you must use Lucas' theorem.

### Pigeonhole principle

**Statement.** If $n$ objects are placed into $m$ boxes and $n > m$, some box contains at least two objects. **Generalized:** some box contains at least $\lceil n/m \rceil$ objects.
*Proof.* If every box had at most $\lceil n/m \rceil - 1 < n/m$ objects, the total would be less than $n$. $\square$

Pigeonhole is an **existence** tool: it says a collision must happen without saying where. Algorithmic consequences:

- **Hash collisions are unavoidable.** Mapping a universe of size $|U| > m$ into $m$ buckets forces some bucket to receive at least $\lceil |U|/m \rceil$ keys; an adversary who knows $h$ can put all keys there. This is why worst-case hashing is $O(n)$ and why randomized (universal) hashing is used ([Topic 1.3](topic3.md)).
- **No lossless compressor shrinks every file.** There are $2^n$ files of length $n$ but only $2^n - 1$ shorter bit strings.
- **Iterated functions on a finite set must cycle.** The sequence $x_0, f(x_0), f(f(x_0)), \dots$ with $f: S \to S$ and $|S| = m$ repeats a value within $m + 1$ terms. This is the basis of cycle detection below.
- **Remainders repeat.** Among any $m + 1$ integers, two have the same remainder modulo $m$; among prefix sums $s_0, \dots, s_m$ of $m$ integers, two agree modulo $m$, so some contiguous block has sum divisible by $m$.

### Inclusion–exclusion

For finite sets $A_1, \dots, A_k$:

$$
\Big|\bigcup_{i=1}^{k} A_i\Big| = \sum_{i} |A_i| - \sum_{i<j} |A_i \cap A_j| + \sum_{i<j<l} |A_i \cap A_j \cap A_l| - \cdots + (-1)^{k+1} |A_1 \cap \cdots \cap A_k| .
$$

*Proof.* Take an element lying in exactly $t \ge 1$ of the sets. It is counted $\binom{t}{1} - \binom{t}{2} + \binom{t}{3} - \cdots = 1 - \sum_{j=0}^{t}(-1)^j\binom{t}{j} = 1 - 0 = 1$ time, using the alternating-sum identity. Elements in no set are counted 0 times. $\square$

Typical use: count objects that avoid **all** of several "bad" properties: $|\text{good}| = |U| - |\bigcup A_i|$. The sum has $2^k - 1$ terms, so it is practical when $k$ is small (about $k \le 20$) and each intersection is easy to count.

### Counting recurrences: Fibonacci and Catalan

**Fibonacci.** $F_0 = 0$, $F_1 = 1$, $F_n = F_{n-1} + F_{n-2}$. Many counts satisfy this recurrence because the last decision has two options of sizes 1 and 2:

- ways to climb $n$ stairs using steps of 1 or 2: $F_{n+1}$;
- tilings of a $2 \times n$ strip by dominoes: $F_{n+1}$;
- binary strings of length $n$ with no two consecutive 1s: $F_{n+2}$.

Growth: $F_n = (\phi^n - \psi^n)/\sqrt5$ with $\phi = \frac{1+\sqrt5}{2} \approx 1.618$ (Binet), so $F_n = \Theta(\phi^n)$. $F_{92}$ is the largest Fibonacci number that fits in a signed 64-bit integer and $F_{93}$ the largest that fits in an unsigned one. Other facts worth recognizing: $\gcd(F_m, F_n) = F_{\gcd(m,n)}$; $F_n \bmod m$ is periodic (the Pisano period, e.g. 60 for $m = 10$); every positive integer is a unique sum of non-consecutive Fibonacci numbers (Zeckendorf). Computing $F_n$ for $n$ up to $10^{18}$ uses matrix exponentiation, covered in [Unit 4.7](../unit4/topic7.md).

**Catalan numbers.**

$$
C_n = \frac{1}{n+1}\binom{2n}{n}, \qquad C_0 = 1,\quad C_{n+1} = \sum_{i=0}^{n} C_i\, C_{n-i}
$$

Sequence: $1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862, \dots$ The recurrence comes from splitting at the first "return to balance": a balanced string is `(` $A$ `)` $B$ with $A$, $B$ balanced.

| Structure | Count |
| --- | --- |
| Balanced strings of $n$ pairs of parentheses | $C_n$ |
| Binary search trees on $n$ distinct keys (tree shapes) | $C_n$ |
| Full binary trees with $n + 1$ leaves | $C_n$ |
| Triangulations of a convex $(n+2)$-gon | $C_n$ |
| Monotone lattice paths $(0,0) \to (n,n)$ never above the diagonal | $C_n$ |
| Ways to fully parenthesize a product of $n + 1$ factors | $C_n$ |
| Non-crossing handshakes among $2n$ people around a table | $C_n$ |

*Reflection proof of the closed form.* There are $\binom{2n}{n}$ monotone paths from $(0,0)$ to $(n,n)$. A bad path touches the line $y = x + 1$; reflect its portion after the first touch across that line. This is a bijection between bad paths and **all** paths to $(n-1, n+1)$, of which there are $\binom{2n}{n+1}$. Hence $C_n = \binom{2n}{n} - \binom{2n}{n+1} = \frac{1}{n+1}\binom{2n}{n}$.

The parenthesization row matters for [Matrix Chain Multiplication (Unit 6.3)](../unit6/topic3.md): the number of ways to parenthesize a chain of $n$ matrices is $C_{n-1} = \Omega(4^n / n^{3/2})$, which is why brute force fails and DP is needed.

## Counting for Complexity Analysis

The most important algorithmic use of combinatorics in this course: **the size of the search space is the cost of brute force**.

| Search space | Size | Brute force | Practical limit ($\approx 10^8$ simple ops/s) |
| --- | --- | --- | --- |
| Pairs $i < j$ | $\binom{n}{2} = \Theta(n^2)$ | Double loop | $n \approx 10^4$ |
| Triples | $\binom{n}{3} = \Theta(n^3)$ | Triple loop | $n \approx 500$ |
| All subsets | $2^n$ | Bitmask enumeration, $O(2^n \cdot n)$ | $n \approx 20$–$25$ |
| Subsets of size $k$ | $\binom{n}{k}$ | Combinations | $\binom{40}{5} \approx 6.6 \times 10^5$ is fine, $\binom{40}{20} \approx 1.4 \times 10^{11}$ is not |
| All orderings | $n!$ | Permutations, $O(n! \cdot n)$ | $n \approx 10$–$11$ |
| Binary strings / assignments of $n$ variables | $2^n$ | | $n \approx 25$ |
| Functions $[n] \to [k]$ (colourings) | $k^n$ | | $3^n$: $n \approx 15$ |

**Stirling's approximation** $n! \approx \sqrt{2\pi n}\,(n/e)^n$ gives $\log_2 n! = n \log_2 n - n\log_2 e + O(\log n) = \Theta(n \log n)$. This is the heart of the **comparison-sorting lower bound** ([Unit 5.2](../unit5/topic2.md)): a decision tree must have at least $n!$ leaves, so its height is at least $\log_2 n! = \Omega(n \log n)$.

Counting also bounds DP: the running time of a memoized algorithm is (number of distinct states) $\times$ (work per state). For example, LCS on strings of lengths $m$ and $n$ has $(m+1)(n+1)$ states ([Unit 6.4](../unit6/topic4.md)), while the naive recursion explores up to $\binom{m+n}{n}$ paths.

!!! warning "Important: $2^n$ vs $n!$"

    $n!$ grows much faster than $2^n$: $2^{20} \approx 10^6$ but $20! \approx 2.4 \times 10^{18}$. "Try every subset" and "try every ordering" are very different budgets. Problems with $n \le 20$ usually intend $O(2^n \cdot n)$ bitmask DP; $n \le 10$ hints at $O(n!)$.

## Method: Solving a Counting Problem

1. **Restate** the objects precisely: ordered or unordered? repetition allowed? distinguishable items and boxes?
2. **Brute-force small cases** (by hand or with `itertools`) to get the first few answers.
3. **Decompose**: product rule over independent decisions, sum rule over disjoint cases, or a recurrence over the "last decision".
4. If constraints are of the form "none of these bad events", use **complement + inclusion–exclusion**.
5. If the small answers match a known sequence ($1, 2, 5, 14, 42$; $1, 1, 2, 3, 5, 8$), suspect Catalan or Fibonacci and look for the matching decomposition.
6. **Verify** the formula against the brute force for all small inputs before trusting it.
7. **Compute** it: exact big integers, Pascal's table, or factorials modulo $p$, depending on size.

## Worked Examples

!!! example "Example 1 (basic): product rule and its trap"

    How many 4-digit PINs have **no repeated digit**? Choices: $10 \cdot 9 \cdot 8 \cdot 7 = 5040 = P(10, 4)$. How many have **at least one** repeated digit? Complement: $10^4 - 5040 = 4960$. Counting "at least one repeat" directly by cases is error-prone; the complement is one subtraction.

!!! example "Example 2 (basic): committees and stars and bars"

    - A 5-card poker hand from 52 cards: order irrelevant, so $\binom{52}{5} = 2{,}598{,}960$.
    - Distributing 7 identical tasks among 3 servers (some servers may get none): $\binom{7 + 2}{2} = 36$.
    - Same, but every server gets at least one: $\binom{6}{2} = 15$.

!!! example "Example 3 (intermediate): inclusion–exclusion, numbers coprime to 30"

    Count $x \in [1, 100]$ divisible by none of $2, 3, 5$. Let $A_p$ = multiples of $p$.

    | Term | Value |
    | --- | --- |
    | $\lvert A_2 \rvert + \lvert A_3 \rvert + \lvert A_5 \rvert$ | $50 + 33 + 20 = 103$ |
    | $\lvert A_6 \rvert + \lvert A_{10} \rvert + \lvert A_{15} \rvert$ | $16 + 10 + 6 = 32$ |
    | $\lvert A_{30} \rvert$ | $3$ |
    | $\lvert A_2 \cup A_3 \cup A_5 \rvert$ | $103 - 32 + 3 = 74$ |

    Answer: $100 - 74 = 26$. (Sanity check: $\varphi(30)/30 \cdot 100 = \tfrac{8}{30} \cdot 100 \approx 26.7$.)

!!! example "Example 4 (intermediate): derangements"

    In how many orderings of $n$ items is **no** item in its original position? Let $A_i$ = permutations fixing item $i$; $|A_{i_1} \cap \cdots \cap A_{i_j}| = (n - j)!$. Inclusion–exclusion gives

    $$
    D_n = \sum_{j=0}^{n} (-1)^j \binom{n}{j} (n-j)! = n! \sum_{j=0}^{n} \frac{(-1)^j}{j!} \approx \frac{n!}{e}.
    $$

    Values: $D_0..D_7 = 1, 0, 1, 2, 9, 44, 265, 1854$. So a random permutation is a derangement with probability about $1/e \approx 0.368$ — a result reused in [Topic 1.3](topic3.md).

!!! example "Example 5 (advanced): pigeonhole and cycle detection"

    The sequence $x_{i+1} = f(x_i)$ on a finite set is eventually periodic: a **tail** of length $\mu$ followed by a **cycle** of length $\lambda$ (the shape of the letter $\rho$). For $f(x) = (x^2 + 1) \bmod 10$ and $x_0 = 3$: $3 \to 0 \to 1 \to 2 \to 5 \to 6 \to 7 \to 0 \to \cdots$, so $\mu = 1$ and $\lambda = 6$.

    A hash set finds $\mu, \lambda$ in $O(\mu + \lambda)$ time but also $O(\mu + \lambda)$ memory. **Floyd's tortoise and hare** uses $O(1)$ memory:

    1. *Meet.* Tortoise moves 1 step, hare 2 steps per tick. Once both are in the cycle, the gap shrinks by 1 (mod $\lambda$) per tick, so they meet; at the meeting time $i$, $2i \equiv i \pmod \lambda$, so $\lambda \mid i$.
    2. *Find $\mu$.* Reset the tortoise to $x_0$; move both 1 step per tick. After $\mu$ steps the tortoise is at $x_\mu$ and the hare is at position $i + \mu \equiv \mu \pmod \lambda$ in the cycle, also $x_\mu$. They first meet at the cycle entry.
    3. *Find $\lambda$.* Walk once around the cycle from $x_\mu$, counting steps.

    Applications: linked-list cycle detection (LeetCode 141/142, and 287 "Find the Duplicate Number"), the period of a pseudorandom generator, and Pollard's rho factorization (Floyd or Brent on $x \mapsto x^2 + c \bmod n$).

## Python Implementation

```python
import math

MOD = 10**9 + 7


def pascal_table(n, mod=None):
    """C[i][j] for 0 <= j <= i <= n, using only additions."""
    C = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        C[i][0] = 1
        for j in range(1, i + 1):
            C[i][j] = C[i - 1][j - 1] + C[i - 1][j]
            if mod is not None:
                C[i][j] %= mod
    return C


class Binomial:
    """O(n) precomputation, O(1) queries of nCr modulo a prime p > max_n."""

    def __init__(self, max_n, p=MOD):
        self.p = p
        self.fact = [1] * (max_n + 1)
        for i in range(1, max_n + 1):
            self.fact[i] = self.fact[i - 1] * i % p
        self.inv_fact = [1] * (max_n + 1)
        self.inv_fact[max_n] = pow(self.fact[max_n], p - 2, p)   # one Fermat inverse
        for i in range(max_n, 0, -1):
            self.inv_fact[i - 1] = self.inv_fact[i] * i % p

    def ncr(self, n, r):
        if r < 0 or r > n:
            return 0
        return self.fact[n] * self.inv_fact[r] % self.p * self.inv_fact[n - r] % self.p


def lucas(n, r, p):
    """nCr mod a small prime p, for arbitrarily large n."""
    result = 1
    while n > 0 or r > 0:
        ni, ri = n % p, r % p
        if ri > ni:
            return 0
        result = result * math.comb(ni, ri) % p
        n //= p
        r //= p
    return result


def count_not_divisible(n, primes):
    """How many x in [1, n] are divisible by none of the given primes."""
    k = len(primes)
    divisible_by_some = 0
    for mask in range(1, 1 << k):                # every non-empty subset of primes
        product = 1
        for i in range(k):
            if mask >> i & 1:
                product *= primes[i]
        term = n // product
        if bin(mask).count("1") % 2 == 1:
            divisible_by_some += term
        else:
            divisible_by_some -= term
    return n - divisible_by_some


def derangements(n):
    return sum((-1) ** j * math.comb(n, j) * math.factorial(n - j) for j in range(n + 1))


def catalan(n):
    return math.comb(2 * n, n) // (n + 1)


def floyd_cycle(f, x0):
    """Return (mu, lam): tail length and cycle length of x0, f(x0), f(f(x0)), ..."""
    tortoise, hare = f(x0), f(f(x0))
    while tortoise != hare:                      # phase 1: meet inside the cycle
        tortoise, hare = f(tortoise), f(f(hare))
    mu, tortoise = 0, x0
    while tortoise != hare:                      # phase 2: find the cycle entry
        tortoise, hare = f(tortoise), f(hare)
        mu += 1
    lam, hare = 1, f(tortoise)
    while tortoise != hare:                      # phase 3: walk once around
        hare = f(hare)
        lam += 1
    return mu, lam
```

**Walkthrough of the non-obvious lines**

- `Binomial.__init__` computes a single modular inverse, `fact[max_n]^(p-2)`, then walks downward using $((i-1)!)^{-1} = (i!)^{-1} \cdot i$. This turns $n$ exponentiations into one.
- `ncr` returns 0 for $r < 0$ or $r > n$; callers in DP code often pass such values at boundaries.
- `lucas` uses `math.comb` on digits smaller than $p$, which is exact; for repeated queries precompute a small Pascal table modulo $p$ instead.
- `count_not_divisible` enumerates subsets with a bitmask; the parity of the popcount decides the sign. The cost is $O(2^k \cdot k)$.
- `catalan` uses exact integer division: $(n+1) \mid \binom{2n}{n}$ always holds, so `//` is safe here (it is **not** safe on residues modulo $p$).
- `floyd_cycle` mirrors the three phases of Example 5.

All functions were verified against brute-force enumeration with `itertools` (Pascal and factorial methods vs `math.comb` for all $n \le 60$; Lucas for random $n \le 5000$; inclusion–exclusion and derangements vs direct counting; Catalan vs counting balanced strings; Floyd vs a hash-map simulation on random functions).

## Edge Cases and Pitfalls

| Case / pitfall | What goes wrong | Fix |
| --- | --- | --- |
| $\binom{n}{r}$ with $r > n$ or $r < 0$ | Index errors or negative factorial indices | Return 0 explicitly |
| $n \ge p$ in the factorial method | $n! \equiv 0 \pmod p$, inverse undefined, silently wrong answers | Use Lucas' theorem (small $p$) |
| Integer division of residues | `fact[n] // (fact[r] * fact[n-r])` after reducing mod $p$ is meaningless | Multiply by modular inverses |
| Computing $n!$ exactly then dividing (C++/Java) | $21!$ already overflows 64-bit | Pascal table, or multiplicative formula dividing as you go, or modular arithmetic |
| Double counting | Counting "choose leader then team" and "choose team then leader" as different when they are not | Check that each object corresponds to exactly one decision sequence; divide by the overcount factor |
| Inclusion–exclusion with large $k$ | $2^k$ terms explode | Restrict to distinct prime factors (at most 15 for numbers $\le 10^{18}$) or find structure |
| Overflow in products of primes in inclusion–exclusion | Product exceeds $n$ and overflows in C++ | Stop early when the product exceeds $n$ (its term is 0) |
| Fibonacci in 64-bit | $F_{93}$ overflows signed `long long`, $F_{94}$ overflows unsigned | Work modulo $p$ or use big integers |
| Empty cases | $\binom{0}{0} = 1$, $0! = 1$, $D_0 = 1$, $C_0 = 1$ | Treat empty selection as one valid object |

## Common Misconceptions

| Wrong belief | Correct mental model |
| --- | --- |
| "Combinations and permutations differ only in a formula." | They answer different questions; decide whether order matters **before** choosing a formula. $P(n,r) = r!\binom{n}{r}$. |
| "Pigeonhole tells me which box has the collision." | It is non-constructive: it guarantees existence only. Finding the collision is an algorithmic problem (hashing, cycle detection). |
| "Inclusion–exclusion is only for 2 or 3 sets." | It works for any $k$ sets; with bitmasks it is a $2^k$ loop. |
| "$2^n$ and $n!$ are both just 'exponential'." | $n! = 2^{\Theta(n \log n)}$ grows strictly faster; $n \le 20$ is fine for $2^n$ and hopeless for $n!$. |
| "Pascal's rule is just a formula." | It is a recurrence with overlapping subproblems — the textbook example motivating DP. |
| "A count modulo $p$ can be reduced and then divided." | Division needs inverses modulo a prime; reduce, then multiply by inverses. |

## Alternatives and Trade-offs

| Goal | Option | Cost | Use when | Avoid when |
| --- | --- | --- | --- | --- |
| Many $\binom{n}{r}$ queries, $n \le 10^6$ | Factorials + inverse factorials mod $p$ | $O(n)$ + $O(1)$/query | Prime modulus $p > n$ | Composite or small modulus |
| $\binom{n}{r}$ with any modulus, small $n$ | Pascal table | $O(n^2)$ | $n \le 5000$, non-prime modulus | $n$ large (memory) |
| Exact single $\binom{n}{r}$ | `math.comb` / multiplicative formula | $O(r)$ big-int ops | Exact answer needed | Many queries modulo $p$ |
| $\binom{n}{r} \bmod p$, $n$ huge, $p$ small | Lucas | $O(\log_p n)$ | $p \le 10^5$-ish prime | Large $p$ (digits are the whole number) |
| Count objects avoiding $k$ properties | Inclusion–exclusion | $O(2^k)$ | $k \le 20$ | Large $k$ without structure |
| Count via a recurrence | DP over the recurrence | states $\times$ transitions | No closed form or closed form hard to compute | Closed form exists and is cheap |
| Count by brute force | Enumerate with `itertools` | size of the space | Small cases, testing oracles | Real inputs |

## In Practice

- **Python**: `math.comb`, `math.perm`, `math.factorial` (exact big integers); `itertools.combinations`, `permutations`, `product` enumerate lazily — perfect as test oracles.
- **Software testing**: exhaustive testing of $k$ parameters with $v$ values needs $v^k$ cases. Combinatorial testing tools generate *covering arrays* so that every pair (or triple) of parameter values appears at least once, using far fewer tests — a direct application of counting.
- **Security**: password-space and key-space size ($62^8$, $2^{128}$) are product-rule counts; they determine whether exhaustive search is feasible.
- **Distributed systems / hashing**: pigeonhole guarantees collisions; designers reason about *how many* (expected collisions, birthday bound in [Topic 1.3](topic3.md)) rather than hoping for none.
- **ML and statistics**: the number of feature subsets ($2^d$) explains why exhaustive feature selection is replaced by greedy or regularized methods; binomial coefficients appear in binomial distributions and combinatorial kernels.
- **Compilers / query optimizers**: the number of join orders for $n$ relations grows like $n!$ (and bushy trees like $C_{n-1} \cdot n!$), so database optimizers use DP over subsets (System R style) or heuristics instead of enumeration.

## Interview and Competitive Programming

**Recognition cues**

| If you see... | Think... |
| --- | --- |
| "Number of ways ... modulo $10^9+7$" with $n \le 10^6$ | Precomputed factorials and inverse factorials |
| "Distribute $n$ identical items into $k$ boxes" | Stars and bars |
| "Grid paths moving only right/down" | $\binom{r + c}{r}$; obstacles $\to$ DP or inclusion–exclusion over obstacles |
| "Count integers in $[1, N]$ not divisible by any of ..." | Inclusion–exclusion with bitmask over the divisors |
| "Balanced", "non-crossing", "never below zero", answers $1, 2, 5, 14$ | Catalan |
| "Each step depends on previous one or two" | Fibonacci-like recurrence; huge $n$ $\to$ matrix power |
| "Prove some two elements share a property" | Pigeonhole |
| "Linked list cycle", "duplicate in array of $n+1$ values in $[1, n]$" | Floyd's tortoise and hare |

**Constraints to complexity**

| $n$ | Feasible brute force |
| --- | --- |
| $\le 10$ | $O(n!)$ permutations |
| $\le 20$ | $O(2^n \cdot n)$ subsets |
| $\le 40$ | Meet in the middle: $O(2^{n/2})$ |
| $\le 500$ | $O(n^3)$ |
| $\le 10^5$–$10^6$ | $O(n \log n)$ or $O(n)$ with precomputed factorials |

**Common traps:** forgetting that the answer must be reduced at every multiplication; using `long long` factorials beyond $20!$; counting ordered pairs when the problem asks for unordered ones (divide by 2, or iterate $i < j$).

## Using AI Assistants Critically

- LLMs frequently confuse "with repetition" and "without repetition", or ordered and unordered selection. Restate the problem precisely in your prompt and check the formula on a tiny case by hand.
- Generated `nCr` code often divides residues with `/` or `//`. Search for any division after a `% MOD`.
- Generated inverse-factorial loops are often off by one (`inv_fact[i] = inv_fact[i + 1] * (i + 1)` vs `* i`). Test `ncr(n, r) == math.comb(n, r) % MOD` for all $n \le 50$.
- Assistants sometimes claim a closed form that matches the first three or four terms but not later ones. Always compare against `itertools` brute force for $n$ up to 8–10.
- For inclusion–exclusion code, check the sign (odd-size subsets add, even-size subtract when computing the union) and the empty-set term.
- When an AI states "the number of states is polynomial so the DP is fast", count the states yourself; bitmask DPs have $2^n$ states.

## Practice

**Beginner**

1. *Licence plates.* Input: integers $L$ (letters) and $D$ (digits), $L, D \le 10$. Output: number of plates with $L$ letters followed by $D$ digits, with and without repetition. Difficulty: easy.
2. *Handshakes.* Input: $n \le 10^9$. Output: number of handshakes when every pair of $n$ people shakes hands once. Difficulty: easy.
3. *Pascal row.* Input: $n \le 60$. Output: row $n$ of Pascal's triangle, exactly. Difficulty: easy.

**Intermediate**

1. *Binomial queries.* Input: $Q \le 10^5$ queries $(n, r)$ with $0 \le r \le n \le 10^6$. Output: $\binom{n}{r} \bmod (10^9+7)$ for each. Difficulty: medium.
2. *Coprime count.* Input: $n \le 10^{12}$ and $N \le 10^{18}$. Output: number of $x \in [1, N]$ with $\gcd(x, n) = 1$. Difficulty: medium.
3. *Equal-sum block.* Input: $m \le 10^5$ integers. Output: a non-empty contiguous block whose sum is divisible by $m$ (prove one always exists). Difficulty: medium.

**Advanced**

1. *Grid paths with obstacles.* Input: an $H \times W$ grid ($H, W \le 10^5$) and $K \le 2000$ blocked cells. Output: number of right/down paths from top-left to bottom-right avoiding them, modulo $10^9+7$. Difficulty: hard.
2. *Huge binomial.* Input: $n, r \le 10^{18}$ and a prime $p \le 10^5$. Output: $\binom{n}{r} \bmod p$. Difficulty: medium–hard.
3. *Counting BST shapes.* Input: $n \le 10^6$. Output: number of distinct BSTs on keys $1..n$ modulo $10^9+7$, and a proof that your formula is correct. Difficulty: medium–hard.

**Interview / CP**

1. *Unique Paths* (LeetCode 62). Input: $m, n \le 100$. Output: number of right/down paths in an $m \times n$ grid. Difficulty: medium.
2. *Linked List Cycle II* (LeetCode 142). Input: head of a singly linked list. Output: the node where the cycle begins, or null, using $O(1)$ extra memory. Difficulty: medium.
3. *Distribute candies.* Input: $n \le 10^6$ identical candies, $k \le 10^6$ children, each child at most $c$ candies. Output: number of distributions modulo $10^9+7$. Difficulty: hard.

## Self-Check Questions

??? question "Q1. How many 8-bit strings contain exactly three 1s? How many contain at least one 1?"

    Exactly three: choose their positions, $\binom{8}{3} = 56$. At least one: complement of the all-zero string, $2^8 - 1 = 255$.

??? question "Q2. Give a combinatorial proof that $\sum_k \binom{n}{k} = 2^n$."

    Both sides count subsets of an $n$-set. The right side builds a subset by deciding include/exclude for each element (product rule). The left side groups subsets by size $k$ (sum rule over disjoint cases).

??? question "Q3. Why must any hash function from 64-bit keys to $2^{20}$ buckets have a bucket containing at least $2^{44}$ possible keys? What does this imply for worst-case hashing?"

    Generalized pigeonhole: $\lceil 2^{64}/2^{20} \rceil = 2^{44}$. An adversary who knows $h$ can choose all inserted keys from that bucket, making operations $\Theta(n)$. Defences: randomized (universal or keyed) hash functions, so the adversary cannot predict collisions.

??? question "Q4. A teammate computes $\binom{n}{r} \bmod 13$ for $n \le 10^6$ with factorials and Fermat inverses. When does this fail and what should be used?"

    For $n \ge 13$, $n!$ contains the factor 13, so $n! \equiv 0$ and the inverse factorials do not exist; the code returns 0 or garbage. Use Lucas' theorem (or Pascal's triangle modulo 13).

??? question "Q5. A problem has $n \le 18$ items and asks for the best ordering. Is $O(n!)$ feasible? What should you consider instead?"

    $18! \approx 6.4 \times 10^{15}$: infeasible. $O(2^n \cdot n^2) \approx 8.5 \times 10^7$ is feasible, which suggests bitmask DP over subsets (as in the Held–Karp TSP algorithm), where the state is "set of items placed so far, last item".

??? question "Q6. Use inclusion–exclusion to count integers in $[1, 60]$ divisible by 4 or 6."

    $\lfloor 60/4 \rfloor + \lfloor 60/6 \rfloor - \lfloor 60/\operatorname{lcm}(4,6) \rfloor = 15 + 10 - 5 = 20$. Note the intersection uses the **lcm** (12), not the product (24).

??? question "Q7. Why is the comparison-sorting lower bound $\Omega(n \log n)$? Which counting fact does it rely on?"

    A comparison sort's decision tree must distinguish all $n!$ input orderings, so it needs at least $n!$ leaves and height $\ge \log_2 n!$. By Stirling, $\log_2 n! = \Theta(n \log n)$. See [Unit 5.2](../unit5/topic2.md).

??? question "Q8. In Floyd's algorithm, why does resetting one pointer to $x_0$ and moving both one step at a time find the cycle entry?"

    At the first meeting time $i$, $\lambda \mid i$. After $\mu$ more single steps, the reset pointer is at $x_\mu$, and the other is at index $i + \mu$, which is in the cycle and congruent to $\mu$ modulo $\lambda$, so also at $x_\mu$. Before $\mu$ steps the reset pointer is still on the tail, where the other pointer never is, so the first meeting is exactly the entry.

## Complexity Summary

| Task | Time | Space |
| --- | --- | --- |
| Pascal's table up to $n$ | $O(n^2)$ | $O(n^2)$ (or $O(n)$ per row) |
| Factorial + inverse-factorial precomputation | $O(n + \log p)$ | $O(n)$ |
| $\binom{n}{r} \bmod p$ query after precomputation | $O(1)$ | — |
| Lucas' theorem | $O(\log_p n)$ digit binomials | $O(1)$ (or $O(p)$ tables) |
| Inclusion–exclusion over $k$ sets | $O(2^k \cdot k)$ | $O(1)$ |
| Catalan $C_n \bmod p$ | $O(1)$ after factorials | $O(n)$ |
| Floyd cycle detection | $O(\mu + \lambda)$ | $O(1)$ |
| Enumerate subsets / permutations | $O(2^n n)$ / $O(n!\, n)$ | $O(n)$ |

## Key Takeaways

- Decide order and distinguishability first; then the product, sum, bijection and complement rules handle most counts.
- Pascal's rule is a DP recurrence; factorials with inverse factorials give $O(1)$ binomials modulo a prime $p > n$; use Lucas when $p$ is small.
- Pigeonhole proves that collisions and cycles must exist — it explains unavoidable hash collisions and eventual periodicity.
- Inclusion–exclusion counts "avoid all bad properties" in $2^k$ terms; intersections of divisibility conditions use the lcm.
- The size of the search space is the cost of brute force: $2^n$ fits $n \le 20$, $n!$ fits $n \le 10$.
- $\log_2 n! = \Theta(n \log n)$ is the counting fact behind the sorting lower bound.
- Fibonacci and Catalan numbers are the two counting recurrences you must recognize on sight.
