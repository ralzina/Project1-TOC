"""
Knapsack - DIMACS-like Multi-instance Format
--------------------------------------------------------------------
Project 1: Tough Problems & The Wonderful World of NP

INPUT FORMAT (multi-instance file):
-----------------------------------
Each instance starts with a comment and a problem definition:

c <instance_id> <target_value> <status?>
p knap <unique_coins>
u v
u v
u v
...

u is the value of the coin
v is the amount of that coin available

Example:
c 1 17 ?
p knap 5
3 3
5 2
11 1
7 9
2 3
c 2 29 ?
p knap 6
7 1
20 1
17 4
15 2
19 5
14 12

OUTPUT:
-------
A CSV file named 'output_<subproblem>_knapsack_results_garcias.csv' with columns:
instance_id, target, n_coins method, feasible, time_seconds, coin_combination

EXAMPLE OUTPUT
--------------
instance_id,n_coins,target_value,method,feasible,time_seconds,coin_combination
1,17,5,BruteForce,YES,0.000145,"{3:1,5:1,7:1,2:1}"
2,29,6,BruteForce,NO,0.000089,{}
"""

from src.helpers.knapsack_helper_garcias import KnapsackAbstractClass
from typing import List, Optional, Tuple, Dict
from collections import defaultdict


class Knapsack(KnapsackAbstractClass):
    """
        NOTE: The output of the CSV file should be same as EXAMPLE OUTPUT above otherwise you will loose marks
        For this you dont need to save anything just make sure to return exact related output.
        
        For ease look at the Abstract Solver class and basically we are having the run method which does the saving
        of the CSV file just focus on the logic
    """

    def knapsack_backtracking(self, target: int, coins: Dict[int, int], used: Dict[int,int] = None) -> Tuple[bool, Optional[List[int]]]:
        """
            Generates a backtracking solution by trying all possible combinations and pruning combinations that have become invalid
            
            This recursive function tries using one of each coin recursively to try all combinations.
            In each recursive call, it subtracts the used coin to the target.
            If the target ever reaches exactly 0, there is a solution, but if not there isn't.
            If the target goes below 0, then it stops checking, prunes that combination and backtracks to try a new one.
            
            Params
            - target: amount that must be reached
            - coins: dictionary of coin values and count pairs
            - used: dictionary of used coin values and count pairs
            
            Return
            Tuple[
                bool: True if you can make a combination of coins to reach target or False if you can't,
                Optional[Dict[int,int]]: value, count pairs of each coin used and what quantity
            ]

            Example
            This is just for demonstration, but it's not a valid runnable test
            >>> coins = {1: 5, 4: 2}
            >>> target = 6
            knapsack_backtracking(target, coins)
            (True, {1: 2, 4: 1})
            - This means 2 coins of value 1 and 1 coin of value 4 = 6
            and note using 6 1's is not possible since only 5 1's exist

            >>> coins = {1: 5, 4: 2}
            >>> target = 11
            knapsack_backtracking(target, coins)
            (False, {})
            - Since it's not solvable we return False and an empty dictionary
        """
        if not used:
            used = defaultdict(int)

        if target == 0:
            return True, dict(used)
        
        # If combination of coins is no longer valid, prune this combination and backtrack
        if target < 0:
            return False, {}

        # Try each coin
        for coin, max_count in coins.items():

            # Skip used up coins
            if used[coin] >= max_count:
                continue

            # Choose the coin
            used[coin] += 1

            # Do the backtracking using recursion
            feasible, solution = self.knapsack_backtracking(target - coin, coins, used)

            if feasible:
                return True, solution

            # Backtrack 
            used[coin] -= 1

        # No solution
        return False, {}


    def knapsack_bruteforce(self, target: int, coins: Dict[int,int], used: Dict[int,int] = None) -> Tuple[bool, Optional[Dict[int,int]]]:
        """
            Generates a brute force solution by trying all valid combinations
            
            This recursive function tries using one of each coin recursively to try all combinations.
            In each recursive call, it subtracts the used coin to the target.
            If the target ever reaches exactly 0, there is a solution, but if not there isn't.
            
            Params
            - target: amount that must be reached
            - coins: dictionary of coin values and count pairs
            - used: dictionary of used coin values and count pairs
            
            Return
            Tuple[
                bool: True if you can make a combination of coins to reach target or False if you can't,
                Optional[Dict[int,int]]: value, count pairs of each coin used and what quantity
            ]

            Example
            This is just for demonstration, but it's not a valid runnable test
            >>> coins = {1: 5, 4: 2}
            >>> target = 6
            knapsack_bruteforce(target, coins)
            (True, {1: 2, 4: 1})
            - This means 2 coins of value 1 and 1 coin of value 4 = 6
            and note using 6 1's is not possible since only 5 1's exist

            >>> coins = {1: 5, 4: 2}
            >>> target = 11
            knapsack_backtracking(target, coins)
            (False, {})
            - Since it's not solvable we return False and an empty dictionary
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

    def knapsack_simple(self, target: int, coins: Dict[int, int], used: Dict[int,int] = None) -> Tuple[bool, Optional[List[int]]]:
        return False, "Not implemented"

    def knapsack_bestcase(self, target: int, coins: Dict[int, int], used: Dict[int,int] = None, best: Dict[int,int] = None) -> Tuple[bool, Optional[List[int]]]:
        """
            Generates a best case solution by trying all valid combinations
            
            This recursive function tries using one of each coin recursively to try all combinations.
            In each recursive call, it subtracts the used coin to the target.
            If the target ever reaches exactly 0, there is a solution, but if not there isn't.
            If the target goes below 0, then it stops checking, prunes that combination and backtracks to try a new one.
            At each iteration, it keeps track of the current used coins, and if the sum of the current used coins
            is better than the best case combination of coins, it updates the best case combination of coins to the
            combination of the current used coins.
            This way, if we reach the target we return the combination of coins that reaches that exact target, but
            if the target is impossible to reach, we return the combination of coins that gets closest to the
            target without going past it.
            
            Params
            - target: amount that must be reached
            - coins: dictionary of coin values and count pairs
            - used: dictionary of used coin values and count pairs
            - best: dictionary of best case of used coin values and coint pairs
            
            Return
            Tuple[
                bool: True if you can make a combination of coins to reach target or False if you can't,
                Optional[Dict[int,int]]: value, count pairs of each coin used and what quantity
            ]

            Example
            This is just for demonstration, but it's not a valid runnable test
            >>> coins = {1: 5, 4: 2}
            >>> target = 6
            knapsack_bestcase(target, coins)
            (True, {1: 2, 4: 1})
            - This means 2 coins of value 1 and 1 coin of value 4 = 6
            and note using 6 1's is not possible since only 5 1's exist

            >>> coins = {3: 2, 11: 5}
            >>> target = 32
            knapsack_bestcase(target, coins)
            (False, {3: 2, 11: 2})
            - This means 2 coins of value 3 and 2 coins of value 11 = 28
            which is the closest we can get to 32 without going past it
            given our combination of coins. We stil return false in our 
            tuple because it's not solvable.
        """

        if not used:
            used = defaultdict(int)
        if best is None:
            best = {}

        curr_sum = sum(coin*cnt for coin, cnt in used.items())
        best_sum = sum(coin*cnt for coin, cnt in best.items()) if best else 0

        # Updating best sum if necessary
        if curr_sum > best_sum:
            best.clear()
            for coin, cnt in used.items():
                if cnt > 0:
                    best[coin] = cnt
        
        if target == 0:
            return True, dict(used)
        
        for coin, max_cnt in coins.items():
            # Move on if coins are used up
            if used[coin] >= max_cnt:
                continue
            #Pruning
            if target - coin < 0:
                continue

            # Choosing coin then recursing with the updated target
            used[coin] += 1
            feasible, solution = self.knapsack_bestcase(target - coin, coins, used, best)
            # Bringing count back
            used[coin] -= 1

            if feasible:
                return True, dict(solution)

        # If an exact sum is impossible, return the combination that got the closest
        return False, dict(best)

