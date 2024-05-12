

from src.experts.expert_1.thinking_flow_utils.BasicAgent import BasicAgent


cot_prompt = { "system" : """Now, you are a Mathematics assistant who can help user to solve the questions.
And here is some hint may help you:
{hint}
""",
"user" : """
Hi! Please solve this question:
{question}  
"""}


def solving_math_cot(question, hint: str = ""):
    solving_cot_agent = BasicAgent(template=cot_prompt)

    final_result = solving_cot_agent.run(question=question, hint=hint)

    return final_result
