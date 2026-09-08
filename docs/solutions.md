# CSF302 — Unit 4 Practice Bank: **Solutions**

### Q1 — MT, merge sort

$a = 2$, $b = 2$, $f(n) = \Theta(n)$. Then $\alpha = \log_2 2 = 1$, so $n^\alpha = n$.

$$f(n) = \Theta(n) = \Theta\!\left(n^{\alpha}\right) \implies \textbf{Case 2},\; k = 0$$

$$\boxed{T(n) = \Theta(n\log n)}$$

This is **merge sort** (also maximum-subarray D&C and counting inversions — all three
share the shape $2T(n/2) + \Theta(n)$). Every level of the tree costs $\Theta(n)$ and
there are $\Theta(\log n)$ levels.

---

### Q2 — step count

- **Non-recursive portion:** one loop, $n$ iterations $\Rightarrow \Theta(n)$
- **Recurrence:** $T(n) = 2T(n/2) + n$, $T(1) = \Theta(1)$
- **MT:** $\alpha = 1$, $f(n) = n = \Theta(n) \Rightarrow$ Case 2

$$\boxed{T(n) = \Theta(n\log n)} \qquad \text{(exact count: } n\log_2 n\text{)}$$

**Position of the loop is irrelevant.** The step-count method sums *all* non-recursive
statements executed in one activation, no matter where they sit relative to the recursive
calls. Moving the loop before, between, or after the calls changes nothing in $f(n)$, so
the recurrence and the bound are identical. It would matter only if the loop's *bound*
depended on something the recursive calls changed.

---

### Q3 — recursion tree

| Level $i$ | nodes | size | cost/node | level cost |
|---|---|---|---|---|
| $0$ | $1$ | $n$ | $n$ | $n$ |
| $1$ | $4$ | $n/2$ | $n/2$ | $2n$ |
| $2$ | $16$ | $n/4$ | $n/4$ | $4n$ |
| $i$ | $4^i$ | $n/2^i$ | $n/2^i$ | $\mathbf{2^i n}$ |

- **Level cost:** $2^i n$ — an *increasing* geometric series (ratio $2$)
- **Height:** $\log_2 n$
- **Leaves:** $4^{\log_2 n} = n^{\log_2 4} = n^2$
- **Total:**

$$T(n) = \sum_{i=0}^{\log n - 1} 2^i n = n\left(2^{\log n} - 1\right) = n(n-1)$$

$$\boxed{T(n) = \Theta(n^2)}$$

The **leaf level** dominates (it alone costs $\Theta(n^2)$); the root contributes only
$\Theta(n)$.

---

### Q4 — exact count

For a fixed $i$ the inner loop runs with $j = 1, 1+i, 1+2i, \dots \le n$, i.e.
$\lceil n/i \rceil$ times:

$$\mathrm{count} = \sum_{i=1}^{n} \left\lceil \frac{n}{i} \right\rceil \approx n\sum_{i=1}^{n}\frac{1}{i} = n H_n$$

Since $H_n = \ln n + \gamma + O(1/n) = \Theta(\log n)$:

$$\boxed{\Theta(n\log n)}$$

**Not** $\Theta(n^2)$. *(Machine check: $\mathrm{count}/(n\log_2 n) \to \ln 2 \approx 0.693$.)*

---

### Q5 — substitution

**Guess:** $T(n) \le c\,n\log n$ for all $n \ge 2$.

**Inductive step** (assume the bound for $n/2$):

$$\begin{aligned}
T(n) &= 2T\!\left(\frac{n}{2}\right) + n \\
     &\le 2 \cdot c\,\frac{n}{2}\log\frac{n}{2} + n \\
     &= c\,n(\log n - 1) + n \\
     &= c\,n\log n - c\,n + n \\
     &\le c\,n\log n \qquad \text{provided } -c\,n + n \le 0,\ \text{i.e. } c \ge 1
\end{aligned}$$

**Base case:** $n = 1$ is unusable because $c \cdot 1 \cdot \log 1 = 0 < T(1)$. Start the
induction at $n_0 = 2$: with $T(1) = d$ we get $T(2) = 2d + 2$ and need
$T(2) \le c\cdot 2\log 2 = 2c$, so take $c \ge d+1$; $T(3)$ is covered by enlarging $c$
similarly.

With $c = \max(1,\, d+1)$ and $n_0 = 2$: $\;\boxed{T(n) = O(n\log n)}\;$ $\blacksquare$

---

### Q6 — binary search searching both halves

Non-recursive work is $\Theta(1)$ (one midpoint computation and comparisons), with two
recursive calls on halves:

$$T(n) = 2T\!\left(\frac{n}{2}\right) + \Theta(1)$$

MT: $\alpha = \log_2 2 = 1$; $f(n) = \Theta(1) = O\!\left(n^{1-\varepsilon}\right)$ with
$\varepsilon = 1 \Rightarrow$ **Case 1**.

$$\boxed{T(n) = \Theta(n)}$$

**What was destroyed:** binary search's whole benefit is *discarding* half the input at
every step — the decrease-and-conquer property $a = 1$. Searching both halves visits every
element, so the algorithm degenerates into a linear scan with extra overhead: the tree now
has $n$ leaves instead of a single root-to-leaf path.

---

### Q7 — telescoping

Let $n = 2^k$:

$$\begin{aligned}
T(2^k)\;   &=\; T(2^{k-1}) + 1 \\
T(2^{k-1}) &=\; T(2^{k-2}) + 1 \\
           &\;\;\vdots \\
T(2^{1})\; &=\; T(2^{0}) + 1
\end{aligned}$$

Adding all $k$ equations, every $T(2^j)$ with $0 < j < k$ appears once on each side and
cancels:

$$T(2^k) = T(1) + k = 1 + k$$

With $k = \log_2 n$: $\;T(n) = \log_2 n + 1$, so

$$\boxed{T(n) = \Theta(\log n)}$$

---

### Q8 — MT, Strassen

$a = 7$, $b = 2$, $f(n) = \Theta(n^2)$, and

$$\alpha = \log_2 7 = 2.807 \implies n^{\alpha} = n^{2.807}$$

$f(n) = n^2 = O\!\left(n^{2.807-\varepsilon}\right)$ with $\varepsilon = 0.5 \Rightarrow$ **Case 1**.

$$\boxed{T(n) = \Theta\!\left(n^{\log_2 7}\right) \approx \Theta\!\left(n^{2.807}\right)}$$

Since $2.807 < 3$, Strassen beats the $\Theta(n^3)$ definition asymptotically. The saving
comes purely from reducing the branching factor from $a = 8$ to $a = 7$ — the combine cost
stayed $\Theta(n^2)$.

---

### Q9 — step count, naive block matrix multiplication

- **Non-recursive:** $n \times n$ loops $\Rightarrow \Theta(n^2)$
- The `k` loop issues **8** recursive calls on $n/2$
- **Recurrence:** $T(n) = 8T(n/2) + n^2$
- **MT:** $\alpha = \log_2 8 = 3$; $f(n) = n^2 = O\!\left(n^{3-1}\right) \Rightarrow$ Case 1

$$\boxed{T(n) = \Theta(n^3)}$$

**Lesson:** divide and conquer *by itself* buys nothing here — splitting into quadrants
still performs $8$ half-size multiplications, which is exactly $\Theta(n^3)$, the same as
the definition. As the module notes put it, "divide and conquer does not reduce the number
of scalar multiplications"; only Strassen's algebraic trick ($8 \to 7$) changes the
exponent.

---

### Q10 — exact count

The outer loop takes $i = n, n/2, n/4, \dots, 1$, and for each the inner loop runs $i$
times:

$$\mathrm{count} = n + \frac{n}{2} + \frac{n}{4} + \dots + 1 = n\sum_{i=0}^{\log n}\left(\frac{1}{2}\right)^{i} < 2n$$

$$\boxed{\Theta(n)} \qquad \text{(machine check: } \mathrm{count}/n \to 2\text{)}$$

**Why $\Theta(n\log n)$ is wrong:** there *are* $\Theta(\log n)$ outer iterations, but the
inner loop does **not** do $\Theta(n)$ work each time — its bound shrinks geometrically.
Multiplying "number of outer iterations $\times$ largest inner cost" overcounts; you must
sum the series. Only when the inner cost is independent of the outer variable may you
multiply.

---

### Q11 — MT, Karatsuba

$a = 3$, $b = 2$, $f(n) = \Theta(n)$, and $\alpha = \log_2 3 = 1.585$.

$f(n) = n = O\!\left(n^{1.585-\varepsilon}\right)$ with $\varepsilon = 0.5 \Rightarrow$
**Case 1**.

$$\boxed{T(n) = \Theta\!\left(n^{\log_2 3}\right) \approx \Theta\!\left(n^{1.585}\right)}$$

This is **Karatsuba integer multiplication**. The $3$ is the number of half-size
multiplications kept after using the identity

$$x_1 y_0 + x_0 y_1 = (x_1 + x_0)(y_1 + y_0) - x_1 y_1 - x_0 y_0$$

which replaces four products with three; the extra additions stay $\Theta(n)$ and so do
not affect the exponent.

---

### Q12 — recursion tree

| Level $i$ | nodes | size | cost/node | level cost |
|---|---|---|---|---|
| $0$ | $1$ | $n$ | $n^2$ | $n^2$ |
| $1$ | $3$ | $n/3$ | $n^2/9$ | $n^2/3$ |
| $i$ | $3^i$ | $n/3^i$ | $n^2/9^i$ | $\mathbf{n^2(1/3)^i}$ |

- **Series:** *decreasing* geometric, ratio $1/3$
- **Height:** $\log_3 n$; **leaves:** $3^{\log_3 n} = n$, total leaf cost $\Theta(n)$
- **Total:**

$$T(n) = n^2\sum_{i=0}^{\log_3 n - 1}\left(\frac{1}{3}\right)^{i} + \Theta(n) \le \frac{3}{2}n^2$$

$$\boxed{T(n) = \Theta(n^2)}$$

The **root** dominates. MT confirms: $\alpha = 1$, $f = n^2 = \Omega(n^{1+\varepsilon})$,
regularity $3(n/3)^2 = n^2/3 \le \tfrac{1}{3}n^2$ with $c = 1/3 \Rightarrow$ Case 3.

---

### Q13 — the fallacy

The step $2 \cdot O(n/2) + n = O(n) + n = O(n)$ **hides a growing constant**. Asymptotic
notation may not be used *inside* an induction as if the constant were shared: what is
being proved must be a concrete inequality with one fixed constant.

Written properly with $T(k) \le c\,k$:

$$T(n) \le 2 \cdot c\,\frac{n}{2} + n = c\,n + n$$

