# Unit 1 Summary

Revision sheet for [Number Theory](topic1.md), [Combinatorics](topic2.md), [Probability](topic3.md) and [Game Theory](topic4.md), plus the general mathematical toolkit (logarithms, sums, bit operations, proof techniques) used throughout the course. Asymptotic notation is covered in [Unit 2](../unit2/topic1.md) and recurrences (including the Master Theorem) in [Unit 3](../unit3/topic1.md).

## Key Results

### Number theory

| Result | Formula / statement | Cost |
| --- | --- | --- |
| Euclid | $\gcd(a, b) = \gcd(b, a \bmod b)$, $\gcd(a, 0) = a$ | $O(\log \min(a,b))$; worst case Fibonacci pairs |
| LCM | $\operatorname{lcm}(a,b) = \dfrac{a}{\gcd(a,b)} \cdot b$ | divide first to avoid overflow |
| Bézout / extended Euclid | $ax + by = \gcd(a,b)$; $x = y_1$, $y = x_1 - \lfloor a/b \rfloor y_1$ | $O(\log \min(a,b))$ |
| Modular rules | $+, -, \times$ commute with $\bmod m$; division does not | reduce after every operation |
| Inverse existence | $a^{-1} \bmod m$ exists $\iff \gcd(a, m) = 1$ | |
| Fermat | $p$ prime, $p \nmid a$: $a^{p-1} \equiv 1$, so $a^{-1} \equiv a^{p-2} \pmod p$ | $O(\log p)$ |
| Euler | $\gcd(a, m) = 1 \Rightarrow a^{\varphi(m)} \equiv 1 \pmod m$ | |
| Totient | $\varphi(n) = n \prod_{p \mid n}(1 - 1/p)$ | $O(\sqrt n)$ |
| Divisor count / sum | $n = \prod p_i^{e_i}$: $d(n) = \prod (e_i + 1)$, $\sigma(n) = \prod \frac{p_i^{e_i+1}-1}{p_i - 1}$ | |
| CRT | Pairwise coprime moduli: unique solution modulo $\prod m_i$ | $O(\log)$ per merge |
| Primality | Composite $n$ has a factor $\le \sqrt n$; primes $> 3$ are $6k \pm 1$ | $O(\sqrt n)$ — exponential in bits |
| Sieve of Eratosthenes | Cross out from $p^2$, only for $p \le \sqrt N$ | $O(N \log\log N)$ time, $O(N)$ space |
| Prime density | $\pi(n) \approx n / \ln n$ | |
| Modular power | Square-and-multiply ([Unit 4.6](../unit4/topic6.md)) | $O(\log e)$ |

### Combinatorics

| Count | Formula |
| --- | --- |
| Ordered, no repetition | $P(n, r) = \dfrac{n!}{(n-r)!}$ |
| Unordered, no repetition | $\dbinom{n}{r} = \dfrac{n!}{r!(n-r)!}$ |
| Ordered, with repetition | $n^r$ |
| Unordered, with repetition (stars and bars) | $\dbinom{n + r - 1}{r}$; solutions of $x_1 + \dots + x_k = n$, $x_i \ge 0$: $\dbinom{n+k-1}{k-1}$ |
| Multiset arrangements | $\dfrac{n!}{k_1! \cdots k_m!}$ |
| Circular arrangements | $(n-1)!$ |
| Pascal's rule | $\binom{n}{k} = \binom{n-1}{k-1} + \binom{n-1}{k}$ |
| Binomial theorem | $(x+y)^n = \sum_k \binom{n}{k}x^k y^{n-k}$; $\sum_k \binom{n}{k} = 2^n$ |
| Hockey stick | $\sum_{i=r}^{n}\binom{i}{r} = \binom{n+1}{r+1}$ |
| Pigeonhole | $n$ items in $m$ boxes: some box has $\ge \lceil n/m \rceil$ |
| Inclusion–exclusion | $\lvert \bigcup A_i \rvert = \sum \lvert A_i \rvert - \sum \lvert A_i \cap A_j \rvert + \cdots$ ($2^k - 1$ terms) |
| Derangements | $D_n = n!\sum_{j=0}^{n} (-1)^j/j! \approx n!/e$ |
| Fibonacci | $F_n = F_{n-1} + F_{n-2}$, $F_n = \Theta(\phi^n)$, $\phi \approx 1.618$ |
| Catalan | $C_n = \frac{1}{n+1}\binom{2n}{n}$: $1, 1, 2, 5, 14, 42, 132, \dots$ |
| Stirling | $n! \approx \sqrt{2\pi n}(n/e)^n$; $\log_2 n! = \Theta(n \log n)$ |
| $\binom{n}{r} \bmod p$ | Factorials + inverse factorials: $O(n)$ setup, $O(1)$ query ($p > n$ prime); Lucas for small $p$ |

