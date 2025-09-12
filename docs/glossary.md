# Glossary

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