and $c\,n + n \le c\,n$ is false for every $c > 0$ — the residual is $+n$, which *grows
with $n$* rather than being absorbed. Each level of the recursion adds another $n$, and
there are $\log n$ levels, so the true bound is $\Theta(n\log n)$.

**Rule:** in a substitution proof, never write $O(\cdot)$ on the right-hand side of the
inductive hypothesis; carry the explicit constant and check that the leftover term is
$\le 0$.

---

### Q14 — a hypothetical 6-multiplication method

$$T(n) = 6T\!\left(\frac{n}{2}\right) + \Theta(n^2)$$

$\alpha = \log_2 6 = 2.585$, and $f(n) = n^2 = O\!\left(n^{2.585-\varepsilon}\right)$ with
$\varepsilon = 0.5 \Rightarrow$ **Case 1**.

$$\boxed{T(n) = \Theta\!\left(n^{\log_2 6}\right) \approx \Theta\!\left(n^{2.585}\right)}$$

Compared with Strassen's $2.807$ this would be a genuine improvement — each product
removed from the $2\times2$ base case lowers the exponent, since the exponent is exactly
$\log_2 a$. (It is known that $7$ is optimal for $2 \times 2$ over a general ring, so no
such method exists; improvements below $2.807$ come from larger base blocks instead.)

---

### Q15 — step count, subtract and conquer

- **Non-recursive:** $\Theta(n)$
- **Recurrence:** $T(n) = T(n-1) + n$
- **MT does not apply:** the subproblem is $n-1$, not $n/b$ — the size shrinks
  *additively*, so there is no $b > 1$
- **Telescoping:**

$$T(n) = \sum_{i=1}^{n} i = \frac{n(n+1)}{2}$$

$$\boxed{T(n) = \Theta(n^2)}$$

---

### Q16 — telescoping

Divide by $n$ and let $S(n) = T(n)/n$:

$$\frac{T(n)}{n} = \frac{3T(n/3)}{n} + 1 = \frac{T(n/3)}{n/3} + 1 \implies S(n) = S\!\left(\frac{n}{3}\right) + 1$$

With $n = 3^k$ the chain telescopes as in Q7: $S(3^k) = S(1) + k = 1 + k$. Hence

$$T(n) = n\,S(n) = n\left(\log_3 n + 1\right)$$

$$\boxed{T(n) = \Theta(n\log n)}$$

---

### Q17 — MT with regularity

$a = 2$, $b = 2$, $f(n) = n^2$, $\alpha = 1$.

**Polynomially larger:** $n^2 = \Omega\!\left(n^{1+\varepsilon}\right)$ with
$\varepsilon = 1$ ✓

**Regularity:**

$$a\,f\!\left(\frac{n}{b}\right) = 2\left(\frac{n}{2}\right)^{2} = \frac{n^2}{2} \le c\,n^2 \quad\text{with } c = \tfrac{1}{2} < 1 \;\checkmark$$

Both Case 3 conditions hold:

$$\boxed{T(n) = \Theta(n^2)}$$

---

### Q18 — exact count

The three loops are independent, so the counts multiply:

- outer: $n$ iterations
- middle: runs while $j^2 \le n$, i.e. $\lfloor\sqrt{n}\rfloor$ iterations
- inner: $k$ doubles, i.e. $\lfloor\log_2 n\rfloor + 1$ iterations

$$\mathrm{count} = n \cdot \lfloor\sqrt{n}\rfloor \cdot \left(\lfloor\log_2 n\rfloor + 1\right)$$

$$\boxed{\Theta\!\left(n^{1.5}\log n\right)} = \Theta\!\left(n\sqrt{n}\log n\right)$$

---

### Q19 — step count with change of variable

- **Non-recursive:** $\Theta(1)$
- **Recurrence:** $T(n) = T(\sqrt{n}\,) + 1$
- Let $n = 2^m$ (so $m = \log_2 n$ and $\sqrt{n} = 2^{m/2}$) and $S(m) = T(2^m)$:

$$S(m) = S\!\left(\frac{m}{2}\right) + 1 \implies S(m) = \Theta(\log m) \quad\text{(by Q7)}$$

Substituting back $m = \log n$:

$$\boxed{T(n) = \Theta(\log\log n)}$$

---

### Q20 — MT

$a = 1$, $b = 2$, $f(n) = n$, $\alpha = \log_2 1 = 0$, so $n^{\alpha} = 1$.

$n = \Omega\!\left(n^{0+\varepsilon}\right)$ with $\varepsilon = 1$ ✓, and regularity
$1 \cdot (n/2) = n/2 \le c\,n$ with $c = \tfrac{1}{2} < 1$ ✓ $\Rightarrow$ **Case 3**.

$$\boxed{T(n) = \Theta(n)}$$

Intuition: the work halves at every level, so the total is the geometric sum
$n + n/2 + n/4 + \dots = 2n$ — the top level dominates.

---

### Q21 — recursion tree

Every complete level's subproblem sizes sum back to $n$:
$\tfrac{n}{3} + \tfrac{2n}{3} = n$, then
$\tfrac{n}{9} + \tfrac{2n}{9} + \tfrac{2n}{9} + \tfrac{4n}{9} = n$, and so on.

- **Level cost:** exactly $n$ while the level is complete ($\le n$ afterwards)
- **Shortest path:** always the $/3$ branch $\Rightarrow \log_3 n$
- **Longest path:** always the $2/3$ branch $\Rightarrow \log_{3/2} n$

$$n\log_3 n \;\le\; T(n) \;\le\; n\log_{3/2} n + O(n)$$

$$\boxed{T(n) = \Theta(n\log n)}$$

**Why the uneven split doesn't matter:** the level cost depends only on the *total* size at
that level, which any partition preserves; and both extreme path lengths are
$\Theta(\log n)$, differing only by the constant $1/\log b$, which $\Theta$ absorbs. It
would matter only if a branch shrank by a non-constant fraction (e.g. $n-1$).

---

### Q22 — parametric, $T(n) = a\,T(n/2) + \Theta(n^2)$

$\alpha = \log_2 a$, compared with the exponent $2$ of $f(n) = n^2$:

| Regime | Condition | MT case | Result |
|---|---|---|---|
| $\alpha < 2$ | $a < 4$ | Case 3, regularity $a(n/2)^2 = \tfrac{a}{4}n^2$, $c = a/4 < 1$ ✓ | $\Theta(n^2)$ |
| $\alpha = 2$ | $a = 4$ | Case 2, $k = 0$ | $\Theta(n^2\log n)$ |
| $\alpha > 2$ | $a > 4$ | Case 1 | $\Theta\!\left(n^{\log_2 a}\right)$ |

The behaviour changes at $a = 4$: below it the combine step dominates, above it the
branching dominates.

- **Strassen, $a = 7$:** $\Theta\!\left(n^{\log_2 7}\right) = \Theta\!\left(n^{2.807}\right)$
- **Naive block, $a = 8$:** $\Theta\!\left(n^{\log_2 8}\right) = \Theta(n^3)$

Every product eliminated from the $2\times2$ base case reduces the exponent, and the
combine cost is irrelevant as long as it stays $O\!\left(n^{\alpha-\varepsilon}\right)$.

---

### Q23 — step count

- **Non-recursive:** the inner loop runs $i$ times for each $i$:

$$\sum_{i=1}^{n} i = \frac{n(n+1)}{2} = \Theta(n^2)$$

- **Recurrence:** $T(n) = T(n/2) + \Theta(n^2)$
- **MT:** $\alpha = \log_2 1 = 0$; $f = \Theta(n^2) = \Omega\!\left(n^{0+2}\right)$;
  regularity $(n/2)^2 = n^2/4 \le \tfrac{1}{4}n^2$, $c = 1/4$ ✓ $\Rightarrow$ Case 3

$$\boxed{T(n) = \Theta(n^2)} \qquad \text{(exact count ratio} \to 2/3)$$

---

### Q24 — substitution

**Guess:** $T(n) \le d\,n\log n$.

$$\begin{aligned}
T(n) &\le d\,\frac{n}{4}\log\frac{n}{4} + d\,\frac{3n}{4}\log\frac{3n}{4} + cn \\
     &= d\,\frac{n}{4}(\log n - 2) + d\,\frac{3n}{4}\!\left(\log n - \log\tfrac{4}{3}\right) + cn \\
     &= d\,n\log n - d\,n\underbrace{\left[\frac{1}{2} + \frac{3}{4}\log\frac{4}{3}\right]}_{=\;\mu} + cn
\end{aligned}$$

Numerically $\tfrac{3}{4}\log_2\tfrac{4}{3} = 0.75 \times 0.415 = 0.311$, so
$\mu = 0.5 + 0.311 = 0.811 > 0$ and

$$T(n) \le d\,n\log n - \mu\,d\,n + cn \le d\,n\log n \quad\text{provided}\quad \mu\,d \ge c,\ \text{i.e. } d \ge \frac{c}{0.811} \approx 1.233\,c$$

**Where the slack comes from:** each recursive term contributes $\log(n/4) = \log n - 2$
and $\log(3n/4) = \log n - \log\tfrac{4}{3}$; those subtracted constants produce the
negative term $-\mu d n$, which is exactly what absorbs the $+cn$ of the combine step.

**Base cases:** for the constant range $1 \le n < n_0$, $T(n) = \Theta(1)$ and
$n\log n \ge 1$ for $n \ge 2$, so $d$ can be enlarged to cover them.

$$\boxed{T(n) = O(n\log n)} \qquad \blacksquare$$

---

### Q25 — MT

$a = 9$, $b = 3$, $f(n) = n^2$, $\alpha = \log_3 9 = 2$, so $n^{\alpha} = n^2$.

$$f(n) = n^2 = \Theta\!\left(n^{\alpha}\right) \implies \textbf{Case 2},\; k = 0$$

Conditions checked: $a = 9 \ge 1$ ✓; $b = 3 > 1$ ✓; $f$ asymptotically positive ✓; and
$f(n) = \Theta(n^{\alpha})$ holds with $c_1 = c_2 = 1$ since the two functions are
identical ✓. Case 2 requires no regularity condition.

$$\boxed{T(n) = \Theta(n^2\log n)}$$

---

### Q26 — exact count

$$\mathrm{count} = \sum_{i=1}^{n}\sum_{j=1}^{i}\sum_{k=1}^{j} 1 = \sum_{i=1}^{n}\sum_{j=1}^{i} j = \sum_{i=1}^{n}\frac{i(i+1)}{2} = \frac{n(n+1)(n+2)}{6} = \binom{n+2}{3}$$

$$\boxed{\Theta(n^3)} \qquad \text{(machine check: } \mathrm{count}/n^3 \to 1/6\text{)}$$

