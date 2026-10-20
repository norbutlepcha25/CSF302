# Lab 6: Dynamic Programming

Notes: [6.1 DP Principles](../unit6/topic1.md), [6.2 Rod Cutting](../unit6/topic2.md), [6.3 Matrix Chain](../unit6/topic3.md), [6.4 LCS](../unit6/topic4.md), [6.5 Optimal BST](../unit6/topic5.md)

## Q1: Rod Cutting

Price table for lengths 1 to 10: `1, 5, 8, 9, 10, 17, 17, 20, 24, 30`.

1. Naive recursive solution.
2. Top-down memoized solution.
3. Bottom-up tabulated solution.

- Print the maximum revenue and the list of piece lengths for n = 1 to 10.
- For n = 5, 10, 15, 20, 25 (extend the price table with `p[i] = 3*i` for i > 10), count the number of recursive calls of each version and measure execution time.
- Tabulate the counts and explain the difference.

## Q2: Matrix Chain Multiplication

1. Compute the minimum number of scalar multiplications using bottom-up DP.
2. Print the optimal parenthesisation, e.g. `((A1(A2A3))A4)`.
3. Verify your answer with a brute-force recursive search for chains of up to 8 matrices.

Test with dimensions `<30, 35, 15, 5, 10, 20, 25>` (expected minimum: 15,125) and `<5, 4, 6, 2, 7>`, plus 5 random chains. Report the cost of the left-to-right order alongside the optimal cost.

## Q3: Longest Common Subsequence

1. Fill the LCS table bottom-up and print it for `X = ABCBDAB`, `Y = BDCABA`.
2. Reconstruct one LCS from the table.
3. Write a space-optimised version that returns only the length using two rows.
4. Compare the running time of the DP with a brute-force solution (try every subsequence of X) for string lengths 5 to 18.
5. Use your LCS to print a line-by-line diff of two short text files (lines in the LCS are unchanged; others are added or removed).

## Q4 (Optional): Optimal Binary Search Tree

Given keys k1..k5 with p = `0.15, 0.10, 0.05, 0.10, 0.20` and q = `0.05, 0.10, 0.05, 0.05, 0.05, 0.10`, compute the expected search cost (expected: 2.75) and print the structure of the optimal tree.
