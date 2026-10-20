# Model of Computation (Word-RAM)

!!! abstract "At a glance"

    - **Problem:** "count the basic operations" ([2.1](topic1.md)) only makes sense once we agree *which* operations are basic and what each one costs.
    - **Key idea:** the Word-RAM is an idealised computer with random-access memory of $w$-bit words, where arithmetic, comparisons, bitwise operations and memory accesses on single words each cost $O(1)$, and $w \ge \log_2 n$.
    - **Limits:** operations on numbers wider than a word (big integers) are **not** unit cost; the model also ignores caches, so two $\Theta(n)$ algorithms can differ in speed by an order of magnitude.
    - **Used for:** essentially every complexity bound in this course and in standard textbooks; external-memory and parallel models refine it when I/O or parallelism dominates.

## Motivation and Problem Context

Consider two claims:

1. "Summing an array of $n$ numbers takes $\Theta(n)$ time."
2. "Computing $n!$ with a loop of $n$ multiplications takes $\Theta(n)$ time."

The first is true on any real machine. The second is false: $n!$ has about $n \log_2 n$ bits, so the later multiplications operate on numbers thousands of bits long, and each one costs far more than one machine instruction. What distinguishes the two claims is the **model of computation**: an explicit agreement about what one "step" is. Without it, complexity bounds are ambiguous, and with the wrong one you can "prove" absurd results (for instance, that very large products cost the same as $2 + 2$).

## Problem Formulation

A model of computation specifies:

- **Memory:** what is stored and how it is addressed.
- **Operations:** which primitive instructions exist.
- **Cost:** what each instruction costs (unit, proportional to operand length, or proportional to data moved).
- **Size of a word:** how large a number one memory cell may hold.

We want a model that is **simple enough** to analyse with pencil and paper and **realistic enough** that its predictions match real hardware for the algorithms we care about.

## Intuition

A real CPU executes one 64-bit addition in about the same time whether the numbers are 2 and 2 or 2,000,000,000 and 2,000,000,000, because the hardware processes all 64 bits in parallel. It does **not** add two 10,000-digit numbers in one instruction. The Word-RAM captures exactly this: numbers that fit in a machine word are cheap and their operations are constant time; anything bigger must be split into words and paid for word by word. Memory is a huge numbered row of lockers: knowing a locker number, you open it directly in one step (random access), rather than walking past every locker before it.

## Definitions

**RAM (Random Access Machine).** A processor with a finite set of registers plus an unbounded array of memory cells $M[0], M[1], M[2], \dots$. Any cell can be read or written in one step given its address. Instructions run one at a time (sequential model).

**Word.** The unit of data a memory cell holds: a $w$-bit integer, i.e. a value in $\{0, \dots, 2^w - 1\}$ (or a signed equivalent).

**Word-RAM.** A RAM whose cells hold $w$-bit words and whose unit-cost instructions operate on single words.

**Word-size assumption ($w \ge \log_2 n$).** The word must be wide enough to hold an index into the input (and therefore a pointer to any input cell). This is sometimes called the *trans-dichotomous* assumption: the machine's word size is tied to the problem size. For 64-bit machines, $w = 64$ covers any $n$ up to $2^{64}$.

**Unit-cost (uniform) model vs bit-cost (logarithmic) model.** In the unit-cost model every word operation costs 1. In the bit-cost model an operation on numbers with $b$ bits costs a function of $b$ (for example $\Theta(b)$ for addition). The Word-RAM is unit-cost **per word**, so it behaves like the bit model for numbers spanning many words.

### Unit-cost operations

| Category | Operations | Cost on Word-RAM |
|---|---|---|
| Arithmetic | $+, -, \times$, integer division, mod on $w$-bit words | $O(1)$ |
| Comparison | $=, \ne, <, \le, >, \ge$ on words | $O(1)$ |
| Bitwise | AND, OR, XOR, NOT, shifts | $O(1)$ |
| Memory | read/write $M[i]$ for an address $i$ held in a word | $O(1)$ |
| Control | jump, conditional branch, call, return | $O(1)$ |
| Allocation | reserve one fixed-size block (e.g. a list node) | $O(1)$ |

### Not unit cost (common traps)

