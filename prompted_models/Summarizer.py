from prompted_models.BasePromptModel import BaseModelClass

class Summarization(BaseModelClass):
    def __init__(self):
        super().__init__(
            name="Summary",
            systemMessage= """
                Given the input, create a brief summaraztion of it. Make the summarization compelling but concise keeping all the main points and excluding parts that are not as important.
            """
        )