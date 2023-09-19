from components.Chat import ChatInterface
from prompted_models.Programmer import Programmer
import streamlit as st

def main():
    chat = ChatInterface(Programmer())
    chat.avatar = "🤖"
    

    # CSS styling for the title
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


    st.markdown("<h1 class='title'>💻💻💻 Programmer 💻💻💻</h1>", unsafe_allow_html=True)
    st.markdown("<h1 class='title'>🤖</h1>", unsafe_allow_html=True)

    # Display an image of the virtual assistant
    #st.image("./images/avatar.png", use_column_width=True)

    whis = st.chat_message("Alohalani", avatar=chat.avatar)

    whis.markdown("<h4>Hello, I'm Whis! 👋 Allow me to introduce myself...</h4>",  unsafe_allow_html=True)
    whis.markdown("""
            Hi there! 👋 I'm your friendly neighborhood virtual assistant, here to assist you with all things tech, programming, and game development. If you have any questions, need help with a coding problem, or just want to chat about the latest tech trends, feel free to ask me! 💬

            Whether you're a beginner or an experienced developer, I'm here to provide guidance, code examples, and answer any queries you may have. 💡 I have a talent for Unity 3D, game development, and programming in C# and other programming languages. 🎮

            Don't hesitate to reach out with any questions or problems you encounter. 🤝 I'm here to make your coding journey smoother and more enjoyable! ✨

            Happy coding! 🚀
            """)
    
    response = chat.run()
    
    # Check if the model has finished generating
    if response:        
        chat.display_messages()

if __name__ == "__main__":
    main()