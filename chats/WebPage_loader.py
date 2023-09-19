import streamlit as st

from embeddings.retriever import Retriever


retriever = Retriever()


import validators


st.title("Enter a webpage's url")

input = st.text_input("Enter a URL")

if st.button("Submit"):    
    if validators.url(input):
        resoponse = retriever.load_web(url=input)
        st.write(resoponse)
    else:
        st.write("Invalid URL")
