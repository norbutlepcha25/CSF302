# 5.3 Quicksort Analysis and Performance

Quicksort is a divide-and-conquer algorithm.

**Divide:** Choose a pivot element and partition the array so that all elements less than the pivot are to its left, and all elements greater are to its right. The pivot is now in its final sorted position.

**Conquer:** Recursively sort the left and right sub-arrays.

**Combine:** No work is needed, as the array is sorted in place.

<figure markdown="span">
    ![RBS](../img/unit5Sorting/quick_sort_partition_animation.gif){width="100%"}
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

## 5.3.1 Quicksort algorithm review

## 5.3.2 Best-case, average-case, and worst-case analysis

## 5.3.3 Techniques for choosing good pivots

## 5.3.4 Optimizations and variations of Quicksort
