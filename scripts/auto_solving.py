

from copy impory deepcopy
import time
import os

from dotenv import load_dotenv

from src.file_io_utils import read_json, save_json
from src.steps.classify_pi import classify_question
from scripts.solving_methods import solving_method_1, solving_method_2, solving_method_3, solving_methods_4


load_dotenv()

if __name__ == "__main__":
    
    problems = read_json("./data/problems.json")

    result = {}
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    os.makedirs(f"./result/{date}", exist_ok=True)
    result_save_path = f"./result/{date}/input.json"
    
    for i, (order, info) in enumerate(problems.items()):
        
        question = info["content"]
        
        if i < 100:
            result = solving_method_1(question)
        else:
            if classify_question(question):
                result = solving_method_3(question)
            else:
                result = solving_method_2(question)
                
        save_json(result, result_save_path)
    