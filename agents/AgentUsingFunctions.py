## GOAL:
# This agent will be able too choose when to use any function from it own list of functions.


from langchain.tools import Tool, format_tool_to_openai_function
from agents.AgentBaseModel import AgentBaseModel

from embeddings.retriever import Retriever
from models.ChatMessage import ChatMessage
from prompted_models.BasePromptModel import BaseModelClass
from langchain.agents import AgentType, initialize_agent



class AgentUsingFunctions(BaseModelClass):
    def __init__(self, name: str, systemMessage: str):
        super().__init__(
            name=name,
            systemMessage=systemMessage
        )
        
        # Set up the functions as tools for the agent to use
        self.tools: list[Tool] =  [
            Tool(name="bid", func=self.bid, description="A function that will bid on if it wants to speak next within a conversation."),
            Tool(name="retrieve", func=self.retrieve, description="A function that will retrieve a response from its vector database of responses based on the input."),
            Tool(name="respond", func=self.respond, description="A function that respoinds to the input."),
            Tool(name="search", func=self.search, description="A function that will search the internet for a response to the input if the retrieval doesnt find a relevant answer to the input."),
            Tool(name="ask human", func=self.search, description="A function that will ask the user for more information if it doesnt understand the input."),
        ]
        
        self.retriever = Retriever()
        self.history: list[ChatMessage] = []
        self.system_message: ChatMessage = None
        self.functions = [format_tool_to_openai_function(t) for t in self.tools]
        self.llmChat = self #ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
        self.agent = initialize_agent(
            self.tools, self.llmChat, agent=AgentType.OPENAI_MULTI_FUNCTIONS, verbose=True
        )
        
    def respond(self, input: ChatMessage) -> ChatMessage:
        pass
    
    def bid(self) -> int:
        pass
    
    def retrieve(self, input: ChatMessage) -> list[tuple[str, float]]:
        pass
    
    def search(self, input: ChatMessage):
        pass
    
    def ask_human(self):
        pass
    