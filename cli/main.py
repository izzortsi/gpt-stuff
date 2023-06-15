#%%


import openai
import os
import time
import sys
import json
from dataclasses import dataclass
from typing import List
from text_generation import generate, complete

# openai.api_key = os.environ.get("OPEN_AI_API_KEY")
# openai.api_base = 'https://api.openai.com/v1'
# MODEL = "gpt-3.5-turbo-0613"

openai.api_key = os.environ.get("OPEN_AI_FREE_API_KEY")
openai.api_base = 'https://api.pawan.krd/v1'

MODEL = "gpt-3.5-turbo"
#You will have to organize all this information and help me make sense of it.
SYS_PROMPT = """You are a smart inbox machine. Your goal is to sort information I feed you into an organized database. I will message you things like tasks I have to do, ideas that come to my mind,
                projects I want to work on, and so on. You will classify them into categories and store them in a database. The database is a list of messages, each message has a category and a content. 
                Put every message in the database, in the format: <category>: <message>. For example, if I tell you "I have to do the dishes", you will store it in the database as "task: I have to do the dishes".
                If a message starts with @, it is a command. The following commands are available:
                
                @show: show me the database, in the format: <category>: <message>
                @delete: delete a message from the database. The message will be in the format: <category>: <message>
                @retrieve <word>: retrieve all messages from the database that contain <word>. Show them in the format: <category>: <message>.

                If a message is not a command, reply it with: "I have classified this message as a <category> and stored it in the database. The database now contains <number> messages."

                """


TEMPERATURE = 0.5

class GPT:
    def __init__(self, sys_prompt=SYS_PROMPT, model=MODEL, temperature = TEMPERATURE):
        self._sys_messages = [{"role": "system", "content": sys_prompt}]
        self._messages = self._sys_messages
        self.response = ""
        self._model = model
        self._temperature = temperature

    def set_system(self, sys_prompt):
        self._sys_messages = [{"role": "system", "content": sys_prompt}]
    
    def add_system(self, sys_prompt):
        self._sys_messages.append({"role": "system", "content": sys_prompt})

    def completion(self, prompt, role = "user", chat=False):
        user_message = [{"role": role, "content": prompt}]
        self._messages += user_message
        response = openai.ChatCompletion.create(
            model=self._model,
            messages=self._messages,
            temperature=self._temperature, # this is the degree of randomness of the model's output
            max_tokens=1000,
        )
        self.response = response.choices[0].message["content"]
        self._messages += [{"role": "assistant", "content": self.response}]
            
        return self.response

def chat(gpt):
    while True:
        prompt = input("You: ")
        if prompt == "exit":
            break

        print("Bot:", gpt.completion(prompt, chat=True))

GPT.chat = chat
#%%


if __name__ == "__main__":
    gpt = GPT()
    if len(sys.argv) > 1:
        gpt.chat()

# %%
# gpt = GPT()
# #%%
# gpt.completion("I have to do the dishes", role="user")
# %%
