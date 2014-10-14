'''
Project 4. Computing global and local alignments.

Authors of the course, I really HATE your pylint configured in SUCH A STUPID
AND PAINFUL WAY, GODDAMN IT!!! I hope you burn in hell.
'''


def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    '''
    Takes as input a set of characters alphabet and three scores diag_score,
    off_diag_score, and dash_score. The function returns a dictionary of
    dictionaries whose entries are indexed by pairs of characters in alphabet
    plus '-'. The score for any entry indexed by one or more dashes is
    dash_score. The score for the remaining diagonal entries is diag_score.
    Finally, the score for the remaining off-diagonal entries is
    off_diag_score
    '''
    scores = {'-': {'-': dash_score}}

    for let_a in alphabet:
        if let_a not in scores:
            scores[let_a] = {}
        scores[let_a]['-'] = dash_score
        scores['-'][let_a] = dash_score

        for let_b in alphabet:
            if let_a == let_b:
                scores[let_a][let_b] = diag_score
            else:
                scores[let_a][let_b] = off_diag_score

    return scores


def _clip(item, global_flag):
    '''Limit values to 0 when global_flag is not set'''
    return item if global_flag else max(0, item)


def compute_alignment_matrix(seq_x, seq_y, scores, global_flag):
    '''
    Takes as input two sequences seq_x and seq_y whose elements share a common
    alphabet with the scoring matrix scores. The function computes and
    returns the alignment matrix for seq_x and seq_y as described in the
    Homework.  If global_flag is True, each entry of the alignment matrix is
    computed using the method described in Question 8 of the Homework. If
    global_flag is False, each entry is computed using the method described in
    Question 12 of the Homework
    '''

    rows, cols = len(seq_x), len(seq_y)
    alignment = [[0 for _ in range(cols + 1)] for _ in range(rows + 1)]
    for idx_i in range(1, rows + 1):
        alignment[idx_i][0] = _clip(alignment[idx_i - 1][0] + scores[seq_x[idx_i - 1]]['-'], global_flag)
    for idx_j in range(1, cols + 1):
        alignment[0][idx_j] = _clip(alignment[0][idx_j - 1] + scores['-'][seq_y[idx_j - 1]], global_flag)
    for idx_i in range(1, rows + 1):
        for idx_j in range(1, cols + 1):
            alignment[idx_i][idx_j] = max([
                _clip(alignment[idx_i - 1][idx_j - 1] + scores[seq_x[idx_i - 1]][seq_y[idx_j - 1]], global_flag),
                _clip(alignment[idx_i - 1][idx_j] + scores[seq_x[idx_i - 1]]['-'], global_flag),
                _clip(alignment[idx_i][idx_j - 1] + scores['-'][seq_y[idx_j - 1]], global_flag)
            ])
    return alignment


def max_index(alignment, rows, cols):
    '''Position of max item in the matrix'''
    max_i, max_j = 0, 0
    for idx_i in range(rows + 1):
        for idx_j in range(cols + 1):
            if alignment[idx_i][idx_j] > alignment[max_i][max_j]:
                max_i, max_j = idx_i, idx_j
    return max_i, max_j


def compute_alignment(seq_x, seq_y, scores, alignment, global_flag):
    '''Universal function for computing global and local alignments'''
    idx_i, idx_j = len(seq_x), len(seq_y)
    if not global_flag:
        idx_i, idx_j = max_index(alignment, len(seq_x), len(seq_y))
    best_score = alignment[idx_i][idx_j]
    new_xs, new_ys = '', ''

    def cond_global(idx_i, idx_j):
        '''Condition for while loops in global mode'''
        if idx_j is None:
            return idx_i != 0
        elif idx_i is None:
            return idx_j != 0
        else:
            return idx_i != 0 and idx_j != 0

    def cond_local(idx_i, idx_j):
        '''Condition for while loops in local mode'''
        return alignment[idx_i][idx_j] != 0

    cond = cond_global if global_flag else cond_local

    while cond(idx_i, idx_j):
        if alignment[idx_i][idx_j] == _clip(alignment[idx_i - 1][idx_j - 1] + scores[seq_x[idx_i - 1]][seq_y[idx_j - 1]], global_flag):
            new_xs, new_ys = seq_x[idx_i - 1] + new_xs, seq_y[idx_j - 1] + new_ys
            idx_i, idx_j = idx_i - 1, idx_j - 1
        elif alignment[idx_i][idx_j] == _clip(alignment[idx_i - 1][idx_j] + scores[seq_x[idx_i - 1]]['-'], global_flag):
            new_xs, new_ys = seq_x[idx_i - 1] + new_xs, '-' + new_ys
            idx_i = idx_i - 1
        else:
            new_xs, new_ys = '-' + new_xs, seq_y[idx_j - 1] + new_ys
            idx_j = idx_j - 1
    while cond(idx_i, None if global_flag else idx_j):
        new_xs, new_ys = seq_x[idx_i - 1] + new_xs, '-' + new_ys
        idx_i = idx_i - 1
    while cond(None if global_flag else idx_i, idx_j):
        new_xs, new_ys = '-' + new_xs, seq_y[idx_j - 1] + new_ys
        idx_j = idx_j - 1
    return best_score, new_xs, new_ys


def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    '''Compute global alignment'''
    return compute_alignment(seq_x, seq_y,
                             scoring_matrix,
                             alignment_matrix,
                             global_flag=True)


def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    '''Compute local alignment'''
    return compute_alignment(seq_x, seq_y,
                             scoring_matrix,
                             alignment_matrix,
                             global_flag=False)


def test(seq_x, seq_y, global_flag):
    '''Testing'''
    alpha = set(seq_x) | set(seq_y)
    scores = build_scoring_matrix(alpha, 10, 4, -1)
    align = compute_alignment_matrix(seq_x, seq_y, scores, global_flag)
    return compute_alignment(seq_x, seq_y, scores, align, global_flag)
