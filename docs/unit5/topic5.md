# Counting Sort

!!! abstract "At a glance"

    - **Problem:** sort $n$ records whose keys are integers in a small range $0..k-1$.
    - **Key idea:** do not compare keys; **count** how many times each key occurs, turn the counts into prefix sums that say where each key's block ends, then place every record directly into its final slot.
    - **Complexity:** $\Theta(n + k)$ time and $\Theta(n + k)$ extra space; linear when $k = O(n)$.
    - **Property:** stable (when placing right to left), which makes it the standard digit sort inside [radix sort](topic6.md).
    - **Used in:** histograms, grading and bucketing by small categories, radix sort passes, suffix-array construction, GPU and database sorting of small-domain keys.

## Motivation and Problem Context

[Topic 5.2](topic2.md) proved that any comparison sort needs $\Omega(n \log n)$ comparisons. But many real keys are not arbitrary: exam marks are $0..100$, ages are $0..150$, pixel intensities are $0..255$, ASCII characters are $0..127$, a department code is one of 20 values. When the key range $k$ is small relative to $n$, we can do better than $n \log n$ by **using the key as an array index**, an operation the comparison model forbids.

Scenario: the Royal University of Bhutan needs to rank 40,000 applicants by their total entrance score, an integer from 0 to 300, while keeping applicants with equal scores in the order they applied (earlier application first). A comparison sort costs about $40000 \times \lg 40000 \approx 6 \times 10^5$ comparisons. Counting sort makes two passes over the 40,000 records plus one pass over 301 counters, and it is stable for free.

## Problem Formulation

- **Input:** array $A[0..n-1]$ of records; each record $x$ has an integer key $\text{key}(x) \in \{0, 1, \dots, k-1\}$.
- **Output:** array $B[0..n-1]$ containing the same records in non-decreasing key order.
- **Requirement:** stability: records with equal keys keep their input order.
- **Assumptions:** $k$ is known (or computed as $\max - \min + 1$); keys can be used as array indices in $O(1)$ time (word-RAM model).

## Intuition

If you know that exactly 2 records have key 0, none has key 1, and 2 have key 2, then the key-2 records must occupy positions 2 and 3 of the output, without comparing anything. In general:

> The last record with key $v$ belongs at position (number of records with key $\le v$) $- 1$.

So we need, for every $v$, the number of keys $\le v$: that is a **prefix sum** of the per-key counts. Placing records from the right end of the input, each at the current end of its key's block, preserves the input order among equal keys.

## Baseline Approach

Two simpler ideas and their bottlenecks:

1. **Comparison sort.** $\Theta(n \log n)$; ignores the fact that keys are small integers.
2. **Count and regenerate.** Count occurrences of each key, then write key 0 `count[0]` times, key 1 `count[1]` times, and so on. This is $\Theta(n + k)$ and works for **bare integers**, but it throws away the records themselves: it cannot sort `(score, name)` records, and there is no notion of stability because the output is regenerated rather than moved.

We want the speed of (2) while moving the actual records, stably. The fix is to convert counts into **positions**.

## Algorithm Design

1. **Count.** `count[v]` = number of records with key $v$. One pass over the input: $\Theta(n)$.
2. **Prefix sums.** Replace `count[v]` by `count[0] + ... + count[v]`, the number of records with key $\le v$. Now the block for key $v$ in the output is positions `count[v-1] .. count[v] - 1`. One pass over the counts: $\Theta(k)$.
3. **Place, right to left.** For each record $x$ from the last to the first: decrement `count[key(x)]` and write $x$ at that index. The last record with key $v$ goes to the last slot of $v$'s block, the second-to-last to the slot before it, and so on. One pass: $\Theta(n)$.

**Why prefix sums?** They convert "how many of each key" into "where each key's block ends" in $\Theta(k)$ time, so that every record can be written to its final position in $O(1)$ without any searching.

**Why right to left?** Each block is filled from its end backwards. Scanning the input backwards means the record that appeared last in the input is written into the last slot of its block: the relative order of equal keys is preserved. Scanning left to right with the same decrement-then-write logic **reverses** equal keys. (A left-to-right version is also possible if you instead use exclusive prefix sums, i.e. block **start** positions, and increment after writing.)

!!! warning "Important"

    Stability is the whole reason counting sort is used inside radix sort. An implementation that scans left to right with inclusive prefix sums still produces sorted keys, so it passes tests on bare integers, but it reverses equal keys and makes LSD radix sort produce wrong results.

