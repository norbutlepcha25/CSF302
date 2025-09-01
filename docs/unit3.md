# Unit 3

## RECURRENCE RELATIONS AND ANALYSIS OF ALGORITHMS

!!! info "Learning outome"

    Assess the efficiency of different approaches to solving recurrence relations, including the substitution method, recursion-tree method, and master method.

## **3.1 Recurrences**

### 3.1.1 INTRODUCTION TO RECURRENCE RELATIONS

What is **Recurrence**?

A recurrence is an equation (or inequality) that defines a function in terms of its value(s) at smaller input(s).
In simple terms: it’s a way of expressing a problem’s solution in terms of **_smaller subproblems_** of the same type.

What is a **recurrence relations**?

A **recurrence relation** is an equation that defines a sequence based on its previous terms. A recurrence relation is the actual formula that shows how the current value depends on previous values.

For example:

Factorial recurrence:
T(𝑛)=𝑛.T(𝑛-1),T(0)=1

This means factorial of 𝑛 is defined in terms of factorial of 𝑛−1.

---

### 3.1.2 GENERAL FORM OF RECURRENCE RELATIONS

\[
T(n) = a \cdot T\!\left(\frac{n}{b}\right) + f(n)
\]

Where:

- \(T(n)\) → the time/space complexity of the problem of size \(n\)
- \(a\) → number of subproblems in the recursion
- \(n/b\) → size of each subproblem
- \(f(n)\) → the cost of dividing the problem and combining the results

---

### 3.1.3 TYPES OF RECURRENCE RELATIONS

1. **Linear Recurrence** – depends linearly on smaller subproblems.
   Example: `T(n) = T(n-1) + O(1)`
2. **Divide-and-Conquer Recurrence** – splits into multiple subproblems.
   Example: `T(n) = aT(n/b) + f(n)`
   - Homogeneous: depends only on subproblems (`T(n) = 2T(n/2)`).
   - Non-Homogeneous: includes an additional function (`T(n) = 2T(n/2) + n`).

---

### 3.2 METHODS OF SOLVING RECURRENCE RELATIONS

When analyzing recursive algorithms, we use different techniques to solve **recurrence relations** and find their closed-form or asymptotic complexity.  
Here are the main methods:

1. Iterative Method
2. Recursion tree
3. Substitution Method
4. Telescoping
5. Master theorem

---

### 1. Iterative Method (Expansion Method)

- Expand the recurrence step by step until a clear pattern emerges.
- Replace the recurrence with successive substitutions.
- Stop once the base case is reached, then simplify.

!!! note "**Example 1:**"

      $$ T(n) = T(n-1) + 1, \quad T(1) = 1 $$

      We’ll solve it by **unrolling** (expanding) step by step until the base case.

      **Step 1. Unroll the Recurrence**

      Start expanding:

      $$ T(n) = T(n-1) + 1 $$

      $$ T(n-1) = T(n-1-1) + 1  \quad\implies\quad T(n) = T(n-2) + 2 $$

      $$ T(n-2) = T(n-2-1) + 1 + 1 \quad\implies\quad T(n) = T(n-3) + 3 $$

      $$ T(n-3) = T(n-3-1) + 1 + 1 + 1  \quad\implies\quad T(n) = T(n-3) + 3 $$

      After \(k\) steps, the pattern is:

      $$      T(n) = T(n-k) + k $$


      **Step 2. Stop at the Base Case**

      Pick \(k\) so that \(n - k\) hits the base index \(b\) (where \(b=1\) in this case):


      $$ n - k = 1 \quad\Rightarrow\quad k = n - 1 $$

      Now substitute \(k = n - 1\) into the pattern:

      $$
      T(n) = T(1) + (n - 1)
      $$

      **Step 3. Plug In Your Base**

      $$
      T(n) = T(1) + (n-1) \newline
            = 1 + (n-1)
      $$

     $ \therefore $ the growth is **linear**.


      **step 4. Final Result (Asymptotics)**

      $$
      \boxed{T(n) = \Theta(n)}
      $$

      **Intuition:** each step reduces \(n\) by 1 and adds a constant cost \(+1\), so the total work scales linearly with \(n\).

