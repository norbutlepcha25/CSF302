# Unit 2 Summary

## Key Results

### Measuring cost ([2.1](topic1.md), [2.2](topic2.md))

| Concept | Key fact |
|---|---|
| Running time $T(n)$ | number of basic operations on inputs of size $n$, under a stated model and case |
| Input size | elements for collections; $V$ and $E$ for graphs; **bits** for numbers |
| Worst / best / average case | $\max$ / $\min$ / expectation (under a stated distribution) over inputs of size $n$ |
| Doubling experiment | $T(2n)/T(n) \to 2^k$ indicates $\Theta(n^k)$ |
| Word-RAM unit cost | arithmetic, comparison, bitwise ops, memory access on one $w$-bit word; $w \ge \lg n$ |
| Not unit cost | $b$-bit integers ($\Theta(b/w)$ add, $\Theta((b/w)^2)$ schoolbook multiply), strings of length $L$ ($\Theta(L)$) |
| Pseudo-polynomial | polynomial in a numeric value (e.g. $\Theta(nW)$), exponential in input bits |
| I/O model | scan $\Theta(N/B)$ I/Os; B-tree search $\Theta(\log_B N)$ I/Os |

### Notation ([2.5](topic5.md))

| Notation | Definition (for all $n \ge n_0$) | Limit of $f/g$ |
|---|---|---|
| $f = O(g)$ | $\exists c > 0$: $0 \le f \le c\,g$ | $< \infty$ |
| $f = \Omega(g)$ | $\exists c > 0$: $0 \le c\,g \le f$ | $> 0$ |
| $f = \Theta(g)$ | $\exists c_1, c_2 > 0$: $c_1 g \le f \le c_2 g$ | $0 < L < \infty$ |
| $f = o(g)$ | $\forall c > 0$: $f < c\,g$ | $0$ |
| $f = \omega(g)$ | $\forall c > 0$: $f > c\,g$ | $\infty$ |

Properties: transitivity (all five); reflexivity ($O, \Omega, \Theta$); $\Theta$ symmetric; $f = O(g) \iff g = \Omega(f)$; $f + g = \Theta(\max(f, g))$; polynomials of degree $d$ are $\Theta(n^d)$.

### Functions ([2.6](topic6.md))

| Fact | Formula |
|---|---|
| Change of base | $\log_a n = \log_b n / \log_b a$, so bases do not matter in $O$ |
| Exponent swap | $a^{\log_b c} = c^{\log_b a}$; e.g. $3^{\lg n} = n^{\lg 3}$ |
| Polylog vs poly vs exp | $\lg^b n = o(n^a)$, $n^b = o(c^n)$ for $a > 0$, $c > 1$ |
| Factorial | $\lg(n!) = \Theta(n \lg n)$; Stirling $n! = \sqrt{2\pi n}(n/e)^n(1 + \Theta(1/n))$ |
| Harmonic | $H_n = \ln n + O(1)$ |
| Iterated log | $\lg^* n \le 5$ for $n \le 2^{65536}$ |
| Floors/ceilings | $\lceil n/2 \rceil + \lfloor n/2 \rfloor = n$; bits of $n$ $= \lfloor \lg n \rfloor + 1$ |
| Hierarchy | $1 \prec \lg^* n \prec \lg\lg n \prec \lg n \prec \sqrt n \prec n \prec n \lg n \prec n^2 \prec 2^n \prec n! \prec n^n$ |

### Design and correctness ([2.3](topic3.md), [2.4](topic4.md))

| Item | Key fact |
|---|---|
| Hardware vs algorithm | $k$× faster hardware: feasible $n$ grows $k$× for $n$, $\sqrt k$× for $n^2$, $+\lg k$ for $2^n$ |
| Worked example | $n = 10^9$: $2n^2$ at $10^{10}$ ops/s ≈ 6.3 years; $50 n \lg n$ at $10^7$ ops/s ≈ 42 hours |
| Loop invariant | Initialization, Maintenance, Termination |
| Insertion sort | best $\Theta(n)$, worst/avg $\Theta(n^2)$, $\Theta(n + I)$ with $I$ inversions, in place, stable |
| Time–space trade-off | hashing, prefix sums, memoisation buy time with memory |

