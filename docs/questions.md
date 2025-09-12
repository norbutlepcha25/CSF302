## Unit 3: Practice Questions

### 1. Iterative method (set 1)

Here are some common recurrence relations, solve this using iterative method:

1.  $ \quad
    T(n) = T(n+1) + 1, \quad T(1) = 1 \quad
    $

2.  $ \quad
    T(n) = T\left(\frac{n}{2} + 1\right) + 1, \quad T(1) = 1
    $

3.  $ \quad
    T(n) = T(n-1) + n, \quad T(1) = 1
    $

4.  $ \quad
    T(n) = 2T\left(\frac{n}{2}\right) + n, \quad T(1) = 1
    $

5.  $ \quad
    T(n) = T(n-1) + 2, \quad T(1) = 1
    $

6.  $ \quad
    T(n) = T\left(\frac{n}{2}\right) + n, \quad T(1) = 1
    $

7.  $ \quad
    T(n) = 2T\left(\frac{n}{2}\right) + n^2, \quad T(1) = 1
    $

### 2. Master Theorem

For each of the following recurrences, give an expression for the runtime **T(n)** if the recurrence can be solved with the Master Theorem. Otherwise, indicate that the Master Theorem does not apply.

1.  $T(n) = 3T\left(\tfrac{n}{2}\right) + n^2$

2.  $T(n) = 4T\left(\tfrac{n}{2}\right) + n^2$

3.  $T(n) = T\left(\tfrac{n}{2}\right) + 2n$

4.  $T(n) = 2n \, T\left(\tfrac{n}{2}\right) + n \cdot n$

5.  $T(n) = 16T\left(\tfrac{n}{4}\right) + n$

6.  $T(n) = 2T\left(\tfrac{n}{2}\right) + n \log n$

7.  $T(n) = 2T\left(\tfrac{n}{2}\right) + \tfrac{n}{\log n}$

8.  $T(n) = 2T\left(\tfrac{n}{4}\right) + n^{0.51}$

9.  $T(n) = 0.5T\left(\tfrac{n}{2}\right) + \tfrac{1}{n}$

10. $T(n) = 16T\left(\tfrac{n}{4}\right) + n!$

11. $T(n) = \sqrt{2} \, T\left(\tfrac{n}{2}\right) + \log n$

12. $T(n) = 3T\left(\tfrac{n}{2}\right) + n$

13. $T(n) = 3T\left(\tfrac{n}{3}\right) + \sqrt{n}$

14. $T(n) = 4T\left(\tfrac{n}{2}\right) + cn$

15. $T(n) = 3T\left(\tfrac{n}{4}\right) + n \log n$

16. $T(n) = 3T\left(\tfrac{n}{3}\right) + \tfrac{n}{2}$

17. $T(n) = 6T\left(\tfrac{n}{3}\right) + n^2 \log n$

18. $T(n) = 4T\left(\tfrac{n}{2}\right) + \tfrac{n}{\log n}$

19. $T(n) = 64T\left(\tfrac{n}{8}\right) - n^2 \log n$

20. $T(n) = 7T\left(\tfrac{n}{3}\right) + n^2$

21. $T(n) = 4T\left(\tfrac{n}{2}\right) + \log n$

22. $T(n) = T\left(\tfrac{n}{2}\right) + n \bigl(2 - \cos n\bigr)$
