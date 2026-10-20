# Greedy Algorithm Design Principles

!!! abstract "At a glance"

    - **Problem:** optimization problems where a solution is built from a sequence of choices (pick an item, an interval, an edge, a merge).
    - **Key idea:** make the choice that looks best *right now*, commit to it permanently, and solve the smaller problem that remains.
    - **When it is correct:** only when the problem has the **greedy-choice property** and **optimal substructure**, and you can *prove* both.
    - **Cost:** usually $O(n \log n)$ (a sort or a heap) plus a linear scan.
    - **Used in:** Huffman coding, Dijkstra, Prim/Kruskal, interval scheduling, caching (Belady), load balancing heuristics, approximation algorithms.

## Motivation and Problem Context

Dynamic programming ([Unit 6](../unit6/topic1.md)) solves optimization problems by trying *every* way of making the next decision and keeping the best. That is safe but often expensive: tables of size $O(nW)$ or $O(n^2)$, and sometimes the state space is simply too large.

Many problems have extra structure: one particular choice is *always* safe to make. If we can identify that choice and prove it is safe, we never need to examine alternatives. The algorithm collapses from "try everything" to "sort, then scan".

Concrete scenario: a university has one seminar hall and 2,000 booking requests for the semester, each with a start and end time. The registrar wants to approve as many requests as possible. Trying all $2^{2000}$ subsets is hopeless; a DP over intervals is possible but unnecessary. The greedy rule "always approve the request that finishes earliest among those still compatible" is optimal and runs in $O(n \log n)$ ([Topic 7.4](topic4.md)).

The danger is equally concrete: the "obvious" greedy rule is frequently *wrong*. "Approve the shortest request first" sounds sensible and fails. Greedy design is therefore half intuition and half proof.

## Problem Formulation

A problem is a candidate for greedy design when it can be phrased as:

- **Input:** a finite set of candidate elements (items, intervals, edges, symbols), each with attributes (weight, value, time, cost).
- **Feasibility:** a rule saying which collections of elements form a valid (partial) solution.
- **Objective:** a function to maximize or minimize over feasible solutions.
- **Construction:** a solution can be built by repeatedly adding one element (or making one decision) to a partial solution, each time reducing the problem to a smaller instance of the same kind.

A **greedy algorithm** is any algorithm of the form:

```text
GREEDY(candidates):
    S = empty partial solution
    while the problem is not finished:
        x = the candidate that is best according to a fixed local rule
        if S + x is feasible:
            S = S + x            // irrevocable: never undone
        remove x from candidates
    return S
```

The entire design effort goes into choosing the **local rule** and proving it produces an optimal $S$.

## Intuition

Think of a greedy algorithm as a hiker who, at every fork, takes the path that looks steepest uphill, never backtracking. On a single smooth hill this reaches the summit. On a mountain range with several peaks it can get stuck on a minor peak (a *local optimum*).

Greedy is correct exactly when the "landscape" of the problem has no misleading minor peaks: every locally best step can be extended to a globally best solution. The two properties below are a precise way of saying "no misleading peaks".

## Definitions

### Greedy-choice property

A problem has the **greedy-choice property** (with respect to a specific rule) if there is always *some* optimal solution that contains the greedy choice.

Note the word *some*: the greedy choice need not be in *every* optimal solution, only in at least one. This is what lets us commit to it without losing optimality.

### Optimal substructure

A problem has **optimal substructure** if, after making a choice $x$, an optimal solution to the original problem consists of $x$ together with an **optimal** solution to the remaining subproblem.

DP needs this property too. The difference:

| | Dynamic programming | Greedy |
|---|---|---|
| Choices examined per step | All possible choices | Exactly one (the greedy one) |
| Subproblems solved | Many, often overlapping, stored in a table | One, the one left after the greedy choice |
| Proof obligation | Recurrence is correct (optimal substructure) | Optimal substructure **and** greedy-choice property |
| Typical cost | Polynomial in table size (e.g. $O(n^2)$, $O(nW)$) | $O(n \log n)$ |
| Typical direction | Bottom-up or memoized top-down | Top-down: choose, then reduce |

