# CSF302 — Algorithm Analysis and Design

### Q1
Solve by the Master Theorem, naming the case and stating $\alpha$:

$$T(n) = 2T\!\left(\frac{n}{2}\right) + \Theta(n)$$


### Q2
Using the step-count method, find the asymptotic running time. Give the cost of the
non-recursive portion, form the recurrence, then solve it by the Master Theorem.

```c
void process(int n) {
    if (n <= 1) return;
    process(n / 2);
    for (int i = 1; i <= n; i++) {
        count++;
    }
    process(n / 2);
}
```

Would your answer change if the loop were placed *before* both recursive calls? Justify.

### Q3
Draw the recursion tree for $T(n) = 4T(n/2) + n$. Give the cost of level $i$, the height,
the number of leaves, and the $\Theta$ bound. State which part of the tree dominates.

### Q4
Count the executions of `count++` exactly as a summation, then give the $\Theta$ bound.

```c
for (int i = 1; i <= n; i++) {
    for (int j = 1; j <= n; j = j + i) {
        count++;
    }
}
```

### Q5
Using the substitution (induction) method, prove that $T(n) = 2T(n/2) + n$ is
$O(n\log n)$. State your guess, the constant you choose, the full inductive step, and how
you handle the base case.

### Q6
A student modifies binary search so that it searches **both** halves of the array instead
of choosing one:

```c
int search(int A[], int lo, int hi, int key) {
    if (lo > hi) return -1;
    int mid = lo + (hi - lo) / 2;
    if (A[mid] == key) return mid;
    int left  = search(A, lo, mid - 1, key);
    int right = search(A, mid + 1, hi, key);
    return (left != -1) ? left : right;
}
```

Write the recurrence, solve it by the Master Theorem, and explain in one or two sentences
what has been destroyed relative to ordinary binary search.

### Q7
Solve by telescoping, showing the cancellation explicitly:

$$T(n) = T\!\left(\frac{n}{2}\right) + 1, \qquad T(1) = 1$$

### Q8
Solve by the Master Theorem, naming the case:

$$T(n) = 7T\!\left(\frac{n}{2}\right) + \Theta(n^2)$$

State which algorithm this is and compare the exponent you obtain with $3$.

### Q9
Using the step-count method, determine the asymptotic running time.

```c
void blockmul(int n) {
    if (n <= 1) return;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) {
            count++;
        }
    }
    for (int k = 1; k <= 8; k++) {
        blockmul(n / 2);
    }
}
```

Which matrix-multiplication method does this correspond to, and what does it tell you
about "divide and conquer alone"?

### Q10
Count the executions of `count++` exactly, then give the $\Theta$ bound. Many students
answer $\Theta(n\log n)$ here — show why that is wrong.

```c
int i = n;
while (i > 0) {
    for (int j = 1; j <= i; j++) {
        count++;
    }
    i = i / 2;
}
```

### Q11
Solve by the Master Theorem, naming the case and giving the exponent to three decimal
places:

$$T(n) = 3T\!\left(\frac{n}{2}\right) + \Theta(n)$$

Name the algorithm and state what the $3$ represents.

### Q12
Draw the recursion tree for $T(n) = 3T(n/3) + n^2$. Give the level cost, the height, the
leaf count, and the $\Theta$ bound. Identify the type of series formed by the level costs.

### Q13
The following "proof" concludes that $T(n) = 2T(n/2) + n$ is $O(n)$. Find the error and
explain precisely why it is invalid.

> Assume $T(k) = O(k)$ for all $k < n$. Then
> $T(n) = 2T(n/2) + n = 2\cdot O(n/2) + n = O(n) + n = O(n)$. $\blacksquare$

### Q14
Suppose a researcher discovers a way to multiply two $2 \times 2$ matrices using only
**six** scalar multiplications, with $\Theta(n^2)$ additions when applied blockwise. Write
the resulting recurrence, solve it by the Master Theorem, and state the exponent to three
decimal places. Compare with Strassen's exponent.

### Q15
Using the step-count method, determine the asymptotic running time. Note that the Master
Theorem does not apply; use telescoping instead.

