import pytest
import os
from src.helpers.project_selection_enum import ProjectSelection, SubProblemSelection
from src.helpers.constants import CONFIGURATION_FILE_PATH, parse_config, TEST_FILE, TEST_BESTCASE_FILE
from src.knapsack_garcias import Knapsack
from src.helpers.dmaics_parser import parse_multi_instance_knapsack
import json

def parse_bestcase_file(filename):
    tests = []
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()] 

    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("c "):
            parts = line.split()
            test_id = parts[1]
            target = int(parts[2])

            s = parts[3][1:-1]  # remove {}
            items = list(map(int, s.split(',')))  # convert all to ints

            expected_dict = {}
            for j in range(0, len(items), 2):
                value = items[j]
                amount = items[j+1]
                expected_dict[value] = amount

            i += 1

            # Read next line p knap <#coins>
            p_line = lines[i]
            if not p_line.startswith("p knap"):
                raise ValueError(f"Expected 'p knap' line after c line, got: {p_line}")
            num_coins = int(p_line.split()[2])
            i += 1

            # Read coin lines
            coins = {}
            for _ in range(num_coins):
                value, amount = map(int, lines[i].split())
                coins[value] = amount
                i += 1

            # Add to tests
            tests.append((test_id, target, coins, expected_dict))
        else:
            i += 1  # skip unknown lines

    return tests

@pytest.fixture(scope="module")
def solver():
    # Parse configuration and initialize solver
    selection, sub_problem = parse_config(CONFIGURATION_FILE_PATH)

    if selection["name"] != ProjectSelection.bin_packing.name:
        pytest.skip("This test only runs for bin_packing projects")

    return Knapsack(TEST_FILE)

def test_knapsack_bruteforce(solver):

    if SubProblemSelection.brute_force not in solver.sub_problems:
        pytest.skip("Brute force test not selected")

    for _, target, coins, solvable in solver.solution_instances:
        bt_ok, status = solver.knapsack_bruteforce(target, coins)
        if status == "Not implemented":
            pytest.skip(status)
        elif solvable != 0:
            expected = solvable == 1
            assert bt_ok == expected


def test_knapsack_backtracking(solver):

    if SubProblemSelection.btracking not in solver.sub_problems:
        pytest.skip("Backtracking test not selected")

    for _, target, coins, solvable in solver.solution_instances:
        bt_ok, status = solver.knapsack_backtracking(target, coins)
        if status == "Not implemented":
            pytest.skip(status)
        elif solvable != 0:
            expected = solvable == 1
            assert bt_ok == expected

def test_knapsack_bestcase():
    solver = Knapsack(TEST_BESTCASE_FILE)  # your solver
    tests = parse_bestcase_file(TEST_BESTCASE_FILE)

    for _, target, coins, expected_dict in tests:
        _, solution = solver.knapsack_bestcase(target, coins)

        if solution == "Not implemented":
            pytest.skip(solution)
        else:
            assert solution == expected_dict or sum(k*v for k,v in solution.items()) == sum(k*v for k,v in expected_dict.items())


def test_knapsack_simple(solver):

    if SubProblemSelection.btracking not in solver.sub_problems:
        pytest.skip("Backtracking test not selected")

    for _, target, coins, solvable in solver.solution_instances:
        bt_ok, status = solver.knapsack_simple(target, coins)
        if status == "Not implemented":
            pytest.skip(status)
        elif solvable != 0:
            expected = solvable == 1
            assert bt_ok == expected