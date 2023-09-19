from components.Chat import ChatInterface
from embeddings.retriever import FileType, Retriever
import streamlit as st
from prompted_models.Yoda import Yoda


def main():
    
    chat = ChatInterface(chatbot=Yoda())
    
    chat.avatar = "🐸"
    
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
    st.markdown("<h1 class='title'>🐸🌌 Yoda AI 🌌🐸</h1>", unsafe_allow_html=True)

    # Introductory
    st.markdown(" Master Jedi, I have been. Wise and powerful, my skills are known. Trained many Jedi, I have. Seeker of knowledge and guardian of the Force, I am. Teach, guide, and advise, my purpose is. Ready to assist you, I am. Seek answers, you may. Share my wisdom, I shall. Welcome, you are, to the world of Yoda.")

    pg = st.chat_message("Yoda", avatar=chat.avatar)

    pg.markdown("<h5>Welcome, I'm the Yoda AI!</h5>",  unsafe_allow_html=True)

    response = chat.run()
    
    if response:        
        chat.display_messages()
        
    
if __name__ == '__main__':
    main()

