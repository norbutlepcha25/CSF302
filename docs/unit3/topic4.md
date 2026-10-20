# Substitution Method

!!! abstract "At a glance"

    - **Problem:** turn a *guessed* bound for a recurrence into a *proof*.
    - **Key idea:** guess the form of the solution, then prove it by (strong) mathematical induction, substituting the guess for $T$ on the smaller arguments; the name comes from that substitution.
    - **Two classic techniques:** *strengthening the hypothesis* (subtract a lower-order term) when the induction almost works, and *changing variables* ($n = 2^m$) when the recurrence has odd arguments like $\sqrt{n}$.
    - **Where it is used:** whenever the master method does not apply (unequal splits, subtractive recurrences, $\sqrt{n}$ arguments), and as the rigorous back-end of the recursion tree and iteration methods.

## Motivation and Problem Context

The [iteration](topic2.md) and [recursion tree](topic3.md) methods find the answer by pattern recognition and summation. They are excellent for discovery but leave gaps: patterns are observed, unbalanced trees are bounded loosely, floors are ignored. The substitution method closes those gaps. It is the only method in this unit that works, in principle, for **any** recurrence, provided you can guess the answer. It is also the method most often done wrongly, because an induction that "looks right" can prove a false statement if the constants are not handled exactly. Learning to do it correctly is learning to reason precisely about asymptotic claims.

## Problem Formulation

- **Input:** a recurrence $T(n)$ with base cases, and a candidate bound $g(n)$.
- **Output:** a proof that there exist constants $c > 0$ and $n_0$ such that $T(n) \le c\,g(n)$ for all $n \ge n_0$ (upper bound, $O$), and/or $T(n) \ge c'\,g(n)$ (lower bound, $\Omega$). Both together give $\Theta$.
- **Assumptions:** $T(n)$ is positive; the recursive arguments are strictly smaller than $n$ for all $n \ge n_0$ (so strong induction is well founded).

## Intuition

Induction works "from the bottom up": if the bound holds for all smaller inputs and the recurrence turns those bounds into the same bound for $n$, then it holds everywhere. The crucial requirement is that the bound **reproduces itself with the same constant**. If you assume $T(k) \le ck$ for smaller $k$ and derive $T(n) \le cn + n$, the constant grew from $c$ to $c+1$; repeat this $\log n$ times and the "constant" is $\log n$. That is why the inductive step must end with *exactly* the hypothesis form, $T(n) \le c\,g(n)$, and not with "$O(g(n))$".

!!! tip "Mental model"
    The inductive hypothesis is a contract with a fixed constant $c$. The inductive step must hand back the same contract, with the same $c$. Anything "bigger by a little" breaks the contract.

## Definitions

**Strong induction.** To prove $P(n)$ for all $n \ge n_0$: prove $P$ for the base values, then prove that if $P(k)$ holds for all $n_0 \le k < n$, then $P(n)$ holds.

**The claim** is a precise inequality with explicit constants: "$T(n) \le c\,n\log_2 n$ for all $n \ge 2$", never "$T(n) = O(n\log n)$" inside the induction.

**Base cases.** The values of $n$ that the inductive step cannot handle because a recursive argument would fall below $n_0$. With floors, there may be several (e.g. $n = 2$ and $n = 3$ when the step needs $\lfloor n/2 \rfloor \ge 2$).

**Strengthening the hypothesis.** Replacing the claim $T(n) \le c\,g(n)$ by the *stronger* claim $T(n) \le c\,g(n) - h(n)$ for a lower-order $h(n)$. A stronger claim gives a stronger assumption on smaller inputs, which can make the inductive step go through.

## Method

