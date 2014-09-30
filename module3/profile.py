import alg_project3_solution as sol
s = sol.Cluster.load_as_list('data/unifiedCancerData_111.csv')
sol.hierarchical_clustering(s, 9)
