## 2. Recursion Tree Method

- Represent the recurrence as a **tree of recursive calls**.
- Each level of the tree corresponds to one stage of recursion.
- Calculate the total cost by summing work done at each level.
- Helps visualize how cost is distributed across recursive calls.
- **Example:** Merge Sort recurrence forms a balanced binary tree.

---

## 3. Substitution Method (Induction Method)

- Guess the solution (closed-form or Big-O).
- Use **mathematical induction** to prove the guess is correct.
- Commonly used for formal correctness proofs.
- **Example:**  
  Guess \(T(n) = O(n \log n)\) for Merge Sort, then prove by induction.

---

## 4. Telescoping (Backward Substitution)

- Special form of the iterative method where terms **cancel out** when expanded.
- Works best when recurrence has differences between consecutive terms.
- **Example:**  
  \[
  T(n) = T(n-1) + \frac{1}{n}
  \]  
  Expands into a **harmonic series** that telescopes.

---

## 5. Master Theorem

- A direct formula to solve **divide and conquer** recurrences:  
  \[
  T(n) = a \cdot T\!\left(\frac{n}{b}\right) + f(n)
  \]
- Provides asymptotic complexity based on comparison of \(f(n)\) with \(n^{\log_b a}\).
- Three main cases:
  - Case 1: \(f(n)\) grows slower → \(T(n) = \Theta(n^{\log_b a})\)
  - Case 2: \(f(n)\) grows equally → \(T(n) = \Theta(n^{\log_b a} \cdot \log n)\)
  - Case 3: \(f(n)\) grows faster → \(T(n) = \Theta(f(n))\) (with regularity condition)

---

## Summary

- **Iterative Method** → Expand step by step.
- **Recursion Tree** → Visualize and sum across levels.
- **Substitution Method** → Guess and prove with induction.
- **Telescoping** → Cancel terms to simplify.
- **Master Theorem** → Direct formula for divide & conquer recurrences.
