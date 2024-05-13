from textwrap import dedent
from openai import OpenAI
import copy
import re

class MathExpert5:
    def __init__(self, llm="gpt-4-turbo", temperature=0.0):
        self.llm = llm
        self.temperature = temperature
    
    def run(self, problem):
        SYS_PROMPT = """Now you are a Mathematics assistant who can help user to solve math problems.
You will be provided with a problem and some hints may be helpful for you to solve the problem.

When solving the problem, you should follow these requirements:
- For a problem, you should first analyze the question and determine which hints are helpful.
- It's possible that none of the hints are helpful for the question you need to solve, in which case you can directly analyze the question and generate a response.
- If the problem is a multiple-choice one, your answer should be one of the options provided.
- Every problem has already provided enough information to solve it, so you don't need to ask for more information.
- You must provide a latex formula as the final answer to the problem.

Use the following format to generate a response:
Thought: <Your thought to analyze the problem, choose the hints or solve the problem>
Final Answer: <Final answer of the problem>
"""
        USER_PROMPT = """
Here are some hints:
<hints>
1. **Ordinary Differential Equations (ODEs) with Power Series Solutions**:
   - Check if the power series solution leads to a recursive formula for the coefficients.
   - Analyze the recursive formula to determine if the series converges or diverges near a specific point (e.g., x=0).

2. **Trigonometric Identities and Equations**:
   - Use known trigonometric identities (e.g., sin(2x) = 2sin(x)cos(x)) to simplify the problem.
   - Determine additional trigonometric values (e.g., cos(x)) using the Pythagorean identity if one value (e.g., sin(x)) is given.

3. **Permutations and Combinatorics**:
   - Understand the structure of permutations and the effect of operations like swaps.
   - Use combinatorial counting techniques to enumerate possible configurations under given constraints.

4. **Properties of Geometric Shapes**:
   - Recall definitions and properties of specific geometric shapes (e.g., kites, rhombuses) to identify them based on given criteria.

5. **Matrix Operations and Polynomial Equations**:
   - Calculate the characteristic polynomial of a matrix to find eigenvalues.
   - Use matrix operations to determine a polynomial that satisfies given conditions (e.g., f(A)v = 0).

6. **Probability and Stochastic Processes**:
   - Apply principles like the reflection principle in stochastic processes to calculate probabilities involving events over intervals.

7. **Combinatorial Design and Graph Theory**:
   - Model problems using graphs or sets and use combinatorial arguments or graph theory to solve them.
   - Consider constraints like no identical choices or specific differences between choices to limit or count valid configurations.

8. **Geometry and Measurement in 3D Shapes**:
   - Use properties of parallel lines and geometric relations in 3D (e.g., tetrahedrons) to find measurements like distances or angles.

9. **Sequences and Logarithmic Conditions**:
   - Convert given conditions into a different form (e.g., differences in sequences) to simplify analysis.
   - Use properties of logarithms and constraints on sequence values to count valid sequences.

10. **Advanced Combinatorics and Graph Theory**:
    - Model complex combinatorial problems with graphs, considering vertices and edges as specific elements (e.g., hats and colors).
    - Use advanced counting principles and inequalities to determine the maximum or minimum number of configurations satisfying all conditions.
</hints>

Here is the problem:
{PROBLEM}

Remember to provide a latex formula as the final answer to the problem.
"""

        messages = [
            {
                "role": "system",
                "content": SYS_PROMPT
            },
            {
                "role": "user",
                "content": USER_PROMPT.format(PROBLEM=problem)
            },
        ]

        client = OpenAI()
        response = client.chat.completions.create(
                    model=self.llm,
                    messages=messages,
                    temperature=self.temperature,
        )
        
        response_text = response.choices[0].message.content
        print (response_text)
        answer = response_text.split("Final Answer:")[-1].strip()
        return answer

def expert_5(problem):
    expert = MathExpert5()
    return expert.run(problem)
 
