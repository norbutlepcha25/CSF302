# Number Theory for Algorithms

!!! abstract "At a glance"

    - **Problem space:** reasoning about integers — divisibility, primes, greatest common divisors, and arithmetic "modulo $m$".
    - **Key ideas:** $\gcd(a,b) = \gcd(b, a \bmod b)$; every composite $n$ has a prime factor $\le \sqrt n$; modular arithmetic keeps numbers small without losing the answer; an inverse modulo $m$ exists iff $\gcd(a, m) = 1$.
    - **Core complexities:** Euclid $O(\log \min(a,b))$; trial division $O(\sqrt n)$; Sieve of Eratosthenes $O(n \log\log n)$; modular inverse $O(\log m)$.
    - **Where it is used:** RSA and Diffie–Hellman, hashing (polynomial rolling hash, universal hashing), checksums, random number generators, and every "print the answer modulo $10^9+7$" contest problem.

## Motivation and Problem Context

Three situations that every software engineer eventually meets:

1. **The answer is too big.** "Count the number of valid passwords of length $10^5$" has an answer with tens of thousands of digits. Contests (and many real systems) ask for the answer **modulo** a prime such as $10^9+7$. You must compute it without ever forming the huge number.
2. **Security.** When your browser opens an HTTPS connection, the server proves its identity using public-key cryptography (RSA or elliptic curves). RSA is nothing more than Euclid's algorithm, modular inverses, and fast modular exponentiation on very large integers.
3. **Hashing.** A hash table that uses `h(k) = k mod m` behaves badly if $m$ shares factors with the patterns in your keys. Choosing $m$ prime and understanding *why* is number theory.

Number theory is therefore not a mathematical curiosity in this course: it is the toolkit that makes integer-heavy algorithms **correct** (no overflow, no wrong division) and **fast** (logarithmic instead of linear).

## Problem Formulation

This topic answers a family of computational questions. For integers given in binary with $b$ bits each:

| Question | Input | Output | Efficient method |
| --- | --- | --- | --- |
| Is $n$ prime? | $n \ge 1$ | yes/no | Trial division to $\sqrt n$ (or Miller–Rabin for huge $n$) |
| All primes up to $N$ | $N$ | list of primes | Sieve of Eratosthenes |
| Greatest common divisor | $a, b \ge 0$ | $\gcd(a,b)$ | Euclid's algorithm |
| Bézout coefficients | $a, b$ | $x, y$ with $ax+by=\gcd(a,b)$ | Extended Euclid |
| Modular inverse | $a, m$ | $x$ with $ax \equiv 1 \pmod m$ | Extended Euclid, or Fermat if $m$ prime |
| Modular power | $a, e, m$ | $a^e \bmod m$ | Square-and-multiply ([Unit 4.6](../unit4/topic6.md)) |

**Assumptions.** Unless stated otherwise, we work in the Word-RAM model ([Unit 2.2](../unit2/topic2.md)): arithmetic on machine words (64-bit) costs $O(1)$. For numbers far larger than a word (RSA uses 2048-bit integers), each operation costs more, and complexities should be read in terms of the number of bits $b = \lceil \log_2 n \rceil$.

!!! warning "Important: input size is the number of bits, not the value"

    Trial division takes $O(\sqrt n)$ steps. That looks "sub-linear", but the input is $n$ written in $b \approx \log_2 n$ bits, so $\sqrt n = 2^{b/2}$ is **exponential in the input size**. This is why factoring a 2048-bit RSA modulus by trial division is hopeless, while Euclid's $O(\log n) = O(b)$ is genuinely efficient.

## Intuition

Almost everything in this topic follows from one observation: **a remainder carries all the information you need about divisibility.** If $d$ divides both $a$ and $b$, it divides $a - qb$ for any $q$, in particular $a \bmod b$. So we may replace a large problem $(a, b)$ by a smaller one $(b, a \bmod b)$ without changing the answer — that is Euclid. Similarly, $(a \cdot b) \bmod m$ depends only on $a \bmod m$ and $b \bmod m$, so we may reduce after every operation — that is modular arithmetic. Mental model: **work on remainders, never on the giant numbers themselves.**

## Definitions

| Term | Definition | Example |
| --- | --- | --- |
| Divides, $a \mid b$ | $b = ka$ for some integer $k$ | $3 \mid 12$, $5 \nmid 12$ |
| Division algorithm | For $b > 0$: unique $q, r$ with $a = qb + r$, $0 \le r < b$; write $r = a \bmod b$ | $17 = 3 \cdot 5 + 2$ |
| Prime | Integer $p > 1$ whose only positive divisors are $1$ and $p$ | $2, 3, 5, 7, 11$ |
| Composite | Integer $n > 1$ that is not prime; $1$ is neither | $12 = 2^2 \cdot 3$ |
| $\gcd(a,b)$ | Largest integer dividing both; $\gcd(a, 0) = a$ | $\gcd(240, 46) = 2$ |
| $\operatorname{lcm}(a,b)$ | Smallest positive integer divisible by both | $\operatorname{lcm}(4, 6) = 12$ |
| Coprime | $\gcd(a, b) = 1$ | $8$ and $15$ |
| Congruence | $a \equiv b \pmod m \iff m \mid (a - b)$ | $17 \equiv 2 \pmod 5$ |
| Modular inverse | $a^{-1}$ with $a \cdot a^{-1} \equiv 1 \pmod m$ | $3^{-1} \equiv 4 \pmod{11}$ |
| Euler's totient $\varphi(n)$ | Number of $k \in [1, n]$ coprime to $n$ | $\varphi(9) = 6$ |