```c
void scan(int n) {
    if (n <= 0) return;
    for (int i = 1; i <= n; i++) {
        count++;
    }
    scan(n - 1);
}
```

### Q16
Solve by telescoping. Divide through by $n$ first to make the recurrence collapse into a
chain.

$$T(n) = 3T\!\left(\frac{n}{3}\right) + n, \qquad T(1) = 1$$

### Q17
Solve by the Master Theorem. You must verify the regularity condition explicitly and state
the value of $c$ you use.

$$T(n) = 2T\!\left(\frac{n}{2}\right) + n^2$$

### Q18
Count the executions of `count++`, then give the $\Theta$ bound. Treat the three loops
independently.

```c
for (int i = 1; i <= n; i++) {
    for (int j = 1; j * j <= n; j++) {
        for (int k = 1; k <= n; k = k * 2) {
            count++;
        }
    }
}
```

### Q19
Using the step-count method, form the recurrence and solve it by a change of variable
(let $n = 2^m$).

```c
void shrink(int n) {
    if (n <= 2) return;
    count++;
    shrink((int) sqrt(n));
}
```

### Q20
Solve by the Master Theorem, naming the case and verifying the regularity condition:

$$T(n) = T\!\left(\frac{n}{2}\right) + n$$

### Q21
Draw the recursion tree for $T(n) = T(n/3) + T(2n/3) + n$. Give the level cost, the
shortest and longest root-to-leaf paths, and the $\Theta$ bound. Explain why the uneven
split does not change the answer.

### Q22
Consider the parametrised recurrence $T(n) = a\,T(n/2) + \Theta(n^2)$, where $a$ is a
positive integer constant. Using the Master Theorem, determine the $\Theta$ bound as a
function of $a$, identifying **all three** regimes and the value of $a$ at which the
behaviour changes. Then state where Strassen ($a = 7$) and naive block multiplication
($a = 8$) sit.

### Q23
Using the step-count method, determine the asymptotic running time.

```c
void tri(int n) {
    if (n <= 1) return;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= i; j++) {
            count++;
        }
    }
    tri(n / 2);
}
```

### Q24
Using the substitution method, prove that $T(n) = T(n/4) + T(3n/4) + cn$ is $O(n\log n)$
for a constant $c > 0$. Show clearly where the slack in the inequality comes from and what
condition your constant must satisfy.

### Q25
Solve by the Master Theorem, naming the case and verifying every condition it requires:

$$T(n) = 9T\!\left(\frac{n}{3}\right) + n^2$$

### Q26
Count the executions of `count++` exactly as a nested summation, then give the $\Theta$
bound.

```c
for (int i = 1; i <= n; i++) {
    for (int j = 1; j <= i; j++) {
        for (int k = 1; k <= j; k++) {
            count++;
        }
    }
}
```

### Q27
Solve by telescoping:

$$T(n) = T(n-1) + n, \qquad T(0) = 0$$

Give the exact closed form, not only the $\Theta$ bound.

### Q28
Using the step-count method, determine the asymptotic running time. Solve the recurrence
by the Master Theorem and state which Unit 4 algorithm has this shape.

```c
void mult(int n) {
    if (n <= 1) return;
    for (int i = 1; i <= n; i++) {
        count++;
    }
    mult(n / 2);
    mult(n / 2);
    mult(n / 2);
}
```

### Q29
Consider $\displaystyle T(n) = 2T\!\left(\frac{n}{2}\right) + \frac{n}{\log n}$.

**(a)** Show that the Master Theorem cannot be applied, naming the case that *almost*
applies and the exact condition that fails.

**(b)** Solve it with a recursion tree, writing the level-cost sum as a harmonic sum.

### Q30
Apply the Karatsuba decomposition by hand to compute $2345 \times 6789$. Take $m = 2$ and
give $X_1, X_0, Y_1, Y_0$, then the three products $P_1, P_2, P_3$, then the recombination

$$X \cdot Y = P_1 \cdot 10^{2m} + P_3 \cdot 10^{m} + P_2$$

Verify against the schoolbook product, and state how many half-size multiplications you
used versus the naive expansion.