---

### Q27 — telescoping

$$\begin{aligned}
T(n)\;   &=\; T(n-1) + n \\
T(n-1)\; &=\; T(n-2) + (n-1) \\
         &\;\;\vdots \\
T(1)\;   &=\; T(0) + 1
\end{aligned}$$

Adding, all intermediate terms cancel:

$$T(n) = T(0) + \sum_{i=1}^{n} i = \frac{n(n+1)}{2}$$

$$\boxed{T(n) = \Theta(n^2)}$$

---

### Q28 — step count, Karatsuba shape

- **Non-recursive:** $\Theta(n)$
- **Recurrence:** $T(n) = 3T(n/2) + n$
- **MT:** $\alpha = \log_2 3 \approx 1.585$; $f = n = O\!\left(n^{1.585-0.5}\right) \Rightarrow$ Case 1

$$\boxed{T(n) = \Theta\!\left(n^{\log_2 3}\right) \approx \Theta\!\left(n^{1.585}\right)} \qquad \text{(machine ratio} \to 2)$$

This is the shape of **Karatsuba's algorithm**: three recursive multiplications of
half-size operands plus linear-time additions, shifts and carries.

---

### Q29 — MT gap and recursion tree

**(a) Why MT fails.** $a = 2$, $b = 2 \Rightarrow \alpha = 1$, $n^{\alpha} = n$, and
$f(n) = n/\log n$.

- Not Case 2: $\dfrac{n/\log n}{n} = \dfrac{1}{\log n} \to 0$, so $f \ne \Theta(n)$.
- Not Case 3: $f$ is *smaller* than $n$, so
  $f = \Omega\!\left(n^{1+\varepsilon}\right)$ is impossible.
- **Case 1 almost applies** — $f$ is indeed smaller than $n^{\alpha}$ — but Case 1
  requires $f(n) = O\!\left(n^{1-\varepsilon}\right)$ for a **fixed** $\varepsilon > 0$,
  i.e. smaller by a *polynomial* factor. Here $f$ is smaller only by the logarithmic
  factor $\log n$, and $n/\log n = \omega\!\left(n^{1-\varepsilon}\right)$ for every
  $\varepsilon > 0$. No valid $\varepsilon$ exists, so the recurrence sits in the **gap
  between Cases 1 and 2**.

**(b) Recursion tree.** Level $i$ has $2^i$ nodes of size $n/2^i$, each costing
$\dfrac{n/2^i}{\log(n/2^i)}$, so

$$\text{level cost} \;=\; 2^i \cdot \frac{n/2^i}{\log n - i} \;=\; \frac{n}{\log n - i}$$

Summing $i = 0, \dots, \log n - 1$ and substituting $k = \log n - i$:

$$T(n) = \sum_{k=1}^{\log n}\frac{n}{k} = n\,H_{\log n} = n\cdot\Theta(\log\log n)$$

$$\boxed{T(n) = \Theta(n\log\log n)}$$

---

### Q30 — Karatsuba by hand, $2345 \times 6789$

$n = 4$ digits, $m = 2$, so $10^m = 100$:

$$X = 2345 \Rightarrow X_1 = 23,\; X_0 = 45 \qquad Y = 6789 \Rightarrow Y_1 = 67,\; Y_0 = 89$$

Three products:

$$\begin{aligned}
P_1 &= X_1 Y_1 = 23 \times 67 = 1541 \\
P_2 &= X_0 Y_0 = 45 \times 89 = 4005 \\
(X_1+X_0)(Y_1+Y_0) &= 68 \times 156 = 10608 \\
P_3 &= 10608 - P_1 - P_2 = 10608 - 1541 - 4005 = 5062
\end{aligned}$$

Check: $X_1 Y_0 + X_0 Y_1 = 23\cdot89 + 45\cdot67 = 2047 + 3015 = 5062$ ✓

Recombination:

$$X\cdot Y = 1541\cdot10^{4} + 5062\cdot10^{2} + 4005 = 15{,}410{,}000 + 506{,}200 + 4{,}005 = \boxed{15{,}920{,}205}$$

Schoolbook check: $2345 \times 6789 = 15{,}920{,}205$ ✓

**Multiplications used: 3** half-size products (plus additions and subtractions), against
**4** for the straightforward expansion

$$X\cdot Y = X_1Y_1\cdot10^{2m} + \left(X_1Y_0 + X_0Y_1\right)\cdot10^{m} + X_0Y_0$$

That $4 \to 3$ reduction is precisely what turns $\Theta(n^2)$ into
$\Theta\!\left(n^{1.585}\right)$.

---

### Q31 — recursion tree

The two children of a node of size $n$ have sizes $n/2$ and $n/4$, so the sizes at level
$i$ sum to $n\left(\tfrac{1}{2} + \tfrac{1}{4}\right)^{i} = n\left(\tfrac{3}{4}\right)^{i}$.
Since a node's cost equals its size:

$$\text{level cost} = n\left(\frac{3}{4}\right)^{i} \quad\text{— decreasing geometric, ratio } \tfrac{3}{4}$$

$$T(n) \le n\sum_{i=0}^{\infty}\left(\frac{3}{4}\right)^{i} = \frac{n}{1 - 3/4} = 4n$$

$$\boxed{T(n) = \Theta(n)} \qquad \text{— root-dominated (machine check: } \mathrm{count}/n \to 4)$$

---

### Q32 — exact count

Each loop's variable doubles, so each runs $\lfloor\log_2 n\rfloor + 1$ times,
independently:

$$\mathrm{count} = \left(\lfloor\log_2 n\rfloor + 1\right)^{2}$$

$$\boxed{\Theta\!\left(\log^2 n\right)}$$

---

### Q33 — MT

$a = 4$, $b = 2$, $f(n) = n^2$, $\alpha = \log_2 4 = 2$.
$f(n) = n^2 = \Theta(n^{\alpha}) \Rightarrow$ **Case 2** ($k = 0$).

$$\boxed{T(n) = \Theta(n^2\log n)}$$

---

### Q34 — step count, MT gap

- **Non-recursive:** outer loop $n$ times; inner loop multiplies $j$ by $3$, so it runs
  $\lfloor\log_3 n\rfloor + 1$ times $\Rightarrow \Theta(n\log n)$
- **Recurrence:** $T(n) = 2T(n/2) + \Theta(n\log n)$
- **Why plain MT (Cases 1/2/3) does not settle it:** $\alpha = 1$; $f = n\log n$ is not
  $\Theta(n)$ (so not the basic Case 2), and it exceeds $n$ by only a logarithmic factor,
  so $f = \Omega\!\left(n^{1+\varepsilon}\right)$ fails for every $\varepsilon > 0$ (no
  Case 3). *With the general Case 2,* $f(n) = \Theta\!\left(n^{\alpha}\log^k n\right)$ with
  $k = 1$, giving $\Theta\!\left(n^{\alpha}\log^{k+1} n\right) = \Theta(n\log^2 n)$
  immediately.
- **Recursion tree:** level $i$ has $2^i$ nodes of size $n/2^i$, so

$$\text{level cost} = 2^i\cdot\frac{n}{2^i}\log\frac{n}{2^i} = n(\log n - i)$$

$$T(n) = \sum_{i=0}^{\log n - 1} n(\log n - i) = n\sum_{j=1}^{\log n} j = \frac{n\log n(\log n + 1)}{2}$$

$$\boxed{T(n) = \Theta\!\left(n\log^2 n\right)} \qquad \text{(machine ratio} \to 1/2)$$

---

### Q35 — substitution, lower bound

**Guess:** $T(n) \ge c\,n\log n$ for all $n \ge 2$, some $c > 0$.

$$\begin{aligned}
T(n) &= 2T\!\left(\frac{n}{2}\right) + n \\
     &\ge 2c\,\frac{n}{2}\log\frac{n}{2} + n \\
     &= c\,n\log n - c\,n + n \\
     &\ge c\,n\log n \qquad \text{provided } -c\,n + n \ge 0,\ \text{i.e. } c \le 1
\end{aligned}$$

So any $c \le 1$ works. **Base case:** $T(2) = 2T(1) + 2 \ge 2$ and
$c\cdot2\log 2 = 2c \le 2$ for $c \le 1$ ✓

Hence $T(n) = \Omega(n\log n)$, and with Q5:

$$\boxed{T(n) = \Theta(n\log n)} \qquad \blacksquare$$

---

### Q36 — naive four-product integer multiplication

With $m = \lfloor n/2 \rfloor$, $X = X_1 10^m + X_0$ and $Y = Y_1 10^m + Y_0$:

$$X\cdot Y = (X_1Y_1)10^{2m} + (X_1Y_0 + X_0Y_1)10^{m} + X_0Y_0$$

Four half-size products plus $\Theta(n)$ additions, shifts and carries:

$$T(n) = 4T\!\left(\frac{n}{2}\right) + \Theta(n)$$

MT: $\alpha = \log_2 4 = 2$; $f(n) = n = O\!\left(n^{2-1}\right) \Rightarrow$ Case 1.

$$\boxed{T(n) = \Theta(n^2)}$$

**Interpretation:** exactly the schoolbook bound. Recursively splitting the operands buys
**nothing** on its own — the gain comes only from Karatsuba's identity, which removes one
of the four products ($4 \to 3$, i.e. $\alpha$ from $2$ down to
$\log_2 3 \approx 1.585$). Same moral as Q9 for matrices.

---

### Q37 — telescoping

$$\begin{aligned}
T(n)\;   &=\; T(n-1) + 2^{n} \\
T(n-1)\; &=\; T(n-2) + 2^{n-1} \\
         &\;\;\vdots \\
T(1)\;   &=\; T(0) + 2^{1}
\end{aligned}$$

Adding:

$$T(n) = T(0) + \sum_{i=1}^{n} 2^{i} = 1 + \left(2^{n+1} - 2\right) = 2^{n+1} - 1$$

$$\boxed{T(n) = \Theta(2^n)}$$

The last term alone dominates the whole sum — the hallmark of a rapidly increasing
geometric series.

---

### Q38 — MT

$a = 2$, $b = 4$, $f(n) = \sqrt{n}$, and $\alpha = \log_4 2 = \tfrac{1}{2}$, so
$n^{\alpha} = n^{1/2} = \sqrt{n}$.

$f(n) = \Theta\!\left(n^{\alpha}\right) \Rightarrow$ **Case 2** ($k = 0$).

$$\boxed{T(n) = \Theta\!\left(\sqrt{n}\log n\right)}$$

Justification: $\log_4 2 = \tfrac{1}{2}$ *exactly*, so $f$ and $n^{\alpha}$ are the same
function — $f$ is neither polynomially smaller (Case 1) nor polynomially larger (Case 3).

