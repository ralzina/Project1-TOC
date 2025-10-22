from enum import Enum


class ProjectSelection(str, Enum):
    sat = "SAT"
    k_partite = "K-Partite Matching"
    bin_packing = "Bin Packing - the Knapsack Problem"
    hamiltonian = "Hamiltonian Path/Cycle: Traveling Salesman Problems"
    graph_coloring = "Graph Coloring"
    k_clique = "K-Clique"

class SubProblemSelection(str, Enum):
    brute_force = "Brute Force"
    btracking = "Backtracking"
    best_case = "Best Case"
    simple = "Simple"