### Q31
Draw the recursion tree for $T(n) = T(n/2) + T(n/4) + n$. Give the level cost, identify
the series it forms, and give the $\Theta$ bound.

### Q32
Count the executions of `count++`, then give the $\Theta$ bound.

```c
for (int i = 1; i <= n; i = i * 2) {
    for (int j = 1; j <= n; j = j * 2) {
        count++;
    }
}
```

### Q33
Solve by the Master Theorem, naming the case:

$$T(n) = 4T\!\left(\frac{n}{2}\right) + n^2$$

### Q34
Using the step-count method, determine the asymptotic running time. The Master Theorem
does not settle this one directly — say why, then solve it with a recursion tree.

```c
void mix(int n) {
    if (n <= 1) return;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j = j * 3) {
            count++;
        }
    }
    mix(n / 2);
    mix(n / 2);
}
```

### Q35
Using the substitution method, prove the **lower** bound: $T(n) = 2T(n/2) + n$ is
$\Omega(n\log n)$. State your guess and complete the inductive step.

### Q36
Write the recurrence for the *naive* divide-and-conquer integer multiplication that
expands $X \cdot Y$ into **four** half-size products, solve it by the Master Theorem, and
explain what this result says about the value of dividing and conquering without
Karatsuba's identity.

### Q37
Solve by telescoping and give the exact closed form:

$$T(n) = T(n-1) + 2^{n}, \qquad T(0) = 1$$

### Q38
Solve by the Master Theorem, naming the case and justifying it by comparing $f(n)$ with
$n^{\alpha}$:

$$T(n) = 2T\!\left(\frac{n}{4}\right) + \sqrt{n}$$

### Q39
For the fragment below, give **two** counts: (i) how many times the `if` condition is
evaluated, and (ii) how many times `count++` executes. Express each as a summation and
give both $\Theta$ bounds.

```c
for (int i = 1; i <= n; i++) {
    for (int j = 1; j <= n; j++) {
        if (j % i == 0) {
            count++;
        }
    }
}
```

### Q40
Using the step-count method, determine the asymptotic running time and name the algorithm.

```c
int bsearch(int A[], int lo, int hi, int key) {
    if (lo > hi) return -1;
    int mid = lo + (hi - lo) / 2;
    count++;
    if (A[mid] == key) return mid;
    if (A[mid] > key) return bsearch(A, lo, mid - 1, key);
    else               return bsearch(A, mid + 1, hi, key);
}
```

Also state the auxiliary space and the stack depth.

### Q41
Solve by the Master Theorem, naming the case and giving $\alpha$ to three decimal places:

$$T(n) = 5T\!\left(\frac{n}{2}\right) + n^2$$

### Q42
Draw the recursion tree for $T(n) = 7T(n/2) + n^2$. Give the level cost, the leaf count in
the form $n^{\log_b a}$, and the $\Theta$ bound. State which level dominates and why.

### Q43
A student guesses that $T(n) = 4T(n/2) + n$ is $O(n)$ and attempts an inductive proof.
Carry out the inductive step, show exactly where it fails, then state the correct tight
bound and prove the upper half of it by induction using a guess of the form
$T(n) \le c\,n^2 - b\,n$.

### Q44
Toom–Cook multiplication splits each $n$-digit operand into **three** parts and needs
**five** multiplications of third-size numbers, with linear-time combination. Write the
recurrence, solve it by the Master Theorem, and give the exponent to three decimal places.
Check your answer against the value quoted for Toom–Cook in the module notes.

### Q45
Using the step-count method, determine the asymptotic running time. The Master Theorem
does not apply — use iteration.

```c
void twin(int n) {
    if (n <= 1) return;
    count++;
    twin(n - 1);
    twin(n - 1);
}
```

### Q46
Count the executions of `count++` exactly, then give the $\Theta$ bound.

```c
for (int i = 1; i <= n; i = i * 2) {
    for (int j = 1; j <= i; j++) {
        count++;
    }
}
```

### Q47
Solve by a change of variable (let $n = 2^m$):

$$T(n) = T(\sqrt{n}\,) + 1, \qquad T(2) = 1$$

