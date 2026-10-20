# Role of Algorithms in Computing

!!! abstract "At a glance"

    - **Question:** why study algorithms at all, when hardware keeps getting faster and libraries already implement the classics?
    - **Key idea:** the order of growth of an algorithm decides what is *feasible*; a better algorithm on slow hardware beats a worse one on fast hardware once $n$ is large.
    - **Worked example:** at $n = 10^9$, a $2n^2$ algorithm on a machine doing $10^{10}$ operations/s needs about 6.3 years; a $50\, n \log_2 n$ algorithm on a machine 1000 times slower needs about 42 hours.
    - **Today:** search, routing, compression, cryptography, databases, and machine learning are all built on algorithms covered in this course.

## Motivation and Problem Context

A common belief among new developers is that efficiency is a hardware problem: if code is slow, buy a bigger server, or wait for next year's processor. That view fails in three ways:

1. **Data grows faster than hardware.** Logs, sensor streams, genomes, and training corpora grow by orders of magnitude; a quadratic algorithm's cost grows by the *square* of that.
2. **Some problems are infeasible at any speed.** An exponential algorithm on $n = 100$ needs on the order of $2^{100} \approx 10^{30}$ steps; no conceivable hardware completes that.
3. **Cost and energy are real.** Cloud bills, battery life, and data-centre energy all scale with the operations performed.

This topic explains the role algorithms play in computing: where they came from, why their efficiency remains decisive, and where they appear in systems you use every day.

## Problem Formulation

The question this topic answers can be stated precisely:

- **Given:** a problem with input size $n$, a time budget $T$, and hardware performing $s$ basic operations per second.
- **Ask:** for an algorithm with cost $f(n)$, what is the largest $n$ with $f(n)/s \le T$? How does that change if $s$ grows by a factor $k$, versus if $f$ is replaced by a function of lower order?
- **Assumption:** costs are counted as in [2.1](topic1.md) under the [Word-RAM model](topic2.md); constants are included where we want concrete numbers.

## Intuition

Hardware speed multiplies the budget; algorithms change the function. If the hardware becomes $k$ times faster:

- for $f(n) = n$, the solvable $n$ grows by $k$;
- for $f(n) = n^2$, it grows only by $\sqrt{k}$;
- for $f(n) = 2^n$, it grows only by an *additive* $\log_2 k$.

A thousand-fold faster machine lets an exponential algorithm handle about 10 more items. Replacing that algorithm with a polynomial one changes the solvable size from tens to millions. This is the central reason algorithm design matters.

## Historical Perspective

| Period | Milestone | Why it matters |
|---|---|---|
| c. 1800–1600 BCE | Babylonian clay tablets record step-by-step numerical procedures | algorithms predate computers by millennia |
| c. 300 BCE | Euclid's algorithm for the greatest common divisor (*Elements*) | one of the oldest algorithms still in daily use (cryptography, fractions) |
| c. 3rd century BCE | Sieve of Eratosthenes for primes | early example of trading memory for speed |
| c. 9th century CE | al-Khwarizmi's works on arithmetic and algebra | the Latinised form of his name gives us the word "algorithm" |
| 1843 | Ada Lovelace's notes include a procedure for computing Bernoulli numbers on Babbage's Analytical Engine | often called the first published computer program |
| 1936 | Turing machines and Church's lambda calculus formalise "computation" | gives a precise meaning to "algorithm" and shows some problems are undecidable |
| 1945–1962 | Merge sort (von Neumann), Huffman coding (1952), Dijkstra's shortest paths (1959), Quicksort (Hoare) | the core algorithms of this course appear with the first computers |
| 1965 | Cooley–Tukey FFT; Hartmanis–Stearns found complexity theory; Edmonds argues polynomial time is the right notion of "efficient" | efficiency becomes a mathematical subject |
| 1968 onward | Knuth's *The Art of Computer Programming* | systematic analysis of algorithms as a discipline |
| 1969–1971 | Strassen's matrix multiplication; Cook's NP-completeness theorem | "obvious" bounds can be beaten; some problems are probably intractable |
| 1976–1977 | Diffie–Hellman key exchange; RSA | public-key cryptography rests on efficient modular arithmetic plus hard problems |
| 1990s–2000s | Web search (PageRank), large-scale distributed algorithms (MapReduce) | algorithms at internet scale |
| 2010s–present | Deep learning at scale; the Transformer (2017); IO-aware kernels such as FlashAttention | matrix multiplication, gradient computation and memory-efficient algorithms drive AI |

