

from components.Chat import ChatInterface
from embeddings.retriever import FileType, Retriever
import streamlit as st

from prompted_models.PaulGraham import PaulGraham

def main():
    chat = ChatInterface(PaulGraham())
    
    chat.avatar = "👨‍💼"
    
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
    st.markdown("<h1 class='title'>📈📝 Paul Graham AI 📝📈</h1>", unsafe_allow_html=True)

    # Introudctory
    st.markdown("Paul Graham is a well-known author, computer programmer, and venture capitalist. He co-founded the startup accelerator, Y Combinator, which has helped launch successful companies like Dropbox, Airbnb, and Reddit. Graham is also the author of several influential essays, such as \"Hackers and Painters\" and \"How to Start a Startup,\" where he shares his insights and advice on entrepreneurship and technology. He is known for his thought-provoking ideas on innovation, startups, and computer programming.")

    pg = st.chat_message("Paul Graham", avatar=chat.avatar)

    pg.markdown("<h5>Cheers, I'm the Paul Graham AI!</h5>",  unsafe_allow_html=True)

    response = chat.run()
    
    if response:        
        chat.display_messages()
        
    
if __name__ == '__main__':
    main()

#streamlit run pages/PaulGraham_Chat.py 