### Q48
Solve by telescoping. Divide through by $n$ first.

$$T(n) = 2T\!\left(\frac{n}{2}\right) + n\log n$$

### Q49
Merge sort is modified so that the merge step is implemented carelessly and costs
$\Theta(n\log n)$ instead of $\Theta(n)$. Write the new recurrence, solve it, and state by
what factor the algorithm has been degraded.

### Q50
Using the step-count method, determine the asymptotic running time.

```c
void half(int n) {
    if (n <= 1) return;
    for (int i = 1; i <= n; i++) {
        for (int j = i; j <= n; j++) {
            count++;
        }
    }
    half(n / 2);
    half(n / 2);
}
```

### Q51
Solve by the Master Theorem, naming the case:

$$T(n) = 16\,T\!\left(\frac{n}{4}\right) + n^2$$

### Q52
Count the executions of `count++` as a summation and give the exact closed form plus the
$\Theta$ bound.

```c
for (int i = 1; i <= n; i++) {
    for (int j = 1; j <= i * i; j++) {
        count++;
    }
}
```

### Q53
Draw the recursion tree for $T(n) = 2T(n/2) + n\log n$. Give the cost of level $i$, sum
the levels, and give the $\Theta$ bound.

### Q54
Using the substitution method, prove that Karatsuba's recurrence $T(n) = 3T(n/2) + cn$ is
$O\!\left(n^{\log_2 3}\right)$. Use a guess of the form
$T(n) \le d\,n^{\log_2 3} - e\,n$ and show what the subtracted term is for.

### Q55
Merge sort is implemented with a broken split that produces subarrays of size $1$ and
$n-1$ instead of two halves. Write the recurrence, solve it by telescoping, and name the
sorting algorithm the result matches.

### Q56
Using the step-count method, determine the asymptotic running time.

```c
void quad(int n) {
    if (n <= 1) return;
    for (int i = 1; i <= n; i++) {
        count++;
    }
    quad(n / 2);
    quad(n / 2);
    quad(n / 2);
    quad(n / 2);
}
```

### Q57
Solve by the Master Theorem. Verify the regularity condition explicitly, giving the value
of $c$.

$$T(n) = 3T\!\left(\frac{n}{4}\right) + n\log n$$

### Q58
Count the executions of `k++`, then give the $\Theta$ bound.

```c
int k = 0;
for (int i = n / 2; i <= n; i++) {
    for (int j = 1; j <= n / 2; j++) {
        for (int l = 1; l <= n; l = l * 2) {
            k++;
        }
    }
}
```

### Q59
Solve by iteration and give the exact closed form:

$$T(n) = n \cdot T(n-1), \qquad T(1) = 1$$

Then state the $\Theta$ bound and compare its growth with $2^n$.

### Q60
Solve by the Master Theorem, naming the case and verifying the regularity condition:

$$T(n) = 7T\!\left(\frac{n}{3}\right) + n^2$$

### Q61
Two mutually recursive functions do linear work each. Using the step-count method, form
the combined recurrence for `f` and solve it.

```c
void f(int n) {
    if (n <= 1) return;
    for (int i = 1; i <= n; i++) count++;
    g(n / 2);
}

void g(int n) {
    if (n <= 1) return;
    for (int i = 1; i <= n; i++) count++;
    f(n / 2);
}
```

### Q62
Using recursion trees, solve **both** of the following and explain what makes the answers
differ:

**(a)** $\displaystyle T(n) = T\!\left(\frac{n}{5}\right) + T\!\left(\frac{7n}{10}\right) + n$ &nbsp; (the median-of-medians selection recurrence)

**(b)** $\displaystyle T(n) = T\!\left(\frac{n}{3}\right) + T\!\left(\frac{2n}{3}\right) + n$

State the general rule about the sum of the split fractions that your two answers
illustrate.

### Q63
Draw the recursion tree for $T(n) = 3T(n/4) + n^2$. Give the level cost, the ratio of the
geometric series, and the $\Theta$ bound. Which part of the tree dominates?

### Q64
Count the executions of `count++` exactly, then give the $\Theta$ bound.

