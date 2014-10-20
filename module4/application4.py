from json import dumps
from json import loads
from random import choice
from random import shuffle
from operator import itemgetter
from string import ascii_lowercase

import matplotlib.pyplot as plt
import numpy as np

from alg_application4_provided import read_scoring_matrix
from alg_application4_provided import read_protein

from solution4 import compute_local_alignment
from solution4 import compute_global_alignment
from solution4 import compute_alignment_matrix
from solution4 import build_scoring_matrix


# URLs for data files
PAM50_URL = "data/alg_PAM50.txt"
HUMAN_EYELESS_URL = "data/alg_HumanEyelessProtein.txt"
FRUITFLY_EYELESS_URL = "data/alg_FruitflyEyelessProtein.txt"
CONSENSUS_PAX_URL = "data/alg_ConsensusPAXDomain.txt"
WORD_LIST_URL = "data/assets_scrabble_words3.txt"


def agreement(xs, ys, scoring, alignment):
    score, x, y = compute_global_alignment(xs, ys, scoring, alignment)
    similar = [1. for (a, b) in zip(x, ys) if a == b]
    return 100. * len(similar) / len(x)


def rprot(n, alpha):
    return ''.join([choice(alpha) for _ in range(n)])


def compare(n, nh, nf, alpha, cons, scoring, align):
    ag1, ag2 = [], []

    for i in range(n):
        xs, ys = rprot(nh, alpha), rprot(nf, alpha)
        _, xs, ys = compute_local_alignment(xs, ys, scoring, align)
        xs_nodash = ''.join([x for x in xs if x != '-'])
        ys_nodash = ''.join([x for x in ys if x != '-'])
        ag1.append(agreement(xs_nodash, cons, scoring, align))
        ag2.append(agreement(ys_nodash, cons, scoring, align))

    hc_agree = sum(ag1) / float(n)
    fc_agree = sum(ag2) / float(n)
    print('Random Human vs Consensus agree = %s%%' % hc_agree)
    print('Random Fly vs Consensus agree = %s%%' % fc_agree)


def question1():
    human = read_protein(HUMAN_EYELESS_URL)
    fly = read_protein(FRUITFLY_EYELESS_URL)
    print(len(human), len(fly))

    scoring = read_scoring_matrix(PAM50_URL)
    local_align = compute_alignment_matrix(human, fly, scoring, False)
    score, xs, ys = compute_local_alignment(human, fly, scoring, local_align)
    print('Question 1')
    print(score)
    print(xs)
    print(ys)
    print()

    print('Question 2')
    consensus = read_protein(CONSENSUS_PAX_URL)
    human_nodash = ''.join([x for x in xs if x != '-'])
    fly_nodash = ''.join([x for x in ys if x != '-'])

    hc_global_align = compute_alignment_matrix(human_nodash, consensus, scoring, True)
    fc_global_align = compute_alignment_matrix(fly_nodash, consensus, scoring, True)

    hc_agree = agreement(human_nodash, consensus, scoring, hc_global_align)
    fc_agree = agreement(fly_nodash, consensus, scoring, fc_global_align)
    print('Human vs Consensus agree = %s%%' % hc_agree)
    print('Fly vs Consensus agree = %s%%' % fc_agree)

    # alpha = "ACBEDGFIHKMLNQPSRTWVYXZ"
    # compare(1000,
    #         len(human), len(fly), alpha,
    #         consensus, scoring, local_align)

    # print()


def generate_null_distribution(seq_x, seq_y, scoring_matrix, num_trials):
    distr = {}
    raw = []

    try:
        with open('distr.json') as f:
            pair = loads(f.read())
            return pair['distr'], pair['raw']
    except Exception as e:
        print('cant open file', str(e))

    for _ in range(num_trials):
        temp = list(seq_y)
        shuffle(temp)
        rand_y = ''.join(temp)
        align = compute_alignment_matrix(seq_x, rand_y, scoring_matrix, False)
        score, _, _ = compute_local_alignment(seq_x, rand_y, scoring_matrix, align)
        if score not in distr:
            distr[score] = 0
        distr[score] += 1
        raw.append(score)
    with open('distr.json', 'w') as f:
        f.write(dumps({'distr': distr, 'raw': raw}))
    return distr, raw


def norm(d):
    total = float(sum(d.itervalues()))
    return {k: v / total for k, v in d.iteritems()}


def str_keys(d):
    return {int(k): v for k, v in d.iteritems()}


def question4(filename):
    human = read_protein(HUMAN_EYELESS_URL)
    fly = read_protein(FRUITFLY_EYELESS_URL)
    scoring = read_scoring_matrix(PAM50_URL)
    distr, raw = generate_null_distribution(human, fly, scoring, 1000)
    from pprint import pprint as pp
    distr = str_keys(distr)
    pp(distr)
    distr = norm(distr)

    pairs = list(distr.iteritems())
    pairs = sorted(pairs, key=itemgetter(0))
    print(pairs)
    index = np.arange(len(pairs))
    plt.bar(index, map(itemgetter(1), pairs))
    plt.xticks(index + 0.4, map(itemgetter(0), pairs), fontsize=8)
    plt.xlabel('Scores')
    plt.ylabel('Fraction of total trials')
    plt.title('Distribution of scores')
    plt.tight_layout()
    plt.savefig(filename)

    s_score = 875
    n = 1000
    mean = sum(raw) / n
    std = np.sqrt(sum((x - mean) ** 2 for x in raw) / n)
    z_score = (s_score - mean) / std

    print('mean = %f' % mean)
    print('std = %f' % std)
    print('z_score = %f' % z_score)


def edit_dist(xs, ys):
    alphabet = ascii_lowercase
    scoring = build_scoring_matrix(alphabet, 2, 1, 0)
    align = compute_alignment_matrix(xs, ys, scoring, True)
    score, x, y = compute_global_alignment(xs, ys, scoring, align)
    return len(xs) + len(ys) - score


def check_spelling(checked_word, dist, word_list):
    return set([word for word in word_list
                if edit_dist(checked_word, word) <= dist])


def question7():
    #dist = edit_dist('abb', 'aa')
    #print(dist)
    words = [x.strip() for x in open(WORD_LIST_URL).readlines()]
    humble = check_spelling('humble', 1, words)
    firefly = check_spelling('firefly', 2, words)
    print(len(humble), humble)
    print(len(firefly), firefly)


def main():
    question1()
    question4('pic/question4.png')
    question7()


if __name__ == '__main__':
    main()