!!! warning "Important"

    Optimal substructure alone does **not** make greedy correct. The 0/1 knapsack problem has optimal substructure (which is why DP solves it), but it does not have the greedy-choice property for any simple ratio rule. You must establish the greedy-choice property separately.

### Characteristics of greedy algorithms

| Characteristic | Meaning |
|---|---|
| Myopic | The choice uses only current information, not consequences further ahead. |
| Irrevocable | A committed choice is never undone (contrast with backtracking). |
| Ordered by a key | Most greedy algorithms sort by a key or use a priority queue keyed on it. |
| Problem-specific | There is no universal greedy rule; the key (finish time, ratio, weight, frequency) is the design. |

## Key Results: How to Prove a Greedy Algorithm Correct

There are three standard proof techniques. Choosing the right one is part of the design skill.

### Technique 1: Exchange argument

**Idea.** Take any optimal solution $O$ that differs from the greedy solution $G$. Show that you can *exchange* a piece of $O$ for the corresponding greedy piece without making $O$ worse. Repeating the exchange transforms $O$ into $G$ step by step, so $G$ is at least as good as $O$.

**Template.**

1. Let $O$ be an optimal solution. Let $g$ be the first greedy choice.
2. If $g \in O$, done for this step. Otherwise, find an element $o \in O$ that "plays the same role" as $g$.
3. Show $O' = O - \{o\} + \{g\}$ is **feasible**.
4. Show $\text{cost}(O')$ is no worse than $\text{cost}(O)$, so $O'$ is also optimal and contains $g$.
5. Apply optimal substructure and induction to the remaining subproblem.

**Used for:** activity selection, fractional knapsack, Huffman coding, minimizing lateness, MST (cut property).

### Technique 2: Greedy stays ahead

**Idea.** Measure progress after each step. Show by induction that after $k$ steps, the greedy solution is at least as far ahead as any other solution after $k$ steps. Then show this lead means the greedy solution cannot end up worse.

**Template.**

1. Define a measure $m_k$ for the first $k$ choices (e.g., finish time of the $k$-th chosen interval, distance of the $k$-th settled vertex).
2. Prove by induction: $m_k(G) \le m_k(O)$ (or $\ge$, whichever is "ahead") for all $k$.
3. Conclude: if $O$ had more elements than $G$, then greedy would have been able to take one more, a contradiction.

**Used for:** activity selection (alternative proof), Dijkstra's algorithm (each settled distance is final).

### Technique 3: Structural bound

**Idea.** Prove a lower bound that *every* solution must satisfy, then show greedy meets it exactly.

**Used for:** interval partitioning (number of rooms $\ge$ maximum overlap depth, and greedy uses exactly that many), and many scheduling problems.

### Matroids: when greedy is guaranteed (enrichment)

A **matroid** is a pair $(E, \mathcal{I})$ of a finite ground set $E$ and a family $\mathcal{I}$ of "independent" subsets such that:

1. $\emptyset \in \mathcal{I}$ and subsets of independent sets are independent (hereditary).
2. If $A, B \in \mathcal{I}$ and $|A| < |B|$, there is $x \in B \setminus A$ with $A \cup \{x\} \in \mathcal{I}$ (exchange property).

**Theorem (Rado–Edmonds).** For a matroid with non-negative weights, the greedy algorithm "sort by weight descending, add an element if the set stays independent" returns a maximum-weight independent set. Conversely, if greedy is optimal for every weight function on a hereditary family, that family is a matroid.

Example: in a graph, sets of edges that contain no cycle form the **graphic matroid**. Kruskal's algorithm is exactly the matroid greedy algorithm (run on transformed weights $C - w(e)$ for a large constant $C$, so that the lightest edges come first and every spanning tree has $|V|-1$ edges), which is why it is correct ([Topic 7.6](topic6.md)).

!!! note

    Matroid theory is not required for exams, but it explains *why* some greedy algorithms work and others do not. The 0/1 knapsack feasibility family is not a matroid (it fails the exchange property), and greedy fails there.

## Method: Designing a Greedy Algorithm

```text
Understand the problem → Identify constraints → Write a brute-force/DP baseline →
Propose candidate greedy keys → Hunt for counterexamples (small cases, by hand and by code) →
Pick the surviving key → Prove greedy-choice property (exchange / stays ahead) →
Prove optimal substructure → Analyze complexity → Implement → Cross-check against baseline
```

The step students skip is **counterexample hunting**. For any proposed key, try 2–4 element instances designed to break it. If you cannot break it, attempt a proof; if the proof stalls, the stall usually points to a counterexample.

## Worked Examples

### Example 1 (easy): Activity selection, choosing the key

Goal: maximum number of non-overlapping intervals. Candidate keys:

| Candidate rule | Counterexample | Greedy result | Optimal |
|---|---|---|---|
| Earliest start time | $[0,10), [1,2), [3,4)$ | 1 (takes $[0,10)$) | 2 |
| Shortest duration | $[0,5), [4,7), [6,11)$ | 1 (takes $[4,7)$, which overlaps both) | 2 |
| Fewest conflicts | Known counterexamples exist (11-interval construction in Kleinberg–Tardos) | suboptimal | larger |
| **Earliest finish time** | None: provably optimal | optimal | optimal |

Exchange proof sketch: let $a_1$ finish earliest. Take any optimal $O$ with first interval $o_1$. Since $f(a_1) \le f(o_1)$, replacing $o_1$ by $a_1$ cannot create an overlap with the rest of $O$. So some optimal solution starts with $a_1$. Full proof in [Topic 7.4](topic4.md).

### Example 2 (medium): Coin change, where greedy depends on the input

Goal: pay amount $A$ with the fewest coins from denominations $D$ (unlimited supply). Greedy rule: repeatedly take the largest coin $\le$ remaining amount.

| Denominations | Amount | Greedy | Optimal | Greedy correct? |
|---|---|---|---|---|
| $\{1, 5, 10, 25\}$ | 30 | $25 + 5$ (2 coins) | 2 coins | yes (this system is *canonical*) |
| $\{1, 3, 4\}$ | 6 | $4 + 1 + 1$ (3 coins) | $3 + 3$ (2 coins) | **no** |
| $\{1, 10, 25\}$ | 30 | $25 + 1 \times 5$ (6 coins) | $10 \times 3$ (3 coins) | **no** |
| $\{1, 7, 10\}$ | 14 | $10 + 1 \times 4$ (5 coins) | $7 + 7$ (2 coins) | **no** |
| $\{4, 10\}$ | 12 | $10$ then stuck at 2 | $4 \times 3$ | **no** (greedy finds no solution) |

A coin system on which greedy is always optimal is called **canonical**. Most real currency systems are designed to be canonical, but this is a property of the *specific denominations*, not of coin change in general. The general problem is solved by DP in $O(|D| \cdot A)$.

!!! warning "Important"

    "Greedy works for coin change" is a classic exam trap. Greedy works for *some* denomination sets. Always state the condition, and give a counterexample such as $\{1, 3, 4\}$ with amount 6.

### Example 3 (medium): 0/1 knapsack versus fractional knapsack

Capacity $W = 50$; items $(v, w)$: $(60, 10)$, $(100, 20)$, $(120, 30)$. Ratios: 6, 5, 4.

| Version | Greedy by ratio | Optimal | Greedy correct? |
|---|---|---|---|
| Fractional (items divisible) | $60 + 100 + \tfrac{20}{30} \cdot 120 = 240$ | 240 | yes |
| 0/1 (take whole or nothing) | $60 + 100 = 160$ (item 3 no longer fits) | $100 + 120 = 220$ | **no** |

Why the exchange argument breaks for 0/1: in the fractional case we can swap *an equal weight* of a low-ratio item for a high-ratio item. In the 0/1 case the swap must move whole items, which can leave capacity unused (here 20 units are wasted). Divisibility is exactly what makes the exchange go through. See [Topic 7.2](topic2.md).

### Example 4 (harder): Minimizing maximum lateness

Jobs with processing time $t_j$ and deadline $d_j$ on one machine; minimize the maximum lateness $\max_j (C_j - d_j)^+$ where $C_j$ is the completion time.

- Rule "shortest job first": fails for $(t, d) = (1, 100), (10, 10)$: SJF finishes job 2 at time 11, lateness 1; doing job 2 first gives lateness 0.
- Rule "smallest slack $d_j - t_j$ first": fails for $(1, 2), (10, 10)$: slack-first runs job 2 then job 1, finishing job 1 at 11 (lateness 9); the reverse order gives lateness 1.
- Rule **earliest deadline first (EDF)** is optimal. Proof by exchange: any schedule with an *inversion* (job $i$ before $j$ but $d_i > d_j$) has an adjacent inversion; swapping that adjacent pair does not increase maximum lateness. Repeat until no inversions remain, which is the EDF schedule.

This example shows the exchange argument in its "remove inversions" form, which reappears in many scheduling proofs.

## Algorithmic Applications

| Problem | Greedy key | Proof technique | Topic |
|---|---|---|---|
| Fractional knapsack | Highest $v_i / w_i$ first | Exchange | [7.2](topic2.md) |
| Optimal prefix code | Merge two least frequent | Exchange + induction | [7.3](topic3.md) |
| Activity selection | Earliest finish time | Exchange or stays ahead | [7.4](topic4.md) |
| Single-source shortest paths ($w \ge 0$) | Closest unsettled vertex | Stays ahead (invariant) | [7.5](topic5.md) |
| Minimum spanning tree | Lightest edge crossing a cut | Cut property (exchange) | [7.6](topic6.md) |
| Interval partitioning | Earliest start, reuse earliest-free room | Structural bound | [7.4](topic4.md) |
| Cache eviction (offline) | Evict item used farthest in future (Belady) | Exchange | enrichment |

## Python: Hunting for Counterexamples

The most practical skill in greedy design is checking a greedy rule against an exact baseline on many small inputs. Here the greedy coin algorithm is compared with an exact DP.

```python
def greedy_coins(coins, amount):
    """Largest-coin-first. Returns number of coins, or None if it gets stuck."""
    count = 0
    for c in sorted(coins, reverse=True):
        take = amount // c
        count += take
        amount -= take * c
    return count if amount == 0 else None


def min_coins_dp(coins, amount):
    """Exact optimum by DP (unbounded coin change)."""
    INF = float("inf")
    best = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and best[a - c] + 1 < best[a]:
                best[a] = best[a - c] + 1
    return None if best[amount] == INF else best[amount]


def find_greedy_counterexample(coins, limit):
    """Smallest amount <= limit where greedy is not optimal, else None."""
    for amount in range(1, limit + 1):
        if greedy_coins(coins, amount) != min_coins_dp(coins, amount):
            return amount
    return None
```

- `find_greedy_counterexample([1, 5, 10, 25], 500)` returns `None`; `[1, 3, 4]` returns `6`; `[1, 10, 25]` returns `30`.
- `greedy_coins` returns `None` when it cannot finish (e.g. `[4, 10]`, amount 12), which is itself a failure mode: greedy can miss feasible solutions entirely, not just optimal ones.
- The same pattern (greedy vs exact baseline on all small inputs) is how you should test every greedy algorithm in this unit.

## Edge Cases and Pitfalls

| Case / pitfall | What goes wrong | Fix |
|---|---|---|
| Choosing the "obvious" key without testing | Shortest-first, earliest-start, etc. are plausible but wrong | Try 2–4 element counterexamples for each candidate key before proving |
| Proving only optimal substructure | Proof is incomplete; algorithm may be wrong (0/1 knapsack) | Also prove the greedy-choice property |
| Exchange that breaks feasibility | The swapped solution $O'$ violates a constraint | Explicitly verify feasibility of $O'$ in the proof |
| Ties in the greedy key | Proof assumes strict order; implementation picks arbitrarily | Show the proof works for any tie-breaking, or fix a tie rule |
| Greedy finds no solution | Coin change $\{4, 10\}$, amount 12: greedy gets stuck | Greedy can fail on feasibility, not only optimality; use DP/backtracking |
| Floating-point keys | Ratios like $v/w$ compared with rounding error | Compare $v_i w_j$ vs $v_j w_i$ with integers when exactness matters |

## Common Misconceptions

- **"Greedy is just a fast heuristic."** Some greedy algorithms are *provably optimal* (Huffman, Kruskal, EDF). Others are heuristics or approximations. The difference is whether a proof exists; always say which one you have.
- **"If greedy works on my examples, it is correct."** Examples cannot prove correctness. A single counterexample disproves it; only a proof establishes it.
- **"Greedy and DP solve different problems."** They can solve the same problem. Greedy is a DP where you can prove that only one choice per step needs to be examined.
- **"The greedy choice must be in every optimal solution."** It only needs to be in *some* optimal solution.
- **"Locally optimal at every step implies globally optimal."** Only under the greedy-choice property; 0/1 knapsack and coin change $\{1, 3, 4\}$ are direct counterexamples.

## Alternatives and Trade-offs

| Paradigm | Examines | Guarantee | Typical cost | Use when |
|---|---|---|---|---|
| Greedy | One choice per step | Optimal only with proof | $O(n \log n)$ | A safe choice exists and you can prove it |
| Dynamic programming | All choices, reuses subproblems | Optimal (if recurrence correct) | Table size $\times$ transition | Overlapping subproblems; no safe greedy choice |
| Divide and conquer | Independent subproblems | Exact | Recurrence-driven | Subproblems do not overlap ([Unit 4](../unit4/topic1.md)) |
| Backtracking / branch and bound | All feasible choices with pruning | Optimal | Exponential worst case | NP-hard problems with small inputs |
| Greedy approximation | One choice per step | Within a proven factor | Polynomial | NP-hard problems at scale (e.g. set cover $\ln n$-approx) |

**When to use greedy:** the problem has a natural ordering key; a short exchange or stays-ahead proof exists; input sizes demand $O(n \log n)$.

**When NOT to use greedy:** you cannot find a proof and a small counterexample exists; choices interact through a shared capacity with indivisible items (0/1 knapsack); the value of a choice depends on which other choices are made (weighted interval scheduling, longest simple path).

## In Practice

- **Compression:** Huffman coding is the entropy-coding stage of DEFLATE (used by gzip, zlib and PNG) and baseline JPEG ([Topic 7.3](topic3.md)).
- **Networking:** link-state routing protocols such as OSPF compute shortest-path trees with Dijkstra's algorithm ([Topic 7.5](topic5.md)).
- **Clustering and network design:** MST algorithms underlie single-linkage clustering and cheapest-cable layouts ([Topic 7.6](topic6.md)).
- **Operating systems and real-time systems:** earliest-deadline-first scheduling is a standard real-time scheduling policy, with the exchange argument above as its theoretical basis.
- **Approximation algorithms:** for NP-hard problems (set cover, vertex cover, makespan scheduling), greedy algorithms are often the best-known polynomial-time approximations with proven ratios.
- **Engineering reality:** greedy algorithms are popular in production because they are simple, cache-friendly (sort then scan), and easy to make incremental or streaming.

## Interview and Competitive Programming

**Recognition cues**

- "Maximum number of non-overlapping ...", "minimum number of ... to cover/remove" → sort intervals by end time.
- "Minimum cost to merge/combine" with cost = sum → min-heap of the two smallest (Huffman pattern).
- "Can we reach / is it possible" with a running resource (gas station, jump game) → greedy with a running maximum or running deficit.
- "Assign to minimize the maximum" or "schedule with deadlines" → sort by deadline (EDF) or by a derived key.
- $n \le 10^5$ to $10^6$ and an optimization objective → expect $O(n \log n)$: sort + scan, or heap. A DP would usually need $O(n^2)$, which is too slow.

**Reusable template**

```text
1. Sort by the key (or push into a heap keyed on it).
2. Scan; keep a small state (last end time, current load, heap of active items).
3. For each element: if compatible with state, take it and update state; else skip or replace.
```

**Common traps**

- Sorting by start time when the problem needs end time (or vice versa).
- Greedy where the constraint has indivisible capacity (0/1 knapsack, subset sum): that is DP.
- Exchange-based "sort by custom comparator" problems (e.g. "largest number from concatenation"): the comparator must be a valid total order; prove transitivity or test it.

## Using AI Assistants Critically

- LLMs readily produce a plausible greedy solution for problems that actually need DP (0/1 knapsack, general coin change, weighted interval scheduling). Ask: "give a counterexample to this greedy rule", then verify with a brute force.
- Generated "proofs" often show only optimal substructure and skip the greedy-choice property, or perform an exchange without checking feasibility. Check each step of the template.
- Assistants frequently claim a coin system is canonical without checking. Run `find_greedy_counterexample` up to a reasonable bound (for a canonical-system check, the smallest counterexample, if any, is less than the sum of the two largest coins).
- Ask the assistant for the *key* and the *proof technique* separately; mismatches (stays-ahead claimed, but no progress measure defined) reveal hand-waving.
- Always cross-check greedy output against an exact solver on thousands of random small inputs; property-based testing (e.g. with the `hypothesis` library) automates this.
- Treat "this is the standard greedy approach" as a claim to verify, not as evidence.

## Practice

### Beginner

1. **Shortest-job-first counterexample.** Input: $n$ intervals. Show by an explicit 3-interval instance that "pick the shortest interval first" does not maximize the number of non-overlapping intervals. Difficulty: Easy.
2. **Canonical coins.** Input: denominations $\{1, 2, 5, 10\}$. Output: argue (by checking amounts up to 20) whether greedy is optimal. Difficulty: Easy.
3. **Classify the proof.** For each of activity selection, Dijkstra, interval partitioning, state which proof technique (exchange, stays ahead, structural bound) fits best. Difficulty: Easy.

### Intermediate

1. **Minimize lateness.** Input: $n \le 10^5$ jobs $(t_j, d_j)$. Output: an order minimizing maximum lateness. Constraints: $1 \le t_j, d_j \le 10^9$. Prove your rule by exchange of adjacent inversions. Difficulty: Medium.
2. **Minimize average completion time.** Input: $n$ jobs with processing times $t_j$ on one machine. Output: order minimizing $\sum_j C_j$. Prove optimality. Difficulty: Medium.
3. **Coin system checker.** Input: up to 10 denominations including 1, each $\le 1000$. Output: the smallest amount where greedy fails, or "canonical". Difficulty: Medium.

### Advanced

1. **Matroid check.** Show that the family of edge sets with no cycle is a matroid, and that the family of item sets with total weight $\le W$ (0/1 knapsack) is not. Difficulty: Hard.
2. **Greedy approximation for set cover.** Input: universe $U$, $|U| = n$, and subsets $S_1, \dots, S_m$. Repeatedly pick the set covering the most uncovered elements. Construct an instance where greedy uses strictly more sets than optimal. Difficulty: Hard.
3. **Weighted completion time.** Input: jobs with weights, minimizing weighted sum of completion times. Show "shortest job first" fails and derive the correct ratio rule ($t_j / w_j$ ascending) with an exchange proof. Difficulty: Hard.

### Interview / CP

1. **Jump reachability.** Input: array $a$ of $n \le 10^5$ non-negative integers; from index $i$ you may jump up to $a_i$ steps. Output: whether index $n-1$ is reachable. Expected $O(n)$. Difficulty: Medium.
2. **Gas station circuit.** Input: arrays `gas` and `cost` of length $n \le 10^5$. Output: the starting index to complete the circuit, or $-1$. Expected $O(n)$. Difficulty: Medium.
3. **Minimum arrows.** Input: $n \le 10^5$ closed intervals on a line. Output: the minimum number of points such that every interval contains at least one point. Difficulty: Medium.

## Self-Check Questions

??? question "Q1. State the two properties required for a greedy algorithm to be optimal. Which one is shared with DP?"

    The greedy-choice property (some optimal solution contains the greedy choice) and optimal substructure (optimal solution = choice + optimal solution of the remaining subproblem). Optimal substructure is shared with DP; the greedy-choice property is what lets greedy examine only one choice.

??? question "Q2. Why does greedy by value/weight ratio solve fractional knapsack but not 0/1 knapsack?"

    The exchange argument swaps an equal *weight* of a lower-ratio item for a higher-ratio item, which needs divisibility. In 0/1 knapsack, items move only as wholes, so a swap may leave capacity unused or exceed it. Counterexample: $W = 50$, items $(60,10), (100,20), (120,30)$; greedy gets 160, optimum is 220.

??? question "Q3. Give a coin system and amount where largest-coin-first is not optimal."

    $\{1, 3, 4\}$ with amount 6: greedy uses $4 + 1 + 1$ (3 coins), optimum $3 + 3$ (2 coins).

??? question "Q4. When would you prefer a greedy-stays-ahead proof over an exchange argument?"

    When there is a natural measure of progress after $k$ steps (finish time of the $k$-th chosen interval, distance of the $k$-th settled vertex) that can be compared directly between greedy and any other solution. Exchange arguments are more natural when the solution is a set or an order and you can swap one element or one adjacent pair.

??? question "Q5. A classmate proves optimal substructure for their greedy algorithm and declares it correct. What is missing?"

    The greedy-choice property: a proof that committing to the greedy choice does not exclude every optimal solution. Without it, the algorithm may pick a choice that no optimal solution contains (as in 0/1 knapsack by ratio).

??? question "Q6. In an exchange argument, what two things must you verify about the modified solution $O'$?"

    That $O'$ is feasible (satisfies all constraints) and that its objective value is no worse than that of $O$. Forgetting feasibility is the most common error.

??? question "Q7. You have $n = 2 \times 10^5$ intervals and must choose the maximum number of disjoint ones. Which complexity is acceptable and which algorithm achieves it?"

    About $4 \times 10^{10}$ operations for $O(n^2)$ is too slow; $O(n \log n)$ (about $3.5 \times 10^6$) is fine. Sort by finish time and scan, keeping the last chosen finish time.

??? question "Q8. Why is Kruskal's algorithm an instance of matroid greedy?"

    Acyclic edge sets form the graphic matroid. Kruskal considers edges in increasing weight and keeps an edge exactly when the set stays acyclic (independent). The Rado–Edmonds theorem guarantees this greedy procedure is optimal on any matroid.

## Complexity Summary

| Algorithm / rule | Time | Space | Optimal? |
|---|---|---|---|
| Generic sort-then-scan greedy | $O(n \log n)$ | $O(n)$ | Only with proof |
| Heap-based greedy ($n$ inserts/extracts) | $O(n \log n)$ | $O(n)$ | Only with proof |
| Greedy coin change | $O(\lvert D \rvert \log \lvert D \rvert)$ | $O(1)$ extra | Only for canonical systems |
| DP coin change (baseline) | $O(\lvert D \rvert \cdot A)$ | $O(A)$ | Always |
| Matroid greedy (with independence oracle cost $T$) | $O(n \log n + nT)$ | $O(n)$ | Always, on matroids |

## Key Takeaways

- A greedy algorithm commits to a locally best choice and never revisits it.
- Correctness needs both the **greedy-choice property** and **optimal substructure**; optimal substructure alone is not enough.
- Prove greedy algorithms with an **exchange argument**, **greedy stays ahead**, or a **structural bound**; pick the one that matches the problem's structure.
- Hunt for counterexamples before proving; most plausible greedy keys are wrong.
- Coin change and 0/1 knapsack are the canonical examples where greedy fails; fractional knapsack is where it succeeds.
- Matroids characterize exactly when the simple "sort and add if independent" greedy is optimal.
- In code, always cross-check a greedy algorithm against an exact baseline on small random inputs.
