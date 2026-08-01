# Unit 1 — Mathematics for Competitive Programming

!!! abstract "Unit Overview"
    This unit covers the mathematical toolkit that appears constantly in programming
    contests: **number theory** (primes, GCD/LCM, modular arithmetic), **combinatorics**
    (Fibonacci, binomial coefficients, Catalan numbers), the **cycle-finding problem**
    (Floyd's algorithm), and the **basics of game theory** (N/P positions, Nim,
    Sprague–Grundy). Every section pairs theory with contest-ready C++ implementations
    and complexity analysis.

---

## 1.1 Number Theory

Number theory is the study of integers and their properties. In competitive programming
it dominates problems involving divisibility, primes, remainders, and counting under a
modulus (typically $10^9 + 7$ or $998\,244\,353$).

### 1.1.1 Prime Numbers, Optimized Trial Division, Modified Sieve

#### Prime numbers — definitions

A **prime** is an integer $p > 1$ whose only positive divisors are $1$ and $p$.
An integer $n > 1$ that is not prime is **composite**. The number $1$ is neither.

Key facts used in contests:

- **Fundamental Theorem of Arithmetic:** every integer $n > 1$ has a *unique*
  factorization $n = p_1^{e_1} p_2^{e_2} \cdots p_k^{e_k}$ (up to ordering).
- **Density:** by the Prime Number Theorem, $\pi(n) \approx \dfrac{n}{\ln n}$.
  There are about $78{,}498$ primes below $10^6$ and $50{,}847{,}534$ below $10^9$.
- If $n$ is composite, it has a prime factor $p \le \sqrt{n}$. This single fact powers
  trial division.

#### Naive trial division — $O(n)$

```cpp
bool isPrimeNaive(long long n) {
    if (n < 2) return false;
    for (long long d = 2; d < n; d++)
        if (n % d == 0) return false;
    return true;
}
```

Testing every $d < n$ is hopeless for large $n$. We optimize in stages.

#### Optimized trial division — $O(\sqrt{n})$ and the $6k \pm 1$ trick

**Stage 1 — stop at $\sqrt{n}$:** divisors come in pairs $(d, n/d)$; if $d > \sqrt{n}$
then $n/d < \sqrt{n}$, so checking up to $\sqrt{n}$ suffices.

**Stage 2 — skip even numbers:** after checking $2$, test only odd candidates.
This halves the work.

**Stage 3 — the $6k \pm 1$ optimization:** every integer can be written as
$6k + r$ with $r \in \{0,1,2,3,4,5\}$. Of these, $6k$, $6k+2$, $6k+4$ are divisible
by $2$ and $6k+3$ is divisible by $3$. Hence **every prime $> 3$ has the form
$6k \pm 1$**. Testing only those candidates cuts the work to one third.

```cpp
bool isPrime(long long n) {
    if (n < 2)              return false;
    if (n < 4)              return true;      // 2, 3
    if (n % 2 == 0 || n % 3 == 0) return false;
    for (long long d = 5; d * d <= n; d += 6)
        if (n % d == 0 || n % (d + 2) == 0)   // tests 6k-1 and 6k+1
            return false;
    return true;
}
```

| Version | Candidates tested | Complexity | Practical limit (1 s) |
|---|---|---|---|
| Naive | all $d < n$ | $O(n)$ | $n \approx 10^8$ (single test) |
| Stop at $\sqrt n$ | $d \le \sqrt n$ | $O(\sqrt n)$ | $n \approx 10^{14}$ |
| Odd only | $\tfrac{1}{2}\sqrt n$ | $O(\sqrt n)$ | $\approx 2\times$ faster |
| $6k \pm 1$ | $\tfrac{1}{3}\sqrt n$ | $O(\sqrt n)$ | $\approx 3\times$ faster |

!!! tip "When to use which"
    Trial division is ideal for **a few queries on large numbers** (up to
    $\sim 10^{14}$). For **many queries on numbers up to $\sim 10^7$**, precompute a
    sieve instead. For a handful of *very* large numbers ($> 10^{16}$), the
    deterministic Miller–Rabin test is the contest-standard tool.

#### Sieve of Eratosthenes — $O(n \log \log n)$

Generates *all* primes up to $n$ by iteratively crossing out multiples of each prime.