---

### Try this Question

??? question " Q1. $ \quad T(n) = T(n-1)+n, \quad T(1) = 1 $ "

      $$ T(n) = T(n-1)+n, \quad T(1) = 1 $$

      **Step 1. Unroll the Recurrence**

      Start expanding:

      $$ T(n) = T(n-1) + n $$

      $$ T(n-1) = T(n-1-1) + n-1  \quad\implies\quad T(n) = (T(n-2) + n-1) + n $$

      $$ T(n-2) = T(n-2-1) + n-2 \quad\implies\quad T(n) = ((T(n-3)+ n-2) + n-1) + n $$

      $$ T(n-3) = T(n-3-1) + n-3  \quad\implies\quad T(n) = ((T(n-4)+n-3)+n-2)+n-1+n $$

      After \(k\) steps, the pattern is:

      $$      T(n) = T(n-k) + (n-k+1) + (n-k+2) + (n-k+3) ... n $$

      **Step 2. Stop at the Base Case**

      Pick \(k\) so that \(n - k\) hits the base index 1:


      $$ n - k = 1 \quad\Rightarrow\quad k = n - 1 $$

      Now substitute \(k = n - 1\) into the pattern:

      $$
      T(n) = T(1) + 2 +3 + 4 +...+n
      $$

      **Step 3. Plug In Your Base**

      $$
      T(n) = T(1) + 2 + 3 + 4 + ... + (n-1) + n \newline
            = 1 + 2 + 3 + 4 + ... + n
      $$

     Since we can observe that the algorithm tends to behave as a sum of first \(n\) integers

     $$ 1 + 2 + 3 + 4 + ... + n = \frac{n(n+1)}{2} $$

     So,
     $$ T(n) = \frac{n(n+1)}{2} $$

     **step 4. Final Result (Asymptotics)**

      $$
      \boxed{T(n) = \Theta(n^2)}
      $$

<!-- Seecond Question -->

??? question " Q2. $ \quad T(n) = T(n/2)+1, \quad T(1) = 1 $ "

      $$ T(n) = T(n-1)+n, \quad T(1) = 1 $$

      **Step 1. Unroll the Recurrence**

      Start expanding:

      $$ T(n) = T(n-1) + n $$

      $$ T(n-1) = T(n-1-1) + n-1  \quad\implies\quad T(n) = (T(n-2) + n-1) + n $$

      $$ T(n-2) = T(n-2-1) + n-2 \quad\implies\quad T(n) = ((T(n-3)+ n-2) + n-1) + n $$

      $$ T(n-3) = T(n-3-1) + n-3  \quad\implies\quad T(n) = ((T(n-4)+n-3)+n-2)+n-1+n $$

      After \(k\) steps, the pattern is:

      $$      T(n) = T(n-k) + (n-k+1) + (n-k+2) + (n-k+3) ... n $$

      **Step 2. Stop at the Base Case**

      Pick \(k\) so that \(n - k\) hits the base index 1:


      $$ n - k = 1 \quad\Rightarrow\quad k = n - 1 $$

      Now substitute \(k = n - 1\) into the pattern:

      $$
      T(n) = T(1) + 2 +3 + 4 +...+n
      $$

      **Step 3. Plug In Your Base**

      $$
      T(n) = T(1) + 2 + 3 + 4 + ... + (n-1) + n \newline
            = 1 + 2 + 3 + 4 + ... + n
      $$

     Since we can observe that the algorithm tends to behave as a sum of first \(n\) integers

     $$ 1 + 2 + 3 + 4 + ... + n = \frac{n(n+1)}{2} $$

     So,
     $$ T(n) = \frac{n(n+1)}{2} $$

     **step 4. Final Result (Asymptotics)**

      $$
      \boxed{T(n) = \Theta(n^2)}
      $$
