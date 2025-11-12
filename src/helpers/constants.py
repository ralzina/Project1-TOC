import os
import json

BASE_PATH = os.path.abspath(os.getcwd())
CONFIG_FOLDER_PATH = os.path.join(BASE_PATH, "configuration")
CONFIGURATION_FILE_PATH = os.path.join(CONFIG_FOLDER_PATH, "student_config.json")
RESULTS_FOLDER = os.path.join(BASE_PATH, "results")
INPUT_FOLDER = os.path.join(BASE_PATH, 'input')
TEST_FOLDER = os.path.join(BASE_PATH, 'tests')
input_file = "data_knapsack_binpacking_file_garcias.cnf"
test_file = "check_knapsack_binpacking_tests.cnf"
test_bestcase_file = "check_bestcase_knapsack_binpacking_tests.cnf"
INPUT_FILE = os.path.join(INPUT_FOLDER, input_file)
TEST_FILE = os.path.join(TEST_FOLDER, test_file)
TEST_BESTCASE_FILE = os.path.join(TEST_FOLDER, test_bestcase_file)

def parse_config(config_path):
    if not os.path.exists(config_path):
        raise Exception("Please make sure the configuration file exists!!!")
    with open(config_path, mode = 'r' , encoding= 'utf-8') as conf_buffer:
        data = json.load(conf_buffer)
    data = data["Project Configuration"]
    selection = data["Selection"]
    sub_problem = data["Sub Problem"]
    return selection, sub_problem