Euclid's algorithm illustrates the whole story in miniature: a 2,300-year-old procedure whose number of steps grows only logarithmically in the size of its inputs, used today inside every RSA key generation.

## Why Efficiency Matters Even With Fast Hardware

### Worked example: $n^2$ versus $n \log n$ at $n = 10^9$

Sort $n = 10^9$ records (roughly the size of a large web log).

- **Machine A** executes $10^{10}$ operations per second and runs an insertion-sort-like algorithm needing $2n^2$ operations.
- **Machine B** is **1000 times slower** ($10^7$ operations per second) and runs a merge-sort-like algorithm needing $50\, n \log_2 n$ operations (a deliberately large constant).

$$
T_A = \frac{2 \cdot (10^9)^2}{10^{10}} = 2 \times 10^8 \text{ s} \approx 6.3 \text{ years},
\qquad
T_B = \frac{50 \cdot 10^9 \cdot \log_2 10^9}{10^7} \approx \frac{50 \cdot 10^9 \cdot 29.9}{10^7} \approx 1.5 \times 10^5 \text{ s} \approx 42 \text{ hours}.
$$

The slower machine with the better algorithm wins by a factor of more than 1300. At $n = 10^6$ the gap is far smaller ($T_A = 200$ s, $T_B \approx 100$ s), and for small enough $n$ machine A wins. **The advantage of a better order of growth increases without bound as $n$ grows.**

!!! warning "Important"

    Do not conclude that constants never matter. They decide the winner at small and moderate $n$, and real libraries combine algorithms for that reason ([2.1](topic1.md), Key Results). The claim is narrower and stronger: for large enough $n$, **no constant-factor hardware advantage compensates for a worse order of growth**.

### Largest problem solvable in a time budget

At $10^9$ simple operations per second (cost exactly $f(n)$, no constants):

| $f(n)$ | 1 second | 1 minute | 1 hour | 1 day |
|---|---|---|---|---|
| $\log_2 n$ | effectively unlimited | effectively unlimited | effectively unlimited | effectively unlimited |
| $n$ | $1.0 \times 10^9$ | $6.0 \times 10^{10}$ | $3.6 \times 10^{12}$ | $8.6 \times 10^{13}$ |
| $n \log_2 n$ | $4.0 \times 10^7$ | $1.9 \times 10^9$ | $9.9 \times 10^{10}$ | $2.1 \times 10^{12}$ |
| $n^2$ | 31,622 | 244,948 | $1.9 \times 10^6$ | $9.3 \times 10^6$ |
| $n^3$ | 1,000 | 3,914 | 15,326 | 44,208 |
| $2^n$ | 29 | 35 | 41 | 46 |

Going from one second to one day (86,400× more time) multiplies the feasible $n$ by about 86,400 for linear time, by about 294 for quadratic time, and adds only 17 for exponential time.

### Algorithms as a technology

Algorithms deserve the same engineering attention as hardware, networks, or databases, because:

- **They determine feasibility,** as the table shows.
- **They compound with hardware.** A faster machine runs a good algorithm faster too; the gains multiply.
- **They are often the cheapest improvement.** Replacing a quadratic join with a hash join, or adding an index, can turn hours into seconds with no new hardware.
- **They are embedded in everything else.** Compilers (register allocation, parsing), operating systems (scheduling, page replacement), networks (routing), and databases (query optimisation) are all collections of algorithms.
- **They define limits.** Lower bounds ([5.2](../unit5/topic2.md)) and intractability results tell engineers when to stop searching for a faster exact algorithm and switch to approximation or heuristics.

