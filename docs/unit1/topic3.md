# Mathematical Foundations and Formula Reference

## Design and Analysis of Algorithms / Competitive Programming

**BE Software Engineering — Year III**
_College of Science and Technology, Royal University of Bhutan_

!!! info "Purpose"
This is a compact, revision-ready reference of the mathematics used repeatedly across the module — complexity analysis, number theory, combinatorics, probability, bitwise tricks, and basic geometry. It doesn't re-derive material covered in the Unit 1 notes in depth; it collects the formulas in one place for quick lookup before assessments and contests.

---

## 1. Asymptotic Notation

| Notation       | Meaning                                               | Informal reading        |
| -------------- | ----------------------------------------------------- | ----------------------- |
| f(n) = O(g(n)) | f grows **no faster** than g, up to a constant factor | "f is at most order g"  |
| f(n) = Ω(g(n)) | f grows **no slower** than g, up to a constant factor | "f is at least order g" |
| f(n) = Θ(g(n)) | f grows **at the same rate** as g                     | "f is exactly order g"  |

**Combining rules**

- **Sum rule:** O(f(n)) + O(g(n)) = O(max(f(n), g(n))) — the dominant term wins; drop lower-order terms and constants.
- **Product rule:** O(f(n)) · O(g(n)) = O(f(n)·g(n)).
- **Nested loops:** an outer loop of O(f(n)) iterations wrapping an inner loop of O(g(n)) gives O(f(n)·g(n)).

**Common growth rates, smallest to largest**

| Complexity | Name         | Typical example                    |
| ---------- | ------------ | ---------------------------------- |
| O(1)       | Constant     | Array index access                 |
| O(log n)   | Logarithmic  | Binary search, Euclidean algorithm |
| O(√n)      | Root         | Trial division primality test      |
| O(n)       | Linear       | Single pass / linear scan          |
| O(n log n) | Linearithmic | Sorting, divide-and-conquer        |
| O(n²)      | Quadratic    | Naive nested-loop comparison       |
| O(n³)      | Cubic        | Naive matrix multiplication        |
| O(2ⁿ)      | Exponential  | Subset enumeration                 |
| O(n!)      | Factorial    | Brute-force permutation search     |

!!! tip "Master Theorem (for divide-and-conquer recurrences)"
For T(n) = a·T(n/b) + f(n), compare f(n) against n^(log_b a):

    - If f(n) = O(n^(log_b a − ε)) → T(n) = Θ(n^(log_b a))
    - If f(n) = Θ(n^(log_b a)) → T(n) = Θ(n^(log_b a) · log n)
    - If f(n) = Ω(n^(log_b a + ε)) (and a regularity condition holds) → T(n) = Θ(f(n))

    Example: merge sort has T(n) = 2T(n/2) + O(n) → a = 2, b = 2, log_b a = 1, f(n) = Θ(n) → case 2 → T(n) = Θ(n log n).

---

## 2. Exponents and Logarithms

**Exponent laws**

$$
\begin{align*}
a^m · a^n = a^{(m+n)} \\
a^m / a^n = a^(m−n) \\
(a^m)^n  = a^(mn) \\
a^0 = 1        a^(−n) = 1 / a^n
\end{align*}
$$

**Logarithm laws** (all identities assume valid bases/arguments)

```
log_b(xy)   = log_b x + log_b y
log_b(x/y)  = log_b x − log_b y
log_b(x^k)  = k · log_b x
log_b b     = 1              log_b 1 = 0
```

**Change of base:**

```
log_b x = log_c x / log_c b        (e.g. log_2 x = ln x / ln 2)
```

!!! note "Why logarithms matter here"
log₂ n counts "how many times can n be halved before reaching 1" — this is exactly the step count of binary search, the recursion depth of balanced divide-and-conquer, and the number of bits needed to represent n. The base rarely matters for Big-O purposes since log_a n and log_b n differ only by a constant factor.

---

## 3. Summations and Series

| Series                             | Closed form             |
| ---------------------------------- | ----------------------- |
| Σ (i=1 to n) 1                     | n                       |
| Σ (i=1 to n) i                     | n(n+1) / 2              |
| Σ (i=1 to n) i²                    | n(n+1)(2n+1) / 6        |
| Σ (i=1 to n) i³                    | [n(n+1)/2]²             |
| Σ (i=0 to n−1) rⁱ (r ≠ 1)          | (rⁿ − 1) / (r − 1)      |
| Σ (i=0 to ∞) rⁱ (\|r\| < 1)        | 1 / (1 − r)             |
| Σ (i=1 to n) 1/i (harmonic series) | ≈ ln n + γ (γ ≈ 0.5772) |