---

### Q39 — two different counts

**(i) `if` evaluations.** The loops are independent of the condition, so the test is
reached on every pair $(i,j)$:

$$\sum_{i=1}^{n}\sum_{j=1}^{n} 1 = n^2 \implies \Theta(n^2)$$

**(ii) `count++` executions.** For a fixed $i$, the multiples of $i$ in $[1,n]$ number
$\lfloor n/i \rfloor$:

$$\sum_{i=1}^{n}\left\lfloor\frac{n}{i}\right\rfloor \approx n H_n \implies \Theta(n\log n)$$

$$\boxed{\text{if-tests: } \Theta(n^2) \qquad \texttt{count++}: \Theta(n\log n)}$$

**Lesson:** the *running time* here is $\Theta(n^2)$ — driven by the loop structure — even
though the counted event happens only $\Theta(n\log n)$ times. Always be clear about which
quantity a step-count question asks for.

---

### Q40 — step count, binary search

- **Non-recursive:** midpoint computation and a constant number of comparisons
  $\Rightarrow \Theta(1)$
- Exactly **one** recursive call, on half the range
- **Recurrence:** $T(n) = T(n/2) + \Theta(1)$
- **MT:** $\alpha = \log_2 1 = 0$, $n^{\alpha} = 1$; $f = \Theta(1) = \Theta(n^0) \Rightarrow$ Case 2 ($k = 0$)

$$\boxed{T(n) = \Theta(\log n)}$$

**Space:** $\Theta(1)$ auxiliary if written iteratively; the recursive version shown has
stack depth $\Theta(\log n)$ (one frame per level), so $\Theta(\log n)$ stack space. This
is *decrease and conquer*: $a = 1$, so only one root-to-leaf path is ever traversed.

*(Aside: the module notes' `mid = lo + (hi - lo)/2` avoids the overflow that
`(lo + hi)/2` can cause for large indices.)*

---

### Q41 — MT

$a = 5$, $b = 2$, $f(n) = n^2$, and $\alpha = \log_2 5 = 2.322$.

$f(n) = n^2 = O\!\left(n^{2.322-\varepsilon}\right)$ with $\varepsilon = 0.3 \Rightarrow$ **Case 1**.

$$\boxed{T(n) = \Theta\!\left(n^{\log_2 5}\right) \approx \Theta\!\left(n^{2.322}\right)} \qquad \text{(machine ratio} \to 4)$$

Note where this sits: a 5-multiplication $2\times2$ scheme would beat Strassen's $2.807$ —
the exponent is determined entirely by $a$.

---

### Q42 — recursion tree

| Level $i$ | nodes | size | cost/node | level cost |
|---|---|---|---|---|
| $0$ | $1$ | $n$ | $n^2$ | $n^2$ |
| $1$ | $7$ | $n/2$ | $n^2/4$ | $\tfrac{7}{4}n^2$ |
| $i$ | $7^i$ | $n/2^i$ | $n^2/4^i$ | $\mathbf{(7/4)^i n^2}$ |

- **Series:** *increasing* geometric, ratio $7/4$
- **Height:** $\log_2 n$
- **Leaves:** $7^{\log_2 n} = n^{\log_2 7} \approx n^{2.807}$
- **Total:**

$$T(n) = n^2\sum_{i=0}^{\log n - 1}\left(\frac{7}{4}\right)^{i} = n^2\cdot\frac{(7/4)^{\log n} - 1}{3/4} = \Theta\!\left(n^2 \cdot n^{\log_2 7 - 2}\right)$$

$$\boxed{T(n) = \Theta\!\left(n^{\log_2 7}\right) \approx \Theta\!\left(n^{2.807}\right)}$$

The **leaf level** dominates: the recursive multiplications, not the $\Theta(n^2)$
additions, set the bound.

---

### Q43 — a failing guess, then the right one

**Attempt $T(n) \le c\,n$:**

$$T(n) \le 4c\,\frac{n}{2} + n = 2c\,n + n = c\,n + \underbrace{(c\,n + n)}_{>\,0}$$

Closing the induction needs $c\,n + n \le 0$, i.e. $c \le -1$ — impossible for $c > 0$.
The residual $(c+1)n$ **grows with $n$**, so no constant can absorb it. Structurally:
halving the size divides a node's cost by $2$ while the branching multiplies it by $4$, so
the recursion *gains* a factor of $2$ per level.

**Correct bound.** MT: $\alpha = \log_2 4 = 2$, $f = n = O\!\left(n^{2-1}\right) \Rightarrow$ Case 1 $\Rightarrow \Theta(n^2)$.

**Proof of $O(n^2)$ with the guess $T(n) \le c\,n^2 - b\,n$:**

$$\begin{aligned}
T(n) &\le 4\left[c\left(\frac{n}{2}\right)^{2} - b\,\frac{n}{2}\right] + n \\
     &= c\,n^2 - 2b\,n + n \\
     &= c\,n^2 - b\,n - (b\,n - n) \\
     &\le c\,n^2 - b\,n \qquad \text{provided } b \ge 1
\end{aligned}$$

**Base case:** with $T(1) = d$ we need $d \le c - b$; take $b = 1$ and $c \ge d+1$. Hence
$T(n) \le c\,n^2 - n = O(n^2)$, and the $n^2$ leaves give the matching $\Omega(n^2)$:

$$\boxed{T(n) = \Theta(n^2)} \qquad \blacksquare$$

The subtracted $-b\,n$ term is the standard device for supplying slack when the plain guess
leaves a positive leftover.

---

### Q44 — Toom–Cook

Three-way split ($b = 3$), five multiplications ($a = 5$), linear combination:

$$T(n) = 5T\!\left(\frac{n}{3}\right) + \Theta(n)$$

$$\alpha = \log_3 5 = \frac{\ln 5}{\ln 3} = \frac{1.6094}{1.0986} = 1.465$$

$f(n) = n = O\!\left(n^{1.465-0.4}\right) \Rightarrow$ **Case 1**.

$$\boxed{T(n) = \Theta\!\left(n^{\log_3 5}\right) \approx \Theta\!\left(n^{1.465}\right)}$$

This matches the $O\!\left(n^{1.465}\right)$ quoted for Toom–Cook (1963) in the module's
timeline, and improves on Karatsuba's $1.585$ — again purely by lowering
$\alpha = \log_b a$, this time by increasing $b$ rather than decreasing $a$.

---

### Q45 — step count, exponential

- **Non-recursive:** $\Theta(1)$
- **Recurrence:** $T(n) = 2T(n-1) + 1$, $T(1) = 0$
- **MT does not apply** (subtract-and-conquer, no $b > 1$)
- **Iteration:**

$$T(n) = 1 + 2 + 4 + \dots + 2^{n-2} = 2^{n-1} - 1$$

$$\boxed{T(n) = \Theta(2^n)}$$

This is the naive-Fibonacci pitfall from the module notes: overlapping subproblems solved
repeatedly. Note how little the body matters — $\Theta(1)$ work per call still yields
exponential time, because the *branching* is applied to a size that shrinks only by $1$.

---

### Q46 — exact count

The outer variable takes $i = 1, 2, 4, \dots, 2^{\lfloor\log_2 n\rfloor}$, and the inner
loop runs $i$ times:

$$\mathrm{count} = 1 + 2 + 4 + \dots + 2^{\lfloor\log_2 n\rfloor} = 2^{\lfloor\log_2 n\rfloor + 1} - 1 \approx 2n$$

$$\boxed{\Theta(n)} \qquad \text{(machine check: } \mathrm{count}/n \to 2\text{)}$$

The trap is the same as Q10: $\Theta(\log n)$ outer iterations, but the inner cost grows
geometrically, so the **last** iteration alone accounts for half the total.

---

### Q47 — change of variable

Let $n = 2^m$, so $m = \log_2 n$ and $\sqrt{n} = 2^{m/2}$. Put $S(m) = T(2^m)$:

$$T(n) = T(\sqrt{n}\,) + 1 \implies S(m) = S\!\left(\frac{m}{2}\right) + 1$$

By Q7, $S(m) = \Theta(\log m)$. Substituting $m = \log n$:

$$\boxed{T(n) = \Theta(\log\log n)}$$

*Sanity check:* from $n = 65536$ the sizes go $65536 \to 256 \to 16 \to 4 \to 2$, i.e. $4$
steps, and $\log_2\log_2 65536 = \log_2 16 = 4$ ✓

---

### Q48 — telescoping

Divide by $n$ and set $S(n) = T(n)/n$:

$$\frac{T(n)}{n} = \frac{2T(n/2)}{n} + \log n = \frac{T(n/2)}{n/2} + \log n \implies S(n) = S\!\left(\frac{n}{2}\right) + \log n$$

With $n = 2^k$, so $S(2^k) = S(2^{k-1}) + k$:

$$\begin{aligned}
S(2^k)\;   &=\; S(2^{k-1}) + k \\
S(2^{k-1}) &=\; S(2^{k-2}) + (k-1) \\
           &\;\;\vdots \\
S(2^{1})\; &=\; S(2^{0}) + 1
\end{aligned}$$

Adding:

$$S(2^k) = S(1) + \sum_{j=1}^{k} j = S(1) + \frac{k(k+1)}{2} = \Theta\!\left(\log^2 n\right)$$

$$\boxed{T(n) = n\,S(n) = \Theta\!\left(n\log^2 n\right)} \qquad \text{(machine ratio} \to 1/2)$$

---

### Q49 — merge sort with a $\Theta(n\log n)$ merge

$$T(n) = 2T\!\left(\frac{n}{2}\right) + \Theta(n\log n)$$

$\alpha = 1$ and $f(n) = \Theta\!\left(n^{1}\log^{1} n\right)$, so the general Case 2
applies with $k = 1$:

$$\boxed{T(n) = \Theta\!\left(n\log^2 n\right)}$$

The algorithm has been degraded by a factor of $\log n$ relative to $\Theta(n\log n)$. It
is still far better than $\Theta(n^2)$ — but no longer optimal for comparison sorting
(Q89).

---

### Q50 — step count

- **Non-recursive:** for each $i$ the inner loop runs from $i$ to $n$, i.e. $n - i + 1$
  times:

$$\sum_{i=1}^{n}(n - i + 1) = \frac{n(n+1)}{2} = \Theta(n^2)$$

- **Recurrence:** $T(n) = 2T(n/2) + \Theta(n^2)$
- **MT:** $\alpha = 1$; $f = \Theta(n^2) = \Omega\!\left(n^{1+1}\right)$; regularity
  $2(n/2)^2 = n^2/2 \le \tfrac{1}{2}n^2$, $c = 1/2$ ✓ $\Rightarrow$ Case 3

