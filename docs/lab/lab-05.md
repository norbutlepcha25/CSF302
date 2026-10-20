# Lab 5: Sorting Algorithms

Notes: [5.3 Quicksort](../unit5/topic3.md), [5.4 Randomised Quicksort](../unit5/topic4.md), [5.5 Counting Sort](../unit5/topic5.md), [5.6 Radix Sort](../unit5/topic6.md), [5.7 Counting Inversions](../unit5/topic7.md)

## Q1: Quicksort Variants

1. Quicksort with Lomuto partition (last element as pivot).
2. Quicksort with Hoare partition.
3. Randomised quicksort (random pivot).
4. Three-way (Dutch national flag) quicksort.

- Count comparisons and measure execution time for each variant on four input types: random, already sorted, reverse sorted, and many duplicates (values from 0 to 9).
- Input sizes: 1,000; 2,000; 4,000; 8,000; 16,000.
- Recurse on the smaller part and loop on the larger one so sorted inputs do not exceed the recursion limit.
- Tabulate the results and explain which variant degrades to Θ(n²) on which input type, and why.

## Q2: Counting Sort and Radix Sort

1. Implement stable counting sort for integers in the range 0 to k.
2. Implement LSD radix sort using counting sort on each digit (base 10, then base 256).
3. Compare both with your merge sort from Lab 1.

- Fix n = 100,000 and vary k = 10, 10³, 10⁵, 10⁷ for counting sort.
- Fix k = 10⁹ and vary n = 10,000 to 1,000,000 for radix sort and merge sort.
- Plot the results and explain when the linear-time sorts win and when they lose.
- Show that your counting sort is stable by sorting (key, original index) pairs.

## Q3: Counting Inversions

1. Brute-force inversion count (check every pair).
2. Merge-sort-based inversion count.

- Verify both give the same answer on random arrays of size up to 2,000.
- Time both for n = 1,000 to 1,000,000 (stop brute force when it exceeds 60 seconds).
- Use your program to compute the similarity (Kendall tau distance) between two users' rankings of 10 movies, entered from the keyboard.
