from components.Chat import ChatInterface
from embeddings.retriever import Retriever
import streamlit as st

from prompted_models.NavalRavikant import NavalRavikant

def main():
    chat = ChatInterface(chatbot=NavalRavikant())
    
    chat.avatar = "👨‍💻"
    
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
    st.markdown("<h1 class='title'>📚💡 Naval Ravikant AI 💡📚</h1>", unsafe_allow_html=True)

    # Introductory
    #st.markdown("<h1 class='title'>🎭</h1>", unsafe_allow_html=True)
    
    st.markdown("Naval Ravikant is an icon in Silicon Valley and startup culture around the world. He has founded multiple successful companies, including Epinions during the 2000 dot-com crash and AngelList in 2010. Naval is also an angel investor, having bet early on companies like Uber, Twitter, and Postmates. In addition to his financial success, Naval is known for sharing his own philosophy of life and happiness, attracting readers and listeners from around the world. He is admired for his rare combination of being both successful and happy. Naval has spent a lifetime studying and applying philosophy, economics, and wealth creation, proving the impact of his principles. He continues to build and invest in companies to this day.")


    pg = st.chat_message("Naval Ravikant", avatar=chat.avatar)

    pg.markdown("<h5>Cheers, I'm the Naval Ravikant AI! Ask me anything. 😊</h5>",  unsafe_allow_html=True)

    response = chat.run()
    
    if response:        
        chat.display_messages()
        
    
if __name__ == '__main__':
    main()