## Pseudocode

```text
COUNTING-SORT(A, n, k)              // keys in 0..k-1
    let count[0..k-1] be all 0
    let B[0..n-1] be a new array
    for i = 0 to n - 1              // 1. count
        count[key(A[i])] = count[key(A[i])] + 1
    for v = 1 to k - 1              // 2. prefix sums: count[v] = #keys <= v
        count[v] = count[v] + count[v - 1]
    for i = n - 1 downto 0          // 3. place, right to left (stable)
        v = key(A[i])
        count[v] = count[v] - 1
        B[count[v]] = A[i]
    return B
```

## Worked Example

Sort $A = \langle 2, 5, 3, 0, 2, 3, 0, 3 \rangle$ with $k = 6$ (CLRS's classic example).

**Step 1, counts:**

| key $v$ | 0 | 1 | 2 | 3 | 4 | 5 |
| --- | --- | --- | --- | --- | --- | --- |
| `count[v]` | 2 | 0 | 2 | 3 | 0 | 1 |

**Step 2, prefix sums** (number of keys $\le v$):

| key $v$ | 0 | 1 | 2 | 3 | 4 | 5 |
| --- | --- | --- | --- | --- | --- | --- |
| `count[v]` | 2 | 2 | 4 | 7 | 7 | 8 |

So key 0 occupies $B[0..1]$, key 2 occupies $B[2..3]$, key 3 occupies $B[4..6]$, key 5 occupies $B[7]$.

**Step 3, placement from right to left:**

| $i$ | $A[i]$ | `count[A[i]]` after decrement | $B$ after write |
| --- | --- | --- | --- |
| 7 | 3 | 6 | `_ _ _ _ _ _ 3 _` |
| 6 | 0 | 1 | `_ 0 _ _ _ _ 3 _` |
| 5 | 3 | 5 | `_ 0 _ _ _ 3 3 _` |
| 4 | 2 | 3 | `_ 0 _ 2 _ 3 3 _` |
| 3 | 0 | 0 | `0 0 _ 2 _ 3 3 _` |
| 2 | 3 | 4 | `0 0 _ 2 3 3 3 _` |
| 1 | 5 | 7 | `0 0 _ 2 3 3 3 5` |
| 0 | 2 | 2 | `0 0 2 2 3 3 3 5` |

**Stability check with records.** Sorting $\langle (2,a), (1,b), (2,c), (1,d), (0,e) \rangle$ by the number gives $\langle (0,e), (1,b), (1,d), (2,a), (2,c) \rangle$: $b$ before $d$ and $a$ before $c$, as in the input.

## Correctness

**Lemma (block positions).** After step 2, `count[v]` equals $c_{\le v}$, the number of records with key $\le v$. Records with key $v$ must occupy exactly the positions $c_{\le v-1}, \dots, c_{\le v} - 1$ of a sorted output (all smaller keys come first).

**Loop invariant for step 3.** At the start of the iteration for index $i$ (going down from $n-1$), for every key $v$:

- `count[v]` $= c_{\le v-1} + (\text{number of records with key } v \text{ in } A[0..i])$, and
- the records with key $v$ from $A[i+1..n-1]$ already occupy positions `count[v]` $.. c_{\le v} - 1$ of $B$, in their input order.

- **Initialization** ($i = n-1$): `count[v]` $= c_{\le v}$, which equals $c_{\le v-1}$ plus all records with key $v$; no records placed.
- **Maintenance:** let $v = \text{key}(A[i])$. Decrementing `count[v]` gives the slot immediately before the already placed key-$v$ records; writing $A[i]$ there keeps all placed key-$v$ records in input order (since $A[i]$ precedes them in the input) and keeps the count formula true for $A[0..i-1]$. Other keys are untouched.
- **Termination** ($i = -1$): `count[v]` $= c_{\le v-1}$, and all key-$v$ records fill positions $c_{\le v-1}..c_{\le v}-1$ in input order. By the lemma, $B$ is sorted, and it is stable.

## Complexity Analysis

| Step | Time |
| --- | --- |
| Initialise `count` | $\Theta(k)$ |
| Count | $\Theta(n)$ |
| Prefix sums | $\Theta(k)$ |
| Place | $\Theta(n)$ |
| **Total** | $\Theta(n + k)$ |

There is no best, average or worst case distinction: the time depends only on $n$ and $k$, never on the order of the input. Extra space is $\Theta(k)$ for `count` plus $\Theta(n)$ for the output array.

### The $k$ versus $n$ trade-off

| Key range $k$ | Counting sort | Better choice |
| --- | --- | --- |
| $k = O(1)$ (e.g. 3 categories) | $\Theta(n)$ | Counting sort or Dutch national flag |
| $k = O(n)$ (e.g. scores $0..n$) | $\Theta(n)$ | Counting sort |
| $k = n^2$ (e.g. keys up to $10^{10}$ with $n = 10^5$) | $\Theta(n^2)$ time **and memory** | [Radix sort](topic6.md): $\Theta(n)$ with 2 passes of base $n$ |
| $k = 2^{32}$ or $2^{64}$ | infeasible: $2^{32}$ counters is 16 GB at 4 bytes each | Radix sort or comparison sort |

Rule of thumb: counting sort is attractive when $k \le c \cdot n$ for a small constant $c$; otherwise split keys into digits and use radix sort.

!!! warning "Important"

    Counting sort does not contradict the $\Omega(n \log n)$ lower bound: it never compares keys, it uses them as indices. Its running time is $\Theta(n + k)$, which is **linear only if $k = O(n)$**. Writing "counting sort is $O(n)$" without the condition is a common exam error.

## Python Implementation

```python
def counting_sort(a, k, key=lambda x: x):
    """Stable sort of a by integer keys in range 0..k-1. Returns a new list."""
    count = [0] * k
    for x in a:
        count[key(x)] += 1
    # prefix sums: count[v] becomes the number of keys <= v
    for v in range(1, k):
        count[v] += count[v - 1]
    out = [None] * len(a)
    for x in reversed(a):              # right-to-left preserves stability
        count[key(x)] -= 1
        out[count[key(x)]] = x
    return out


def sort_integers(a):
    """Sort arbitrary (possibly negative) integers when max - min is small."""
    if not a:
        return []
    low = min(a)
    k = max(a) - low + 1
    return counting_sort(a, k, key=lambda x: x - low)
```

- The `key` parameter lets the same routine sort records by one integer field, which is what [radix sort](topic6.md) needs (key = one digit).
- `reversed(a)` iterates right to left without copying.
- `sort_integers` shifts keys by the minimum so negative numbers work; the range is $\max - \min + 1$, so a single outlier (e.g. one key of $10^9$) makes $k$ huge.
- Tested against `sorted()` on random inputs with negatives and duplicates, and for stability against Python's stable `sorted(..., key=...)` on `(key, index)` records.

## Edge Cases and Pitfalls

| Case / pitfall | What goes wrong | Fix |
| --- | --- | --- |
| Placing left to right with "decrement then write" | Equal keys come out reversed: unstable; breaks radix sort | Iterate right to left, or use exclusive prefix sums (block starts) and increment |
| Negative keys | Negative index: Python silently wraps around, other languages crash | Offset by the minimum key |
| Key equal to $k$ (off-by-one in range) | Index out of range | Allocate $k = \max + 1$ counters for keys $0..\max$ |
| Huge range with few elements | $\Theta(k)$ time and memory dominates; out of memory | Use radix sort or a comparison sort; compress coordinates if values are reused |
| Floating-point keys | Cannot index by a float | Map to integers (e.g. fixed-point) or use comparison/bucket sort |
| Empty input | `min()`/`max()` raise on empty list | Return early |
| Sorting in place by overwriting $A$ during placement | Records are overwritten before being read | Use a separate output array $B$ (counting sort is not in place) |

## Common Misconceptions

- **"Counting sort is always $O(n)$."** It is $\Theta(n + k)$; with $k \gg n$ it is slower than a comparison sort.
- **"Counting sort is in place."** It needs $\Theta(n + k)$ extra memory.
- **"Stability does not matter for integers."** For bare integers it is unobservable, but counting sort is mostly used on records or as a radix-sort pass, where stability is essential.
- **"The count-and-regenerate version is the same algorithm."** It only works for bare keys; it cannot carry satellite data.
- **"Counting sort has a worst-case input."** Its running time does not depend on input order at all.

## Alternatives and Trade-offs

| Algorithm | Time | Extra space | Stable | Requirement on keys |
| --- | --- | --- | --- | --- |
| Counting sort | $\Theta(n + k)$ | $\Theta(n + k)$ | Yes | Integers in a range of size $k$ |
| [Radix sort](topic6.md) (LSD) | $\Theta(d(n + r))$ | $\Theta(n + r)$ | Yes | $d$ digits in base $r$ |
| Bucket sort | $\Theta(n)$ expected | $\Theta(n)$ | Yes (with stable bucket sort) | Roughly uniform distribution |
| [Merge sort](../unit3/topic6.md) | $\Theta(n \log n)$ | $\Theta(n)$ | Yes | Any total order |
| [Quicksort](topic3.md) / introsort | $\Theta(n \log n)$ | $O(\log n)$ | No | Any total order |

**When to use:** small integer keys or categories, $k = O(n)$; stable grouping of records by a small field; as the digit sort in radix sort; computing histograms or ranks in one pass.

**When NOT to use:** keys with a large or unknown range; floating-point or composite keys without a small integer mapping; memory-constrained settings where $\Theta(n + k)$ extra space is unacceptable; very small $n$ (library sort is simpler and fast enough).

## In Practice

- **Radix sort passes.** Every LSD radix sort pass is a counting sort on one digit (often one byte, $k = 256$). GPU sorting libraries such as NVIDIA CUB's radix sort and many database engines use exactly this pattern for integer and fixed-width keys.
- **Histogram-based processing.** Image processing (histogram equalisation on 8-bit pixels), compression (frequency counting before building Huffman codes) and analytics (`GROUP BY` on small categorical columns) all use the count-then-prefix-sum pattern.
- **Prefix sums as a parallel primitive.** On GPUs and multi-core CPUs, the "count, prefix-sum, scatter" structure of counting sort parallelises well: each thread counts its chunk, a parallel scan computes offsets, and each thread scatters its records independently. The same pattern is used for stream compaction and partitioning in data-parallel systems.
- **Suffix arrays and string algorithms.** Linear-time suffix-array constructions (and the common $O(n \log n)$ prefix-doubling method) rely on stable counting-sort passes over integer ranks, as used in bioinformatics for genome indexing.
- **Memory realities.** For $k$ in the millions, the `count` array no longer fits in cache and random increments become cache misses; at that point radix sort with smaller digits is usually faster even though both are "linear".

## Interview and Competitive Programming

**Recognition cues**

- "Values are in $[0, 100]$ / $[1, 10^5]$ / lowercase letters" → counting array instead of sorting.
- "Sort by frequency", "top $k$ frequent with $O(n)$" → counting + buckets indexed by frequency (LeetCode 347 Top K Frequent Elements, LeetCode 451 Sort Characters By Frequency).
- "How many numbers are smaller than each element" with small values → prefix sums of counts (LeetCode 1365 How Many Numbers Are Smaller Than the Current Number).
- "H-index" with citations bounded by $n$ → counting with values capped at $n$ (LeetCode 274 H-Index).
- "Sort array A by the order defined in array B" → counting by position (LeetCode 1122 Relative Sort Array).

**Constraints to complexity**

| Constraint | Signal |
| --- | --- |
| $n \le 10^6$, values $\le 10^6$ | Counting sort $\Theta(n + k)$ fits easily |
| values $\le 10^9$, $n \le 10^5$ | Counting sort infeasible; sort or coordinate-compress |
| 26 letters / 10 digits | $k$ is a constant: $\Theta(n)$ |

**Traps**

- Allocating `[0] * (10**9)` in Python: memory error or time limit.
- Forgetting that values may be negative in hidden tests.
- Using the regenerate version when indices or satellite data are needed.

## Using AI Assistants Critically

- LLM-generated counting sort often places elements left to right after inclusive prefix sums, producing a **non-stable** sort that still passes integer-only tests. Test stability explicitly with `(key, index)` records.
- Generated code frequently allocates `max(a)` counters instead of `max(a) + 1`, or ignores negative numbers. Include `0`, the maximum value and negative values in your tests.
- Assistants tend to call counting sort "$O(n)$" unconditionally; check that the answer mentions $k$.
- Some generated versions mutate the input while placing; compare the input before and after, or assert the output is a permutation using `collections.Counter`.
- Verify with a brute-force oracle: `counting_sort(xs, k) == sorted(xs)` and, for records, `== sorted(records, key=...)` (Python's `sorted` is stable, so it is a correct stability oracle).
- For performance claims, time $n = 10^6$ with $k = 10^2$ versus $k = 10^7$: the second is dominated by the counter array, confirming the $\Theta(n + k)$ model.

## Practice

**Beginner**

1. *Trace.* Input: $\langle 6, 0, 2, 0, 1, 3, 4, 6, 1, 3, 2 \rangle$, $k = 7$. Output: the count array, the prefix-sum array, and $B$ after each placement. Difficulty: easy.
2. *Grades.* Input: $n$ student records with integer marks $0..100$. Output: records sorted by mark, stable. Constraints: $n \le 10^5$. Difficulty: easy.
3. *Letters.* Input: a string of lowercase letters. Output: the string with its characters sorted, in $\Theta(n)$. Constraints: length $\le 10^6$. Difficulty: easy.

**Intermediate**

1. *Left-to-right stable variant.* Rewrite counting sort to scan the input left to right while remaining stable. Prove it with a loop invariant. Difficulty: medium.
2. *Range queries.* Input: $n$ integers in $[0, k)$ and $q$ queries "how many values lie in $[a, b]$?". Output: answers in $O(1)$ each after $O(n + k)$ preprocessing. Difficulty: medium.
3. *Sort by frequency.* Input: an array of integers. Output: values sorted by decreasing frequency, ties by increasing value, in $O(n + k)$. Difficulty: medium.

**Advanced**

1. *In-place counting sort.* Design an in-place (unstable) variant that uses $O(k)$ extra space by cycling elements into their blocks (American-flag style). Analyse its time. Difficulty: hard.
2. *Parallel counting sort.* Describe a $p$-processor version using per-processor counts and a prefix-sum (scan) across processors; give its work and span. Difficulty: hard.
3. *Choosing k.* Given $n$ 64-bit keys, derive when splitting into two 32-bit digits beats a single counting pass, accounting for memory. Difficulty: hard.

**Interview / CP**

1. *LeetCode 75 Sort Colors.* Input: array of 0, 1, 2. Output: sorted in place; solve once with counting (two passes) and once in one pass. Difficulty: medium.
2. *LeetCode 274 H-Index.* Input: citation counts, $n \le 5000$. Output: the h-index in $O(n)$ using counting. Difficulty: medium.
3. *LeetCode 1122 Relative Sort Array.* Input: arrays `arr1`, `arr2` with values $\le 1000$. Output: `arr1` sorted by the order of `arr2`, then remaining values ascending. Difficulty: easy.

## Self-Check Questions

??? question "Q1. What does `count[v]` hold after the prefix-sum step, and why is that useful?"

    The number of records with key $\le v$. That is one past the last output index of key $v$'s block, so records can be placed directly into their final positions.

??? question "Q2. Why must the placement loop go from right to left?"

    Each block is filled from its end backwards. Going right to left puts the last input occurrence into the last slot, preserving input order among equal keys. Left to right would reverse them.

??? question "Q3. What is the running time of counting sort when $k = n^2$? What should you use instead?"

    $\Theta(n^2)$ time and memory. Use radix sort with base $n$: two counting-sort passes, $\Theta(n)$ total.

??? question "Q4. Does counting sort have a best case and a worst case?"

    No. It always does the same passes: $\Theta(n + k)$ regardless of the input order.

??? question "Q5. Why does counting sort not violate the $\Omega(n \log n)$ bound?"

    It never compares two keys. Indexing `count[key]` branches $k$ ways at once using the key's value, which is outside the comparison model.

??? question "Q6. A colleague wants to counting-sort 1000 timestamps in milliseconds since 1970. Good idea?"

    No: the range is about $10^{12}$, so the count array is infeasible. Either subtract the minimum (if the timestamps span a short interval) or use radix sort / the library sort.

??? question "Q7. Is counting sort in place? What extra memory does it use?"

    No. It uses $\Theta(k)$ for counts and $\Theta(n)$ for the output array.

## Complexity Summary

| Measure | Counting sort |
| --- | --- |
| Time (all cases) | $\Theta(n + k)$ |
| Extra space | $\Theta(n + k)$ |
| Comparisons between keys | 0 |
| Stable | Yes (right-to-left placement) |
| In place | No |
| Linear when | $k = O(n)$ |

## Key Takeaways

- Counting sort uses keys as indices: count, prefix-sum, place.
- Prefix sums convert counts into final block positions in $\Theta(k)$ time.
- Right-to-left placement makes it stable, which is why it powers radix sort.
- Time and space are $\Theta(n + k)$, independent of input order; linear only when $k = O(n)$.
- It escapes the comparison lower bound by leaving the comparison model, not by being a faster comparison sort.
- For large key ranges, split keys into digits and use radix sort instead.
