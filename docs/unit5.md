# Unit V: Sorting Algorithms and Analysis

## 5.1 Comparison-based Sorting Analysis

These algorithms determine the sorted order by comparing elements. The fundamental operation is the "compare-and-swap."
Examples: Insertion Sort, Selection Sort, Bubble Sort, Merge Sort, Heap Sort, Quick Sort.

### 5.1.1 Common Comparison based sorting Algorithms

**Simple Sorts:**

1. **Insertion Sort:** Builds the final sorted array one item at a time. It is efficient for ==**_small datasets or nearly sorted data_**==.

2. **Selection Sort:** Repeatedly finds the minimum element from the unsorted part and puts it at the beginning i.e, ==**_minimizes number of swaps_**==

3. **Bubble Sort:** Simplest Comparison based sorting algorithm, Repeatedly steps through the list, compares adjacent elements, and swaps them if they are in the wrong order.

| Algorithm      | Best Case | Average Case | Worst Case | Stable | In-place |
| -------------- | --------- | ------------ | ---------- | ------ | -------- |
| Insertion Sort | O(n)      | O(n²)        | O(n²)      | Yes    | Yes      |
| Selection Sort | O(n²)     | O(n²)        | O(n²)      | No     | Yes      |
| Bubble Sort    | O(n)      | O(n²)        | O(n²)      | Yes    | Yes      |

!!! info "Note"

    Insertion Sort (Best Case O(n)): Occurs when the input is already sorted. Each new element is only compared to its immediate predecessor and immediately placed, leading to n-1 comparisons and 0 swaps.

     Selection Sort (Always Θ(n²)): It always performs ~n²/2 comparisons, regardless of input order, because it must scan the entire unsorted segment to find the minimum each time.

**Efficient Sorts:**

1. **Merge Sort:** A divide-and-conquer algorithm that splits the array in half, recursively sorts each half, and then merges the two sorted halves.

2. **Heap Sort:** Builds a binary max-heap from the input and then repeatedly extracts the maximum element, which gives the items in sorted order.

| Algorithm  | Best Case  | Average Case | Worst Case | Stable | In-place |
| ---------- | ---------- | ------------ | ---------- | ------ | -------- |
| Merge Sort | O(n log n) | O(n log n)   | O(n log n) | Yes    | No       |
| Heap Sort  | O(n log n) | O(n log n)   | O(n log n) | No     | Yes      |

!!! info "Note"

    Merge Sort: The recurrence relation is $T(n) = 2T(n/2) + Θ(n)$. Applying the Master Theorem (Case 2), this solves to Θ(n log n). The linear Θ(n) term comes from the merge operation. The space complexity O(n) is for the temporary array used during merging.

    Heap Sort: Building the heap takes O(n) time. Each of the n extract-max operations takes O(log n) time. Thus, the total is O(n) + O(n log n) = O(n log n).

## 5.2 Lower Bound of Sorting

> A lower bound is the best possible (minimum) time complexity that any algorithm of a certain type can achieve for a given problem.

All comparison-based sorting algorithms (like Merge Sort, Quick Sort, Heap Sort, etc.) decide the order of elements by comparing pairs of elements (using <, >). Every sorting process can be seen as a series of decisions — each comparison narrows down the possible orderings of the input.

### 5.2.1 Decision tree model for comparison-based sorting

<figure markdown="span">
    ![DT](img/unit5Sorting/decisionTree.png){width="60%"}
    <figcaption>Example of a decision Tree</figcaption>
    <p align='right' style="font-size:0.8em"><i>Image Source: <a href="https://www.comp.nus.edu.sg/~stevenha/cs3230/lectures/lec04a.pdf" target="_blank"> NUS Notes</a ></i></p>
</figure>

A decision tree is a rooted tree

- Start from the root.
- At every node, a question is asked.
- Depending on the answer, a child is chosen.
- At a leaf, a decision is taken.

Similarly any comparison-based algorithm can be modeled using a decision tree:

