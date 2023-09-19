from langchain import LLMChain, PromptTemplate
from langchain.llms import OpenAIChat
from langchain.memory import ConversationBufferMemory

from prompted_models.BasePromptModel import BaseModelClass


class Critic(BaseModelClass):
    def __init__(self):
        super().__init__(
            name="Critic",
            systemMessage="""
                Act as a harsh but experience critic. Take any input and give a clear and concise critic about multiple aspects of the input. Provide clear instructions on how to make the input a better. 
            """
        )
