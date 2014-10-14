def sample_cost(a, b):
    if '-' in (a, b):
        return -6
    elif a == b:
        return 10
    else:
        return 4


GLOBAL = False


def clip(x):
    return x if GLOBAL else max(0, x)


def compute_global_alignment_scores(X, Y, M):
    m, n = len(X), len(Y)
    S = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    for i in range(1, m + 1):
        S[i][0] = clip(S[i - 1][0] + M(X[i - 1], '-'))
    for j in range(1, n + 1):
        S[0][j] = clip(S[0][j - 1] + M('-', Y[j - 1]))
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            S[i][j] = max([
                clip(S[i - 1][j - 1] + M(X[i - 1], Y[j - 1])),
                clip(S[i - 1][j] + M(X[i - 1], '-')),
                clip(S[i][j - 1] + M('-', Y[j - 1]))
            ])
    return S


def max_index(S, m, n):
    mi, mj = 0, 0
    for i in range(m + 1):
        for j in range(n + 1):
            if S[i][j] > S[mi][mj]:
                mi, mj = i, j
    return mi, mj


def compute_alignment(X, Y, M, S):
    i, j = len(X), len(Y)
    if not GLOBAL:
        i, j = max_index(S, len(X), len(Y))
    print('compute_alignment starts at', i, j, S[i][j])
    NX, NY = '', ''

    def cond_global(i, j):
        if j is None:
            return i != 0
        elif i is None:
            return j != 0
        else:
            return i != 0 and j != 0

    def cond_local(i, j):
        return S[i][j] != 0

    cond = cond_global if GLOBAL else cond_local

    while cond(i, j):
        if S[i][j] == clip(S[i - 1][j - 1] + M(X[i - 1], Y[j - 1])):
            NX, NY = X[i - 1] + NX, Y[j - 1] + NY
            i, j = i - 1, j - 1
        elif S[i][j] == clip(S[i - 1][j] + M(X[i - 1], '-')):
            NX, NY = X[i - 1] + NX, '-' + NY
            i = i - 1
        else:
            NX, NY = '-' + NX, Y[j - 1] + NY
            j = j - 1
    while cond(i, None if GLOBAL else j):
        NX, NY = X[i - 1] + NX, '-' + NY
        i = i - 1
    while cond(None if GLOBAL else i, j):
        NX, NY = '-' + NX, Y[j - 1] + NY
        j = j - 1
    print('compute_alignment ends at', i, j, S[i][j])
    return NX, NY


def global_alignment(xs, ys, cost=None):
    if cost is None:
        cost = sample_cost

    scores = compute_global_alignment_scores(xs, ys, cost)
    print('scores', scores)
    # return scores
    return compute_alignment(xs, ys, cost, scores)