## Key Results

### Primes

**Fundamental Theorem of Arithmetic.** Every integer $n > 1$ has a unique factorization $n = p_1^{e_1} p_2^{e_2} \cdots p_k^{e_k}$ (up to order). Many functions are read straight off this factorization:

$$
d(n) = \prod_{i=1}^{k} (e_i + 1), \qquad
\sigma(n) = \prod_{i=1}^{k} \frac{p_i^{e_i+1} - 1}{p_i - 1}, \qquad
\varphi(n) = n \prod_{i=1}^{k}\Big(1 - \frac{1}{p_i}\Big)
$$

where $d(n)$ counts divisors and $\sigma(n)$ sums them. Example: $60 = 2^2 \cdot 3 \cdot 5$ gives $d(60) = 3 \cdot 2 \cdot 2 = 12$ and $\varphi(60) = 60 \cdot \tfrac12 \cdot \tfrac23 \cdot \tfrac45 = 16$.

**Small-factor lemma.** If $n$ is composite, it has a divisor $d$ with $1 < d \le \sqrt n$.
*Proof.* Write $n = d \cdot e$ with $1 < d \le e$. If $d > \sqrt n$ then $d \cdot e > \sqrt n \cdot \sqrt n = n$, a contradiction. $\square$

**$6k \pm 1$ lemma.** Every prime $p > 3$ is of the form $6k \pm 1$.
*Proof.* Any integer is $6k + r$ with $r \in \{0,\dots,5\}$. $6k, 6k+2, 6k+4$ are even and $6k+3$ is divisible by 3, so only $r = 1$ and $r = 5$ ($= 6(k+1) - 1$) remain. $\square$

**Density (Prime Number Theorem).** The number of primes $\le n$ is $\pi(n) \approx n / \ln n$. Concretely $\pi(10^6) = 78{,}498$ and $\pi(10^9) = 50{,}847{,}534$. Primes are common enough that a random 1024-bit odd number is prime with probability roughly $2/\ln(2^{1024}) \approx 1/355$ — which is why RSA key generation simply samples random numbers and tests them.

### GCD and Euclid's Algorithm

**Lemma (Euclid).** For $b > 0$: $\gcd(a, b) = \gcd(b, a \bmod b)$.
*Proof.* Let $r = a \bmod b = a - qb$. If $d \mid a$ and $d \mid b$ then $d \mid a - qb = r$. Conversely if $d \mid b$ and $d \mid r$ then $d \mid qb + r = a$. The pairs $(a, b)$ and $(b, r)$ have **exactly the same set of common divisors**, so the same greatest one. $\square$

**Termination and running time.** The second argument strictly decreases and stays $\ge 0$, so the loop terminates. Faster still: **after two steps, the first argument at least halves.** If $b \le a/2$ then $a \bmod b < b \le a/2$; if $b > a/2$ then $a \bmod b = a - b < a/2$. Either way the value two positions later is $< a/2$, so there are at most $2\log_2 a + O(1)$ steps: $O(\log \min(a,b))$ arithmetic operations.

**Lamé's theorem** sharpens this: the worst inputs are consecutive Fibonacci numbers, because each quotient is $1$ and the remainders shrink as slowly as possible. Euclid on $(F_{k+1}, F_k)$ takes about $k$ steps, and $F_k \approx \phi^k/\sqrt5$, so the step count is about $\log_\phi n \approx 1.44 \log_2 n$.

**Bézout's identity.** For any $a, b$ there exist integers $x, y$ with $ax + by = \gcd(a, b)$. Moreover $\gcd(a,b)$ is the **smallest positive** integer of the form $ax + by$. The extended Euclidean algorithm constructs $x, y$.

**GCD/LCM via factorization.** $\gcd$ takes the **minimum** exponent of each prime, $\operatorname{lcm}$ the **maximum**. Since $\min(e, f) + \max(e, f) = e + f$:

$$
\gcd(a,b) \cdot \operatorname{lcm}(a,b) = a \cdot b .
$$

| Property | Statement |
| --- | --- |
| Associativity | $\gcd(a, b, c) = \gcd(\gcd(a,b), c)$, so the gcd of an array is a fold |
| Scaling | $\gcd(ka, kb) = k\gcd(a,b)$ for $k > 0$ |
| Differences | $\gcd(a, b) = \gcd(a, b - a)$, so $\gcd$ of an array equals $\gcd(a_1, a_2 - a_1, \dots)$ |
| Idempotence | $\gcd(a, a) = a$, which allows overlapping ranges in sparse tables |

### Modular Arithmetic

For a modulus $m \ge 1$, addition, subtraction and multiplication respect congruence:

$$
\begin{aligned}
(a + b) \bmod m &= \big((a \bmod m) + (b \bmod m)\big) \bmod m \\
(a - b) \bmod m &= \big((a \bmod m) - (b \bmod m) + m\big) \bmod m \\
(a \cdot b) \bmod m &= \big((a \bmod m)(b \bmod m)\big) \bmod m
\end{aligned}
$$

*Why:* write $a = q_1 m + r_1$, $b = q_2 m + r_2$. Then $ab = m(\dots) + r_1 r_2$, so $ab \equiv r_1 r_2$. The same expansion works for $\pm$.

