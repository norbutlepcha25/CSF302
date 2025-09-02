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

## 3.2 METHODS OF SOLVING RECURRENCE RELATIONS

When analyzing recursive algorithms, we use different techniques to solve **recurrence relations** and find their closed-form or asymptotic complexity.  
Here are the main methods:

1. Iterative Method
2. Recursion tree
3. Substitution Method
4. Telescoping
5. Master theorem

---

### 3.2.1. Iterative Method (Expansion Method)

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

#### Try this Question

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

<!-- Second Question -->

??? question " Q2. $ \quad T(n) = T(n/2)+1, \quad T(1) = 1 $ "

      $$ T(n) = T(n/2)+1, \quad T(1) = 1 $$

      **Step 1. Unroll the Recurrence**

      Start expanding:

      $$ T(n) = T(n/2) + 1 $$

      $$ T(n/2) = T(n/4) + 1  \quad\implies\quad T(n) = T(n/4) +  2 $$

      $$ T(n/4) = T(n/8) + 2 \quad\implies\quad T(n) = T(n/8)+ 3 $$

      $$ T(n/8) = T(n/16) + 3  \quad\implies\quad T(n) = T(n/16) + 4 $$

      After \(k\) steps, the pattern is:

      $$      T(n) = T(n/2^k) + k $$

      **Step 2. Stop at the Base Case**

      Pick \(k\) so that \(n/2^k\) hits the base index 1:


      $$ n/2^k = 1 \quad\Rightarrow\quad k = c . log n $$

      Now substitute \(k = clog n\) into the pattern:

      $$
      T(n) = T(1) + c.log n
      $$

      **Step 3. Plug In Your Base**

      $$
      T(n) = T(1) + c.log n \newline
            = 1 + c.logn
      $$


     **step 4. Final Result (Asymptotics)**

      $$
      \boxed{T(n) = \Theta (logn)}
      $$

#### Practice set 1 of [Practice Questions](questions.md):

### 3.2.2 Recursion Tree Method

In a recursion tree, each node represents the cost of a **_single subproblem_** somewhere in the set of recursive function invocations.
We sum the costs within each level of the tree to obtain a set of per-level costs, and then we sum all the per-level costs to determine the total cost of all levels of the recursion

Steps

1.  Write the recurrence $ \quad T(n)=aT(n/b)+f(n) $

2.  Expand the recurrence (first few levels)

                1. Root: cost = 𝑓(𝑛)
                2. Level 1: 𝑎 subproblems, each of size (𝑛/𝑏)
                3. cost per node = 𝑓(𝑛/𝑏)
                4. Total cost at level 1 = 𝑎⋅𝑓(𝑛/𝑏)

3.  Generalize the cost at level 𝑖

    $$ Level cost = 𝑎^𝑖⋅𝑓(𝑛/𝑏^𝑖) $$

4.  Find the depth of the tree

            Stop when subproblem size = 1

5.  Add up costs across levels

$$
T(n) = \sum_{i=0} ^ {\log_b n} a^i \cdot f\!\left(\frac{n}{b^i}\right)
$$

Evaluate the sum Simplify the expression to get asymptotic complexity (Θ, O, etc.).

!!! example "Example 1:"

      - for a given recurrence relation $\quad T(n)=2T(n/2)+n $
      - Level 0 : root node

      <div class="center-mermaid">

      ```mermaid
            flowchart TD
            A@{shape : rect, label: "n"}


      ```
      </div>

      - Level 1

    !!! info inline end "Cost of Level 1"
        Level cost = 𝑎^𝑖⋅ 𝑓(𝑛/𝑏^𝑖)

        cost =$ \frac{n}{2}+\frac{n}{2} = 2\frac{n}{2}= cn $

    !!! info inline start "At Level 1"
        The problem will be subdivided into ***2*** numbers with a cost of ***(n/2)***

       <div class="center-mermaid">
      ```mermaid
            flowchart TD
            A["n"] --> B1["n/2"]
            A --> B2["n/2"]

      ```
      </div>


      - Level 2

    !!! info inline end "Cost of Level 2"
        Level cost = 𝑎^𝑖⋅ 𝑓(𝑛/𝑏^𝑖)

        cost = $ \frac{n}{4}+\frac{n}{4}+\frac{n}{4}+\frac{n}{4} = 4\frac{n}{4} = cn $

      ```mermaid
            flowchart TD
            A["n"] --> B1["n/2"]
            A --> B2["n/2"]

            B1 --> C1["n/4"]
            B1 --> C2["n/4"]

            B2 --> C3["n/4"]
            B2 --> C4["n/4"]

      ```


      5. Until i level


      ```mermaid
            flowchart TD
            A["n"] --> B1["n/2"]
            A --> B2["n/2"]

            B1 --> C1["n/4"]
            B1 --> C2["n/4"]

            B2 --> C3["n/4"]
            B2 --> C4["n/4"]

            C1 --> D1["T(1)"]
            C2 --> D2["T(1)"]
            C3 --> D3["T(1)"]
            C4 --> D4["T(1)"]

      ```

      6. Total Cost
      From the tree we observe that the sum at each level of "cn", thus we can conclude for depth till "i" , the sum will be i * n or as per the formula

      $$
      T(n) = \sum_{i=0} ^ {\log_2 n} cn \implies T(n) = cn \sum_{i=0} ^ {\log_2 n} 1
      $$

      $$
      T(n) = cn . {\log n} \implies \Theta (nlogn)
      $$

      **Final Result (Asymptotics)**

      $$
      \boxed{T(n) = \Theta (nlogn)}
      $$

