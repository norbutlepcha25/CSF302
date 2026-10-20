# Standard Notation and Common Functions

!!! abstract "At a glance"

    - **Purpose:** the vocabulary of functions that appear in running times: polynomials, logarithms, exponentials, floors and ceilings, factorials, binomial coefficients, harmonic numbers, and the iterated logarithm.
    - **Most-used facts:** log base changes cost only a constant factor; $a^{\log_b c} = c^{\log_b a}$; $\lg(n!) = \Theta(n \lg n)$; $H_n = \ln n + O(1)$; $\lg^* n \le 5$ for any realistic $n$.
    - **Growth hierarchy:** $1 \prec \lg^* n \prec \lg \lg n \prec \lg n \prec \sqrt{n} \prec n \prec n \lg n \prec n^2 \prec 2^n \prec n! \prec n^n$.
    - **Use:** simplifying cost expressions, solving recurrences ([Unit 3](../unit3/overview.md)), and comparing algorithms quickly.

## Motivation and Problem Context

Analysing real algorithms produces expressions such as $\sum_{k=1}^{n} \frac{1}{k}$ (quicksort), $\lg(n!)$ (the sorting lower bound), $n^{\log_2 3}$ (Karatsuba), $T(\lceil n/2 \rceil) + T(\lfloor n/2 \rfloor)$ (merge sort), or $\lg^* n$ (union-find). To compare algorithms you must know how each such function grows and how to simplify it. This topic is the reference toolkit; [2.5](topic5.md) supplies the notation used to state the results.

## Problem Formulation

- **Given:** an expression arising from step counting or a recurrence.
- **Goal:** rewrite it into a simple representative $g(n)$ with $f = \Theta(g)$, and place $g$ in the growth hierarchy.
- **Conventions in this course:** $\lg n = \log_2 n$, $\ln n = \log_e n$, $\lg^k n = (\lg n)^k$, $\lg \lg n = \lg(\lg n)$. Logarithms in $O$-expressions may omit the base.

## Intuition

Each family of functions corresponds to a kind of computation:

| Function | Arises from |
|---|---|
| $\lg n$ | repeatedly halving (binary search, tree height, number of bits) |
| $n$ | touching every element once |
| $n \lg n$ | $\lg n$ levels of linear work (merge sort), or sorting as a preprocessing step |
| $n^k$ | $k$ nested loops over the input |
| $2^n$ | all subsets |
| $n!$ | all orderings |
| $H_n \approx \ln n$ | summing $1/k$: probabilities of "new minimum", expected work in randomised algorithms |
| $\lg^* n$ | repeatedly taking logarithms: extremely slowly growing data-structure bounds |

## Definitions and Key Results

### Monotonicity

$f$ is **monotonically increasing** if $m \le n \Rightarrow f(m) \le f(n)$, and **strictly increasing** if $m < n \Rightarrow f(m) < f(n)$ (similarly for decreasing). Running-time functions are normally assumed monotonically increasing, which justifies statements like "if $n \le 2^k$, then $T(n) \le T(2^k)$" used when rounding $n$ up to a power of 2.

### Floors and ceilings

$\lfloor x \rfloor$ is the greatest integer $\le x$; $\lceil x \rceil$ is the least integer $\ge x$.

| Fact | Statement |
|---|---|
| Sandwich | $x - 1 < \lfloor x \rfloor \le x \le \lceil x \rceil < x + 1$ |
| Halves | $\lceil n/2 \rceil + \lfloor n/2 \rfloor = n$ for integer $n$ |
| Nesting | $\lceil \lceil n/a \rceil / b \rceil = \lceil n/(ab) \rceil$ and $\lfloor \lfloor n/a \rfloor / b \rfloor = \lfloor n/(ab) \rfloor$ for integers $a, b > 0$ |
| Integer division bounds | $\lceil a/b \rceil \le (a + b - 1)/b$ and $\lfloor a/b \rfloor \ge (a - b + 1)/b$ |
| Bits | a positive integer $n$ has $\lfloor \lg n \rfloor + 1$ binary digits |
| Modulo | $a \bmod n = a - n \lfloor a/n \rfloor$, so $0 \le a \bmod n < n$ for $n > 0$ |

