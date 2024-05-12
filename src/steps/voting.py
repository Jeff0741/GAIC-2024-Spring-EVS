

from src.experts.expert_1.thinking_flow_utils.BasicAgent import BasicAgent
import re

def extract_content(text):
    pattern = r'\|\|\|(.*?)\|\|\|'
    matches = re.findall(pattern, text)
    return matches

voting_prompt_1 = {
    "system": """ 
Now you are a math teacher. Your job is to find the correct answer from the answers of three students.

Tasks:
1. You will see three students' answers to this question.
2. You need to think carefully and choose the right answer.
3. Your final result must be expressed in a specified format, e.g. |||S1|||.
Here, S1 is student 1's answer.

Requirements
1. Explain your thought process.
2. You can verify your answer in a variety of ways.
3. If there are multiple correct answers, choose the one you think is the best.

You have to choose an answer. If you think both are wrong, choose the answer that you think is closest to the correct 
answer.
""", "user": """ 
Question:
{question} 

Student 1: {answer_1}
Student 2: {answer_2}
Student 3: {answer_3}

Please tell me which one you will choose.
"""
}

voting_prompt_2 = {
    "system": """
You are a mathematical teacher known for logical thinking and problem-solving.

Tasks:
1. Review the three students' answers to the given question.
2. Use your analytical skills to identify the most accurate answer.
3. Your final decision should follow the format: |||S2|||, where S2 is student 2's answer.

Requirements:
1. Describe your reasoning for choosing this answer.
2. Consider evidence and rationale presented in each student's solution.
3. If no student provides a fully accurate answer, select the one closest to correct and justify your choice.
""",
    "user": """
Question:
{question} 

Student 1: {answer_1}
Student 2: {answer_2}
Student 3: {answer_3}

Please select the most accurate answer and explain your rationale.
"""
}


voting_prompt_3 = {
    "system": """
Now you're a debate mathematical coach guiding your students to logical conclusions.

Tasks:
1. Examine the responses from three students.
2. Compare their answers objectively, weighing their logic and reasoning.
3. Your decision should be formatted as: |||S3|||, representing the student whose response you chose.

Requirements:
1. Justify your choice by pointing out the strengths and weaknesses of each student's answer.
2. Emphasize logical soundness and completeness in your analysis.
3. If no answer is entirely correct, identify the closest and justify why it's the best option.
""",
    "user": """
Question:
{question} 

Student 1: {answer_1}
Student 2: {answer_2}
Student 3: {answer_3}
"""}

voting_prompt_4 = {
    "system": """
Now you're a debate coach guiding your students to logical conclusions.

Tasks:
1. Examine the responses from three students.
2. Compare their answers objectively, weighing their logic and reasoning.
3. Your decision should be formatted as: |||S3|||, representing the student whose response you chose.

Requirements:
1. Justify your choice by pointing out the strengths and weaknesses of each student's answer.
2. Emphasize logical soundness and completeness in your analysis.
3. If no answer is entirely correct, identify the closest and justify why it's the best option.
""",
    "user": """
Question:
{question} 

Student 1: {answer_1}
Student 2: {answer_2}
Student 3: {answer_3}

Share which answer you believe is best and provide your reasoning.
"""
}


voting_prompt_5 = {
    "system": """
You're a professional examiner trained in evaluating diverse student answers.

Tasks:
1. Assess the responses of three students to the given question.
2. Select the answer that best meets the requirements of the question.
3. Express your final choice in this format: |||S2|||.

Requirements:
1. Provide a detailed explanation for your selection.
2. Take note of the clarity, completeness, and logical structure of each student's response.
3. If none of the responses are fully correct, choose the nearest correct answer and explain why.
""",
    "user": """
Question:
{question} 

Student 1: {answer_1}
Student 2: {answer_2}
Student 3: {answer_3}

Make your selection and explain your reasoning.
"""
}


def voting(question, answers):

    print("The experts is voting the answers")

    voter_1 = BasicAgent(template=voting_prompt_1)
    voter_2 = BasicAgent(template=voting_prompt_2)
    voter_3 = BasicAgent(template=voting_prompt_3)
    voter_4 = BasicAgent(template=voting_prompt_4)
    voter_5 = BasicAgent(template=voting_prompt_5)

    voting_result = [0,0,0]

    feedback_1 = voter_1.run(question=question, answer_1=answers[0], answer_2=answers[1], answer_3=answers[2])
    feedback_2 = voter_2.run(question=question, answer_1=answers[0], answer_2=answers[1], answer_3=answers[2])
    feedback_3 = voter_3.run(question=question, answer_1=answers[0], answer_2=answers[1], answer_3=answers[2])
    feedback_4 = voter_4.run(question=question, answer_1=answers[0], answer_2=answers[1], answer_3=answers[2])
    feedback_5 = voter_5.run(question=question, answer_1=answers[0], answer_2=answers[1], answer_3=answers[2])

    choices = [extract_content(feedback_1),
               extract_content(feedback_2),
               extract_content(feedback_3),
               extract_content(feedback_4),
               extract_content(feedback_5)]

    for choice in choices:
        if "1" in choice:
            voting_result[0] += 1
        elif "2" in choice:
            voting_result[1] += 1
        elif "3" in choice:
            voting_result[2] += 1

    max_index = voting_result.index(max(voting_result))

    # print(f"The voting result is: the expert_{max_index+1} is the most confident.")

    return answers[max_index]

