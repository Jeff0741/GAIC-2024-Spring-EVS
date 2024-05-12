
from src.experts.expert_1.SolvingMachine import SolvingMachine


def expert_1(question: str, hint: str="") -> dict:
    sm = SolvingMachine()
    result = sm(question=question, hint=hint)
    return result
