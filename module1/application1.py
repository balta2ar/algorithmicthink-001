import random
import matplotlib.pyplot as plt
import alg_load_graph
import alg_dpa_trial
import project1


def norm(distr):
    total = float(sum(distr.itervalues()))
    return {degree: num / total for degree, num in distr.iteritems()}


def question1():
    graph = alg_load_graph.load_graph('./data/alg_phys-cite.txt')
    normed = norm(project1.in_degree_distribution(graph))
    plt.subplot(211)
    plt.plot(normed.keys(), normed.values(), 'bo', ms=2.0)
    plt.yscale('log')
    plt.title('Normalized in-degree distribution of a citation graph')
    plt.xlabel('In-degree')
    plt.ylabel('Normalized weight')
    plt.xlim(0, 1000)
    plt.tight_layout()
    plt.savefig('pic/question1.png')
    # plt.show()


def algorithm_er(n, p):
    graph = {key: set() for key in xrange(n)}
    for i in xrange(n):
        for j in xrange(n):
            if i == j:
                continue
            if random.random() < p:
                graph[i].add(j)
            if random.random() < p:
                graph[j].add(i)

    return graph


def avg_out_degree(graph):
    N = float(len(graph))
    return sum(len(x) for x in graph.itervalues()) / N


def question2():
    rnd = algorithm_er(3000, 0.1)
    normed = norm(project1.in_degree_distribution(rnd))
    plt.subplot(312)
    plt.plot(normed.keys(), normed.values(), 'bo', ms=2.0)
    plt.yscale('log')
    plt.title('Normalized in-degree distribution of a random graph')
    plt.xlabel('In-degree')
    plt.ylabel('Normalized weight')
    plt.tight_layout()
    plt.savefig('pic/question2.png')
    # plt.show()


def algorithm_dpa(n, m):
    graph = project1.make_complete_graph(m)
    dpa = alg_dpa_trial.DPATrial(m)
    for i in xrange(m, n):
        graph[i] = dpa.run_trial(m)
    return graph


def question3():
    graph = alg_load_graph.load_graph('./data/alg_phys-cite.txt')
    print('avg_out_degree', avg_out_degree(graph))
    dpa = algorithm_dpa(27700, 13)
    normed = norm(project1.in_degree_distribution(dpa))
    plt.subplot(212)
    plt.plot(normed.keys(), normed.values(), 'bo', ms=2.0)
    plt.yscale('log')
    plt.title('Normalized in-degree distribution of a DPA-generated graph')
    plt.xlabel('In-degree')
    plt.ylabel('Normalized weight')
    plt.xlim(0, 1000)
    plt.tight_layout()
    plt.savefig('pic/question3.png')
    plt.show()


def main():
    #from pprint import pprint as pp
    question1()
    # question2()
    question3()


if __name__ == '__main__':
    main()
