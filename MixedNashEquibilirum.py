import itertools

# small epsilon value to handle floating point comparison issues
EPSILON = 1e-8


def read_input():
    n = int(input().strip())
    A = []
    for _ in range(n):
        row = input().strip().split()
        row = [float(x) for x in row]
        A.append(row)

    B = []
    for _ in range(n):
        row = input().strip().split()
        row = [float(x) for x in row]
        B.append(row)

    return n, A, B  


def gaussian_elimination(matrix, rhs):
    n = len(matrix)
    augmented = [list(matrix[i]) + [rhs[i]] for i in range(n)]

    for i in range(n):
        pivot = i
        max_val = abs(augmented[i][i])
        for r in range(i + 1, n):
            val = abs(augmented[r][i])
            if val > max_val:
                pivot = r
                max_val = val

        if max_val < EPSILON:
            return None

        if pivot != i:
            augmented[i], augmented[pivot] = augmented[pivot], augmented[i]

        pivot_val = augmented[i][i]
        if abs(pivot_val) < EPSILON:
            return None
        for j in range(i, n + 1):
            augmented[i][j] /= pivot_val

        for r in range(n):
            if r == i:
                continue
            factor = augmented[r][i]
            if abs(factor) < EPSILON:
                continue
            for j in range(i, n + 1):
                augmented[r][j] -= factor * augmented[i][j]

    solution = [augmented[i][n] for i in range(n)]
    return solution


# solve for Player 2's strategy q given supports S1, S2
def solve_for_q(A, S1, S2):
    k = len(S2)
    mat = [[0.0] * (k + 1) for _ in range(k + 1)]
    rhs = [0.0] * (k + 1)

    # build the linear system
    for row_idx, i in enumerate(S1):
        for col_idx, j in enumerate(S2):
            mat[row_idx][col_idx] = A[i][j]
        mat[row_idx][k] = -1.0

    mat[k] = [1.0] * k + [0.0]
    rhs[k] = 1.0

    sol = gaussian_elimination(mat, rhs)
    if sol is not None:
        return sol[:k], sol[k]

    # fallback: equal distribution (rarely used but avoids crashes)
    q_guess = [1.0 / k] * k
    u = sum(A[S1[0]][j] * q_guess[idx] for idx, j in enumerate(S2))
    return q_guess, u


# solve for Player 1's strategy p given supports S1, S2
def solve_for_p(B, S1, S2):
    k = len(S1)
    mat = [[0.0] * (k + 1) for _ in range(k + 1)]
    rhs = [0.0] * (k + 1)

    for row_idx, j in enumerate(S2):
        for col_idx, i in enumerate(S1):
            mat[row_idx][col_idx] = B[i][j]
        mat[row_idx][k] = -1.0

    mat[k] = [1.0] * k + [0.0]
    rhs[k] = 1.0

    sol = gaussian_elimination(mat, rhs)
    if sol is not None:
        return sol[:k], sol[k]

    # fallback case again (uniform)
    p_guess = [1.0 / k] * k
    v = sum(B[i][S2[0]] * p_guess[idx] for idx, i in enumerate(S1))
    return p_guess, v


def extract_full_strategy(n, p_s, q_s, S1, S2):
    p = [0.0] * n
    q = [0.0] * n

    sum_p = sum(p_s)
    sum_q = sum(q_s)

    if sum_p == 0 or sum_q == 0:
        return None

    # normalize (small floating rounding might cause weird scaling otherwise)
    p_s = [x / sum_p for x in p_s]
    q_s = [x / sum_q for x in q_s]

    # fill in the supports
    for idx, i in enumerate(S1):
        p[i] = p_s[idx]
    for idx, j in enumerate(S2):
        q[j] = q_s[idx]

    return p, q


def verify_equilibrium(n, A, B, p, q, S1, S2):
    # expected payoffs for rows in S1
    u_vals = [sum(A[i][j] * q[j] for j in range(n)) for i in S1]
    u = u_vals[0]

    # check all payoffs within tolerance
    if any(abs(val - u) > 1e-6 for val in u_vals):
        return False

    # check for any better deviation
    for i in range(n):
        if i not in S1:
            payoff = sum(A[i][j] * q[j] for j in range(n))
            if payoff > u + 1e-6:
                return False

    # do same for player 2
    v_vals = [sum(B[i][j] * p[i] for i in range(n)) for j in S2]
    v = v_vals[0]

    if any(abs(val - v) > 1e-6 for val in v_vals):
        return False

    for j in range(n):
        if j not in S2:
            payoff = sum(B[i][j] * p[i] for i in range(n))
            if payoff > v + 1e-6:
                return False

    return True


def find_mixed_equilibrium(n, A, B):
    for k in range(2, n + 1):
        for S1 in itertools.combinations(range(n), k):
            for S2 in itertools.combinations(range(n), k):
                q_s, u = solve_for_q(A, S1, S2)
                p_s, v = solve_for_p(B, S1, S2)

                # skip invalid probabilities
                if any(x < -1e-8 for x in p_s) or any(x < -1e-8 for x in q_s):
                    continue

                full = extract_full_strategy(n, p_s, q_s, S1, S2)
                if not full:
                    continue

                p, q = full
                if sum(x > 1e-6 for x in p) < 2 or sum(x > 1e-6 for x in q) < 2:
                    continue

                if verify_equilibrium(n, A, B, p, q, S1, S2):
                    return p, q
    return None


def find_pure_equilibrium(n, A, B):
    for i in range(n):
        for j in range(n):
            if all(A[i][j] >= A[ii][j] - EPSILON for ii in range(n)) and \
               all(B[i][j] >= B[i][jj] - EPSILON for jj in range(n)):
                p = [0.0] * n
                q = [0.0] * n
                p[i] = 1.0
                q[j] = 1.0
                return p, q
    return None


def main():
    n, A, B = read_input()

    # Try finding mixed equilibrium first
    result = find_mixed_equilibrium(n, A, B)

    if result is None:
        result = find_pure_equilibrium(n, A, B)

    if result is None:
        p = [1.0 / n] * n
        q = [1.0 / n] * n
    else:
        p, q = result

    print(" ".join(f"{x:.4f}" for x in p))
    print(" ".join(f"{x:.4f}" for x in q))


if __name__ == "__main__":
    main()
