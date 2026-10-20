# Basics of Game Theory

!!! abstract "At a glance"

    - **Problem space:** two players alternate moves with full information and no chance; who wins with perfect play, and what is a winning move?
    - **Key ideas:** classify positions backwards from the end — a position is **winning** iff some move leads to a **losing** position. Nim is solved by XOR; the Sprague–Grundy theorem reduces every impartial game to Nim; minimax evaluates general (partisan, scored) game trees.
    - **Core complexities:** win/lose DP $O(\text{states} \times \text{moves})$; Nim $O(k)$ for $k$ piles; minimax $O(b^d)$ for branching factor $b$ and depth $d$; alpha–beta $O(b^{d/2})$ with perfect move ordering.
    - **Where it is used:** competitive programming game problems, game AI (chess, Go, checkers engines), adversarial reasoning in security and testing, and as a showcase of backward induction (a form of dynamic programming).

## Motivation and Problem Context

"Alice and Bob play a game, Alice moves first, both play optimally — who wins?" is one of the most common problem types in programming contests and interviews. It looks like it requires simulating every possible game, which is exponential. The insight of this topic is that **you never need to simulate games, only to classify positions**, and that classification has rich mathematical structure (XOR in Nim, the mex function in Sprague–Grundy).

The same backward reasoning powers game-playing software. Chess engines search game trees with minimax and alpha–beta pruning; checkers was "solved" (shown to be a draw with perfect play) by combining search with huge endgame databases computed by backward induction. Outside games, minimax is the model for any adversarial setting: worst-case analysis of algorithms is itself a game against an adversary choosing the input.

## Problem Formulation

A **combinatorial game** in this topic has:

- two players who **alternate** moves;
- **perfect information** (both see the whole position) and **no randomness**;
- a finite set of positions, and every play **terminates** (no infinite games);
- under **normal play**, the player who cannot move **loses**. (Under *misère* play, the player who cannot move wins.)

The game is **impartial** if the available moves depend only on the position, not on whose turn it is (Nim, subtraction games). It is **partisan** if players have different moves (chess: White moves white pieces).

**Input:** a description of positions and legal moves, and a starting position. **Output:** whether the player to move wins with optimal play, and ideally a winning move. For scored games (tic-tac-toe with values $+1/0/-1$, chess evaluations), the output is the **minimax value** of the position.

## Intuition

Think backwards from the end. If you are in a position with no moves, you have lost. A position is good for you if you can push your opponent into a bad position; it is bad for you if **every** move hands your opponent a good position. That rule, applied from terminal positions upward, labels the whole game. Mental model: *a winning strategy is "always move to a losing position for the opponent"; a losing position is one where no such move exists.*

## Definitions

| Term | Definition |
| --- | --- |
| P-position | The **P**revious player (the one who just moved) wins: the player to move loses with optimal play |
| N-position | The **N**ext player (the one to move) wins |
| Terminal position | No legal moves; a P-position under normal play |
| Game graph | Directed acyclic graph: nodes are positions, edges are moves |
| $\operatorname{mex}(S)$ | Minimum excludant: smallest non-negative integer not in $S$; $\operatorname{mex}\{0, 1, 3\} = 2$, $\operatorname{mex}\{\} = 0$ |
| Grundy number $g(v)$ | $g(v) = \operatorname{mex}\{g(u) : v \to u\}$ |
| Sum of games $G_1 + G_2$ | Play several games side by side; each move is made in exactly one component |
| Nim-sum | Bitwise XOR $a_1 \oplus a_2 \oplus \dots \oplus a_k$ of pile sizes |
| Minimax value | Best outcome the maximizing player can guarantee against an optimal minimizing opponent |

## Key Results

### Classification of positions

**Theorem.** In a finite impartial game under normal play, every position is exactly one of P or N, determined by:

1. terminal positions are P;
2. a position is N iff **at least one** move leads to a P-position;
3. a position is P iff **every** move leads to an N-position.

*Proof (strong induction on the length of the longest play from the position).* Terminal positions have length 0 and are P (the mover cannot move and loses). For a non-terminal position $v$, all successors have shorter longest plays, so by induction each is labelled correctly. If some successor $u$ is P, the mover moves to $u$ and then, by induction, wins as the "previous player" there: $v$ is N. If all successors are N, whatever the mover does, the opponent becomes the next player in an N-position and wins: $v$ is P. $\square$

