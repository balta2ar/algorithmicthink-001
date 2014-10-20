algorithmicthink-001
====================

### Coursera [Algorithmic Thinking](https://class.coursera.org/algorithmicthink-001)

This is a source code for projects and applications of Algorithmic Thinking
class on Coursera.

### Assignments

## 1. Graph Basics and Random Digraphs

The goal of this Module is to get you started with simple, yet central, concepts
in graph theory, simple principles of discrete probability, and a light version
of hypothesis testing.

For your first project, you will write Python code that creates dictionaries
corresponding to some simple examples of graphs. You will also implement two
short functions that compute information about the distribution of the
in-degrees for nodes in these graphs. You will then use these functions in the
Application component of Module 1 where you will analyze the degree distribution
of a citation graph for a collection of physics papers. This final portion of
module will be peer assessed.

## 2. BFS and Connected Components

The goal of this Module is for you to learn about graph exploration, how to use
it to compute the connected components of graphs, and how to use the latter
structure to reason about the resilience of networks. The module emphasizes the
efficiency of algorithms, asymptotics, and the significance of efficient
implementations. You will be exposed again to random graphs, graph properties,
and the use of data structures like queues.

For the Project component of Module 2, you will first write Python code that
implements breadth-first search. Then, you will use this function to compute the
set of connected components (CCs) of an undirected graph as well as determine
the size of its largest connected component. Finally, you will write a function
that computes the resilience of a graph (measured by the size of its largest
connected component) as a sequence of nodes are deleted from the graph.

You will use these functions in the Application component of Module 2 where you
will analyze the resilience of a computer network, modeled by a graph. As in
Module 1, graphs will be represented using dictionaries.

## 3. Divide and conquer method and applications to clustering

The goal of this Module is for you to learn about the closest pair problem, how
to solve it using the divide-and-conquer algorithmic strategy, and how to use
the solution in algorithms for data clustering, which is a very powerful tool in
the toolkit of any data scientist. You will also use the programs you write to
cluster cancer data collected from many counties across the United States. The
module emphasizes divide-and-conquer algorithms, their recursive
implementations, and how to analyze the running times of such algorithms.

For the Project and Application portion of Module 3, we will implement and
assess two methods for clustering data. For Project 3, you will implement two
methods for computing closest pairs and two methods for clustering data. In
Application 3, you will then compare these two clustering methods in terms of
efficiency, automation, and quality.

## 4. Dynamic programming and applications to sequence alignment and edit distances

The goal of this Module is for you to learn about the pairwise sequence
alignment problem, how to solve two versions of it (local and global) using the
dynamic programming (DP) algorithmic strategy, and how to use the solutions in
two applications involving genomic data and spell checking. The module
emphasizes dynamic programming algorithms and their implementation.

In Homework 4, we explored the use of dynamic programming in measuring the
similarity between two sequences of characters. Given an alphabet Σ and a
scoring matrix M defined over Σ∪{′−′}, the dynamic programming method computed a
score that measured the similarity of two sequences X and Y based on the values
of this scoring matrix. In particular, this method involved computing an
alignment matrix S between X and Y whose entry Sij scored the similarity of the
substrings X[0…i−1] and Y[0…j−1]. These notes provided an overview of the
process.

In Project 4, we will implement four functions. The first pair of functions will
return matrices that we will use in computing the alignment of two sequences.
The second pair of functions will return global and local alignments of two
input sequences based on a provided alignment matrix. You will then use these
functions in Application 4 to analyze two problems involving comparison of
similar sequences.
