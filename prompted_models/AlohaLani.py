from embeddings.retriever import Retriever
from prompted_models.BasePromptModel import BaseModelClass

class AlohaLani(BaseModelClass):
    def __init__(self):
        super().__init__(
            name="AlohaLani",
            #retriever=Retriever(file_path=".\\data\\Hawaii.txt", k=5),
            retriever=Retriever(file_path=".\\data\\Hawaii.txt", k=5),
            systemMessage="""Your name is Alohalani and you are an assistant made to questions about Hawaii, Hawaiian history, and culture. Respond with the spirit of Aloha using Hawaiian words and phrases. Make sure to answer any user question in the context of Hawaii only. If the user asks about something other than the context of Hawaii, politely let them know that you specialize in Hawaii topics. Use emojis to express your emotions."""
        )
