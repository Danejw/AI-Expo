from components.Chat import ChatInterface
from prompted_models.EnvironmentDesigner import Environment
import streamlit as st


def main():
    chat = ChatInterface(Environment())
    chat.avatar = "🌴"
    
    
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
    st.markdown("<h1 class='title'>🌳🗺️ Environment Designer 🗺️🌳</h1>", unsafe_allow_html=True)

    # Display image of Alohalani
    #st.image("./images/AlohaLaniTrans.png", use_column_width=True)
    
    # Introudctory methods
    st.markdown("<h1 class='title'>🌴</h1>", unsafe_allow_html=True)

    alohalani = st.chat_message("Envisionia", avatar=chat.avatar)

    alohalani.markdown("<h5>I'm Envisionia, Your Environment Designer!</h5>",  unsafe_allow_html=True)
    alohalani.markdown("""
        Through my careful craftsmanship, I build enchanting 🏰 structures that captivate the imagination and ignite a sense of wonder. With a heart full of passion ❤️ and a touch of mysticism 🔮, I weave together artistry and storytelling to transport you to extraordinary realms.

        Using the power of design and aesthetics, I pull your ideas into visually stunning realities. Each creation is a unique journey, blending elements of nature 🌿, architecture 🏢, and fantasy ✨ to create a resplendent tapestry of emotions. Through this, my aim is to create environments that not only engage the senses but also leave a lasting impact.

        Collaborating closely with you, I bring a harmonious blend of 🌈 creativity, technical expertise, and an innovative spirit into every project. The goal is to create spaces that radiate joy, spark curiosity, and inspire those who venture into them. My artistry is a symphony 🎶 where imagination takes flight and magic comes alive.

        Let's discover a world of endless possibilities. ✨🌍🎨🏰❤️🔮 Prepare to be immersed in a universe where dreams become tangible and where art tells stories that resonate deeply within your soul.
        """)
    
    response = chat.run()
    
    if response:        
        chat.display_messages()
        
        
        
if __name__ == "__main__":
    main()