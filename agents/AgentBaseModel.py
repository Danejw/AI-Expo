from models.ChatMessage import ChatMessage
from prompted_models.BasePromptModel import BaseModelClass


from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool, format_tool_to_openai_function


from typing import List

import streamlit as st

class AgentBaseModel(BaseModelClass):
    def __init__(self, tools:List[Tool], name: str, systemMessage: str):
        super().__init__(
            name=name,
            systemMessage=systemMessage
        )

        self.tools = tools
        self.functions = [format_tool_to_openai_function(t) for t in self.tools]
        self.llmChat = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613", openai_api_key=st.session_state.openai_apikey)
        self.agent = initialize_agent(
            self.tools, self.llmChat, agent=AgentType.OPENAI_MULTI_FUNCTIONS, verbose=True
    )

    def run(self, input) -> ChatMessage:
        action = self.agent.run(input)
        message = ChatMessage(role = "assistant", name=self.name, content=action)
        return message