### Probability

| Result | Statement |
| --- | --- |
| Complement / union bound | $\Pr[\overline A] = 1 - \Pr[A]$; $\Pr[\bigcup A_i] \le \sum \Pr[A_i]$ |
| Conditional / independence | $\Pr[A \mid B] = \Pr[A \cap B]/\Pr[B]$; independent iff $\Pr[A \cap B] = \Pr[A]\Pr[B]$ |
| Expectation | $E[X] = \sum_x x\Pr[X = x]$; $\operatorname{Var}[X] = E[X^2] - E[X]^2$ |
| Linearity | $E[\sum X_i] = \sum E[X_i]$ — **no independence needed** |
| Indicators | $E[I\{A\}] = \Pr[A]$, so $E[\text{count}] = \sum \Pr[\text{event}_i]$ |
| Bernoulli / Binomial | $E = p$ / $E = np$, $\operatorname{Var} = np(1-p)$ |
| Geometric | Trials to first success: $E = 1/p$ |
| Harmonic numbers | $H_n = \sum_{k=1}^n 1/k = \ln n + O(1)$ |
| Markov | $X \ge 0$: $\Pr[X \ge t] \le E[X]/t$ |
| Hiring problem | Random order: $E[\text{hires}] = H_n$ (worst case $n$) |
| Random permutation | $E[\text{fixed points}] = 1$; $E[\text{inversions}] = n(n-1)/4$ |
| Hashing ($n$ keys, $m$ buckets) | Chain length $n/m$; colliding pairs $\binom{n}{2}/m$; first collision likely after $\approx 1.18\sqrt m$ keys |
| Coupon collector | $nH_n = \Theta(n \log n)$ draws |
| Randomized quicksort | $E[\text{comparisons}] = 2(n+1)H_n - 4n = O(n\log n)$ ([Unit 5.4](../unit5/topic4.md)) |

### Game theory

| Result | Statement | Cost |
| --- | --- | --- |
| P/N rules | Terminal = P; N iff some move to P; P iff all moves to N | DP $O(\text{states} \times \text{moves})$ |
| Bouton (Nim) | P-position $\iff a_1 \oplus \cdots \oplus a_k = 0$; winning move: $a_i \to a_i \oplus s$ where $a_i \oplus s < a_i$ | $O(k)$ |
| Grundy number | $g(v) = \operatorname{mex}\{g(u) : v \to u\}$; P iff $g = 0$ | |
| Sprague–Grundy | $g(G_1 + \dots + G_k) = g(G_1) \oplus \dots \oplus g(G_k)$ | |
| Misère Nim | As Nim unless all piles $\le 1$; then mover wins iff the number of non-empty piles is even | $O(k)$ |
| Minimax | MAX takes max, MIN takes min of children | $O(b^d)$ |
| Alpha–beta | Same value; prune when $\alpha \ge \beta$ | $O(b^{d/2})$ best ordering, $O(b^d)$ worst |

### General toolkit: logarithms, exponents and sums