```cpp
const int N = 10'000'000;
vector<bool> isComposite(N + 1, false);
vector<int> primes;

void sieve() {
    for (int i = 2; i <= N; i++) {
        if (!isComposite[i]) {
            primes.push_back(i);
            for (long long j = (long long)i * i; j <= N; j += i)
                isComposite[j] = true;         // start at i*i, not 2*i
        }
    }
}
```

Two classic optimizations are already included:

1. **Start crossing at $i^2$** — every smaller multiple $i \cdot k$ ($k < i$) was
   already removed by the smaller prime factor of $k$.
2. **`long long` for `i * i`** — avoids overflow when $i$ is near $10^7$... a classic
   silent bug in contests.

#### Modified sieves

The plain sieve stores only a yes/no answer. **Modified sieves** store richer
information in the same pass — this is where most contest value lies.

**(a) Smallest Prime Factor (SPF) sieve — factorize any $n \le N$ in $O(\log n)$:**

```cpp
vector<int> spf(N + 1);

void spfSieve() {
    for (int i = 2; i <= N; i++)
        if (spf[i] == 0)
            for (int j = i; j <= N; j += i)
                if (spf[j] == 0) spf[j] = i;
}

vector<pair<int,int>> factorize(int n) {      // (prime, exponent) pairs
    vector<pair<int,int>> f;
    while (n > 1) {
        int p = spf[n], e = 0;
        while (n % p == 0) n /= p, e++;
        f.push_back({p, e});
    }
    return f;
}
```

After $O(n \log \log n)$ preprocessing, **each factorization query costs only
$O(\log n)$** — compare with $O(\sqrt n)$ per query by trial division. Essential for
problems with $10^5$–$10^6$ factorization queries.

**(b) Linear (Euler) sieve — $O(n)$, each composite crossed exactly once:**

```cpp
vector<int> lp(N + 1);      // lp[i] = least prime factor
vector<int> pr;             // list of primes

void linearSieve() {
    for (int i = 2; i <= N; i++) {
        if (lp[i] == 0) { lp[i] = i; pr.push_back(i); }
        for (int p : pr) {
            if (p > lp[i] || (long long)p * i > N) break;
            lp[p * i] = p;  // p*i is crossed only by its least prime factor p
        }
    }
}
```

Its real power: multiplicative functions such as Euler's totient $\varphi$ or the
number-of-divisors function $d(n)$ can be computed **for all $n \le N$ in $O(n)$**
alongside the sieve.

**(c) Segmented sieve** — primes in a window $[L, R]$ with $R \le 10^{12}$ but
$R - L \le 10^6$: sieve $[2, \sqrt R]$ first, then cross multiples of those primes
inside the segment. Memory drops from $O(R)$ to $O(\sqrt R + (R - L))$.

**(d) Divisor-count / divisor-sum sieve** — harmonic-series double loop:

```cpp
vector<int> numDiv(N + 1, 0);
for (int i = 1; i <= N; i++)
    for (int j = i; j <= N; j += i)
        numDiv[j]++;                 // O(n log n) total
```

---

### 1.1.2 Greatest Common Divisor & Least Common Multiple

#### Definitions

- $\gcd(a, b)$: the largest integer dividing both $a$ and $b$.
- $\operatorname{lcm}(a, b)$: the smallest positive integer divisible by both.

#### Euclid's algorithm

Built on the identity $\gcd(a, b) = \gcd(b,\ a \bmod b)$, with base case
$\gcd(a, 0) = a$.

```cpp
long long gcd(long long a, long long b) {
    while (b) { a %= b; swap(a, b); }
    return a;
}
// or simply: __gcd(a, b) / std::gcd(a, b) in C++17
```

