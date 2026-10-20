# Longest Common Subsequence

!!! abstract "At a glance"

    - **Problem:** given sequences $X = x_1 \dots x_m$ and $Y = y_1 \dots y_n$, find a longest sequence that is a subsequence of both.
    - **Key idea:** compare the **last** characters. If they match, they end an LCS; otherwise drop one of them. State $c[i][j]$ = LCS length of the prefixes $X[1..i]$, $Y[1..j]$.
    - **Complexity:** $\Theta(mn)$ time; $\Theta(mn)$ space with reconstruction, $\Theta(\min(m,n))$ for the length only; Hirschberg's method reconstructs in linear space.
    - **Pattern:** the template for **two-sequence DP** (edit distance, sequence alignment, shortest common supersequence).
    - **Used in:** `diff` and version control, DNA/protein alignment, plagiarism detection, the ROUGE-L metric for summarization.

## Motivation and Problem Context

When you run `git diff`, the tool must decide which lines were kept, which were deleted, and which were inserted. The kept lines, in order, form a common subsequence of the old and new file; the *longest* such subsequence gives the *smallest* set of changes. The same question, asked about DNA bases instead of lines of code, measures how closely two genes are related.

!!! danger "Subsequence vs substring"

    - **Substring:** contiguous, e.g. `"BCD"` in `"ABCDE"`.
    - **Subsequence:** delete zero or more elements without reordering, e.g. `"ACE"` from `"ABCDE"`.

    LCS is about **subsequences**. The longest common **substring** is a different problem with a different recurrence (it resets to 0 on a mismatch).

| Sequence $X$ | Sequence $Y$ | An LCS | Length |
| --- | --- | --- | --- |
| `ABCDGH` | `AEDFHR` | `ADH` | 3 |
| `AGGTAB` | `GXTXAYB` | `GTAB` | 4 |
| `ABCBDAB` | `BDCABA` | `BCBA` (also `BDAB`, `BCAB`) | 4 |

## Problem Formulation

- **Input:** sequences $X = \langle x_1, \dots, x_m \rangle$ and $Y = \langle y_1, \dots, y_n \rangle$ over any alphabet with an equality test (characters, lines, tokens, DNA bases).
- **Output:** the length of a longest common subsequence, **and** one such subsequence. An LCS need not be unique.
- **Definition:** $Z = \langle z_1, \dots, z_k \rangle$ is a subsequence of $X$ if there are indices $i_1 < i_2 < \dots < i_k$ with $x_{i_t} = z_t$.
- **Notation:** $X_i$ denotes the prefix $\langle x_1, \dots, x_i \rangle$; $X_0$ is empty.

## Intuition

Look at the last characters $x_m$ and $y_n$.

- If they are **equal**, there is an LCS that ends with that character: match them and solve the problem for $X_{m-1}, Y_{n-1}$.
- If they **differ**, at least one of them is not the last character of the LCS, so we can discard $x_m$ or discard $y_n$, and take the better of the two.

Each step shortens a prefix, so the subproblems are always *pairs of prefixes*: only $(m+1)(n+1)$ of them.

## Baseline Approach

Brute force enumerates all $2^m$ subsequences of $X$ and checks each against $Y$ in $O(n)$: $\Theta(n 2^m)$.

Direct recursion on the intuition:

$$
\text{LCS}(i, j) =
\begin{cases}
0 & i = 0 \text{ or } j = 0 \\
\text{LCS}(i-1, j-1) + 1 & x_i = y_j \\
\max\bigl(\text{LCS}(i-1, j),\ \text{LCS}(i, j-1)\bigr) & x_i \ne y_j
\end{cases}
$$

When no characters match, every call branches twice until a prefix becomes empty, so the recursion has one leaf per monotone path from $(m, n)$ to the boundary: exactly $\binom{m+n}{m}$ leaves, which is $\Theta(4^n/\sqrt{n})$ when $m = n$. The running time is exponential (and $O(2^{m+n})$ in general). The call $\text{LCS}(i-1, j-1)$ is reached from both $\text{LCS}(i-1, j)$ and $\text{LCS}(i, j-1)$: classic overlapping subproblems.

## Algorithm Design

