# Number Theory, Combinatorics, and Algorithmic Foundations

## 1.1 Number Theory

Number theory underlies a large fraction of competitive-programming and algorithmic problems — from hashing and cryptography to combinatorial counting under a modulus. This section builds the toolbox: primality testing, prime generation, divisibility (GCD/LCM), and modular arithmetic, culminating in the Extended Euclidean Algorithm.

### 1.1.1 Prime Numbers, Optimized Trial Division, Modified Sieve

A prime number is a natural number greater than 1 that has exactly two positive divisors: 1 and itself. Primality testing and prime generation are foundational sub-routines: factorisation, Euler's totient function, and many combinatorial formulas depend on them.

#### A. Naive and Optimized Trial Division

The direct definition suggests testing every integer from 2 to n − 1 as a possible divisor — an O(n) test. This can be improved sharply using two observations:

- If n has a divisor d > √n, it must also have a corresponding divisor n / d < √n. So it suffices to check divisors only up to √n.
- Every prime greater than 3 has the form 6k ± 1. Hence, after ruling out divisibility by 2 and 3, we only need to test candidates of the form 6k − 1 and 6k + 1.

**Optimized trial division — O(√n) per query**

```cpp
bool isPrime(long long n) {
    if (n < 2) return false;
    if (n == 2 || n == 3) return true;
    if (n % 2 == 0 || n % 3 == 0) return false;
    for (long long i = 5; i * i <= n; i += 6) {
        if (n % i == 0 || n % (i + 2) == 0) return false;
    }
    return true;
}
```

This is the right tool when you need to test a handful of large numbers (e.g. n up to 10^18) and a full sieve would not fit in memory.

#### B. Sieve of Eratosthenes

When many numbers up to some bound N must be classified as prime or composite, precomputing is far cheaper than testing each one individually. The Sieve of Eratosthenes marks composites by striking out multiples of each prime, starting from p² (smaller multiples of p were already struck out by smaller primes).

**Sieve of Eratosthenes — O(N log log N) time, O(N) space**

```cpp
vector<bool> sieve(int n) {
    vector<bool> isComposite(n + 1, false);
    for (int i = 2; (long long)i * i <= n; i++) {
        if (!isComposite[i]) {
            for (int j = i * i; j <= n; j += i)
                isComposite[j] = true;
        }
    }
    return isComposite;   // isComposite[i] == false  =>  i is prime  (i >= 2)
}
```

#### C. Modified Sieves

Two common modifications extend the basic sieve to handle larger ranges or richer queries:

**Linear (Euler) Sieve** — guarantees every composite is marked exactly once, giving true O(N) time. It also produces each number's smallest prime factor (SPF), enabling O(log n) factorisation afterwards.

```cpp
vector<int> spf;              // spf[i] = smallest prime factor of i
vector<int> primes;

void linearSieve(int n) {
    spf.assign(n + 1, 0);
    for (int i = 2; i <= n; i++) {
        if (spf[i] == 0) {            // i is prime
            spf[i] = i;
            primes.push_back(i);
        }
        for (int p : primes) {
            if (p > spf[i] || (long long)i * p > n) break;
            spf[i * p] = p;
        }
    }
}
```

**Segmented Sieve** — used when the range [L, R] is large (e.g. R up to 10^12) but R − L is small (e.g. ≤ 10^6). Precompute primes up to √R with a normal sieve, then use only those primes to strike out composites directly within [L, R].

```cpp
vector<bool> segmentedSieve(long long L, long long R) {
    int limit = (int)sqrt((double)R) + 1;
    vector<bool> baseComposite = sieve(limit);      // primes up to sqrt(R)
    vector<bool> isComposite(R - L + 1, false);

    for (int i = 2; i <= limit; i++) {
        if (!baseComposite[i]) {
            long long start = max((long long)i * i, ((L + i - 1) / i) * i);
            for (long long j = start; j <= R; j += i)
                isComposite[j - L] = true;
        }
    }
    return isComposite;   // isComposite[x - L] == false  =>  x is prime
}
```