**Complexity:** $O(\log \min(a, b))$. The worst case is consecutive Fibonacci
numbers (Lamé's theorem) — the remainder sequence shrinks slowest there.

#### LCM via GCD

$$
\gcd(a,b) \cdot \operatorname{lcm}(a,b) = a \cdot b
\quad\Longrightarrow\quad
\operatorname{lcm}(a,b) = \frac{a}{\gcd(a,b)} \cdot b
$$

```cpp
long long lcm(long long a, long long b) {
    return a / gcd(a, b) * b;        // divide FIRST to avoid overflow
}
```

!!! warning "Overflow pitfall"
    Computing `a * b / gcd(a, b)` can overflow `long long` even when the final LCM
    fits. Always divide before multiplying.

#### Properties worth memorizing

| Property | Statement |
|---|---|
| Associativity | $\gcd(a, b, c) = \gcd(\gcd(a,b), c)$ — extends to arrays |
| Distributive | $\gcd(ka, kb) = k \gcd(a, b)$ |
| Coprimality | $a, b$ coprime $\iff \gcd(a,b) = 1$ |
| Via factorization | $\gcd$: take **min** exponents; $\operatorname{lcm}$: take **max** exponents |
| Bézout | $\exists\, x, y \in \mathbb{Z}: ax + by = \gcd(a,b)$ |

Prime-exponent view example: $a = 2^3 \cdot 3^1,\ b = 2^1 \cdot 3^2$
$\Rightarrow \gcd = 2^1 3^1 = 6$, $\operatorname{lcm} = 2^3 3^2 = 72$.

---

### 1.1.3 Modular Arithmetic, Extended Euclidean Algorithm

#### Why we compute modulo a number

Contest answers often grow astronomically (e.g., $1000!$ has $2568$ digits), so
problems ask for the answer **mod** $m$, usually $m = 10^9 + 7$ (a prime). Modular
arithmetic lets us keep every intermediate value small.

#### Core rules

For any integers $a, b$ and modulus $m$:

$$
\begin{aligned}
(a + b) \bmod m &= \big((a \bmod m) + (b \bmod m)\big) \bmod m \\
(a - b) \bmod m &= \big((a \bmod m) - (b \bmod m) + m\big) \bmod m \\
(a \cdot b) \bmod m &= \big((a \bmod m)(b \bmod m)\big) \bmod m
\end{aligned}
$$

!!! warning "Two classic bugs"
    1. **Negative remainders:** in C++, `(-7) % 3 == -1`. Normalize with
       `((x % m) + m) % m`.
    2. **Division does *not* distribute:** $(a/b) \bmod m \ne (a \bmod m)/(b \bmod m)$.
       Division requires a **modular inverse** (below).

#### Fast modular exponentiation — $O(\log e)$

Repeated squaring: to get $b^e$, square-and-multiply following the bits of $e$.

```cpp
long long power(long long b, long long e, long long m) {
    long long r = 1; b %= m;
    while (e > 0) {
        if (e & 1) r = r * b % m;
        b = b * b % m;
        e >>= 1;
    }
    return r;
}
```

#### Modular inverse

The inverse of $a$ modulo $m$ is $a^{-1}$ with $a \cdot a^{-1} \equiv 1 \pmod m$.
It **exists iff $\gcd(a, m) = 1$**. Two standard routes:

1. **Fermat's little theorem** (when $m$ is prime):
   $a^{m-1} \equiv 1 \pmod m \Rightarrow a^{-1} \equiv a^{m-2} \pmod m$.
   One `power(a, m-2, m)` call — the go-to for $10^9+7$.
2. **Extended Euclidean algorithm** (any coprime $m$) — next.

#### Extended Euclidean Algorithm

Ordinary Euclid returns only $\gcd(a,b)$. The **extended** version also returns the
Bézout coefficients $x, y$ satisfying

$$
a x + b y = \gcd(a, b).
$$

Recurrence: if $(x_1, y_1)$ solves the subproblem for $(b,\ a \bmod b)$, then

$$
x = y_1, \qquad y = x_1 - \left\lfloor \tfrac{a}{b} \right\rfloor y_1 .
$$

```cpp
long long extgcd(long long a, long long b, long long &x, long long &y) {
    if (b == 0) { x = 1; y = 0; return a; }
    long long x1, y1;
    long long g = extgcd(b, a % b, x1, y1);
    x = y1;
    y = x1 - (a / b) * y1;
    return g;
}

long long modInverse(long long a, long long m) {   // requires gcd(a, m) == 1
    long long x, y;
    extgcd(a, m, x, y);          // a*x + m*y = 1  =>  a*x ≡ 1 (mod m)
    return ((x % m) + m) % m;
}
```

**Worked example.** Find $3^{-1} \pmod{11}$.
Extended Euclid on $(3, 11)$ gives $3 \cdot 4 + 11 \cdot (-1) = 1$, so
$3^{-1} \equiv 4 \pmod{11}$. Check: $3 \times 4 = 12 \equiv 1$. ✔

**Other uses of extgcd:**

- **Linear Diophantine equations** $ax + by = c$: solvable iff $\gcd(a,b) \mid c$;
  scale the Bézout solution by $c / \gcd(a,b)$; the full family is
  $x = x_0 + t\,\tfrac{b}{g}$, $y = y_0 - t\,\tfrac{a}{g}$.
- **Chinese Remainder Theorem** constructions (merging congruences).
- Inverses when the modulus is **not prime** (Fermat unavailable).

---

### 1.1.4 Number Theory in Programming Competitions

How the pieces above combine into recurring contest patterns:

**1. Prime factorization drives counting.** If
$n = p_1^{e_1} \cdots p_k^{e_k}$, then

$$
d(n) = \prod_{i=1}^{k} (e_i + 1),
\qquad
\sigma(n) = \prod_{i=1}^{k} \frac{p_i^{e_i+1} - 1}{p_i - 1},
\qquad
\varphi(n) = n \prod_{i=1}^{k}\Big(1 - \frac{1}{p_i}\Big).
$$

Example: $n = 60 = 2^2 \cdot 3 \cdot 5 \Rightarrow d(60) = 3 \cdot 2 \cdot 2 = 12$
divisors.

**2. Choose the right primality tool by constraints.**

| Constraint pattern | Tool |
|---|---|
| Single $n \le 10^{14}$ | $O(\sqrt n)$ trial division ($6k\pm1$) |
| $Q \le 10^6$ queries, $n \le 10^7$ | Sieve + $O(1)$ lookup |
| Factorize $Q$ numbers $\le 10^7$ | SPF sieve, $O(\log n)$ each |
| Primes in $[L, R]$, $R \le 10^{12}$ | Segmented sieve |
| $n$ up to $10^{18}$ | Deterministic Miller–Rabin |

**3. Everything big is done mod $10^9+7$.** Factorials, powers, DP counts —
precompute factorials and inverse factorials once, then answer $\binom{n}{r}$ queries
in $O(1)$ (code in §1.2.1).

**4. GCD patterns.** Range-GCD (sparse tables — GCD is idempotent), reducing
fractions before comparing, "make all elements equal by adding $d$" problems
($d \mid$ pairwise differences), and coprimality counting via $\varphi$ or
inclusion–exclusion.

**5. Classic theorem name-drops** you should recognize on sight: Fermat's little
theorem (inverses), Euler's theorem ($a^{\varphi(m)} \equiv 1$ for coprime $a$),
Wilson's theorem ($(p-1)! \equiv -1 \pmod p$), CRT (merging congruences), and
Legendre's formula (exponent of prime $p$ in $n!$ is $\sum_{i\ge1} \lfloor n/p^i \rfloor$
— e.g., trailing zeros of $n!$).

