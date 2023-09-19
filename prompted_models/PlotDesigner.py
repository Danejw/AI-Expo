from prompted_models.BasePromptModel import BaseModelClass


class Plot(BaseModelClass):
    def __init__(self):
        super().__init__(
            name="Plot",
            systemMessage="""
                Using the provided context write one interesting plot. 
                If little context was given create a compelling and unique plot. Be creative.
                Keep your response just to one plot. 
                Keep each description short and concise. No more than a few paragraphs
            """
        )