Where they appear: merge sort splits into $\lceil n/2 \rceil$ and $\lfloor n/2 \rfloor$; binary search computes $\lfloor (lo + hi)/2 \rfloor$; a loop that halves $n$ runs $\lfloor \lg n \rfloor$ times ([2.1](topic1.md)). The nesting identity justifies treating "$n/4$" in recurrences as $n/2$ applied twice.

!!! warning "Important"

    In asymptotic analysis, floors and ceilings almost never change the order of growth: $T(\lceil n/2 \rceil)$ and $T(n/2)$ lead to the same $\Theta$ bound for standard recurrences, which is why we often ignore them when solving recurrences ([Unit 3](../unit3/overview.md)). In **code**, however, they matter: an off-by-one in a ceiling causes infinite loops and missed elements.

### Polynomials

A polynomial of degree $d$ is $p(n) = \sum_{i=0}^{d} a_i n^i$ with $a_d \ne 0$. If $a_d > 0$ then $p(n) = \Theta(n^d)$ (proved in [2.5](topic5.md)). A function is **polynomially bounded** if $f(n) = O(n^k)$ for some constant $k$; polynomially bounded running times are the usual formal meaning of "efficient".

### Exponentials

For $a > 0$ and integers $m, n$: $a^0 = 1$, $a^{m+n} = a^m a^n$, $(a^m)^n = a^{mn}$, $a^{-1} = 1/a$.

**Key result: every exponential beats every polynomial.** For constants $a > 1$ and $b$:

$$
\lim_{n \to \infty} \frac{n^b}{a^n} = 0, \qquad\text{so}\qquad n^b = o(a^n).
$$

Even $n^{100}$ is eventually smaller than $1.01^n$. Also useful: $e^x \ge 1 + x$ for all real $x$, and $\left(1 + \frac{x}{n}\right)^n \to e^x$.

Different bases give different classes: $2^n = o(3^n)$, since $(2/3)^n \to 0$. Contrast with logarithms below, where the base does not matter.

### Logarithms

For $a, b, c > 0$ with bases $\ne 1$:

| Identity | Use in analysis |
|---|---|
| $a = b^{\log_b a}$ | converting between exponential and logarithmic forms |
| $\log(ab) = \log a + \log b$ | logs of products, e.g. $\lg(n!) = \sum \lg k$ |
| $\log(a/b) = \log a - \log b$ | |
| $\log_b a^n = n \log_b a$ | pulling exponents out: $\lg(n^3) = 3 \lg n$ |
| $\log_b a = \dfrac{\log_c a}{\log_c b}$ | **change of base**: all log bases are within a constant factor |
| $\log_b (1/a) = -\log_b a$ | |
| $\log_b a = \dfrac{1}{\log_a b}$ | |
| $a^{\log_b c} = c^{\log_b a}$ | rewriting $a^{\log_b n} = n^{\log_b a}$: the leaf count in the Master Theorem |

*Proof of the last identity.* Take $\log_b$ of both sides: $\log_b c \cdot \log_b a = \log_b a \cdot \log_b c$. $\blacksquare$

Consequences:

- **Base does not matter in $O$:** $\log_a n = \Theta(\log_b n)$ for constants $a, b > 1$.
- **Exponent inside vs outside:** $\lg(n^k) = k \lg n = \Theta(\lg n)$, but $\lg^k n = (\lg n)^k$ is a different, larger class for $k > 1$.
- **Polylogarithms lose to polynomials:** for constants $a > 0$ and $b$, $\lg^b n = o(n^a)$ (substitute $n = 2^m$ and use the exponential result). So $\lg^{100} n = o(n^{0.01})$.
- **Recursion trees:** a divide-and-conquer recurrence $T(n) = aT(n/b) + f(n)$ has depth $\log_b n$ and $a^{\log_b n} = n^{\log_b a}$ leaves; this is the quantity compared against $f(n)$ in the [Master Theorem](../unit3/topic5.md). For Karatsuba, $3^{\lg n} = n^{\lg 3} \approx n^{1.585}$.

