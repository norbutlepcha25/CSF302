# Lab 3: Divide and Conquer

Notes: [4.2 Strassen](../unit4/topic2.md), [4.3 Integer Multiplication](../unit4/topic3.md), [4.5 Binary and Ternary Search](../unit4/topic5.md)

## Q1: Matrix Multiplication — Strassen vs Traditional

1. Traditional method (triple nested loop).
2. Strassen's algorithm (7 recursive multiplications per split).

- Matrix sizes: powers of 2 from 2×2 up to 128×128.
- Input the matrices manually or generate them randomly.
- Display the result from both methods and verify they match.
- Count scalar multiplications and measure execution time for each size. Try a base-case cutoff (switch to the traditional method below size 8, 16, 32...) and report the fastest cutoff.

## Q2: Karatsuba Large Integer Multiplication

1. Traditional grade-school multiplication.
2. Karatsuba's algorithm (3 recursive multiplications per split).

- Represent integers as strings or digit arrays so sizes can go beyond native limits: 8, 16, 32, ..., 1024 digits.
- Pad both operands to the same length in **every** recursive call (x₀ + x₁ may carry an extra digit). Use a base case of at least 4 digits.
- Input the numbers manually or generate them randomly.
- Verify Karatsuba's result matches the traditional method for every test case.
- Count digit multiplications and measure execution time for each size.

## Q3: Binary Search vs Ternary Search (Menu-Driven Program)

Search for a key in a sorted array of `n` integers using Binary Search and Ternary Search.

**Menu:**

1. Generate `n` sorted random numbers into an array
2. Display the array
3. Search for a key using Binary Search
4. Search for a key using Ternary Search
5. Comparison count for the best case
6. Comparison count for the worst case (key absent)
7. Comparison count table for n = 10, 100, ..., 100,000

Explain the result using the recurrences T(n) = T(n/2) + 2 and T(n) = T(n/3) + 4 (comparisons per round).
