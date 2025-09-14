# Unit 3: Recurrence Relations and Master Theorem

!!! info "Learning outome"

    Assess the efficiency of different approaches to solving recurrence relations, including the substitution method, recursion-tree method, and master method.

## **3.1 Recurrences**

### 3.1.1 Introduction

What is **<unit3:Recurrence>?**

A recurrence is an equation (or inequality) that defines a function in terms of its value(s) at smaller input(s).It’s a way of expressing a problem’s solution in terms of **_smaller subproblems_** of the same type. In simple terms, we can say that when a function calls itself within that function, only the parameter are different, which is usally the smaller sub problem.

What is a **recurrence relations**?

A **recurrence relation** is an {== equation that defines a sequence based on its previous terms ==}. A recurrence relation is the actual formula that shows how the current value depends on previous values.

For example:

Factorial recurrence:
$ T(𝑛)=𝑛.T(𝑛-1), T(0)=1 $

This means factorial of 𝑛 is defined in terms of factorial of 𝑛−1.

### 3.1.2 General Form

\[
T(n) = a \cdot T\!\left(\frac{n}{b}\right) + f(n)
\]

Where:

- \(T(n)\) → the time/space complexity of the problem of size \(n\)
- \(a\) → number of subproblems in the recursion
- \(n/b\) → size of each subproblem
- \(f(n)\) → the cost of dividing the problem and combining the results

---

### 3.1.3 Types of Recurrence Relations

1.  **Linear Recurrence** – depends linearly on smaller subproblems.
    Example: $T(n) = T(n-1) + O(1)$
2.  **Divide-and-Conquer Recurrence** – splits into multiple subproblems.
    Example: $T(n) = aT(\frac{n}{b}) + f(n)$

    - Homogeneous: depends only on subproblems ($T(n) = 2T(\frac{n}{2})$).
    - Non-Homogeneous: includes an additional function ($T(n) = 2T(\frac{n}{2}) + n$).

---

## 3.2 Methods of Solving Recurrence Relations

When analyzing recursive algorithms, we use different techniques to solve **recurrence relations** and find their {==closed-form or asymptotic complexity==}.  
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

### 3.2.3 Substitution Method

It is a method used to solve a recurrence relation by proving the guessed form of the relation.

The substitution method for solving recurrences comprises two steps:

1. Guess the form of the solution.
2. Use mathematical induction to find the constants and show that the solutionworks.
   We substitute the guessed solution for the function when applying the inductive hypothesis to smaller values; hence the name “substitution method.”

!!! example "Example 1"

    !!! info inline end "Note: General guess"
        - For divide-and-conquer recurrences = 𝑇(𝑛)=𝑂(𝑛log⁡𝑛).
        - For simple ones like 𝑇(𝑛)=𝑇(𝑛−1)+𝑛,  guess a polynomial.
      - step 1: Given recurrence relation
             $\quad T(n)=2T(\frac{n}{2})+n, \quad T(1) =1 $

      - step 2: Making a informed guess ( say using iterative or recursion tree)
            $$ T(n) = \Theta (n\log n) $$

      Testing the basis:

      We’ll try to prove that the guess for upper bound T(n)=O(nlog⁡n) is true for all cases using induction method

      By definition : $ T(n) ≤ c(nlogn) \quad for \quad Ǝ c > 0, ∀n > n0 $

      Basis : for $ n = 1, \newline T(1) ≤ c(1log1) : fails, \therefore n > 1 $

      Basis : for $ n = 2 \newline
      T(2) ≤ c(2log2) \newline
      4 ≤ 2c  $

      Therefore we need value of c >2 and n>1
      So we can conclude that the eq 1 hold true for all value of n ≥ 2,
      i.e 2, 3, 4 ,.... Kth term

      - step 3: Inductive Hypothesis

      Assuming n = k for all value of $ 2 ≤ k ≤ n $
    $$ T(k) ≤ c(klogk)  $$

    It implies that the condition would hold true for $ k = n/2 $
    	$$ T(\frac{n}{2}) ≤ c(\frac{n}{2} \log \frac{n}{2}) $$

      - step 4: Substitute it back
      $$ Thus, \quad T(n) = 2T(\frac{n}{2}) + n \newline $$
    	$$≤ 2 (c(\frac{n}{2} \log \frac{n}{2}))  + n          $$
    	$$ ≤ cn (\log \frac{n}{2})  + n         $$
      $$ ≤ cn (\log n - 1) + n $$
      $$ ≤ cn log n + n (1 - C) $$
      $$ \approx T(n) = \Theta( n \log n ) $$
      Hence proved

