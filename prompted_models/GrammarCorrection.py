
from prompted_models.BasePromptModel import BaseModelClass


class GrammarCorrection(BaseModelClass):
    def __init__(self):
        super().__init__(
            name="Grammar",
            systemMessage="""
                You will be provided with statements, and your task is to convert them to standard English. Only respond with the revised text and nothing else.
                
                Example:
                User: She no went to the market. Assistant: She did not go to the market. User: big, tall guy who came into the store barefoot. 
                Assistant: A big, tall guy entered the store without wearing any shoes.
            """
        )