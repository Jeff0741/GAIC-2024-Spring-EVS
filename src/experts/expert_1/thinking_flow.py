
from src.experts.expert_1.thinking_flow_utils.special_agents.MathCoding import MathCoding
from src.experts.expert_1.thinking_flow_utils.BasicAgent import BasicAgent
from src.experts.expert_1.thinking_flow_utils.prompts import (
    plan_ctf, solving_ctf, fix_ctf, plan_correction, solving_correction, fix_correction
)      


# ================================== CTF: Solving a question by CTF

def CTF_thinking_flow(question:str, hint:str = "",  llm="gpt-4-turbo") -> dict:

    # step 1: Create Agents
    plan_agent = BasicAgent(template=plan_ctf, llm=llm)
    solving_agent = BasicAgent(template=solving_ctf, llm=llm)
    calculus_agent = MathCoding(type=1)
    fix_agent = BasicAgent(template=fix_ctf, llm=llm)
        
    wrong = ""

    do_it = 0
    while do_it < 2:
        # Step 3: Generate a plan
        plan = plan_agent.run(wrong=wrong, question=question,  hint=hint)
        hint = "\nAnd we make a plan which you should follow:\n" + plan + "\n" +  hint
            
        # Step 4: Solving this problem by following the plan
        process = solving_agent.run(hint=hint, question=question)
        # print(f"======{do_it}\n{process}")
        # Step 5: Using coding method to re-do the solving process
        coding_answer = calculus_agent(question=question, answer=process)

        
        if coding_answer == "":
            wrong += f"\nThis plan is wrong, which can not solve this problem, please change another method:{plan}"
            do_it += 1
        else:
            do_it = 2

    # Step 6: Combain the llm-result and the coding-result
    final_answer = fix_agent.run(hint=hint, question=question, original=process, computed=coding_answer)
            
    return {"final_answer": final_answer, "solving_process":process, "coding_answer":coding_answer,  "plan":plan}

def CTF_thinking_flow_correction(question:str, old_plan:str, old_process:str, evaluate:str, hint:str = "",
                                 llm="gpt-4-turbo") -> dict:
    
    # step 1: Create Agents
    plan_agent = BasicAgent(template=plan_correction, llm=llm)
    solving_agent = BasicAgent(template=solving_correction, llm=llm)
    calculus_agent = MathCoding(type=1)
    fix_agent = BasicAgent(template=fix_correction, llm=llm)
        
    wrong = ""

    do_it = 0
    while do_it < 2:
        # Step 3: Generate a plan
        plan = plan_agent.run(old_plan=old_plan, old_process=old_process, evaluate=evaluate, question=question, hint=hint)
        hint = "\nAnd we make a plan which you should follow:\n" + plan + "\n" +  hint
            
        # Step 4: Solving this problem by following the plan
        process = solving_agent.run(hint=hint, old_plan=old_plan, old_process=old_process, evaluate=evaluate, question=question)

        # Step 5: Using coding method to re-do the solving process
        coding_answer = calculus_agent(question=question, answer=process)
        
        if coding_answer == "":
            wrong += f"\nThis plan is wrong, which can not solve this problem, please change another method:{plan}"
            do_it += 1
        else:
            do_it = 2

    # Step 6: Combain the llm-result and the coding-result
    final_answer = fix_agent.run(hint=hint,  old_plan=old_plan, old_process=old_process, evaluate=evaluate, 
                                              question=question, original=process, computed=coding_answer)
            
    return {"final_answer": final_answer, "solving_process":process, "coding_answer":coding_answer,"plan":plan}