!!! example "Representative problems"
    - *UVa 10394 — Twin Primes* (sieve)
    - *Codeforces 230B — T-primes* (numbers with exactly 3 divisors = squares of primes)
    - *SPOJ PRIME1* (segmented sieve)
    - *UVa 10104 — Euclid Problem* (extended Euclid, output $x, y, g$)
    - Any "count ways … mod $10^9+7$" problem (modular arithmetic + inverses)

---

## 1.2 Combinatorics

Combinatorics is the art of counting without enumerating. Most contest combinatorics
reduces to a recurrence (solved by DP) or a closed-form product (solved with modular
factorials).

### 1.2.1 Fibonacci Numbers, Binomial Coefficients

#### Fibonacci numbers

$$
F_0 = 0,\quad F_1 = 1,\quad F_n = F_{n-1} + F_{n-2}
$$

giving $0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, \dots$

**Computation strategies:**

| Method | Complexity | Notes |
|---|---|---|
| Naive recursion | $O(\phi^n)$ — exponential | never in contests |
| Bottom-up DP / iteration | $O(n)$ | fine for $n \le 10^7$ |
| **Matrix exponentiation** | $O(\log n)$ | for $n$ up to $10^{18}$ (mod $m$) |
| Fast doubling | $O(\log n)$ | same power, less code |

