# Project 1 — Finding a Mixed Nash Equilibrium  
CMSC 474 — Fall 2025

## Overview
This project implements an algorithm to compute a **mixed Nash equilibrium (NE)** for a two-player normal-form game.  
The input consists of two `n × n` payoff matrices — one for each player — and the output is any valid mixed NE, expressed as two probability vectors.

A mixed Nash equilibrium always exists (Nash, 1950), and the assignment accepts **any** correct equilibrium.

---

## Input Format
The program reads from **standard input**:

1. An integer `n`  
2. An `n × n` payoff matrix for Player 1  
3. An `n × n` payoff matrix for Player 2  

Numbers may be integers or real values.

---

## Output Format
The program prints exactly **two lines**:

- Line 1: Player 1’s mixed strategy (probabilities for each row)  
- Line 2: Player 2’s mixed strategy (probabilities for each column)

Each line must form a valid probability distribution:  
- values ≥ 0  
- sum to 1 (within floating-point tolerance)  
- up to 4 decimal places  

---

## Approach
This solution uses a **support enumeration algorithm**, which is guaranteed to find at least one Nash equilibrium for sufficiently small games.

### Why support enumeration?
- Each player in equilibrium is indifferent among strategies in their support.  
- For supports of size `k`, this produces a small system of linear equations that can be solved directly.  
- Because typical `n` in this project’s test cases is small, this method is efficient and passes within time limits.

### Algorithm Summary
1. For support sizes `k = 1..n`, enumerate all support pairs `(S, T)` of size `k`.  
2. For each pair:
   - Solve a linear system to compute:
     - Player 1’s mixed strategy over `S`
     - Player 2’s mixed strategy over `T`
   - Verify all Nash equilibrium conditions:
     - Indifference within support  
     - No deviation outside support  
     - Probabilities are non-negative and sum to 1  
3. If no mixed support works, fall back to checking pure-strategy Nash equilibria.  
4. If all else fails (pathological case), return uniform random distributions (not expected in normal inputs).

### Key Features
- Custom Gaussian elimination (no external libraries required)
- Numerical stability improvements  
- Full best-response verification  
- Handles arbitrary real payoff matrices  

---

## How to Run
From the command line:

```bash
python3 project1.py < input.txt