This is **backward induction**, and it is dynamic programming over the game DAG: subproblems are positions, the recurrence is the rule above, and evaluation order is a reverse topological order.

### Nim and Bouton's theorem

**Nim:** $k$ piles of stones; a move removes any positive number of stones from one pile; the player who takes the last stone wins.

**Bouton's theorem.** $(a_1, \dots, a_k)$ is a P-position iff $a_1 \oplus a_2 \oplus \dots \oplus a_k = 0$.

*Proof.* We check the three properties of the classification theorem for the set $Z$ of zero-XOR positions.

- *Terminal:* all piles 0, XOR is 0, so the terminal position is in $Z$.
- *From $Z$, every move leaves $Z$:* changing one pile $a_i$ to $a_i' \ne a_i$ changes the XOR by $a_i \oplus a_i' \ne 0$.
- *From outside $Z$, some move enters $Z$:* let $s \ne 0$ be the nim-sum and $t$ its highest set bit. Some pile $a_i$ has bit $t$ set (otherwise bit $t$ of $s$ would be 0). Then $a_i \oplus s < a_i$ — bit $t$ is cleared and higher bits are unchanged — so reducing pile $i$ to $a_i \oplus s$ is legal, and the new nim-sum is $s \oplus a_i \oplus (a_i \oplus s) = 0$.

Positions in $Z$ therefore satisfy exactly the P-rules, so $Z$ is the set of P-positions. $\square$

### Sprague–Grundy theorem

**Theorem.** Every position $v$ of an impartial game (under normal play) is equivalent to a single Nim pile of size $g(v)$, where $g(v) = \operatorname{mex}\{g(u) : v \to u\}$. In particular:

1. $v$ is a P-position iff $g(v) = 0$;
2. for a sum of games, $g(G_1 + G_2 + \dots + G_k) = g(G_1) \oplus g(G_2) \oplus \dots \oplus g(G_k)$.

*Why mex?* A Nim pile of size $g$ can move to piles of every size $0, 1, \dots, g-1$, but not to $g$ itself. If a position's options have Grundy values that include all of $0, \dots, g-1$ but not $g$, it can do everything that pile can do. It may also have options with values larger than $g$, but those never help the mover: the opponent can answer such a move by moving straight back to a position of value $g$. So the position "behaves like" a pile of size $\operatorname{mex}$ of its options. Part 1 follows because $g(v) = 0$ means no option has value 0, which matches the P-rule. Part 2 follows from Bouton's argument applied to the Grundy values. Nim is the special case where a pile of size $n$ has $g = n$.

!!! warning "Important: XOR Grundy numbers, never win/lose flags"

    For a sum of independent games, combine components with the XOR of their **Grundy numbers**. Combining win/lose bits does not work: two N-positions can sum to a P-position (e.g. two Nim piles of size 1), or to an N-position (piles 1 and 2). The Grundy value carries the extra information that a single bit loses.

### Minimax for scored and partisan games

