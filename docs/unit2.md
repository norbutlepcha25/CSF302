# Unit 2

## 2.1 Fundamentals

!!! note "Defination of Algorithms"

    Algorithms are a set of finite rules or instructions to be followed in calculations or other problem-solving operations

### 2.1.1 Features of Algorithm

1. Every algorithm must satisfy the following Criteria:

2. Input: there are zero or more quantities, which are externally supplied;

3. Output: at least one quantity is produced;

4. Definiteness: each instruction must be clear and unambiguous;

5. Finiteness: if we trace out the instructions of an algorithm, then for all cases the algorithm will terminate after a finite number of steps;

6. Effectiveness: every instruction must be sufficiently basic that it can in
   principle be carried out by a person using only pencil and paper. It is not enough that each operation be definite, but it must also be feasible.

## **2.2 Asymptotic Analysis**

<img src="img/asymptoticgraph.png" alt="Logo" width="100%">

### 2.1.1 Concept of Growth Rates

- Growth rate describes how the running time of an algorithm increases as the input size grows. We consider only the leading term of a formula **_(e.g., an^2^)_**, since the lower-order terms are
  relatively insignificant for large values of n. We also ignore the leading term’s constant coefficient, since constant factors are less significant than the rate of growth
  in determining computational efficiency for large inputs.
- Example: Linear (O(n)), Quadratic (O(n²)), Logarithmic (O(log n)).
- Helps compare algorithms independently of hardware.

!!! warning "For lower value of input some worst case may perform better"

    We usually consider one algorithm to be more efficient than another if its worstcase running time has a lower order of growth. Due to constant factors and lowerorder terms, an algorithm whose running time has a higher order of growth might take less time for small inputs than an algorithm whose running time has a lower2.3 Designing algorithms 29 order of growth. But for large enough inputs, a ‚.n2/ algorithm, for example, will run more quickly in the worst case than a ‚.n3/ algorithm.

### 2.1.2 Best-case, Worst-case, and Average-case Analysis

- **Best-case:** Minimum time an algorithm takes for any input (optimistic).
- **Worst-case:** Maximum time an algorithm takes (pessimistic, most commonly used).
- **Average-case:** Expected time over all inputs (realistic measure).

### 2.1.3 Importance of Asymptotic Analysis in Algorithm Design

- Provides machine-independent evaluation of algorithms.
- Helps predict scalability for large input sizes.
- Guides selection of efficient algorithms.

---

## 2.2 Model of Computation (Word-RAM)

### 2.2.1 Basic Operations and Their Time Complexity

- Arithmetic (+, -, \*, /), comparisons, and assignments assumed **O(1)**.
- Array access and pointer dereferencing also **O(1)**.

### 2.2.2 Memory Model and Addressing

- Memory is modeled as an array of words (fixed size).
- Each word can be accessed in constant time.
- Suitable for analyzing most modern computers.

### 2.2.3 Comparison with Other Computation Models

- **Turing Machine:** Theoretical, less practical for real hardware analysis.
- **PRAM (Parallel RAM):** Models parallel computing.
- **Word-RAM:** Balances practicality and simplicity.

---

## 2.3 Role of Algorithms in Computing

### 2.3.1 Historical Perspective on Algorithms

- Algorithms date back to ancient mathematics (Euclid’s GCD algorithm).
- Modern computing relies on algorithmic foundations.

### 2.3.2 Importance of Efficient Algorithms in Modern Computing

- Efficiency saves time and resources.
- Critical in big data, AI, cybersecurity, and distributed systems.

### 2.3.3 Real-world Applications of Algorithm Analysis

- Search engines, data compression, cryptography, scheduling, and machine learning.

---

## 2.4 Analyzing and Designing Algorithms

### 2.4.1 Principles of Algorithm Design

- Divide and Conquer, Dynamic Programming, Greedy strategies.
- Aim for correctness, clarity, and efficiency.

### 2.4.2 Trade-offs Between Time and Space Complexity

- Faster algorithms may use more memory (e.g., precomputed tables).
- Memory-efficient algorithms may be slower.

---

## 2.5 O-notation, Ω-notation, and Θ-notation

### 2.5.1 O-notation (Upper Bound)

- Describes the **worst-case upper limit** on growth rate.
- Example: f(n) = 3n² + 2n + 1 ∈ O(n²).

### 2.5.2 Ω-notation (Lower Bound)

- Describes the **minimum growth rate** of an algorithm.
- Example: f(n) = 3n² + 2n + 1 ∈ Ω(n²).

### 2.5.3 Θ-notation (Tight Bound)

- When both upper and lower bounds are the same.
- Example: f(n) = 3n² + 2n + 1 ∈ Θ(n²).

### 2.5.4 Relationships Between Notations

- If f(n) ∈ Θ(g(n)), then f(n) ∈ O(g(n)) and f(n) ∈ Ω(g(n)).

---

## 2.6 Standard Notation & Common Functions

### 2.6.1 Polynomial Functions and Their Growth Rates

- n, n², n³ … grow faster as degree increases.
- Example: n³ grows faster than n².

### 2.6.2 Logarithmic and Exponential Functions

- log n grows very slowly, exponential (2ⁿ) grows very fast.
- Example: log₂(1024) = 10, but 2¹⁰ = 1024.

### 2.6.3 Floor and Ceiling Functions

- Floor ⌊x⌋: Largest integer ≤ x.
- Ceiling ⌈x⌉: Smallest integer ≥ x.

### 2.6.4 Factorial and Combinatorial Functions

- n! = n × (n-1) × … × 1 (grows extremely fast).
- Useful in probability, combinatorics, and complexity analysis.

---

## ✅ Key Takeaways

- Asymptotic analysis helps compare algorithms abstractly.
- Word-RAM is the standard computation model for analysis.
- Big-O, Ω, Θ notations formalize algorithm growth rates.
- Real-world efficiency depends on balancing time and space trade-offs.

### addtional reading

### presentation and notes
