

from typing import Any

from src.experts.expert_1.thinking_flow import CTF_thinking_flow, CTF_thinking_flow_correction
from src.experts.expert_1.thinking_flow_utils.special_agents.Evaluator import Evaluator


class SolvingMachine:
    
    def __init__(self, max_evaluate_times: int=30, llm: str="gpt-4-turbo"):
        
        self.max_evaluate_times = max_evaluate_times
        self.llm = llm
        self.evaluator = Evaluator(self.llm)
        self.ctf = CTF_thinking_flow
        self.ctf_correct = CTF_thinking_flow_correction
        
    def __call__(self, question: str, hint:str = "") -> tuple[list[dict], list[Any], list[Any], list[Any]]:

        history_info = []
        processes = []
        answers = []
        evaluates_result = []
        
        solving_time = 0 
        solving_info_each_time = {}
        
        # Step 1: Do the CTF
        solving_info = self.ctf(question, llm=self.llm, hint=hint)

        history_info.append(solving_info)
        processes.append(solving_info["solving_process"])
        answers.append(solving_info["final_answer"])
        
        # Step 2: Evaluate the answer
        evaluate_results = {}
        wrong_time = 0
        for method in ["contradiction", "algebra", "flow"]:
            evaluate_info, if_right = self.evaluator(question, solving_info["final_answer"], method=method)
            evaluate_results[method] = {"result": evaluate_info, "if_right": if_right}

            evaluates_result.append(evaluate_info)
            
            if not if_right:
                wrong_time += 1
                
        ans_local = solving_info['final_answer']
        solving_info_each_time[ans_local] = wrong_time
        
        # Step 3: If the answer is right, return the result
        if wrong_time == 0:
            return {"history_info": history_info, "processes":processes, "answer": answers, "evaluates_result": evaluates_result}

        # Step 4: If the answer is wrong, do the correction and re-evaluate, until the answer is right( we also have
        # a max_evaluate_times)
        else:
            while solving_time < self.max_evaluate_times: 

                evaluate_info = ""
                for evaluate_result in evaluate_results.values():
                    if not evaluate_result["if_right"]:
                        evaluate_info  += evaluate_result["result"]
                old_plan = solving_info["plan"]
                old_process = solving_info["solving_process"]
                
                solving_info = self.ctf_correct(question, old_plan, old_process, evaluate_info, llm=self.llm, hint=hint)

                history_info.append(solving_info)
                processes.append(solving_info["solving_process"])
                answers.append(solving_info["final_answer"])

                for method in ["contradiction", "algebra", "flow"]:
                    evaluate_info, if_right = self.evaluator(question, solving_info["final_answer"], method=method)
                    evaluate_results[method] = {"result": evaluate_info, "if_right": if_right}
                    evaluates_result.append(evaluate_info)
                    
                    if not if_right:
                        wrong_time += 1
                        
                if wrong_time == 0:
                    return {"history_info": history_info, "processes":processes, "answer": answers, "evaluates_result": evaluates_result}
                else:
                    solving_time += 1
                    ans_local = solving_info['final_answer']
                    solving_info_each_time[ans_local] = wrong_time
                    continue
        
        # Step 5: If the answer is still wrong, return the answer which has the least wrong times.
        solving_info_each_time = self.sort_dict_by_value(solving_info_each_time)
        ans_local = list(solving_info_each_time.keys())[-1]
        return {"history_info": history_info, "processes":processes, "answer": answers, "evaluates_result": evaluates_result}

    @staticmethod
    def sort_dict_by_value(d) -> dict:
        return dict(sorted(d.items(), key=lambda item: item[1], reverse=True))
                
