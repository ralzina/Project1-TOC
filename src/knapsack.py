"""
Knapsack - DIMACS-like Multi-instance Format
--------------------------------------------------------------------
Project 1: Tough Problems & The Wonderful World of NP

INPUT FORMAT (multi-instance file):
-----------------------------------
Each instance starts with a comment and a problem definition:

c <instance_id> <target_value> <status?>
p knap <n_coins>
d
d
d
...

Example:
c 1 17 ?
p knap 5
3
5
11
7
2
c 2 30 ?
p knap 6
4
6
10
11
13
14

OUTPUT:
-------
A CSV file named 'resultsfile.csv' with columns:
instance_id, target_value, n_coins method, feasible, time_seconds, subset

EXAMPLE OUTPUT
--------------
instance_id,n_coins,target_value,method,feasible,time_seconds,subset
1,17,5,BruteForce,YES,0.000145,"[1,1,0,1,1]"
2,30,6,BruteForce,NO,0.000089,[]
"""

from src.helpers.knapsack_helper import KnapsackAbstractClass
from typing import List, Optional, Tuple


class Knapsack(KnapsackAbstractClass):
    """
        NOTE: The output of the CSV file should be same as EXAMPLE OUTPUT above otherwise you will loose marks
        For this you dont need to save anything just make sure to return exact related output.
        
        For ease look at the Abstract Solver class and basically we are having the run method which does the saving
        of the CSV file just focus on the logic
    """

    def knapsack_backtracking(self, target: int, coins: List[int]) -> Tuple[bool, Optional[List[int]]]:
        pass

    def knapsack_bruteforce(self, target: int, coins: List[int]) -> Tuple[bool, Optional[List[int]]]:
        pass

    def knapsack_simple(self, target: int, coins: List[int]) -> Tuple[bool, Optional[List[int]]]:
        pass

    def knapsack_bestcase(self, target: int, coins: List[int]) -> Tuple[bool, Optional[List[int]]]:
        pass
