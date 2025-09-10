# Divide and Conquer Algorithms

## 4.1 Fundamentals Divide & Conquer Algorithm Design

### 4.1.1 Principles and structure of divide and conquer algorithms

Definition:
Divide and Conquer is a problem-solving strategy that breaks a problem into smaller subproblems, solves them independently, and then combines their solutions to form the final answer.

General Steps:

Divide – Break the main problem into smaller subproblems of the same type.

Conquer – Solve the subproblems recursively. If the subproblem is small enough, solve it directly (base case).

Combine – Merge the solutions of the subproblems into a solution for the original problem.

```mermaid
flowchart TD
 A[Start: Problem of size n] --> B{Is n small enough?}
 B -->|Yes| C[Solve directly-base case]
 B-->|No| D[Divide problem into sub-problem]
 D --> E[Conquer: Solve subproblems recursively]
 E --> F[Combine solutions]
 F --> G[Final Solution]
 G --> H[End]
```

### 4.1.2 Advantages and limitations of divide and conquer

| **Advantages**                                                                                               | **Limitations**                                                                                                    |
| ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------ |
| **Efficiency** – Often reduces time complexity vs straightforward methods (e.g., merge sort vs bubble sort). | **Overhead of recursion** – Recursive calls use more memory (stack space) and may be inefficient for small inputs. |
| **Parallelism** – Independent subproblems can be solved in parallel.                                         | **Not always optimal** – Iterative solutions can be simpler/faster in some cases (e.g., linear search).            |
| **Simplicity in design** – Breaks problems into smaller, manageable parts.                                   | **Combination step cost** – If merging results is costly, performance suffers (e.g., merging in merge sort).       |
| **Reusability** – Same principle applies across many domains (sorting, searching, matrix multiplication).    | **Divide evenly issue** – Problems may not split evenly (e.g., quicksort with bad pivots).                         |
| **Reduces complexity in proofs** – Recursive definitions simplify correctness proofs.                        | **Implementation complexity** – Code can be harder to implement/debug compared to iterative methods.               |

## 4.2 Strassen’s Algorithm for Matrix Multiplication

### 4.2.1 Standard Matrix Multiplication

Given two 𝑛 × 𝑛 matrices(square matrix) 𝐴 and 𝐵, the product 𝐶 = 𝐴×𝐵 is also an 𝑛×𝑛 matrix where

$$
 𝐶_{𝑖𝑗}=∑_{𝑘=1}^𝑛𝐴_{𝑖𝑘}⋅𝐵_{𝑘𝑗}
$$

Pseudocode for Square Matrix Multiplication

!!! note ""

    ```text
    SQUARE MATRIX MULTIPLY(A, B)
        n = A.rows
        let C be a new n x n matrix
        for i = 1 to n
            for j = 1 to n
                C[i][j] = 0
                for k = 1 to n
                    C[i][j] = C[i][j] + A[i][k] * B[k][j]
    ```

From a standard matrix multiplication, for every element in the resultant matrix C has to perform **$n$** multiplication and **$(n-1)$** addition i.e, for example 2x2 matrix A multiplied with 2x2 matrix B, so to get the first element $C[i][j]$ it will take 2 multiplication and 1 addition.

### 4.2.2 Divide and conqure method for Matrix Multiplication

when we use a divide-and-conquer algorithm to compute the matrix product C = A.B, we **_assume that n is an exact power of 2_** in each of the nxn matrices. We make this assumption because in each divide step, we will
divide nxn matrices into four n/2 x n/2 matrices, and by assuming that n is an
exact power of 2, we are guaranteed that as long as $n \ge 2$, the dimension n=2 is an
integer.

Steps:

    1.Break down two 𝑛 × 𝑛 matrices into 4 submatrices of size 𝑛/2 × 𝑛/ 2.
    2.Multiply the submatrices recursively.
    3.Combine results to form the final product.

Pseudocode for matrix multiplication using divide and conquer

```
SQUARE-MATRIX-MULTIPLY-RECURSIVE (A, B)
1 n = A.rows
2 let C be a new nxn matrix
3 if n == 1
4     C[1][1] =  A[1][1].B[1][1]
5 else partition A, B, and C
6     C[1][1] = SQUARE-MATRIX-MULTIPLY-RECURSIVE(A[1][1].B[1][1]) +
                SQUARE-MATRIX-MULTIPLY-RECURSIVE(A[1][2].B[2][1])
7     C[1][2] = SQUARE-MATRIX-MULTIPLY-RECURSIVE(A[1][1].B[1][2]) +
                SQUARE-MATRIX-MULTIPLY-RECURSIVE(A[1][2].B[2][2])
8     C[2][1] = SQUARE-MATRIX-MULTIPLY-RECURSIVE(A[2][1].B[1][1]) +
                SQUARE-MATRIX-MULTIPLY-RECURSIVE(A[2][2].B[2][1])
9     C[2][2] = SQUARE-MATRIX-MULTIPLY-RECURSIVE(A[2][1].B[1][2]) +
                SQUARE-MATRIX-MULTIPLY-RECURSIVE(A[2][2].B[2][2])
10 return C
```

## Steps

Let:

$$
A =
\begin{bmatrix}
A_{11} & A_{12} \\
A_{21} & A_{22}
\end{bmatrix},
\quad
B =
\begin{bmatrix}
B_{11} & B_{12} \\
B_{21} & B_{22}
\end{bmatrix}
$$

Then the product is:

$$
C = A \times B =
\begin{bmatrix}
C_{11} & C_{12} \\
C_{21} & C_{22}
\end{bmatrix}
$$

where:

$$
\begin{aligned}
C_{11} &= A_{11}B_{11} + A_{12}B_{21} \\
C_{12} &= A_{11}B_{12} + A_{12}B_{22} \\
C_{21} &= A_{21}B_{11} + A_{22}B_{21} \\
C_{22} &= A_{21}B_{12} + A_{22}B_{22}
\end{aligned}
$$

---

## Recurrence Relation

- Each step requires **8 multiplications** of size \((n/2) \times (n/2)\), plus some additions.

\[
T(n) = 8T\left(\frac{n}{2}\right) + O(n^2)
\]

---

## Complexity (Master Theorem)

\[
T(n) = O(n^3)
\]

(same as classical matrix multiplication).

---