1. **Guess** the form of the solution, using a [recursion tree](topic3.md), [iteration](topic2.md), the [master method](topic5.md), or similarity to a known recurrence.
2. **State the claim** with explicit constants: $T(n) \le c\,g(n)$ for $n \ge n_0$.
3. **Inductive step:** assume the claim for all smaller arguments; substitute it into the recurrence; manipulate until you reach $T(n) \le c\,g(n) - (\text{residual})$; find the condition on $c$ (and $n$) that makes the residual non-negative.
4. **Base cases:** identify every $n$ the step relies on but cannot itself prove; choose $c$ (and $n_0$) large enough to cover them.
5. **Repeat for the lower bound** with $\ge$ if you need $\Theta$.
6. **If the step fails by a lower-order term**, strengthen the hypothesis (subtract that term) and redo steps 3 and 4. If it fails by a higher-order term, the guess is wrong.

!!! warning "Important"
    The inductive step must end in **exactly** $T(n) \le c\,g(n)$ with the **same** $c$. Ending with "$\le cn + n = O(n)$" is not a proof; it is the most common error in substitution proofs and is penalised in exams.

## Worked Examples

### Example 1: $T(n) = 2T(\lfloor n/2 \rfloor) + n$, $T(1) = 1$ is $O(n\log n)$

(Logs base 2.) **Guess:** $T(n) \le c\,n\log n$ for all $n \ge 2$.

**Inductive step** (for $n \ge 4$, so that $\lfloor n/2 \rfloor \ge 2$ is covered by the hypothesis):

$$
\begin{aligned}
T(n) &= 2T(\lfloor n/2 \rfloor) + n \\
     &\le 2c\lfloor n/2 \rfloor\log\lfloor n/2 \rfloor + n && \text{(hypothesis)} \\
     &\le 2c\,\frac{n}{2}\log\frac{n}{2} + n && (\lfloor n/2 \rfloor \le n/2) \\
     &= cn\log n - cn + n \\
     &\le cn\log n && \text{if } c \ge 1 .
\end{aligned}
$$

**Base cases.** The claim cannot start at $n = 1$: $c \cdot 1 \cdot \log 1 = 0 < T(1) = 1$. That is why $n_0 = 2$. The step needs $\lfloor n/2 \rfloor \ge 2$, i.e. $n \ge 4$, so $n = 2$ and $n = 3$ are base cases:

- $T(2) = 2T(1) + 2 = 4 \le c \cdot 2\log 2 = 2c$ requires $c \ge 2$.
- $T(3) = 2T(1) + 3 = 5 \le c \cdot 3\log 3 \approx 4.75c$ requires $c \ge 1.06$.

Choose $c = 2$, $n_0 = 2$. Then $T(n) \le 2n\log n$ for all $n \ge 2$, so $T(n) = O(n\log n)$. $\blacksquare$

**Lower bound** (for $n$ a power of 2, to keep it short). Claim $T(n) \ge d\,n\log n$. Then $T(n) \ge 2d\frac{n}{2}\log\frac{n}{2} + n = dn\log n + (1 - d)n \ge dn\log n$ if $d \le 1$; base $T(2) = 4 \ge 2d$. So $d = 1$ works and $T(n) = \Theta(n\log n)$.

### Example 2: the classic false proof that $T(n) = 2T(n/2) + n$ is $O(n)$

!!! danger "A wrong proof"
    "Assume $T(k) \le ck$ for $k < n$. Then $T(n) \le 2c(n/2) + n = cn + n = O(n)$. Done."

The last step silently changes the constant from $c$ to $c+1$. The claim was $T(n) \le cn$; the derivation produced $T(n) \le (c+1)n$, which is **not** the claim. Since $cn + n \le cn$ is false for every $c$ and every $n \ge 1$, the induction fails, as it must: $T(n) = \Theta(n\log n)$, and the ratio $T(n)/n$ grows without bound (see the Python table below). Asymptotic notation is a statement about a whole function; it cannot be applied to a single step of an induction.

### Example 3: strengthening the hypothesis, $T(n) = 2T(n/2) + 1$, $T(1) = 1$