### Factorials

$n! = 1 \cdot 2 \cdots n$, with $0! = 1$. Bounds:

- $n! \le n^n$, so $n! = O(n^n)$, and in fact $n! = o(n^n)$.
- $n! \ge 2^{n-1}$, and $n! = \omega(2^n)$.
- **Stirling's approximation:** $n! = \sqrt{2\pi n}\left(\dfrac{n}{e}\right)^n \left(1 + \Theta\!\left(\dfrac{1}{n}\right)\right)$.

**Key result: $\lg(n!) = \Theta(n \lg n)$.**

*Elementary proof.* Upper: $n! \le n^n$ gives $\lg(n!) \le n \lg n$. Lower: the largest $\lceil n/2 \rceil$ factors are each at least $n/2$, so $n! \ge (n/2)^{n/2}$ and $\lg(n!) \ge \frac{n}{2}\lg\frac{n}{2} = \frac{n}{2}(\lg n - 1) \ge \frac{n}{4}\lg n$ for $n \ge 4$. $\blacksquare$

Stirling gives the sharper $\lg(n!) = n \lg n - n \lg e + O(\lg n) \approx n \lg n - 1.44 n$. This is exactly the comparison-sorting lower bound: any comparison sort needs at least $\lceil \lg(n!) \rceil = \Omega(n \lg n)$ comparisons in the worst case ([5.2](../unit5/topic2.md)).

### Binomial coefficients

$\binom{n}{k} = \frac{n!}{k!(n-k)!}$ counts $k$-subsets of an $n$-set. Useful bounds for $1 \le k \le n$:

$$
\left(\frac{n}{k}\right)^k \le \binom{n}{k} \le \left(\frac{en}{k}\right)^k, \qquad \sum_{k=0}^{n} \binom{n}{k} = 2^n, \qquad \binom{n}{n/2} = \Theta\!\left(\frac{2^n}{\sqrt{n}}\right).
$$

For fixed $k$, $\binom{n}{k} = \Theta(n^k)$: checking all pairs is $\Theta(n^2)$, all triples $\Theta(n^3)$. Brute force over all subsets is $\Theta(2^n)$. Counting arguments are developed in [Unit 1](../unit1/overview.md).

### Harmonic numbers

$$
H_n = \sum_{k=1}^{n} \frac{1}{k} = \ln n + O(1), \qquad \ln(n+1) \le H_n \le \ln n + 1.
$$

