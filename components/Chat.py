
from embeddings.retriever import FileType, Retriever
from models.ChatHistory import ChatHistory
from models.ChatHistoryWithKey import ChatHistoryWithKey
from models.ChatMessage import ChatMessage
from prompted_models.BasePromptModel import BaseModelClass
import streamlit as st
  
class ChatInterface:
    def __init__(self, chatbot: BaseModelClass = None) -> None:
        self.chatbot = chatbot
        self.avatar = "🧠"
        self.placeholder = "Type a message..."
        
        if "chatbot" not in st.session_state:
            st.session_state['chatbot'] = self.chatbot
            
        if "history" not in st.session_state:
            st.session_state['history'] = ChatHistory(history=[])
    
    def add_message(self, message: ChatMessage) -> None:
        st.session_state['history'].history.append(message)
        
    def display_messages(self):
        displayed_messages = set()
        
        for message in st.session_state['history'].history:
            message_content = message.content
            if message.role == "user":
                if message_content not in displayed_messages:
                    with st.chat_message("You", avatar="🙂"):
                        st.markdown(message_content)
                        displayed_messages.add(message_content)
                        st.markdown("---")  # Add a horizontal line as a separator
            elif message.role == "assistant":
                if message_content not in displayed_messages:
                    if self.chatbot is None:       
                        with st.chat_message("AI", avatar=self.avatar):
                            st.markdown(message_content)
                            displayed_messages.add(message_content)
                            st.markdown("---")  # Add a horizontal line as a separator
                    else:
                        with st.chat_message(self.chatbot.name, avatar=self.avatar):
                            st.markdown(message_content)
                            displayed_messages.add(message_content)
                            st.markdown("---")  # Add a horizontal line as a separator

    def run(self) -> ChatMessage:        
        if user_input := st.chat_input(self.placeholder, key="user_input"): 
            
            # Add user input to chat history
            user_message = ChatMessage(role="user", name="You", content=user_input)
            self.add_message(user_message)
            

            assistant_response = self.chatbot.retrieve(input=st.session_state['history'].history)
            self.add_message(assistant_response)
            
            return assistant_response
