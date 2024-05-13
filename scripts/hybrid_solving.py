
from dotenv import load_dotenv

from scripts.solving_methods import solving_method_1, solving_method_2, solving_method_3, solving_method_4


load_dotenv()

def set_args():
    """
    Set arguments for the script
    """
    parser = argparse.ArgumentParser(description="Auto solving problems")
    parser.add_argument("-p", "--problem", type=str, default="1+1?", help="Path to problems file")
    parser.add_argument("-m", "--method", type=str, default="1", choice=["1", "2", "3", "4"]
                        ,help="Path to result file")
    parser.add_argument("-s", "--save_path", type=str, default="temp_result.json", help="Path to result file")
    args = parser.parse_args()
    return args


if __name__ == "__main__":

    args = set_args()

    problem = args.problem

    if args.method == "1":
        result = solving_methods = solving_method_1(problem)
    if args.method == "2":
        result = solving_methods = solving_method_2(problem)
    if args.method == "3":
        result = solving_methods = solving_method_3(problem)
    if args.method == "4":
        result = solving_methods = solving_method_4(problem)

    save_json({"problem": problem, "result": result}, args.save_path)
