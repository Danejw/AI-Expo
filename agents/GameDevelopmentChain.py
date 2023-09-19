from models.ChatHistory import ChatHistory
from prompted_models.Programmer import Programmer, ProgrammingBlueprint, ProgramReasoning

from prompted_models.StoryDesigner import Story, StoryStructure, StoryOutline


programmer = Programmer()
programmingBlueprint = ProgrammingBlueprint()
programReasoning = ProgramReasoning()

story = Story()
storyStructure = StoryStructure()
storyOutline = StoryOutline()




import streamlit as st



input = st.text_area("prompt me")
if st.button("Chain it up"):    
    outline = storyOutline.convert_chat_message(message=input)
    structure = storyStructure.convert_chat_message(message=outline)
    reasoning = programReasoning.convert_chat_message(message=structure)
    blueprint = programmingBlueprint.convert_chat_message(message= reasoning)
    
    st.markdown(outline)
    st.markdown(structure)
    st.markdown(reasoning)
    st.markdown(blueprint)
    