```cpp
// Iterative, O(n)
long long fib(int n) {
    long long a = 0, b = 1;
    while (n--) { long long c = a + b; a = b; b = c; }
    return a;
}
```

**Matrix exponentiation identity:**

$$
\begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}^{\!n}
=
\begin{pmatrix} F_{n+1} & F_n \\ F_n & F_{n-1} \end{pmatrix}
$$

Raise the matrix to the $n$-th power by repeated squaring — $O(\log n)$
multiplications — to get $F_n \bmod m$ for gigantic $n$.

**Fast-doubling formulas** (equivalent power, no matrices):

$$
F_{2k} = F_k\,(2F_{k+1} - F_k), \qquad F_{2k+1} = F_k^2 + F_{k+1}^2 .
$$

**Useful facts:**

- **Closed form (Binet):** $F_n = \dfrac{\phi^n - \psi^n}{\sqrt 5}$ with
  $\phi = \tfrac{1+\sqrt5}{2} \approx 1.618$; growth is exponential —
  $F_{93}$ already overflows `unsigned long long`.
- **Zeckendorf's theorem:** every positive integer is a unique sum of
  non-consecutive Fibonacci numbers (greedy construction works).
- **Pisano period:** $F_n \bmod m$ is periodic (e.g., period $60$ for $m = 10$) —
  key for "last digit of $F_{10^{18}}$" problems.
- $\gcd(F_m, F_n) = F_{\gcd(m,n)}$ — a beautiful bridge back to §1.1.2.
- Counting interpretations: ways to tile a $2 \times n$ strip with dominoes,
  ways to climb $n$ stairs taking 1 or 2 steps, binary strings with no two
  consecutive 1s — all Fibonacci.

#### Binomial coefficients

$$
\binom{n}{k} = \frac{n!}{k!\,(n-k)!}
$$

counts the ways to choose $k$ objects from $n$ (order irrelevant).

**Pascal's rule** — the DP view:

$$
\binom{n}{k} = \binom{n-1}{k-1} + \binom{n-1}{k},
\qquad \binom{n}{0} = \binom{n}{n} = 1 .
$$

("Either item $n$ is chosen, or it isn't.")

```cpp
// Pascal's triangle, O(n^2) — safe, no division, works mod anything
long long C[MAXN][MAXN];
for (int i = 0; i < MAXN; i++) {
    C[i][0] = 1;
    for (int j = 1; j <= i; j++)
        C[i][j] = (C[i-1][j-1] + C[i-1][j]) % MOD;
}
```

**Factorial precomputation — the contest workhorse.** For up to $10^6$-scale $n$
with prime modulus, precompute factorials and inverse factorials once; each query is
then $O(1)$:

```cpp
const long long MOD = 1e9 + 7;
const int MX = 1'000'000;
long long fact[MX + 1], inv_fact[MX + 1];

void precompute() {
    fact[0] = 1;
    for (int i = 1; i <= MX; i++) fact[i] = fact[i-1] * i % MOD;
    inv_fact[MX] = power(fact[MX], MOD - 2, MOD);      // Fermat inverse
    for (int i = MX; i >= 1; i--) inv_fact[i-1] = inv_fact[i] * i % MOD;
}

long long nCr(int n, int r) {
    if (r < 0 || r > n) return 0;
    return fact[n] * inv_fact[r] % MOD * inv_fact[n-r] % MOD;
}
```

Notice how this fuses §1.1.3 (modular inverse via Fermat + fast power) with
combinatorics — the single most reused snippet in counting problems.

**Identities to recognize:**

$$
\sum_{k=0}^{n} \binom{n}{k} = 2^n, \qquad
\binom{n}{k} = \binom{n}{n-k}, \qquad
(x+y)^n = \sum_{k=0}^n \binom{n}{k} x^k y^{n-k}
$$

plus the **hockey stick** identity
$\sum_{i=r}^{n} \binom{i}{r} = \binom{n+1}{r+1}$ and **stars and bars**: the number of
non-negative integer solutions of $x_1 + \dots + x_k = n$ is $\binom{n+k-1}{k-1}$.
For huge $n$ with small prime modulus, **Lucas' theorem** computes
$\binom{n}{k} \bmod p$ digit-by-digit in base $p$.