## Current Applications

| Domain | Problem | Algorithmic core | Where in this course |
|---|---|---|---|
| Web search | find relevant documents among billions in milliseconds | inverted indexes (sorted posting lists, merging), link analysis (PageRank as an iterative linear-algebra computation), top-$k$ selection | sorting and merging: [Unit 5](../unit5/overview.md) |
| Navigation and routing | shortest route in a road network; packet routing | Dijkstra's algorithm (link-state protocols such as OSPF), A*, preprocessing-based speedups such as contraction hierarchies | [7.5 Dijkstra](../unit7/topic5.md) |
| Compression | shrink files and network traffic losslessly | DEFLATE (LZ77 + Huffman coding) in gzip, zlib, PNG; transform coding in JPEG | [7.3 Huffman](../unit7/topic3.md) |
| Cryptography | secure communication (TLS), digital signatures | modular exponentiation by repeated squaring, Euclid/extended Euclid for inverses, hashing | [4.6 Modular Power](../unit4/topic6.md), [Unit 1](../unit1/overview.md) |
| Databases | answer queries over huge tables | B+ tree indexes, hash join and sort-merge join, external sorting, dynamic-programming join-order optimisation | [Unit 5](../unit5/overview.md), [Unit 6](../unit6/overview.md) |
| ML training and inference | fit and run models with billions of parameters | matrix multiplication, gradient computation by reverse-mode automatic differentiation (backpropagation), attention (quadratic in sequence length), memory-efficient kernels | [4.2 Strassen](../unit4/topic2.md) for the matrix-multiply story |
| Vector search / retrieval for LLMs | nearest neighbours among millions of embeddings | approximate nearest-neighbour graphs (e.g. HNSW), quantisation | trade exactness for speed |
| Signal and image processing | filtering, audio, convolution in large CNN layers | Fast Fourier Transform, $\Theta(n \log n)$ convolution | [4.4 FFT](../unit4/topic4.md) |
| Bioinformatics | align DNA/protein sequences | dynamic programming (edit distance, Needleman–Wunsch, Smith–Waterman), heuristic seeding (BLAST) | [6.4 LCS](../unit6/topic4.md) |
| Scheduling and logistics | assign jobs, plan deliveries | greedy algorithms, matching, integer programming | [Unit 7](../unit7/overview.md) |

!!! tip "Pattern to notice"

    Almost every row combines an exact algorithm from this course with an engineering compromise: indexing (preprocess once, query many times), approximation (ANN search), or hardware awareness (cache- and GPU-friendly kernels). Knowing the exact algorithm and its complexity is what lets you judge the compromise.

## Python Implementation

Two small tools: a calculator for "largest feasible $n$" (reproduces the table above) and Euclid's algorithm compared with the obvious brute-force GCD.

```python
import math

GROWTH = {
    "log n": lambda n: math.log2(n),
    "n": lambda n: n,
    "n log n": lambda n: n * math.log2(n),
    "n^2": lambda n: n ** 2,
    "n^3": lambda n: n ** 3,
    "2^n": lambda n: 2.0 ** n if n < 1024 else math.inf,
}


def largest_n(cost, budget_seconds, ops_per_second=1e9, limit=10 ** 18):
    """Largest n <= limit with cost(n) within budget (0 if even n = 1 is too slow)."""
    budget_ops = budget_seconds * ops_per_second
    if cost(1) > budget_ops:
        return 0
    lo, hi = 1, 2
    while hi <= limit and cost(hi) <= budget_ops:
        lo, hi = hi, hi * 2
    hi = min(hi, limit + 1)
    # Invariant: cost(lo) fits the budget; hi is too slow or beyond the limit.
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if cost(mid) <= budget_ops:
            lo = mid
        else:
            hi = mid
    return lo


def gcd_euclid(a, b):
    """Euclid's algorithm; returns (gcd, number of division steps)."""
    steps = 0
    while b != 0:
        a, b = b, a % b
        steps += 1
    return a, steps


def gcd_brute(a, b):
    """Try every candidate from min(a, b) down; returns (gcd, candidates tried)."""
    tried = 0
    for d in range(min(a, b), 0, -1):
        tried += 1
        if a % d == 0 and b % d == 0:
            return d, tried
    return max(a, b), tried
```

