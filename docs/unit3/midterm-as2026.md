# Midterm Autumn Semester 2026

## Question 1 — Multiple Choice

**1.1** The recurrence $T(n) = 3T\left(\dfrac{n}{3}\right) + \sqrt{n}$ solves to:

- ==(a) $\Theta(n)$==
- (b) $\Theta(n \log n)$
- (c) $\Theta(n^2)$
- (d) $\Theta(\log n)$

**1.2** The Master Theorem can **NOT** be applied to which of the following recurrences?

- (a) $T(n) = 2T\left(\dfrac{n}{2}\right) + n$
- (b) $T(n) = 9T\left(\dfrac{n}{3}\right) + n$
- (c) ==$T(n) = 2T(n - 1) + n$==
- (d) $T(n) = 7T(n/2) + n^2$

**1.3** How many leaves does the recursion tree for $T(n) = 3T\left(\dfrac{n}{4}\right) + n^2$ have?

- ==(a) $n^{\log_4 3}$==
- (b) $n^{\log_3 4}$
- (c) $3n$
- (d) $n^2$

**1.4** In a recursion tree whose level costs form a decreasing geometric series, the asymptotic bound is set by:

- (a) The leaves
- ==(b) The root==
- (c) The height of the tree
- (d) The total number of nodes

**1.5** Which of the following lists the time complexities in increasing order of growth rate?

- (a) $O(n) < O(\log n) < O(n\log n) < O(n^2)$
- ==(b) $O(\log n) < O(n) < O(n\log n) < O(n^2)$==
- (c) $O(\log n) < O(n\log n) < O(n) < O(n^2)$
- (d) $O(1) < O(n) < O(\log n) < O(n^2)$

??? success "Answer Key — Question 1"

    | # | Answer | Why |
    |---|--------|-----|
    | 1.1 | **(a)** $\Theta(n)$ | $a=3,\ b=3 \Rightarrow n^{\log_b a} = n^{\log_3 3} = n$. $f(n)=\sqrt{n}=O(n^{1-\varepsilon})$ with $\varepsilon=0.5>0$ $\Rightarrow$ **Case 1** $\Rightarrow \Theta(n)$. |
    | 1.2 | **(c)** $T(n)=2T(n-1)+n$ | The Master Theorem needs the form $T(n)=aT(n/b)+f(n)$ with $a\ge 1,\ b>1$ — a subproblem that is a *constant fraction* of $n$. (c) subtracts a constant ($n-1$), so no valid $b$ exists; it must be solved by substitution/iteration, giving $\Theta(n^2)$. (a), (b), (d) are all valid Master Theorem forms. |
    | 1.3 | **(a)** $n^{\log_4 3}$ | Branching factor $a=3$, subproblem shrinks by $b=4$ each level $\Rightarrow$ depth $=\log_4 n$. Leaves $= a^{\text{depth}} = 3^{\log_4 n} = n^{\log_4 3}$. (General rule: leaves $= n^{\log_b a}$.) |
    | 1.4 | **(b)** The root | A decreasing geometric series $\sum r^i c_0$ with $r<1$ sums to $\Theta(c_0)$ — dominated by its first term, the cost of the root level. |
    | 1.5 | **(b)** $O(\log n) < O(n) < O(n\log n) < O(n^2)$ | The correct growth hierarchy is constant $<$ logarithmic $<$ linear $<$ linearithmic $<$ quadratic. (a), (c), (d) all misorder $O(n)$ against $O(\log n)$ or $O(n)$ against $O(n\log n)$. |

    **Marks:** 0.5 for each correct option.

---

## Question 2 — Recurrence Solving

**[2, 2, 2, 2 marks]**

**2(a)** Use a recursion tree to solve $T(n) = T\left(\dfrac{n}{3}\right) + T\left(\dfrac{2n}{3}\right) + n^2$, $T(1) = 1$; give the level cost, the height, the leaf count, and the $\Theta$ bound. Assume rounding of subproblem sizes is ignored.

