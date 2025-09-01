# Unit 1

**1.1 Number Theory**

### 1.1.1 Prime Numbers

- **Definition:** A prime number is a natural number greater than 1 that has no divisors other than 1 and itself.

- **Optimized Trial Division:**
  - Instead of dividing by all numbers up to `n`, divide up to `√n`.
  - Skip even numbers after checking 2.
- **Modified Sieve (Sieve of Eratosthenes):**
  - Efficient algorithm to generate all primes ≤ `n`.
  - Mark multiples of each prime starting from 2.

**Example:**\
Primes up to 30 → 2, 3, 5, 7, 11, 13, 17, 19, 23, 29

---

### 1.1.2 Greatest Common Divisor (GCD) & Least Common Multiple (LCM)

- **GCD (Euclidean Algorithm):**
  - `gcd(a, b) = gcd(b, a mod b)`
- **LCM relation:**
  - `lcm(a, b) = |a × b| / gcd(a, b)`

**Example:**\
gcd(48, 18) = 6\
lcm(48, 18) = (48×18)/6 = 144

---

### 1.1.3 Modular Arithmetic

- **Definition:** Arithmetic under a fixed modulus.
  - `(a + b) mod m = (a mod m + b mod m) mod m`
  - `(a × b) mod m = (a mod m × b mod m) mod m`
- **Extended Euclidean Algorithm:**\
  Finds integers `x, y` such that:\
  `ax + by = gcd(a, b)`\
  → Used for **modular inverse**.

**Application:** Cryptography (RSA, Diffie-Hellman)

---

### 1.1.4 Number Theory in Programming Competitions

- Fast modular exponentiation (Binary exponentiation).
- Modular inverses for division under modulus.
- Precomputation of factorials with mod for combinatorics.

---

## 1.2 Combinatorics

### 1.2.1 Fibonacci Numbers, Binomial Coefficients

- **Fibonacci Sequence:**
  - `F(n) = F(n-1) + F(n-2)`\
  - Closed form: **Binet's Formula**\
    `F(n) = (φ^n - (1-φ)^n) / √5`, where φ = (1+√5)/2.
- **Binomial Coefficient:**
  - `C(n, k) = n! / (k!(n-k)!)`
  - Appears in **Pascal's Triangle**.

**Applications:** Counting problems, probability, DP.

---

### 1.2.2 Catalan Numbers

- **Formula:**\
  `C_n = (1 / (n+1)) (2n choose n)`\
- **Applications:**
  - Counting valid parenthesis expressions\
  - Number of binary search trees with `n` nodes\
  - Ways to triangulate polygons

Example: `C_3 = 5`

---

## 1.3 Cycle-Finding Problem (Floyd's Algorithm)

- **Problem:** Detect a cycle in a sequence or linked list.\
- **Floyd's Tortoise and Hare Algorithm:**
  - Move one pointer 1 step, another pointer 2 steps.\
  - If they meet → cycle exists.\
  - Used in detecting infinite loops in functional graphs.

**Time complexity:** O(n)\
**Space complexity:** O(1)

---

## 1.4 Basics of Game Theory

- **Zero-sum games:** One player's gain = other's loss.
- **Nim Game:** Classic impartial game; winning strategy depends on
  **XOR-sum** of piles.
- **Grundy Numbers (Sprague-Grundy theorem):**
  - Reduces impartial games to Nim.
  - `Grundy(state) = mex({Grundy(next_states)})`

**Applications:** Competitive programming, AI decision making,
algorithms for optimal play.

---
