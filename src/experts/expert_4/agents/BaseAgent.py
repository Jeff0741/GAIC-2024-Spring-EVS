from typing import Any
from pydantic import BaseModel, model_validator
import os
from openai import OpenAI

class BaseOpenaiAgent(BaseModel):
    """class to identify semantic category for human reaction messages such as twitter response
    """
    
    openai_model_name: str=None
    api_key: str = None
    client: Any = None
    template: Any = None
    
    @model_validator(mode="after")
    def validate_openai(self):
        """validation function before calling openai
        """
        if os.environ["OPENAI_API_KEY"]:
            self.api_key = os.environ["OPENAI_API_KEY"]
        
        if "api_key" not in self.__dict__:
            raise ValueError("openai api key required to use tools with openai api.")
        
        # set client if validated
        self.client = OpenAI(api_key=self.api_key)
        return self
    
    
class OpenaiAgent(BaseOpenaiAgent):
    
    def __init__(self, template, llm="gpt-4-1106-preview"):
        super().__init__()
        self.template = template
        self.openai_model_name = llm
        
    def run(self, **kwargs):
        system = self.template["system"]
        user = self.template["user"]

        prompts = system + "||--||" + user
        unsplit_message = prompts.format(**kwargs)
        [system, user] = unsplit_message.split("||--||")
        message = [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]
        try:
            response = self.client.chat.completions.create(
                model=self.openai_model_name,
                messages=message,
                temperature=0,
            ) 
            text_response = response.choices[0].message.content
        except Exception as error:
            raise ValueError(f"Error occurred when deciding tool usage: {error}")
        
        return text_response