**Complexity summary**

| Method                | Preprocessing    | Per-query cost              | Best used when                        |
| --------------------- | ---------------- | --------------------------- | ------------------------------------- |
| Trial division        | —                | O(√n)                       | Testing a few large, isolated numbers |
| Sieve of Eratosthenes | O(N log log N)   | O(1)                        | Many queries, N ≤ ~10^7               |
| Linear / Euler sieve  | O(N)             | O(1), O(log n) to factorise | Need SPF / fast factorisation         |
| Segmented sieve       | O(√R log log √R) | O((R−L) log log R)          | Large R, small window (R − L)         |

---

### 1.1.2 Greatest Common Divisor & Least Common Divisor

The greatest common divisor gcd(a, b) is the largest integer dividing both a and b. The Euclidean Algorithm computes it using the identity gcd(a, b) = gcd(b, a mod b), terminating when the second argument reaches 0.

!!! tip "Why it works"
If d divides both a and b, then d also divides a mod b = a − ⌊a/b⌋·b. Conversely any common divisor of b and a mod b also divides a. Hence gcd(a, b) = gcd(b, a mod b) exactly — no information is lost at each step.

**Euclidean Algorithm — O(log(min(a, b)))**

```cpp
long long gcd(long long a, long long b) {
    while (b) {
        a %= b;
        swap(a, b);
    }
    return a;
}

long long lcm(long long a, long long b) {
    return a / gcd(a, b) * b;    // divide first to avoid overflow
}
```

The O(log(min(a,b))) bound follows from the fact that consecutive Fibonacci numbers form the worst case: each step of the algorithm reduces the pair size by at least the golden-ratio factor, so the number of steps grows logarithmically with the input — Lamé's theorem formalises this and gives the connection to Fibonacci numbers seen again in section 1.2.1.

The LCM formula lcm(a, b) = a·b / gcd(a, b) follows directly from unique prime factorisation: for each prime p, gcd takes the minimum exponent across a and b, while lcm takes the maximum, and min(x,y) + max(x,y) = x + y.

