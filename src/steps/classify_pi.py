

from src.experts.expert_1.thinking_flow_utils.BasicAgent import BasicAgent


classify = {
    "system": """
You are an expert evaluator in the field of probability and statistics. Your task is to analyze the given question 
    thoroughly and provide step-by-step reasoning to determine whether it belongs to the category of probability and 
    statistics. 

## Requirements:
- If the question relates to probability and statistics, respond with |||TRUE|||. Otherwise, respond with |||FALSE|||. 
- Your analysis must follow logical steps to ensure accuracy.
""",
    "user": """
Please analyze the following question to determine if it is related to probability and statistics. Provide step-by-step 
    reasoning and explain your thought process in determining your answer. If the question is related to probability 
    and statistics, respond with |||TRUE|||; otherwise, respond with |||FALSE|||:
    
{question}
"""
}


def classify_question(question):

    classify_agent = BasicAgent(template=classify)

    classify_result = classify_agent.run(question=question)

    if "TRUE" in classify_result:
        return True
    else:
        return False