#### Try this Question

<!-- Question 1 -->

??? question " Q1. $ \quad T(n) = 2T(n-1)+1, \quad T(1) = 1 $ "

      - step 1: Given recurrence relation
      $$ \quad T(n) = 2T(n-1)+1, \quad T(1) = 1 $$

      - step 2 : Guessing a solution
      $$ T(n)=2^n - 1 $$

          for upper bound $ T(n) ≤ \Theta (2^n - 1) $


          Basis for n = 1
          $$ T(1) ≤ C(1), Holds True$$

          So we can conclude that the eq 1 hold true for all value of n ≥ 1,
          i.e 1, 2, 3, 4 ,.... Kth term


      - step 3 : Inductive Hypothesis

        Assuming n  ≥ k for all values 1 ≤ k ≤ n
    				$$ T(k) ≤ c(2^k - 1) $$

        Therefore $ K= n-1 $ should also hold true
    				$$ T(n-1) ≤ c(2^{n-1} - 1) $$

        Thus, $$T(n) = 2T(n-1) + 1 $$
    		      $$ ≤ 2 (c(2^{n-1} - 1)) + 1 $$
    		      $$ ≤ 2c2^{n-1} - 2  + 1 $$
                  $$ ≤ c2^n - 1 $$
                  Hence proved

<!-- Question 2 -->

??? question " Q1. $ \quad T(n) = T(n-1)+n, \quad T(1) = 1 $ "

      - step 1: Given recurrence relation
      $$ \quad T(n) = T(n-1)+n, \quad T(1) = 1 $$

      - step 2 : Guessing a solution
      $$ T(n)=\Theta (n^2) $$

          for upper bound $ T(n) ≤ c (n^2)$


          Basis for n = 1
          $$ T(1) ≤ C(1), Holds True$$

          So we can conclude that the eq 1 hold true for all value of n ≥ 1,
          i.e 1, 2, 3, 4 ,.... Kth term


      - step 3 : Inductive Hypothesis

        Assuming n  ≥ k for all values 1 ≤ k ≤ n
    				$$ T(k) ≤ c(k^2) $$

        Therefore $ K= n-1 $ should also hold true
    				$$ T(n-1) ≤ c((n-1)^2) $$

        Thus, $$T(n) = T(n-1) + n $$
    		      $$ ≤ c((n-1)^{2}) + n $$
    		      $$ ≤ c(n^2 - 2n + 1)  + n $$
                  $$ ≤ cn^2 - 2cn + c +n  $$
                  Hence proved

         OR futher checking
         We want to show $ 𝑇(𝑛)≤𝑐𝑛^2 $

         That means checking if:
          $$ 𝑐𝑛^2−2𝑐𝑛+𝑐+𝑛  ≤   𝑐𝑛^2  $$

         Cancel $ 𝑐𝑛^2 $ on both sides:

         $$ −2𝑐𝑛+𝑐+𝑛  ≤   0 $$
         $$ n(1-2c)+c ≤  0 $$

         If we choose $ 𝑐 ≥ 1 $ then $ n(1-2c) ≤ -1 $ so the inequality holds for all sufficiently large values

### 3.2.4 Master Theorem

