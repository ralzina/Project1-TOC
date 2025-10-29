from abc import ABC, abstractmethod
import os
from src.helpers.dmaics_parser import parse_multi_instance_knapsack
from src.helpers.constants import RESULTS_FOLDER, CONFIGURATION_FILE_PATH
from typing import List, Tuple, Dict, Any, Optional
import json
import csv
import time
from src.helpers.project_selection_enum import ProjectSelection, SubProblemSelection
import matplotlib.pyplot as plt


class KnapsackAbstractClass(ABC):

    def __init__(self, 
                    file_input_path: str,
                    result_file_name:str = "knapsack_results",
                    results_folder_path: str = RESULTS_FOLDER):
        self.file_input_path = file_input_path
        self.results_folder_path = results_folder_path
        self.result_file_name = result_file_name
        self.config_path = CONFIGURATION_FILE_PATH
        self.solution_instances = self.parse_input_file()
        print(f"Parsed {len(self.solution_instances)} instances from {self.file_input_path}")
        self.sub_problems = self.set_config()

    def set_config(self):
        if not os.path.exists(self.config_path):
            raise Exception("Please make sure the configuration file exists!!!")
        with open(self.config_path, mode = 'r' , encoding= 'utf-8') as conf_buffer:
            data = json.load(conf_buffer)
        data = data["Project Configuration"]
        selection = data["Selection"]
        sub_problem = data["Sub Problem"]
        sub_probs = []
        for sub_prob in sub_problem:
            if sub_prob["value"] == SubProblemSelection.brute_force.value:
                sub_probs.append(SubProblemSelection.brute_force)
            elif sub_prob["value"] == SubProblemSelection.btracking.value:
                sub_probs.append(SubProblemSelection.btracking)
            elif sub_prob["value"] == SubProblemSelection.simple.value:
                sub_probs.append(SubProblemSelection.simple)
            elif sub_prob["value"] == SubProblemSelection.best_case.value:
                sub_probs.append(SubProblemSelection.best_case)        
        return sub_probs
        
    def parse_input_file(self):
        return parse_multi_instance_knapsack(self.file_input_path)
    
    def save_results(self, run_results: List[Any], sub_problem):
        # Write to CSV
        dir_name, file_name = os.path.split(self.file_input_path)
        file_name_only, ext = os.path.splitext(file_name)
        temp_result = os.path.join(self.results_folder_path, f"{sub_problem}_{file_name_only}_{self.result_file_name}.csv")
        with open(temp_result, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["instance_id", "target", "n_coins",
                    "method", "feasible", "time_seconds", "coin_combination"])
            w.writerows(run_results)
        print(f"\nResults written to {temp_result}")

        # Plot
        plot_filename = os.path.splitext(temp_result)[0] + ".png"

        # Extract data
        x_green = []
        y_green = []
        x_red = []
        y_red = []

        for row in run_results:
            n_coins = int(row[2])
            time_sec = float(row[5])
            feasible = row[4]

            if feasible == "YES":
                x_green.append(n_coins)
                y_green.append(time_sec)
            else:
                x_red.append(n_coins)
                y_red.append(time_sec)

        # Create plot
        plt.figure(figsize=(8,5))
        plt.scatter(x_green, y_green, color='green', label='Feasible')
        plt.scatter(x_red, y_red, color='red', label='Not feasible')
        plt.xlabel("Number of Coins (Problem Size)")
        plt.ylabel("Time (seconds)")
        plt.title(f"Knapsack Runtime vs Problem Size ({sub_problem})")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        # Save plot to same folder as CSV
        plt.savefig(plot_filename)
        plt.close()
        print(f"Plot saved to {plot_filename}")

    def plot(self, plot_file_name):
        pass
    
    @abstractmethod
    def knapsack_backtracking(self, target: int, coins: List[int]) -> Tuple[bool, Optional[Dict[int, bool]]]:
        pass

    @abstractmethod
    def knapsack_bruteforce(self, target: int, coins: List[int]) -> Tuple[bool, Optional[Dict[int, bool]]]:
        pass

    @abstractmethod
    def knapsack_simple(self, target: int, coins: List[int]) -> Tuple[bool, Optional[Dict[int, bool]]]:
        pass

    @abstractmethod
    def knapsack_bestcase(self, target: int, coins: List[int]) -> Tuple[bool, Optional[Dict[int, bool]]]:
        pass

    def run(self):
        results = []
        
        for instance_id, target, coins in self.solution_instances:
            if SubProblemSelection.brute_force in self.sub_problems:
                t0 = time.perf_counter()
                bt_ok, bt_assign = self.knapsack_bruteforce(target, coins)
                bt_time = time.perf_counter() - t0
                results.append([instance_id, target, sum(coins.values()),
                        "BruteForce", "YES" if bt_ok else "NO",
                        f"{bt_time:.6f}", str(bt_assign)])

        if SubProblemSelection.brute_force in self.sub_problems:
            self.save_results(results, SubProblemSelection.brute_force.name)
            results = []

        for instance_id, target, coins in self.solution_instances:

            if SubProblemSelection.btracking in self.sub_problems:
                t0 = time.perf_counter()
                bt_ok, bt_assign = self.knapsack_backtracking(target, coins)
                bt_time = time.perf_counter() - t0
                results.append([instance_id, target, sum(coins.values()),
                        "BackTracking", "YES" if bt_ok else "NO",
                        f"{bt_time:.6f}", str(bt_assign)])
        
        if SubProblemSelection.btracking in self.sub_problems:
            self.save_results(results, SubProblemSelection.btracking.name)
            results = []

        for instance_id, target, coins in self.solution_instances:

            if SubProblemSelection.simple in self.sub_problems:
                t0 = time.perf_counter()
                bt_ok, bt_assign = self.knapsack_simple(target, coins)
                bt_time = time.perf_counter() - t0
                results.append([instance_id, target, sum(coins.values()),
                        "Simple", "YES" if bt_ok else "NO",
                        f"{bt_time:.6f}", str(bt_assign)])
        
        if SubProblemSelection.simple in self.sub_problems:
            self.save_results(results, SubProblemSelection.simple.name)
            results = []
        

        for instance_id, target, coins in self.solution_instances:

            if SubProblemSelection.best_case in self.sub_problems:
                t0 = time.perf_counter()
                bt_ok, bt_assign = self.knapsack_bestcase(target, coins)
                bt_time = time.perf_counter() - t0
                results.append([instance_id, target, sum(coins.values()),
                        "BestCase", "YES" if bt_ok else "NO",
                        f"{bt_time:.6f}", str(bt_assign)])
        
        if SubProblemSelection.best_case in self.sub_problems:
            self.save_results(results, SubProblemSelection.best_case.name)
            results = []