```c
for (int i = 1; i <= n; i++) {
    for (int j = i; j <= n; j++) {
        count++;
    }
}
```

### Q65
Solve by the Master Theorem. This needs the general form of Case 2 (with the $\log^k n$
factor) — state $k$.

$$T(n) = 4T\!\left(\frac{n}{2}\right) + n^2\log n$$

### Q66
Using the step-count method, determine the asymptotic running time. Note carefully how
many recursive calls the loop generates.

```c
void quart(int n) {
    if (n <= 2) return;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) {
            count++;
        }
    }
    for (int k = 1; k <= 16; k++) {
        quart(n / 4);
    }
}
```

### Q67
Using the substitution method, prove that $T(n) = T(n/2) + 1$ is $O(\log n)$. Explain why
the base case cannot be taken at $n = 1$ and what you do instead.

### Q68
Suppose Strassen's algorithm is implemented so clumsily that the additions and
subtractions cost $\Theta(n^2\log n)$ rather than $\Theta(n^2)$, while still using seven
recursive multiplications. Write the recurrence, solve it by the Master Theorem, and state
whether the asymptotic running time changes. Explain what this tells you about which part
of a divide-and-conquer algorithm the exponent comes from.

### Q69
Solve by telescoping and give the $\Theta$ bound:

$$T(n) = T(n-1) + \frac{1}{n}, \qquad T(1) = 1$$

### Q70
Solve by the Master Theorem, naming the case and stating the $\varepsilon$ you use:

$$T(n) = 2T\!\left(\frac{n}{2}\right) + \sqrt{n}$$

### Q71
Count the executions of `count++` for each fragment separately and give both $\Theta$
bounds.

```c
/* fragment A */
for (int i = 1; i * i <= n; i++) {
    count++;
}

/* fragment B */
int m = n;
while (m > 1) {
    count++;
    m = m / 2;
}
```

### Q72
Using the step-count method, determine the asymptotic running time. Pay attention to the
loop bound.

```c
void tiny(int n) {
    if (n <= 1) return;
    for (int k = 1; k <= 100; k++) {
        count++;
    }
    tiny(n / 2);
}
```

### Q73
Apply Strassen's algorithm by hand to

$$A = \begin{pmatrix} 2 & 4 \\ 5 & 3 \end{pmatrix}, \qquad B = \begin{pmatrix} 1 & 7 \\ 6 & 2 \end{pmatrix}$$

Compute all seven products $m_1, \dots, m_7$ using

$$\begin{aligned}
m_1 &= (A_{11}+A_{22})(B_{11}+B_{22}) & m_2 &= B_{11}(A_{21}+A_{22}) \\
m_3 &= A_{11}(B_{12}-B_{22}) & m_4 &= A_{22}(B_{21}-B_{11}) \\
m_5 &= B_{22}(A_{11}+A_{12}) & m_6 &= (A_{21}-A_{11})(B_{11}+B_{12}) \\
m_7 &= (A_{12}-A_{22})(B_{21}+B_{22})
\end{aligned}$$

then assemble

$$C = \begin{pmatrix} m_1 + m_4 - m_5 + m_7 & m_3 + m_5 \\ m_2 + m_4 & m_1 + m_3 - m_2 + m_6 \end{pmatrix}$$

and verify against the ordinary product. Count the multiplications you performed versus
the definition.

### Q74
For each recurrence below, state whether the Master Theorem applies. If it does not, name
the specific precondition that is violated.

**(a)** $T(n) = 2T(n-1) + n$

**(b)** $T(n) = \tfrac{1}{2}T(n/2) + n$

**(c)** $T(n) = 64\,T(n/8) - n^2\log n$

**(d)** $T(n) = 2^{n}\,T(n/2) + n^{n}$

**(e)** $T(n) = 2T(n/2) + n/\log n$

**(f)** $T(n) = T(n/2) + T(n/4) + n$

### Q75
Draw the recursion tree for $T(n) = T(n-1) + n$. Describe its shape, state its height and
its branching factor, and give the $\Theta$ bound. Explain why this tree is a chain rather
than a branching tree.

### Q76
Using the step-count method, determine the asymptotic running time and give the exponent
to three decimal places.