!!! tip "Where the harmonic series shows up"
The O(N log log N) bound for the Sieve of Eratosthenes, and the O(N log N) bound for many "for each divisor, for each multiple" loops, both come from a sum of the form Σ (N/p) over primes p, which behaves like the harmonic series — this is the standard justification for those complexities in Unit 1.

---

## 4. Combinatorics Essentials

```
Permutations:   P(n, r) = n! / (n − r)!
Combinations:   C(n, r) = n! / (r! (n − r)!)
Pascal's rule:  C(n, r) = C(n−1, r−1) + C(n−1, r)
Binomial thm:   (x + y)ⁿ = Σ (k=0 to n) C(n, k) xᵏ yⁿ⁻ᵏ
```

**Stars and bars** — the number of ways to distribute n identical items into k distinct bins (bins may be empty):

```
C(n + k − 1, k − 1)
```

**Inclusion–Exclusion Principle**

```
|A ∪ B| = |A| + |B| − |A ∩ B|
|A ∪ B ∪ C| = |A|+|B|+|C| − |A∩B|−|A∩C|−|B∩C| + |A∩B∩C|
```

Generalises to n sets by alternating +/− over all intersections of increasing size — common in "count numbers NOT divisible by any of p₁…pₖ" problems.

!!! note "Pigeonhole Principle"
If n items are placed into m containers and n > m, at least one container holds more than one item. Deceptively simple, but the standard tool for existence proofs (e.g. guaranteeing a repeated remainder, or a repeated state in a bounded search space — this is exactly the argument underlying cycle-finding in Unit 1.3).

See also: **Fibonacci numbers**, **Catalan numbers**, and **precomputed nCr mod p** — covered in depth in the Unit 1 notes (§1.2).

---

## 5. Number Theory Quick Reference

_(condensed cross-reference — see Unit 1 §1.1 for derivations and code)_

```
gcd(a, b) · lcm(a, b) = a · b
gcd(a, b) = gcd(b, a mod b)                          (Euclidean algorithm)
a·x + b·y = gcd(a, b)                                (Bézout's identity / Extended Euclid)
```

**Modular arithmetic**

```
(a ± b) mod m = ((a mod m) ± (b mod m) + m) mod m
(a × b) mod m = ((a mod m) × (b mod m)) mod m
a⁻¹ (mod m) exists  ⇔  gcd(a, m) = 1
```

**Fermat's Little Theorem** (m prime, a not divisible by m):

```
a^(m−1) ≡ 1 (mod m)      ⇒      a⁻¹ ≡ a^(m−2) (mod m)
```

**Euler's Totient Function** — φ(n) counts integers in [1, n] coprime to n:

```
φ(n) = n · Π (1 − 1/p)     over each distinct prime p dividing n
```

**Euler's theorem** (generalises Fermat, works for any m with gcd(a, m) = 1):

```
a^φ(m) ≡ 1 (mod m)
```

---

## 6. Probability and Expectation

```
P(A ∪ B) = P(A) + P(B) − P(A ∩ B)
P(A | B) = P(A ∩ B) / P(B)                      (conditional probability)
P(A ∩ B) = P(A) · P(B)                          (only if A, B independent)
```

**Expectation:**

```
E[X] = Σ x · P(X = x)
```

!!! tip "Linearity of expectation"
E[X + Y] = E[X] + E[Y] **always holds**, even when X and Y are dependent. This is one of the most powerful tricks in competitive programming: it lets you compute the expected value of a complicated combined quantity by summing the expectations of simple pieces, without needing independence.

**Variance:**

```
Var(X) = E[X²] − (E[X])²
```

---

## 7. Bitwise Operations Reference

| Operation   | Symbol   | Effect                                   |
| ----------- | -------- | ---------------------------------------- |
| AND         | `a & b`  | 1 only where both bits are 1             |
| OR          | `a \| b` | 1 where at least one bit is 1            |
| XOR         | `a ^ b`  | 1 where exactly one bit is 1             |
| NOT         | `~a`     | flips every bit                          |
| Left shift  | `a << k` | multiply by 2ᵏ                           |
| Right shift | `a >> k` | divide by 2ᵏ (floor, for non-negative a) |