**Division does not distribute.** $(a / b) \bmod m \ne (a \bmod m) / (b \bmod m)$ in general (try $a = 12, b = 4, m = 5$: the left side is $3$, the right side is $2/4$, not even an integer). "Dividing by $b$" modulo $m$ means **multiplying by the inverse** $b^{-1}$.

**Inverse existence theorem.** $a$ has an inverse modulo $m$ **iff** $\gcd(a, m) = 1$.
*Proof.* ($\Leftarrow$) By Bézout, $ax + my = 1$, so $ax \equiv 1 \pmod m$. ($\Rightarrow$) If $ax \equiv 1$ then $ax + my = 1$ for some $y$; any common divisor of $a$ and $m$ divides $1$. $\square$

Consequently, when $m = p$ is **prime**, every $a \not\equiv 0$ has an inverse. This is the reason contest moduli ($10^9+7$, $998\,244\,353$) are prime.

**Fermat's little theorem.** If $p$ is prime and $p \nmid a$, then $a^{p-1} \equiv 1 \pmod p$, hence

$$
a^{-1} \equiv a^{p-2} \pmod p .
$$

*Proof sketch.* The numbers $a, 2a, \dots, (p-1)a$ are non-zero modulo $p$ and pairwise distinct: if $ia \equiv ja$ then $p \mid (i-j)a$, and since $p \nmid a$ and $p$ is prime, $p \mid i - j$, forcing $i = j$. So modulo $p$ they are a permutation of $1, \dots, p-1$. Multiplying them all: $a^{p-1}(p-1)! \equiv (p-1)!$, and $(p-1)!$ is coprime to $p$, so it cancels. $\square$

**Euler's theorem** generalizes this to any modulus: if $\gcd(a, m) = 1$ then $a^{\varphi(m)} \equiv 1 \pmod m$.

**Chinese Remainder Theorem (CRT).** If $m_1, \dots, m_k$ are pairwise coprime, the system $x \equiv r_i \pmod{m_i}$ has exactly one solution modulo $M = m_1 m_2 \cdots m_k$. For two moduli, with $m_1 p + m_2 q = 1$ from extended Euclid,

$$
x = r_1 + m_1 \cdot \big((r_2 - r_1)\, p \bmod m_2\big)
$$

works: it is clearly $\equiv r_1 \pmod{m_1}$, and modulo $m_2$ we have $m_1 p \equiv 1$, so $x \equiv r_1 + (r_2 - r_1) = r_2$.

!!! warning "Important: when does $a^{-1} \bmod m$ exist?"

    Exactly when $\gcd(a, m) = 1$ — not "when $m$ is prime". Fermat's formula $a^{m-2}$ requires $m$ prime; extended Euclid works for any modulus coprime to $a$. A common exam and production bug is applying $a^{m-2}$ with a composite $m$: it silently returns a wrong value.

## Methods

### Primality testing and the sieve

**Trial division** (single query): handle $n < 4$ and divisibility by 2 and 3, then test $d = 5, 11, 17, \dots$ and $d+2$ while $d^2 \le n$. By the two lemmas above this is correct and does about $\sqrt n / 3$ divisions.

**Sieve of Eratosthenes** (all primes up to $N$): mark every multiple of each prime as composite, starting from $p^2$ — every smaller multiple $p \cdot k$ with $k < p$ has a prime factor smaller than $p$ and is already crossed out. Only primes $p \le \sqrt N$ need to cross anything out.

```text
SIEVE(N)
    is_prime[0..N] <- true;  is_prime[0] <- is_prime[1] <- false
    p <- 2
    while p * p <= N
        if is_prime[p]
            for j <- p*p, p*p + p, ..., up to N
                is_prime[j] <- false
        p <- p + 1
    return is_prime
```

*Complexity.* Prime $p$ crosses out about $N/p$ numbers, so the total work is $N \sum_{p \le \sqrt N} 1/p = O(N \log\log N)$, using Mertens' theorem that the sum of reciprocals of primes up to $x$ grows like $\ln\ln x$. Space is $O(N)$.

**Variants worth knowing:**

| Variant | What it stores | Cost | Use when |
| --- | --- | --- | --- |
| Smallest-prime-factor (SPF) sieve | `spf[i]` = least prime dividing $i$ | $O(N\log\log N)$ build, $O(\log n)$ per factorization | Many factorization queries, $n \le 10^7$ |
| Linear (Euler) sieve | Each composite crossed exactly once, by its least prime | $O(N)$ | Computing multiplicative functions ($\varphi$, $d$) for all $n \le N$ |
| Segmented sieve | Sieve primes up to $\sqrt R$, then cross out inside $[L, R]$ | $O(\sqrt R + (R-L)\log\log R)$ time, $O(\sqrt R + R - L)$ space | $R \le 10^{12}$ but $R - L \le 10^6$ |
| Divisor-count sieve | `for i: for j = i, 2i, ...: cnt[j] += 1` | $O(N \log N)$ (harmonic sum) | $d(n)$ for all $n \le N$ |

The SPF factorization loop is $O(\log n)$ because each division at least halves $n$.

### Extended Euclid

Suppose the recursive call on $(b, a \bmod b)$ returned $x_1, y_1$ with $b x_1 + (a \bmod b) y_1 = g$. Substitute $a \bmod b = a - \lfloor a/b \rfloor b$:

$$
g = b x_1 + \big(a - \lfloor a/b\rfloor b\big) y_1 = a\, y_1 + b\,\big(x_1 - \lfloor a/b\rfloor y_1\big).
$$