**Binary GCD (Stein's Algorithm)** — an alternative that avoids division, using only subtraction and bit shifts; useful on hardware where division is expensive relative to shifts. It has the same asymptotic complexity but a smaller constant factor in some settings.

---

### 1.1.3 Modular Arithmetic, Extended Euclidean Algorithm

Competitive programming problems routinely ask for an answer "modulo 10^9 + 7" because the true answer would otherwise overflow standard integer types. Modular arithmetic lets us carry out the entire computation using only remainders.

#### A. Basic Rules

- (a + b) mod m = ((a mod m) + (b mod m)) mod m
- (a − b) mod m = ((a mod m) − (b mod m) + m) mod m — add m to keep the result non-negative
- (a × b) mod m = ((a mod m) × (b mod m)) mod m
- Division is **not** distributed the same way — (a / b) mod m requires the modular inverse of b (see below).

**Fast (binary) exponentiation — O(log e)**

```cpp
long long power(long long base, long long exp, long long mod) {
    long long result = 1;
    base %= mod;
    while (exp > 0) {
        if (exp & 1) result = (result * base) % mod;
        base = (base * base) % mod;
        exp >>= 1;
    }
    return result;
}
```

#### B. The Extended Euclidean Algorithm

The Extended Euclidean Algorithm augments the standard Euclidean algorithm to also find integers x, y satisfying Bézout's identity:

```
a·x + b·y = gcd(a, b)
```

It is derived by unwinding the recursion: if gcd(b, a mod b) = b·x₁ + (a mod b)·y₁, substitute a mod b = a − ⌊a/b⌋·b to express the same gcd as a combination of a and b directly.

**Extended Euclidean Algorithm**

```cpp
long long extgcd(long long a, long long b, long long &x, long long &y) {
    if (b == 0) {
        x = 1; y = 0;
        return a;                    // gcd(a, 0) = a
    }
    long long x1, y1;
    long long g = extgcd(b, a % b, x1, y1);
    x = y1;
    y = x1 - (a / b) * y1;
    return g;
}
```

**Modular inverse via Extended Euclid** — a modular inverse of a, written a⁻¹ (mod m), is a value x such that a·x ≡ 1 (mod m). It exists exactly when gcd(a, m) = 1. Setting b = m above, x from a·x + m·y = 1 is that inverse.

```cpp
long long modInverse(long long a, long long m) {
    long long x, y;
    long long g = extgcd(a, m, x, y);
    if (g != 1) return -1;            // inverse does not exist
    return ((x % m) + m) % m;
}
```

**Modular inverse via Fermat's Little Theorem** — when m is prime, a^(m−1) ≡ 1 (mod m) for any a not divisible by m, so a⁻¹ ≡ a^(m−2) (mod m). This only needs fast exponentiation, but requires m to be prime (e.g. the common modulus 10^9 + 7).

```cpp
long long modInverseFermat(long long a, long long m /* m is prime */) {
    return power(a, m - 2, m);
}
```

!!! note "Chinese Remainder Theorem (CRT)"
When you need x mod (m₁·m₂) given x mod m₁ and x mod m₂ with gcd(m₁, m₂) = 1, CRT reconstructs a unique solution mod m₁·m₂. It is built directly from the Extended Euclidean Algorithm and appears whenever a modulus is composite or the answer is required modulo a product of primes.

---

### 1.1.4 Number Theory in Programming Competitions

A short field guide to how these tools tend to appear in problems:

- "Count something mod 10^9 + 7" → precompute factorials and inverse factorials once with fast exponentiation, then answer each nCr query in O(1).
- "Sum of divisors / number of divisors" → factorise using a precomputed smallest-prime-factor table, then apply the standard divisor-count and divisor-sum formulas from the prime factorisation.
- "Two numbers are compatible if gcd(a, b) = 1" (coprimality) → often solved by counting through Euler's totient function φ(n), itself computed via a sieve variant.
- "Solve for integer solutions of a·x + b·y = c" → linear Diophantine equation; solvable iff gcd(a, b) divides c, using the Extended Euclidean Algorithm to find one solution and then parametrising all others.
- "Answer must be found modulo a composite number" → factor the modulus and combine results with the Chinese Remainder Theorem.

!!! warning "Common pitfalls"
Forgetting that the `%` operator in C++/Java can return a negative result for negative operands (always normalise with `((x % m) + m) % m`); multiplying two ~10^9 values without first casting to a 64-bit type, causing silent overflow; and assuming a modular inverse exists without checking gcd(a, m) = 1.

---

## 1.2 Combinatorics

Combinatorics supplies the counting machinery behind probability, DP state counting, and closed-form answers. This section covers two families that recur constantly: Fibonacci-type linear recurrences and the counting numbers built from binomial coefficients.

### 1.2.1 Fibonacci Numbers, Binomial Coefficients

#### A. Fibonacci Numbers

Defined by F(0) = 0, F(1) = 1, F(n) = F(n−1) + F(n−2). Direct recursion is exponential; a bottom-up DP already gives O(n). For very large n (e.g. n up to 10^18, answer mod p), matrix exponentiation reduces this to O(log n) using the identity:

```
[F(n+1) F(n); F(n) F(n-1)] = [1 1; 1 0]ⁿ
```

**Fibonacci via matrix exponentiation — O(log n)**

```cpp
struct Mat { long long a, b, c, d; };

Mat mul(const Mat &m1, const Mat &m2, long long mod) {
    return {
        (m1.a * m2.a + m1.b * m2.c) % mod,
        (m1.a * m2.b + m1.b * m2.d) % mod,
        (m1.c * m2.a + m1.d * m2.c) % mod,
        (m1.c * m2.b + m1.d * m2.d) % mod
    };
}

long long fibonacci(long long n, long long mod) {
    if (n == 0) return 0;
    Mat result = {1, 0, 0, 1};        // identity matrix
    Mat base    = {1, 1, 1, 0};
    n--;
    while (n > 0) {
        if (n & 1) result = mul(result, base, mod);
        base = mul(base, base, mod);
        n >>= 1;
    }
    return result.a;
}
```

#### B. Binomial Coefficients

nCr, read "n choose r", counts the number of ways to choose an unordered subset of r items from n. It satisfies Pascal's identity nCr = (n−1)C(r−1) + (n−1)Cr, giving Pascal's Triangle, and the closed form:

```
nCr = n! / (r! · (n − r)!)
```

For competitive programming, the standard pattern is to precompute factorials and their modular inverses once (using fast exponentiation, section 1.1.3), then answer each query in O(1):

**Precomputed nCr mod p — O(N) build, O(1) per query**

```cpp
const int MAXN = 200005;
const long long MOD = 1e9 + 7;
long long fact[MAXN], invFact[MAXN];

void precompute() {
    fact[0] = 1;
    for (int i = 1; i < MAXN; i++) fact[i] = fact[i - 1] * i % MOD;
    invFact[MAXN - 1] = power(fact[MAXN - 1], MOD - 2, MOD);
    for (int i = MAXN - 2; i >= 0; i--)
        invFact[i] = invFact[i + 1] * (i + 1) % MOD;
}

long long nCr(int n, int r) {
    if (r < 0 || r > n) return 0;
    return fact[n] * invFact[r] % MOD * invFact[n - r] % MOD;
}
```

!!! note "Lucas' Theorem"
When n and r can be astronomically large but the modulus p is a small prime, nCr mod p can be computed digit-by-digit in base p, combining small nCr values via Lucas' Theorem — useful when N is too large for the precomputed-factorial table above.

---

### 1.2.2 Catalan Numbers

The n-th Catalan number Cₙ counts an unusually wide range of combinatorial structures that all turn out to be equinumerous:

- The number of ways to correctly match n pairs of balanced parentheses.
- The number of distinct binary search trees (equivalently, distinct binary tree shapes) with n nodes.
- The number of ways to triangulate a convex polygon with n + 2 sides.
- The number of monotonic lattice paths from (0,0) to (n,n) that never cross above the diagonal (Dyck paths).

Catalan numbers satisfy the recurrence

```
C₀ = 1,      Cₙ₊₁ = Σ (Cᵢ · Cₙ₋ᵢ)  for i = 0..n
```

and the closed form built directly from binomial coefficients:

```
Cₙ = (2n)Cn / (n + 1)
```

**Catalan number mod p, using precomputed nCr**

```cpp
long long catalan(int n) {
    long long c = nCr(2 * n, n);
    long long invNPlus1 = power(n + 1, MOD - 2, MOD);
    return c * invNPlus1 % MOD;
}
```

---

## 1.3 Cycle-Finding Problem, Floyd's Algorithm

Given a sequence x₀, x₁ = f(x₀), x₂ = f(x₁), … generated by repeatedly applying a function f over a finite domain, the sequence must eventually repeat a value and enter a cycle — there are only finitely many possible values. The cycle-finding problem asks for two numbers describing this structure:

- **μ (mu)** — the length of the "tail" before the cycle begins (the first index at which a value repeats an earlier one).
- **λ (lambda)** — the length of the cycle itself.

This model applies directly to detecting a cycle in a linked list (f = "next pointer"), detecting the period of a pseudorandom number generator, and as the core sub-routine of Pollard's rho integer-factorisation algorithm.

### A. Naive Approach

Store every visited value in a hash set and stop as soon as a repeat is seen. This correctly finds μ and λ in O(μ + λ) time, but uses O(μ + λ) auxiliary space — potentially prohibitive when the domain is huge or memory is tightly bounded (as in embedded or interview settings).

### B. Floyd's Tortoise and Hare Algorithm

Floyd's algorithm finds the same μ and λ using only O(1) extra memory, by racing two pointers at different speeds:

- The tortoise moves one step at a time: `tortoise ← f(tortoise)`.
- The hare moves two steps at a time: `hare ← f(f(hare))`.
- If there is a cycle, the hare — being faster — eventually "laps" the tortoise and they meet somewhere inside the cycle.

!!! tip "Why they must meet"
Once both pointers are inside the cycle, the distance between hare and tortoise decreases by exactly 1 (mod λ) every step, since the hare gains one extra step on the tortoise each iteration. A decreasing-mod-λ quantity must eventually hit 0, so the pointers are guaranteed to coincide within at most λ further steps.

Once a meeting point is found, two further phases recover μ and λ:

1. Reset one pointer to x₀ and keep the other at the meeting point; advance both one step at a time — they meet again exactly at the start of the cycle, after μ steps. This works because of the modular-distance argument above.
2. From that meeting point, advance one pointer around the cycle, counting steps until it returns to the same position — this count is λ.

**Floyd's Cycle Detection — O(μ + λ) time, O(1) space**

```cpp
pair<long long, long long> floydCycle(function<long long(long long)> f, long long x0) {
    // Phase 1: find a meeting point inside the cycle
    long long tortoise = f(x0);
    long long hare = f(f(x0));
    while (tortoise != hare) {
        tortoise = f(tortoise);
        hare = f(f(hare));
    }

    // Phase 2: find mu, the start of the cycle
    long long mu = 0;
    tortoise = x0;
    while (tortoise != hare) {
        tortoise = f(tortoise);
        hare = f(hare);
        mu++;
    }

    // Phase 3: find lambda, the cycle length
    long long lambda = 1;
    hare = f(tortoise);
    while (tortoise != hare) {
        hare = f(hare);
        lambda++;
    }

    return {mu, lambda};
}
```

!!! note "Brent's Algorithm"
A refinement of the same idea that avoids calling f twice per iteration in the search phase by advancing the hare in doubling-length blocks. It typically performs fewer function evaluations in practice while remaining O(μ + λ) time and O(1) space — worth mentioning as the practical alternative used inside many library implementations.

---

## 1.4 Basics of Game Theory

Combinatorial game theory studies two-player games with perfect information (both players see the full state) and no element of chance, where players alternate moves and the game ends in a finite number of moves. Under the normal play convention, the player unable to move loses.

### A. Winning and Losing Positions

- A **P-position** ("Previous player wins") is a losing position for the player about to move — every move from it leads to an N-position.
- An **N-position** ("Next player wins") is a winning position for the player about to move — at least one move from it leads to a P-position.
- A terminal position with no available moves is, by definition, a P-position (the player to move has already lost).

!!! note "Core recursive rule"
A position is a P-position if and only if every move from it leads to an N-position. A position is an N-position if and only if at least one move from it leads to a P-position. This single recursive rule, evaluated from terminal positions backward, classifies every position in any finite impartial game.

### B. The Game of Nim

Nim is the canonical impartial game: several piles of stones; on each turn a player removes any positive number of stones from exactly one pile; the player who removes the last stone wins (normal play). Remarkably, the winner is determined purely by a bitwise computation:

```
Position is a P-position  ⇔  pile₁ ⊕ pile₂ ⊕ … ⊕ pileₖ = 0
```

where ⊕ denotes bitwise XOR. If the XOR (called the Nim-sum) is non-zero, the position is an N-position, and a winning move always exists that reduces some pile so as to zero out the XOR.

**Nim: determine the winner and a winning move**

```cpp
bool firstPlayerWins(vector<int> &piles) {
    int nimSum = 0;
    for (int pile : piles) nimSum ^= pile;
    return nimSum != 0;
}

// If nimSum != 0, a winning move exists: find a pile where
// (pile ^ nimSum) < pile, and reduce that pile to (pile ^ nimSum).
```

### C. The Sprague–Grundy Theorem

The Sprague–Grundy theorem generalises Nim's XOR trick to any impartial game (or sum of several independent impartial games played simultaneously). Every position of an impartial game is assigned a Grundy number (also called a nimber) g(position), defined recursively using the minimum excludant (mex) — the smallest non-negative integer not present in a given set:

```
g(position) = mex { g(next) : next is reachable in one move }
```

- g(position) = 0 exactly when the position is a P-position — this matches the earlier recursive rule.
- For a sum of independent games played together (a move affects exactly one component game per turn), the Grundy number of the whole is the XOR of the Grundy numbers of the parts — exactly generalising Nim, where each pile's Grundy number equals its own size.

**Computing Grundy numbers by memoised search**

```cpp
unordered_map<int, int> memo;

int grundy(int state) {
    if (memo.count(state)) return memo[state];
    set<int> reachable;
    for (int next : movesFrom(state))          // problem-specific move generator
        reachable.insert(grundy(next));

    int mex = 0;
    while (reachable.count(mex)) mex++;        // smallest non-negative integer not seen
    return memo[state] = mex;
}

bool isWinningPosition(vector<int> &components) {
    int total = 0;
    for (int c : components) total ^= grundy(c);
    return total != 0;                          // non-zero => N-position, mover wins
}
```

### D. Worked Example

Consider Nim with piles (3, 4, 5). The Nim-sum is 3 ⊕ 4 ⊕ 5 = 2, which is non-zero, so the position is an N-position: the player to move wins. A winning move exists on the pile where (pile ⊕ 2) < pile — here pile = 3 gives 3 ⊕ 2 = 1 < 3, so reducing the first pile from 3 to 1 stones leaves (1, 4, 5) with Nim-sum 0, a P-position handed to the opponent.

---

## Unit Summary

| Topic                        | Core algorithm(s)                                                              | Typical complexity                        |
| ---------------------------- | ------------------------------------------------------------------------------ | ----------------------------------------- |
| Primality / prime generation | Optimized trial division; Sieve of Eratosthenes; Linear sieve; Segmented sieve | O(√n) query; O(N log log N) or O(N) build |
| GCD / LCM                    | Euclidean Algorithm                                                            | O(log(min(a,b)))                          |
| Modular arithmetic           | Fast exponentiation; Extended Euclidean Algorithm; Fermat's Little Theorem     | O(log e) / O(log m)                       |
| Fibonacci numbers            | Matrix exponentiation                                                          | O(log n)                                  |
| Binomial coefficients        | Precomputed factorials + modular inverse                                       | O(N) build, O(1) query                    |
| Catalan numbers              | Closed form via nCr                                                            | O(1) given precomputed nCr                |
| Cycle finding                | Floyd's Tortoise and Hare (or Brent's algorithm)                               | O(μ + λ) time, O(1) space                 |
| Combinatorial games          | P/N-position analysis; Sprague–Grundy theorem                                  | Problem-dependent state space             |

