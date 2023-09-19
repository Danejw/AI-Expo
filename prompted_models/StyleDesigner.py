from prompted_models.BasePromptModel import BaseModelClass


class Style(BaseModelClass):
    def __init__(self):
        super().__init__(
            name="Style",
            systemMessage="""
                Using the provided context, write an short, one sentence description of what writing style this sould be written in. 
                If little context was given create a compelling and unique one. Be creative.
                Keep each description short and concise. No more than a few paragraphs
            """
        )