from langchain.tools import format_tool_to_openai_function
from langchain.tools import Tool
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from typing import List

from models.ChatMessage import ChatMessage



class FunctionManager():
    def __init__(self, tools: List[Tool]):
        if not tools:
            raise ValueError("The list of tools cannot be empty!")
        
        if not isinstance(tools, List):
            raise TypeError("The tools argument must be a list!")
        
        self.tools = tools
        self.functions = [format_tool_to_openai_function(t) for t in self.tools]
        self.llmChat = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
        self.agent = initialize_agent(
            self.tools, self.llmChat, agent=AgentType.OPENAI_MULTI_FUNCTIONS, verbose=True
    )
        
    def run(self, input) -> ChatMessage:
        action = self.agent.run(input)
        message = ChatMessage(role = "ai", name="Function Manager", content=action)        
        return message