$$\boxed{T(n) = \Theta(n^2)}$$

Compare with Q2: the same branching, but a quadratic body makes the **root** dominate
instead of every level contributing equally.

---

### Q51 — MT

$a = 16$, $b = 4$, $f(n) = n^2$, $\alpha = \log_4 16 = 2$.
$f(n) = \Theta(n^{\alpha}) \Rightarrow$ **Case 2** ($k = 0$).

$$\boxed{T(n) = \Theta(n^2\log n)}$$

---

### Q52 — exact count

$$\mathrm{count} = \sum_{i=1}^{n} i^{2} = \frac{n(n+1)(2n+1)}{6}$$

$$\boxed{\Theta(n^3)} \qquad \text{(machine check: } \mathrm{count}/n^3 \to 1/3\text{)}$$

---

### Q53 — recursion tree

Level $i$ has $2^i$ nodes of size $n/2^i$, each costing
$\dfrac{n}{2^i}\log\dfrac{n}{2^i}$:

$$\text{level cost} = 2^i \cdot \frac{n}{2^i}\log\frac{n}{2^i} = n(\log n - i)$$

The level costs decrease *linearly*, not geometrically, so no single level dominates:

$$T(n) = \sum_{i=0}^{\log n - 1} n(\log n - i) = n\sum_{j=1}^{\log n} j = \frac{n\log n(\log n + 1)}{2}$$

$$\boxed{T(n) = \Theta\!\left(n\log^2 n\right)}$$

---

### Q54 — substitution, Karatsuba

Write $\beta = \log_2 3$ and note $2^{\beta} = 3$, hence
$\left(\tfrac{n}{2}\right)^{\beta} = \tfrac{n^{\beta}}{3}$.

**Guess:** $T(n) \le d\,n^{\beta} - e\,n$.

$$\begin{aligned}
T(n) &\le 3\left[d\left(\frac{n}{2}\right)^{\beta} - e\,\frac{n}{2}\right] + cn \\
     &= 3\left[\frac{d\,n^{\beta}}{3} - \frac{e\,n}{2}\right] + cn \\
     &= d\,n^{\beta} - \frac{3}{2}e\,n + cn \\
     &= d\,n^{\beta} - e\,n - \left(\frac{1}{2}e\,n - c\,n\right) \\
     &\le d\,n^{\beta} - e\,n \qquad \text{provided } \tfrac{1}{2}e \ge c,\ \text{i.e. } e \ge 2c
\end{aligned}$$

**What the $-e\,n$ term is for:** with the plain guess $T(n) \le d\,n^{\beta}$ the algebra
gives $d\,n^{\beta} + cn$, and the leftover $+cn$ cannot be absorbed however large $d$ is
(it is *lower order* than $n^{\beta}$, so it never gets multiplied away). Subtracting
$e\,n$ creates a negative $\Theta(n)$ term of exactly the right order to cancel it.

**Base case:** for small $n$, $T(n) = \Theta(1)$ and $d$ can be enlarged (with $e$ fixed at
$2c$) so that $d\,n^{\beta} - e\,n \ge T(n)$ over the finite range.

$$\boxed{T(n) = O\!\left(n^{\log_2 3}\right)} \qquad \blacksquare$$

---

### Q55 — merge sort with a $1 : (n-1)$ split

Sorting a 1-element piece is free; the other recursive call has size $n-1$; merging a
1-element list with an $(n-1)$-element list is $\Theta(n)$:

$$T(n) = T(n-1) + \Theta(n)$$

Telescoping:

$$T(n) = \sum_{i=1}^{n}\Theta(i) = \Theta\!\left(\frac{n(n+1)}{2}\right)$$

$$\boxed{T(n) = \Theta(n^2)}$$

This is exactly **insertion sort** (repeatedly inserting one element into a sorted list).
It is the "unequal splits ($1$ vs $n-1$) $\Rightarrow \Theta(n^2)$ degradation" pitfall
from the module notes: the balance of the split, not the merge, is what earns merge sort
its $\log n$.

---

### Q56 — step count

- **Non-recursive:** $\Theta(n)$
- **Recurrence:** $T(n) = 4T(n/2) + n$
- **MT:** $\alpha = \log_2 4 = 2$; $f = n = O\!\left(n^{2-1}\right) \Rightarrow$ Case 1

$$\boxed{T(n) = \Theta(n^2)}$$

Dominated by the $n^2$ leaves (see Q3).

---

### Q57 — MT with regularity

$a = 3$, $b = 4$, $f(n) = n\log n$, and
$\alpha = \log_4 3 = \dfrac{\ln 3}{\ln 4} \approx 0.792$.

**Polynomially larger:** $n\log n \ge n = \Omega\!\left(n^{0.792+\varepsilon}\right)$ with
$\varepsilon = 0.2$ (since $0.792 + 0.2 = 0.992 < 1$) ✓

**Regularity:**

$$a\,f\!\left(\frac{n}{b}\right) = 3\cdot\frac{n}{4}\log\frac{n}{4} = \frac{3n}{4}(\log n - 2) \le \frac{3}{4}\,n\log n \quad\text{so } c = \tfrac{3}{4} < 1 \;\checkmark$$

$\Rightarrow$ **Case 3**:

$$\boxed{T(n) = \Theta(n\log n)}$$

---

### Q58 — exact count

- outer: $i$ runs from $n/2$ to $n$, i.e. $\left(\tfrac{n}{2} + 1\right)$ iterations
- middle: $\tfrac{n}{2}$ iterations, independent of $i$
- inner: $l$ doubles, i.e. $\lfloor\log_2 n\rfloor + 1$ iterations

$$\mathrm{count} = \left(\frac{n}{2}+1\right)\cdot\frac{n}{2}\cdot\left(\lfloor\log_2 n\rfloor + 1\right) \approx \frac{n^2}{4}\log_2 n$$

$$\boxed{\Theta\!\left(n^2\log n\right)} \qquad \text{(machine ratio} \to 1/4)$$

---

### Q59 — iteration

$$T(n) = n\,T(n-1) = n(n-1)T(n-2) = \dots = n(n-1)(n-2)\cdots 2 \cdot T(1)$$

$$\boxed{T(n) = n!\;=\;\Theta(n!)}$$

This grows *much* faster than $2^n$: by Stirling,

$$n! \approx \sqrt{2\pi n}\left(\frac{n}{e}\right)^{n} \implies \frac{n!}{2^{n}} \to \infty$$

(the ratio of consecutive terms is $n$ for $n!$ against $2$ for $2^n$). Note this
recurrence is multiplicative, so it does not telescope by addition — you telescope the
*product* instead.

---

### Q60 — MT with regularity

$a = 7$, $b = 3$, $f(n) = n^2$, and
$\alpha = \log_3 7 = \dfrac{1.9459}{1.0986} \approx 1.771$.

**Polynomially larger:** $n^2 = \Omega\!\left(n^{1.771+\varepsilon}\right)$ with
$\varepsilon = 0.2$ ✓

**Regularity:**

$$7\left(\frac{n}{3}\right)^{2} = \frac{7}{9}n^2 \le c\,n^2 \quad\text{with } c = \tfrac{7}{9} \approx 0.778 < 1 \;\checkmark$$

$\Rightarrow$ **Case 3**:

$$\boxed{T(n) = \Theta(n^2)} \qquad \text{(machine ratio} \to 4.5 = \tfrac{1}{1-7/9})$$

---

### Q61 — mutual recursion

Let $F(n)$ and $G(n)$ be the costs of `f` and `g`. Each does $\Theta(n)$ non-recursive
work and calls the other on $n/2$:

$$F(n) = n + G\!\left(\frac{n}{2}\right), \qquad G(n) = n + F\!\left(\frac{n}{2}\right)$$

Substituting the second into the first eliminates $G$:

$$F(n) = n + \frac{n}{2} + F\!\left(\frac{n}{4}\right) = F\!\left(\frac{n}{4}\right) + \frac{3n}{2}$$

MT: $a = 1$, $b = 4$, $\alpha = \log_4 1 = 0$; $f = \tfrac{3}{2}n = \Omega\!\left(n^{0+1}\right)$; regularity
$\tfrac{3}{2}\cdot\tfrac{n}{4} = \tfrac{3}{8}n \le \tfrac{1}{4}\cdot\tfrac{3}{2}n$ ✓ with
$c = \tfrac{1}{4}$ $\Rightarrow$ Case 3.

$$\boxed{F(n) = \Theta(n)} \qquad \text{(machine ratio} \to 2,\ \text{i.e. } F(n) \approx 2n)$$

**Method:** with mutual recursion, always unroll one function into the other first to get a
single-function recurrence; the effective shrink factor becomes $b^2$ (here $4$), not $b$.

---

### Q62 — two split-sum regimes

**(a)** $T(n) = T(n/5) + T(7n/10) + n$. The child sizes at level $i$ sum to
$n\left(\tfrac{1}{5} + \tfrac{7}{10}\right)^{i} = n\left(\tfrac{9}{10}\right)^{i}$, and a
node's cost equals its size, so

$$\text{level cost} = n\left(\frac{9}{10}\right)^{i}, \qquad T(n) \le n\sum_{i=0}^{\infty}\left(\frac{9}{10}\right)^{i} = \frac{n}{1 - 9/10} = 10n$$

$$\boxed{T(n) = \Theta(n)} \qquad \text{— root-dominated}$$

This linearity is exactly why median-of-medians gives worst-case $\Theta(n)$ selection.

**(b)** $T(n) = T(n/3) + T(2n/3) + n$. Here $\tfrac{1}{3} + \tfrac{2}{3} = 1$, so **every
complete level costs exactly $n$**, and the tree has $\Theta(\log n)$ levels (between
$\log_3 n$ and $\log_{3/2} n$):

$$\boxed{T(n) = \Theta(n\log n)}$$

**The rule.** For $T(n) = \sum_i T(\alpha_i n) + \Theta(n)$ with constants
$\alpha_i \in (0,1)$:

| $\sum_i \alpha_i$ | Behaviour | Result |
|---|---|---|
| $< 1$ | level costs decay geometrically | $\Theta(n)$ |
| $= 1$ | every level costs $\Theta(n)$ | $\Theta(n\log n)$ |
| $> 1$ | level costs grow geometrically | $\Theta(n^p)$, $p > 1$ (Akra–Bazzi) |

The *number* of subproblems and the balance of the split matter far less than whether the
fractions sum to less than $1$.

---

### Q63 — recursion tree

| Level $i$ | nodes | size | cost/node | level cost |
|---|---|---|---|---|
| $0$ | $1$ | $n$ | $n^2$ | $n^2$ |
| $1$ | $3$ | $n/4$ | $n^2/16$ | $\tfrac{3}{16}n^2$ |
| $i$ | $3^i$ | $n/4^i$ | $n^2/16^i$ | $\mathbf{(3/16)^i n^2}$ |

