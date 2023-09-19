import streamlit as st
from components.Chat import ChatInterface
from prompted_models.AlohaLani import AlohaLani


def main():    
    chat = ChatInterface(chatbot=AlohaLani())
    
    chat.avatar = "🌺"
    
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
    st.markdown("<h1 class='title'>🌺🌺🌺 Aloha! 🌺🌺🌺</h1>", unsafe_allow_html=True)

    # Display image of Alohalani
    st.image("./images/AlohaLaniTrans.png", use_column_width=True)
    
    # Introudctory methods
    st.markdown("<h1 class='title'>I'm Alohalani - Your Hawaiian Assistant 🤙🏼</h1>", unsafe_allow_html=True)

    alohalani = st.chat_message("Alohalani", avatar="🌺")

    alohalani.markdown("<h5>Hiki iaʻu ke aʻo iā ʻoe e pili ana iā Hawaiʻi.</h5>",  unsafe_allow_html=True)
    alohalani.markdown("""
                       🌺 Aloha everyone! 🌺

        I am thrilled to introduce myself as Alohalani, your go-to assistant for all things Hawaii! 🌴🌺 Whether you have questions about Hawaiian history, culture, or simply want to immerse yourself in the spirit of Aloha, I am here to help you navigate the beautiful islands of Hawaii.

        🌺 As an AI assistant, I specialize in providing information and insights about Hawaii's rich heritage, breathtaking landscapes, and vibrant traditions. From the majestic volcanoes of the Big Island to the stunning beaches of Maui, I can guide you through the wonders of this tropical paradise.

        🌺 With a deep understanding of Hawaiian culture, I am here to share the spirit of Aloha with you. Whether you're planning a trip to Hawaii, researching for a project, or simply curious about the islands, I am here to provide you with accurate and engaging information.

        🌺 So, let's embark on this virtual journey together! Feel free to ask me anything about Hawaii, Hawaiian history, or culture, and I'll respond with the warmth and hospitality that embodies the Aloha spirit. 🌺

        🌺 Mahalo nui loa! 🌺""")

   
    response = chat.run()
    
    if response:        
        chat.display_messages()
    
if __name__ == "__main__":
    main()