**First guess:** $T(n) \le cn$. Step: $T(n) \le 2c(n/2) + 1 = cn + 1$. Fails, but only by the constant $1$, which is lower order than $cn$. The guess is right; the hypothesis is too weak.

**Strengthened guess:** $T(n) \le cn - d$ for constants $c > 0$, $d \ge 0$.

$$
T(n) \le 2\left(c\frac{n}{2} - d\right) + 1 = cn - 2d + 1 \le cn - d \quad\text{iff}\quad d \ge 1 .
$$

**Base:** $T(1) = 1 \le c - d$. Take $d = 1$, $c = 2$: the claim $T(n) \le 2n - 1$ holds, with equality, for every power of 2. So $T(n) = O(n)$.

!!! tip "Why subtracting makes the proof easier"
    Proving a *stronger* statement seems harder, but in induction the statement is also what you *assume* for smaller inputs. Assuming $T(n/2) \le cn/2 - d$ gives you $2d$ of slack after doubling, which pays for the $+1$.

### Example 4: strengthening again, $T(n) = 2T(n-1) + 1$, $T(1) = 1$

**Guess** $T(n) \le c\,2^n$: step gives $c\,2^n + 1$. Fails by a constant.

**Strengthen** to $T(n) \le c\,2^n - d$:

$$
T(n) \le 2(c\,2^{n-1} - d) + 1 = c\,2^n - 2d + 1 \le c\,2^n - d \quad\text{iff}\quad d \ge 1 .
$$

**Base:** $T(1) = 1 \le 2c - 1$ needs $c \ge 1$. With $c = d = 1$: $T(n) \le 2^n - 1$, which is in fact exact (Towers of Hanoi, [3.2](topic2.md)).

(Note the algebra: $2 \cdot c\,2^{n-1} = c\,2^n$ and $2 \cdot d = 2d$. Writing "$-2 + 1$" instead of "$-2d + 1$" silently sets $d = 1$ and is an error even when the conclusion happens to be right.)

### Example 5: $T(n) = T(n-1) + n$, $T(1) = 1$ is $\Theta(n^2)$

**Upper**, claim $T(n) \le cn^2$:

$$
T(n) \le c(n-1)^2 + n = cn^2 - (2c - 1)n + c \le cn^2 \quad\text{iff}\quad (2c-1)n \ge c .
$$

For $c = 1$: $n \ge 1$, always true. Base $T(1) = 1 \le c$. So $T(n) \le n^2$.

**Lower**, claim $T(n) \ge dn^2$: $T(n) \ge d(n-1)^2 + n = dn^2 + (1 - 2d)n + d \ge dn^2$ if $d \le 1/2$. Base $T(1) = 1 \ge d$. So $T(n) \ge n^2/2$, and $T(n) = \Theta(n^2)$ (exact value $n(n+1)/2$).

### Example 6: naive Fibonacci, $T(n) = T(n-1) + T(n-2) + 1$, $T(0) = T(1) = 1$

Let $\varphi = (1+\sqrt{5})/2$, which satisfies $\varphi^2 = \varphi + 1$.

**Upper**, strengthened claim $T(n) \le c\varphi^n - d$:

$$
T(n) \le c\varphi^{n-1} - d + c\varphi^{n-2} - d + 1 = c\varphi^{n-2}(\varphi + 1) - 2d + 1 = c\varphi^n - 2d + 1 \le c\varphi^n - d
$$

when $d \ge 1$. Base: $1 \le c - 1$ and $1 \le c\varphi - 1$ hold for $c = 2$. **Lower**, claim $T(n) \ge c'\varphi^n$: $T(n) \ge c'\varphi^{n-1} + c'\varphi^{n-2} + 1 \ge c'\varphi^n$; base needs $c' \le 1/\varphi$. Hence $T(n) = \Theta(\varphi^n) \approx \Theta(1.618^n)$.

