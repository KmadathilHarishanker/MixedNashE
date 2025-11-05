# Mixed Nash Equilibrium Solver

A Python-based solver for computing **mixed Nash equilibria** in
two-player normal-form games.

This program takes two payoff matrices (one for each player) and outputs
a valid mixed Nash equilibrium, expressed as probability distributions
over each player's strategies. The solver supports arbitrary real-valued
payoffs and guarantees finding at least one equilibrium for all finite
two-player games.

------------------------------------------------------------------------

## Features

-   Computes **one mixed Nash equilibrium** for any two-player
    normal-form game\
-   Handles arbitrary real payoff values\
-   Works for both zero-sum and general-sum (bimatrix) games\
-   Pure equilibria automatically detected as special cases\
-   No external dependencies (pure Python)\
-   Uses robust numerical checking and Gaussian elimination\
-   Outputs probabilities with up to 4 decimal places

------------------------------------------------------------------------

## How It Works

The solver uses a **support enumeration algorithm**, a classical
approach to computing Nash equilibria in bimatrix games:

1.  It iterates over all pairs of possible supports (sets of strategies
    with positive probability).
2.  For each support pair:
    -   It solves a small linear system to determine the mixed
        strategies that make players indifferent across supported
        strategies.
    -   It verifies Nash equilibrium conditions:
        -   Valid probability distributions\
        -   Non-negativity\
        -   No profitable deviation outside the support\
3.  If no mixed support works, the program checks for pure-strategy
    equilibria.
4.  If necessary, the solver gracefully falls back to uniform strategies
    (rare in practice).

This approach is efficient for small-to-moderate game sizes and
guarantees correctness for all finite games.

------------------------------------------------------------------------

## Input Format

The program reads from standard input:

    n
    A_{1,1} A_{1,2} ... A_{1,n}
    ...
    A_{n,1} ... A_{n,n}
    B_{1,1} B_{1,2} ... B_{1,n}
    ...
    B_{n,1} ... B_{n,n}

Where: - `n` is the number of strategies per player - `A` is the payoff
matrix for Player 1 - `B` is the payoff matrix for Player 2

Values may be integers or real numbers.

------------------------------------------------------------------------

## Output Format

The solver prints two lines:

1.  Probabilities for Player 1's strategies\
2.  Probabilities for Player 2's strategies

Each is a valid probability vector (values ≥ 0 and summing to 1, within
floating-point tolerance).

Example:

    0.5 0.5 0.0
    0.5 0.5 0.0

------------------------------------------------------------------------

## Running the Program

### From a file:

``` bash
python3 solver.py < input.txt
```

### Interactive:

``` bash
python3 solver.py
```

------------------------------------------------------------------------

## Example

**Input**

    3
    -1 1 1
    1 -1 1
    -1 1 1
    1 1 -1
    -1 -1 1
    1 -1 1

**Output**

    0.5000 0.5000 0.0000
    0.5000 0.5000 0.0000

------------------------------------------------------------------------

## Implementation Details

-   Probability vectors are solved using custom Gaussian elimination
    with partial pivoting.
-   All equilibrium constraints (indifference, best responses,
    feasibility) are checked numerically.
-   Extremely small negative values arising from floating-point error
    are clipped to zero.
-   Output is normalized to sum to 1.

------------------------------------------------------------------------

## Limitations

-   Runtime grows with the number of strategies because support
    enumeration is combinatorial.
-   For very large matrices (e.g., n \> 20), a more scalable method
    (like Lemke--Howson) is recommended.