## Suggested Practice

The following problem types are good practice targets on judges such as Codeforces and SPOJ (search each judge by topic tag rather than by name, since exact problem sets vary by term):

- **Primality / sieve:** precompute primes up to 10^6–10^7 and answer many range or factorisation queries.
- **GCD/LCM and modular arithmetic:** problems requiring an answer modulo 10^9 + 7 that involve division (forcing use of a modular inverse).
- **Extended Euclidean Algorithm:** linear Diophantine equation problems, and modular inverse computation where the modulus is not prime.
- **Combinatorics:** counting problems solvable with precomputed nCr, and problems whose recurrence matches the Catalan pattern (balanced sequences, tree counting).
- **Cycle finding:** "find the period" or "detect a repeated state" problems, including simple pseudo-random sequence or functional-graph tasks.
- **Game theory:** small impartial games (Nim variants, subtraction games) where students derive the Grundy numbers by hand before coding the memoised search.

## References

- Cormen, Leiserson, Rivest, Stein — _Introduction to Algorithms_ (CLRS), chapters on number-theoretic algorithms.
- Antti Laaksonen — _Competitive Programmer's Handbook_, chapters on number theory, combinatorics, and game theory.
- Halim & Halim — _Competitive Programming_ (4th ed.), relevant chapters on mathematics for contests.
- Knuth — _The Art of Computer Programming, Vol. 2: Seminumerical Algorithms_ (for cycle detection and number theory background).