| Operation | True cost | Why |
|---|---|---|
| Arithmetic on $b$-bit integers, $b \gg w$ | addition $\Theta(b/w)$; schoolbook multiplication $\Theta((b/w)^2)$ | number occupies $\lceil b/w \rceil$ words |
| Comparing / hashing / copying a string of length $L$ | $\Theta(L)$ worst case | $L$ characters ≈ $L/w$ words to touch |
| Allocating **and initialising** an array of $n$ cells | $\Theta(n)$ | each cell must be written |
| Copying or slicing a list of $n$ items | $\Theta(n)$ | elements are copied one by one |
| Python `x in list`, `list.insert(0, x)`, `list.pop(0)` | $\Theta(n)$ | scan or shift of the underlying array |
| Floating point `x ** 0.5`, `math.log` | $O(1)$ for fixed-precision floats | fixed-width hardware/library routine; not for arbitrary precision |

!!! warning "Important"

    The Word-RAM charges $O(1)$ only for operations on **one word**. Whenever numbers can grow beyond $\Theta(\log n)$ bits (factorials, Fibonacci numbers, products of many values, exact rationals), analyse in terms of the number of words or bits. Python hides this because its integers grow automatically, which makes the trap easy to fall into.

## Key Results

### Why $w \ge \log_2 n$ and not more

- **Lower requirement:** if $w < \log_2 n$, a single word cannot hold an index into the input, so even "read element $i$" would need several words; the model would no longer reflect machines that can address their input directly.
- **Upper caution:** if words were *unbounded* with unit-cost multiplication, repeated squaring would produce $2^{2^k}$ in $k$ steps, a number with $2^k$ bits. A machine that manipulates exponentially many bits per step is unrealistically powerful, so analyses that rely on it are meaningless. The standard assumption is therefore $w = \Theta(\log n)$ (word large enough for indices, but not arbitrarily large).

### Memory model

Memory is a flat array of words. An array `A` stored from base address $b$ places `A[i]` at address $b + i$ (or $b + i \cdot s$ for elements of $s$ words), so computing the address and loading the value are $O(1)$. A linked list stores nodes at arbitrary addresses; reaching the $i$-th node requires following $i$ pointers, $\Theta(i)$. The model therefore explains why arrays support $O(1)$ indexing and linked lists do not.

### Comparison with other models

| Model | Memory and cost | Main use | Relationship to Word-RAM |
|---|---|---|---|
| Turing machine | sequential tape; head moves one cell per step | computability, complexity classes (P, NP) | polynomially equivalent: each simulates the other with polynomial overhead, but polynomial factors matter for algorithm analysis |
| Pointer machine | memory reachable only by following pointers; no address arithmetic | pointer-based data structures (lists, trees, union-find lower bounds) | weaker: cannot compute `A[i]`'s address directly |
| Real RAM | registers hold exact real numbers; arithmetic is unit cost | computational geometry | stronger than real hardware; used with care |
| PRAM (Parallel RAM) | $p$ processors share memory, synchronous steps | theory of parallel algorithms (work and depth) | Word-RAM is the $p = 1$ case |
| External memory (I/O model) | fast memory of size $M$, disk in blocks of $B$; cost = number of block transfers | databases, large-scale sorting, B-trees | adds the memory hierarchy the Word-RAM ignores |
| Cache-oblivious | like the I/O model but the algorithm does not know $M$ or $B$ | portable cache-efficient algorithms | analysis in I/O model, algorithm written as on a RAM |

!!! note "Why the Word-RAM is the default"

    It is close to how real processors execute single instructions, simple enough to analyse, and its predictions are accurate for a very wide class of algorithms. Its main blind spots are big-number arithmetic (handled by counting words or bits) and the memory hierarchy (handled by I/O models or measurement).

## Method: Analysing Under the Word-RAM

1. **Identify the data that grows.** Which values can exceed $\Theta(\log n)$ bits? Indices, counters and pointers cannot; sums of $n$ values each of $O(\log n)$ bits fit in $O(\log n)$ bits too. Products of many values, factorials, and exponentials can.
2. **For word-sized data,** count each primitive operation as 1 (the method of [2.1](topic1.md)).
3. **For multi-word data,** replace each operation by its cost in words: addition of $b$-bit numbers costs $\Theta(b/w)$, schoolbook multiplication $\Theta((b/w)^2)$ (faster algorithms in [4.3 Integer Multiplication](../unit4/topic3.md)).
4. **Check library calls** for hidden linear work (copying, slicing, string building).
5. **If performance matters at scale,** also ask how the algorithm accesses memory (sequential vs scattered); the Word-RAM will not tell you.

## Worked Examples

### Example 1: array sum (fits the model)