```c
void strassen(int n) {
    if (n <= 1) return;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) {
            count++;
        }
    }
    for (int k = 1; k <= 7; k++) {
        strassen(n / 2);
    }
}
```

### Q77
Count the executions of `count++` exactly, then give the $\Theta$ bound.

```c
for (int i = 1; i <= n; i++) {
    int j = n;
    while (j > 1) {
        count++;
        j = j / 2;
    }
}
```

### Q78
Using the substitution method, prove that $T(n) = 2T(n/2) + n^2$ is $O(n^2)$. A plain
guess of $T(n) \le c\,n^2$ will work here — carry out the step and state the condition on
$c$. Then explain why the same plain guess fails for $T(n) = 2T(n/2) + n$.

### Q79
Explain why telescoping works cleanly on $T(n) = 4T(n/4) + cn$ but not on
$T(n) = T(n/2) + T(n/4) + n$. Identify the structural property a recurrence must have for
telescoping to work, and name the method you would use for the second one.

### Q80
Solve by a change of variable (let $n = 2^m$), then apply the Master Theorem to the
transformed recurrence:

$$T(n) = 2T(\sqrt{n}\,) + \log n$$

### Q81
Quicksort's partition is analysed under two assumptions. Using recursion trees, solve both
and state what the comparison shows about the importance of a *balanced* split:

**(a)** every partition splits $n$ into $n/10$ and $9n/10$

**(b)** every partition splits $n$ into $1$ and $n-1$

### Q82
The closest-pair-of-points algorithm splits the point set in half, recurses on each half,
and then examines the strip around the dividing line.

**(a)** If the strip is handled by sorting the strip points afresh at every level, the
non-recursive work is $\Theta(n\log n)$. Write and solve the recurrence.

**(b)** If the points are pre-sorted once and the strip is scanned in linear time, the
non-recursive work is $\Theta(n)$. Write and solve the recurrence.

State the practical lesson.

### Q83
Count the executions of `count++` exactly, then give the $\Theta$ bound.

```c
for (int i = n; i > 1; i = i / 3) {
    for (int j = 1; j <= i; j++) {
        count++;
    }
}
```

### Q84
Solve by the Master Theorem, using the general form of Case 2 and stating $k$:

$$T(n) = 4T\!\left(\frac{n}{4}\right) + n\log n$$

### Q85
A four-way merge sort splits the array into four parts, sorts each recursively, and merges
all four in $\Theta(n)$ time.

**(a)** Write the recurrence and solve it by the Master Theorem.

**(b)** Does it beat ordinary two-way merge sort asymptotically? Explain using $\alpha$
and the level-cost structure of the recursion tree.

### Q86
Using the step-count method, determine the asymptotic running time. Be careful to add both
non-recursive loops.

```c
void twice(int n) {
    if (n <= 1) return;
    for (int i = 1; i <= n; i++) count++;
    twice(n / 2);
    twice(n / 2);
    for (int i = 1; i <= n; i++) count++;
}
```

### Q87
Using the substitution method, prove that $T(n) = T(n-1) + n$ is $O(n^2)$.

### Q88
Solve the following. The Master Theorem does not apply — say why, then solve it by
dividing through by $n$ and using a change of variable.

$$T(n) = \sqrt{n}\;T(\sqrt{n}\,) + n$$

### Q89
Using a decision-tree argument, show that any comparison-based sorting algorithm needs
$\Omega(n\log n)$ comparisons in the worst case. State the number of leaves the tree must
have and use $\log(n!) = \Theta(n\log n)$. Then state what this implies about merge sort's
optimality.

### Q90
**(a)** For $T(n) = a\,T(n/4) + n^2$, use the Master Theorem to determine the $\Theta$
bound as a function of the positive integer constant $a$, identifying all three regimes
and the threshold value of $a$.

**(b)** Separately, write and solve the recurrence for the **stack depth** of a
divide-and-conquer routine that makes two recursive calls on $n/2$ and uses $\Theta(1)$
local space per frame. Contrast it with the stack depth of the broken $1$ versus $(n-1)$
split of Q55.

[solutions](solutions.md)