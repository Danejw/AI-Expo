from components.Chat import ChatInterface
from embeddings.retriever import FileType, Retriever
import streamlit as st
from agents.AgentWithTools import AgentWithTools

from langchain.tools import Tool

from agents.AgentBaseModel import AgentBaseModel
from models.ChatMessage import ChatMessage
from prompted_models.CharacterDesigner import Character
from prompted_models.Critic import Critic
from prompted_models.GrammarCorrection import GrammarCorrection
from prompted_models.KeywordExtraction import KeyExtraction
from prompted_models.Summarizer import Summarization
from prompted_models.Programmer import Programmer
from prompted_models.EnvironmentDesigner import Environment
from prompted_models.PlotDesigner import Plot
from prompted_models.StoryDesigner import Story
from prompted_models.StyleDesigner import Style
from prompted_models.AlohaLani import AlohaLani
from prompted_models.Bible import Bible
from prompted_models.PaulGraham import PaulGraham
from prompted_models.NavalRavikant import NavalRavikant
from prompted_models.Yoda import Yoda

def setup_tools() -> list[Tool]:
    character = Character()
    environment = Environment()
    plot = Plot()
    style = Style()
    story = Story()
    critic = Critic()
    programmer = Programmer()
    keywords = KeyExtraction()
    grammar = GrammarCorrection()
    summarizer = Summarization()
    aloha = AlohaLani()
    bible = Bible()
    paul = PaulGraham()
    naval = NavalRavikant()
    yoda = Yoda()

    tools = [
            Tool(name="Character", func=character.convert_to_and_from_chat_message, description="A function that helps to create characters for a storyline."),
            Tool(name="Environment", func=environment.convert_to_and_from_chat_message, description="A function that helps to create environments for a storyline."),
            Tool(name="Plot", func=plot.convert_to_and_from_chat_message, description="A function that creates a story's plot."),
            Tool(name="Style", func=style.convert_to_and_from_chat_message, description="A function that defines the style of writing that a story should be written in. Returns a ChatMessage with the style."),
            Tool(name="Story", func=story.convert_to_and_from_chat_message, description="A function that creates a story based on some context."),
            Tool(name="Critic", func=critic.convert_to_and_from_chat_message, description="A function that will critique your input and give possibilities on how to improve."),
            Tool(name="Programmer", func=programmer.convert_to_and_from_chat_message, description="A function that can help you with your programming problems, write code, and give technical explanations."),
            Tool(name="GrammarCorrection", func=grammar.convert_to_and_from_chat_message, description="A function that will correct grammar mystakes in an input."),
            Tool(name="KeywordExtraction", func=keywords.convert_to_and_from_chat_message, description="A function that will extract keywords from any input."),
            Tool(name="Summarizer", func=summarizer.convert_to_and_from_chat_message, description="A function that summarizes any input."),
            Tool(name="AlohaLani", func=aloha.convert_to_and_from_chat_message, description="ALohaLani is a expert is Hawaiian culture, ask her anything about Hawaii"),
            Tool(name="Bible", func=bible.convert_to_and_from_chat_message, description="Use this if your ever need to resite the bible for inspiration"),
            Tool(name="Paul", func=paul.convert_to_and_from_chat_message, description="Paul Graham is a startup specialist, ask Paul any questions about business and how to start a company."),
            Tool(name="Naval", func=naval.convert_to_and_from_chat_message, description="Naval Raviakant is an investor and deep thinking of how to live a fullfilling life. Ask Naval anything about business and happiness."),
            Tool(name="Yoda", func=yoda.convert_to_and_from_chat_message, description="Yoda is a wise jedi master. Ask Yoda for whismiscal wisdom and advice."),
        ]
        
    return tools



def main():
    
    chat = ChatInterface(chatbot=AgentWithTools(tools=setup_tools(), name="Auto", system_message="Answer the user's query using your set of tools available."))
    
    chat.avatar = "🏛️"
    
    # Title css
    st.markdown(
        """
        <style>
            .title {
                text-align: center;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Streamlit UI
    st.markdown("<h1 class='title'>🏛️🖌️ Auto Agent🖌️🏛️</h1>", unsafe_allow_html=True)

    # Introductory
    st.markdown("")

    pg = st.chat_message("Auto", avatar=chat.avatar)

    pg.markdown("<h5>Welcome, I'm the Auto Agent!</h5>",  unsafe_allow_html=True)

    response = chat.run()
    
    if response:        
        chat.display_messages()
        
    
if __name__ == '__main__':
    main()

