

from src.experts.expert_3.cot_math import solving_math_cot

def expert_3(question, hint:str = ""):

    ans = solving_math_cot(question=question, hint=hint)

    return ans