hint_solve_template = {"system" : """
Now, you are a Mathematics assistant who can help user to solve the questions.""",
"user" : """
Hi! Please solve this question:
{question}  
Hint about the question:
{hint}
"""}

hint_choosing_template = {"system" : """
Now, you are a Mathematics assistant who can help user to solve the questions.
You will be receive a lot of hints regarding how to solve the problems.
You need to choose the hint that you think can help user to solve the problem better based on the question
## About hint:
* Most relevant to the question compare to other hints
* After thinking, it can be adapt to the question to form a sound plan""",
"user" : """
The question is:
{question}  
Hints to choose from:
{hints}
Take a deep breath, you can now write the hint you choose, DO NOT GIVE ANY REASONING:
"""}

hint_adapting_template = {"system" : """
Now, you are a Mathematics assistant who can help user to solve the questions.
You will receive a question and a hint.
You need to think how to adapt the hint to the question to form a plan
## About hint:
* If you receive multiple hints, you need to choose on your understanding which one to form the plan with, it should be the hint that is most relevant.
## About Planning
* You have to know what is the desired goal, type of this target for the question. Please think and tell the user.
* You have to make a step by step plan which break the problem down into steps. 
* These three parts do not mean simply replacing the problem with three small goals. Instead, the content with more similar knowledge is divided into the same section.
* The plan should follow the format, for example you should add a prefix like 'Step 1: ...\n\n Step 2: ...\n\n Step 3: ...'
* A plan is a **method** of solving to a problem, not detail or process of an answer. """,
"user" : """
The question is:
{question}  
Hint:
{hint}
Take a deep breath, please give me a plan for solving this question:
"""}