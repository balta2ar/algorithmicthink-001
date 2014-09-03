import random
import matplotlib.pyplot as plt
import alg_load_graph
import alg_dpa_trial
import project1


def norm(distr):
    total = float(sum(distr.itervalues()))
    return {degree: num / total for degree, num in distr.iteritems()}


def plot(graph, name, subplot=None, filename=None):
    if subplot:
        plt.subplot(subplot)
    plt.plot(graph.keys(), graph.values(), 'bo', ms=2.0)
    plt.loglog()
    plt.title('Normalized in-degree distribution of a %s graph (log-log)' % name)
    plt.xlabel('In-degree')
    plt.ylabel('Normalized weight')
    plt.xlim(0, 1000)
    plt.tight_layout()
    if filename:
        plt.savefig(filename)


def question1(subplot=None, filename=None):
    graph = alg_load_graph.load_graph('./data/alg_phys-cite.txt')
    normed = norm(project1.in_degree_distribution(graph))
    plot(normed, 'citation', subplot, filename)


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


def question2(subplot=None, filename=None):
    rnd = algorithm_er(3000, 0.1)
    normed = norm(project1.in_degree_distribution(rnd))
    plot(normed, 'random generated', subplot, filename)


def algorithm_dpa(n, m):
    graph = project1.make_complete_graph(m)
    dpa = alg_dpa_trial.DPATrial(m)
    for i in xrange(m, n):
        graph[i] = dpa.run_trial(m)
    return graph


def question3(subplot=None, filename=None):
    graph = alg_load_graph.load_graph('./data/alg_phys-cite.txt')
    print('avg_out_degree', avg_out_degree(graph))
    dpa = algorithm_dpa(27700, 13)
    normed = norm(project1.in_degree_distribution(dpa))
    plot(normed, 'DPA-generated', subplot, filename)


def main():
    # plot all graphs individually
    question1(None, 'pic/1-citation.png')
    plt.clf()
    question2(None, 'pic/2-random.png')
    plt.clf()
    question3(None, 'pic/3-dpa.png')

    # plot all three graphs on a single plot
    plt.clf()
    plt.cla()
    question1(311)
    question2(312)
    question3(313, 'pic/citation-random-dpa.png')

    # plot two graphs on a single plot and show it
    plt.clf()
    plt.cla()
    question1(211)
    question3(212, 'pic/citation-dpa.png')
    plt.show()


if __name__ == '__main__':
    main()