Apply the [5-step DP recipe](topic1.md#the-5-step-dp-recipe):

1. **State:** $c[i][j]$ = length of an LCS of $X_i$ and $Y_j$, for $0 \le i \le m$, $0 \le j \le n$.
2. **Transition:** the recurrence above.
3. **Base cases:** $c[i][0] = c[0][j] = 0$ (an empty prefix has only the empty subsequence).
4. **Order:** $c[i][j]$ reads the cells above, to the left, and diagonally up-left; fill row by row, left to right.
5. **Answer:** $c[m][n]$.
6. **Reconstruction:** start at $(m, n)$. If $x_i = y_j$, output $x_i$ and move diagonally; otherwise move to the larger of $c[i-1][j]$ (up) and $c[i][j-1]$ (left). Reverse the output at the end. CLRS stores arrows in a table $b$; recomputing the decision from $c$ needs no extra table.

!!! tip "Filling a cell by hand"

    | diagonal | up |
    | --- | --- |
    | **left** | **current** |

    1. If the row character equals the column character: current = diagonal + 1, arrow ↖.
    2. Otherwise: current = max(up, left), arrow ↑ if up $\ge$ left, else ←.

## Pseudocode

```text
LCS-LENGTH(X, Y)
    m = length(X), n = length(Y)
    let c[0..m, 0..n] be a new table
    for i = 0 to m: c[i, 0] = 0
    for j = 0 to n: c[0, j] = 0
    for i = 1 to m
        for j = 1 to n
            if X[i] == Y[j]
                c[i, j] = c[i-1, j-1] + 1
            else if c[i-1, j] >= c[i, j-1]
                c[i, j] = c[i-1, j]
            else
                c[i, j] = c[i, j-1]
    return c

LCS-RECONSTRUCT(c, X, Y)
    i = length(X), j = length(Y), Z = empty list
    while i > 0 and j > 0
        if X[i] == Y[j]
            append X[i] to Z
            i = i - 1, j = j - 1
        else if c[i-1, j] >= c[i, j-1]
            i = i - 1
        else
            j = j - 1
    return reverse(Z)
```

## Worked Example

$X = \texttt{ABCBDAB}$ ($m = 7$), $Y = \texttt{BDCABA}$ ($n = 6$). Each cell shows the arrow and $c[i][j]$; row 0 and column 0 are all 0. Bold cells lie on the reconstruction path.

| | $j$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $i$ | | | **B** | **D** | **C** | **A** | **B** | **A** |
| 0 | | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | **A** | 0 | ↑0 | ↑0 | ↑0 | ↖1 | ←1 | ↖1 |
| 2 | **B** | 0 | **↖1** | **←1** | ←1 | ↑1 | ↖2 | ←2 |
| 3 | **C** | 0 | ↑1 | ↑1 | **↖2** | **←2** | ↑2 | ↑2 |
| 4 | **B** | 0 | ↖1 | ↑1 | ↑2 | ↑2 | **↖3** | ←3 |
| 5 | **D** | 0 | ↑1 | ↖2 | ↑2 | ↑2 | **↑3** | ↑3 |
| 6 | **A** | 0 | ↑1 | ↑2 | ↑2 | ↖3 | ↑3 | **↖4** |
| 7 | **B** | 0 | ↖1 | ↑2 | ↑2 | ↑3 | ↖4 | **↑4** |

**Traceback** from $(7,6)$:

| Cell | $x_i$ vs $y_j$ | Move | Output so far |
| --- | --- | --- | --- |
| $(7,6)$ | B vs A, up $4 \ge$ left $4$ | ↑ | |
| $(6,6)$ | A = A | ↖ | A |
| $(5,5)$ | D vs B, up $3 \ge$ left $2$ | ↑ | A |
| $(4,5)$ | B = B | ↖ | A B |
| $(3,4)$ | C vs A, up $1 <$ left $2$ | ← | A B |
| $(3,3)$ | C = C | ↖ | A B C |
| $(2,2)$ | B vs D, up $0 <$ left $1$ | ← | A B C |
| $(2,1)$ | B = B | ↖ | A B C B |

Reversed: **LCS = `BCBA`**, length $c[7][6] = 4$. Other LCSs (`BDAB`, `BCAB`) are found with different tie-breaking.

!!! warning "Important"

    Always check your reconstructed answer: it must be a subsequence of **both** strings, in order. A traceback that follows arrows in the wrong direction produces strings like `BADB`, which has the right length but is not a subsequence of `ABCBDAB` (there is no `D` after the `A` at position 6).

## Correctness

**Theorem (optimal substructure of LCS, CLRS 15.1).** Let $Z = \langle z_1, \dots, z_k \rangle$ be any LCS of $X_m$ and $Y_n$.

1. If $x_m = y_n$, then $z_k = x_m = y_n$ and $Z_{k-1}$ is an LCS of $X_{m-1}$ and $Y_{n-1}$.
2. If $x_m \ne y_n$ and $z_k \ne x_m$, then $Z$ is an LCS of $X_{m-1}$ and $Y_n$.
3. If $x_m \ne y_n$ and $z_k \ne y_n$, then $Z$ is an LCS of $X_m$ and $Y_{n-1}$.

**Proof.**

1. If $z_k \ne x_m$, appending $x_m = y_n$ to $Z$ gives a common subsequence of length $k+1$, a contradiction; so $z_k = x_m$. Then $Z_{k-1}$ is a common subsequence of $X_{m-1}, Y_{n-1}$; if a longer one $W$ existed, $W$ followed by $x_m$ would beat $Z$.
2. If $z_k \ne x_m$, then $Z$ does not use $x_m$, so it is a common subsequence of $X_{m-1}$ and $Y_n$. A longer one would also be common to $X_m$ and $Y_n$, contradicting that $Z$ is an LCS.
3. Symmetric to 2.

When $x_m \ne y_n$, $z_k$ cannot equal both, so case 2 or case 3 applies and the max of the two subproblems is correct. **Induction** on $i + j$ (the table is filled so that all three neighbors are computed first) then shows every $c[i][j]$ is correct.

**Reconstruction correctness.** Each traceback step moves to a neighbor whose value explains $c[i][j]$ (diagonal with $+1$ on a match, otherwise the larger neighbor equal to $c[i][j]$), so exactly $c[m][n]$ characters are output, in reverse order of position, and each output character is a matched pair: the result is a common subsequence of length $c[m][n]$.

## Complexity Analysis

| Version | Time | Space |
| --- | --- | --- |
| Brute force | $\Theta(n 2^m)$ | $O(m)$ |
| Naive recursion | exponential, $O(2^{m+n})$ | $O(m+n)$ stack |
| Memoized / bottom-up table | $\Theta(mn)$ | $\Theta(mn)$ |
| Reconstruction | $O(m+n)$ | uses the table |
| Length only, two rows | $\Theta(mn)$ | $\Theta(\min(m,n))$ |
| Hirschberg (length + LCS) | $\Theta(mn)$ | $\Theta(m+n)$ |

Each of the $(m+1)(n+1)$ cells is filled in $O(1)$. The traceback reduces $i + j$ by at least one per step.

**Hirschberg's algorithm (1975)** in one paragraph: compute the last row of LCS lengths for the top half of $X$ against all prefixes of $Y$ (forward, two rows), and for the bottom half against all suffixes of $Y$ (backward, two rows). The column $k$ where forward + backward is maximal is where an optimal path crosses the middle row. Recurse on (top half, $Y[1..k]$) and (bottom half, $Y[k+1..n]$). The work halves at each level, so total time stays $\Theta(mn)$ while space drops to linear. This divide-and-conquer + DP combination is how long sequences are aligned when an $m \times n$ table does not fit in memory.

**Lower bound.** No algorithm is known that solves LCS of two length-$n$ strings in $O(n^{2-\varepsilon})$ time for any $\varepsilon > 0$, and such an algorithm would refute the Strong Exponential Time Hypothesis (Abboud, Backurs, Vassilevska Williams 2015; Bringmann and Künnemann 2015). Practical speedups come from bit-parallelism or from exploiting similarity, not from beating quadratic in general.

## Python Implementation

```python
def lcs(x, y):
    """Return (length, one LCS) of sequences x and y (strings or lists)."""
    m, n = len(x), len(y)
    c = [[0] * (n + 1) for _ in range(m + 1)]   # c[i][j]: LCS length of x[:i], y[:j]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if x[i - 1] == y[j - 1]:
                c[i][j] = c[i - 1][j - 1] + 1
            elif c[i - 1][j] >= c[i][j - 1]:
                c[i][j] = c[i - 1][j]
            else:
                c[i][j] = c[i][j - 1]
    out = []
    i, j = m, n
    while i > 0 and j > 0:                       # walk back from (m, n)
        if x[i - 1] == y[j - 1]:
            out.append(x[i - 1])
            i -= 1
            j -= 1
        elif c[i - 1][j] >= c[i][j - 1]:
            i -= 1
        else:
            j -= 1
    out.reverse()
    return c[m][n], out


def lcs_length_two_rows(x, y):
    """LCS length in O(min(m, n)) extra space."""
    if len(y) > len(x):
        x, y = y, x                              # make the row the shorter sequence
    prev = [0] * (len(y) + 1)
    for i in range(1, len(x) + 1):
        curr = [0] * (len(y) + 1)
        for j in range(1, len(y) + 1):
            if x[i - 1] == y[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev = curr
    return prev[-1]


print(lcs("ABCBDAB", "BDCABA"))                 # (4, ['B', 'C', 'B', 'A'])
print(lcs_length_two_rows("AGGTAB", "GXTXAYB")) # 4
```

- Python strings are 0-indexed, so table cell `c[i][j]` compares `x[i - 1]` with `y[j - 1]`; the extra row and column hold the base cases.
- Returning a list (not a joined string) makes the function work for sequences of lines or tokens, as in a diff tool.
- The tie rule `>=` (prefer up) matches the pseudocode and determines *which* LCS is returned.
- `lcs_length_two_rows` swaps arguments so the stored row has length $\min(m,n) + 1$; it cannot reconstruct the LCS.

## Edge Cases and Pitfalls

| Case / pitfall | What goes wrong | Fix |
| --- | --- | --- |
| Empty $X$ or $Y$ | Indexing `x[-1]` wraps around in Python | Base row/column handle it; the loops do not execute |
| Index shift between table and string | Comparing `x[i]` with `y[j]` skips the first character and overflows at the end | Table index $i$ corresponds to `x[i - 1]` |
| Confusing substring and subsequence | Resetting to 0 on mismatch solves longest common *substring* | Mismatch takes $\max(\text{up}, \text{left})$ |
| Traceback moves to a neighbor with a smaller value | Output shorter than $c[m][n]$, or not a common subsequence | On mismatch move to the neighbor equal to $c[i][j]$ |
| Building the output with string `+=` in the loop | Quadratic time from repeated copying | Append to a list, reverse once |
| Two-row version used to reconstruct | Earlier rows are gone | Keep the table, or use Hirschberg |
| Very long inputs (e.g. $10^5 \times 10^5$) | $10^{10}$ cells: impossible in time and memory | Use diff-specific algorithms (Myers), banding, or heuristics |

## Common Misconceptions

- **"The LCS is unique."** Many LCSs can exist (`BCBA`, `BDAB`, `BCAB` above); the DP returns one, chosen by the tie-breaking rule.
- **"LCS is the same as edit distance."** They are related, not identical. With only insertions and deletions, the edit distance is $m + n - 2\,\text{LCS}(X, Y)$. Levenshtein distance also allows substitutions (cost 1), which this formula does not capture: `"ab"` vs `"cd"` has LCS 0, indel distance 4, but Levenshtein distance 2.
- **"Greedily matching each character at its earliest possible position works."** For $X = \texttt{DABC}$, $Y = \texttt{ABCD}$, greedy matches `D` with the last character of $Y$ and then nothing else fits (length 1), while the LCS is `ABC` (length 3). The DP must keep both options open, which is why the mismatch case takes a max.
- **"LCS generalizes easily to many sequences."** For $k$ sequences the table has $\prod (n_i+1)$ cells, and for an arbitrary number of sequences the problem is NP-hard.
- **"Python's difflib computes an LCS."** `difflib.SequenceMatcher` uses a Ratcliff-Obershelp style approach (repeatedly finding the longest contiguous matching block); its output is human-friendly but is not guaranteed to be a minimal diff.

## Alternatives and Trade-offs

| Approach | Time | Space | When to use |
| --- | --- | --- | --- |
| Full DP table + traceback | $\Theta(mn)$ | $\Theta(mn)$ | Default for moderate sizes; need the LCS |
| Two-row DP | $\Theta(mn)$ | $\Theta(\min(m,n))$ | Only the length (similarity score) is needed |
| Hirschberg | $\Theta(mn)$ | $\Theta(m+n)$ | Long sequences, need the alignment, memory-bound |
| Myers $O(ND)$ diff | $O((m+n)D)$, $D$ = edit distance | linear variants exist | Files that are mostly similar (version control) |
| Hunt-Szymanski | $O((r + n)\log n)$, $r$ = matching pairs | $O(r + n)$ | Few matching pairs (large alphabets, lines of code) |
| Bit-parallel LCS | $O(mn / w)$, $w$ = word size | $O(n/w)$ | Short-alphabet, performance-critical scoring |

**Use the textbook DP** when sizes are up to a few thousand and you need clarity and correctness. **Avoid it** when inputs are huge but similar (use Myers), or when only an approximate similarity score is needed (use hashing/shingling).

## In Practice

- **Version control:** Git's default diff algorithm is Myers' algorithm, which finds a shortest edit script (equivalently, an LCS of lines) in $O((m+n)D)$ time, fast when the files differ in few lines. Git also offers `--minimal`, `--patience`, and `--histogram`, which trade minimality for more readable diffs. The original Unix `diff` was based on the Hunt-McIlroy algorithm, an LCS method that only considers matching line pairs.
- **Bioinformatics:** Needleman-Wunsch (global alignment, 1970) and Smith-Waterman (local alignment, 1981) are LCS-style two-sequence DPs with a scoring matrix for matches/mismatches and gap penalties. Database search tools such as BLAST use fast heuristics (seed-and-extend) precisely because full DP against an entire database is too slow; the DP is used to extend and verify promising seeds, often SIMD-accelerated.
- **NLP evaluation:** ROUGE-L scores a generated summary by the LCS with a reference summary.
- **Plagiarism and code-similarity detection:** token-level LCS (after normalizing identifiers) highlights copied regions that survived reordering of surrounding code.
- **Performance reality:** a Python $5000 \times 5000$ table means 25 million cell updates, which takes seconds; the same loop in C is about two orders of magnitude faster. Memory for full tables grows quickly ($10^4 \times 10^4$ entries in Python lists need close to a gigabyte just for the references), which is why linear-space methods matter.

## Interview and Competitive Programming

**Recognition cues:** two strings/arrays, "delete/insert/replace to make equal", "common", "interleave", "supersequence", "alignment" → two-sequence DP over prefix pairs $(i, j)$.

**Family (same table shape, different transitions):**

| Problem | Match | Mismatch | Base |
| --- | --- | --- | --- |
| LCS | $c[i-1][j-1] + 1$ | $\max(c[i-1][j], c[i][j-1])$ | 0 |
| Longest common substring | $c[i-1][j-1] + 1$ | $0$ (answer = max over table) | 0 |
| Edit distance (Levenshtein) | $E[i-1][j-1]$ | $1 + \min(E[i-1][j], E[i][j-1], E[i-1][j-1])$ | $E[i][0] = i$, $E[0][j] = j$ |
| Shortest common supersequence length | — | — | $m + n - \text{LCS}$ |
| Longest palindromic subsequence | — | — | $\text{LCS}(s, \text{reverse}(s))$ |

**Constraints:** $m, n \le 1000$ to $5000$ → $O(mn)$. If $m, n \le 10^5$, look for extra structure (e.g. LCS of two permutations reduces to LIS in $O(n \log n)$).

**Traps:** off-by-one between string and table indices; returning the substring answer for a subsequence question; memory limits for full tables (roll to two rows if only the length is asked).

## Using AI Assistants Critically

- Generated LCS code often confuses subsequence with substring (resets to 0 on mismatch); test with `("ABCBDAB", "BDCABA")`, whose answer is 4.
- Tracebacks written by assistants frequently produce strings of the right length that are **not** common subsequences; always assert that the result is a subsequence of both inputs.
- Watch for `x[i]` vs `x[i - 1]` indexing errors that pass on examples where the first characters do not matter.
- Claims like "space-optimized LCS that also returns the subsequence in $O(n)$ space" usually omit Hirschberg's recursion and are wrong; check what is actually stored.
- Cross-check with a brute-force LCS (enumerate subsequences of the shorter string) on random strings over a 2-3 letter alphabet, which forces many ties.
- Recommending `difflib` as "an LCS implementation" is inaccurate; it is not guaranteed minimal.

## Practice

### Beginner

1. Fill the LCS table for $X = \texttt{ABCB}$, $Y = \texttt{BDCAB}$ and reconstruct one LCS. *Difficulty: easy.*
2. List all LCSs of $X = \texttt{ABC}$ and $Y = \texttt{ACB}$. *Difficulty: easy.*
3. Compute the indel (insert/delete only) distance between `"kitten"` and `"sitting"` using $m + n - 2\,\text{LCS}$. *Difficulty: easy.*

### Intermediate

1. Modify the reconstruction to return **all** distinct LCSs; discuss why the output can be exponential in size. *Difficulty: medium.*
2. *Longest common substring.* Input: two strings of length $\le 2000$. Output: the longest contiguous common block. Give the recurrence and explain how the answer location differs from LCS. *Difficulty: medium.*
3. *Shortest common supersequence.* Input: two strings of length $\le 1000$. Output: a shortest string containing both as subsequences, built from the LCS table. *Difficulty: medium.*

### Advanced

1. Implement Hirschberg's algorithm and verify that it returns an LCS of the same length as the full-table method on random inputs. *Difficulty: hard.*
2. Show that the LCS of two permutations of $1..n$ can be computed in $O(n \log n)$ by reduction to LIS. *Difficulty: hard.*
3. Design an $O(kn)$ algorithm that decides whether the indel distance between two strings is at most $k$ (banded DP). Justify why cells outside the band can be ignored. *Difficulty: hard.*

### Interview / Competitive Programming

1. *LeetCode 1143 Longest Common Subsequence.* *Difficulty: medium.*
2. *LeetCode 583 Delete Operation for Two Strings.* Minimum deletions to make two strings equal. *Difficulty: medium.*
3. *LeetCode 516 Longest Palindromic Subsequence.* *Difficulty: medium.*

## Self-Check Questions

??? question "Q1. Why is an LCS subproblem identified by a pair of prefixes rather than arbitrary substrings?"
    The recurrence only ever removes the **last** character of $X$, of $Y$, or of both. Starting from the full strings, every reachable subproblem is $(X_i, Y_j)$ for some $i, j$, giving $(m+1)(n+1)$ states.

??? question "Q2. Prove that if x_m = y_n then every LCS of X and Y ends with that character."
    If an LCS $Z$ did not end with $x_m$, then $Z$ uses neither $x_m$ nor $y_n$ as its last matched pair, and appending $x_m$ to $Z$ yields a longer common subsequence, contradicting maximality.

??? question "Q3. The full LCS table uses Θ(mn) memory. How can you get (a) the length and (b) the LCS itself in linear space?"
    (a) Keep only the previous and current rows. (b) Hirschberg: find the column where an optimal path crosses the middle row by combining a forward pass on the top half and a backward pass on the bottom half, then recurse on the two quadrants; time stays $\Theta(mn)$.

??? question "Q4. Relate LCS to edit distance."
    If only insertions and deletions are allowed, every character not in the LCS must be deleted from $X$ or inserted from $Y$: distance $= m + n - 2\,\text{LCS}$. Levenshtein distance also allows substitutions and needs its own DP (same table shape, different transition).

??? question "Q5. What is wrong with this claim: 'LCS(ABCBDAB, BDCABA) = BADB'?"
    The length 4 is right, but `BADB` is not a subsequence of `ABCBDAB`: after matching `B` (position 2) and `A` (position 6), there is no `D` later. A correct LCS is `BCBA`.

??? question "Q6. Git diffs two 50,000-line files that differ in 20 lines. Why would a plain O(mn) DP be a poor choice, and what does Git do instead?"
    $mn = 2.5 \times 10^9$ cells is too slow and too large. Git's Myers algorithm runs in $O((m+n)D)$ with $D$ the edit distance (here about 20), i.e. roughly $2 \times 10^6$ steps, and uses linear space.

??? question "Q7. How does the recurrence change for the longest common substring, and where is the answer?"
    On a match $L[i][j] = L[i-1][j-1] + 1$; on a mismatch $L[i][j] = 0$, because a contiguous block cannot skip characters. The answer is the maximum entry anywhere in the table, not $L[m][n]$.

## Complexity Summary

| Algorithm | Time | Space |
| --- | --- | --- |
| Brute force | $\Theta(n 2^m)$ | $O(m)$ |
| DP table + traceback | $\Theta(mn)$ | $\Theta(mn)$ |
| Length only (two rows) | $\Theta(mn)$ | $\Theta(\min(m,n))$ |
| Hirschberg | $\Theta(mn)$ | $\Theta(m+n)$ |
| Myers diff | $O((m+n)D)$ | $O(m+n)$ (linear-space variant) |
| LCS of two permutations | $O(n \log n)$ | $O(n)$ |

## Key Takeaways

- State $c[i][j]$ over prefix pairs; compare the last characters: match → diagonal $+1$, mismatch → max(up, left).
- Correctness follows from the three-case optimal substructure theorem plus induction on $i + j$.
- $\Theta(mn)$ time; reconstruct by tracing back, and always check that the result is a subsequence of both inputs.
- Length alone needs two rows; Hirschberg recovers the LCS in linear space with divide and conquer.
- LCS anchors the two-sequence DP family: edit distance, alignment, supersequence, palindromic subsequence.
- Real tools (Git, aligners) use LCS ideas but specialize them (Myers, seed-and-extend) for scale.
