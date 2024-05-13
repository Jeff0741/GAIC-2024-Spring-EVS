from dotenv import load_dotenv
# 加载 .env 文件
load_dotenv()

import json

from src.experts.expert_4.agents.BaseAgent import OpenaiAgent
from src.experts.expert_4.agents.prompts import hint_adapting_template, hint_choosing_template, hint_solve_template

# load hints
with open('src/experts/expert_4/agents/all_hints.json', 'r') as f:
    all_hints = json.load(f)
    
class MathExpert4:
    
    def __init__(self, llm='gpt-4-0125-preview', all_hints=all_hints) -> None:
        self.all_hints = all_hints
        self.hint_choosing_agent = OpenaiAgent(template=hint_choosing_template, llm=llm)
        self.hint_adapting_agent  = OpenaiAgent(template=hint_adapting_template, llm=llm)
        self.hint_solving_agent = OpenaiAgent(template=hint_solve_template, llm=llm)
    
    def solve(self, question:str):
        # Step 1: choose from the hints the one suits the problem
        chosen_hint = self.hint_choosing_agent.run(hints=self.all_hints, question=question)
        
        # (Optional Step 2): adapt hint to form plan
        plan = self.hint_adapting_agent.run(hint=chosen_hint, question=question)
        
        # Step 3: solve with hint
        answer = self.hint_solving_agent.run(hint=chosen_hint + plan, question=question)
        
        return answer