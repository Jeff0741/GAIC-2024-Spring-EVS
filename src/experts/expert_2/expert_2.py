from src.experts.expert_2.agents.code_interpreter import MathCodeInterpreter, VerifyAndVote
from src.experts.expert_2.agents.code_generator import MathCodeGenerator, MathVerifierCodeGenerator

class MathExpert2:
    def __init__(self) -> None:

        self.math_code_generator = MathCodeGenerator(llm="gpt-4-turbo")
        self.math_code_interpreter = MathCodeInterpreter()
        self.math_verifier_code_generator = MathVerifierCodeGenerator(llm="gpt-4-turbo")
        self.verify_and_vote = VerifyAndVote()
    
    def run(self, problem: str, solution_number: int) -> str:
        # Step 1. Generate multiple solutions to the problem
        answers = []
        all_solution_codes = []
        for i in range(solution_number):
            solution_code = self.math_code_generator(problem=problem)
            all_solution_codes.append(solution_code)
            # print (f"Generate {i+1} solution code")
            # # save code for debug
            # with open(f"./solu_{i}.py", "w") as f:
            #     f.write(solution_code)

            try:
                answer = self.math_code_interpreter(code=solution_code)
                answers.append(answer)
                # print (f"Solution {i+1} Code execution success, answer: {answer}")
            except Exception as e:
                # print (f"Solution {i+1} Code execution failed {e}")
                answers.append(f"Code execution failed: {e}")
                pass

        if len(answers) == 0:
            return "We try to generate a Python code to solve the problem, but we failed to generate a valid code."
        # Step 2. Generate a verification code for the answer
        # We only need to generate one verification code for the first answer, 
        # because the verification code is the same for all answers.
        verification_code = self.math_verifier_code_generator(problem=problem, answer=answers[0])
        # print (f"Generate verification code")

        # save code for debug
        # with open("./tmp.py", "w") as f:
        #     f.write(verification_code)

        # Step 3. Verify the answer
        vote_answer = self.verify_and_vote(answers=answers, code=verification_code)
        valid_code = ""
        for i, (_answer, _code) in enumerate(zip(answers, all_solution_codes)):
            if str(_answer) == str(vote_answer):
                valid_code = _code
                break
            # print (f"Solu: {i}\nAnswer: {_answer}\nCode: {_code}\n")
        
        ret = """We generated Python code to solve the problem. Here is the Python code:
```python
{CODE}
```
Here is the answer we get from the execution of the code:
{ANS}
"""
    
        return ret.format(
            CODE=valid_code,
            ANS=vote_answer
        )

def expert_2(question):
    agent = MathExpert2()
    ans = agent.run(problem=question, solution_number=5)
    return ans

