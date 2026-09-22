## Q1: Matrix Multiplication — Strassen's vs Traditional

**Objective:**  
Multiply two square matrices (`n × n`) using **two algorithms** and compare their performance.  

**Algorithms:**  
1. Traditional Method (triple nested loop, O(n³))  
2. Strassen's Algorithm (divide and conquer, 7 multiplications per split)  

**Instructions:**  
- Make matrix size a power of 2, e.g. 2x2, 4x4, 8x8, 16x16, ... 128x128.  
- Input matrices manually or generate randomly.  
- Display the resultant matrix from both methods and verify they match.  
 

---

## Q2: Karatsuba's Algorithm for Large Integer Multiplication

**Objective:**  
Multiply two large integers using **two algorithms** and compare their performance.  

**Algorithms:**  
1. Traditional Method (grade-school multiplication, O(n²))  
2. Karatsuba's Algorithm (divide and conquer, 3 multiplications per split)  

**Instructions:**  
- Represent integers as strings/digit arrays so sizes can go well beyond native integer limits (e.g. 8, 16, 32, ..., 1024 digits).  
- Pad operands to the same length and to the next power of 2 as required by your recursive split.  
- Input numbers manually or generate them randomly.  
- Verify Karatsuba's result matches the traditional method for every test case.  

---

## Q3: Binary Search vs Ternary Search (Menu-Driven Program)

**Objective:**  
Write a menu driven program to search for a key in a sorted array of `n` integers using **Binary Search** and **Ternary Search**, and analyze step/frequency counts.  

**Menu:**  
1. Generate `n` sorted random numbers → Array  
2. Display Array  
3. Search for a key using Binary Search  
4. Search for a key using Ternary Search  
5. Step/frequency count for best case (key present, minimum comparisons)  
6. Step/frequency count for worst case (key absent / last comparison)  
7. Step/frequency count comparison table across increasing `n`  

**Instructions:**  
- Record step/frequency counts (number of comparisons) for each search.  
- Compare number of comparisons made by Binary Search vs Ternary Search for the same `n`, and explain the result in terms of recurrence relations $T(n) = T(n/2) + O(1)$ vs $T(n) = T(n/3) + O(1)$.  

---

**Deliverables:**  
1. Source code files for all programs (e.g., `matrix_mult.py`, `strassen.py`, `karatsuba.py`, `search.py`)  
2. Step/frequency count tables for all experiments  
3. Graphs showing time complexity comparisons as and when asked in the question  
4. Brief analysis/conclusion (write it as a comment)