- Internal Nodes: Represent a comparison between two elements (e.g., aᵢ ≤ aⱼ?).
- Branches: Represent the outcome of the comparison (Yes/No).
- Leaves: Represent one of the possible n! permutations of the input. A correct sorting algorithm must have a unique leaf for each permutation.

<figure markdown="span">
    ![DT](img/unit5Sorting/exampleDTSA.png){width="80%"}
    <figcaption>Example of a decision Tree</figcaption>
    <p align='right' style="font-size:0.8em"><i>Image Source: <a href="https://www.comp.nus.edu.sg/~stevenha/cs3230/lectures/lec04a.pdf" target="_blank"> NUS Notes</a ></i></p>
</figure>

!!! note "Proof: The worst-case time complexity of any comparison-based sorting algorithm is Ω (𝑛 log 𝑛) ."

    !!! note inline end "Sterling Approximation"

        Stirling's approximation formula for the factorial of a large integer \(n\) is \(n!\approx \sqrt{2\pi n}(\frac{n}{e})^{n}\). This approximation is used to estimate large factorials that would be difficult or impossible to calculate directly, providing a close approximation to the actual value.
    1. The decision tree must have at least n! leaves to account for all possible input permutations.

    2. A binary tree of height h has at most 2ʰ leaves. Therefore, 2ʰ ≥ n!. (Remember: height of the decision tree (number of comparisons in the worst case) )
    3.  Taking logarithms: h ≥ log₂(n!).

           ***The factorial function $𝑛!$ grows extremely fast. It’s hard to directly compute or simplify $log_2 (𝑛!)$ in terms of 𝑛***

    4. Using Stirling's Approximation $$ n! ≈ \sqrt {2πn}(\frac{n}{e})ⁿ $$,

           we get:
    $$
        \begin{align*}
        \log_2(n!) &\approx \log_2(\sqrt{2\pi n}) + n\log_2\!\left(\frac{n}{e}\right) \\
         &\approx n\log_2 n - n\log_2 e + \tfrac{1}{2}\log_2(2\pi n) \\
         &\approx n\log_2 n - n\log_2 e + O(\log n)
         \end{align*}
    $$

    The other terms are much smaller in magnitude compared to $𝑛 log_2 𝑛 $

    This simplifies to $h = Ω(n log n)$.

    Conclusion: The height of the decision tree (which represents the number of comparisons in the worst case) is Ω(n log n).

### 5.2.2 Implications and limitation of lower bound

Merge Sort and Heap Sort are asymptotically optimal comparison-based sorts because their worst-case running time O(n log n) matches the lower bound Ω(n log n). It is impossible to create a general-purpose comparison sort that is faster than this in the worst case.

**Limitations**

This proof only applies to comparison-based sorts. It does not apply to algorithms that leverage other information about the data, such as:

- The integer structure of keys (e.g., Counting Sort, Radix Sort).
- The distribution of the keys.
  These "non-comparison" sorts can achieve O(n) time, breaking the n log n barrier.

## 5.3 Quick Sort Analysis and and Peformance

Quicksort is a divide-and-conquer algorithm.

**Divide:** Choose a pivot element and partition the array so that all elements less than the pivot are to its left, and all elements greater are to its right. The pivot is now in its final sorted position.

**Conquer:** Recursively sort the left and right sub-arrays.

**Combine:** No work is needed, as the array is sorted in place.

<figure markdown="span">
    ![RBS](img/unit5Sorting/quick_sort_partition_animation.gif){width="100%"}
    <figcaption>Quick sort Algorithm</figcaption>
    <p align='right' style="font-size:0.8em"><i>Image Source: <a href="https://akshitadixit.github.io/Structurex/quickSort.html/"> Strucrex</a ></i></p>
</figure>

**Steps**

**Step 1: Choose a Pivot**

Select an element from the array as the pivot. Common strategies:

- First element
- Last element
- Middle element
- Random element
- Median of three

**Step 2: Partitioning**

Rearrange the array so that:

- All elements less than pivot come before it
- All elements greater than pivot come after it
- The pivot is in its final sorted position

**Step 3: Recursively Sort**

Apply the same process to the sub-arrays on left and right of the pivot.

## 5.4 Randomized Pivot Selection in Quicksort