### Example 7: confirming the unbalanced tree, $T(n) = T(n/3) + T(2n/3) + cn$

The [recursion tree](topic3.md) suggested $\Theta(n\log n)$. Claim $T(n) \le dn\log n$:

$$
\begin{aligned}
T(n) &\le d\frac{n}{3}\log\frac{n}{3} + d\frac{2n}{3}\log\frac{2n}{3} + cn \\
     &= dn\log n - dn\left(\frac{1}{3}\log 3 + \frac{2}{3}\log\frac{3}{2}\right) + cn \\
     &= dn\log n - dn\left(\log 3 - \frac{2}{3}\right) + cn \\
     &\le dn\log n \quad\text{iff}\quad d \ge \frac{c}{\log 3 - 2/3} \approx 1.09\,c .
\end{aligned}
$$

The same computation with $\ge$ gives the lower bound with $d \le c/(\log 3 - 2/3)$. So $T(n) = \Theta(n\log n)$, now rigorously.

## Change of Variables

Some recurrences become standard after renaming the argument. The typical sign is an argument like $\sqrt{n}$ or $\log n$.

**Procedure.** Substitute $n = 2^m$ (so $m = \log_2 n$ and $\sqrt{n} = 2^{m/2}$), define $S(m) = T(2^m)$, solve the recurrence for $S$, then substitute $m = \log_2 n$ back.

### Example 8: $T(n) = 2T(\sqrt{n}) + \log_2 n$

With $n = 2^m$: $T(2^m) = 2T(2^{m/2}) + m$. Let $S(m) = T(2^m)$:

$$
S(m) = 2S(m/2) + m \;\Longrightarrow\; S(m) = \Theta(m\log m) \quad\text{(master method, case 2).}
$$

Substituting back, $m = \log_2 n$:

$$
\boxed{T(n) = \Theta(\log n \cdot \log\log n)}
$$

### Example 9: $T(n) = T(\sqrt{n}) + 1$ (van Emde Boas)

$S(m) = S(m/2) + 1 = \Theta(\log m)$, so $T(n) = \Theta(\log\log n)$. This is why a van Emde Boas tree over a universe of size $u$ supports successor queries in $O(\log\log u)$ time.

### Example 10: $T(n) = \sqrt{n}\,T(\sqrt{n}) + n$

Divide by $n$ first: $\dfrac{T(n)}{n} = \dfrac{T(\sqrt{n})}{\sqrt{n}} + 1$. Let $U(n) = T(n)/n$; then $U(n) = U(\sqrt{n}) + 1 = \Theta(\log\log n)$ by Example 9. Therefore

$$
\boxed{T(n) = \Theta(n\log\log n)} .
$$

!!! note "Tight versus valid bounds"
    Proving $T(n) = O(n\log n)$ for this recurrence by induction is correct (the claim $T(n) \le cn\log n$ reproduces itself with room to spare), but it is not tight. Change of variables shows the true growth is $\Theta(n\log\log n)$. When an induction closes with a lot of slack (here, $\frac{c}{2}n\log n + n \le cn\log n$), suspect that a smaller bound may also be provable.

## Algorithmic Applications

| Recurrence | Where it arises | Bound proved here |
|---|---|---|
| $2T(\lfloor n/2\rfloor) + n$ | merge sort with real floors | $\Theta(n\log n)$ |
| $2T(n/2) + 1$ | divide-and-conquer max, tree traversal | $2n - 1$, $\Theta(n)$ |
| $T(n-1) + T(n-2) + 1$ | naive recursive Fibonacci | $\Theta(\varphi^n)$ |
| $T(n/3) + T(2n/3) + n$ | quicksort with a guaranteed 1:2 split | $\Theta(n\log n)$ |
| $T(\sqrt{n}) + 1$ | van Emde Boas trees | $\Theta(\log\log n)$ |
| $\sqrt{n}\,T(\sqrt{n}) + n$ | recursive $\sqrt{n}$-way splitting: $\sqrt{n}$ blocks of size $\sqrt{n}$, linear work to combine | $\Theta(n\log\log n)$ |

