# GAIC-Spring-2024-VE

This repository is dedicated to housing the code for the competition "2024 GAIC Maths Questions and Solutions Now Available for Download" organized by AGI Odyssey in 2024. You can access the competition [here](https://www.agiodyssey.org/#/Olympic).

## User Guide

### Installation of Environment

```bash
conda env create -f environment.yaml

conda activate math_gaic

```

Configuration with .env File

```bash
OPENAI_API_KEY=sk-
```

Before you run this project, please complete your openai key.

Automated Script for Problem Solving

```bash
bash solving.sh
```

Utilizing the Interface for Solving Specific Questions

```bash
question="..."
save_path="..."
method="1" # should in ["1", "2", "3"]
python scripts/hybrid_solving.py \
    --question "$question" \
    --method "1" \
    --save_path "$save_path"
```

Project Overview
File Structure

```bash
.
├── data
│   ├── chi-square-table.md
│   ├── data_process.ipynb
│   ├── Global_Artificial_Intelligence_Championship_Math2024.tex
│   ├── __init__.py
│   ├── problems.json
│   ├── statistic_table.py
│   ├── t-distribution.md
│   └── Z-distribution.md
├── LICENSE
├── README.md
├── requirements.txt
├── scripts
│   ├── auto_solving.py
│   ├── hybrid_solving.py
│   ├── __init__.py
│   └── solving_methods.py
├── src
│   ├── experts
│   ├── file_io_utils.py
│   ├── __init__.py
│   ├── main_scripts.py
│   └── steps
└── test_ritht.py
```

### What we du in this competition:

1. We select different solving methods for different problems.
2. We have crafted more professional prompts for some challenging problems. (The first 100 problems use solving_method_1 or solving_method_4)
3. For statistical problems that require table lookup, we have adopted a specialized table lookup method. (We use solving_method_3)
4. For the remaining problems, we have adopted a more generalized method. (We use solving_method_2)

During the competition, we set the parameter `src.experts.expert_1.SolvingMachine.max_correction_times=30` to 
maximize the accuracy as much as possible.  
If you want to try, we suggest you can set `src.experts.expert_1.SolvingMachine.max_correction_times=5` to reduce 
the runtime.  

Our code does not print additional information in the terminal or store logs. 
If needed, please add it yourself. You can refer to `src/experts/expert_1/thinking_flow_utils/logger.py` for guidance.

```
python scripts/auto_solving.py
```

We actually employ parallel processing with 10 processes to handle these tasks. 
Sometimes, the program might get stuck, and we utilize `scripts/hybrid_solving.py` to address the stalled tasks.

### File Introduction

#### ./data Directory

This directory stores data. We utilize the data_process.ipynb to process questions into problems.json.

Example data within problems.json:

```
{
    "1": {
        "content": "Let $S=\\left\\{ 1,2,\\cdots 2024 \\right\\}$, if the set of any $n$ pairwise prime numbers in $S$ has at least one prime number, the minimum value of $n$ is \\underline{\\hspace{2cm}}.",
        "answer": "",
    },
    "2": {
        "content": "Let $A_l = (4l+1)(4l+2) \\cdots \\left(4(5^5+1)l\\right)$. Given a positive integer $l$ such that $5^{25l} \\mid A_l$ and $5^{25l+1} \\nmid A_l$, the minimum value of $l$ satisfying these conditions is \\underline{\\hspace{2cm}}.",
        "answer": "",
    },
    "3": {
        "content": "Sasha collects coins and stickers, with fewer coins than stickers, but at least 1 coin. Sasha chooses a positive number $t > 1$ (not necessarily an integer). If he increases the number of coins by a factor of $t$, then he will have a total of 100 items in his collection. If he increases the number of stickers by a factor of $t$, then he will have a total of 101 items in his collection. If Sasha originally had more than 50 stickers, then he originally had \\underline{\\hspace{2cm}} stickers.",
        "answer": "",
    },
    ...
}
```
### File Introduction

#### ./data Directory

Data is stored here. We utilize `data_process.ipynb` to process questions into` problems.json`.

Example data within `problems.json`:

We also collect commonly used statistical information for table lookup: `statistic_table.py`.

#### ./scripts Directory

This directory stores the scripts we directly use:

`auto_solving.py`: A script capable of automatically selecting solving methods, useful for bulk problem solving. This is a simplified automation script for our strategy of choosing solutions for different problems when we participate in competitions.

`hybrid_solving.py`: Allows manual selection of solving methods to solve specific questions. Refer to the above for usage.

`solving_methods.py`: Stores all our solving methods, detailed descriptions will follow.

#### ./src Directory

`./src/experts`: Stores our solving experts, each expert is a multi-agents system or Agent. Their respective structures will be explained below.

### Solving Multi-Agents System Design

We have constructed this solving system based on large language models, employing Prompts Engineering, CoT, Multi-Agents, Agents Interaction, and Tools. 

#### Structure
 
IMPORTANT: All the llm-based agnnt in this project baes on `gpt-4-turbo` with `temprature=0`

Main Method intro: `solving_method_2`:  
Agent:

These agents are AI-Agents or Multi-Agents systems based on LLM.

1. experts: Each expert is a multi-agents system or Agent. Their structures will be explained below. Each expert is capable of individually solving a question.
2. voting: An agents-system composed of multiple voting-agents, capable of voting on questions from different perspectives to select a final answer.
3. simplify: Able to condense a long and complex answer into a concise summary.
4. classification: Capable of determining if a question requires statistical table lookup.

Execution Process:

Step 1: Each Expert independently solves the question.
Step 2: The Voting-System selects the most appropriate answer.
Step 3: The most appropriate answer is simplified.

### Experts Introduction

#### expert_1

Solving Entry: `./src/experts/expert_1/SolvingMachine.py`

Comprising three parts: CTF_thinking_flow, CTF_thinking_flow_correction, Evaluator

1. CTF_thinking_flow `./src/experts/expert_1/thinking_flow.py`:
    1. Plan Agent: Outlines a plan for the question.
    2. Solving Agent: Answers the question according to the plan.
    3. Calculus Agent: Translates the process of 1.ii into Python code, then uses a Python interpreter to execute it, thus avoiding the limitation of LLM computational power. The agent writing the code is in `./src/experts/expert_1/thinking_flow_utils/special_agents/MathCoding.py`.
    4. Fix Agent: Combines 1.ii and 1.iii to produce the final answer, correcting 1.ii based on 1.iii as the final result.
2. Evaluator `./src/experts/expert_1/thinking_flow_utils/special_agents/Evaluator.py`:
    1. prompts_1 Evaluator.evaluator_contradiction: Validates the answer using the method of contradiction.
    2. prompts_2 Evaluator.evaluator_algebra: Validates the answer using algebraic methods.
    3. prompts_3 Evaluator.evaluator_flow: Validates the answer using sequential reasoning.

`CTF_thinking_flow_correction`: Similar internal structure to `CTF_thinking_flow`, but includes information from previous errors to avoid repeating them as much as possible.

PS: All LLM Agents above are instances of `./src/experts/expert_1/thinking_flow_utils/BasicAgent.py`. Their prompts are stored in: `./src/experts/expert_1/thinking_flow_utils/prompts.py`.

Execution Process:

Initially solve with `CTF_thinking_flow`, then validate with `Evaluator`. If incorrect, use `CTF_thinking_flow_correction` for correction. After correction, continue validation with `Evaluator`. Maximum correction times can be set when initializing `SolvingMachine`.

#### expert_2

Solving Entry: `./src/experts/expert_2/expert_2.py`  

Comprising four parts: Solution Code Generator, Solution Validation Code Generator, Code Interpreter, and Voting Agent.  

1. Solution Code Generator: Generates Python code to solve the question.  
2. Solution Validation Code Generator: Generates Python code to validate the solution.  
3. Code Interpreter: Interprets the generated code.  
4. Voting Agent: Votes on the solution based on the generated code.   

Execution Process:  

1. Multiple code solutions are generated by the Solution Code Generator. And one validation code is generated by the Solution Validation Code Generator.
2. Code solutions are interpreted by the Code Interpreter. We will parse the answer from the output of the code. Now we have multiple answers and each answer will be validated by the validation code.
3. The Voting Agent will vote on the answers and select the final answer. Answers that passed the validation will be given higher weights when voting. 

#### expert_3

This is a simple Agent that only uses prompts. It is an instance of `./src/experts/expert_1/thinking_flow_utils/BasicAgent.py`.

Prompts are stored in: `./src/experts/expert_3/cot_math.py`.

This is designed to utilize the basic abilities of GPT-4 to solve problems.

#### expert_4 

Mathematics professionals have designed prompts specifically to solve the first 100 problems.

### Runtime Consumption

The time required for complete solution of a question is: 5-25 mins. (most of them is about 5-10 mins)

We aim to leverage this system to harness the capabilities of GPT-4 as much as possible.