- **Ratio:** $\tfrac{3}{16}$ — a *decreasing* geometric series
- **Height:** $\log_4 n$; **leaves:** $3^{\log_4 n} = n^{\log_4 3} \approx n^{0.792}$
- **Total:**

$$T(n) = n^2\sum_{i=0}^{\log_4 n - 1}\left(\frac{3}{16}\right)^{i} \le n^2\cdot\frac{16}{13} \approx 1.23\,n^2$$

$$\boxed{T(n) = \Theta(n^2)}$$

The **root** dominates; the leaves contribute only $\Theta\!\left(n^{0.792}\right)$.
*(Machine ratio $\to 1.23$ ✓)*

---

### Q64 — exact count

$$\mathrm{count} = \sum_{i=1}^{n}(n - i + 1) = n + (n-1) + \dots + 1 = \frac{n(n+1)}{2}$$

$$\boxed{\Theta(n^2)}$$

Half the iterations of a full double loop — the same order.

---

### Q65 — MT, general Case 2

$a = 4$, $b = 2$, $f(n) = n^2\log n$, $\alpha = \log_2 4 = 2$.

$$f(n) = n^2\log n = \Theta\!\left(n^{\alpha}\log^{k} n\right) \text{ with } k = 1 \implies T(n) = \Theta\!\left(n^{\alpha}\log^{k+1} n\right)$$

$$\boxed{T(n) = \Theta\!\left(n^2\log^2 n\right)} \qquad \text{(machine ratio} \to 1/2)$$

---

### Q66 — step count

- **Non-recursive:** $n \times n$ loops $\Rightarrow \Theta(n^2)$
- The `k` loop issues **16** recursive calls on $n/4$
- **Recurrence:** $T(n) = 16\,T(n/4) + n^2$
- **MT:** $\alpha = \log_4 16 = 2$; $f = n^2 = \Theta(n^2) \Rightarrow$ Case 2

$$\boxed{T(n) = \Theta(n^2\log n)} \qquad \text{(machine ratio} \to 1/2)$$

The balanced case: $16$ subproblems of a quarter the size each do a sixteenth of the work,
so every level costs $\Theta(n^2)$.

---

### Q67 — substitution

**Guess:** $T(n) \le c\log n$ for $n \ge 2$.

$$\begin{aligned}
T(n) &= T\!\left(\frac{n}{2}\right) + 1 \\
     &\le c\log\frac{n}{2} + 1 \\
     &= c\log n - c + 1 \\
     &\le c\log n \qquad \text{provided } -c + 1 \le 0,\ \text{i.e. } c \ge 1
\end{aligned}$$

**Why the base case cannot be $n = 1$:** $\log 1 = 0$, so the claimed bound at $n = 1$ is
$T(1) \le 0$, contradicting $T(1) = \Theta(1) > 0$. No choice of $c$ can fix this — the
bound function *vanishes* at $n = 1$.

**What to do instead:** asymptotic statements need only hold for $n \ge n_0$, so start the
induction at $n_0 = 2$ and treat $n = 1$ as part of the finite base range. With $T(1) = d$
we need $T(2) = d + 1 \le c\log 2 = c$, so take $c = \max(1,\, d+1)$.

$$\boxed{T(n) = O(\log n)} \qquad \blacksquare$$

---

### Q68 — clumsy Strassen

$$T(n) = 7T\!\left(\frac{n}{2}\right) + \Theta\!\left(n^2\log n\right)$$

$\alpha = \log_2 7 \approx 2.807$. Is $f(n) = n^2\log n = O\!\left(n^{2.807-\varepsilon}\right)$? Yes — take $\varepsilon = 0.5$, since
$n^2\log n = O\!\left(n^{2.307}\right)$ ✓ $\Rightarrow$ **Case 1**.

$$\boxed{T(n) = \Theta\!\left(n^{\log_2 7}\right) \approx \Theta\!\left(n^{2.807}\right) \quad \text{— unchanged}}$$

**What this tells you:** in a divide-and-conquer algorithm sitting in Case 1, the exponent
is determined **entirely by the branching structure** ($a$ and $b$), i.e. by the number of
leaves $n^{\log_b a}$. The combine step is invisible asymptotically as long as it stays
polynomially smaller than $n^{\alpha}$. Making the additions $\log n$ times more expensive
costs a constant-factor slowdown in practice and nothing at all asymptotically — whereas
removing one multiplication ($a = 7 \to 6$) would change the exponent itself (Q14).

---

### Q69 — telescoping

$$\begin{aligned}
T(n)\;   &=\; T(n-1) + \tfrac{1}{n} \\
T(n-1)\; &=\; T(n-2) + \tfrac{1}{n-1} \\
         &\;\;\vdots \\
T(2)\;   &=\; T(1) + \tfrac{1}{2}
\end{aligned}$$

Adding:

$$T(n) = T(1) + \sum_{i=2}^{n}\frac{1}{i} = 1 + (H_n - 1) = H_n$$

Since $H_n = \ln n + \gamma + O(1/n)$:

$$\boxed{T(n) = \Theta(\log n)}$$

---

### Q70 — MT

$a = 2$, $b = 2$, $f(n) = \sqrt{n}$, $\alpha = \log_2 2 = 1$.

$$f(n) = n^{1/2} = O\!\left(n^{1-\varepsilon}\right) \text{ with } \varepsilon = \tfrac{1}{2} \implies \textbf{Case 1}$$

$$\boxed{T(n) = \Theta(n)}$$

The $n$ leaves dominate: sub-linear combine work cannot compete with the branching.

---

### Q71 — two fragments

**Fragment A:** the loop runs while $i^2 \le n$, i.e. $i \le \sqrt{n}$, so
$\mathrm{count} = \lfloor\sqrt{n}\rfloor$:

$$\boxed{\Theta(\sqrt{n})}$$

**Fragment B:** $m$ takes $n, n/2, n/4, \dots, 2$, so
$\mathrm{count} = \lfloor\log_2 n\rfloor$:

$$\boxed{\Theta(\log n)}$$

Worth contrasting: `i++` with a bound of $\sqrt{n}$ gives $\Theta(\sqrt{n})$; *dividing*
the variable gives $\Theta(\log n)$. The update rule matters more than the bound.

---

### Q72 — step count

- **Non-recursive:** the loop bound is the **constant** $100$, so this is $\Theta(1)$, not
  $\Theta(n)$ — a constant number of iterations never contributes a factor of $n$
- **Recurrence:** $T(n) = T(n/2) + \Theta(1)$
- **MT:** $\alpha = \log_2 1 = 0$; $f = \Theta(1) = \Theta(n^0) \Rightarrow$ Case 2
  ($k = 0$)

$$\boxed{T(n) = \Theta(\log n)} \qquad \text{(exact count: } 100\log_2 n\text{)}$$

---

### Q73 — Strassen by hand

$$A_{11} = 2,\; A_{12} = 4,\; A_{21} = 5,\; A_{22} = 3; \qquad B_{11} = 1,\; B_{12} = 7,\; B_{21} = 6,\; B_{22} = 2$$

| product | expression | value |
|---|---|---|
| $m_1$ | $(A_{11}+A_{22})(B_{11}+B_{22}) = (2+3)(1+2) = 5\times3$ | $15$ |
| $m_2$ | $B_{11}(A_{21}+A_{22}) = 1\times(5+3)$ | $8$ |
| $m_3$ | $A_{11}(B_{12}-B_{22}) = 2\times(7-2)$ | $10$ |
| $m_4$ | $A_{22}(B_{21}-B_{11}) = 3\times(6-1)$ | $15$ |
| $m_5$ | $B_{22}(A_{11}+A_{12}) = 2\times(2+4)$ | $12$ |
| $m_6$ | $(A_{21}-A_{11})(B_{11}+B_{12}) = (5-2)(1+7) = 3\times8$ | $24$ |
| $m_7$ | $(A_{12}-A_{22})(B_{21}+B_{22}) = (4-3)(6+2) = 1\times8$ | $8$ |

Assembly:

$$\begin{aligned}
C_{11} &= m_1 + m_4 - m_5 + m_7 = 15 + 15 - 12 + 8 = 26 \\
C_{12} &= m_3 + m_5 = 10 + 12 = 22 \\
C_{21} &= m_2 + m_4 = 8 + 15 = 23 \\
C_{22} &= m_1 + m_3 - m_2 + m_6 = 15 + 10 - 8 + 24 = 41
\end{aligned}$$

$$\boxed{C = \begin{pmatrix} 26 & 22 \\ 23 & 41 \end{pmatrix}}$$

Direct verification:

$$\begin{aligned}
C_{11} &= 2\cdot1 + 4\cdot6 = 26 \;\checkmark & C_{12} &= 2\cdot7 + 4\cdot2 = 22 \;\checkmark \\
C_{21} &= 5\cdot1 + 3\cdot6 = 23 \;\checkmark & C_{22} &= 5\cdot7 + 3\cdot2 = 41 \;\checkmark
\end{aligned}$$

**Multiplications: 7** (against $8$ for the definition), at the cost of $18$ additions and
subtractions instead of $4$. For $2\times2$ scalars this is a *worse* trade; the benefit
appears only when the entries are $\tfrac{n}{2}\times\tfrac{n}{2}$ blocks, because then
each saved multiplication saves $\Theta\!\left(n^{2.807}\right)$ work while the extra
additions cost only $\Theta(n^2)$.

---

### Q74 — does the Master Theorem apply?

| | Verdict | Reason |
|---|---|---|
| (a) $T(n) = 2T(n-1) + n$ | **No** | Not of the form $aT(n/b)$: the size shrinks *additively*, so there is no $b > 1$. Subtract-and-conquer — use iteration/telescoping. *(Answer: $\Theta(2^n)$.)* |
| (b) $T(n) = \tfrac{1}{2}T(n/2) + n$ | **No** | Violates $a \ge 1$: $a = \tfrac{1}{2}$ means "half a subproblem", outside the theorem's hypotheses. |
| (c) $T(n) = 64T(n/8) - n^2\log n$ | **No** | Violates the requirement that $f(n)$ be **asymptotically positive**; here $f(n) = -n^2\log n < 0$. |
| (d) $T(n) = 2^{n}T(n/2) + n^{n}$ | **No** | $a$ must be a **constant**; here $a = 2^n$ depends on $n$ (and $f$ is not of the required form). |
| (e) $T(n) = 2T(n/2) + n/\log n$ | **No** | Correct *form*, but $f$ falls in the **gap between Cases 1 and 2**: smaller than $n^{\alpha} = n$ by only a log factor, so no $\varepsilon > 0$ satisfies $f = O\!\left(n^{1-\varepsilon}\right)$. *(Answer: $\Theta(n\log\log n)$ — Q29.)* |
| (f) $T(n) = T(n/2) + T(n/4) + n$ | **No** | Two **different** subproblem sizes — not a single $aT(n/b)$ term. Use a recursion tree or Akra–Bazzi. *(Answer: $\Theta(n)$ — Q31.)* |

