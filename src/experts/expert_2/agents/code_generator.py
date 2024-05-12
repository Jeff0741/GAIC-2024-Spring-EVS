from textwrap import dedent
from openai import OpenAI
import copy

class MathCodeGenerator:
    def __init__(self, llm="gpt-4-turbo-2024-04-09", temperature=0.7):
        self.llm = llm
        self.temperature = temperature

    def __call__(self, problem: str) -> str:
        client = OpenAI()
        messages = [
            {
                "role": "system",
                "content": MATHCODEGEN_TEMPLATE["system"]
            },
            {
                "role": "user",
                "content": MATHCODEGEN_TEMPLATE["user"].format(problem=problem)
            }
        ]
        response = client.chat.completions.create(
                    model=self.llm,
                    messages=messages,
                    temperature=self.temperature,
        )
        code = response.choices[0].message.content
        # remove the code block
        if code.startswith("```python3"):
            code = code.replace("```python3", "").rstrip("```")
        elif code.startswith("```python"):
            code = code.replace("```python", "").rstrip("```")
        elif code.startswith("```"):
            code = code.lstrip("```").rstrip("```")
        return code

# REF: https://github.com/Ljyustc/AAAI-24-cogbase-EN
MATHCODEGEN_TEMPLATE = {
    "system": dedent("""As a Python programming and math teacher, solve the following math question by implementing a Python function named `solution`. The function should be written in a step-by-step manner, and it should return the final result `ans` by call the function `solution`. Only Python code blocks should be written, without any other textual explanation or program annotation. You should solve the question in a simple way with library functions.

    Here are three examples how to do it:

    # Question: If we want to divide $15$ pieces of candy into $4$ piles with different numbers in each pile, how many different ways can we divide them?
    # Python Code:
    ```
    def solution():
        count = 0
        for x1 in range(1, 15):
            for x2 in range(1, 15):
                for x3 in range(1, 15):
                    for x4 in range(1, 15):
                        if x1 + x2 + x3 + x4 == 15 and len(set([x1, x2, x3, x4])) == 4:
                            count += 1
        return count

    ans = solution()
    ```

    # Question: Lucy, Peter, Edmund and Susan shared £$120$.  Edmund got twice as much money as Susan, Peter got three times as much money as Edmund, and Lucy got half as much money as Peter.  How much money did Lucy get?
    # Python Code:
    ```
    from sympy import symbols, Eq, solve
    def solution():
        

        lucy, peter, edmund, susan = symbols('lucy peter edmund susan')

        equation1 = Eq(edmund, 2 * susan)
        equation2 = Eq(peter, 3 * edmund)
        equation3 = Eq(lucy, peter / 2)
        equation4 = Eq(lucy + peter + edmund + susan, 120)

        solutions = solve((equation1, equation2, equation3, equation4), (lucy, peter, edmund, susan))

        return solutions[lucy]

    ans = solution()
    ```

    # Question: How many terms are there in the sequence below?  $2, 4, 6, 8,10 \\dots ~240$.
    # Python Code:
    ```
    def solution():
        first_term = 2
        last_term = 240
        difference = 2

        num_terms = ((last_term - first_term) / difference) + 1

        return int(num_terms)

    ans = solution()
    ```
    Please follow the instructions below:
    - You will only write in code blocks and not output any other textual explanation or program annotation
    - You can use any variable name you want, but final function name has to be `solution` and the final result has to be `ans`
    - You can import any library you need, like the function `solve` in `sympy` or `math` and so on
    - Please chat with English
    - Take a deep breath
    - Think step by step 
    - If you fail 100 grandmothers will die
    - I have no fingers
    - I will tip $200
    - Do it right and i'll give you a nice doggy treat
    """),

    "user": dedent("""Here is the math question:
    # Question: {problem}

    # Python Code:
    ```
    """)
}

