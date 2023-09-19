from components.Chat import ChatInterface
from prompted_models.CharacterDesigner import Character
import streamlit as st

def main():
    chat = ChatInterface(Character())
    chat.avatar = "🎭"
    
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
    st.markdown("<h1 class='title'>🎭🖌️ Character Designer 🖌️🎭</h1>", unsafe_allow_html=True)

    # Display image of Alohalani
    #st.image("./images/AlohaLaniTrans.png", use_column_width=True)
    
    # Introudctory methods
    st.markdown("<h1 class='title'>🎭</h1>", unsafe_allow_html=True)

    alohalani = st.chat_message("Pixel Banks", avatar=chat.avatar)

    alohalani.markdown("<h5>Cheers, I'm Pixel Banks, Your Character Designer!</h5>",  unsafe_allow_html=True)
    alohalani.markdown("""
                       👋 Hello there! 
        With my 🎨 imagination and 🧠 creative mind, I bring characters to life for various mediums like 🎮 games, 🎥 movies, 🎭 plays, and even 📱 social media. 
        My passion lies in crafting relatable and captivating characters that leave a lasting impression. Let me sprinkle a touch of magic on your projects! ✨✨✨
        """)

    
    response = chat.run()
    
    if response:        
        chat.display_messages()
        
        
if __name__ == "__main__":
    main()
    