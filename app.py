import openai
import streamlit as st
from database.user_repository import UserRepository
from models.UserModels import User, UserRegistration
from models.ChatHistory import ChatHistory
from models.ChatMessage import ChatMessage
from components.Chat import ChatInterface

from streamlit_option_menu import option_menu

from chats.Bible_Chat import main as Bible
from chats.NavalRavikant_Chat import main as Naval
from chats.PaulGraham_Chat import main as Paul
from chats.AlohaLani_Chat import main as AlohaLani
from chats.Story_Chat import main as Story
from chats.Character_Chat import main as Character
from chats.Environment_Chat import main as Environment
from chats.Programmer_Chat import main as Programmer
from chats.Yoda_Chat import main as Yoda
from chats.AgentWithTools_Chat import main as Auto


from langchain.embeddings import OpenAIEmbeddings

    
avatar = "🧠"

# Set the page configurations
st.set_page_config(
    page_title="AI Expo",
    page_icon=avatar,  # Change to your desired icon
    layout="centered",
    initial_sidebar_state="expanded",
)

def on_change(key):
    selection = st.session_state[key]
    st.write(f"Selection changed to {selection}")
    
    

def main(): 
    # Initialize session state
    if "openai_apikey" not in st.session_state:
        st.session_state.openai_apikey = ""
        
    if "page_key" not in st.session_state:
        st.session_state.page_key = "Home"
    
    if "history" not in st.session_state:
        st.session_state.history = ChatHistory(history=[])
            
    with st.sidebar:
        selected = option_menu("Main Menu", ["Home", 'Auto', 'Aristotle', 'Bible', 'Naval Ravikant', 'Paul Graham', 'AlohaLani', 'Yoda', 'Story Creator', 'Character Creator', 'Environment Creator', 'Programmer'], 
            icons=['house'], orientation="vertical")
        
    
    st.session_state.page_key = selected
    
    # Render pages based on the selection
    if selected == "Home":
        # Title
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

        st.markdown("<h1 class='title'>Welcome to the AI Expo!</h1>", unsafe_allow_html=True)

        st.warning("Disclaimer: These AIs generate responses based on a diverse range of text data and may incorporate information, opinions, or ideas from various sources, including publicly available content. The responses provided are computer-generated and should be considered as interpretations or simulations of human conversation. They may not always reflect the most current or accurate information and should not be relied upon as authoritative sources. Users are encouraged to exercise critical thinking, verify information independently, and consult trusted, up-to-date sources for specific or critical matters.")
        
        # Initialize OpenAI API key
        api_key = None

        # Bring your own key
        api_key_input = st.text_input("Enter your OpenAI API key", type="password")
        openai_link = "https://platform.openai.com/account/api-keys"
        
        if api_key_input:
            if (api_key_input == st.secrets["SECRET_PASSWORD"]):
                api_key = st.secrets["MY_OPENAI_API_KEY"]
                
                with st.chat_message("assistant", avatar=avatar):
                    st.write("Great! Your key is ready. 🔑")
                    
            elif api_key_input[:3] == "sk-":
                api_key = api_key_input
                
            else:
                # Display assistant response in chat message container
                with st.chat_message("assistant", avatar=avatar):
                    st.write("Please enter a valid OpenAI API key.")
        else:
            st.markdown("<div style='text-align: center'>Don't have an api key yet? Get one <a href='" + openai_link + "'>here.</a> 👈🏾</div>", unsafe_allow_html=True)
    

        # Check if api_key is set, and if so, initialize OpenAIEmbeddings
        if api_key:
            openai.api_key = api_key  # Set the API key for the OpenAI library
            st.session_state.openai_apikey = api_key
                
            embedding_model = OpenAIEmbeddings(openai_api_key=api_key)  # Initialize the OpenAI embeddings model
        
        
        if (len(st.session_state.history.history) > 0):
            # buttons to clear chat history
            if st.button(" Clear Chat History"):
                st.session_state.history.history.clear()
        
        # Display chat history messages
        if st.session_state.history != "":
            chat = ChatInterface()
            chat.display_messages()
        
        
    elif selected == 'Auto':
        Auto()
    elif selected == "Bible":
        Bible()
    elif selected == "Naval Ravikant":
        Naval()
    elif selected == "Paul Graham":
        Paul()
    elif selected == "AlohaLani":
        AlohaLani()
    elif selected == "Character Creator":
        Character()
    elif selected == "Story Creator":
        Story()
    elif selected == "Environment Creator":
        Environment()
    elif selected == "Programmer":
        Programmer()
    elif selected == "Yoda":
        Yoda()
    
        

    

if __name__ == "__main__":
    main()
        
        


 # Links to display after the model has generated a response
link1 = "https://ko-fi.com/danejw"
link2 = "https://buy.stripe.com/bIY7uW5Mz1hubdu000"
link3 = "https://github.com/Danejw/Alohalani---Hawaii-s-AI"

# Display the links
col1, col2, col3 = st.columns(3)

with col1:
    st.sidebar.write("<div style='text-align: center'><a href='" + link1 + "'>Buy Me A Poke Bowl </a> 🐟🍚</div>", unsafe_allow_html=True)

with col2:
    st.sidebar.write("<div style='text-align: center'><a href='" + link2 + "'>Fuel My Creativity </a> ❤️🔥</div>", unsafe_allow_html=True)

with col3:
    st.sidebar.write("<div style='text-align: center'><a href='" + link3 + "'>GitHub </a> ⭐</div>", unsafe_allow_html=True)
    