## Python Implementation

Code cannot prove a bound, but it can *refute* a wrong guess quickly and confirm constants before you invest in a proof. The ratio $T(n)/g(n)$ under doubling of $n$ should settle to a constant if $g$ is the right growth rate.

```python
import math
from functools import lru_cache


@lru_cache(maxsize=None)
def T_merge(n):
    """T(n) = T(floor(n/2)) + T(ceil(n/2)) + n, T(1) = 1."""
    if n <= 1:
        return 1
    return T_merge(n // 2) + T_merge(n - n // 2) + n


@lru_cache(maxsize=None)
def T_tree(n):
    """T(n) = T(floor(n/2)) + T(ceil(n/2)) + 1, T(1) = 1."""
    if n <= 1:
        return 1
    return T_tree(n // 2) + T_tree(n - n // 2) + 1


def ratio_table(T, guess, ns):
    """Print T(n) / guess(n). A bounded ratio supports the guess; it does not prove it."""
    for n in ns:
        print(f"n={n:>8}  T(n)={T(n):>10}  T(n)/guess(n)={T(n) / guess(n):.4f}")


if __name__ == "__main__":
    doubling = [2**k for k in range(4, 19, 2)]
    ratio_table(T_merge, lambda n: n, doubling)                    # guess O(n)
    ratio_table(T_merge, lambda n: n * math.log2(n), doubling)     # guess O(n lg n)
    ratio_table(T_tree, lambda n: 2 * n - 1, doubling)             # strengthened guess
```

| $n$ | $T_\text{merge}(n)/n$ | $T_\text{merge}(n)/(n\lg n)$ | $T_\text{tree}(n)/(2n-1)$ |
|---|---|---|---|
| 16 | 5.0 | 1.250 | 1.0 |
| 256 | 9.0 | 1.125 | 1.0 |
| 4096 | 13.0 | 1.083 | 1.0 |
| 65536 | 17.0 | 1.063 | 1.0 |
| 262144 | 19.0 | 1.056 | 1.0 |

- The first column grows by 2 every time $n$ is multiplied by 4 (it equals $\lg n + 1$): empirical confirmation that the "$O(n)$ proof" of Example 2 is false.
- The second column settles toward 1, consistent with $T(n) = n\lg n + n$ on powers of 2.
- The third column is exactly 1: $T_\text{tree}(n) = 2n - 1$ for *all* $n$, matching the strengthened hypothesis of Example 3 even with floors and ceilings.

## Edge Cases and Pitfalls

| Case / pitfall | What goes wrong | Fix |
|---|---|---|
| Ending with "$= O(g(n))$" | Constant drifts from $c$ to $c+1$; proves false claims | End with $T(n) \le c\,g(n)$, same $c$ |
| Base case at $n = 1$ with $g(n) = n\log n$ | $c \cdot 1 \cdot \log 1 = 0$ cannot bound $T(1) > 0$ | Start at $n_0 = 2$; check every base value the step relies on |
| Floors reaching small values | For $n = 3$, $\lfloor 3/2 \rfloor = 1$ is below $n_0$ | Add $n = 2, 3$ (or whatever is needed) as base cases |
| Step fails by a lower-order term | Concluding the guess is wrong | Strengthen: subtract a lower-order term ($-d$, $-dn$) |
| Step fails by a higher-order term | Trying to fix it by strengthening | The guess is too small; increase it |
| Adding a lower-order term instead of subtracting | $T(n) \le cn + d$ gives $cn + 2d + 1$, worse | Subtract; the slack must come from the hypothesis |
| Algebra slips with constants | "$2c \cdot 2^{n-1} - 2 + 1$" loses the $c$ or $d$ multiplier | Carry every constant symbolically to the end |
| Proving only $O$ and claiming $\Theta$ | Upper bound alone does not give tightness | Do the $\Omega$ induction too, or cite a matching lower bound |

