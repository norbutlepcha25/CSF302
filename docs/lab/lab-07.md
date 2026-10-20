# Lab 7: Greedy and Randomized Algorithms

Notes: [7.2 Fractional Knapsack](../unit7/topic2.md), [7.3 Huffman Coding](../unit7/topic3.md), [7.4 Activity Selection](../unit7/topic4.md), [7.5 Dijkstra](../unit7/topic5.md), [7.6 MST](../unit7/topic6.md), [7.7 Randomized Algorithms](../unit7/topic7.md)

## Q1: Activity Selection and Knapsack

1. Implement greedy activity selection (earliest finish time). Read activities as (start, finish) pairs and print the selected set.
2. Implement two other greedy rules (earliest start, shortest duration) and find, by random testing, an input where each gives a smaller answer than earliest finish.
3. Implement fractional knapsack (highest value/weight ratio first).
4. Apply the same greedy rule to 0/1 knapsack and compare it with a DP solution on random inputs. Report the worst ratio of greedy to optimal value you find.

## Q2: Huffman Coding

1. Build a Huffman tree from the character frequencies of a text file (use a priority queue; `heapq` is allowed).
2. Print the code table.
3. Encode the file into a bit string and decode it back. Verify the decoded text equals the original.
4. Report the compression ratio compared with 8-bit fixed-length encoding for at least three different text files.

## Q3: Shortest Paths and Minimum Spanning Trees

1. Implement Dijkstra's algorithm with a binary heap. Read a weighted directed graph from a file and print the shortest distance and path from a source to every vertex.
2. Implement Kruskal's algorithm (with union-find) and Prim's algorithm (with a heap).
3. Verify both MST algorithms give the same total weight on random connected graphs.
4. Time Kruskal and Prim for V = 1,000 on a sparse graph (E ≈ 3V) and a dense graph (E ≈ V²/4). Explain which wins on each.
5. Add one negative edge to a small graph and show an input where Dijkstra gives a wrong answer.

## Q4: Randomized Algorithms

1. Implement randomized quickselect to find the k-th smallest element. Compare its time with sorting and indexing for n = 10⁴ to 10⁶.
2. Implement the Miller–Rabin primality test. Compare it with trial division (√n) on 20 random 12-digit numbers, and check both agree.
3. Run Miller–Rabin with 1 round on the Carmichael number 561 a thousand times and report how often it answers "prime".