| Identity | Note |
| --- | --- |
| $a = b^{\log_b a}$ | definition |
| $\log_b(xy) = \log_b x + \log_b y$, $\log_b(x/y) = \log_b x - \log_b y$ | |
| $\log_b x^k = k\log_b x$, $\log_b(1/a) = -\log_b a$ | |
| $\log_b x = \dfrac{\log_c x}{\log_c b}$, $\log_b a = \dfrac{1}{\log_a b}$ | change of base: bases differ by a constant factor, so they do not matter inside $O(\cdot)$ |
| $a^{\log_b c} = c^{\log_b a}$ | used in the Master Theorem, e.g. $2^{\log_2 n} = n$, $4^{\log_2 n} = n^2$ |
| $\log^k n = (\log n)^k$, $\log\log n = \log(\log n)$ | notation |
| $a^m a^n = a^{m+n}$, $(a^m)^n = a^{mn}$, $a^{-n} = 1/a^n$, $a^0 = 1$ | |
| $\sum_{i=1}^n i = \frac{n(n+1)}{2}$ | arithmetic series; nested loops $i < j$ |
| $\sum_{i=1}^n i^2 = \frac{n(n+1)(2n+1)}{6}$, $\sum_{i=1}^n i^3 = \left(\frac{n(n+1)}{2}\right)^2$ | |
| $\sum_{i=0}^{n} r^i = \frac{r^{n+1}-1}{r-1}$ ($r \ne 1$); $\sum_{i \ge 0} r^i = \frac{1}{1-r}$ ($\lvert r \rvert < 1$) | geometric series: dominated by the largest term |
| $\sum_{i=1}^n \frac{1}{i} = \ln n + \gamma + O(1/n)$, $\gamma \approx 0.5772$ | harmonic series: hiring problem, divisor sieve $O(n \log n)$ |
| $\sum_{p \le n,\ p \text{ prime}} \frac{1}{p} = \ln\ln n + O(1)$ | gives the sieve's $O(n \log\log n)$ |

$\log_2 n$ counts how many times $n$ can be halved before reaching 1: the step count of binary search, the depth of balanced divide-and-conquer recursion, the number of bits of $n$, and the number of squarings in fast exponentiation.

### General toolkit: bit operations

| Operation | Python | Effect |
| --- | --- | --- |
| AND / XOR | `a & b`, `a ^ b` | bitwise; XOR is 1 where exactly one bit is 1 |
| OR | vertical-bar operator between `a` and `b` | 1 where at least one bit is 1 |
| Shifts | `a << k`, `a >> k` | multiply / floor-divide by $2^k$ (non-negative $a$) |
| XOR identities | `a ^ a == 0`, `a ^ 0 == a`; commutative and associative | Nim-sum; cancelling pairs |
| Power of two test | `n > 0 and n & (n - 1) == 0` | |
| Lowest set bit | `n & -n` | Fenwick trees |
| Popcount | `bin(n).count("1")` or `n.bit_count()` (3.10+) | inclusion–exclusion sign |
| Subset enumeration | `for mask in range(1 << n)` | $2^n$ subsets; bitmask DP |

### General toolkit: proof techniques

| Technique | Shape | Used in this unit for |
| --- | --- | --- |
| Direct proof | Assume premises, derive conclusion | Euclid's lemma $\gcd(a,b) = \gcd(b, a \bmod b)$ |
| Contradiction | Assume the negation, derive an impossibility | Small-factor lemma ($n$ composite has a factor $\le \sqrt n$) |
| Induction | Base case + step (or strong induction) | P/N classification; extended Euclid correctness |
| Combinatorial (double counting / bijection) | Count one set two ways | Pascal's rule, $\sum \binom{n}{k} = 2^n$, Catalan reflection |
| Loop invariant | Initialization, maintenance, termination | Euclid: the gcd of the current pair never changes |
| Invariant-set argument | Show a set satisfies the defining properties | Bouton's theorem for Nim |

## Important for Exams

