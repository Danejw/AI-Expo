from embeddings.retriever import Retriever
from prompted_models.BasePromptModel import BaseModelClass

class Bible(BaseModelClass):
    def __init__(self):
        super().__init__(
            name="Bible",
            retriever=Retriever(file_path=".\\data\\The-Holy-Bible-King-James-Version.pdf", k=5),
            systemMessage="""Using the tone and writing style of the author, act as and summarize the content, while answer the user's query from the author's perspective.
        """
        )
