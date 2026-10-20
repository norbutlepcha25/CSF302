# Iteration Method

!!! abstract "At a glance"

    - **Problem:** turn a recurrence such as $T(n) = T(n-1) + n$ into a closed form or a $\Theta$ bound.
    - **Key idea (also called the expansion method):** substitute the recurrence into itself repeatedly ("unroll" it) until a pattern in the $k$-th expansion is visible, choose $k$ so the argument reaches the base case, then evaluate the resulting sum.
    - **Variant:** *telescoping* rewrites the recurrence so that consecutive terms cancel when added.
    - **Best for:** subtract-and-conquer recurrences ($T(n-1)$, $T(n-c)$) that the master method cannot handle, and for exact closed forms.

## Motivation and Problem Context

The [master method](topic5.md) answers $T(n) = aT(n/b) + f(n)$ in seconds, but it says nothing about $T(n) = 2T(n-1) + 1$ (Towers of Hanoi), $T(n) = T(n-1) + n$ (worst-case quicksort, recursive selection sort), or the exact constant in $T(n) = 2T(n/2) + n$. These appear constantly: any algorithm that peels off one element at a time produces a subtract-and-conquer recurrence. The iteration method handles all of them with nothing more than algebra and a table of standard sums, and it is the most direct way to see *where* the cost of a recursion comes from.

## Problem Formulation

