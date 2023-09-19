import json
from typing import List

import openai
from embeddings.retriever import Retriever
from models.ChatMessage import ChatMessage

import os
from dotenv import load_dotenv

from models.ChatModelsInfo import OPEN_AI_CHAT_MODELS
import streamlit as st

# # Load .env file
# env = load_dotenv('.env')

# # Retrieve API key
# #API_KEY = os.getenv("OPENAI_API_KEY")
# API_KEY = st.secrets("OPENAI_API_KEY")

# # Check if the API key is loaded correctly
# if not API_KEY:
#     raise ValueError("API Key not found!")

# openai.api_key = API_KEY

if "openai_apikey" in st.session_state:
        openai.api_key = st.session_state.openai_apikey

    


class BaseModelClass:
    def __init__(self, name: str ="", systemMessage: str = None, retriever: Retriever = None) :
        self.name = name
        self.system_message = ChatMessage(
            role="system",
            name="System",
            content=systemMessage
        )
        
        self.model: str = "gpt-3.5-turbo-0613"
        self.retriever = retriever
        
        # TODO: Summary of the history
            
    def run(self, input: List[ChatMessage]) -> ChatMessage:
        self.history = input
        managed_list = self.manage_messages(input)
        
        # Insert the system message before calling dicts
        managed_list.insert(0, self.system_message)
        
        # Convert ChatMessage objects to dictionaries
        history_dicts = [chat.dict(exclude={"cost"}) for chat in managed_list]
                
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=history_dicts
        )
        
        # Extracting relevant fields directly into ChatMessage
        return ChatMessage(
            role=response["choices"][0]["message"]["role"],
            content=response["choices"][0]["message"]["content"],
            name=self.name,
            cost=self.get_cost(response=response)
        )
          
    async def run_async(self, input: List[ChatMessage]) -> ChatMessage:
        self.history = input
        managed_list = self.manage_messages(input)
        
        # Insert the system message before calling dicts
        managed_list.insert(0, self.system_message)
        
        # Convert ChatMessage objects to dictionaries
        history_dicts = [chat.dict(exclude={"cost"}) for chat in managed_list]
                
        response = await openai.ChatCompletion.acreate(      
            model=self.model,
            messages=history_dicts,
        )
        
        # Extracting relevant fields directly into ChatMessage
        return ChatMessage(
            role=response["choices"][0]["message"]["role"],
            content=response["choices"][0]["message"]["content"],
            name=self.name,
            cost=self.get_cost(response=response)
        )
            
    def run_async_with_key(self, input: List[ChatMessage], api_key: str) -> ChatMessage:
        # Set up the openai api using the provided key
        openai.api_key = api_key        
        # Use the run_async
        return self.run_async(input)
     
    def manage_messages(self, messages: List[ChatMessage]) -> List[ChatMessage]:
        # TODO: Summarize context and add the summary as a ChatMessage before trimming
        
        # If the list of messages exceeds 10, trim it
        if len(messages) > 10:
            messages = messages[-10:]
        return messages
    
    def convert_to_and_from_chat_message(self, message: str) -> str:
        # turn string into ChatMessage
        message: ChatMessage = ChatMessage(role="assistant", name=self.name, content=message)
        
        # run the model and get a response
        response = self.run([message])
        
        # turn ChatMessage into a string
        return response.content

    def get_cost(self, response) -> float:
        model_info = OPEN_AI_CHAT_MODELS[self.model]
        prompt_tokens = response["usage"]["prompt_tokens"]
        completion_tokens = response["usage"]["completion_tokens"]
        return (prompt_tokens * model_info.prompt_token_cost) + (completion_tokens * model_info.completion_token_cost)

    # TODO: Streaming is not working properly the the current ChatMessage Implementation    
    def run_stream(self, input: List[ChatMessage]) -> ChatMessage:
        self.history = input
        managed_list = self.manage_messages(input)
        
        # Insert the system message before calling dicts
        managed_list.insert(0, self.system_message)
        
        # Convert ChatMessage objects to dictionaries
        history_dicts = [chat.dict(exclude={"cost"}) for chat in managed_list]
                
        full_response = ""


        for response in openai.ChatCompletion.create(
            model=self.model,
            messages=history_dicts,
            stream=True
        ):
            full_response += response.choices[0].delta.get("content", "")            
                        
        return ChatMessage(
            role="assistant",
            content=full_response,
            name=self.name,
            #cost=self.get_cost(response=response)
        )   

    def retrieve(self, input:List[ChatMessage]) -> ChatMessage:
        if self.retriever is None:
            response = self.run(input)
            print("Retriever not set")
            return response
        else:
            retrieved = self.retriever.run(input[-1].content)
            
            # this does not include the retrieved results in the history
            retrieval_history = []
            retrieval_history.append(retrieved)
            
            return self.run(input + retrieval_history)