!!! warning "Classic mistakes"

    - Dividing under a modulus. Replace $a/b$ by $a \cdot b^{-1}$, and check that $\gcd(b, m) = 1$.
    - Using Fermat's $a^{m-2}$ with a composite $m$. Fermat needs a prime modulus; extended Euclid works whenever $\gcd(a, m) = 1$.
    - Calling $O(\sqrt n)$ trial division "polynomial". Input size is $\log n$ bits, so $\sqrt n$ is exponential.
    - Using the factorial method for $\binom{n}{r} \bmod p$ with $n \ge p$. Use Lucas' theorem.
    - Confusing ordered and unordered selections ($P(n,r)$ vs $\binom{n}{r}$), or distinguishable and identical objects.
    - Intersecting divisibility sets with the product instead of the **lcm** in inclusion–exclusion.
    - Thinking linearity of expectation needs independence. It does not; $E[XY] = E[X]E[Y]$ does.
    - Mixing up average-case analysis (random input) with the expected running time of a randomized algorithm (random choices, any input).
    - XOR-ing win/lose results instead of Grundy numbers when games are summed.

**Proofs you should be able to reproduce:**

1. $\gcd(a, b) = \gcd(b, a \bmod b)$ and the $O(\log n)$ bound (halving every two steps).
2. Extended Euclid's update $x = y_1$, $y = x_1 - \lfloor a/b \rfloor y_1$.
3. The inverse of $a$ modulo $m$ exists iff $\gcd(a, m) = 1$.
4. Pascal's rule and stars and bars (combinatorial proofs).
5. Linearity of expectation, and the hiring problem's $E[\text{hires}] = H_n$.
6. Bouton's theorem for Nim.

## Choosing the Right Technique

| The problem says or implies... | Reach for | Topic |
| --- | --- | --- |
| Answer is huge; "print modulo $10^9+7$" | Modular arithmetic; inverses for division | [1.1](topic1.md) |
| Divisibility, common divisors, "make all equal by steps of $d$" | gcd / lcm, Euclid | [1.1](topic1.md) |
| Many primality or factorization queries on small numbers | Sieve / SPF sieve | [1.1](topic1.md) |
| $ax + by = c$, modular inverse with non-prime modulus | Extended Euclid | [1.1](topic1.md) |
| "How many ways ...", choose / arrange | Product and sum rules, binomials, factorial tables | [1.2](topic2.md) |
| "None of these bad properties" | Complement + inclusion–exclusion | [1.2](topic2.md) |
| "Prove some two must coincide" | Pigeonhole | [1.2](topic2.md) |
| Can brute force work? | Count the search space ($2^n$, $n!$, $\binom{n}{k}$) | [1.2](topic2.md) |
| "Expected number of ..." | Indicators + linearity | [1.3](topic3.md) |
| "Repeat until success" | Geometric distribution, $1/p$ | [1.3](topic3.md) |
| Collisions in hashing / IDs | Birthday bound $\approx \sqrt m$ | [1.3](topic3.md) |
| Two players, perfect play, win/lose | P/N DP; Nim / Grundy for impartial sums | [1.4](topic4.md) |
| Two players, scores or different move sets | Minimax, alpha–beta | [1.4](topic4.md) |

**How the topics connect:** number theory supplies the inverses that make modular binomials possible; combinatorics supplies the sizes of sample spaces that probability divides by; probability supplies expectations for randomized algorithms; game theory reuses XOR and dynamic programming over states. When a problem mixes them (e.g. "expected value modulo $998\,244\,353$"), compute the exact rational answer with probability and combinatorics, then convert with a modular inverse.

## Mixed Practice

??? question "Q1. Compute $7^{-1} \bmod 26$. Which method can you use, and why not Fermat?"

    $\gcd(7, 26) = 1$, so the inverse exists. 26 is not prime, so Fermat's $a^{m-2}$ does not apply; use extended Euclid: $26 = 3 \cdot 7 + 5$, $7 = 1 \cdot 5 + 2$, $5 = 2 \cdot 2 + 1$; back-substituting gives $7 \cdot 15 - 26 \cdot 4 = 1$. So $7^{-1} \equiv 15$ (check: $105 = 4 \cdot 26 + 1$).