## Important for Exams

!!! warning "Classic mistakes"

    - **$O$ is not "worst case".** $O$, $\Omega$, $\Theta$ bound functions; best/worst/average case choose which function. "The best case of insertion sort is $\Theta(n)$" is correct and meaningful.
    - **"Insertion sort is $\Omega(n^2)$" is false** (sorted inputs take $\Theta(n)$); "its worst-case running time is $\Omega(n^2)$" is true.
    - **Always give both $c$ and $n_0$** when proving a bound; $c$ must not depend on $n$.
    - **$\Theta$ needs two proofs**, the upper and the lower bound.
    - **"=" in $f = O(g)$ means membership** and is one-directional.
    - **Exponential bases matter** ($2^n \ne \Theta(4^n)$); **logarithm bases do not**.
    - **Input size for numbers is the number of bits**: $\Theta(\sqrt N)$ trial division and $\Theta(nW)$ subset-sum DP are not polynomial.
    - **Loop invariant answers need all three parts**, and the invariant must be strong enough to give the result at termination (for sorting: "sorted" and "same elements").
    - **Average case requires a stated input distribution.**
    - **Big-integer arithmetic is not $O(1)$** on the Word-RAM.

## Choosing the Right Technique

| You need to... | Use | Topic |
|---|---|---|
| estimate how a loop-based algorithm scales | step counting with sums | [2.1](topic1.md) |
| check whether an implementation matches its claimed complexity | doubling experiment | [2.1](topic1.md) |
| decide if arithmetic can be treated as $O(1)$ | Word-RAM rules; count bits when values grow | [2.2](topic2.md) |
| justify spending effort on a better algorithm | feasibility table, crossover point | [2.3](topic3.md) |
| design a new algorithm | workflow: baseline → bottleneck → property → paradigm | [2.4](topic4.md) |
| prove an iterative algorithm correct | loop invariant (Init/Maint/Term) | [2.4](topic4.md) |
| prove $f = O/\Omega/\Theta(g)$ | explicit $c, n_0$; or the limit test | [2.5](topic5.md) |
| show $f \ne O(g)$ | contradiction ($n \le c$ for all large $n$) | [2.5](topic5.md) |
| rank unusual functions | take logs, substitute $n = 2^m$, use identities | [2.6](topic6.md) |
| solve a recursive cost | recurrences | [Unit 3](../unit3/overview.md) |

| Statement type | Best notation |
|---|---|
| guarantee that holds on every input | $O$ on the running time, or $\Theta$ on the worst case |
| exact order of a specific case | $\Theta$ with the case named |
| no algorithm can do better | $\Omega$ for the problem (lower bound) |
| one function strictly dominates another | $o$ / $\omega$ |
| same order, compare leading constants | tilde ($\sim n^2/2$ vs $\sim n^2/4$) |

## Mixed Practice

??? question "Q1. Prove $7n^2 - 10n + 3 = \Theta(n^2)$ with explicit constants."

    Upper: for $n \ge 1$, $7n^2 - 10n + 3 \le 7n^2 + 3n^2 = 10n^2$. Lower: $7n^2 - 10n + 3 \ge 7n^2 - 10n \ge 2n^2$ when $5n^2 \ge 10n$, i.e. $n \ge 2$. So $c_1 = 2$, $c_2 = 10$, $n_0 = 2$.

??? question "Q2. A function's doubling ratios are 7.9, 8.0, 8.1. What growth is suggested, and how would you confirm it?"

    $\log_2 8 = 3$: cubic, $\Theta(n^3)$. Confirm by step counting the code (look for three nested loops over $n$) and, if possible, prove matching upper and lower bounds.

