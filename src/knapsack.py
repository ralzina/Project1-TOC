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
1,17,5,BruteForce,YES,0.000145,"{3:1,5:1,7:1,2:1}"
2,30,6,BruteForce,NO,0.000089,{}
"""

from src.helpers.knapsack_helper import KnapsackAbstractClass
from typing import List, Optional, Tuple, Dict
from collections import defaultdict


class Knapsack(KnapsackAbstractClass):
    """
        NOTE: The output of the CSV file should be same as EXAMPLE OUTPUT above otherwise you will loose marks
        For this you dont need to save anything just make sure to return exact related output.
        
        For ease look at the Abstract Solver class and basically we are having the run method which does the saving
        of the CSV file just focus on the logic
    """

    def knapsack_backtracking(self, target: int, coins: List[int]) -> Tuple[bool, Optional[List[int]]]:
        return False, None

    def knapsack_bruteforce(self, target: int, coins: Dict[int,int], used: Dict[int,int] = None) -> Tuple[bool, Optional[Dict[int,int]]]:
            """
            Generates a brute force solution by trying all possible combinations
            
            This recursive function tries using one of each coin recursively to try all combinations.
            In each recursive call, it subtracts the used coin to the target.
            If the target ever reaches exactly 0, there is a solution, but if not there isn't.
            
            Params
            - coins: dictionary of coin values and count pairs
            - target: amount that must be reached
            
            Return
            Tuple[
                bool: True if you can make a combination of coins to reach target or False if you can't,
                Optional[Dict[int,int]]: value, count pairs of each coin used and what quantity
            ]

            Example
            >>> coins = {1: 5, 4: 2}
            >>> target = 6
            >>> knapsack_bruteforce(coins,counts,target)
            (True, {1: 2, 4: 1})
            - This means 2 coins of value 1 and 1 coin of value 4 = 6
            and note using 6 1's is not possible since only 5 1's exist
            """

            if not used:
                used = defaultdict(int)

            if target == 0:
                return True, dict(used)
            
            # Go through coins
            for coin in coins:
                # If no more coins available, continue
                if used[coin] >= coins[coin]:
                    continue
                
                # If a coin is available, use and subtract the value from target
                used[coin] += 1
                feasible, solution = self.knapsack_bruteforce(target-coin,coins,used)

                # If we reached a solution, return
                if feasible:
                    return True, dict(solution)

                # Restore original count
                used[coin] -= 1

            # If no solution worked, return False
            return False, {}               

    def knapsack_simple(self, target: int, coins: List[int]) -> Tuple[bool, Optional[List[int]]]:
        pass

    def knapsack_bestcase(self, target: int, coins: List[int]) -> Tuple[bool, Optional[List[int]]]:
        return False, None