Summing $n$ values, each fitting in a word: $n$ loads, $n$ additions, $n$ loop tests. If each value has at most $c \log n$ bits, the sum has at most $c\log n + \log_2 n$ bits, still $O(1)$ words. Total $\Theta(n)$.

### Example 2: factorial (does not fit the model)

The loop does $n - 1$ multiplications, but the running product $k!$ has $\log_2 k! = \Theta(k \log k)$ bits ([Stirling, 2.6](topic6.md)). Multiplying a $\Theta(k \log k)$-bit number by a one-word number $k$ costs $\Theta(k \log k / w)$ word operations, so the total is

$$
\sum_{k=2}^{n} \Theta\!\left(\frac{k \log k}{w}\right) = \Theta\!\left(\frac{n^2 \log n}{w}\right),
$$

which is $\Theta(n^2)$ word operations when $w = \Theta(\log n)$, far from the naive "$\Theta(n)$".

| $n$ | bits in $n!$ | $\log_2 n!$ (Stirling) | sum of bit lengths of all intermediate products |
|---|---|---|---|
| 10 | 22 | 21.8 | 97 |
| 100 | 525 | 524.8 | 23,106 |
| 1000 | 8,530 | 8,529.4 | 3,911,239 |

From $n = 100$ to $n = 1000$ the last column grows about 170×, close to the $10^2 \cdot \frac{\log 1000}{\log 100} = 150$ predicted by $n^2 \log n$ and nothing like the 10× that "$\Theta(n)$" would predict.

### Example 3: iterative Fibonacci

Computing $F(n)$ by $n$ additions is $\Theta(n)$ **additions**, but $F(n) \approx \varphi^n/\sqrt{5}$ has about $0.694n$ bits ($\log_2 \varphi \approx 0.694$). Each addition of $\Theta(k)$-bit numbers costs $\Theta(k/w)$ word operations, so the bit-aware cost is $\Theta(n^2 / w)$. Both statements are correct, each in its own cost model; an answer must say which.

### Example 4: pseudo-polynomial time

A dynamic program for Subset Sum with target $W$ runs in $\Theta(nW)$. That looks polynomial, but the input encodes $W$ in only $\log_2 W$ bits. Increase $W$ from $10^6$ to $10^{12}$: the input grows by about 20 bits, and the running time grows by a factor of $10^6$. An algorithm polynomial in the numeric **value** of the input but not in its **length** is called **pseudo-polynomial**.

!!! warning "Important"

    "Polynomial time" means polynomial in the **length of the input in bits**. $\Theta(nW)$ for Subset Sum, and trial division in $\Theta(\sqrt{N})$ for primality, are exponential in input length. This is a standard exam question.

### Example 5: same complexity, different speed (memory hierarchy)

Summing an $n \times n$ matrix stored in row-major order (as in C, and as NumPy arrays default to):

```c
/* Row-by-row: consecutive addresses, cache-friendly */
for (int i = 0; i < n; i++)
    for (int j = 0; j < n; j++)
        sum += a[i][j];

/* Column-by-column: stride of n elements, cache-unfriendly */
for (int j = 0; j < n; j++)
    for (int i = 0; i < n; i++)
        sum += a[i][j];
```

Both perform exactly $n^2$ additions, so the Word-RAM says both are $\Theta(n^2)$ with the same constant. On real hardware, once the matrix is larger than the caches, the column-wise version is typically several times slower: each access loads a whole cache line (commonly 64 bytes) but uses only one value from it before moving on.

## Modern Hardware Reality: The Memory Hierarchy

The Word-RAM assumes every memory access costs the same. Real machines have a hierarchy whose levels differ by orders of magnitude (indicative figures; exact values vary by hardware):

| Level | Typical size | Approximate access latency |
|---|---|---|
| Registers | tens of words | under 1 ns |
| L1 cache | tens of KB per core | about 1 ns |
| L2 / L3 cache | hundreds of KB to tens of MB | several to tens of ns |
| Main memory (DRAM) | GB | on the order of 100 ns |
| SSD | hundreds of GB to TB | tens to hundreds of µs |
| Hard disk | TB | milliseconds |

Consequences for algorithm design:

- **Locality matters.** Algorithms that scan memory sequentially (arrays, merge passes) exploit spatial locality and hardware prefetching; algorithms that chase pointers randomly (linked lists, naive trees) stall on cache misses.
- **Arrays usually beat linked lists in practice** even where both are asymptotically equal, because of locality.
- **B-trees exist because of the hierarchy.** A binary search tree and a B-tree both have $\Theta(\log n)$ height up to constants, but a B-tree with fan-out $B$ needs only $\Theta(\log_B n)$ block reads, which is why databases and file systems use B-trees and B+ trees.
- **External-memory analysis** counts block transfers: scanning $N$ items costs $\Theta(N/B)$ I/Os, and sorting costs $\Theta\!\left(\frac{N}{B}\log_{M/B}\frac{N}{B}\right)$ I/Os.

## Python Implementation

Python integers are arbitrary-precision, so the cost of arithmetic grows with the number of digits. The functions below make that visible.

```python
import time


def factorial_with_sizes(n):
    """Compute n! by n-1 multiplications; return (n!, bit length of each intermediate product)."""
    result = 1
    sizes = []
    for k in range(2, n + 1):
        result *= k
        sizes.append(result.bit_length())
    return result, sizes


def fib_iterative(n):
    """Return F(n) using n additions (F(0) = 0, F(1) = 1)."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def time_multiplication(bits, repeats=5):
    """Best time to multiply two numbers of the given bit length."""
    x = (1 << bits) - 12345
    y = (1 << bits) - 67891
    best = float("inf")
    for _ in range(repeats):
        t0 = time.perf_counter()
        x * y
        best = min(best, time.perf_counter() - t0)
    return best
```

Walkthrough:

- `result.bit_length()` exposes how many bits the running product occupies; summing these values reproduces the table in Example 2.
- `fib_iterative(10_000).bit_length()` returns 6942, matching $10{,}000 \cdot \log_2 \varphi \approx 6942$.
- `time_multiplication` shows that multiplying two $10^6$-bit numbers takes far longer than multiplying two $10^5$-bit numbers. On one test machine the ratio was about 40× for 10× more bits, consistent with Karatsuba's $\Theta(b^{1.585})$ (CPython switches from schoolbook to Karatsuba multiplication for large integers), and certainly not $O(1)$.

## Edge Cases and Pitfalls

| Case / pitfall | What goes wrong | Fix |
|---|---|---|
| Treating big-integer arithmetic as $O(1)$ | factorial, Fibonacci, exact combinatorics look linear but are quadratic or worse | count words/bits once values exceed $O(\log n)$ bits |
| Treating string comparison or hashing as $O(1)$ | a dictionary of $n$ strings of length $L$ costs $\Theta(nL)$ to build, not $\Theta(n)$ | include $L$ in the bound |
| Fixed-width overflow in C/C++/Java | `int` products or sums wrap around silently | use 64-bit types, or reduce modulo $m$, or check bounds |
| Assuming allocation of an $n$-array is $O(1)$ | zero-initialising costs $\Theta(n)$ | count it, or reuse buffers |
| Ignoring cache behaviour | two $\Theta(n^2)$ loops differ by several times in speed | access memory sequentially; measure |
| Calling an algorithm polynomial because it is polynomial in a numeric value | pseudo-polynomial algorithms blow up when values are large | express cost in input bits |

## Common Misconceptions

- **"$O(1)$ means fast."** It means *bounded by a constant independent of $n$*. A cache miss to DRAM is $O(1)$ and can cost on the order of a hundred additions.
- **"Python integers are words."** They are variable-length objects. Small ones behave like words; large ones cost time proportional to their length (or more, for multiplication).
- **"The Word-RAM is unrealistic, so its results are useless."** It is the right abstraction for *growth*; its blind spots (caches, big numbers, parallelism) are known and handled by refined models or measurement.
- **"A Turing machine analysis gives the same bounds."** TMs and RAMs agree on what is polynomial-time, but exact bounds can differ by polynomial factors (a TM cannot index memory directly), so algorithm analysis uses the RAM.
- **"Multiplication is always unit cost."** On words, yes in the standard Word-RAM. On numbers wider than a word it is not, and fast multiplication algorithms ([4.3](../unit4/topic3.md)) exist precisely because it is not.

## Alternatives and Trade-offs

| Model | Use when | Avoid when |
|---|---|---|
| Word-RAM, unit cost | standard algorithm analysis; values fit in $O(\log n)$ bits | numbers grow large; I/O dominates |
| Bit-cost model | arithmetic algorithms, cryptography, number theory | ordinary array/graph algorithms (needless detail) |
| External-memory (I/O) model | data larger than RAM; databases; big-data sorting | in-memory workloads where computation dominates |
| PRAM / work–depth | designing parallel algorithms, GPU-style computation | sequential code |
| Measurement | tuning constants, cache effects, real systems | proving guarantees |