#### 1. Master Theorem (Classic)

**Definition:**  
The Master Theorem provides a method to determine the asymptotic time complexity of divide-and-conquer recurrences of the form:

$$
T(n) = a \, T\left(\frac{n}{b}\right) + f(n)
$$

Where:

- \(a \ge 1\) → number of subproblems
- \(b > 1\) → factor by which the problem size is divided
- \(f(n)\) → non-recursive work done per call

**Cases:**

!!! success "Case 1: **Recursion dominates:**"

    $$
    if \quad f(n) = O(n^{\log_b a - \epsilon}) \; for \; some \; constant \; \epsilon > 0  \quad Result: T(n) = \Theta(n^{\log_b a})
    $$

!!! success "Case 2: **Balanced:**"

    $$
    f(n) = \Theta(n^{\log_b a}) \quad Result:T(n) = \Theta(n^{\log_b a} \log n)
    $$

!!! success "case 3: **Outside work dominates:**"

    $$
    f(n) = \Omega(n^{\log_b a + \epsilon}) \; for \; some \; constant \; \epsilon > 0  \quad \text{(with regularity condition)} \quad Result:T(n) = \Theta(f(n))
    $$

    regualarity Condition:
    $$ af(\frac{n}{b}) \le cf(n) $$
    for some constant c < 1 and all sufficiently large n, then
    $$ Result : T(n) = \Theta (f(n)) $$

---

**Steps for Master Theorem**

- From the equation note the values of a, b and $ f(n)$
- calculate the thershold function $ n^{\log_b a} $, let be denoted as $ g(n) $
- compare $f(n)$ with $g(n)$ and check which category it falls into
- Note down the final result

!!! example "Example 1"

     **Q1. $ T(n) = 4T(\frac{n}{2}) + n $**

      step 1: from the given equation noting the required value : $ a = 4, b = 2, f(n) = n$

      step 2: Calcuating Threshold function : $ g(n) = n^{\log_b n} \implies g(n) = n^{\log_2 4} \implies g(n) = n^2$

      step 3: compare the $f(n)$ and $ g(n)$

      $$ f(n) \le g(n) $$
      $$ n \le n^2 $$

      step 4: Case 1 condition satisfied $f(n) = O (n^{log_b a- \epsilon}) $ where $\epsilon > 0$ i.e, $\epsilon = 1$

      step 5: Result : $ T(n) = \Theta (n^ {log_b a} )$
      $$
      \boxed{T(n) = \Theta (n^ 2)}
      $$

      **Q2. $ T(n) = T(\frac{n}{2}) + 1$**

      step 1: from the given equation noting the required value : $ a = 1, b = 2, f(n) = 1$

      step 2: Calcuating Threshold function : $ g(n) = n^{\log_b n} \implies g(n) = n^{\log_2 1} \implies g(n) = n^0 = 1$

      step 3: compare the $f(n)$ and $ g(n)$

      $$ f(n) = g(n) $$
      $$ 1 = 1 $$

      step 4: Case 2 condition satisfied $f(n) = \theta (n^{log_b a}) $

      step 5: Result : $ T(n) = \Theta (n^ {log_b a} \log n)$
      $$
      \boxed{T(n) = \Theta (log n)}
      $$
       **Q3. $ T(n) = 2T(\frac{n}{2}) + n^4$**

      step 1: from the given equation noting the required value : $ a = 2, b = 2, f(n) = n^4$

      step 2: Calcuating Threshold function : $ g(n) = n^{\log_b n} \implies g(n) = n^{\log_2 2} \implies g(n) = n^1 = n$

      step 3: compare the $f(n)$ and $ g(n)$

      $$ f(n) > g(n) $$
      $$ n^4 = n $$

      step 4: Case 3 : thus, go for regularity condition check
      condition satisfied i.e, $af(\frac{n}{b}) \le cf(n) $

     $$af(\frac{n}{b}) \le cf(n) $$

      $$
      2 \cdot (n^{4} /2^{4}) \le c \cdot n^{4}
      $$
      $$
       (\frac{1}{8}) \le c \cdot 1
      $$

      $\therefore $ condition holds for the regularity check


      step 5: Result : $ T(n) = \Theta (n^ {4} )$

      $$
      \boxed{T(n) = \Theta (n^4)}
      $$

