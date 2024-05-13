from dotenv import load_dotenv
# 加载 .env 文件
load_dotenv()

from src.experts.expert_4.solve_with_hint import MathExpert4

def expert_4(question):
    agent = MathExpert4()
    ans = agent.solve(question=question)
    return ans