So $x = y_1$, $y = x_1 - \lfloor a/b \rfloor y_1$. Base case: $\gcd(a, 0) = a = a \cdot 1 + 0 \cdot 0$.

```text
EXTENDED-GCD(a, b)                 // returns (g, x, y) with a*x + b*y = g
    if b = 0
        return (a, 1, 0)
    (g, x1, y1) <- EXTENDED-GCD(b, a mod b)
    return (g, y1, x1 - floor(a / b) * y1)

MOD-INVERSE(a, m)
    (g, x, y) <- EXTENDED-GCD(a mod m, m)
    if g != 1
        error "no inverse"
    return x mod m                  // normalize into [0, m)
```

### Fast modular exponentiation (brief)

To compute $a^e \bmod m$, use the binary digits of $e$: square the base each step and multiply it into the result when the current bit is 1. That needs $O(\log e)$ multiplications instead of $e - 1$. The full derivation, proof, and recursion analysis live in [Unit 4.6 Efficient Modular Exponentiation](../unit4/topic6.md); here we only use it as a building block for Fermat inverses and RSA. In Python it is built in: `pow(a, e, m)`, and since Python 3.8 `pow(a, -1, m)` returns the modular inverse.

## Worked Examples

!!! example "Example 1 (basic): Euclid on $(240, 46)$"

    | Step | $a$ | $b$ | $a \bmod b$ |
    | --- | --- | --- | --- |
    | 1 | 240 | 46 | 10 |
    | 2 | 46 | 10 | 6 |
    | 3 | 10 | 6 | 4 |
    | 4 | 6 | 4 | 2 |
    | 5 | 4 | 2 | 0 |
    | end | 2 | 0 | — |

    $\gcd(240, 46) = 2$ after 5 steps; $\operatorname{lcm} = 240/2 \cdot 46 = 5520$.

!!! example "Example 2 (intermediate): extended Euclid, back-substitution"

    Unwind the calls for $(240, 46)$ from the base case upward, using $x = y_1$, $y = x_1 - q y_1$:

    | Call $(a, b)$ | $q = \lfloor a/b \rfloor$ | returned $(g, x, y)$ | check $ax + by$ |
    | --- | --- | --- | --- |
    | $(2, 0)$ | — | $(2, 1, 0)$ | $2$ |
    | $(4, 2)$ | 2 | $(2, 0, 1)$ | $0 + 2 = 2$ |
    | $(6, 4)$ | 1 | $(2, 1, -1)$ | $6 - 4 = 2$ |
    | $(10, 6)$ | 1 | $(2, -1, 2)$ | $-10 + 12 = 2$ |
    | $(46, 10)$ | 4 | $(2, 2, -9)$ | $92 - 90 = 2$ |
    | $(240, 46)$ | 5 | $(2, -9, 47)$ | $-2160 + 2162 = 2$ |

!!! example "Example 3 (intermediate): $3^{-1} \bmod 11$ two ways"

    - Extended Euclid on $(3, 11)$ returns $(1, 4, -1)$: $3 \cdot 4 + 11 \cdot (-1) = 1$, so $3^{-1} \equiv 4$.
    - Fermat: $3^{11-2} = 3^9 = 19683 = 1789 \cdot 11 + 4$, so again $4$. Check: $3 \cdot 4 = 12 \equiv 1 \pmod{11}$.

!!! example "Example 4 (intermediate): CRT"

    Find $x$ with $x \equiv 2 \pmod 3$ and $x \equiv 3 \pmod 5$. Extended Euclid gives $3 \cdot 2 + 5 \cdot (-1) = 1$, so $p = 2$. Then $x = 2 + 3 \cdot ((3 - 2) \cdot 2 \bmod 5) = 2 + 3 \cdot 2 = 8$. Check: $8 \bmod 3 = 2$, $8 \bmod 5 = 3$. The solution is unique modulo $15$.

!!! example "Example 5 (advanced): toy RSA"

    1. Choose primes $p = 61$, $q = 53$. Then $n = pq = 3233$ and $\varphi(n) = (p-1)(q-1) = 3120$.
    2. Choose public exponent $e = 17$ with $\gcd(17, 3120) = 1$.
    3. Private exponent $d = e^{-1} \bmod 3120 = 2753$ (extended Euclid; check $17 \cdot 2753 = 46801 = 15 \cdot 3120 + 1$).
    4. Encrypt message $M = 65$: $C = 65^{17} \bmod 3233 = 2790$ (fast modular exponentiation).
    5. Decrypt: $2790^{2753} \bmod 3233 = 65$. This works because $ed \equiv 1 \pmod{\varphi(n)}$ and Euler's theorem.

    Security rests on the belief that recovering $d$ requires factoring $n$; with 2048-bit $n$ no known classical algorithm does that in feasible time. Real RSA also uses padding (OAEP, PSS); "textbook RSA" as above is insecure.

## Algorithmic Applications