*Proof sketch.* Compare the sum with $\int \frac{dx}{x}$: each term $\frac1k$ lies between $\int_k^{k+1}\frac{dx}{x}$ and $\int_{k-1}^{k}\frac{dx}{x}$. More precisely $H_n - \ln n \to \gamma \approx 0.5772$ (Euler's constant).

Where it appears: randomised quicksort's expected comparison count is $2(n+1)H_n - 4n \approx 2n \ln n \approx 1.39\, n \lg n$ ([5.4](../unit5/topic4.md)); the expected number of times the running maximum changes in a random permutation is $H_n$; the coupon collector needs $n H_n$ draws in expectation.

### Iterated logarithm

$\lg^* n$ is the number of times $\lg$ must be applied, starting from $n$, before the result is at most 1.

| $n$ | $\lg^* n$ |
|---|---|
| 1 | 0 |
| 2 | 1 |
| 3, 4 | 2 |
| 5 to 16 | 3 |
| 17 to 65,536 | 4 |
| 65,537 to $2^{65536}$ | 5 |

Since $2^{65536}$ vastly exceeds the number of atoms in the observable universe (about $10^{80}$), $\lg^* n \le 5$ for every input you will ever process, yet $\lg^* n = \omega(1)$. It appears in bounds for union-find with path compression (the classic Hopcroft–Ullman bound; the tight bound uses the even slower inverse Ackermann function $\alpha(n)$) and in some parallel and distributed algorithms.

### Fibonacci numbers

$F_0 = 0$, $F_1 = 1$, $F_i = F_{i-1} + F_{i-2}$. With $\varphi = \frac{1 + \sqrt5}{2} \approx 1.618$ and $\hat\varphi = \frac{1 - \sqrt5}{2}$:

$$
F_i = \frac{\varphi^i - \hat\varphi^{\,i}}{\sqrt5}, \qquad F_i = \left\lfloor \frac{\varphi^i}{\sqrt5} + \frac12 \right\rfloor .
$$

Fibonacci numbers grow exponentially, $F_i = \Theta(\varphi^i)$. They give the worst case of Euclid's algorithm ([2.3](topic3.md)) and the cost of naive recursive Fibonacci, which makes $\Theta(\varphi^n)$ calls (motivating memoisation, [Unit 6](../unit6/topic1.md)).

### Series used in analysis

$$
\sum_{k=1}^{n} k = \frac{n(n+1)}{2} = \Theta(n^2), \qquad \sum_{k=1}^{n} k^d = \Theta(n^{d+1}), \qquad \sum_{k=0}^{n} x^k = \frac{x^{n+1}-1}{x-1}\ (x \ne 1), \qquad \sum_{k=0}^{\infty} x^k = \frac{1}{1-x}\ (|x| < 1).
$$

A geometric series is dominated by its largest term: $\Theta(1)$ when the ratio is below 1 (sum of $1 + \frac12 + \frac14 + \dots$), $\Theta(x^n)$ when the ratio $x > 1$. This single fact explains the three cases of recursion-tree analysis ([3.3](../unit3/topic3.md)). Further formulas are collected in [Unit 1](../unit1/topic3.md).

## The Growth Hierarchy

For constants $0 < \varepsilon < 1 < c$ and $k > 1$:

$$
1 \prec \lg^* n \prec \lg \lg n \prec \lg n \prec \lg^k n \prec n^{\varepsilon} \prec \sqrt n \prec n \prec n \lg n \prec n^{c} \prec 2^n \prec 3^n \prec n! \prec n^n
$$

where $f \prec g$ means $f = o(g)$.

| Class | Representative | Typical algorithm or source |
|---|---|---|
| Constant | $1$ | array access, hash lookup (expected) |
| Iterated log | $\lg^* n$ | union-find (Hopcroft–Ullman bound) |
| Double log | $\lg \lg n$ | interpolation search on uniformly distributed keys (expected); van Emde Boas trees ($\lg \lg u$ for key universe size $u$) |
| Logarithmic | $\lg n$ | binary search, balanced BST operations |
| Polylogarithmic | $\lg^2 n$ | some parallel and data-structure bounds |
| Sublinear root | $\sqrt n$ | trial division to $\sqrt N$ (in terms of the value $N$) |
| Linear | $n$ | scanning, counting sort with small key range |
| Linearithmic | $n \lg n$ | merge sort, heapsort, FFT |
| Polynomial | $n^2$, $n^3$, $n^{\lg 7}$ | insertion sort, naive / Strassen matrix multiplication |
| Exponential | $2^n$ | all subsets, brute-force SAT |
| Factorial | $n!$ | all permutations, brute-force TSP |

<figure markdown="span">
    ![Common growth rates](../img/u2/algoGrowthRate.jpg){width="70%"}
    <figcaption>The main growth classes plotted together; the curves separate rapidly as the input size grows.</figcaption>
</figure>

### Method: placing a function in the hierarchy

1. **Simplify** using the identities above (expand logs of products, rewrite $a^{\log_b n}$ as $n^{\log_b a}$, apply Stirling to factorials).
2. **Take logarithms** when comparing functions with exponents: $f \prec g$ is often clearer after comparing $\lg f$ with $\lg g$. Caution: $\lg f = o(\lg g)$ implies $f = o(g)$, but $\lg f = \Theta(\lg g)$ does **not** imply $f = \Theta(g)$ (compare $2^n$ and $4^n$).
3. **Substitute** $n = 2^m$ to turn logarithms into polynomials and polynomials into exponentials.
4. **Confirm** with the limit test ([2.5](topic5.md)).

## Worked Examples

### Example 1: rank $n^{\lg \lg n}$ against $n^3$ and $2^n$

$\lg(n^{\lg\lg n}) = \lg n \cdot \lg\lg n$. Compare with $\lg(n^3) = 3\lg n$ and $\lg(2^n) = n$. Since $\lg\lg n \to \infty$, $3\lg n = o(\lg n \lg\lg n)$, and $\lg n \lg\lg n = o(n)$. So $n^3 \prec n^{\lg\lg n} \prec 2^n$: it is **superpolynomial but subexponential**.

### Example 2: $2^{\lg n}$, $4^{\lg n}$, $2^{\sqrt{\lg n}}$

- $2^{\lg n} = n$.
- $4^{\lg n} = n^{\lg 4} = n^2$ (by $a^{\log_b c} = c^{\log_b a}$).
- $2^{\sqrt{\lg n}}$: its log is $\sqrt{\lg n}$, which is $\omega(\lg\lg n)$ but $o(\lg n)$, so $2^{\sqrt{\lg n}}$ grows faster than every polylogarithm but slower than every $n^\varepsilon$.

### Example 3: $\lg(n!)$ and $(\lg n)!$

$\lg(n!) = \Theta(n \lg n)$ (shown above). For $(\lg n)!$, let $m = \lg n$: $\lg((\lg n)!) = \Theta(m \lg m) = \Theta(\lg n \lg\lg n)$, so $(\lg n)! = n^{\Theta(\lg\lg n)}$, superpolynomial, like Example 1.

### Example 4: simplify $T(n) = 5n^2 + 3n \log_{10} n + 2^{\lg n} + 100$

$2^{\lg n} = n$; $3n\log_{10} n = \Theta(n \lg n)$. The dominant term is $5n^2$, so $T(n) = \Theta(n^2)$.

### Example 5: harmonic sum in an algorithm

A loop runs `for k in 1..n: for j in 1..n step k: work()`. The inner loop runs about $n/k$ times, giving $\sum_{k=1}^{n} \lceil n/k \rceil = n H_n + O(n) = \Theta(n \lg n)$. This is the cost of the harmonic-sum pattern used, for example, when iterating over all multiples of every number (sieve-style loops).

## Python Implementation

Small utilities to compute and check the functions above. `ceil_div` is the integer ceiling used in real code.

```python
import math


def log_star(n):
    """Iterated logarithm (base 2): times log2 must be applied until the value is <= 1."""
    count = 0
    x = n
    while x > 1:
        x = math.log2(x)
        count += 1
    return count


def harmonic(n):
    """H_n = 1 + 1/2 + ... + 1/n."""
    return sum(1 / k for k in range(1, n + 1))


def stirling(n):
    """Stirling's approximation sqrt(2 pi n) (n/e)^n."""
    return math.sqrt(2 * math.pi * n) * (n / math.e) ** n


def ceil_div(a, b):
    """Ceiling of a / b for integers, b > 0, without floating point."""
    return -(-a // b)
```

Walkthrough:

- `log_star(65536)` is 4 and `log_star(2 ** 65536)` is 5; `math.log2` accepts arbitrarily large Python integers, so the second call works.
- `harmonic(10**6) - math.log(10**6)` is about 0.57722, approaching Euler's constant $\gamma$.
- `math.factorial(n) / stirling(n)` is about 1.0083 at $n = 10$ and 1.00083 at $n = 100$, matching the correction factor $1 + \frac{1}{12n}$.
- `ceil_div` uses Python's floor division on the negated numerator. `math.ceil(a / b)` goes through floating point and can be wrong for integers beyond $2^{53}$.

## Edge Cases and Pitfalls

| Case / pitfall | What goes wrong | Fix |
|---|---|---|
| $\lg 0$ or $\lg$ of a negative number | undefined; crashes in code | handle $n \le 1$ separately (e.g. `log_star(1) == 0`) |
| `math.ceil(a / b)` for huge integers | floating-point rounding gives a wrong integer | use `-(-a // b)` |
| Negative operands with `//` and `%` | Python rounds toward $-\infty$; C/Java truncate toward 0, so `-7 // 2` is `-4` in Python but `-7 / 2` is `-3` in C | know your language's rule; normalise with `% m` |
| Confusing $\lg(n^k)$ with $\lg^k n$ | wrong class: $\Theta(\lg n)$ vs $\Theta(\lg^k n)$ | write parentheses explicitly |
| Assuming exponential bases are interchangeable | $2^n$ and $4^n$ are different classes | only logarithm bases can be ignored |
| Overflow computing $n!$ or $\binom{n}{k}$ in fixed-width types | wraps silently in C/Java | use modular arithmetic or logs ($\lg n!$ via `math.lgamma`) |
| Using Stirling for tiny $n$ as exact | relative error about $1/(12n)$ | use exact values for small $n$ |

## Common Misconceptions

- **"$\lg n$ and $\ln n$ are different complexity classes."** They differ by the constant factor $\ln 2$; $\Theta(\lg n) = \Theta(\ln n)$.
- **"$n^{100}$ is basically exponential."** It is polynomial and eventually far smaller than $1.01^n$, although for practical sizes it may be infeasible. Polynomial vs exponential is about growth, not about practicality at a particular $n$.
- **"$\lg^* n$ is constant."** It is unbounded but at most 5 for any practical input; asymptotically it is $\omega(1)$.
- **"$n! \approx n^n$."** $n! = o(n^n)$; Stirling shows $n!/n^n \approx \sqrt{2\pi n}\, e^{-n} \to 0$. But $\lg(n!) = \Theta(\lg(n^n)) = \Theta(n \lg n)$: logs can hide large ratios.
- **"Floors and ceilings change complexity."** For standard recurrences they do not change the $\Theta$ class; they do matter for exact counts and for code correctness.

## Alternatives and Trade-offs

| When you need... | Use | Avoid |
|---|---|---|
| order of growth of $n!$ or $\lg n!$ | the elementary bounds $(n/2)^{n/2} \le n! \le n^n$ | full Stirling (more precision than needed) |
| numerical value of large factorials or binomials | `math.lgamma`, log-space arithmetic | computing the exact huge integer if only magnitude is needed |
| exact integer ceilings in code | `-(-a // b)` | floating-point `ceil` |
| comparing two exotic functions | logs, substitution $n = 2^m$, then the limit test | plotting at small $n$ |
| precise constants in sums | integral bounds ($H_n$ between $\ln(n+1)$ and $\ln n + 1$) | rough order-of-growth only, when constants matter |

## In Practice

- Library functions mirror these definitions: Python's `math.log2`, `math.log`, `math.comb`, `math.factorial`, `math.lgamma`, and `int.bit_length()` (which returns $\lfloor \lg n \rfloor + 1$ for positive $n$).
- Integer ceiling division (`(a + b - 1) / b` for non-negative values in C, `-(-a // b)` in Python) appears in pagination, buffer allocation, and splitting work into chunks.
- Machine learning uses log-space arithmetic (log-probabilities, log-sum-exp) for the same reason we analyse $\lg(n!)$ rather than $n!$: the raw values overflow.
- Data structures with $\lg\lg n$ or $\lg^* n$ terms are often replaced in practice by simpler $\lg n$ structures, because at realistic sizes the difference is a small constant and simplicity wins.

## Interview and Competitive Programming

- Know the hierarchy cold; "rank these functions" is a standard question.
- $\lg(10^9) \approx 30$, $\lg(10^{18}) \approx 60$, $2^{10} \approx 10^3$, $2^{20} \approx 10^6$, $2^{30} \approx 10^9$; $10! \approx 3.6 \times 10^6$, $12! \approx 4.8 \times 10^8$, $20! \approx 2.4 \times 10^{18}$.
- Recognition cue: "iterate over multiples of every $k$" → harmonic sum → $O(n \log n)$.
- Recognition cue: "number of digits/bits" → $\lfloor \log_b n \rfloor + 1$.
- Trap: in C++/Java, `(a + b - 1) / b` overflows for large `a`; for negative values the formula is wrong. Use 64-bit types and check signs.
- Trap: counting digits with floating-point logs. `int(math.log10(n)) + 1` returns 17 for $n = 10^{16} - 1$, which has 16 digits, because the float rounds $n$ up to $10^{16}$. Prefer integer methods such as `len(str(n))` or `n.bit_length()`.

## Using AI Assistants Critically

- LLMs frequently mix up $\lg(n^2)$ and $\lg^2 n$, or claim $2^n = \Theta(4^n)$ by "ignoring constants in the exponent"; check each identity.
- Generated rankings of functions often misplace $n^{\lg\lg n}$, $(\lg n)!$, or $2^{\sqrt{\lg n}}$; verify by taking logarithms as in the worked examples.
- Code from assistants commonly uses `math.ceil(a / b)` or `int(math.log2(n))` for integer work; replace with exact integer arithmetic and test at powers of two and at large values.
- Ask for the base case of any claimed identity (e.g. whether $\lg^* 1 = 0$) and check it with a direct computation.
- Use `math.lgamma` and exact `math.factorial` to sanity-check any Stirling-based numerical claim.

## Practice

### Beginner

1. **Log identities.** Simplify $\lg(8n^3)$, $\log_4 n$ in terms of $\lg n$, and $2^{3\lg n}$. Difficulty: easy.
2. **Floor and ceiling.** For $n = 17$, compute $\lfloor n/2 \rfloor$, $\lceil n/2 \rceil$, $\lceil \lceil n/2 \rceil / 2 \rceil$, and $\lceil n/4 \rceil$. Difficulty: easy.
3. **Bits.** How many bits does $n = 10^6$ have? Give the formula and the value. Difficulty: easy.

### Intermediate

1. **Rank functions.** Order by growth: $n \lg n$, $n^{1.01}$, $\lg^{10} n$, $2^{\lg n}$, $\sqrt n \lg n$, $(\sqrt 2)^{\lg n}$. Difficulty: medium.
2. **Factorial bounds.** Prove $n! = \omega(2^n)$ and $n! = o(n^n)$. Difficulty: medium.
3. **Harmonic loop.** Analyse `for i in 1..n: j = i; while j <= n: work(); j += i`. Output: order of growth. Difficulty: medium.

### Advanced

1. **Superpolynomial ranking.** Rank $n^{\lg n}$, $2^{\sqrt n}$, $(\lg n)^{\lg n}$, $n^{\lg\lg n}$. Difficulty: hard.
2. **Prove an identity.** Prove $\lceil \lceil n/a \rceil / b \rceil = \lceil n/(ab) \rceil$ for positive integers $n, a, b$. Difficulty: medium-hard.
3. **Iterated log.** Is $\lg^*(\lg n) = \Theta(\lg^* n)$? Is $\lg(\lg^* n) = O(\lg^*(\lg n))$? Difficulty: hard.

### Interview / Competitive Programming

1. **Count digits.** Given $n \le 10^{18}$, return the number of decimal digits without floating point. Difficulty: easy.
2. **Pages.** $n$ items, $k$ per page: how many pages? Write overflow-safe integer code. Difficulty: easy.
3. **Feasibility by factorial.** Brute force over permutations: what is the largest $n$ for which $n \cdot n!$ operations fit in $10^8$? Difficulty: easy-medium.

## Self-Check Questions

??? question "Q1. Why can the base of a logarithm be omitted in $O(\log n)$ but the base of an exponential cannot be omitted in $O(2^n)$?"

    $\log_a n = \log_b n / \log_b a$: changing the base multiplies by a constant, which $O$ absorbs. $3^n / 2^n = (3/2)^n$ is not bounded, so different exponential bases give different classes.

??? question "Q2. Show that $3^{\lg n} = n^{\lg 3}$ and explain where this form appears."

    Using $a^{\log_b c} = c^{\log_b a}$ with $a = 3$, $b = 2$, $c = n$. It is the number of leaves in the recursion tree of $T(n) = 3T(n/2) + \Theta(n)$ (Karatsuba), giving $\Theta(n^{\lg 3}) \approx \Theta(n^{1.585})$.

??? question "Q3. Prove $\lg(n!) = \Omega(n \lg n)$ without Stirling."

    At least $n/2$ of the factors of $n!$ are $\ge n/2$, so $n! \ge (n/2)^{n/2}$, hence $\lg(n!) \ge \frac n2 \lg \frac n2 = \frac n2(\lg n - 1) \ge \frac n4 \lg n$ for $n \ge 4$.

??? question "Q4. What is $\lg^* 65536$, and why is $\lg^* n$ considered 'effectively constant'?"

    $65536 \to 16 \to 4 \to 2 \to 1$: four applications, so $\lg^* 65536 = 4$. It stays at most 5 up to $2^{65536}$, a number far larger than any realistic input size, even though it is unbounded mathematically.

??? question "Q5. Rank $n^{\lg\lg n}$, $n^3$, $2^n$."

    Compare logarithms: $\lg n \lg\lg n$, $3\lg n$, $n$. Since $\lg\lg n \to \infty$ and $\lg n \lg\lg n = o(n)$, the order is $n^3 \prec n^{\lg\lg n} \prec 2^n$.

??? question "Q6. Why does $\sum_{k=1}^n n/k$ appear in sieve-like loops, and what is its order?"

    For each $k$, iterating over all multiples of $k$ up to $n$ takes $n/k$ steps; summing gives $n H_n = \Theta(n \log n)$.

??? question "Q7. Is $\lg(\lg n)$ the same as $\lg^2 n$?"

    No. $\lg\lg n$ is a logarithm applied twice and grows extremely slowly; $\lg^2 n = (\lg n)^2$ grows faster than $\lg n$. Notation: $\lg^k n$ means a power, $\lg^* n$ means iterated application.

## Complexity Summary

| Function | Order / key fact |
|---|---|
| $\log_a n$ (any constant $a > 1$) | $\Theta(\lg n)$ |
| $a^{\log_b n}$ | $n^{\log_b a}$ |
| $\lg^b n$ vs $n^a$ ($a > 0$) | $\lg^b n = o(n^a)$ |
| $n^b$ vs $a^n$ ($a > 1$) | $n^b = o(a^n)$ |
| $\lg(n!)$ | $\Theta(n \lg n)$; $\approx n\lg n - 1.44n$ |
| $n!$ | $\sqrt{2\pi n}(n/e)^n(1 + \Theta(1/n))$; $\omega(2^n)$, $o(n^n)$ |
| $\binom{n}{k}$, fixed $k$ | $\Theta(n^k)$ |
| $\binom{n}{n/2}$ | $\Theta(2^n/\sqrt n)$ |
| $H_n$ | $\ln n + O(1)$ |
| $F_n$ | $\Theta(\varphi^n)$, $\varphi \approx 1.618$ |
| $\lg^* n$ | $\le 5$ for $n \le 2^{65536}$; $\omega(1)$ |
| Bits of $n$ | $\lfloor \lg n \rfloor + 1$ |

## Key Takeaways

- Logarithm bases differ by constant factors and can be ignored inside $O$; exponential bases cannot.
- $a^{\log_b n} = n^{\log_b a}$ converts recursion-tree leaf counts into polynomials and drives the Master Theorem.
- Polylogarithms are dominated by every positive power of $n$; polynomials are dominated by every exponential with base above 1.
- $\lg(n!) = \Theta(n \lg n)$, which underlies the $\Omega(n \lg n)$ comparison-sorting lower bound; Stirling gives the precise form.
- Harmonic numbers ($H_n \approx \ln n$) appear in randomised analysis and in loops over multiples.
- $\lg^* n$ is unbounded but at most 5 for all practical inputs.
- Floors and ceilings rarely change the order of growth but often cause off-by-one bugs; use exact integer arithmetic in code.