??? question "Q2. How many integers in $[1, 1000]$ are coprime to 1000? Solve it two ways."

    Totient: $1000 = 2^3 5^3$, so $\varphi(1000) = 1000 \cdot \tfrac12 \cdot \tfrac45 = 400$. Inclusion–exclusion: $1000 - (500 + 200) + 100 = 400$.

??? question "Q3. How many ways can 10 identical jobs be assigned to 4 distinct servers? What if each server must get at least one?"

    Stars and bars: $\binom{10 + 3}{3} = 286$. With at least one each: $\binom{9}{3} = 84$.

??? question "Q4. A problem has $n = 12$ and asks for the best ordering of all items. Is $O(n!)$ brute force feasible in about a second? What about $n = 20$?"

    $12! = 479{,}001{,}600 \approx 4.8 \times 10^8$: borderline — probably too slow in Python, feasible in C++ with a cheap check. $20! \approx 2.4 \times 10^{18}$: impossible; look for an $O(2^n n^2)$ bitmask DP instead.

??? question "Q5. What is the probability that a random permutation of 4 elements has no fixed point? What is the expected number of fixed points?"

    $D_4 = 9$, so $9/24 = 3/8$. The expected number of fixed points is $1$ (linearity: $4 \times \tfrac14$), even though the events are dependent.

??? question "Q6. $n$ keys are hashed uniformly into $n$ buckets. What is the expected number of empty buckets?"

    Indicator per bucket: empty with probability $(1 - 1/n)^n$. So $E = n(1 - 1/n)^n \approx n/e \approx 0.368n$. For $n = 10$: $10 \cdot 0.9^{10} \approx 3.49$.

??? question "Q7. A system issues 48-bit random IDs. About how many IDs can it issue before a collision has probability $1/2$?"

    Birthday bound with $m = 2^{48}$: $n \approx 1.18\sqrt{m} = 1.18 \cdot 2^{24} \approx 2 \times 10^7$ IDs.

??? question "Q8. Express the expected value of a fair six-sided die modulo $p = 998\,244\,353$."

    $E = 7/2$. Modulo $p$: $7 \cdot 2^{-1} \bmod p$. Since $2^{-1} \equiv 499\,122\,177$, the answer is $7 \cdot 499\,122\,177 \bmod p = 499\,122\,180$. This combines probability with modular inverses.

??? question "Q9. Who wins Nim $(2, 5, 6)$, and with which move?"

    $2 \oplus 5 \oplus 6 = 1 \ne 0$: the first player wins. The highest set bit of 1 is bit 0; pile 5 (`101`) has it, and $5 \oplus 1 = 4$. Remove 1 stone from the pile of 5 to reach $(2, 4, 6)$, whose nim-sum is 0.

??? question "Q10. A move removes 1 or 2 stones; the player taking the last stone wins. Who wins with $n = 10^{18}$ stones?"

    By backward induction the P-positions are $n \equiv 0 \pmod 3$. $10^{18} \equiv 1 \pmod 3$, so the first player wins by removing 1 stone, leaving a multiple of 3, and then always restoring a multiple of 3.

??? question "Q11. Which pair $(a, b)$ with $1 \le b \le a \le 100$ maximizes the number of steps of Euclid's algorithm, and why?"

    $(89, 55)$, consecutive Fibonacci numbers, with 9 steps. All quotients are 1, so remainders shrink as slowly as possible (Lamé's theorem).

??? question "Q12. Why does sorting by comparisons need $\Omega(n \log n)$ comparisons, and which result from this unit does the proof use?"

    A comparison sort is a binary decision tree that must have at least $n!$ leaves (one per input ordering), so its height is at least $\log_2 n!$. Stirling's approximation gives $\log_2 n! = \Theta(n \log n)$. The proof uses counting ([Topic 1.2](topic2.md)); the full argument is in [Unit 5.2](../unit5/topic2.md).