??? question "Solution 2(a)"

    **Step 1 — Level cost**

    - Level 0 (root): $n^2$
    - Level 1: $\left(\dfrac{n}{3}\right)^2 + \left(\dfrac{2n}{3}\right)^2 = \dfrac{n^2}{9} + \dfrac{4n^2}{9} = \dfrac{5}{9}n^2$
    - Level 2: $\left(\dfrac{5}{9}\right)^2 n^2$
    - Level $i$: $\text{cost}(i) = \left(\dfrac{5}{9}\right)^i n^2$ — a **decreasing geometric series** with ratio $r = \dfrac{5}{9} < 1$.

    <div class="center-mermaid">

    ```mermaid
    flowchart TD
        A["n&sup2;<br/>size n"] --> B1["(n/3)&sup2;<br/>size n/3"]
        A --> B2["(2n/3)&sup2;<br/>size 2n/3"]

        B1 --> C1["(n/9)&sup2;<br/>size n/9"]
        B1 --> C2["(2n/9)&sup2;<br/>size 2n/9"]
        B2 --> C3["(2n/9)&sup2;<br/>size 2n/9"]
        B2 --> C4["(4n/9)&sup2;<br/>size 4n/9"]

        C1 --> D1["..."]
        C2 --> D2["..."]
        C3 --> D3["..."]
        C4 --> D4["..."]

        D1 --> E1["T(1)=1<br/>shortest path<br/>height log&#8323; n"]
        D4 --> E4["T(1)=1<br/>longest path<br/>height log&#8321;.&#8324;&#8325; n"]
    ```
    </div>

    Every left branch shrinks by $\tfrac{1}{3}$ and every right branch shrinks by $\tfrac{2}{3}$, so the tree is unbalanced: the leftmost path reaches a leaf after $\log_3 n$ levels while the rightmost path takes $\log_{3/2} n$ levels — this asymmetry is exactly what Step 2 quantifies below.

    **Step 2 — Height**

    The tree is unbalanced.

    - Shortest root-to-leaf path (always taking the $n/3$ branch): $\log_3 n$.
    - Longest root-to-leaf path (always taking the $2n/3$ branch): solve $n(2/3)^h = 1 \Rightarrow h = \log_{3/2} n \approx 1.71\log_2 n$.

    Height of the tree $= \log_{3/2} n$.

    **Step 3 — Leaf count**

    Branching factor 2, maximum depth $\log_{3/2} n$ $\Rightarrow$ at most

    $$2^{\log_{3/2} n} = n^{\log_{3/2} 2} \approx n^{1.71}$$

    leaves, each costing $T(1) = 1$. Total leaf cost $\approx n^{1.71} = o(n^2)$, so the leaves do **not** dominate.

    **Step 4 — $\Theta$ bound**

    - Upper bound: $T(n) \le \displaystyle\sum_{i=0}^{\infty} \left(\frac{5}{9}\right)^i n^2 = n^2 \cdot \dfrac{1}{1-5/9} = \dfrac{9}{4}n^2 = O(n^2)$
    - Lower bound: the root alone costs $n^2 \Rightarrow T(n) = \Omega(n^2)$

    $$\boxed{T(n) = \Theta(n^2)}$$

    — the root dominates (decreasing geometric series).

    **Marking breakdown (2 marks):** level cost $\left(\tfrac{5}{9}\right)^i n^2$ — 0.5; height $\log_{3/2} n$ — 0.5; leaf count $n^{\log_{3/2} 2}$ — 0.5; summing the geometric series to $\Theta(n^2)$ — 0.5.

**2(b)** Solve $T(n) = 6T\left(\dfrac{n}{4}\right) + \dfrac{n}{\log n}$ by the Master Theorem, verifying every condition the case requires.

??? question "Solution 2(b)"

    **Step 1 — Identify the parameters**

    $a=6$, $b=4$, $f(n) = n/\log n$. Pre-conditions: $a=6\ge 1$ ✓, $b=4>1$ ✓, $f(n)$ asymptotically positive ✓, subproblem size a constant fraction $n/4$ ✓.

    **Step 2 — Compute the watershed function**

    $$\log_b a = \log_4 6 = \frac{\ln 6}{\ln 4} = \frac{1.7918}{1.3863} \approx 1.2925$$

    $$n^{\log_b a} = n^{\log_4 6} \approx n^{1.2925}$$

    **Step 3 — Compare $f(n)$ with $n^{\log_b a}$**

    $f(n) = n/\log n \le n = n^1$ for all $n \ge 2$. Choose $\varepsilon = 0.2925$ (any $0 < \varepsilon \le 0.2925$ works). Then

    $$n^{\log_4 6 - \varepsilon} = n^{1.2925 - 0.2925} = n^1, \qquad f(n) = \frac{n}{\log n} = O(n^1)$$

    So $f(n) = O\!\left(n^{\log_b a - \varepsilon}\right)$ with $\varepsilon > 0$ $\Rightarrow$ **Case 1** applies.

    **Step 4 — Conditions required by Case 1**

    Case 1 only requires that $f(n)$ be polynomially smaller than $n^{\log_b a}$ by a factor $n^{\varepsilon}$, $\varepsilon > 0$ — verified above. (The regularity condition $a\,f(n/b) \le c\,f(n)$ is needed only for Case 3, so it does not need to be checked here.)

    **Step 5 — Conclusion**

    $$\boxed{T(n) = \Theta\!\left(n^{\log_4 6}\right) = \Theta(n^{1.2925\ldots})}$$

    (the recursion / leaf level dominates.)

    **Marking breakdown (2 marks):** $a$, $b$, $f(n)$ identified — 0.5; $\log_4 6$ computed — 0.5; correct case with an explicit $\varepsilon$ and the comparison shown — 0.75; final $\Theta$ answer — 0.25.