## In Practice

- **Fixed-width integers in systems languages:** C, C++, Java, Rust and Go use 32- or 64-bit integers by default; operations are genuinely unit cost, and overflow is the corresponding risk.
- **Arbitrary precision where needed:** Python `int`, Java `BigInteger`, and the GMP library implement multi-word arithmetic with algorithms whose costs depend on operand length (schoolbook, Karatsuba, and, in GMP, asymptotically faster methods for very large operands).
- **Cryptography is analysed in the bit model:** RSA works with numbers of 2048 bits or more, so the cost of modular exponentiation ([4.6](../unit4/topic6.md)) is stated in terms of the bit length.
- **Databases and file systems** design data structures for block transfers (B+ trees, sorted runs merged in passes), which is the external-memory model in action.
- **ML workloads** are often limited by memory bandwidth rather than arithmetic; FlashAttention, for example, reorganises the attention computation to reduce reads and writes to GPU high-bandwidth memory without changing the arithmetic it performs. That is a memory-hierarchy optimisation invisible in the Word-RAM.

## Interview and Competitive Programming

- In C++/Java, values up to about $2 \times 10^9$ fit in 32-bit signed `int`; up to about $9.2 \times 10^{18}$ in 64-bit `long long`/`long`. "Answer modulo $10^9+7$" exists to keep values word-sized.
- Products of two values up to $10^9$ need 64 bits; products of two 64-bit values need 128 bits or modular multiplication tricks.
- In Python there is no overflow, but large numbers silently slow down. If an intermediate value grows without bound, reduce it modulo $m$ as you go.
- Recognition cue: "count the ways", "number can be huge" → reduce modulo $m$ at every step to keep each operation $O(1)$.
- Recognition cue: a DP indexed by a numeric value (capacity, sum, target) is pseudo-polynomial; check the value bound in the constraints, not just $n$.

## Using AI Assistants Critically

- LLMs routinely state "$O(n)$" for loops that build factorials, Fibonacci numbers or large products in Python; ask how many bits the values reach.
- Generated C/Java code often overflows in `a * b` or in `(lo + hi)` for large indices; check every product and sum against the type's range (or use `lo + (hi - lo) / 2`).
- Assistants may claim dictionary operations are $O(1)$ on long string keys; remind them hashing a key of length $L$ costs $\Theta(L)$.
- When an assistant labels a value-indexed DP as "polynomial", ask for the bound in terms of input bits.
- Claims that "algorithm X is faster because of caches" should be verified by a benchmark at realistic sizes; the Word-RAM cannot confirm or refute them.
- Verify any arithmetic-heavy routine by timing it at sizes $b, 2b, 4b$ bits, exactly as `time_multiplication` does.

## Practice

### Beginner

1. **Unit cost or not?** For each operation, state its Word-RAM cost: `a[i] = a[i-1] + 1`; `s == t` for strings of length $L$; `x * y` for 64-bit `x, y`; `x * y` for 10,000-bit `x, y`. Difficulty: easy.
2. **Word size.** What is the minimum word size needed to index an array of $10^9$ elements? Difficulty: easy.
3. **Array vs list.** Explain, using the memory model, why accessing the $i$-th element is $O(1)$ for an array but $\Theta(i)$ for a singly linked list. Difficulty: easy.

### Intermediate

1. **Bit cost of $2^n$.** Analyse computing $2^n$ by $n$ repeated doublings in the bit-cost model. Output: order of growth. Difficulty: medium.
2. **Sum of products.** Given $n$ integers each below $2^{32}$, analyse computing their sum and their product on a 64-bit Word-RAM. Difficulty: medium.
3. **Pseudo-polynomial.** An algorithm runs in $\Theta(n \cdot K)$, where $K$ is a number in the input. Is it polynomial? Explain in terms of input bits. Difficulty: medium.

### Advanced

1. **Unbounded words.** Show that with unbounded word size and unit-cost multiplication, $2^{2^k}$ can be computed in $O(k)$ steps; explain why this makes the model unrealistic. Difficulty: hard.
2. **External-memory scan.** In the I/O model with block size $B$, how many I/Os does a linear scan of $N$ items take? How many does following a linked list of $N$ nodes scattered in memory take in the worst case? Difficulty: medium-hard.
3. **Matrix transpose.** Explain why a naive transpose of an $n \times n$ matrix is cache-unfriendly and outline a blocked (tiled) approach. Difficulty: hard.

