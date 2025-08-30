# Unit 3

## Recurrences & Analysis of Algorithms

## 3.1 Recurrences & Master Theorem (Analysis)

### 3.1.1 Introduction to Recurrence Relations

- A **recurrence relation** is an equation that defines a sequence based on its previous terms.
- Used to describe the running time of recursive algorithms.
- Example:
  - Binary Search: `T(n) = T(n/2) + O(1)`
  - Merge Sort: `T(n) = 2T(n/2) + O(n)`

### 3.1.2 Types of Recurrences

1. **Linear Recurrence** – depends linearly on smaller subproblems.
   - Example: `T(n) = T(n-1) + O(1)`
2. **Divide-and-Conquer Recurrence** – splits into multiple subproblems.
   - Example: `T(n) = aT(n/b) + f(n)`
3. **Homogeneous vs. Non-Homogeneous**
   - Homogeneous: depends only on subproblems (`T(n) = 2T(n/2)`).
   - Non-Homogeneous: includes an additional function (`T(n) = 2T(n/2) + n`).

### 3.1.3 Overview of the Master Theorem

- Provides an efficient way to solve divide-and-conquer recurrences:  
  `T(n) = aT(n/b) + f(n)`  
  where
  - `a ≥ 1`: number of subproblems
  - `b > 1`: factor by which input is divided
  - `f(n)`: cost outside recursion

---

## 3.2 Merge Sort Analysis

### 3.2.1 Merge Sort Algorithm Review

- Divide array into two halves.
- Recursively sort each half.
- Merge the two sorted halves.
- Time complexity analyzed using recurrence.

### 3.2.2 Deriving the Recurrence Relation for Merge Sort

- Each split divides the array into two parts.
- Work for merging is `O(n)`.
- Recurrence:  
  `T(n) = 2T(n/2) + O(n)`

### 3.2.3 Solving the Merge Sort Recurrence

- Using Master Theorem:
  - `a = 2, b = 2, f(n) = n`
  - Compare `n^(log_b a) = n^(log_2 2) = n` with `f(n) = n`.
  - Case 2 ⇒ `T(n) = Θ(n log n)`

---

## 3.3 Recursion Trees

### 3.3.1 Constructing Recursion Trees

- Expand recurrence into a tree where each node represents a subproblem.
- Each level shows the cost at that stage.

### 3.3.2 Analyzing Recurrences Using Recursion Trees

- Compute cost at each level.
- Sum over all levels to get total complexity.

### 3.3.3 Advantages and Limitations of the Recursion Tree Method

- **Advantages**: Intuitive visualization, useful for deriving guesses.
- **Limitations**: Informal, requires verification using substitution.

---

## 3.4 Telescoping Method

### 3.4.1 Principles of Telescoping Series

- In telescoping, terms cancel out across steps.
- Example: `T(n) = T(n-1) + n` expands to a series where most terms cancel.

### 3.4.2 Applying Telescoping to Solve Recurrences

- Write recurrence in expanded form.
- Observe cancellation of terms.
- Derive closed form.
- Example: `T(n) = T(n-1) + n` ⇒ `T(n) = O(n^2)`.

---

## 3.5 Solving Recurrences: Substitution Method

### 3.5.1 Steps in the Substitution Method

1. Guess a solution.
2. Use induction to prove upper and/or lower bounds.

### 3.5.2 Guessing the Solution

- Make an educated guess from expansion or recursion tree.

### 3.5.3 Proving the Guess by Induction

- Base case: check for smallest `n`.
- Induction step: assume for `k < n`, prove for `n`.

---

## 3.6 Solving Recurrences: Recursion-Tree Method

### 3.6.1 Detailed Steps for Constructing Recursion Trees

1. Write recurrence.
2. Expand into levels of recursion.
3. Assign costs to each level.

### 3.6.2 Analyzing the Tree to Obtain Asymptotic Bounds

- Sum costs level by level.
- Identify dominating term.

### 3.6.3 Comparing Recursion-Tree Method with Other Methods

- Easier than substitution for intuition.
- Less formal – requires confirmation.
- Master Theorem provides direct solution when applicable.

---

## 3.7 Solving Recurrences: Master Method

### 3.7.1 Statement of the Master Theorem

For `T(n) = aT(n/b) + f(n)`:

- Compare `f(n)` with `n^(log_b a)`.

### 3.7.2 Three Cases of the Master Theorem

1. If `f(n) = O(n^(log_b a - ε))`, then `T(n) = Θ(n^(log_b a))`.
2. If `f(n) = Θ(n^(log_b a))`, then `T(n) = Θ(n^(log_b a) log n)`.
3. If `f(n) = Ω(n^(log_b a + ε))` and regularity condition holds, then `T(n) = Θ(f(n))`.

### 3.7.3 Applying the Master Theorem to Common Recurrences

- Merge Sort: `T(n) = 2T(n/2) + n` ⇒ Case 2 ⇒ Θ(n log n).
- Binary Search: `T(n) = T(n/2) + 1` ⇒ Case 1 ⇒ Θ(log n).
- Strassen’s Matrix Multiplication: `T(n) = 7T(n/2) + n^2` ⇒ Case 1 ⇒ Θ(n^log₂7).

### 3.7.4 Limitations and Extensions of the Master Theorem

- Does not apply when:
  - Non-polynomial `f(n)` (e.g., `n/log n`).
  - Unbalanced recursions.
- **Extended Master Theorem** and **Akra-Bazzi theorem** handle more complex recurrences.