**2(c)** Using the induction method, prove that $T(n) = \sqrt{n}\,T(\sqrt{n}) + n$ has a time complexity of $T(n) = O(n\log n)$.

??? question "Solution 2(c)"

    (all logarithms to base 2)

    **Step 1 — State the inductive hypothesis**

    Claim: there exist constants $c > 0$ and $n_0$ such that $T(n) \le c\, n \log n$ for all $n \ge n_0$. Assume (strong induction) that the claim holds for every value smaller than $n$ — in particular for $\sqrt{n}$, since $\sqrt{n} < n$ for $n > 1$.

    **Step 2 — Inductive step**

    $$
    \begin{aligned}
    T(n) &= \sqrt{n}\cdot T(\sqrt{n}) + n \\
         &\le \sqrt{n}\cdot\left[c\cdot\sqrt{n}\log\sqrt{n}\right] + n && \text{(inductive hypothesis)} \\
         &= c\cdot n \cdot \log\sqrt{n} + n && (\sqrt{n}\cdot\sqrt{n}=n) \\
         &= c\cdot n \cdot \left(\tfrac{1}{2}\log n\right) + n && (\log\sqrt{n} = \tfrac{1}{2}\log n) \\
         &= \frac{c}{2}\, n\log n + n
    \end{aligned}
    $$

    **Step 3 — Force the result into the required form**

    We need $\dfrac{c}{2} n\log n + n \le c\, n\log n$

    $$\iff n \le \frac{c}{2} n \log n \iff c \ge \frac{2}{\log n}$$

    For all $n \ge 4$, $\log n \ge 2$, so $2/\log n \le 1$. Therefore any $c \ge 2$ satisfies it.

    **Step 4 — Base case**

    Take $n_0 = 4$. Choose $c \ge \max\!\left(2,\ T(4)/(4\log 4)\right) = \max(2,\ T(4)/8)$. Since $T(4)$ is a constant, such a $c$ exists and $T(4) \le c\cdot 4\log 4$ holds.

    **Step 5 — Conclusion**

    By strong induction, $T(n) \le c\, n\log n$ for all $n \ge 4$, hence

    $$\boxed{T(n) = O(n\log n)} \qquad \blacksquare$$

    **Marking breakdown (2 marks):** correct hypothesis $T(n)\le c\,n\log n$ — 0.5; correct substitution and algebra to $\tfrac{c}{2}n\log n + n$ — 0.75; closing the induction by choosing $c$ ($c\ge 2$) — 0.5; base case — 0.25.

**2(d)** Explain why telescoping works cleanly on $T(n) = 2T\left(\dfrac{n}{2}\right) + cn$ but not on $T(n) = T\left(\dfrac{n}{3}\right) + T\left(\dfrac{2n}{3}\right) + n$.

??? question "Solution 2(d)"

    **Principle:** telescoping needs each expansion to produce exactly **one** recursive term at a single smaller argument, so the equations form a linear chain in which every intermediate term cancels with the next.

    **Case A — $T(n) = 2T(n/2) + cn$ (telescopes cleanly)**

    Divide both sides by $n$: $\dfrac{T(n)}{n} = \dfrac{T(n/2)}{n/2} + c$

    Let $n = 2^k$ and $S(k) = T(2^k)/2^k$: $S(k) = S(k-1) + c$

    Write the chain and add:

    $$
    \begin{aligned}
    S(k) &= S(k-1) + c \\
    S(k-1) &= S(k-2) + c \\
    &\ \ \vdots \\
    S(1) &= S(0) + c
    \end{aligned}
    $$

    All intermediate $S$ terms cancel: $S(k) = S(0) + ck \Rightarrow T(n)/n = T(1) + c\log_2 n$

    $$\Rightarrow T(n) = \Theta(n\log n)$$

    This works because (i) there is a single recursive term after normalising by $n$, (ii) all subproblems at a level have the **same** size $n/2^i$, and (iii) every root-to-leaf path has the same length $\log_2 n$.

    **Case B — $T(n) = T(n/3) + T(2n/3) + n$ (does not telescope)**

    Expanding gives **two** recursive terms with **different** arguments, so the expansion is a binary tree, not a linear chain — there is no single "previous" term to cancel against.

    No normalising divisor works: dividing by $n$ turns the terms into $\dfrac{1}{3}\cdot\dfrac{T(n/3)}{n/3} + \dfrac{2}{3}\cdot\dfrac{T(2n/3)}{2n/3}$, a weighted sum of two *different* unknowns, not one.

    The subproblem sizes are unequal and the tree is unbalanced — paths have different lengths ($\log_3 n$ to $\log_{3/2} n$) — so the levels do not line up and nothing cancels.

    **Correct method:** recursion tree (levels cost $n$ each, height $\log_{3/2} n$) or the substitution method, giving $T(n) = \Theta(n\log n)$.

    **Marking breakdown (2 marks):** statement of the telescoping requirement (single recursive term / uniform size) — 0.5; worked telescoping of $2T(n/2)+cn$ — 0.75; reason it fails for the unbalanced recurrence (two different arguments, unequal path lengths) — 0.75.