**Useful identities**

```
a ^ a = 0            a ^ 0 = a            a ^ b = b ^ a   (XOR is its own inverse — used to "cancel" values)
```

**Common tricks**

```cpp
bool isPowerOfTwo(int n)   { return n > 0 && (n & (n - 1)) == 0; }
int  lowestSetBit(int n)   { return n & (-n); }
int  popcount(unsigned n)  { return __builtin_popcount(n); }
int  toggleBit(int n,int i){ return n ^ (1 << i); }
```

!!! note "Where this connects"
XOR is exactly the Nim-sum operation from Unit 1.4 (Sprague–Grundy theory), and iterating over `1 << n` subset masks is the standard way to enumerate all 2ⁿ subsets of a set in bitmask dynamic programming.

---

## 8. Basic Geometry (Vectors)

For 2D points/vectors A = (a₁, a₂), B = (b₁, b₂):

```
Dot product:    A · B = a₁b₁ + a₂b₂                        (0 ⇔ perpendicular)
Cross product:  A × B = a₁b₂ − a₂b₁                        (signed area of the parallelogram spanned by A, B)
```

**Orientation test** — for three points O, A, B, the sign of the cross product of (A − O) and (B − O) tells you the turn direction:

```cpp
long long cross(Point O, Point A, Point B) {
    return (long long)(A.x - O.x) * (B.y - O.y)
         - (long long)(A.y - O.y) * (B.x - O.x);
}
// cross > 0  =>  counter-clockwise turn (left turn)
// cross < 0  =>  clockwise turn (right turn)
// cross == 0 =>  collinear
```

!!! tip "Where this connects"
This orientation test is the core primitive behind Graham Scan (convex hull construction): points are sorted by polar angle, and the sign of `cross()` decides whether to keep or discard the last point on the hull as each new point is considered.

---

## 9. Proof Techniques Used in Correctness Arguments

- **Mathematical induction** — prove a base case, then show that if the statement holds for n it holds for n + 1. Standard tool for proving a recurrence's closed form or a loop invariant holds for all iterations.
- **Proof by contradiction** — assume the claim is false and derive an impossibility. Used, e.g., to show √2 is irrational, or that a smallest counter-example to a greedy-choice claim cannot exist.
- **Loop invariants** — a condition that is true before the loop starts, remains true after every iteration, and (combined with the loop's termination condition) implies correctness when the loop ends. This is the standard way to formally justify why an algorithm like the Euclidean algorithm or a sieve produces the correct result.

---

## 10. Where Each Tool Is Used in the Module

| Math tool                                        | Appears in                                                                  |
| ------------------------------------------------ | --------------------------------------------------------------------------- |
| Big-O / Master Theorem                           | Complexity analysis of every algorithm; divide-and-conquer recurrences      |
| Logarithms                                       | Binary search, sieve complexity, fast exponentiation, matrix exponentiation |
| Summations / harmonic series                     | Sieve of Eratosthenes complexity, amortised analysis                        |
| Combinatorics (nCr, Pascal, inclusion-exclusion) | Binomial coefficients, Catalan numbers, counting problems                   |
| Modular arithmetic / Fermat / Euler              | Any "answer mod 10^9+7" problem, modular inverses                           |
| GCD / Extended Euclid                            | Linear Diophantine equations, modular inverses, CRT                         |
| Probability / linearity of expectation           | Randomised algorithms, expected-value problems                              |
| Bitwise XOR / masks                              | Nim and Sprague–Grundy theory, subset/bitmask DP                            |
| Vectors / cross product                          | Graham Scan and other computational-geometry algorithms                     |
| Induction / loop invariants                      | Correctness proofs for any iterative or recursive algorithm                 |

---

## References

- Cormen, Leiserson, Rivest, Stein — _Introduction to Algorithms_ (CLRS), Chapter 3 (Growth of Functions) and Appendix A (Summations).
- Graham, Knuth, Patashnik — _Concrete Mathematics_, for summation and combinatorics identities.
- Antti Laaksonen — _Competitive Programmer's Handbook_, Part I (Basic Techniques) and the Mathematics chapters.
