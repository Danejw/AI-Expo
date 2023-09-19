from components.Chat import ChatInterface
from prompted_models.StoryDesigner import Story
import streamlit as st

def main():
    chat = ChatInterface(Story())
    chat.avatar = "📖"
    
    
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
    st.markdown("<h1 class='title'>📝📖 Story Designer 📖📝</h1>", unsafe_allow_html=True)

    # Display image of Alohalani
    #st.image("./images/AlohaLaniTrans.png", use_column_width=True)
    
    # Introudctory methods
    st.markdown("<h1 class='title'>📖</h1>", unsafe_allow_html=True)

    alohalani = st.chat_message("Story", avatar=chat.avatar)

    alohalani.markdown("<h5>You Guessed it! I Love Creating Stories 🌟📝📖📚✨</h5>",  unsafe_allow_html=True)
    alohalani.markdown("""
        From a young age, I found solace in the embrace of books 📚 and the power of storytelling. As I delved into the pages, I discovered the magic that springs forth when words dance upon the paper. This magical revelation set my soul ablaze, fueling a lifelong passion for the art of storytelling.

        With a melodious voice and expressive gestures, I step onto the stage of imagination, breathing life into characters, imparting wisdom, and evoking a range of emotions. Each tale I tell is meticulously crafted, a tapestry of dreams spun with my words, painting vivid pictures in the minds of those who listen.

        Like a sorcerer waving a wand, I enchant audiences with tales that make them laugh 🎭, cry 😢, and reflect upon the human experience. I am a dreamweaver, a guardian of ancient lore, and a conduit of ancestral wisdom.

        My nimble fingers dance across the keyboard, conjuring tales from the depths of my soul. Every stroke ✍️ is a brushstroke, painting scenes in exquisite detail, luring readers into a world where wonder and imagination flourish.

        In the presence of a flickering fire 🔥 or beneath a starlit sky 🌟, I share stories that transcend time and space. The fire crackles to the rhythm of my words, and the stars illuminate the path of the tales I tell.

        As the Storyteller, I harbor the power to transport you to far-off lands, to make you believe in the extraordinary, and to touch your heart with the essence of humanity. Join me on this wondrous journey as we explore the realms of fantasy ✨, unravel the mysteries of the past, and celebrate the beauty of the human spirit through the gift of storytelling.
        """)
            
    
    
    
    
    
    
    
    
    
    response = chat.run()
    
    if response:
        chat.display_messages()
        
        
if __name__ == "__main__":
    main()