---

## Question 3 — Step-Count Analysis

**[1 x 4.5 = 4.5 marks]**

Consider the following recursive function. Using the step-count method, determine the asymptotic running time of the function. First determine the cost of the non-recursive portion, formulate the recurrence relation, and then solve the recurrence using the Master Theorem. Show all major steps.

```c
void function(int n) {
    if (n <= 1)
        return;

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j = j * 2) {
            count++;
        }
    }

    function(n / 2);
    function(n / 2);
}
```

??? question "Solution 3"

    **Step 1 — Cost of the non-recursive portion**

    - Base-case test `if (n <= 1) return;` $\rightarrow O(1)$
    - Inner loop: $j = 1, 2, 4, 8, \ldots$ up to $n$ ($j = j\times 2$) $\Rightarrow$ $j$ takes the values $2^0, 2^1, \ldots, 2^{\lfloor\log_2 n\rfloor}$ $\Rightarrow$ $\lfloor\log_2 n\rfloor + 1$ iterations.
    - Outer loop: $i = 1 \to n \Rightarrow n$ iterations, and the inner loop runs in full each time.

    Total `count++` executions $= n\cdot(\lfloor\log_2 n\rfloor + 1) = \Theta(n\log n)$

    $$\therefore \text{non-recursive cost } f(n) = \Theta(n\log n)$$

    **Step 2 — Formulate the recurrence**

    The function calls itself twice, each on input $n/2$: `function(n/2); function(n/2);`

    $$T(n) = 2\cdot T(n/2) + \Theta(n\log n), \qquad T(1) = \Theta(1)$$

    **Step 3 — Solve by the Master Theorem**

    $a=2$, $b=2$, $f(n) = n\log n$. Watershed: $n^{\log_b a} = n^{\log_2 2} = n^1 = n$.

    - **Case 1?** Needs $f(n) = O(n^{1-\varepsilon})$. But $n\log n$ grows *faster* than $n$ $\rightarrow$ does not apply.
    - **Case 3?** Needs $f(n) = \Omega(n^{1+\varepsilon})$ for some $\varepsilon>0$. Here $f(n)/n = \log n$, and $\log n = o(n^{\varepsilon})$ for every $\varepsilon>0$, so $f(n)$ is not polynomially larger than $n$ $\rightarrow$ does not apply.
    - **Case 2 (extended/general form):** $f(n) = \Theta\!\left(n^{\log_b a}\cdot\log^k n\right)$ with $k=1$, since $f(n) = n\log n = \Theta(n^1\log^1 n)$. The extended Case 2 then gives

    $$T(n) = \Theta\!\left(n^{\log_b a}\cdot\log^{k+1} n\right) = \Theta(n\log^2 n)$$

    **Step 4 — Answer**

    $$\boxed{T(n) = \Theta(n\log^2 n)}$$

    **Verification by recursion tree (optional check)**

    Level $i$ has $2^i$ nodes of size $n/2^i$; cost per level $= 2^i\cdot(n/2^i)\cdot\log(n/2^i) = n(\log n - i)$.

    Summing $i = 0 \ldots \log n$: $n\cdot\sum(\log n - i) = n\cdot\dfrac{\log^2 n}{2} = \Theta(n\log^2 n)$ ✓

    **Marking breakdown (4.5 marks):**

    - Inner loop $= \lfloor\log_2 n\rfloor + 1$ iterations (doubling) — 0.75
    - Outer $\times$ inner $\Rightarrow$ non-recursive cost $\Theta(n\log n)$ — 0.75
    - Correct recurrence $T(n) = 2T(n/2) + \Theta(n\log n)$ with base case — 1.0
    - $a$, $b$ and watershed $n^{\log_2 2} = n$ identified — 0.5
    - Ruling out Case 1 and Case 3 ($\log n$ is not polynomial) — 1.0
    - Final answer $T(n) = \Theta(n\log^2 n)$ — 0.5