## Common Misconceptions

- **"If the induction goes through with $O(\cdot)$ at the end, the bound is proved."** No: the hypothesis must be an explicit inequality with a fixed constant.
- **"Strengthening the hypothesis makes the proof harder."** It makes the *assumption* stronger too, which is what rescues the step.
- **"If the proof fails, the guess is wrong."** Not necessarily. A failure by a lower-order term means the hypothesis needs strengthening; a failure by a higher-order term means the guess is wrong.
- **"A successful induction gives a tight bound."** It gives a valid bound. $T(n) = \sqrt{n}T(\sqrt{n}) + n$ satisfies $O(n\log n)$, but the tight bound is $\Theta(n\log\log n)$.
- **"Base cases are a formality."** They fix the constant $c$ and $n_0$, and with $g(n) = n\log n$ the obvious base case $n = 1$ is actually false.

## Alternatives and Trade-offs

| Method | Strength relative to substitution | When to prefer it |
|---|---|---|
| [Iteration](topic2.md) | Finds the answer without a guess | One recursive term; exact closed form wanted |
| [Recursion tree](topic3.md) | Visual; produces the guess | Multiple or unequal recursive terms |
| [Master method](topic5.md) | Fastest by far | $aT(n/b) + f(n)$ with $f$ outside the gaps |
| Substitution | Rigorous; handles any recurrence; handles floors exactly | You need a proof, or no other method applies |
| Change of variables + another method | Reduces odd recurrences to standard ones | Arguments like $\sqrt{n}$, $\log n$, $n^{1/k}$ |

**When NOT to use substitution:** when you have no idea of the answer (get one from a tree first), or when the master method applies directly and only the bound is required.

## In Practice

- **Rigorous guarantees.** Library and systems designers who claim worst-case bounds (e.g. "$O(n\log n)$ worst case" for a sort, "$O(\log\log u)$" for a predecessor structure) rely on proofs of exactly this kind; papers on algorithms state and prove such inductions explicitly.
- **Proof assistants and verified software.** Formal verification tools (Coq, Isabelle, Lean) prove complexity bounds by induction in this style; a step that ends in "$O(\cdot)$" instead of an explicit inequality would simply not be accepted, which is a good mental model for what a correct manual proof must look like.
- **Performance testing.** Doubling experiments like the ratio table above are standard practice for catching complexity regressions: if $T(2n)/T(n)$ drifts from the expected constant, either the analysis or the implementation is wrong.

## Interview and Competitive Programming

- Interviews rarely ask for an induction proof, but they do ask "can you justify that bound?". A two-line substitution argument ("assume $T(k) \le ck\log k$; then $2c\frac{n}{2}\log\frac{n}{2} + n = cn\log n - cn + n \le cn\log n$ for $c \ge 1$") is a strong answer.
- **Recognition cue:** argument $\sqrt{n}$ means change variables; $\log\log n$ factors are likely.
- **Recognition cue:** two recursive calls of different sizes $n - 1$ and $n - 2$ means exponential with base the root of $x^2 = x + 1$; in general $T(n) = \sum c_i T(n - i)$ grows like $r^n$ for the largest root $r$ of the characteristic equation.
- **Trap:** "it is $O(n)$ because each call does $O(1)$ work and there are two calls" (wrong for $2T(n-1)$). Count the calls, not the work per call.

## Using AI Assistants Critically