When outcomes are scores (win $+1$, draw $0$, loss $-1$, or an engine's evaluation), label each node of the game tree with the value the player to move can force:

$$
\text{value}(v) =
\begin{cases}
\text{score}(v) & v \text{ terminal (or depth limit reached)}\\
\max_{u} \text{value}(u) & \text{MAX to move}\\
\min_{u} \text{value}(u) & \text{MIN to move}
\end{cases}
$$

Win/lose classification is the special case with scores $\pm 1$. **Zermelo's theorem** follows from the same induction: every finite two-player game of perfect information without chance has a determined value — for tic-tac-toe it is a draw.

**Alpha–beta pruning** computes the same value while skipping subtrees that cannot affect it. It maintains $\alpha$ (the best value MAX can already guarantee on the current path) and $\beta$ (the best value MIN can guarantee); once $\alpha \ge \beta$, the remaining children of the current node are irrelevant. With best-first move ordering it examines about $b^{\lceil d/2 \rceil} + b^{\lfloor d/2 \rfloor} - 1$ leaves instead of $b^d$ (Knuth and Moore), effectively doubling the searchable depth for the same effort; with the worst ordering it saves nothing.

## Method

### Solving an unfamiliar impartial game

1. **Model** positions and moves; confirm the game is impartial, finite, and normal play.
2. **Brute force** the P/N labels (or Grundy numbers) for small positions with a DP.
3. **Print the table and find the pattern** — periodicity is extremely common (subtraction games are eventually periodic).
4. **Prove the pattern** by checking the three P-position properties (as in Bouton's proof), or at least verify it against the brute force on a large range.
5. If the position splits into **independent parts**, compute each part's Grundy number and XOR them.

```text
GRUNDY-TABLE(n, moves)               // subtraction game: remove m in moves stones
    g[0] <- 0
    for i <- 1 to n
        S <- { g[i - m] : m in moves, m <= i }
        g[i] <- MEX(S)
    return g

MEX(S)
    x <- 0
    while x in S
        x <- x + 1
    return x
```

### Searching a game tree

```text
ALPHABETA(node, maximizing, alpha, beta)
    if node is terminal or depth limit reached
        return EVALUATE(node)
    if maximizing
        best <- -infinity
        for each child c of node
            best <- max(best, ALPHABETA(c, false, alpha, beta))
            alpha <- max(alpha, best)
            if alpha >= beta
                break                     // beta cut-off
        return best
    else
        best <- +infinity
        for each child c of node
            best <- min(best, ALPHABETA(c, true, alpha, beta))
            beta <- min(beta, best)
            if alpha >= beta
                break                     // alpha cut-off
        return best
```

Initial call: `ALPHABETA(root, true, -infinity, +infinity)`. Removing the two `if alpha >= beta` lines gives plain minimax.

## Worked Examples

!!! example "Example 1 (basic): take-away game, 1 to 3 stones"

    One pile of $n$ stones; a move removes 1, 2 or 3; taking the last stone wins.

    | $n$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
    | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
    | label | P | N | N | N | P | N | N | N | P |
    | $g(n)$ | 0 | 1 | 2 | 3 | 0 | 1 | 2 | 3 | 0 |

    $n = 4$ is P because its moves lead to 3, 2, 1 — all N. Pattern: **P iff $n \equiv 0 \pmod 4$**, and $g(n) = n \bmod 4$. *Proof:* from a multiple of 4, any move leaves a non-multiple; from a non-multiple, removing $n \bmod 4$ stones restores a multiple. Strategy: always leave a multiple of 4.

!!! example "Example 2 (intermediate): subtraction set $\{1, 3, 4\}$"

    | $n$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
    | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
    | $g(n)$ | 0 | 1 | 0 | 1 | 2 | 3 | 2 | 0 | 1 | 0 | 1 | 2 | 3 | 2 | 0 |

    For example $g(4) = \operatorname{mex}\{g(3), g(1), g(0)\} = \operatorname{mex}\{1, 1, 0\} = 2$. The sequence has period 7, so P-positions are $n \equiv 0, 2 \pmod 7$. With two piles of sizes 4 and 6, the sum has value $g(4) \oplus g(6) = 2 \oplus 2 = 0$: a P-position, even though each pile alone is an N-position.

!!! example "Example 3 (intermediate): Nim $(3, 4, 5)$"

    | pile | binary |
    | --- | --- |
    | 3 | `011` |
    | 4 | `100` |
    | 5 | `101` |
    | nim-sum | `010` = 2 |

    The nim-sum is 2, so the first player wins. The highest set bit of 2 is bit 1; pile 3 (`011`) has it set, and $3 \oplus 2 = 1 < 3$. Winning move: reduce pile 3 to 1 (remove 2 stones), leaving $(1, 4, 5)$ with $1 \oplus 4 \oplus 5 = 0$.

!!! example "Example 4 (advanced): minimax with alpha–beta pruning"

    MAX moves at the root, MIN at depth 1, MAX at depth 2; leaves are evaluations. Visiting children left to right:

    ```mermaid
    flowchart TD
        R["MAX root = 5"] --> A["MIN = 5"]
        R --> B["MIN = 2 (cut)"]
        A --> A1["MAX = 5"]
        A --> A2["MAX >= 6 (cut)"]
        B --> B1["MAX = 2"]
        B --> B2["pruned"]
        A1 --> L1["3"]
        A1 --> L2["5"]
        A2 --> L3["6"]
        A2 --> L4["9 (pruned)"]
        B1 --> L5["1"]
        B1 --> L6["2"]
        B2 --> L7["0 (pruned)"]
        B2 --> L8["-1 (pruned)"]
    ```

    | Step | Node | $\alpha, \beta$ on entry | Event |
    | --- | --- | --- | --- |
    | 1 | A1 | $-\infty, +\infty$ | leaves 3, 5: value 5 |
    | 2 | A | — | $\beta \leftarrow 5$ |
    | 3 | A2 | $-\infty, 5$ | leaf 6: $\alpha = 6 \ge \beta = 5$, cut leaf 9 (MIN at A will never allow $\ge 6$) |
    | 4 | R | — | A = 5, so $\alpha \leftarrow 5$ |
    | 5 | B1 | $5, +\infty$ | leaves 1, 2: value 2 |
    | 6 | B | — | $\beta \leftarrow 2 \le \alpha = 5$: cut B2 entirely (MAX at the root already has 5) |

    Root value 5, found after visiting 5 of the 8 leaves. Plain minimax gives the same value after visiting all 8.

## Algorithmic Applications

| Problem type | Tool |
| --- | --- |
| One pile, fixed move set | Win/lose DP, then find the period |
| Several independent piles / boards | Grundy number per component, XOR |
| Nim variants (take from one pile) | Nim-sum directly |
| Misère Nim (last stone loses) | Same as Nim unless all piles have size $\le 1$; then the mover wins iff the number of non-empty piles is even |
| Games on a DAG (move a token along edges) | Grundy numbers in reverse topological order |
| Partisan or scored games, small state space | Minimax with memoization |
| Large game trees (chess-like) | Depth-limited alpha–beta with an evaluation function, move ordering, transposition tables |
| Games with chance (dice) | Expectiminimax — chance nodes take expectations ([Topic 1.3](topic3.md)) |

## Python Implementation

```python
from functools import lru_cache, reduce
from operator import xor


def win_table(n, moves):
    """win[i] is True iff the player to move wins with i stones (normal play)."""
    win = [False] * (n + 1)                      # win[0] = False: no move, you lose
    for i in range(1, n + 1):
        win[i] = any(m <= i and not win[i - m] for m in moves)
    return win


def mex(values):
    seen = set(values)
    g = 0
    while g in seen:
        g += 1
    return g


def grundy_table(n, moves):
    g = [0] * (n + 1)
    for i in range(1, n + 1):
        g[i] = mex(g[i - m] for m in moves if m <= i)
    return g


def nim_winning_move(piles):
    """Return (pile_index, new_size) of a winning move, or None if in a P-position."""
    s = reduce(xor, piles, 0)
    if s == 0:
        return None
    for i, a in enumerate(piles):
        if a ^ s < a:                            # pile with the top bit of s set
            return i, a ^ s


def minimax(node, maximizing):
    """node is a number (leaf value) or a list of child nodes."""
    if not isinstance(node, list):
        return node
    values = [minimax(child, not maximizing) for child in node]
    return max(values) if maximizing else min(values)


def alphabeta(node, maximizing, alpha=float("-inf"), beta=float("inf"), visited=None):
    if not isinstance(node, list):
        if visited is not None:
            visited.append(node)
        return node
    if maximizing:
        best = float("-inf")
        for child in node:
            best = max(best, alphabeta(child, False, alpha, beta, visited))
            alpha = max(alpha, best)
            if alpha >= beta:                    # MIN above will never allow this
                break
        return best
    best = float("inf")
    for child in node:
        best = min(best, alphabeta(child, True, alpha, beta, visited))
        beta = min(beta, best)
        if alpha >= beta:                        # MAX above already has better
            break
    return best


LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
         (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]


@lru_cache(maxsize=None)
def tic_tac_toe_value(board, player):
    """+1 if X wins with best play, -1 if O wins, 0 for a draw. board is a 9-char string."""
    for a, b, c in LINES:
        if board[a] != "." and board[a] == board[b] == board[c]:
            return 1 if board[a] == "X" else -1
    if "." not in board:
        return 0
    nxt = "O" if player == "X" else "X"
    values = [tic_tac_toe_value(board[:i] + player + board[i + 1:], nxt)
              for i, cell in enumerate(board) if cell == "."]
    return max(values) if player == "X" else min(values)
```

**Walkthrough of the non-obvious lines**

- `win[i] = any(m <= i and not win[i - m] ...)` is the classification rule verbatim: N iff some move reaches a P-position. `and` short-circuits, so `win[i - m]` is never read with a negative index.
- `a ^ s < a` holds exactly for piles containing the highest set bit of `s` (Bouton's proof), so the loop always finds a move when `s != 0`.
- `alphabeta` passes `alpha`/`beta` **down** by value; updates in a child do not leak to siblings, which is what makes the cut-offs correct.
- `tic_tac_toe_value` is minimax with memoization: identical boards reached by different move orders are evaluated once (5,478 distinct legal positions are cached from the empty board). Its result for the empty board is 0 — a draw.

These functions were verified by brute force: P-positions of Nim with up to three piles of size $\le 5$ against exhaustive search, the XOR rule for sums of two $\{1,3,4\}$-subtraction piles, and `alphabeta == minimax` on 500 random trees.

## Edge Cases and Pitfalls

| Case / pitfall | What goes wrong | Fix |
| --- | --- | --- |
| Misère rules read as normal play | Terminal position labelled P instead of N; strategy inverted near the end | Re-derive the base case; misère Nim needs the "all piles $\le 1$" special case |
| XOR-ing win/lose booleans across components | Wrong result for sums of games | XOR Grundy numbers |
| Grundy recursion without memoization | Exponential recomputation | Bottom-up table or `lru_cache` |
| Game graph with cycles (positions can repeat) | Recursion never terminates; P/N theory as stated does not apply | Detect cycles; use retrograde analysis with "draw" labels |
| Guessing a pattern from too few values | Subtraction games can have long pre-periods | Check the conjectured period over a long range against brute force |
| `mex` over a list with duplicates or large values | Wrong mex if implemented with sorting mistakes | Use a set and count up from 0 |
| Alpha–beta with shared mutable alpha/beta across siblings | Incorrect pruning and wrong values | Pass bounds as parameters; compare with plain minimax on random trees |
| Evaluation from the wrong player's perspective | Engine plays the worst move | Fix one perspective (MAX) or use negamax consistently |

## Common Misconceptions

| Wrong belief | Correct mental model |
| --- | --- |
| "To know who wins, simulate all games." | Classify **positions** with DP; the number of positions is usually far smaller than the number of games. |
| "The first player has the advantage." | It depends on the starting position: from a P-position the first player loses against optimal play. |
| "Grundy number = number of moves available." | It is the mex of the successors' Grundy numbers; it measures equivalence to a Nim pile, not mobility. |
| "Alpha–beta may return an approximate value." | It returns exactly the minimax value; it only skips subtrees that cannot change it. |
| "Alpha–beta always makes search $O(b^{d/2})$." | Only with near-perfect move ordering; worst case is still $O(b^d)$. |
| "Sprague–Grundy applies to chess." | It applies to **impartial** games under normal play; chess is partisan, needs minimax. |

## Alternatives and Trade-offs

| Technique | Applies to | Cost | Use when | Avoid when |
| --- | --- | --- | --- | --- |
| Win/lose DP (backward induction) | Any finite game with small state space | $O(\text{states} \times \text{moves})$ | States $\le 10^6$–$10^7$ | State space astronomical |
| Pattern / closed form | Impartial games with regular structure | $O(1)$ per query after analysis | Huge $n$ (up to $10^{18}$) | No provable pattern |
| Nim-sum | Nim and games reducible to Nim | $O(k)$ | Independent piles, take-any moves | Moves span several piles |
| Sprague–Grundy | Sums of impartial games | $\sum$ component DP + XOR | Position splits into independent parts | Partisan games, misère sums |
| Minimax | Partisan / scored games | $O(b^d)$ | Small trees; exact value needed | Large depth |
| Alpha–beta | Same as minimax | $O(b^{d/2})$ to $O(b^d)$ | Game engines, good move ordering available | Need values of *all* moves (pruning hides them) |
| Monte Carlo tree search | Huge branching (Go), no good evaluation | Anytime, sampling-based | Evaluation function hard to write | Exact answers required |

## In Practice

- **Chess engines** (e.g. Stockfish) use alpha–beta search (in its principal-variation form) with iterative deepening, move ordering heuristics, transposition tables (hash tables of already-evaluated positions) and endgame tablebases built by retrograde analysis — backward induction on all positions with few pieces. Modern versions use a neural-network evaluation function (NNUE).
- **Go programs** (AlphaGo and successors) replaced alpha–beta with Monte Carlo tree search guided by neural networks, because Go's branching factor (around 250) makes exhaustive minimax search infeasible.
- **Checkers** was proven a draw (Schaeffer et al., 2007) by combining search with endgame databases.
- **Adversarial thinking in engineering.** Worst-case complexity is a game in which an adversary picks the input; lower-bound proofs (such as the sorting lower bound in [Unit 5.2](../unit5/topic2.md)) are "adversary arguments". Security testing and fuzzing adopt the same mindset.
- **Economic game theory** (Nash equilibria, auctions, mechanism design) is a different branch dealing with simultaneous moves and hidden information; it is used in ad auctions and networking protocols but is outside this topic.

## Interview and Competitive Programming

**Recognition cues**

| If you see... | Think... |
| --- | --- |
| "Both play optimally; who wins?" with small $n$ | Win/lose DP over positions |
| Same, with $n$ up to $10^{18}$ | Brute force small $n$, find the period, prove it |
| "Remove any number from one pile" | Nim: XOR of pile sizes |
| "Several independent piles/boards, each with its own rule" | Grundy numbers, XOR |
| "Move a token along edges of a DAG" | Grundy numbers in reverse topological order |
| "Maximize your score minus opponent's score" (e.g. take from either end of an array) | Minimax DP over intervals: $f(i,j) = \max(a_i - f(i+1, j),\ a_j - f(i, j-1))$ |
| "Last player to move loses" | Misère: re-derive the base case |

**Constraints to approach**

| State space | Approach |
| --- | --- |
| $\le 10^6$ positions | Direct DP |
| $n \le 10^{18}$, one pile | Period detection / closed form |
| $k \le 10^5$ piles, each $\le 10^9$ | Per-pile closed-form Grundy, XOR |
| Two-player array/interval games, $n \le 5000$ | $O(n^2)$ interval DP (minimax form) |

**Common traps:** answering for the wrong player (the problem may ask whether the *second* player wins); missing that a "pass" move breaks the theory; XOR-ing booleans.

## Using AI Assistants Critically

- LLMs often "recognize" a game as Nim when the move rule differs (for example, removing up to $k$ stones). Always brute-force small cases and compare with the claimed formula.
- Generated Grundy code frequently confuses normal and misère play or sets the terminal Grundy value incorrectly; check the base case explicitly.
- Assistants sometimes XOR win/lose results instead of Grundy numbers for sums of games — test on two piles where the answer is known.
- Generated alpha–beta code can update `alpha` in the MIN branch (or `beta` in the MAX branch), silently producing wrong values. Cross-check `alphabeta(t) == minimax(t)` on hundreds of random trees.
- Claims like "alpha–beta reduces complexity to $O(\sqrt{b^d})$" omit the move-ordering assumption; ask for the best- and worst-case bounds.
- Periodicity claims ("the pattern repeats every 7") should be verified for thousands of values, not the first 20.

## Practice

**Beginner**

1. *Take-away.* Input: $n \le 10^{18}$, and a move removes 1 to $k$ stones ($k \le 10^9$). Output: `First` or `Second` (who wins). Difficulty: easy.
2. *Nim.* Input: $k \le 10^5$ pile sizes $\le 10^9$. Output: winner and one winning move if the first player wins. Difficulty: easy.
3. *Grundy by hand.* Input: subtraction set $\{2, 3\}$. Output: $g(0..15)$ and the P-positions; state the period. Difficulty: easy.

**Intermediate**

1. *Several subtraction piles.* Input: $k \le 10^5$ piles with sizes $\le 10^6$ and a common move set $S$ ($|S| \le 10$). Output: winner. Difficulty: medium.
2. *Token on a DAG.* Input: a DAG with $V \le 10^5$, $E \le 2 \times 10^5$ and $t$ tokens on given vertices; a move slides one token along an edge. Output: winner. Difficulty: medium.
3. *Misère Nim.* Input: $k$ pile sizes. Output: winner when the player who takes the last stone loses. Difficulty: medium.

**Advanced**

1. *Split piles.* Input: piles of size $\le 10^4$; a move either removes one stone from a pile or splits a pile into two non-empty unequal piles. Output: winner (use Grundy numbers of split positions as XORs of parts). Difficulty: hard.
2. *Tic-tac-toe solver.* Input: a partially filled $3 \times 3$ board. Output: the minimax value and an optimal move; report how many positions alpha–beta visits compared with plain minimax. Difficulty: medium–hard.
3. *Pattern proof.* Input: subtraction set $\{1, 4\}$. Output: conjecture the P-positions from brute force and prove the conjecture with the three P-position properties. Difficulty: hard.

**Interview / CP**

1. *Nim Game* (LeetCode 292). Input: $n$ stones, remove 1 to 3 per turn. Output: whether the first player wins. Difficulty: easy.
2. *Stone Game* (LeetCode 877) / *Predict the Winner* (LeetCode 486). Input: an array; players alternately take from either end. Output: whether the first player can score at least as much as the second. Difficulty: medium.
3. *Grundy game on grids.* Input: several $r \times c$ chocolate bars; a move breaks one bar along a grid line into two bars. The player unable to move loses. Output: winner. Difficulty: hard.

## Self-Check Questions

??? question "Q1. State the rules that classify P- and N-positions and explain why they amount to dynamic programming."

    Terminal positions are P; a position is N iff some move leads to a P-position; otherwise it is P. Each position's label depends only on its successors' labels (optimal substructure), many play sequences share positions (overlapping subproblems), and evaluating in reverse topological order is a bottom-up DP.

??? question "Q2. Who wins Nim $(1, 2, 3)$? Justify."

    $1 \oplus 2 \oplus 3 = 0$, so it is a P-position: the player to move loses with optimal play by the opponent.

??? question "Q3. Find a winning move in Nim $(5, 7, 9)$."

    Nim-sum: $5 \oplus 7 = 2$, $2 \oplus 9 = 11$ (`1011`). Highest bit is 8; only 9 (`1001`) has it. $9 \oplus 11 = 2$, so reduce the pile of 9 to 2, leaving $(5, 7, 2)$ with $5 \oplus 7 \oplus 2 = 0$.

??? question "Q4. Compute $\operatorname{mex}\{0, 2, 3\}$, $\operatorname{mex}\{1, 2\}$, $\operatorname{mex}\{\}$, and explain the role of mex."

    1, 0, 0. The Grundy number of a position is the mex of its options' Grundy numbers, making the position equivalent to a Nim pile of that size: it can move to every smaller value but not to its own.

??? question "Q5. Two separate games are both N-positions. Is their sum necessarily an N-position?"

    No. Nim piles $(1)$ and $(1)$ are each N, but their sum $(1, 1)$ has nim-sum $0$ and is P. Piles $(1)$ and $(2)$ are each N and their sum has nim-sum $3$, which is N. Only Grundy numbers determine the sum.

??? question "Q6. Why does alpha–beta return exactly the minimax value even though it skips subtrees?"

    A subtree is skipped only when $\alpha \ge \beta$: the player above already has an alternative at least as good as anything this subtree could yield for them. Whatever value the skipped subtree has, the optimizing player at the ancestor would not choose this branch, so the root's value is unchanged.

??? question "Q7. A game's state space is all $n \le 10^{18}$. How would you approach it?"

    Compute P/N labels or Grundy values for small $n$ by DP, look for a periodic pattern, prove it (or validate it extensively), and answer each query with the closed form in $O(1)$.

??? question "Q8. When would you choose minimax over Sprague–Grundy?"

    When the game is partisan (players have different moves), has scores rather than win/lose outcomes, or is not a sum of independent impartial games. Sprague–Grundy requires impartial games under normal play.

## Complexity Summary

| Method | Time | Space |
| --- | --- | --- |
| Win/lose or Grundy DP | $O(\text{states} \times \text{moves})$ | $O(\text{states})$ |
| `mex` of $k$ values | $O(k)$ with a set | $O(k)$ |
| Nim decision and winning move | $O(k)$ | $O(1)$ |
| Sum of $k$ games | $\sum_i (\text{DP for } G_i) + O(k)$ | per component |
| Minimax on a tree of branching $b$, depth $d$ | $O(b^d)$ | $O(d)$ (DFS) |
| Alpha–beta, best ordering | $O(b^{\lceil d/2\rceil} + b^{\lfloor d/2 \rfloor})$ leaves | $O(d)$ |
| Alpha–beta, worst ordering | $O(b^d)$ | $O(d)$ |

## Key Takeaways

- Classify positions, not games: terminal is P; N iff some move reaches P; P iff all moves reach N.
- Backward induction on positions is dynamic programming over the game DAG.
- Nim is solved by XOR: P-positions are exactly those with nim-sum 0; the winning move reduces a pile containing the top bit of the nim-sum.
- Sprague–Grundy: every impartial game position equals a Nim pile of size $g = \operatorname{mex}$ of its options; sums of games XOR their Grundy numbers.
- For huge parameters, brute-force small cases, find the period, then prove it.
- Minimax handles scored and partisan games; alpha–beta returns the same value while pruning, reaching about $b^{d/2}$ leaves with good move ordering.
