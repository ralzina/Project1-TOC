import os
from typing import List, Tuple
from collections import defaultdict

def parse_multi_instance_dimacs(path: str) -> Tuple[str, int, List[List[int]]]:
    """
    Parses a DIMACS-like file containing multiple CNF instances.
    Returns a list of (instance_id, n_vars, clauses) tuples.
    """

    if not os.path.exists(path = path):
        raise Exception(f"File path: {path} does not exists!!")

    instances = []
    with open(path) as f:
        lines = [ln.strip() for ln in f if ln.strip()]
    
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("c "):
            # Example: c 3 2 ?
            parts = line.split()
            instance_id = parts[1] if len(parts) > 1 else str(len(instances) + 1)
            i += 1
            if i >= len(lines):
                break
            # Expect next line: p cnf n_vars n_clauses
            if not lines[i].startswith("p cnf"):
                raise ValueError(f"Expected 'p cnf' after {line}")
            _, _, n_vars_str, n_clauses_str = lines[i].split()
            n_vars = int(n_vars_str)
            n_clauses = int(n_clauses_str)
            i += 1
            clauses = []
            # Read next n_clauses lines (allow commas)
            for _ in range(n_clauses):
                if i >= len(lines) or lines[i].startswith("c "):
                    break
                clause = [int(x) for x in lines[i].replace(",", " ").split() if x != "0"]
                if clause:
                    clauses.append(clause)
                i += 1
            instances.append((instance_id, n_vars, clauses))
        else:
            i += 1
    return instances


def parse_multi_instance_graph(path: str):
    """
    Parse file into list of (instance_id, k, n_vertices, edges)
    Each instance starts with `c` and `p edge` lines.
    """
    instances = []
    with open(path) as f:
        lines = [ln.strip() for ln in f if ln.strip()]

    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("c "):
            parts = line.split()
            instance_id = parts[1] if len(parts) > 1 else str(len(instances) + 1)
            k = int(parts[2]) if len(parts) > 2 else 3
            i += 1
            if i >= len(lines) or not lines[i].startswith("p cnf"):
                raise ValueError(f"Expected 'p cnf' after line: {line}")
            _, _, n_vertices_str, n_edges_str = lines[i].split()
            n_vertices = int(n_vertices_str)
            n_edges = int(n_edges_str)
            i += 1
            edges = []
            # Read next n_edges lines (edge pairs)
            for _ in range(n_edges):
                if i >= len(lines) or lines[i].startswith("c "):
                    break
                parts = lines[i].replace(",", " ").split()
                if len(parts) >= 2:
                    u, v = int(parts[0]), int(parts[1])
                    edges.append((u - 1, v - 1))  # use 0-based indexing
                i += 1
            instances.append((instance_id, k, n_vertices, edges))
        else:
            i += 1

    return instances

def parse_multi_instance_knapsack(path: str):
    """
    Parse file into list of (instance_id, target, n_coins)
    Each instance starts with `c` and `p coins` lines.
    """
    instances = []
    with open(path) as f:
        lines = [ln.strip() for ln in f if ln.strip()]

    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("c "):
            parts = line.split()
            instance_id = parts[1]
            target = int(parts[2])
            i += 1
            if i >= len(lines) or not lines[i].startswith("p knap"):
                raise ValueError(f"Expected 'p knap' after line: {line}")
            _, _, unique_coins_str= lines[i].split()
            unique_coins = int(unique_coins_str)
            i += 1
            coins = defaultdict(int)
            # Read next n_coins lines
            for _ in range(unique_coins):
                if i >= len(lines) or lines[i].startswith("c "):
                    break
                parts = lines[i].replace(",", " ").split()
                if len(parts) >= 2:
                    coin = int(parts[0])
                    coins[coin] = int(parts[1])
                i += 1
            instances.append((instance_id, target, coins))
        else:
            i += 1

    return instances