---

### Q75 — recursion tree of $T(n) = T(n-1) + n$

- **Shape:** a single **chain** (path), not a branching tree — one node per level
- **Branching factor:** $a = 1$, so each level has exactly one node
- **Height:** $n$ levels (sizes $n, n-1, \dots, 1$), *not* $\Theta(\log n)$
- **Level cost:** the node at depth $i$ has size $n - i$, so its cost is $n - i$
- **Total:**

$$T(n) = \sum_{i=0}^{n-1}(n-i) = \frac{n(n+1)}{2}$$

$$\boxed{T(n) = \Theta(n^2)}$$

**Why a chain:** branching in a recursion tree comes from $a \ge 2$. Here $a = 1$, so there
is never more than one child. The quadratic total comes from the *height* ($n$ instead of
$\log n$), which is what an additive size reduction costs you — the same reason Q55
degenerates.

---

### Q76 — step count, Strassen

- **Non-recursive:** $n \times n$ loops $\Rightarrow \Theta(n^2)$ (the block additions and
  subtractions)
- The `k` loop issues **7** recursive calls on $n/2$
- **Recurrence:** $T(n) = 7T(n/2) + n^2$
- **MT:** $\alpha = \log_2 7 = 2.807$; $f = n^2 = O\!\left(n^{2.807-0.5}\right) \Rightarrow$ Case 1

$$\boxed{T(n) = \Theta\!\left(n^{\log_2 7}\right) \approx \Theta\!\left(n^{2.807}\right)}$$

---

### Q77 — exact count

For each of the $n$ outer iterations the inner `while` halves $j$ from $n$ down to $2$,
running $\lfloor\log_2 n\rfloor$ times, and the inner cost does **not** depend on $i$:

$$\mathrm{count} = n\cdot\lfloor\log_2 n\rfloor$$

$$\boxed{\Theta(n\log n)} \qquad \text{(machine ratio} \to 1)$$

Contrast with Q4 and Q10, where the inner bound *did* depend on the outer variable and
multiplying was invalid.

---

### Q78 — substitution

**For $T(n) = 2T(n/2) + n^2$, guess $T(n) \le c\,n^2$:**

$$\begin{aligned}
T(n) &\le 2c\left(\frac{n}{2}\right)^{2} + n^2 \\
     &= \frac{c\,n^2}{2} + n^2 \\
     &\le c\,n^2 \qquad \text{provided } n^2 \le \frac{c\,n^2}{2},\ \text{i.e. } c \ge 2
\end{aligned}$$

So $c = 2$ closes the induction (base case: enlarge $c$ to cover the constant range).

$$\boxed{T(n) = O(n^2)} \qquad \blacksquare$$

**Why the plain guess fails for $T(n) = 2T(n/2) + n$:**

$$T(n) \le 2c\,\frac{n}{2} + n = c\,n + n > c\,n \quad \text{for every } c > 0$$

The leftover is $+n$, of exactly the same order as the bound itself, so it can never be
absorbed. Structurally: with $f(n) = n^2$ the level costs *shrink* geometrically
($n^2, n^2/2, n^2/4, \dots$), so the sum is a constant multiple of the root — a bound of
the same order as $f$ is achievable. With $f(n) = n$ every level costs the same $n$, so
$\log n$ levels give $\Theta(n\log n)$ and no linear bound can hold. In MT terms: Case 3
versus Case 2.

---

### Q79 — when telescoping works

**$T(n) = 4T(n/4) + cn$ telescopes.** Divide by $n$:

$$\frac{T(n)}{n} = \frac{4T(n/4)}{n} + c = \frac{T(n/4)}{n/4} + c \implies S(n) = S\!\left(\frac{n}{4}\right) + c$$

— a single recursive term. Each unrolled equation then contributes exactly one term that
cancels against the next, so the chain collapses to $S(n) = S(1) + c\log_4 n$, giving
$T(n) = \Theta(n\log n)$.

**$T(n) = T(n/2) + T(n/4) + n$ does not.** Unrolling once gives two *different*
subproblems ($n/2$, $n/4$); unrolling those gives four ($n/4, n/8, n/8, n/16$), and so on.
The right-hand terms never match the left-hand side of a single earlier equation, so
nothing cancels — you get a branching tree of terms, not a linear chain.

**Structural property required:** the recurrence must reduce to a **linear chain with one
recursive term**, i.e. the form $S(n) = S(n/b) + g(n)$, possibly after dividing through by
a suitable function. Several recursive calls of *differing* sizes destroy the
one-in/one-out cancellation.

**Use instead:** a **recursion tree** (sum level by level) or the **Akra–Bazzi method**;
substitution also works if you can guess the bound. Here the tree gives $\Theta(n)$, since
the level costs are $n(3/4)^i$ (Q31).

---

### Q80 — change of variable, then MT

Let $n = 2^m$ (so $m = \log_2 n$), giving $\sqrt{n} = 2^{m/2}$ and $\log n = m$. Put
$S(m) = T(2^m)$:

$$T(n) = 2T(\sqrt{n}\,) + \log n \implies S(m) = 2S\!\left(\frac{m}{2}\right) + m$$

MT on $S$: $a = 2$, $b = 2$, $\alpha = \log_2 2 = 1$; $f(m) = m = \Theta(m) \Rightarrow$
Case 2, so $S(m) = \Theta(m\log m)$. Substituting $m = \log n$:

$$\boxed{T(n) = \Theta(\log n \cdot \log\log n)} \qquad \text{(machine ratio} \to 1)$$

---

### Q81 — the value of a balanced partition

**(a)** $T(n) = T(n/10) + T(9n/10) + \Theta(n)$. The split fractions sum to
$\tfrac{1}{10} + \tfrac{9}{10} = 1$, so every complete level costs $\Theta(n)$. The
shortest root-to-leaf path is $\log_{10} n$ and the longest is $\log_{10/9} n$, both
$\Theta(\log n)$:

$$n\log_{10} n \;\le\; T(n) \;\le\; n\log_{10/9} n + O(n) \implies \boxed{T(n) = \Theta(n\log n)}$$

**(b)** $T(n) = T(n-1) + \Theta(n)$. The tree is a chain of height $n$ with level cost
$n - i$:

$$T(n) = \sum_{i=1}^{n}\Theta(i) \implies \boxed{T(n) = \Theta(n^2)}$$

**What the comparison shows:** a partition may be *badly* unbalanced — $10 : 90$, even
$1 : 99$ — and quicksort still runs in $\Theta(n\log n)$, because what matters is only that
each side is a **constant fraction** of $n$, which keeps the height at $\Theta(\log n)$
(the constant $1/\log(10/9)$ is absorbed by $\Theta$). The bound collapses to
$\Theta(n^2)$ only when a side shrinks by a *non*-constant fraction, e.g. peeling off one
element, making the height $\Theta(n)$. This is why quicksort's worst case is a sorted
array with a first-element pivot, and why randomised or median-of-three pivots are used.

---

### Q82 — closest pair of points

**(a) Sorting the strip at every level.**

$$T(n) = 2T\!\left(\frac{n}{2}\right) + \Theta(n\log n)$$

$\alpha = \log_2 2 = 1$ and $f(n) = \Theta\!\left(n^{1}\log^{1} n\right)$, so the general
Case 2 applies with $k = 1$:

$$\boxed{T(n) = \Theta\!\left(n\log^2 n\right)}$$

**(b) Pre-sorted once, linear strip scan.**

$$T(n) = 2T\!\left(\frac{n}{2}\right) + \Theta(n)$$

$\alpha = 1$, $f = \Theta(n) = \Theta(n^{\alpha}) \Rightarrow$ Case 2 with $k = 0$:

$$\boxed{T(n) = \Theta(n\log n)}$$

matching the $\Theta(n\log n)$ quoted for closest pair in the module's complexity table.

**Practical lesson:** do expensive preprocessing **once, outside the recursion**. Work done
inside a divide-and-conquer routine is paid for at every one of the $\Theta(\log n)$
levels, so an extra log factor in the combine step becomes an extra log factor in the
answer. Passing pre-sorted arrays (or index lists) down the recursion is the standard fix.

---

### Q83 — exact count

The outer variable takes $i = n, n/3, n/9, \dots$, and the inner loop runs $i$ times:

$$\mathrm{count} = n + \frac{n}{3} + \frac{n}{9} + \dots = n\sum_{i=0}^{\log_3 n}\left(\frac{1}{3}\right)^{i} \le \frac{3n}{2}$$

$$\boxed{\Theta(n)} \qquad \text{(machine check: } \mathrm{count}/n \to 1.5\text{)}$$

Only $\Theta(\log_3 n)$ outer iterations, but again the inner costs form a decaying
geometric series — the first iteration alone accounts for two-thirds of the total.

---

### Q84 — MT, general Case 2

$a = 4$, $b = 4$, $f(n) = n\log n$, $\alpha = \log_4 4 = 1$.

$$f(n) = n\log n = \Theta\!\left(n^{\alpha}\log^{k} n\right) \text{ with } k = 1$$

$$\boxed{T(n) = \Theta\!\left(n\log^2 n\right)} \qquad \text{(machine ratio} \to 1/4)$$

---

### Q85 — four-way merge sort

**(a)** Four subproblems of size $n/4$ and a $\Theta(n)$ four-way merge:

$$T(n) = 4T\!\left(\frac{n}{4}\right) + \Theta(n)$$

MT: $\alpha = \log_4 4 = 1$; $f = \Theta(n) = \Theta(n^{\alpha}) \Rightarrow$ Case 2:

$$\boxed{T(n) = \Theta(n\log n)}$$

**(b) No — it does not beat two-way merge sort asymptotically.**

$\alpha = 1$ in both cases and both sit in Case 2, so both are $\Theta(n\log n)$. In
recursion-tree terms: the four-way tree has height
$\log_4 n = \tfrac{1}{2}\log_2 n$, *half* as many levels — but each level still costs
$\Theta(n)$, so the product is the same up to the constant $\tfrac{1}{2}$. And that
constant is illusory: merging four sorted runs needs more comparisons per output element
than merging two (about $2$ against $1$), so the saving in levels is paid back in the
merge.

