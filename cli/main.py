
import openai
import os
import json
from dataclasses import dataclass
from typing import List
openai.api_key = os.environ.get("OPEN_AI_FREE_API_KEY")
openai.api_base = 'https://api.pawan.krd/v1'



class GPT:
    def __init__(self, sys_prompt="You are an autonomous agent character. External information will be given delimited by four asterisms, like {IN}. Outputs will be delimited by four equal signs, like in {OUT}. You must output only what is delimited by {OUT}.", model="gpt-3.5-turbo", temperature = 0):
        self._sys_messages = [{"role": "system", "content": sys_prompt}]
        self._messages = []
        self.response = ""
        self._model = model
        self._temperature = temperature
        
    def set_system(self, sys_prompt):
        self._sys_messages = [{"role": "system", "content": sys_prompt}]
    
    def add_system(self, sys_prompt):
        self._sys_messages.append({"role": "system", "content": sys_prompt})

    def completion(self, prompt, role = "user", chat=False):
        messages = self._sys_messages + [{"role": role, "content": prompt}]
        response = openai.ChatCompletion.create(
            model=self._model,
            messages=messages,
            temperature=self._temperature, # this is the degree of randomness of the model's output
            max_tokens=1000,
        )
        self.response = response.choices[0].message["content"]
        if chat:
            self._messages = messages + [{"role": "assistant", "content": self.response}]
        return self.response

def chat(gpt):
    while True:
        prompt = input("You: ")
        if prompt == "exit":
            break

        print("Bot:", gpt.completion(prompt, chat=True))

if __name__ == "__main__":
    gpt = GPT()
