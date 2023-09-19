from typing import List

import langchain
import streamlit as st
from langchain.tools import Tool

from agents.AgentBaseModel import AgentBaseModel
from models.ChatMessage import ChatMessage


class AgentWithTools(AgentBaseModel):
    def __init__(self, tools : List[Tool] = None, system_message: str = None, name: str = None):
        super().__init__(        
            name=name,
            systemMessage=system_message,
            tools=tools

        )
        
    def send_chat_message(self, message: ChatMessage):
        yield f"data: {message.json()}\n\n"
        
    def run_agent(self, input: str):
        return self.run(input)