**General principle:** for $T(n) = a\,T(n/a) + \Theta(n)$ the answer is $\Theta(n\log n)$
for *every* constant $a \ge 2$ — changing $a$ alone moves nothing, because $\alpha$ stays
$1$. (Multi-way merging is still used in practice, but for I/O and cache reasons, not
asymptotics.)

---

### Q86 — step count

- **Non-recursive:** *two* loops of $n$ iterations each $\Rightarrow n + n = 2n = \Theta(n)$
- **Recurrence:** $T(n) = 2T(n/2) + 2n$
- **MT:** $\alpha = 1$; $f = 2n = \Theta(n) \Rightarrow$ Case 2

$$\boxed{T(n) = \Theta(n\log n)}$$

The factor $2$ in $f(n)$ is a constant and vanishes into $\Theta$ — doubling the combine
work changes only the constant (here $2n\log_2 n$ instead of $n\log_2 n$).

---

### Q87 — substitution

**Guess:** $T(n) \le c\,n^2$ for $n \ge 1$.

$$\begin{aligned}
T(n) &= T(n-1) + n \\
     &\le c(n-1)^{2} + n \\
     &= c\,n^2 - 2c\,n + c + n \\
     &= c\,n^2 - \left(2c\,n - c - n\right) \\
     &\le c\,n^2 \qquad \text{provided } 2c\,n - c - n \ge 0
\end{aligned}$$

With $c = 1$ the condition reads $2n - 1 - n = n - 1 \ge 0$, true for all $n \ge 1$ ✓

**Base case:** $T(1) = \Theta(1) = d \le c\cdot1^2$ requires $c \ge d$; take
$c = \max(1, d)$.

$$\boxed{T(n) = O(n^2)} \qquad \blacksquare$$

The matching $\Omega(n^2)$ follows from $T(n) = \tfrac{n(n+1)}{2}$ exactly (Q27).

---

### Q88 — a non-constant branching factor

**Why MT fails:** the theorem requires $a$ to be a **constant**. Here the number of
subproblems is $a = \sqrt{n}$, which grows with $n$, so the form $aT(n/b) + f(n)$ does not
apply at all — this is not a gap or boundary case, it is outside the hypotheses.

**Solution.** Divide through by $n$ and set $S(n) = T(n)/n$:

$$\frac{T(n)}{n} = \frac{\sqrt{n}\,T(\sqrt{n}\,)}{n} + 1 = \frac{T(\sqrt{n}\,)}{\sqrt{n}} + 1 \implies S(n) = S(\sqrt{n}\,) + 1$$

By Q47, $S(n) = \Theta(\log\log n)$. Therefore

$$\boxed{T(n) = n\,S(n) = \Theta(n\log\log n)} \qquad \text{(machine ratio} \to 1)$$

---

### Q89 — the comparison-sorting lower bound

Model any comparison-based sorting algorithm as a **decision tree**: each internal node is
a comparison $A[i] \le A[j]$ with two outcomes, and each leaf is one output permutation.

1. The algorithm must be able to produce **every** ordering of $n$ distinct elements, so
   the tree needs at least $n!$ leaves.
2. A binary tree of height $h$ has at most $2^{h}$ leaves, so

$$2^{h} \ge n! \implies h \ge \log_2(n!)$$

3. By Stirling's approximation,

$$\log_2(n!) = n\log_2 n - n\log_2 e + \Theta(\log n) = \Theta(n\log n)$$

4. The worst-case number of comparisons is the height $h$ of the tree.

$$\boxed{\text{Any comparison sort makes } \Omega(n\log n) \text{ comparisons in the worst case.}}$$

**Implication:** merge sort achieves $\Theta(n\log n)$ worst case, so it is
**asymptotically optimal** among comparison sorts — no comparison-based algorithm can do
better by more than a constant factor. Sub-$\Theta(n\log n)$ sorting is possible only by
abandoning comparisons (counting or radix sort, which exploit the structure of the keys).

---

### Q90

**(a)** $T(n) = a\,T(n/4) + n^2$, so $\alpha = \log_4 a$ compared with the exponent $2$ of
$f$:

| Regime | Condition | MT case | Result |
|---|---|---|---|
| $\alpha < 2$ | $a < 16$ | Case 3, regularity $a(n/4)^2 = \tfrac{a}{16}n^2$, $c = a/16 < 1$ ✓ | $\Theta(n^2)$ |
| $\alpha = 2$ | $a = 16$ | Case 2, $k = 0$ | $\Theta(n^2\log n)$ |
| $\alpha > 2$ | $a > 16$ | Case 1 | $\Theta\!\left(n^{\log_4 a}\right)$ |

The threshold is $a = 16 = b^2$ — exactly where the branching rate matches the rate at
which the combine cost shrinks. (Q66 and Q51 are the $a = 16$ case.)

**(b) Stack depth.** Only the frames on the *current* root-to-leaf path are live at any
moment — sibling calls execute one after the other and their frames are popped — so the
branching factor does not enter:

$$S(n) = S\!\left(\frac{n}{2}\right) + \Theta(1) \implies \boxed{S(n) = \Theta(\log n)}$$

**Contrast with the broken split of Q55:** there the recursion is
$S(n) = S(n-1) + \Theta(1)$, giving $\boxed{S(n) = \Theta(n)}$ stack depth. Two calls of
size $n/2$ give a tree of *height* $\log n$; one call of size $n-1$ gives height $n$. That
is the "stack overflow from deep recursion on unbalanced splits" pitfall from the module
notes — and the reason merge sort's $\Theta(\log n)$ stack is safe while a naive quicksort
on sorted input can crash.

Note the asymmetry worth remembering: **time** depends on $a$, $b$ and $f$ (the whole
tree), whereas **stack depth** depends only on the tree's height, i.e. on $b$ (or on the
additive decrement) — $a$ is irrelevant to it.

---

## Answer summary

| Q | Answer | Q | Answer |
|---|---|---|---|
| 1 | $\Theta(n\log n)$ | 46 | $\Theta(n)$ |
| 2 | $\Theta(n\log n)$ | 47 | $\Theta(\log\log n)$ |
| 3 | $\Theta(n^2)$ | 48 | $\Theta(n\log^2 n)$ |
| 4 | $\Theta(n\log n)$ | 49 | $\Theta(n\log^2 n)$ |
| 5 | $O(n\log n)$ | 50 | $\Theta(n^2)$ |
| 6 | $\Theta(n)$ | 51 | $\Theta(n^2\log n)$ |
| 7 | $\Theta(\log n)$ | 52 | $\Theta(n^3)$ |
| 8 | $\Theta\!\left(n^{\log_2 7}\right)$ | 53 | $\Theta(n\log^2 n)$ |
| 9 | $\Theta(n^3)$ | 54 | $O\!\left(n^{\log_2 3}\right)$ |
| 10 | $\Theta(n)$ | 55 | $\Theta(n^2)$ |
| 11 | $\Theta\!\left(n^{\log_2 3}\right)$ | 56 | $\Theta(n^2)$ |
| 12 | $\Theta(n^2)$ | 57 | $\Theta(n\log n)$ |
| 13 | fallacy: hidden constant | 58 | $\Theta(n^2\log n)$ |
| 14 | $\Theta\!\left(n^{\log_2 6}\right)$ | 59 | $\Theta(n!)$ |
| 15 | $\Theta(n^2)$ | 60 | $\Theta(n^2)$ |
| 16 | $\Theta(n\log n)$ | 61 | $\Theta(n)$ |
| 17 | $\Theta(n^2)$ | 62 | $\Theta(n)$ / $\Theta(n\log n)$ |
| 18 | $\Theta\!\left(n^{1.5}\log n\right)$ | 63 | $\Theta(n^2)$ |
| 19 | $\Theta(\log\log n)$ | 64 | $\Theta(n^2)$ |
| 20 | $\Theta(n)$ | 65 | $\Theta(n^2\log^2 n)$ |
| 21 | $\Theta(n\log n)$ | 66 | $\Theta(n^2\log n)$ |
| 22 | $\Theta(n^2)$ / $\Theta(n^2\log n)$ / $\Theta\!\left(n^{\log_2 a}\right)$ | 67 | $O(\log n)$ |
| 23 | $\Theta(n^2)$ | 68 | $\Theta\!\left(n^{\log_2 7}\right)$ |
| 24 | $O(n\log n)$ | 69 | $\Theta(\log n)$ |
| 25 | $\Theta(n^2\log n)$ | 70 | $\Theta(n)$ |
| 26 | $\Theta(n^3)$ | 71 | $\Theta(\sqrt{n})$ / $\Theta(\log n)$ |
| 27 | $n(n+1)/2$ | 72 | $\Theta(\log n)$ |
| 28 | $\Theta\!\left(n^{\log_2 3}\right)$ | 73 | $C = \begin{pmatrix}26 & 22\\ 23 & 41\end{pmatrix}$ |
| 29 | $\Theta(n\log\log n)$ | 74 | none apply |
| 30 | $15{,}920{,}205$ | 75 | $\Theta(n^2)$ |
| 31 | $\Theta(n)$ | 76 | $\Theta\!\left(n^{\log_2 7}\right)$ |
| 32 | $\Theta(\log^2 n)$ | 77 | $\Theta(n\log n)$ |
| 33 | $\Theta(n^2\log n)$ | 78 | $O(n^2)$ |
| 34 | $\Theta(n\log^2 n)$ | 79 | needs one recursive term |
| 35 | $\Omega(n\log n)$ | 80 | $\Theta(\log n\log\log n)$ |
| 36 | $\Theta(n^2)$ | 81 | $\Theta(n\log n)$ / $\Theta(n^2)$ |
| 37 | $\Theta(2^n)$ | 82 | $\Theta(n\log^2 n)$ / $\Theta(n\log n)$ |
| 38 | $\Theta(\sqrt{n}\log n)$ | 83 | $\Theta(n)$ |
| 39 | $\Theta(n^2)$ / $\Theta(n\log n)$ | 84 | $\Theta(n\log^2 n)$ |
| 40 | $\Theta(\log n)$ | 85 | $\Theta(n\log n)$, no gain |
| 41 | $\Theta\!\left(n^{\log_2 5}\right)$ | 86 | $\Theta(n\log n)$ |
| 42 | $\Theta\!\left(n^{\log_2 7}\right)$ | 87 | $O(n^2)$ |
| 43 | $\Theta(n^2)$ | 88 | $\Theta(n\log\log n)$ |
| 44 | $\Theta\!\left(n^{\log_3 5}\right)$ | 89 | $\Omega(n\log n)$ |
| 45 | $\Theta(2^n)$ | 90 | $\Theta(n^2)$/$\Theta(n^2\log n)$/$\Theta\!\left(n^{\log_4 a}\right)$; $\Theta(\log n)$ |