### 1.2.2 Catalan Numbers

$$
C_n = \frac{1}{n+1}\binom{2n}{n} = \frac{(2n)!}{(n+1)!\,n!}
$$

Sequence: $1, 1, 2, 5, 14, 42, 132, 429, 1430, \dots$

**Recurrences:**

$$
C_{n+1} = \sum_{i=0}^{n} C_i \, C_{n-i}
\qquad\text{(segmented / divide form, } O(n^2)\text{)}
$$

$$
C_{n+1} = \frac{2(2n+1)}{n+2}\,C_n
\qquad\text{(} O(n) \text{ with modular inverses)}
$$

```cpp
// O(n) Catalan mod p using precomputed factorials (§1.2.1)
long long catalan(int n) {
    return fact[2*n] * inv_fact[n] % MOD * inv_fact[n+1] % MOD;
}
```

**What Catalan counts** — the pattern to recognize is *"balanced / non-crossing /
never-go-below-zero"* structures:

| Structure | Count |
|---|---|
| Balanced strings of $n$ '(' and $n$ ')' | $C_n$ |
| Distinct **BSTs** (binary search trees) on $n$ keys | $C_n$ |
| Full binary trees with $n+1$ leaves | $C_n$ |
| Triangulations of a convex $(n+2)$-gon | $C_n$ |
| Monotonic lattice paths $(0,0) \to (n,n)$ not crossing the diagonal (Dyck paths) | $C_n$ |
| Ways to fully parenthesize $n+1$ factors | $C_n$ |
| Non-crossing handshakes of $2n$ people around a table | $C_n$ |

**Why the formula works (ballot/reflection argument, sketch):** of the
$\binom{2n}{n}$ unrestricted paths from $(0,0)$ to $(n,n)$, each *bad* path (one that
crosses the diagonal) reflects bijectively to a path ending at $(n-1, n+1)$, of which
there are $\binom{2n}{n+1}$. Hence
$C_n = \binom{2n}{n} - \binom{2n}{n+1} = \frac{1}{n+1}\binom{2n}{n}$.

!!! example "Contest cue"
    If a counting problem answer begins $1, 2, 5, 14, 42, \dots$ for small cases —
    it is almost certainly Catalan. Compute small cases by brute force first, then
    match against OEIS-famous sequences (Fibonacci, Catalan, powers of two).

---

## 1.3 Cycle-Finding Problem, Floyd's Algorithm

### The problem

Given a function $f: S \to S$ on a **finite** set and a start value $x_0$, the
iterated sequence

$$
x_0,\; x_1 = f(x_0),\; x_2 = f(x_1),\; \dots
$$

must eventually repeat (pigeonhole principle). Its shape is the Greek letter **ρ
(rho)**: a *tail* of length $\mu$ followed by a *cycle* of length $\lambda$:

$$
\underbrace{x_0, x_1, \dots, x_{\mu-1}}_{\text{tail, length } \mu},\;
\underbrace{x_\mu, \dots, x_{\mu+\lambda-1}}_{\text{cycle, length } \lambda},\;
x_{\mu+\lambda} = x_\mu, \dots
$$

**Goal:** find $\mu$ and $\lambda$ — ideally in $O(\mu + \lambda)$ time and
$O(1)$ memory. (Storing every value in a hash set also works but costs
$O(\mu + \lambda)$ **memory**, which fails when states are huge, e.g., pseudorandom
generators.)

### Floyd's Tortoise and Hare algorithm

Two pointers move at different speeds:

- **Tortoise:** one step per tick, $x_{i+1} = f(x_i)$.
- **Hare:** two steps per tick, $x_{2(i+1)} = f(f(x_{2i}))$.

**Phase 1 — meeting inside the cycle.** Once both pointers are in the cycle, the
hare gains one position per tick, so they must meet. If they meet at index $i$,
then $i \equiv 2i \pmod{\lambda}$, i.e., $\lambda \mid i$ — the meeting index is a
multiple of the cycle length.

**Phase 2 — finding $\mu$.** Reset the hare to $x_0$; move **both** one step per
tick. Because the tortoise sits at a position $\equiv$ (multiple of $\lambda$) into
the rho, after exactly $\mu$ more steps both pointers coincide at $x_\mu$ — the
cycle's entry point.