### Interview / Competitive Programming

1. **Overflow audit.** Given constraints $a_i \le 10^9$, $n \le 10^5$, decide which variables need 64-bit integers when computing $\sum a_i$ and $\max a_i \cdot a_j$. Difficulty: easy.
2. **Large answer.** Compute $n! \bmod (10^9 + 7)$ for $n \le 10^6$. State why reducing modulo at each step keeps the algorithm $\Theta(n)$. Difficulty: easy-medium.
3. **String-key hashing.** You insert $n$ strings of total length $S$ into a hash map. What is the expected total time? Difficulty: medium.

## Self-Check Questions

??? question "Q1. Why must the word size satisfy $w \ge \log_2 n$?"

    An index into an input of $n$ cells needs $\lceil \log_2 n \rceil$ bits. If a word could not hold it, the machine could not address its own input with single-word operations, and "read $A[i]$" would no longer be one step.

??? question "Q2. Iterative Fibonacci uses $n$ additions. Is it $\Theta(n)$?"

    In the unit-cost model counting additions, yes. In a bit-aware or Word-RAM analysis it is $\Theta(n^2/w)$, because $F(k)$ has $\Theta(k)$ bits and adding $\Theta(k)$-bit numbers costs $\Theta(k/w)$ word operations. A complete answer names the model.

??? question "Q3. Is Subset Sum's $\Theta(nW)$ dynamic program polynomial time?"

    No. $W$ is encoded in $\Theta(\log W)$ bits, so $\Theta(nW)$ is exponential in the input length. It is pseudo-polynomial: efficient only when $W$ is small.

??? question "Q4. Two loops both perform exactly $n^2$ additions, yet one is five times slower. What explains this, and does it contradict the Word-RAM?"

    Memory access pattern: one accesses consecutive addresses (cache-friendly), the other strides across rows and misses the cache. It does not contradict the model; it falls outside what the model measures, since the Word-RAM assumes uniform memory cost.

??? question "Q5. Why do databases use B-trees instead of binary search trees?"

    In the external-memory model, cost is block transfers. A B-tree node fills a block and has fan-out $B$, giving $\Theta(\log_B n)$ I/Os per search, versus $\Theta(\log_2 n)$ for a binary tree whose nodes are scattered across blocks.

??? question "Q6. Is a Turing machine a better model for analysing sorting algorithms?"

    No. Turing machines lack random access, so simulating array indexing adds polynomial overhead; the resulting bounds do not reflect real computers. TMs are the right tool for computability and complexity classes; the Word-RAM is the right tool for concrete algorithm analysis.

??? question "Q7. A colleague computes $\binom{n}{k}$ exactly in Python for $n = 10^5$ and says it is $O(k)$. Comment."

    It is $O(k)$ multiplications and divisions, but the intermediate values have up to $\Theta(n)$ bits, so each operation costs time proportional to the operand length. The real cost is superlinear; state the bound in word or bit operations.

## Complexity Summary

| Operation | Word-RAM cost |
|---|---|
| Arithmetic, comparison, bitwise op on one word | $O(1)$ |
| Read/write $M[i]$ | $O(1)$ |
| Add two $b$-bit integers | $\Theta(b/w)$ |
| Multiply two $b$-bit integers (schoolbook) | $\Theta((b/w)^2)$ |
| Compare/hash/copy a length-$L$ string | $\Theta(L)$ (in characters; $\Theta(L/w)$ words if packed) |
| Linear scan of $N$ items, I/O model | $\Theta(N/B)$ I/Os |
| Search in a B-tree, I/O model | $\Theta(\log_B N)$ I/Os |

## Key Takeaways

- A complexity bound is meaningful only relative to a model of computation that defines unit-cost operations.
- The Word-RAM charges $O(1)$ for arithmetic, comparison, bitwise operations and memory access on single $w$-bit words, with $w \ge \log_2 n$.
- Numbers wider than a word cost time proportional to their length; factorials, Fibonacci numbers and products of many values break the "$O(1)$ arithmetic" assumption.
- "Polynomial time" means polynomial in the bit length of the input; algorithms polynomial in numeric values are pseudo-polynomial.
- The Word-RAM ignores the memory hierarchy; locality can change real performance by large factors, and external-memory models (and B-trees) address this.
- Turing machines, pointer machines, PRAM and I/O models each serve a different purpose; the Word-RAM is the standard for algorithm analysis.
