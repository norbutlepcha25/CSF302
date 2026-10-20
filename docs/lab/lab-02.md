# Lab 2: Step/Frequency Counting

Notes: [2.1 Asymptotic Analysis](../unit2/topic1.md), [2.2 Word-RAM Model](../unit2/topic2.md), [3.6 Merge Sort](../unit3/topic6.md)

## Q1: Prime Number Testing

Test whether a number `n` is prime using two algorithms and compare their performance.

1. Naive method: check divisibility from 2 to n−1.
2. Optimised method: check divisibility up to √n.
3. Optional: list all primes up to `n` using the Sieve of Eratosthenes.

- Input at least 10 numbers from the user (include large primes such as 1,000,003 and a square of a prime such as 100,140,049).
- For each number, decide if it is prime using both algorithms.
- Record the step/frequency count (number of divisions) for each algorithm.
- Plot step count against `n` and identify the faster algorithm.

## Q2: Merge Sort Analysis (Menu-Driven Program)

Write a menu-driven program to sort an array of `n` integers using Merge Sort and record step/frequency counts (comparisons and moves).

**Menu:**

1. Generate `n` random numbers into an array
2. Display the array
3. Sort in ascending order using Merge Sort
4. Sort in descending order using any sorting algorithm
5. Step count table for random data (n = 256, 512, ..., 8192)
6. Step count table for already-sorted data
7. Step count table for descending-sorted data

Plot comparisons against `n` for options 5, 6 and 7 on one graph.

## Q3: Square Matrix Multiplication

Multiply two square matrices (`n × n`, `n` a power of 2: 2, 4, 8, ..., 64).

- Input the matrices manually or generate them randomly.
- Display the resultant matrix.
- Count the number of scalar multiplications and additions, and tabulate them for each `n`.