---

#### 2. Generalized Master Theorem

**Definition:**  
The Generalized Master Theorem generalizes the Master Theorem to handle recurrences where \(f(n)\) has **logarithmic factors**, i.e.,

$$
T(n) = a \, T\left(\frac{n}{b}\right) + f(n)
$$

where

$$
f(n) = \Theta(n^{\log_b a} \cdot \log^k n), \quad k \ge 0
$$

!!! tip ""

     Use this formula if there is no <unit3:polynomial growth> or directly when you use log function in the addtional cost for other function

!!! note "Intution behind the Generalized Master Theorem"

      Lets say for example a recurrence relation is represented by $T(n) = 2T(\frac{n}{2})+nlogn$

      if we used the Classic Master theorem than
      $$ a= 2, b=2, f(n) = n \log n$$

      - calculating the $g(n)$, we get $g(n)= n$

      - comparing $f(n)$ and $g(n)$, we can see that $f(n)$ is greater than $g(n)$ and we might say that CASE 3 applies and proceed to check the regularity condition. However, that would be an **{==Error==}** as the function $f(n)$ is growing logrithmically with respect to $g(n)$ and not polynomially. (see <unit3:polynomial Growth>). Thus classic master theorem cannot be applied to this recurrence relation.

      - for such recurrence relations we use the generalized master theorem which takes into account the logarithmic factors

!!! success "Case 1: **k > -1**"

    $$
    T(n) = \Theta(n^{\log_b a} \log^{k+1} n)
    $$

!!! success "Case 2: **k = -1**"

    $$
    T(n) = \Theta(n^{\log_b a} \log \log n)
    $$

!!! success "Case 3: **k < 1**"

    $$
    T(n) = \Theta(n^{\log_b a} )
    $$

!!! example "Example"

     **Q1. $ (T(n) = 2T(n/2) + n \log n\) $**

      $$ a=2, b=2, f(n)= n \log n k=1$$

      Classic Master theorem cannot be applied here thus, using the generalized Master theorem for $k=1$

      Result: $T(n) = \Theta(n^{\log_b a} \log^{k+1} n)$

      Thus final Answer:

      $$
      \boxed{T(n) = \Theta(n \log^2 n)}
      $$

#### 3. Extended Master Theorem

**Definition:**

$$
T(n) = a \, T\left(\frac{n}{b}\right) + f(n)
$$

where

$$
f(n) = \Theta(n^k \cdot \log^p n), \quad k \ge 0
$$

**Steps for Master Theorem**

- From the equation note the values of a, b , k and p
- calculate the $ b^k $
- compare $a$ with $b^k$ and check which category it falls into and the value of p
- Note down the final result

!!! success "Case 1: **$ a > b^k $** "

    $$
    T(n) = \Theta(n^{\log_b a})
    $$

!!! success "Case 2: **$ a = b^k $**"

      Then check the value of p

    $$ p > -1 \: then \: result \:  T(n) = \Theta(n^{k} \log^{p+1} n) $$

    $$
    p = -1 \: then \: result \:  T(n) = \Theta(n^{k} \log \log n)
    $$

    $$
    p < -1 \: then \: result \:  T(n) = \Theta(n^{k} )
    $$

!!! success "Case 3: **$ a < b^k $**"

    Then check the value of p

    $$ p \ge 0 \: then \: result \:  T(n) = \Theta(n^{k} \log^{p} n) $$

    $$
    p < 0 \: then \: result \:  T(n) = \Theta(n^{k})
    $$

### References
