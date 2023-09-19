import os
from langchain.tools import Tool


import langchain

import openai
import asyncio
import time

import streamlit as st

import os
from dotenv import load_dotenv

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
from prompted_models.FunctionManager import FunctionManager


load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("Auto Story Gen")

# Set up tools
character = Character
environment = Environment
plot = Plot
style = Style
story = Story
critic = Critic
programmer = Programmer
keywords = KeyExtraction
grammar = GrammarCorrection
summarizer = Summarization

tools = [
    Tool(name="Character", func=character.run, description="A function that helps to create characters for a storyline. Returns a ChatMessage describing a character."),
    Tool(name="Environment", func=environment.run, description="A function that helps to create environments for a storyline. Returns a ChatMessage describing an environment."),
    Tool(name="Plot", func=plot.run, description="A function that creates a story's plot. Returns a ChatMessage describing the plot in detail."),
    Tool(name="Style", func=style.run, description="A function that defines the style of writing that a story should be written in. Returns a ChatMessage with the style."),
    Tool(name="Story", func=story.run, description="A function that creates a story based on some context. Returns a ChatMessage with the story."),
    Tool(name="Critic", func=critic.run, description="A function that will critique your input and give possibilities on how to improve. Returns a ChatMessage."),
    Tool(name="Programmer", func=programmer.run, description="A function that can help you with your programming problems, write code, and give technical explanations. Returns a ChatMessage with the story."),
    Tool(name="GrammarCorrection", func=grammar.run, description="A function that will correct grammar mystakes in an input. Returns a ChatMessage."),
    Tool(name="KeywordExtraction", func=keywords.run, description="A function that will extract keywords from any input. Returns a ChatMessage."),
    Tool(name="Summarizer", func=summarizer.run, description="A function that summarizes any input. Returns a ChatMessage."),

]

# Set up function manager
functionManager = FunctionManager(tools)

input = st.text_input("Write your prompt here")

langchain.debug = True

if st.button("Function Call"):
    action = functionManager.run(input)
    st.markdown(action.name)
    st.markdown(action.role)
    st.markdown(action.content)

    print(action.content)