Walkthrough:

- `largest_n` doubles `hi` until the cost exceeds the budget, then binary-searches between the last feasible and first infeasible size. It relies on `cost` being non-decreasing, which holds for every growth function here. `largest_n(GROWTH["n^2"], 1)` returns 31622.
- `2.0 ** n` would overflow to an error for huge `n`, so the lambda returns infinity beyond 1023, which the search treats as "too slow".
- `gcd_euclid(1071, 462)` returns `(21, 3)`; `gcd_brute(1071, 462)` tries 442 candidates. For $a, b$ near $10^{12}$, Euclid needs at most a few dozen steps (its step count is $O(\log \min(a,b))$, with consecutive Fibonacci numbers as the worst case), while brute force could need up to $10^{12}$.

## Edge Cases and Pitfalls

| Case / pitfall | What goes wrong | Fix |
|---|---|---|
| Comparing algorithms only at small $n$ | the asymptotically worse algorithm looks better | evaluate at the production $n$, or compute the crossover |
| Ignoring constants entirely | a "better" algorithm with huge constants loses at all practical $n$ (some theoretical matrix-multiplication algorithms are like this) | include realistic constants when $n$ is bounded |
| Assuming hardware scaling fixes exponential cost | 1000× speedup adds only about 10 to feasible $n$ for $2^n$ | change the algorithm, restrict the input, or approximate |
| Forgetting preprocessing cost | an index makes queries fast but must be built and maintained | analyse build cost + per-query cost × number of queries |
| Optimising the wrong part | algorithmic work spent on a step that is 1% of runtime | profile first, then improve the dominant step |

## Common Misconceptions

- **"Hardware improvements made algorithm design obsolete."** Hardware improvement multiplies throughput by a constant; data volumes grow too. The order of growth still decides feasibility, as the worked example shows.
- **"Libraries already implement every algorithm, so understanding them is unnecessary."** Choosing the right library call, data structure, or database index requires knowing complexities; misuse (e.g. `list` membership tests in a loop) is a common source of slow code.
- **"Algorithms are only about speed."** They are also about memory, energy, I/O, network messages, correctness guarantees, and security (constant-time cryptographic code avoids leaking secrets through timing).
- **"An exponential algorithm is always useless."** For small, bounded $n$ (e.g. $n \le 20$ in a configuration search) it may be the simplest correct choice. The issue is unbounded growth, not exponentials per se.
- **"AI models replace algorithms."** Training and running models is itself built on algorithms (matrix multiplication, automatic differentiation, nearest-neighbour search), and their cost is analysed with exactly the tools of this unit.

## Alternatives and Trade-offs

Ways to make a slow system fast, compared:

| Lever | Typical gain | Limit | Use when |
|---|---|---|---|
| Better algorithm (lower order of growth) | grows without bound with $n$ | may not exist; may be complex | $n$ is large or growing |
| Better constants (tuning, compiled code, vectorisation) | constant factor | does not change scaling | algorithm is already optimal in order |
| Faster hardware | constant factor | cost, physical limits | quick fix for a bounded workload |
| Parallelism / distribution | up to number of processors, minus coordination overhead | inherently sequential parts (Amdahl's law) | work is divisible |
| Preprocessing / indexing / caching | queries become much cheaper | build cost, memory, staleness | many queries over slowly changing data |
| Approximation / heuristics | can turn intractable into fast | answer not exact or not guaranteed optimal | exact problem is NP-hard or too slow |

## In Practice

- Production sorting uses carefully engineered hybrids (Timsort/Powersort in CPython, introsort-style `std::sort` in C++, pattern-defeating quicksort variants in Rust's unstable sort), illustrating that asymptotic choice and constant-factor engineering go together.
- Database query optimisers choose among algorithms (nested-loop, hash, or merge join) using cost models: an automated version of the analysis in this unit.
- In ML engineering, the quadratic cost of attention in sequence length motivates a large body of work on memory-efficient exact kernels and on approximate or sub-quadratic alternatives.
- Large-scale systems often prefer simpler $O(n \log n)$ algorithms with predictable memory access over theoretically faster but cache-hostile ones.

## Interview and Competitive Programming

- Interviewers expect you to state the complexity of your first idea, explain its bottleneck, and improve it. That is the "baseline → bottleneck → better algorithm" workflow formalised in [2.4](topic4.md).
- Use the feasibility table: about $10^8$ simple operations per second in C++ (fewer in Python). If $n = 10^5$, a $\Theta(n^2)$ solution needs about $10^{10}$ operations: too slow.
- A common question is "what if the data does not fit in memory?" The expected answer involves external sorting, streaming (one pass, small memory), or partitioning (MapReduce-style).
- Know Euclid's algorithm by heart; it appears in fraction simplification, modular inverses, and number-theory problems.

## Using AI Assistants Critically

- Assistants often produce correct but asymptotically naive first solutions (e.g. nested loops for pair problems). Ask explicitly for the complexity and whether a better order of growth exists.
- When an assistant claims "this is the most efficient approach", ask for the lower-bound argument; without one, the claim is unsupported.
- Historical facts and attributions generated by LLMs (dates, inventors, "first algorithm") are frequently wrong; check them in a textbook or primary source.
- When an assistant recommends "just parallelise it" or "use a GPU", compare the constant-factor gain with what a better algorithm would give at your $n$.
- Verify feasibility claims numerically, as `largest_n` does, instead of trusting a stated "this will run in under a second".

## Practice

### Beginner

1. **Feasibility.** At $10^8$ operations per second, what is the largest $n$ an $n^2$ algorithm can handle in 2 seconds? Difficulty: easy.
2. **Hardware vs algorithm.** If a machine becomes 100 times faster, by what factor does the feasible $n$ grow for $n$, $n^2$, $n^3$ algorithms, and by how much does it grow for $2^n$? Difficulty: easy.
3. **Euclid trace.** Trace Euclid's algorithm on $(252, 105)$ and count the division steps. Difficulty: easy.

### Intermediate

1. **Crossover.** Algorithm A costs $8n^2$, algorithm B costs $64 n \log_2 n$. Find the smallest $n \ge 2$ for which B is faster. Difficulty: medium.
2. **Index or scan.** A table has $10^8$ rows. Building a B+ tree index costs about $n \log_2 n$ operations; each indexed query costs $\log_2 n$; each unindexed query scans all rows. After how many queries does the index pay off? Difficulty: medium.
3. **Application mapping.** For three applications from the table (your choice), name the core algorithm and its complexity. Difficulty: medium.

### Advanced

1. **Euclid's worst case.** Prove that if Euclid's algorithm takes $k$ division steps on $(a, b)$ with $a > b > 0$, then $a \ge F_{k+2}$ and $b \ge F_{k+1}$ (Fibonacci numbers with $F_1 = F_2 = 1$), and conclude the step count is $O(\log b)$. Difficulty: hard.
2. **Amdahl vs algorithm.** A job is 90% parallelisable and runs in $\Theta(n^2)$. Compare the gain from 64 processors with the gain from an $\Theta(n \log n)$ sequential algorithm at $n = 10^6$. Difficulty: hard.
3. **Feasibility under growth.** Data doubles every year; hardware throughput doubles every two years. For a $\Theta(n^2)$ algorithm, how does runtime evolve over 10 years? Difficulty: medium-hard.

### Interview / Competitive Programming

1. **Constraint check.** $n \le 2 \times 10^5$, time limit 1 s. Is an $O(n \sqrt{n})$ solution acceptable in C++? In Python? Difficulty: easy-medium.
2. **Big data dedup.** Remove duplicate lines from a 1 TB file on a machine with 16 GB of RAM. Outline an approach and its I/O cost. Difficulty: medium.
3. **GCD of an array.** Compute the GCD of $n \le 10^5$ integers up to $10^{18}$; state the complexity. Difficulty: easy.

## Self-Check Questions

??? question "Q1. If computers become 1000 times faster, how much larger an input can a $2^n$ algorithm handle in the same time?"

    About $\log_2 1000 \approx 10$ more items: $2^{n'} = 1000 \cdot 2^n$ gives $n' = n + \log_2 1000$. Exponential algorithms barely benefit from hardware.

??? question "Q2. In the $n = 10^9$ example, machine B is 1000 times slower and still wins. Would B win at $n = 1000$?"

    No. $T_A = 2 \cdot 10^6 / 10^{10} = 0.2$ ms; $T_B = 50 \cdot 1000 \cdot 9.97 / 10^7 \approx 50$ ms. A wins comfortably. The better order of growth wins only beyond the crossover.

??? question "Q3. Why is Euclid's algorithm still relevant 2,300 years later?"

    It computes GCDs in $O(\log \min(a,b))$ division steps, and its extended form computes modular inverses, which are needed in RSA key generation, rational arithmetic, and many number-theoretic algorithms.

??? question "Q4. Give two reasons algorithms count as a 'technology' alongside hardware."

    Their choice determines what is feasible (an engineering decision with measurable cost), and their improvements compound with hardware improvements. They are also designed, tested, and maintained like any other technology.

??? question "Q5. A team proposes moving a slow nightly job to a machine 4 times faster. The job is $\Theta(n^2)$ and data grows 3× per year. Evaluate."

    Next year the work grows by $3^2 = 9$×, so a 4× faster machine leaves the job about 2.25× slower than today. The fix is temporary; reducing the order of growth (sorting plus merging, hashing, indexing) is the durable solution.

??? question "Q6. Name an application where an approximate algorithm is preferred over an exact one, and why."

    Vector search for retrieval: exact nearest neighbour among millions of high-dimensional embeddings is too slow per query, so approximate methods such as HNSW trade a small loss in recall for large speedups.

## Complexity Summary

| Algorithm / task mentioned | Complexity |
|---|---|
| Euclid's GCD | $O(\log \min(a,b))$ division steps |
| Brute-force GCD | $O(\min(a,b))$ trial divisions |
| Comparison sorting (good algorithms) | $\Theta(n \log n)$ |
| Insertion sort (worst case) | $\Theta(n^2)$ |
| Dijkstra with a binary heap | $O((V + E)\log V)$ |
| FFT | $\Theta(n \log n)$ |
| Modular exponentiation by squaring | $O(\log e)$ multiplications |

## Key Takeaways

- Algorithms are much older than computers, from Babylonian procedures and Euclid's GCD to today's ML training pipelines.
- Faster hardware multiplies throughput by a constant; a better algorithm changes the growth function, and its advantage grows without bound with $n$.
- At $n = 10^9$, an $n \log n$ algorithm on hardware 1000 times slower beats an $n^2$ algorithm by over a thousandfold.
- Hardware speedups barely help exponential algorithms: 1000× faster adds about 10 to the feasible $n$.
- Search, routing, compression, cryptography, databases, and ML are built on algorithms covered in this course.
- Real systems combine asymptotically good algorithms with constant-factor engineering, preprocessing, and approximation.
