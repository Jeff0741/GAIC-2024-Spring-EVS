

from src.experts.expert_1.expert_1 import expert_1
from src.experts.expert_2.expert_2 import expert_2
from src.experts.expert_3.expert_3 import expert_3
from src.experts.expert_4.expert_4 import expert_4
from src.steps.voting import voting
from src.steps.simplify import simplify_answer

from data.statistic_table import z_distribution, chi_distribution, t_distribution


def solving_method_1(question: str) -> str:
    return expert_4(question)

def solving_method_2(question: str) -> str:

    answer_1 = expert_1(question=question)
    answer_2 = expert_2(question=question)
    answer_3 = expert_3(question=question)

    results = [answer_1['answer'], answer_2, answer_3]

    voting_result = voting(question, results)

    final_answer = simplify_answer(question=question, answer=voting_result)

    return final_answer

def solving_method_3(question: str) -> str:

    hint = (f"STANDARD NORMAL DISTRIBUTION: Table: {z_distribution}"
            f"\n\n\nChi-Square Distribution Table {chi_distribution}"
            f"\n\n\nT-Distribution Table: {t_distribution}")
    answer_1 = expert_1(question=question, hint=hint)
    answer_2 = expert_2(question=question)
    answer_3 = expert_3(question=question, hint=hint)

    results = [answer_1['answer'], answer_2, answer_3]

    voting_result = voting(question, results)

    final_answer = simplify_answer(question=question, answer=voting_result)

    return final_answer