- LLM-written induction proofs frequently end with "$\le cn + n = O(n)$" and declare victory. This is exactly the Example 2 fallacy; reject any proof whose final line is not the hypothesis with the same constant.
- They often skip base cases or use $n = 1$ for an $n\log n$ claim, where the bound is false. Ask for every base value the step uses.
- Algebra with symbolic constants is a weak spot (dropping $c$ or $d$ when multiplying). Re-derive each line or check it symbolically (e.g. with `sympy`).
- Assistants tend to propose a guess and "prove" it even when the guess is wrong. Refute or support the guess numerically first with a ratio table under doubling.
- For change-of-variables problems, verify the back-substitution: an assistant may correctly get $S(m) = \Theta(m\log m)$ and then write $\Theta(\log\log\log n)$ (an error that appeared in an earlier version of these notes) instead of $\Theta(\log n\log\log n)$.

## Practice

### Beginner

1. Prove by substitution that $T(n) = T(n-1) + 2$, $T(1) = 1$ satisfies $T(n) \le 2n$. *Output:* full proof with base case. *Difficulty:* easy.
2. Prove $T(n) = T(\lfloor n/2 \rfloor) + 1$, $T(1) = 1$ satisfies $T(n) \le 1 + \log_2 n$. *Difficulty:* easy.
3. Identify the error in the claim "$T(n) = 4T(n/2) + n$ is $O(n^2)$ because $4c(n/2)^2 + n = cn^2 + n = O(n^2)$", and repair the proof. *Difficulty:* easy-medium.

### Intermediate

1. Prove $T(n) = 4T(n/2) + n^2$ is $O(n^2\log n)$ by substitution. *Difficulty:* medium.
2. Show that the hypothesis $T(n) \le cn^2$ fails for $T(n) = 4T(n/2) + n$ only by a lower-order term, and complete the proof by strengthening. *Difficulty:* medium.
3. Solve $T(n) = 2T(\sqrt{n}) + 1$ by change of variables. *Difficulty:* medium.

### Advanced

1. Prove that $T(n) = T(\lceil n/2 \rceil) + T(\lfloor n/2 \rfloor) + 1$, $T(1) = 1$ equals $2n - 1$ for every $n \ge 1$ (not just powers of 2). *Difficulty:* hard.
2. Prove $T(n) = T(n/2) + T(n/4) + T(n/8) + n$ is $\Theta(n)$ by substitution. *Difficulty:* hard.
3. Solve $T(n) = n^{2/3}T(n^{1/3}) + n$ by an appropriate normalisation and change of variables. *Difficulty:* hard.

### Interview / CP

1. A recursive solution computes `f(n) = f(n-1) + f(n-3)` without memoisation. Determine the growth rate of its running time to within a constant base (characteristic root), and estimate the largest feasible $n$ for one second. *Difficulty:* medium.
2. Justify in two lines that a recursion with two calls on $n/2$ and $O(n)$ work is $O(n\log n)$, in a form you would say in an interview. *Difficulty:* easy.
3. An interviewer claims your recursive solution with recurrence $T(n) = 2T(n/2) + O(1)$ is $O(n\log n)$. Prove the tighter $O(n)$ bound by strengthening. *Difficulty:* medium.

## Self-Check Questions

??? question "Q1. What is wrong with: 'Assume $T(k) \le ck$. Then $T(n) = 2T(n/2) + n \le cn + n = O(n)$'?"
    The claim was $T(n) \le cn$ with a fixed $c$. The derivation produces $T(n) \le (c+1)n$, which is a different, weaker statement. The induction does not close; in fact no constant works, since $T(n) = \Theta(n\log n)$.

??? question "Q2. Why can't the base case of a $T(n) \le cn\log n$ proof be $n = 1$?"
    $c \cdot 1 \cdot \log 1 = 0$, but $T(1)$ is a positive constant, so the inequality is false at $n = 1$ for every $c$. Asymptotic bounds only need to hold for $n \ge n_0$, so start at $n_0 = 2$ and treat every small value the step relies on as a base case.