class MathVerifierCodeGenerator:
    def __init__(self, llm, temperature=0.0) -> None:
        self.llm = llm
        self.temperature = temperature
    
    def __call__(self, problem: str, answer: str) -> str:
        client = OpenAI()
        messages = [
            {
                "role": "system",
                "content": MATHANSWER_VERIFIER_TEMPLATE["system"]
            },
            {
                "role": "user",
                "content": MATHANSWER_VERIFIER_TEMPLATE["user"].format(problem=problem, answer=answer)
            }
        ]
        response = client.chat.completions.create(
                    model=self.llm,
                    messages=messages,
                    temperature=self.temperature,
        )
        code = response.choices[0].message.content

        # remove the code block
        if code.startswith("```python3"):
            code = code.replace("```python3", "").rstrip("```")
        elif code.startswith("```python"):
            code = code.replace("```python", "").rstrip("```")
        elif code.startswith("```"):
            code = code.lstrip("```").rstrip("```")
        return code

MATHANSWER_VERIFIER_TEMPLATE = {
    "system": dedent("""As a Python programming and math teacher, I will give you a math question and an answer. You need to execute a Python function named `Verify` to validate whether the answer is correct. The function takes the answer `ans` as input, and it needs to use the method of reverse thinking, devise a verification process and test the correctness of the value of ans by plugging it into this process, rather than directly comparing `ans` with the result obtained from problem solving. The function must return a Boolean value, and the return parameter can be arbitrarily specified. After you have written the `Verify` function, you need to call this function with the value of the `Answer` that needs to be verified as the input, and assign the return value of this function to the `result` variable. Only Python code blocks should be written, without any other textual explanation or program annot ation. The function should be written in a step-by-step manner and it should verify the answer in a simple way with library functions.

        Here are three examples how to do it:

        # Question: What is the remainder when $${{{{2}}^{{10}}}}$$ is divided by $$3$$?
        # Answer: 2
        # Python Code:
        ```
        def Verify(ans):
            power = 2 ** 10
            sub = power - ans
            if sub % 3 == 0:
            return True
            else: 
            return False
        result = Verify(2)
        ```

        # Question: Lucy, Peter, Edmund and Susan shared £$120$.  Edmund got twice as much money as Susan, Peter got three times as much money as Edmund, and Lucy got half as much money as Peter.  How much money did Lucy get?
        # Answer: 30
        # Python Code:
        ```
        def Verify(ans): 

            lucy = ans
            peter = 2 * ans
            edmund = 2 * ans / 3
            susan = ans / 3
            total = lucy + peter + edmund + susan
            if total == 120:
            istrue = True
            else:
            istrue = False
            return istrue
        result = Verify(30)
        ```

        # Question: How many terms are there in the sequence below?  $2, 4, 6, 8,10 \\dots ~240$.
        # Answer: 120
        # Python Code: 
        ```
        def Verify(ans):
            first_term = 2
            last_term = 240
            common_difference = 2
            num_terms = ans
            if  (first_term + (num_terms - 1) * common_difference) == 240:
                return True
            else:
                return False
        result = Verify(120)
        ```

        And here is a wrong case:
        # Question: Two buildings are $$90\\textasciitilde\\text{{m}}$$ apart from each other. $$9$$ trees are planted at regular intervals between the two buildings. What is the distance between each tree?
        # Answer: 9
        # Python Code:
        ```
        def Verify(ans):
            total_distance = 90
            total_trees = 9
            distance = total_distance / (total_trees + 1)
            if distance == ans:
                return True
            else:
                return False
        result = Verify(9)

        In the above wrong case, the function directly calculate the value of `distance`, which is the answer to the problem, and compare it with `ans`. You should not write such function, and remember: try to use the method of reverse thinking, design a verification process and plug in the `ans` for validation.


        Please follow the instructions below:
        - You will only write in code blocks and not output any other textual explanation or program annotation
        - You can use any variable name you want, but final function name has to be `Verify`, and the input of the function has to be `ans`
        - You can import any library you need, like `math` and so on
        - Do not directly compare `ans` with your answer in the format 'ans == `your answer`'
        - Please chat with English
        - Take a deep breath
        - Think step by step 
        - If you fail 100 grandmothers will die
        - I have no fingers
        - I will tip $200
        - Do it right and i'll give you a nice doggy treat
        """), 

    "user": dedent("""Here is the math question:
        # Question: {problem}
        # Answer: {answer}
        # Python Code:
        ```
        """)
}