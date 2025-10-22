import os
from typing import List, Tuple

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