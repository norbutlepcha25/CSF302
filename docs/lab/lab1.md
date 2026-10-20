# Lab 1: Empirical Growth Rate Measurement

Notes: [2.1 Asymptotic Analysis](../unit2/topic1.md), [4.5 Binary Search](../unit4/topic5.md), [3.6 Merge Sort](../unit3/topic6.md)

## Q1: Linear Search vs Binary Search

1. Implement Linear Search.
2. Implement Binary Search (iterative).
3. Generate random datasets of the sizes below.
4. Sort the dataset before applying Binary Search (do not include the sorting time).
5. Measure the average execution time of 100 searches for both algorithms.
6. Plot time against input size for both algorithms.

**Input sizes:** 1,000; 5,000; 10,000; 50,000; 100,000; 500,000; 1,000,000

## Q2: Bubble Sort vs Merge Sort

1. Implement Bubble Sort (stop early when a pass makes no swap).
2. Implement Merge Sort.
3. Generate random arrays of the sizes below.
4. Measure the average execution time of each algorithm.
5. Plot time against input size on a log-log scale and report the slope of each line.

**Input sizes:** 100; 500; 1,000; 2,000; 4,000; 8,000

## Q3: Generating Primes

Generate all primes up to **N** using:

1. Naive trial division (check divisors 2 to k−1).
2. Optimised trial division (check divisors d while d·d ≤ k).
3. Sieve of Eratosthenes.

Measure the execution time of each method and plot the results. If a method takes longer than 60 seconds for a size, stop it and record "did not finish".

**Input sizes (N):** 10,000; 50,000; 100,000; 500,000; 1,000,000

## Analysis (as comments)

- Which algorithm wins for each question, and from what input size?
- Do the measured slopes match the theoretical complexities?
