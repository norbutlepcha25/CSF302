# Glossary

<!-- Unit 2 -->

unit2: Algorithms
: Algorithms are a set of finite rules or instructions to be followed in calculations or other problem-solving operations

<!-- Unit 3 Notes -->

unit3:Recurrence
: An equation (or inequality) that defines a function in terms of its value(s) at smaller input(s).
It expresses a problem’s solution in terms of **smaller subproblems** of the same type.
Simply, when a function calls itself within that function with different parameters, it refers to smaller subproblems.

unit3:Recurrence Relation
: The actual formula that defines a sequence based on its previous terms.
A recurrence relation shows how the current value depends on previous values.
Example: Factorial recurrence
$ T(n) = n \cdot T(n-1), T(0) = 1 $
This means the factorial of `n` is defined in terms of factorial of `n-1`.

unit3:Polynomial Growth
: Polynomial growth in an algorithm refers to a characteristic where the algorithm's running time or space complexity grows proportionally to a polynomial function of the input size. This means that as the input size, typically denoted by 'n', increases, the resources required by the algorithm (time or memory) increase at a rate that can be expressed as \(n^{k}\), where 'k' is a non-negative constant. $\frac{f(n)}{g(n)}$ where $f(n)$ is the actual running time of the algorithm and $g(n)$ is the reference function, thus their ratio would provide a growth rate of $f(n)$ with respect to $g(n)$. In simple terms, if the for input "n" has a a exponential value, we can say that it is a polynomial growth. eg. $n^2$, $n^{0.1}$, or $n^{0.7}$
