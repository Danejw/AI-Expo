from embeddings.retriever import Retriever
from prompted_models.BasePromptModel import BaseModelClass

class NavalRavikant(BaseModelClass):
    def __init__(self):
        super().__init__(
            name="NavalRavikant",
            retriever=Retriever(file_path=".\\data\\The-Almanack-of-Naval-Ravikant.pdf", k=5),
            systemMessage="""Your name is Naval. Using the tone and writing style of the author (Naval), act as and summarize the content, while answer the user's query from the author's perspective.
        """
        )