| Application | Number theory used |
| --- | --- |
| "Answer modulo $10^9+7$" counting problems | Modular $+,-,\times$; division via Fermat inverse; factorial tables ([Topic 1.2](topic2.md)) |
| Reducing fractions, rational arithmetic (`fractions.Fraction`) | $\gcd$ |
| Polynomial rolling hash (Rabin–Karp) | Arithmetic modulo a large prime; inverse powers to "remove" a character |
| Hash table with `k mod m` buckets | A prime $m$ avoids collisions from keys sharing factors with $m$ |
| Universal hashing $h(k) = ((ak + b) \bmod p) \bmod m$ | Arithmetic in the field $\mathbb{Z}_p$ (collision analysis is probabilistic, see [Topic 1.3](topic3.md)) |
| RSA, Diffie–Hellman, digital signatures | Modular exponentiation, inverses, Euler's theorem, primality testing |
| Linear Diophantine equation $ax + by = c$ | Solvable iff $\gcd(a,b) \mid c$; scale Bézout; all solutions $x_0 + t\,b/g$, $y_0 - t\,a/g$ |
| Number-theoretic transform (NTT) | FFT ([Unit 4.4](../unit4/topic4.md)) over $\mathbb{Z}_p$ with $p = 998\,244\,353$ |
| Linear congruential generators $x_{i+1} = (a x_i + c) \bmod m$ | Full period conditions use gcd and prime factors of $m$ |

## Python Implementation

```python
def is_prime(n):
    if n < 2:
        return False
    if n < 4:
        return True                      # 2 and 3
    if n % 2 == 0 or n % 3 == 0:
        return False
    d = 5
    while d * d <= n:                    # test 6k - 1 and 6k + 1
        if n % d == 0 or n % (d + 2) == 0:
            return False
        d += 6
    return True


def sieve(n):
    """Return is_prime[0..n] using the Sieve of Eratosthenes."""
    is_p = [True] * (n + 1)
    is_p[0:2] = [False] * min(2, n + 1)
    p = 2
    while p * p <= n:
        if is_p[p]:
            for multiple in range(p * p, n + 1, p):
                is_p[multiple] = False
        p += 1
    return is_p


def smallest_prime_factors(n):
    spf = list(range(n + 1))             # spf[i] == i means "not yet marked"
    p = 2
    while p * p <= n:
        if spf[p] == p:                  # p is prime
            for multiple in range(p * p, n + 1, p):
                if spf[multiple] == multiple:
                    spf[multiple] = p
        p += 1
    return spf


def factorize(x, spf):
    factors = {}
    while x > 1:
        p = spf[x]
        while x % p == 0:
            x //= p
            factors[p] = factors.get(p, 0) + 1
    return factors


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return abs(a)


def lcm(a, b):
    if a == 0 or b == 0:
        return 0
    return abs(a // gcd(a, b) * b)       # divide first: keeps intermediates small


def extended_gcd(a, b):
    """Return (g, x, y) with a*x + b*y == g == gcd(a, b), for a, b >= 0."""
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    return g, y1, x1 - (a // b) * y1


def mod_inverse(a, m):
    g, x, _ = extended_gcd(a % m, m)
    if g != 1:
        raise ValueError(f"{a} has no inverse modulo {m}")
    return x % m


def mod_pow(base, exp, mod):
    result = 1 % mod                     # handles mod == 1
    base %= mod
    while exp > 0:
        if exp & 1:
            result = result * base % mod
        base = base * base % mod
        exp >>= 1
    return result


def crt_pair(r1, m1, r2, m2):
    """Solve x = r1 (mod m1), x = r2 (mod m2) for coprime m1, m2."""
    g, p, _ = extended_gcd(m1, m2)       # m1*p + m2*q == 1
    if g != 1:
        raise ValueError("moduli must be coprime")
    x = r1 + m1 * ((r2 - r1) * p % m2)
    return x % (m1 * m2)


def euler_phi(n):
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p        # multiply by (1 - 1/p) exactly
        p += 1
    if n > 1:                            # one prime factor > sqrt(original n) remains
        result -= result // n
    return result
```

**Walkthrough of the non-obvious lines**

- `is_p[0:2] = [False] * min(2, n + 1)` keeps `sieve(0)` and `sieve(1)` from indexing past the list.
- `spf[i] == i` doubles as "unmarked": primes keep `spf[p] = p`, which is exactly their smallest prime factor.
- `extended_gcd` mirrors the pseudocode line for line; Python's `//` is floor division, matching $\lfloor a/b \rfloor$ for non-negative inputs.
- `x % m` in `mod_inverse` normalizes a possibly negative Bézout coefficient. In Python `%` with a positive modulus is always non-negative; in C, C++, Java and Go it is not (`-7 % 3 == -1`), so those languages need `((x % m) + m) % m`.
- `result = 1 % mod` makes `mod_pow(a, 0, 1)` return `0`, matching Python's built-in `pow`.
- In `euler_phi`, `result -= result // p` is exact integer arithmetic for $\text{result} \cdot (1 - 1/p)$ because $p$ divides the current result.

All functions were checked against brute force and the standard library (`math.gcd`, `math.lcm`, `pow(a, -1, m)`), including the RSA example above.

## Edge Cases and Pitfalls

| Case / pitfall | What goes wrong | Fix |
| --- | --- | --- |
| $n = 0, 1$ in primality | Reported as prime by a naive loop that never executes | Return `False` for $n < 2$ explicitly |
| `i * i` in C/C++/Java sieves near $10^5$ and above | 32-bit overflow wraps negative; loop misbehaves | Use 64-bit (`long long`) for `i * i`, or loop while `i <= n / i` |
| `a * b / gcd(a, b)` | Product overflows 64 bits even when the LCM fits | Compute `a / gcd(a, b) * b` |
| Product of two residues near $10^9$ | $\approx 10^{18}$ fits in signed 64-bit (max $\approx 9.2 \times 10^{18}$), but three factors do not | Reduce after **every** multiplication |
| Negative operands to `%` | C/C++/Java/Go return negative remainders | Normalize with `((x % m) + m) % m` |
| Subtraction under a modulus | `(a - b) % m` negative in C-family languages | Add `m` before taking `%` |
| Inverse when $\gcd(a, m) \ne 1$ | Fermat formula returns garbage; extended Euclid gives $g \ne 1$ | Check $\gcd$ first and handle "no inverse" |
| $\gcd(0, 0)$ | Undefined mathematically; code returns 0 | Document the convention; Python's `math.gcd(0, 0) == 0` |
| Deep recursion in `extended_gcd` | Not a real risk: depth is $O(\log n)$ | Recursive version is fine; iterative also acceptable |
| Floating-point `sqrt(n)` as loop bound | Rounding error near perfect squares for $n > 2^{52}$ | Use `d * d <= n` or `math.isqrt(n)` |

