
from prompted_models.BasePromptModel import BaseModelClass


class KeyExtraction(BaseModelClass):
    def __init__(self):
        super().__init__(
            name="KeyExtraction",
            systemMessage="""
                You will be provided with a block of text, and your task is to extract a list of keywords from it, separated by commas.

                Example:
                Black-on-black ware, pottery tradition, Puebloan Native American, ceramic artists, Northern New Mexico, reduction-fired blackware, pueblo artists, smooth surface, designs, selective burnishing, refractory slip, carving, incising designs, polishing, generations, families, Kha'po Owingeh, P'ohwhóge Owingeh pueblos, matriarch potters, contemporary artists, ancestors
            """
        )