??? question "Q3. The step for $T(n) = 2T(n/2) + 1$ with hypothesis $T(n) \le cn$ gives $cn + 1$. Is the guess wrong?"
    No. It fails by a constant, which is lower order than $cn$. Strengthen to $T(n) \le cn - d$: the step gives $cn - 2d + 1 \le cn - d$ for $d \ge 1$, and the base $T(1) = 1 \le c - d$ holds for $c = 2, d = 1$.

??? question "Q4. Solve $T(n) = 2T(\sqrt{n}) + \log n$ and explain each substitution."
    Set $n = 2^m$, so $\sqrt{n} = 2^{m/2}$ and $\log n = m$. Define $S(m) = T(2^m)$: $S(m) = 2S(m/2) + m$, which is $\Theta(m\log m)$. Since $m = \log n$, $T(n) = \Theta(\log n\log\log n)$.

??? question "Q5. How do you tell whether a failing induction needs strengthening or a bigger guess?"
    Compare the leftover term with the bound. If the step yields $c\,g(n) + h(n)$ with $h = o(g)$ (lower order), strengthen by subtracting a multiple of $h$ (or of something that grows like $h$). If $h$ is of the same or higher order than $g$ for every choice of $c$, the guess is too small.

??? question "Q6. Prove the lower bound $T(n) \ge \frac{1}{2}n^2$ for $T(n) = T(n-1) + n$, $T(1) = 1$."
    Assume $T(n-1) \ge \frac{1}{2}(n-1)^2$. Then $T(n) \ge \frac{1}{2}(n^2 - 2n + 1) + n = \frac{1}{2}n^2 + \frac{1}{2} \ge \frac{1}{2}n^2$. Base: $T(1) = 1 \ge \frac{1}{2}$.

??? question "Q7. Why is substitution needed after a recursion-tree analysis of $T(n) = T(n/3) + T(2n/3) + n$?"
    The tree analysis bounds incomplete levels by "at most $n$" and uses a heuristic for the leaf count. The induction with $T(n) \le dn\log n$ and $d \ge c/(\log 3 - 2/3)$ removes those approximations and proves the bound for all $n$.

## Complexity Summary

| Recurrence | Hypothesis that closes | Result |
|---|---|---|
| $2T(\lfloor n/2\rfloor) + n$ | $T(n) \le 2n\lg n$, $n \ge 2$ | $\Theta(n\log n)$ |
| $2T(n/2) + 1$ | $T(n) \le 2n - 1$ (strengthened) | $\Theta(n)$ |
| $2T(n-1) + 1$ | $T(n) \le 2^n - 1$ (strengthened) | $\Theta(2^n)$ |
| $T(n-1) + n$ | $\frac{1}{2}n^2 \le T(n) \le n^2$ | $\Theta(n^2)$ |
| $T(n-1) + T(n-2) + 1$ | $T(n) \le 2\varphi^n - 1$ | $\Theta(\varphi^n)$ |
| $T(n/3) + T(2n/3) + cn$ | $T(n) \le dn\lg n$, $d \ge c/(\lg 3 - 2/3)$ | $\Theta(n\log n)$ |
| $2T(\sqrt{n}) + \log n$ | change of variables | $\Theta(\log n\log\log n)$ |
| $\sqrt{n}\,T(\sqrt{n}) + n$ | normalise, change of variables | $\Theta(n\log\log n)$ |

## Key Takeaways

- Substitution = guess + strong induction; it is the rigorous method of this unit.
- The inductive step must return exactly $T(n) \le c\,g(n)$ with the same constant; "$= O(g)$" at the end is not a proof.
- Base cases fix the constants; with floors, there may be several, and $n = 1$ may be impossible for $n\log n$ bounds.
- Failure by a lower-order term: strengthen by subtracting. Failure by a higher-order term: the guess is wrong.
- Prove the lower bound separately to claim $\Theta$.
- Change of variables ($n = 2^m$) turns $\sqrt{n}$ recurrences into standard ones; remember to substitute back correctly.
- Use a ratio table under doubling to test a guess before trying to prove it.