#### Try this Question

<!-- Question 1 -->

??? question " Q1. $ \quad T(n) = 3T(n/2)+n, \quad T(1) = 1 $ "

      - for a given recurrence relation $\quad T(n)=3T(n/2)+ cn $
      - Level 0 : root node

      <div class="center-mermaid">

      ```mermaid
            flowchart TD
            A@{shape : rect, label: "n"}


      ```
      </div>


      - Level 1

    !!! info inline end "Cost of Level 1"
        Level cost = 𝑎^𝑖⋅ 𝑓(𝑛/𝑏^𝑖)

        cost = $ \frac{n}{2} + \frac{n}{2} + \frac{n}{2} = 3\frac{n}{2}  $

    !!! info inline start "At Level 1"
        subdivided into ***3*** numbers with a cost of ***(n/2)***


       <div class="center-mermaid">
      ```mermaid
            flowchart TD
            A["n"] --> B1["n/2"]
            A --> B2["n/2"]
            A --> B3["n/2"]

      ```
      </div>

      - Level 2

    !!! info inline end "Cost of Level 2"


        cost = $ 3\frac{n}{4} + 3\frac{n}{4} + 3\frac{n}{4} \newline = 9\frac{n}{4} \newline = (\frac {3}{2})^2 n $

      ```mermaid
            flowchart TD
            A["n"] --> B1["n/2"]
            A --> B2["n/2"]
            A --> B3["n/2"]

            B1 --> C1["n/4"]
            B1 --> C2["n/4"]
            B1 --> C3["n/4"]

            B2 --> C4["n/4"]
            B2 --> C5["n/4"]
            B2 --> C6["n/4"]

            B3 --> C7["n/4"]
            B3 --> C8["n/4"]
            B3 --> C9["n/4"]

      ```


       4. Level 3

    !!! info inline end "Cost of Level 3"


        cost = $ 3\frac{n}{8} + 3\frac{n}{8} + 3\frac{n}{8} ... \newline = 36\frac{n}{8} \newline = (\frac {3}{2})^3 n $

      ```mermaid
            flowchart TD
            A["n"] --> B1["n/2"]
            A --> B2["n/2"]
            A --> B3["n/2"]

            B1 --> C1["n/4"]
            B1 --> C2["n/4"]
            B1 --> C3["n/4"]

            B2 --> C4["n/4"]
            B2 --> C5["n/4"]
            B2 --> C6["n/4"]

            B3 --> C7["n/4"]
            B3 --> C8["n/4"]
            B3 --> C9["n/4"]

            C1 --> D1["n/8"]
            C1 --> D2["n/8"]
            C1 --> D3["n/8"]



      ```


      Until i level
    !!! info inline end "Cost of Level i"

           cost =  $ (\frac {3}{2})^i n $



      ```mermaid
            flowchart TD
            A["n"] --> B1["n/2"]
            A --> B2["n/2"]
            A --> B3["n/2"]

            B1 --> C1["n/4"]
            B1 --> C2["n/4"]
            B1 --> C3["n/4"]

            B2 --> C4["n/4"]
            B2 --> C5["n/4"]
            B2 --> C6["n/4"]

            B3 --> C7["n/4"]
            B3 --> C8["n/4"]
            B3 --> C9["n/4"]

            C1 --> D1["n/8"]
            C1 --> D2["n/8"]
            C1 --> D3["n/8"]


            D1 --> E1["T(1)"]
            D2 --> E2["T(1)"]
            D3 --> E3["T(1)"]


      ```
      ```

      Total Cost = $ \sum $ cost of each level


      $ = n + \frac{3}{2} + \frac{9}{4} + \frac{27}{8} + ... + (\frac{3}{2})^i $
      $ \newline = n (1 + \frac{3}{2} + (\frac{3}{2})^2 + (\frac{3}{2})^3 + .... + (3/2)^i) $

      We can observe that the sum of all the levels tends to follow the summation of n numbers for a GEOMETRIC SERIES pattern, thus we can reduce it in the form of sum of GP series

      $ \newline = n (\frac{ 1 -(3/2)^{k+1}}{1- 3/2})  $

    !!! info "Sum of Geometric Series"
         $$ S= a( \frac{1-r^n}{1-r}) $$
         where  r = common ratio, n = number of terms, a = first term

      on solving:

      $$ T(n) = 2n((3/2)^{k+1}-1) $$

      as k tends to $ \infty $ , -1 becomes negligible

      $$ T(n) \approx 2n((3/2)^{k+1}) $$

      and the value for k = height of tree, k = log n

      $$
      \approx 2n((3/2)^{\log_2 n +1})
      $$
      $$
      \approx 2n((3/2)^{\log_2 n})(3/2)^{1}
      $$
      $$
      \approx 3n((3/2)^{\log_2 n})
      $$
    !!! info "Log Property"
         $$ a^{ \log_b n} = n^{\log_b a} $$

      $$
      \approx 3n((n)^{\log_2 3/2})
      $$
      $$
      \approx 3((n)^{1 + \log_2 3/2})
      $$

      simplfy the exponent part
      $$
      1 + \log_2 3/2 \newline
      = 1+ \log_2 3 - \log_2 2
      = \log_2 3
      $$

      therefore
      $$
      T(n) \approx 3n^{log_2 3}
      $$


      **Final Result (Asymptotics)**

      $$
      \boxed{T(n) = \Theta (n^{1.585})}
      $$
