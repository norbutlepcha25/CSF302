# Lab 4: Modular and Matrix Exponentiation

Notes: [4.6 Modular Exponentiation](../unit4/topic6.md), [4.7 Matrix Exponentiation](../unit4/topic7.md)

## Part A: Efficient Modular Exponentiation

1. Implement a naive modular exponentiation algorithm to calculate `a^b mod m` using repeated multiplication.
2. Implement binary exponentiation using the square-and-multiply method to calculate `a^b mod m`.
3. Compare the outputs of naive and binary modular exponentiation for different bases, exponents and moduli.
4. Modify your binary exponentiation to use bitwise operations (`b & 1`, `b >>= 1`) to test for odd exponents and halve them.
5. Add input validation: zero exponent (return `1 mod m`), negative exponent (raise an error), negative base (reduce `a mod m` first), invalid modulus `m < 1` (raise an error).
6. Measure and compare the execution times of naive and binary modular exponentiation for b = 10, 100, ..., 10⁶.

## Part B: Efficient Matrix Modular Exponentiation

7. Implement a function to multiply two square matrices, reducing each element modulo `m`.
8. Implement a function to generate an identity matrix of a given dimension.
9. Implement naive matrix exponentiation to calculate `A^n mod m` using repeated multiplication.
10. Implement binary matrix exponentiation using repeated squaring.
11. Compare naive and binary matrix exponentiation for different matrices, exponents and moduli.
12. Calculate the nth Fibonacci number modulo `m` using matrix exponentiation.
13. Calculate F(10¹⁸) mod (10⁹ + 7) without generating the preceding Fibonacci numbers.
14. Count the number of walks of exactly `k` edges between two vertices of a directed graph using its adjacency matrix and a modulus.
15. Benchmark naive and binary matrix exponentiation for different dimensions (d = 2, 4, 8, 16, 32) and exponents (n = 2⁴, ..., 2¹²).