## Common Misconceptions

| Wrong belief | Correct mental model |
| --- | --- |
| "Trial division is $O(\sqrt n)$, so it is polynomial." | It is polynomial in the **value** but exponential in the **bit length**. Complexity is measured in input size. |
| "You can divide under a modulus like normal numbers." | Only multiplication by an inverse is valid, and the inverse exists only when $\gcd(b, m) = 1$. |
| "Fermat's little theorem gives inverses for any modulus." | It requires a **prime** modulus. For composite $m$ use extended Euclid (or Euler's theorem with $\varphi(m)$). |
| "Euclid's algorithm is $O(\log n)$ because it halves each step." | It halves the first argument every **two** steps; one step can shrink it very little (Fibonacci inputs). |
| "If $a \equiv b \pmod m$ then $a^k \equiv b^k$ only if $m$ is prime." | Powers and products respect congruence for **every** modulus; only division is restricted. |
| "A big random modulus makes hashing collision-free." | It reduces collision probability; it never removes collisions (pigeonhole, [Topic 1.2](topic2.md)). |

## Alternatives and Trade-offs

| Task | Method | Cost | Use when | Avoid when |
| --- | --- | --- | --- | --- |
| Primality, one $n$ | Trial division ($6k\pm1$) | $O(\sqrt n)$ | $n \le 10^{12}$–$10^{14}$, few queries | $n$ near $10^{18}$ or cryptographic sizes |
| Primality, one huge $n$ | Miller–Rabin | $O(k \log^3 n)$ bit operations | $n \le 2^{64}$ (deterministic base sets exist) or crypto sizes (probabilistic) | Many small queries — a sieve is simpler |
| Primality, many $n \le N$ | Sieve + lookup | $O(N\log\log N)$ build, $O(1)$ query | $N \le 10^7$–$10^8$ (memory) | $N$ too large to store |
| Factorize many $n \le N$ | SPF sieve | $O(\log n)$ per query | $N \le 10^7$ | Single large $n$ (use trial division or Pollard's rho) |
| $\gcd$ | Euclid | $O(\log n)$ | Default | — |
| $\gcd$ without division | Binary GCD (Stein) | $O(\log^2 n)$ bit ops | Hardware where division is slow | High-level code (built-in gcd is faster) |
| Modular inverse | Fermat $a^{p-2}$ | $O(\log p)$ | Prime modulus, already have `pow` | Composite modulus |
| Modular inverse | Extended Euclid | $O(\log m)$ | Any modulus with $\gcd(a, m) = 1$ | — |
| Inverses of $1..n$ mod $p$ | Recurrence $\text{inv}[i] = -\lfloor p/i \rfloor \cdot \text{inv}[p \bmod i]$ | $O(n)$ total | Need all of them | Need only a few |

## In Practice

- **Standard libraries.** Python: `math.gcd`, `math.lcm` (3.9+), `math.isqrt` (3.8+), `pow(a, e, m)` and `pow(a, -1, m)` (3.8+); arbitrary-precision `int` means no overflow, but big numbers cost more. C++17: `std::gcd`, `std::lcm` in `<numeric>`. Java: `BigInteger.gcd`, `modPow`, `modInverse`, `isProbablePrime`.
- **Cryptography.** TLS uses RSA or elliptic-curve keys; key generation samples random large odd numbers and runs probabilistic primality tests (Miller–Rabin). Production libraries (OpenSSL, BoringSSL, libsodium) use **constant-time** modular arithmetic so that timing does not leak secret bits — a textbook square-and-multiply that branches on the exponent bit is vulnerable to timing attacks. Never implement your own crypto for production.
- **Hashing.** Polynomial string hashes (Rabin–Karp, rolling hashes in deduplication systems such as rsync-style chunking) compute $\sum c_i B^{i} \bmod p$. Moduli such as $2^{61}-1$ (a Mersenne prime) allow fast reduction with shifts.
- **Contest moduli.** $10^9+7$ is prime and fits so that the product of two residues fits in signed 64-bit. $998\,244\,353 = 119 \cdot 2^{23} + 1$ is prime and has large power-of-two roots of unity, enabling the number-theoretic transform.
- **Performance realities.** A 64-bit division/modulo is far slower than an addition or multiplication on modern CPUs, so hot loops (hashing, NTT) often use Barrett or Montgomery reduction to replace `%` with multiplications.

## Interview and Competitive Programming

**Recognition cues**

| If you see... | Think... |
| --- | --- |
| "Output the answer modulo $10^9+7$" | Reduce after every operation; division means Fermat inverse |
| "Make all elements equal by adding/subtracting $d$" | $d$ must divide all pairwise differences: $\gcd(a_2 - a_1, \dots)$ |
| "Count numbers in $[1, N]$ coprime to $n$" | $\varphi$ or inclusion–exclusion over prime factors ([Topic 1.2](topic2.md)) |
| "Exactly 3 divisors" | $d(n) = 3 \iff n = p^2$ for prime $p$ |
| "Trailing zeros of $n!$" | Legendre's formula: exponent of $p$ in $n!$ is $\sum_{i \ge 1} \lfloor n/p^i \rfloor$; zeros $= $ exponent of 5 |
| "Solve $ax + by = c$" / "jug problems" | Extended Euclid; solvable iff $\gcd(a,b) \mid c$ |
| "Many queries: is $x$ prime / factorize $x$", $x \le 10^7$ | Sieve / SPF sieve |
| "Remainders modulo several moduli" | CRT |

**Constraints to method**

| Constraint | Feasible approach |
| --- | --- |
| One $n \le 10^{12}$ | $O(\sqrt n) = 10^6$ trial division |
| $Q \le 10^5$ queries, values $\le 10^7$ | SPF sieve, $O(\log n)$ per query |
| $n \le 10^{18}$ primality | Deterministic Miller–Rabin with 128-bit multiplication |
| Primes in $[L, R]$, $R \le 10^{12}$, $R - L \le 10^6$ | Segmented sieve |
| Exponent up to $10^{18}$ | Binary exponentiation, $\approx 60$ squarings |

**Common traps:** forgetting `long long` for products in C++; forgetting to normalize negatives; computing $\binom{n}{r} = n!/(r!(n-r)!)$ with integer division *after* reducing mod $p$; using $a^{p-2}$ when $a \equiv 0 \pmod p$.

## Using AI Assistants Critically

- LLM-generated sieves often start the inner loop at `2 * p` (correct but slower) or at `p * p` without a 64-bit guard in C++ — check the bound and the integer type.
- Generated `mod_inverse` code frequently uses `pow(a, m - 2, m)` regardless of whether `m` is prime. Ask: "what if `m = 12`?" and test it.
- C/Java code translated from Python often loses the non-negative `%` behaviour; grep for every `%` applied to a value that can be negative.
- Assistants sometimes claim trial division is "polynomial time" or that the sieve is "$O(n)$". Verify complexity claims against the bit-length argument and the harmonic-sum derivation.
- Verify with a brute-force oracle: compare `is_prime` against direct divisor counting for all $n \le 10^4$, `gcd` against `math.gcd`, and `mod_inverse(a, m)` by checking `a * inv % m == 1`.
- Property-based tests (`hypothesis`) fit naturally: for random $a, b$ assert `a * x + b * y == g` and that `g` divides both.
- Never accept AI-written cryptographic code (RSA, key generation) for production; it typically lacks padding and constant-time arithmetic.

## Practice

**Beginner**

1. *Prime counter.* Input: $N$ ($1 \le N \le 10^7$). Output: number of primes $\le N$. Constraint: 1 second. Difficulty: easy.
2. *GCD and LCM of an array.* Input: $n \le 10^5$ integers $a_i \le 10^9$. Output: $\gcd$ and $\operatorname{lcm}$ of all, the latter modulo $10^9+7$. Note: the LCM cannot be reduced modulo $p$ naively — think in prime exponents. Difficulty: easy–medium.
3. *Modular calculator.* Input: $Q$ lines `a op b` with op in $\{+,-,\times,/\}$, $0 \le a, b < 10^9+7$. Output: each result modulo $10^9+7$, or `undefined` for division by 0. Difficulty: easy.

**Intermediate**

1. *Divisor queries.* Input: $Q \le 10^5$ numbers $x_i \le 10^6$. Output: number of divisors and sum of divisors of each. Difficulty: medium.
2. *Linear Diophantine.* Input: $a, b, c$ with $|a|, |b|, |c| \le 10^9$. Output: any integer solution $(x, y)$ of $ax + by = c$, or `NO`. Difficulty: medium.
3. *Euclid step counter.* Input: $N \le 10^{18}$. Output: a pair $a, b \le N$ that maximizes the number of Euclid steps, and that number. Difficulty: medium.

**Advanced**

1. *Primes in a window.* Input: $L, R$ with $1 \le L \le R \le 10^{12}$, $R - L \le 10^6$. Output: all primes in $[L, R]$. Difficulty: medium–hard.
2. *CRT with non-coprime moduli.* Input: $k \le 10$ congruences $x \equiv r_i \pmod{m_i}$, $m_i \le 10^9$. Output: smallest non-negative solution or `NONE`. Difficulty: hard.
3. *Totients for all.* Input: $N \le 10^7$. Output: $\sum_{i=1}^{N} \varphi(i)$. Required: $O(N)$ or $O(N\log\log N)$. Difficulty: hard.

**Interview / CP**

1. *Count Primes* (LeetCode 204). Input: $n \le 5 \times 10^6$. Output: number of primes strictly less than $n$. Difficulty: medium.
2. *Codeforces 230B T-primes.* Input: $n \le 10^5$ numbers $x_i \le 10^{12}$. Output: `YES` if $x_i$ has exactly three divisors. Difficulty: medium.
3. *Water jug feasibility.* Input: capacities $x, y \le 10^6$ and target $z$. Output: whether $z$ litres can be measured. Hint-free; difficulty: medium.

## Self-Check Questions

??? question "Q1. Why does Euclid's algorithm terminate, and why is it logarithmic rather than linear?"

    The second argument is a remainder, strictly smaller than the previous second argument and non-negative, so it reaches 0. It is logarithmic because every two steps the first argument at least halves: if $b \le a/2$ the next remainder is below $b \le a/2$; otherwise $a \bmod b = a - b < a/2$.

??? question "Q2. Is $O(\sqrt n)$ trial division a polynomial-time algorithm? Justify in terms of input size."

    No. The input is $n$ in $b = \Theta(\log n)$ bits, and $\sqrt n = 2^{b/2}$, which is exponential in $b$. Polynomial time means polynomial in the input length. Euclid's $O(\log n)$ steps, by contrast, is polynomial (linear) in $b$.

??? question "Q3. Does 6 have an inverse modulo 9? Modulo 35? Find it if it exists."

    $\gcd(6, 9) = 3 \ne 1$, so no inverse modulo 9. $\gcd(6, 35) = 1$, so it exists: $6 \cdot 6 = 36 \equiv 1 \pmod{35}$, so $6^{-1} \equiv 6$.

??? question "Q4. Why does the sieve start crossing out at $p^2$ and stop the outer loop at $\sqrt N$?"

    Any multiple $kp$ with $k < p$ has a prime factor of $k$ that is smaller than $p$, so it was already crossed out. If $p > \sqrt N$ then $p^2 > N$, so there is nothing new left for $p$ to cross out; every composite $\le N$ has a prime factor $\le \sqrt N$.

??? question "Q5. A teammate computes $\binom{n}{r} \bmod p$ as `(fact[n] // (fact[r] * fact[n-r])) % p` where `fact` is stored modulo $p$. What is wrong?"

    Integer division of residues is meaningless: `fact[n]` has already been reduced, so it need not be divisible by the reduced denominator. Replace division by multiplication with the modular inverse of the denominator (Fermat, since $p$ is prime): `fact[n] * inv(fact[r]) * inv(fact[n-r]) % p`.

??? question "Q6. Prove that the number of steps of Euclid on $(F_{k+1}, F_k)$ is $k - 1$ for $k \ge 2$ and explain why this is the worst case."

    $F_{k+1} \bmod F_k = F_{k-1}$ (the quotient is 1 for $k \ge 3$), so each step moves to the previous Fibonacci pair, ending at $(F_3, F_2) = (2, 1) \to (1, 0)$. Every quotient being 1 means each remainder is as large as possible, so the sequence shrinks as slowly as possible; Lamé's theorem formalizes that any pair needing $k$ steps has $b \ge F_{k+1}$.

??? question "Q7. Your hash table uses `h(k) = k mod 1000` and keys are order IDs that are always multiples of 8. What happens and how would you fix it?"

    $\gcd(8, 1000) = 8$, so $k \bmod 1000$ is always a multiple of 8: only 125 of the 1000 buckets are ever used, multiplying collisions by 8. Use a prime table size (or a good mixing hash function) so that common factors in keys do not collapse the bucket range.

??? question "Q8. Compare Fermat and extended Euclid for computing $a^{-1} \bmod m$."

    Both cost $O(\log m)$ arithmetic operations. Fermat ($a^{m-2}$) needs only `pow`, but is valid only for prime $m$ and $a \not\equiv 0$. Extended Euclid works for any $m$ with $\gcd(a, m) = 1$ and also **detects** non-invertibility (returns $g \ne 1$). Prefer extended Euclid when the modulus is not guaranteed prime.

## Complexity Summary

| Operation | Time | Space | Notes |
| --- | --- | --- | --- |
| Trial division | $O(\sqrt n)$ | $O(1)$ | Exponential in bit length |
| Sieve of Eratosthenes | $O(N \log\log N)$ | $O(N)$ | Harmonic sum over primes |
| Linear sieve | $O(N)$ | $O(N)$ | Each composite crossed once |
| SPF factorization query | $O(\log n)$ | $O(N)$ table | After sieve |
| Segmented sieve on $[L, R]$ | $O(\sqrt R + (R-L)\log\log R)$ | $O(\sqrt R + R - L)$ | |
| Euclid / extended Euclid | $O(\log \min(a,b))$ | $O(1)$ / $O(\log)$ recursion | Worst case: Fibonacci inputs |
| Modular inverse | $O(\log m)$ | $O(1)$ | Fermat (prime $m$) or extended Euclid |
| Modular exponentiation | $O(\log e)$ multiplications | $O(1)$ | See [Unit 4.6](../unit4/topic6.md) |
| $\varphi(n)$ for one $n$ | $O(\sqrt n)$ | $O(1)$ | Trial division factorization |
| CRT, two moduli | $O(\log \min(m_1, m_2))$ | $O(1)$ | |

## Key Takeaways

- Replace big problems by remainders: $\gcd(a,b) = \gcd(b, a \bmod b)$ and $(a \cdot b) \bmod m$ depends only on the residues.
- Euclid is $O(\log n)$ because the first argument halves every two steps; Fibonacci pairs are the worst case.
- An inverse modulo $m$ exists iff $\gcd(a, m) = 1$; Fermat's $a^{p-2}$ only works for prime $p$.
- Measure number-theoretic complexity in **bits**: $O(\sqrt n)$ is exponential, $O(\log n)$ is efficient.
- Sieve for many small numbers, trial division for a few medium numbers, Miller–Rabin for huge numbers.
- In C-family languages, reduce after every multiplication and normalize negative remainders; Python avoids overflow but not the cost of big integers.
- RSA, hashing and contest "mod $10^9+7$" problems all reuse the same four tools: gcd, extended Euclid, modular inverse, fast modular power.
