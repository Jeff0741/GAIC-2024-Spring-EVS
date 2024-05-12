

from src.experts.expert_1.thinking_flow_utils.BasicAgent import BasicAgent


SIMPLIFY_ANSWER = { "system" : """ 
You're a math teacher, and your job is to extract useful information from data.

Your task is to extract the final answer which should be a number or a Polynomial or a matrix or other formath which can explain this answer very clear in math.

Requirements:
- Please extract only one answer for me, please only answer me what the this answer is for this problem. Don't say anything else.
- Please do not use the LaTex format.
- You must write succinctly.
- If you encounter a decimal, keep four decimal places!!!
- If you encounter an irrational number, take an approximate value, such as pi=3.1416

You are not allowed to make mistake, please make sure you are right.
""", "user" : """ 
Here is your information for this time:
{info}
"""}


def simplify_answer(question, answer):

    simplify_agent = BasicAgent(template=SIMPLIFY_ANSWER)

    info = f"The question is: {question}.\n The answer is: {answer}"

    simplify_result = simplify_agent.run(info=info)

    return simplify_result