??? question "Q3. Is computing $2^n$ by repeated doubling in Python a $\Theta(n)$ algorithm?"

    It performs $n$ doublings, but the $k$-th value has $k$ bits, so each doubling costs $\Theta(k/w)$ word operations. The total is $\Theta(n^2/w)$ under the Word-RAM; only in a unit-cost model counting doublings is it $\Theta(n)$.

??? question "Q4. Rank: $n \lg n$, $\lg(n!)$, $n^{1.5}$, $2^{\lg n}$, $4^{\lg n}$, $(\lg n)^3$."

    $2^{\lg n} = n$, $4^{\lg n} = n^2$, $\lg(n!) = \Theta(n \lg n)$. Order: $(\lg n)^3 \prec n \prec n \lg n \asymp \lg(n!) \prec n^{1.5} \prec n^2$.

??? question "Q5. State and prove the loop invariant for computing the maximum of $A[1..n]$ with `m ← A[1]; for i ← 2 to n: if A[i] > m then m ← A[i]`."

    Invariant: at the start of iteration $i$, $m = \max(A[1..i-1])$. Initialization: $i = 2$, $m = A[1] = \max(A[1..1])$. Maintenance: after comparing with $A[i]$, $m = \max(\max(A[1..i-1]), A[i]) = \max(A[1..i])$. Termination: $i = n + 1$, so $m = \max(A[1..n])$.

??? question "Q6. A machine becomes 64 times faster. How does the feasible $n$ change for algorithms with costs $n^2$, $n^3$, and $2^n$?"

    $n^2$: $\sqrt{64} = 8$× larger. $n^3$: $\sqrt[3]{64} = 4$× larger. $2^n$: $\lg 64 = 6$ more items.

??? question "Q7. Explain why 'Big-O is the worst case' is wrong, using linear search."

    Linear search's best case is $\Theta(1)$ and its worst case $\Theta(n)$. We can say "the best case is $O(1)$" (an upper bound on the best-case function) and "the worst case is $\Omega(n)$" (a lower bound on the worst-case function). Notation and case are independent choices.

??? question "Q8. Is an $O(n \cdot K)$ algorithm, where $K$ is an input number, polynomial time?"

    Not in general. $K$ takes $\Theta(\lg K)$ bits, so $nK$ can be exponential in the input length. It is pseudo-polynomial; it is polynomial only if $K$ is bounded by a polynomial in the input size.

??? question "Q9. Two loops each perform $n^2$ additions over the same matrix, one row-wise, one column-wise. The column-wise loop is 5× slower. Which model explains this?"

    Not the Word-RAM, which charges all memory accesses equally. The memory hierarchy (caches, cache lines) explains it; the external-memory/I-O model or cache-aware analysis captures it.

??? question "Q10. You need $q = 10^5$ range-sum queries on a fixed array of $n = 10^5$ elements. Compare the naive approach with prefix sums."

    Naive: $\Theta(n)$ per query, $\Theta(nq) = 10^{10}$ operations in the worst case: too slow. Prefix sums: $\Theta(n)$ preprocessing and $\Theta(n)$ extra memory, then $\Theta(1)$ per query, total $\Theta(n + q)$. A classic time–space trade-off.

??? question "Q11. Prove $\lg(n!) = O(n \lg n)$ and $\lg(n!) = \Omega(n \lg n)$."

    $n! \le n^n$ gives $\lg(n!) \le n \lg n$. At least $n/2$ factors are $\ge n/2$, so $\lg(n!) \ge \frac n2 \lg \frac n2 \ge \frac n4 \lg n$ for $n \ge 4$.

??? question "Q12. Does the limit test fail for $f(n) = n(2 + \cos n)$ and $g(n) = n$? What is the relationship?"

    $f/g = 2 + \cos n$ oscillates between 1 and 3, so the limit does not exist and the test gives no answer. Directly, $n \le f(n) \le 3n$, so $f = \Theta(n)$.