**Phase 3 — finding $\lambda$.** Freeze the tortoise at $x_\mu$; walk the hare
around once, counting steps until it returns.

```cpp
// Returns (mu, lambda) for sequence x0, f(x0), f(f(x0)), ...
pair<int,int> floydCycle(function<int(int)> f, int x0) {
    // Phase 1: find a meeting point inside the cycle
    int t = f(x0), h = f(f(x0));
    while (t != h) { t = f(t); h = f(f(h)); }

    // Phase 2: find mu (start of the cycle)
    int mu = 0; h = x0;
    while (t != h) { t = f(t); h = f(h); mu++; }

    // Phase 3: find lambda (cycle length)
    int lambda = 1; h = f(t);
    while (t != h) { h = f(h); lambda++; }

    return {mu, lambda};
}
```

**Complexity:** $O(\mu + \lambda)$ time, $O(1)$ memory. (Brent's algorithm is a
constant-factor-faster variant that only teleports the tortoise at powers of two —
worth knowing by name.)

### Where it shows up

- **Linked-list cycle detection** (LeetCode 141/142 — *find the duplicate number* is
  literally Phase 2).
- **Pseudorandom sequences:** period of an LCG $x_{i+1} = (a x_i + b) \bmod m$.
- **Pollard's rho factorization** — the famous $O(n^{1/4})$ integer factoring
  heuristic runs Floyd/Brent on $f(x) = x^2 + c \bmod n$.
- **Digit-process iterations:** e.g., "happy numbers", repeated digit-sum-of-squares —
  detect when the process loops.
- **Function-graph problems:** every node has out-degree 1 ⇒ each component is a rho;
  many Codeforces problems ask for cycle entry/length per node.

!!! example "Worked micro-example"
    $f(x) = (x^2 + 1) \bmod 10$, $x_0 = 3$ gives
    $3 \to 0 \to 1 \to 2 \to 5 \to 6 \to 7 \to 0 \to \dots$
    Tail $= \{3\}$ so $\mu = 1$; cycle $= (0,1,2,5,6,7)$ so $\lambda = 6$.

---

## 1.4 Basics of Game Theory

Contest game theory concerns **two-player, perfect-information, impartial games**:
both players see everything, moves available depend only on the position (not on
*who* moves), and — under the **normal play convention** — the player who cannot
move **loses**. Both players play optimally.

### Winning and losing positions (N / P positions)

- **P-position** (Previous player wins) — the player **about to move loses**.
- **N-position** (Next player wins) — the player **about to move wins**.

Classification rules (backward induction):

1. Every **terminal** position (no moves) is a **P-position**.
2. A position is an **N-position** if **at least one** move leads to a P-position.
3. A position is a **P-position** if **every** move leads to an N-position.

Your strategy as the winner: always move to a P-position, handing your opponent a
lost game.

!!! example "Take-away game (1, 2, or 3 stones)"
    A pile of $n$ stones; a move removes 1–3 stones; taking the last stone wins.
    Working backwards: $n=0$ is P; $n = 1,2,3$ are N (move to 0);
    $n = 4$ is P (all moves land on N); pattern:
    **P-positions are exactly $n \equiv 0 \pmod 4$.**
    Winning strategy: always leave a multiple of 4.

```cpp
// Generic win/lose DP: O(states × moves)
bool winning(int n) {                 // take-away 1..3 game
    vector<char> win(n + 1, false);   // win[0] = false (P-position)
    for (int i = 1; i <= n; i++)
        for (int k = 1; k <= 3 && k <= i; k++)
            if (!win[i - k]) { win[i] = true; break; }
    return win[n];
}
```

### Nim — the canonical impartial game

$k$ piles of stones; a move removes **any positive number** from **one** pile;
last stone wins.

**Bouton's theorem:** the position $(a_1, a_2, \dots, a_k)$ is a **P-position iff**

$$
a_1 \oplus a_2 \oplus \cdots \oplus a_k = 0
$$

where $\oplus$ is bitwise XOR (the **nim-sum**).