- **Input:** a recurrence with a single recursive term (possibly multiplied by a constant), e.g. $T(n) = a\,T(g(n)) + f(n)$, where $g(n) = n - c$ or $g(n) = n/b$, plus a base case $T(n_0)$.
- **Output:** an exact closed form for $T(n)$ (on a convenient subset of $n$, such as powers of $b$), and from it a $\Theta$ bound.
- **Assumptions:** for dividing recurrences, $n$ is an exact power of $b$ so that $n/b^k$ is an integer; the bound extends to all $n$ by monotonicity ([3.1](topic1.md#floors-ceilings-and-why-they-can-usually-be-ignored)).

## Intuition

Unrolling a recurrence is the same as walking down one root-to-leaf path of its recursion tree while keeping a running total of the work encountered. Each expansion step peels off one level of "local work" and pushes the unknown $T(\cdot)$ one level deeper. When the unknown finally reaches the base case, what is left is an ordinary sum, which we know how to evaluate.

!!! tip "Mental model"
    $T(n) = (\text{work at level } 0) + (\text{work at level } 1) + \cdots + (\text{work at level } k-1) + (\text{multiplier}) \cdot T(\text{base}).$
    The iteration method is bookkeeping that produces exactly this sum.

## Definitions and Key Results

The iteration method reduces every problem to a sum. These are the sums you need.

| Sum | Closed form | Asymptotic |
|---|---|---|
| Arithmetic: $\sum_{i=1}^{n} i$ | $\dfrac{n(n+1)}{2}$ | $\Theta(n^2)$ |
| Squares: $\sum_{i=1}^{n} i^2$ | $\dfrac{n(n+1)(2n+1)}{6}$ | $\Theta(n^3)$ |
| Powers: $\sum_{i=1}^{n} i^d$, constant $d \ge 0$ | | $\Theta(n^{d+1})$ |
| Geometric: $\sum_{i=0}^{k} r^i$, $r \ne 1$ | $\dfrac{r^{k+1} - 1}{r - 1}$ | $\Theta(1)$ if $r<1$; $\Theta(r^k)$ if $r>1$ |
| Harmonic: $H_n = \sum_{i=1}^{n} \dfrac{1}{i}$ | $\ln n + \gamma + o(1)$ | $\Theta(\log n)$ |
| Log sum: $\sum_{i=1}^{n} \log i = \log n!$ | | $\Theta(n \log n)$ |

Two identities used in almost every dividing recurrence:

$$
a^{\log_b n} = n^{\log_b a} \qquad\text{and}\qquad \log_b n = \frac{\log_2 n}{\log_2 b}.
$$

The first says that the number of leaves of a recursion tree with branching factor $a$ and depth $\log_b n$ is $n^{\log_b a}$. Proof: take $\log_b$ of both sides; both equal $\log_b a \cdot \log_b n$.

!!! note "Why $\log n! = \Theta(n \log n)$"
    Upper: $\sum_{i=1}^{n} \log i \le n \log n$. Lower: the largest $n/2$ terms are each at least $\log(n/2)$, so the sum is at least $\frac{n}{2}\log\frac{n}{2} = \Omega(n \log n)$.

## Method

1. **Expand** the recurrence 2 to 4 times, substituting the recurrence for the $T(\cdot)$ term each time. *Keep the terms unsimplified* (write $n + (n-1) + (n-2)$, not $3n - 3$) so that the pattern is visible.
2. **Generalise** to the form after $k$ expansions: $T(n) = (\text{multiplier}_k)\,T(\text{arg}_k) + \sum_{i=0}^{k-1}(\text{term}_i)$.
3. **Stop at the base case:** solve $\text{arg}_k = n_0$ for $k$ (e.g. $n - k = 1 \Rightarrow k = n-1$; $n/2^k = 1 \Rightarrow k = \log_2 n$).
4. **Substitute** $k$ and the base value; evaluate the sum with the table above.
5. **State the bound** ($\Theta$), and if rigour is required, verify the closed form by [induction](topic4.md).

!!! warning "Important"
    Step 2 is a pattern you *observed*, not one you *proved*. In an exam, the iteration method is accepted as a derivation, but a fully rigorous answer confirms the closed form by induction (substitution method). Do not simplify early: $T(n) = T(n-3) + 3$ hides the pattern that $T(n) = T(n-3) + (n-2) + (n-1) + n$ would reveal.

## Worked Examples

### Example 1: $T(n) = T(n-1) + 1$, $T(1) = 1$

$$
\begin{aligned}
T(n) &= T(n-1) + 1 \\
     &= [T(n-2) + 1] + 1 = T(n-2) + 2 \\
     &= [T(n-3) + 1] + 2 = T(n-3) + 3 \\
     &\;\;\vdots \\
     &= T(n-k) + k .
\end{aligned}
$$

Base case: $n - k = 1 \Rightarrow k = n - 1$. So $T(n) = T(1) + (n-1) = n$.

$$\boxed{T(n) = n = \Theta(n)}$$

Each level removes one element and costs a constant; there are $n$ levels.

### Example 2: $T(n) = T(n-1) + n$, $T(1) = 1$

$$
\begin{aligned}
T(n) &= T(n-1) + n \\
     &= T(n-2) + (n-1) + n \\
     &= T(n-3) + (n-2) + (n-1) + n \\
     &= T(n-k) + \sum_{i=0}^{k-1} (n - i) .
\end{aligned}
$$

With $k = n-1$: $T(n) = T(1) + \sum_{j=2}^{n} j = 1 + 2 + \cdots + n = \dfrac{n(n+1)}{2}$.

$$\boxed{T(n) = \tfrac{n(n+1)}{2} = \Theta(n^2)}$$

This is the recurrence of recursive selection sort and of quicksort when every pivot is the minimum or maximum.

### Example 3: $T(n) = T(n/2) + 1$, $T(1) = 1$, $n = 2^m$

$$
\begin{aligned}
T(n) &= T(n/2) + 1 \\
     &= [T(n/4) + 1] + 1 = T(n/4) + 2 \\
     &= [T(n/8) + 1] + 2 = T(n/8) + 3 \\
     &= T(n/2^k) + k .
\end{aligned}
$$

Base case: $n/2^k = 1 \Rightarrow k = \log_2 n$. So $T(n) = 1 + \log_2 n$.

$$\boxed{T(n) = \log_2 n + 1 = \Theta(\log n)}$$

This is binary search: $\log_2 n + 1$ probes in the worst case on $n = 2^m$ elements.

### Example 4: $T(n) = 2T(n-1) + 1$, $T(1) = 1$ (Towers of Hanoi)

$$
\begin{aligned}
T(n) &= 2T(n-1) + 1 \\
     &= 2[2T(n-2) + 1] + 1 = 4T(n-2) + 2 + 1 \\
     &= 8T(n-3) + 4 + 2 + 1 \\
     &= 2^k T(n-k) + \sum_{i=0}^{k-1} 2^i = 2^k T(n-k) + (2^k - 1) .
\end{aligned}
$$

With $k = n - 1$: $T(n) = 2^{n-1} \cdot 1 + 2^{n-1} - 1 = 2^n - 1$.

$$\boxed{T(n) = 2^n - 1 = \Theta(2^n)}$$

The multiplier $2^k$ grows at each step; this is the signature of exponential recursion.

### Example 5: $T(n) = 2T(n/2) + n$, $T(1) = 1$, $n = 2^m$

$$
\begin{aligned}
T(n) &= 2T(n/2) + n \\
     &= 2[2T(n/4) + n/2] + n = 4T(n/4) + n + n \\
     &= 8T(n/8) + n + n + n \\
     &= 2^k T(n/2^k) + kn .
\end{aligned}
$$

With $k = \log_2 n$: $T(n) = n \cdot T(1) + n\log_2 n = n\log_2 n + n$.

$$\boxed{T(n) = n\log_2 n + n = \Theta(n \log n)}$$

Each expansion contributes exactly $n$: every level of merge sort touches every element once ([3.6](topic6.md)).

### Example 6: $T(n) = T(n/2) + n$, $T(1) = 1$, $n = 2^m$

$$
T(n) = n + \frac{n}{2} + \frac{n}{4} + \cdots + 2 + T(1) = \sum_{i=0}^{\log_2 n} \frac{n}{2^i} = 2n - 1 .
$$

$$\boxed{T(n) = 2n - 1 = \Theta(n)}$$

A decreasing geometric series is dominated by its first term: the top-level work decides the bound.

### Example 7: $T(n) = 4T(n/2) + n$, $T(1) = 1$, $n = 2^m$

$$
T(n) = 4^k T(n/2^k) + n\left(1 + 2 + 4 + \cdots + 2^{k-1}\right) = 4^k T(n/2^k) + n(2^k - 1).
$$

With $k = \log_2 n$: $4^{\log_2 n} = n^{\log_2 4} = n^2$, so $T(n) = n^2 + n(n - 1) = 2n^2 - n$.

$$\boxed{T(n) = 2n^2 - n = \Theta(n^2)}$$

Now the series is *increasing*: the leaves ($n^2$ of them) dominate.

### Example 8: $T(n) = T(n-1) + \log n$, $T(1) = 0$

$$
T(n) = \log n + \log(n-1) + \cdots + \log 2 = \log n! = \Theta(n \log n)
$$

using the bound proved above. (This is the cost of inserting $n$ items one by one into a structure with logarithmic insertion.)

### Example 9: $T(n) = 2T(n/2) + n\log_2 n$, $T(1) = 0$, $n = 2^m$

Level $i$ has $2^i$ calls of size $n/2^i$, each costing $\frac{n}{2^i}\log_2\frac{n}{2^i}$, so level $i$ costs $n(\log_2 n - i)$:

$$
T(n) = \sum_{i=0}^{m-1} n(m - i) = n\sum_{j=1}^{m} j = \frac{n\,m(m+1)}{2} = \Theta(n \log^2 n).
$$

The classic master theorem cannot do this one (see the [gap discussion](topic5.md)); unrolling settles it directly.

## Telescoping

**Definition.** A sum $\sum_{i}(a_i - a_{i-1})$ *telescopes*: every intermediate term cancels and only $a_k - a_0$ remains. To use it on a recurrence, rewrite the recurrence so that it reads $S(k) - S(k-1) = (\text{known term})$ for some normalised function $S$.

### Example 10: $T(n) = 2T(n/2) + cn$ by telescoping

Divide by $n$: $\dfrac{T(n)}{n} = \dfrac{T(n/2)}{n/2} + c$. With $n = 2^k$ and $S(k) = T(2^k)/2^k$:

$$
\begin{aligned}
S(k) - S(k-1) &= c \\
S(k-1) - S(k-2) &= c \\
&\;\;\vdots \\
S(1) - S(0) &= c .
\end{aligned}
$$

Adding, all intermediate $S$ terms cancel: $S(k) = S(0) + ck$, so $T(n) = n\,T(1) + cn\log_2 n = \Theta(n \log n)$.

### Example 11 (advanced): average-case quicksort comparisons

The expected number of comparisons $C(n)$ of randomised quicksort satisfies ([Unit 5](../unit5/topic4.md))

$$
C(n) = (n - 1) + \frac{2}{n}\sum_{k=0}^{n-1} C(k), \qquad C(0) = C(1) = 0 .
$$

The full-history sum is removed by a telescoping trick. Multiply by $n$, write the same equation for $n-1$, and subtract:

$$
nC(n) - (n-1)C(n-1) = 2(n-1) + 2C(n-1) \;\Longrightarrow\; nC(n) = (n+1)C(n-1) + 2(n-1).
$$

Divide by $n(n+1)$: $\dfrac{C(n)}{n+1} = \dfrac{C(n-1)}{n} + \dfrac{2(n-1)}{n(n+1)}$. Now the left side telescopes, and summing the right side gives the exact result

$$
C(n) = 2(n+1)H_n - 4n \approx 2n\ln n \approx 1.39\,n\log_2 n = \Theta(n \log n).
$$

### When telescoping fails

Telescoping needs **one** recursive term per equation so that the expansions form a chain. $T(n) = T(n/3) + T(2n/3) + n$ has two recursive terms with different arguments; its expansion is a tree, not a chain, so nothing cancels. Use a [recursion tree](topic3.md) instead.

## Algorithmic Applications

| Algorithm | Recurrence | Iteration result |
|---|---|---|
| Linear recursion (sum, factorial, list length) | $T(n-1) + 1$ | $\Theta(n)$ |
| Recursive selection sort; quicksort worst case | $T(n-1) + n$ | $\Theta(n^2)$ |
| Towers of Hanoi; include/exclude enumeration | $2T(n-1) + 1$ | $2^n - 1$ |
| Binary search | $T(n/2) + 1$ | $\log_2 n + 1$ |
| Merge sort | $2T(n/2) + n$ | $n\log_2 n + n$ |
| Randomised quicksort (expected) | full-history | $2(n+1)H_n - 4n$ |

## Python Implementation

The iteration method is literally the conversion of a recursion into a loop that accumulates a sum. The code below evaluates the unrolled sums, which lets you check a hand-derived closed form exactly.

```python
def unroll_subtractive(n, f, base):
    """T(n) = T(n-1) + f(n), T(1) = base, evaluated by summing the expansion."""
    total = base
    for i in range(2, n + 1):        # the terms f(2), f(3), ..., f(n)
        total += f(i)
    return total


def unroll_dividing(n, a, b, f, base):
    """T(n) = a*T(n/b) + f(n), T(1) = base, for n an exact power of b.

    Level i of the expansion contributes a**i * f(n / b**i); the last level
    contributes a**k * base where k = log_b n.
    """
    total, size, mult = 0, n, 1
    while size > 1:
        total += mult * f(size)
        size //= b
        mult *= a
    return total + mult * base     # mult == a**k == n**log_b(a) leaves


if __name__ == "__main__":
    n = 1024
    assert unroll_subtractive(n, lambda i: i, 1) == n * (n + 1) // 2          # Example 2
    assert unroll_dividing(n, 1, 2, lambda m: 1, 1) == 11                       # Example 3
    assert unroll_dividing(n, 2, 2, lambda m: m, 1) == n * 10 + n               # Example 5
    assert unroll_dividing(n, 1, 2, lambda m: m, 1) == 2 * n - 1                # Example 6
    assert unroll_dividing(n, 4, 2, lambda m: m, 1) == 2 * n * n - n            # Example 7
    print("all closed forms confirmed")
```

- `unroll_dividing` keeps `mult` $= a^i$ and `size` $= n/b^i$, exactly the two quantities tracked by hand. When the loop ends, `mult` equals $a^{\log_b n} = n^{\log_b a}$, the number of leaves.
- Using integers (not floats) makes the checks exact, so an off-by-one in a hand-derived closed form shows up immediately.
- Both functions are iterative, so they do not hit Python's recursion limit even for $n$ in the millions.

## Edge Cases and Pitfalls

| Case / pitfall | What goes wrong | Fix |
|---|---|---|
| Simplifying during expansion | $T(n-3) + 3n - 3$ hides that the terms are $n, n-1, n-2$ | Keep terms in raw form until the pattern is clear |
| Wrong stopping index | Using $k = n$ when the base case is $T(1)$ gives $T(0)$, which may be undefined | Solve $\text{arg}_k = n_0$ for the actual base index |
| Dropping the leaf term | Writing $T(n) = kn$ for Example 5 and forgetting $2^k T(1) = n$ | Always add $(\text{multiplier}_k) \cdot T(n_0)$; it is $n^{\log_b a}$ leaves |
| Treating $\log$ terms as constants | In Example 9, $\log(n/2^i)$ shrinks with $i$; treating it as $\log n$ gives only an upper bound | Track how $f$ changes with the level |
| Non-integer arguments | $n/2^k$ not an integer when $n$ is not a power of 2 | Assume $n = b^m$, then extend by monotonicity |
| Applying to multi-branch recurrences | $T(n/3) + T(2n/3)$ branches into a tree, expansion explodes | Use the recursion tree or substitution |
| Geometric series with $r$ close to 1 | Misjudging which term dominates | Compute $r$ explicitly: $r<1$ root, $r=1$ every level, $r>1$ leaves |

## Common Misconceptions

- **"The iteration method is a proof."** It derives a candidate closed form by pattern recognition. The pattern is proved by induction ([substitution](topic4.md)); for standard recurrences this step is routine and often omitted.
- **"$T(n) = T(n-1) + n$ is $\Theta(n \log n)$ because it looks like merge sort."** Merge sort halves; this recurrence peels off one element. It is $\Theta(n^2)$.
- **"$2T(n-1)$ is like $2T(n/2)$."** One is $\Theta(2^n)$, the other $\Theta(n)$ (with $O(1)$ extra work). The subtraction creates depth $n$; the division creates depth $\log n$.
- **"Telescoping works for any recurrence."** It needs a single recursive term after normalisation.
- **"Constants in the base case change the bound."** They change the leaf contribution by a constant factor only.

## Alternatives and Trade-offs

| Method | Use when | Avoid when |
|---|---|---|
| Iteration | One recursive term; subtractive recurrences; exact constants needed | Several recursive terms with different sizes |
| Telescoping | Recurrence can be normalised to $S(k) = S(k-1) + g(k)$; full-history recurrences | Two or more distinct recursive arguments |
| [Recursion tree](topic3.md) | Multiple branches, unequal splits, building intuition | You need an exact closed form |
| [Master method](topic5.md) | $aT(n/b) + f(n)$ and only $\Theta$ is needed | Subtract-and-conquer; non-constant $a$ |
| [Substitution](topic4.md) | Proving a guess rigorously | You have no guess yet |

## In Practice

- **Exact operation counts.** Exact formulas such as $2^n - 1$ moves, $\log_2 n + 1$ probes, or $n\lceil \lg n\rceil - 2^{\lceil \lg n\rceil} + 1$ comparisons come from unrolling. They matter when constants matter: comparing algorithms with the same $\Theta$, or sizing hardware.
- **Recursion to iteration.** Unrolling a recurrence is exactly what an engineer does when converting a tail-recursive function into a loop (to avoid stack overflow). The loop index is the expansion depth $k$.
- **Performance regressions.** A recursive function that accidentally rebuilds a list at each level turns $T(n-1) + O(1)$ into $T(n-1) + O(n)$, i.e. $\Theta(n)$ into $\Theta(n^2)$. Example 2 is the arithmetic behind many real slowdowns (string building in loops, `list.pop(0)` in recursion).

## Interview and Competitive Programming

- **Recognition cue:** "process one element and recurse on the rest" means $T(n-1) + f(n)$, so the answer is $\sum f(i)$. Linear work per step gives $O(n^2)$; that is often the brute force the interviewer wants you to beat.
- **Exponential detector:** if the multiplier in front of $T(n-1)$ is at least 2, the solution is at least $2^n$. With $n > 30$ this is infeasible; look for memoisation or a different decomposition.
- **Quick mental unrolling:** for $T(n) = T(n/2) + f(n)$, the answer is $f(n) + f(n/2) + f(n/4) + \cdots$. For polynomial $f$ this is $\Theta(f(n))$; for $f = 1$ it is $\Theta(\log n)$.
- **Trap:** the bound of a recursion that halves but does linear work, $T(n/2) + n$, is $O(n)$, not $O(n \log n)$. This is why quickselect is expected linear while quicksort is $n \log n$.

## Using AI Assistants Critically

- LLM derivations often "skip to the pattern" and get the stopping index wrong (e.g. $k = n$ instead of $n-1$), producing off-by-one closed forms. Check the closed form at $n = 1, 2, 3$ by hand.
- They commonly drop the leaf term $a^k T(1)$ in dividing recurrences; for $4T(n/2) + n$ this loses the dominant $n^2$ term entirely.
- Expect confident misuse of geometric series, such as treating $\sum (3/2)^i$ as bounded. Ask for the ratio $r$ explicitly.
- Verify any claimed closed form with an exact evaluator like `unroll_dividing` over many $n$ (integers, not floats).
- If an assistant claims a subtractive recurrence is solved "by the master theorem", reject the derivation; the theorem does not apply to $T(n-1)$.

## Practice

### Beginner

1. Solve $T(n) = T(n-1) + 3$, $T(0) = 2$ exactly. *Output:* closed form and $\Theta$ bound. *Difficulty:* easy.
2. Solve $T(n) = T(n/3) + 1$, $T(1) = 1$, for $n = 3^m$. *Output:* closed form. *Difficulty:* easy.
3. Solve $T(n) = T(n-2) + 1$, $T(0) = T(1) = 0$. *Output:* closed form for even and odd $n$. *Difficulty:* easy.

### Intermediate

1. Solve $T(n) = 3T(n-1) + 2$, $T(0) = 0$ exactly and give its $\Theta$ bound. *Difficulty:* medium.
2. Solve $T(n) = 3T(n/3) + n$, $T(1) = 1$, for $n = 3^m$ exactly. *Difficulty:* medium.
3. Solve $T(n) = T(n-1) + n^2$, $T(0) = 0$ exactly using the sum of squares. *Difficulty:* medium.

### Advanced

1. Solve $T(n) = 2T(n/2) + n/\log_2 n$, $T(2) = 1$, for $n = 2^m$ by iteration and show it is $\Theta(n \log\log n)$. *Hint domain:* harmonic numbers. *Difficulty:* hard.
2. Use telescoping to solve $T(n) = \frac{n+1}{n}T(n-1) + 1$, $T(1) = 1$. *Difficulty:* hard.
3. Solve $T(n) = 8T(n/2) + n^2$, $T(1) = 1$, exactly for $n = 2^m$ and identify which level of the expansion dominates. *Difficulty:* hard.

### Interview / CP

1. A recursive function to reverse a string returns `reverse(s[1:]) + s[0]` in Python. Write its recurrence including slicing and concatenation and solve it. *Constraints:* $|s| \le 10^5$. *Difficulty:* medium.
2. Count the exact number of moves for Towers of Hanoi with 64 disks and estimate the time at one move per microsecond. *Difficulty:* easy.
3. A function computes `f(n) = f(n-1) + f(n-1)` (called twice, not reused). Give the recurrence for its running time and a one-line fix that changes it to $O(n)$. *Difficulty:* easy.

## Self-Check Questions

??? question "Q1. In Example 2, why must we stop at $k = n-1$ and not $k = n$?"
    The base case is given at $T(1)$. The argument after $k$ expansions is $n-k$, and $n-k = 1$ gives $k = n-1$. Using $k = n$ would require $T(0)$, which is not defined by the recurrence.

??? question "Q2. Unroll $T(n) = 3T(n/2) + n$ for $n = 2^m$ and identify which part dominates."
    $T(n) = n\sum_{i=0}^{m-1}(3/2)^i + 3^m T(1)$. The ratio $3/2 > 1$, so the series is dominated by its last term, of order $3^m = n^{\log_2 3}$. The leaves dominate: $T(n) = \Theta(n^{\log_2 3}) \approx \Theta(n^{1.585})$.

??? question "Q3. Why does $T(n) = T(n/2) + n$ give $\Theta(n)$ while $T(n) = 2T(n/2) + n$ gives $\Theta(n \log n)$?"
    In the first, level $i$ costs $n/2^i$, a decreasing geometric series summing to less than $2n$. In the second, level $i$ has $2^i$ calls of size $n/2^i$, so every level costs $n$, and there are $\log_2 n$ levels.

??? question "Q4. What is the exact solution of $T(n) = 2T(n-1) + 1$ with $T(0) = 0$, and how would you verify it without induction?"
    $T(n) = 2^n - 1$. Check small values: $T(0) = 0 = 2^0 - 1$, $T(1) = 1$, $T(2) = 3$, $T(3) = 7$. Then substitute the formula into the recurrence: $2(2^{n-1} - 1) + 1 = 2^n - 1$. (That substitution is, in fact, the inductive step.)

??? question "Q5. Explain why telescoping works on $T(n) = 2T(n/2) + cn$ but not on $T(n) = T(n/3) + T(2n/3) + n$."
    After dividing by $n$, the first becomes $S(k) = S(k-1) + c$: one unknown per equation, so the equations chain and intermediate terms cancel. The second has two unknowns with different arguments; any normalisation leaves a weighted sum of two different values, the expansion branches into a tree, and nothing cancels.

??? question "Q6. Show that $\sum_{i=1}^{n}\log i = \Theta(n \log n)$."
    Each term is at most $\log n$, so the sum is at most $n\log n$. The last $n/2$ terms are each at least $\log(n/2)$, so the sum is at least $\frac{n}{2}(\log n - 1) = \Omega(n \log n)$.

??? question "Q7. A student solves $T(n) = 4T(n/2) + n$ by iteration and gets $T(n) = n(n-1) = \Theta(n^2)$. The bound is right; what was dropped, and when would it matter?"
    The leaf term $4^{\log_2 n}T(1) = n^2 T(1)$. With $T(1) = 1$ the exact answer is $2n^2 - n$. The $\Theta$ bound survives by luck; for $T(n) = 4T(n/2) + 1$ dropping the leaves would give $\Theta(n)$ instead of $\Theta(n^2)$.

## Complexity Summary

| Recurrence | Exact (base as shown) | $\Theta$ |
|---|---|---|
| $T(n-1) + 1$, $T(1) = 1$ | $n$ | $\Theta(n)$ |
| $T(n-1) + n$, $T(1) = 1$ | $n(n+1)/2$ | $\Theta(n^2)$ |
| $T(n-1) + \log n$, $T(1) = 0$ | $\log n!$ | $\Theta(n \log n)$ |
| $2T(n-1) + 1$, $T(1) = 1$ | $2^n - 1$ | $\Theta(2^n)$ |
| $T(n/2) + 1$, $T(1) = 1$ | $\log_2 n + 1$ | $\Theta(\log n)$ |
| $T(n/2) + n$, $T(1) = 1$ | $2n - 1$ | $\Theta(n)$ |
| $2T(n/2) + n$, $T(1) = 1$ | $n\log_2 n + n$ | $\Theta(n \log n)$ |
| $4T(n/2) + n$, $T(1) = 1$ | $2n^2 - n$ | $\Theta(n^2)$ |
| $2T(n/2) + n\log_2 n$, $T(1) = 0$ | $\frac{n}{2}\log_2 n(\log_2 n + 1)$ | $\Theta(n \log^2 n)$ |

## Key Takeaways

- Unroll, generalise to step $k$, stop at the base case, evaluate the sum.
- Keep terms unsimplified while expanding; patterns hide behind early simplification.
- Never forget the leaf term $a^k T(n_0) = n^{\log_b a} \cdot T(n_0)$.
- The shape of the level-cost series decides the answer: decreasing geometric means the top dominates, constant means multiply by depth, increasing geometric means the leaves dominate.
- Iteration is the method of choice for subtract-and-conquer recurrences and for exact constants.
- Telescoping is a fast special case that needs a single recursive term after normalisation.
- The pattern is observed, not proved; confirm it by induction when rigour is required.
