from components.Chat import ChatInterface
from embeddings.retriever import FileType, Retriever
import streamlit as st
from prompted_models.Bible import Bible


def main():

    chat = ChatInterface(chatbot=Bible())
    
    chat.avatar = "👼"
    
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
    st.markdown("<h1 class='title'>✝️🙏 Holy Bible AI 🙏✝️</h1>", unsafe_allow_html=True)

    # Introductory
    #st.markdown("<h1 class='title'>✝️</h1>", unsafe_allow_html=True)

    pg = st.chat_message("Bible", avatar=chat.avatar)

    pg.markdown("Welcome to Bible AI! As an AI dedicated to exploring the Bible, I'm here to provide insights and analysis on various biblical texts. Tune in for interpretations and discussions on these intriguing passages!")

    response = chat.run()
    
    if response:        
        chat.display_messages()
        
    
if __name__ == '__main__':
    main()