*Why it works:* from a zero-XOR position every move breaks the balance (XOR becomes
nonzero); from a nonzero-XOR position there is always a move restoring XOR $= 0$ —
reduce the pile containing the highest set bit of the nim-sum $s$ from $a_i$ to
$a_i \oplus s$.

```cpp
bool firstPlayerWinsNim(const vector<long long>& a) {
    long long x = 0;
    for (long long v : a) x ^= v;
    return x != 0;                    // nonzero nim-sum => N-position
}
```

!!! example "Nim (3, 4, 5)"
    $3 \oplus 4 \oplus 5 = 2 \ne 0$ — first player wins. The winning move: change
    the pile of 3 to $3 \oplus 2 = 1$, i.e., take 2 stones from it, leaving
    $(1, 4, 5)$ with nim-sum $0$.

### Sprague–Grundy theory (the unifying theorem)

Every impartial game position is equivalent to a Nim pile of size $g(v)$ — its
**Grundy number** (nimber):

$$
g(v) = \operatorname{mex}\big(\{\, g(u) : v \to u \text{ is a legal move} \,\}\big)
$$

where $\operatorname{mex}(S)$ = minimum excludant = smallest non-negative integer not
in $S$. For example $\operatorname{mex}\{0,1,3\} = 2$, $\operatorname{mex}\{\} = 0$.

Consequences:

- $g(v) = 0 \iff v$ is a **P-position**.
- **Sums of games** (several independent boards, a move plays in exactly one):
  the combined position's Grundy value is the **XOR** of the components' values.
  This is why Nim's answer is a XOR — each pile is an independent game with
  $g(\text{pile of } n) = n$.

```cpp
// Grundy numbers for a subtraction game with move set M
int grundy(int n, const vector<int>& M, vector<int>& g) {
    if (g[n] != -1) return g[n];
    set<int> s;
    for (int m : M) if (m <= n) s.insert(grundy(n - m, M, g));
    int mex = 0;
    while (s.count(mex)) mex++;
    return g[n] = mex;
}
```

**Standard workflow for an unfamiliar game:**

1. Write the brute-force Grundy/win-lose DP for small states.
2. Print a table and **hunt for the pattern** (periodicity is extremely common —
   e.g., take-away(1..3) has $g(n) = n \bmod 4$).
3. Prove or trust the pattern; answer huge inputs with the closed form.
4. If the game splits into independent parts, XOR the Grundy values.

**Named games worth recognizing:** Nim and Misère Nim (last stone *loses* — same
strategy except when all piles are size 1), subtraction games, Wythoff's game
(two piles, take from one or equally from both — P-positions follow the golden
ratio), and Green Hackenbush.

!!! example "Representative problems"
    - *UVa 10165 — Stone Game* (pure Nim)
    - *Codeforces — Game of Stones / divide-and-Grundy variants*
    - *SPOJ MMMGAME / TRANSMIT* (Sprague–Grundy on composite games)

---

## Quick Revision Matrix

| Topic | Key result | Complexity | Snippet |
|---|---|---|---|
| Primality (single $n$) | $6k \pm 1$ trial division | $O(\sqrt n)$ | `isPrime` |
| Primes up to $N$ | Sieve of Eratosthenes | $O(N \log\log N)$ | `sieve` |
| Factorize many | SPF sieve | $O(\log n)$/query | `spfSieve` |
| GCD / LCM | Euclid; `a/g*b` | $O(\log \min)$ | `gcd` |
| $b^e \bmod m$ | Binary exponentiation | $O(\log e)$ | `power` |
| $a^{-1} \bmod m$ | Fermat ($m$ prime) / extgcd | $O(\log m)$ | `modInverse` |
| $F_n$, huge $n$ | Matrix power / fast doubling | $O(\log n)$ | — |
| $\binom{n}{r} \bmod p$ | Factorial + inverse factorial tables | $O(1)$/query | `nCr` |
| Catalan $C_n$ | $\frac{1}{n+1}\binom{2n}{n}$ | $O(1)$/query | `catalan` |
| Cycle $(\mu, \lambda)$ | Floyd tortoise–hare | $O(\mu+\lambda)$, $O(1)$ mem | `floydCycle` |
| Impartial games | mex / Grundy, XOR of components | DP over states | `grundy` |
| Nim | P-position $\iff$ nim-sum $=0$ | $O(k)$ | — |