from abc import ABC, abstractmethod
import csv
from enum import Enum
import os
from typing import Any, List
from dotenv import load_dotenv
from langchain.schema import Document
from langchain.callbacks.manager import Callbacks

import openai

from langchain.chains import RetrievalQA
from langchain.embeddings import OpenAIEmbeddings


from langchain.document_loaders import CSVLoader, TextLoader, WebBaseLoader, PyPDFLoader, GoogleDriveLoader, DirectoryLoader
import pandas as pd
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter


from models.ChatMessage import ChatMessage

import streamlit as st


# # Load .env file
# env = load_dotenv('.env')

# # Retrieve API key
# API_KEY = os.getenv("OPENAI_API_KEY")
# #API_KEY = st.secrets("MY_OPENAI_API_KEY")

# # Check if the API key is loaded correctly
# if not API_KEY:
#     raise ValueError("API Key not found!")

# openai.api_key = API_KEY

if "openai_apikey" in st.session_state:
        openai.api_key = st.session_state.openai_apikey


class FileType(Enum):
    csv = 1
    pdf = 2
    txt = 3

class Retriever():
    def __init__(self, file_path:str=None, k:int = 5):
        self.vectorstore = Chroma()
        self.embeddings_model = OpenAIEmbeddings(openai_api_key=st.session_state.openai_apikey)
        self.file_path = file_path
        self.k = k
        self.persist_directory = "data/vectorstore" + "_" + f"{self.file_path}"
    
    def load_csv(self, csv_file: str, column_name=None) -> list[str]:

        with open(csv_file) as f:
            rows = list(csv.reader(f))

        if column_name:
            header = rows[0]
            col_index = header.index(column_name)  
            data = [row[col_index] for row in rows[1:]]

        else:
            data = [item for sublist in rows for item in sublist]

        texts = [str(item) for item in data]

        return texts
           
    # load pdf
    def load_pdf(self, pdf_file: str) -> list[Document]:
        loader = PyPDFLoader(pdf_file)
        pages = loader.load()
        return pages
          
    # load txt
    def load_txt(self, txt_file: str) -> list[Document]:
        loader = TextLoader(txt_file, encoding="utf-8")
        pages = loader.load()
        return pages
    
    def load_web(self, url: str) -> list[Document]:
        loader = WebBaseLoader(url)
        pages = loader.load()
        return pages
    
    # TODO: Test this!
    # load googe drive
    def load_google_drive(self, folder_id: str) -> list[Document]:
        loader = GoogleDriveLoader(folder_id=folder_id)
        pages = loader.load()
        return pages
    
    # TODO: Test this
    # load directory       
    def load_directory(self, directory: str, extensions: str) -> list[Document]:
        loader = DirectoryLoader(directory, extensions)
        pages = loader.load()
        return pages
    
    def parse_filepath_to_filetype(self, file_path: str) -> FileType:
        extension = os.path.splitext(file_path)[1]
        if extension == '.csv':
            return FileType.csv
        elif extension == '.pdf':
            return FileType.pdf
        elif extension == '.txt':
            return FileType.txt
        else:
            raise ValueError(f"Unsupported file type: {extension}")
    
    def load_file_and_split(self, file_path: str) -> list[Document]:
        file_type = self.parse_filepath_to_filetype(file_path)
        
        split = []
        if (file_type == FileType.csv):
            # Load the CSV file              
            content = self.load_csv(csv_file=file_path, column_name='Body')     
            # split text
            split = self.split_text_into_documents(content)
            
        elif (file_type == FileType.pdf):
            # Load the PDF file
            content = self.load_pdf(pdf_file=file_path)
            
            # split doucments
            split = self.split_documents(content)
            
        elif (file_type == FileType.txt):
            # Load the TXT file
            content = self.load_txt(txt_file=file_path)
            
            # split doucments
            split = self.split_documents(content)
        
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        return split
    
    def split_text_into_documents(self, documents: list[str]) -> list[Document]:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, separators="\n\n")
        
        documents = text_splitter.create_documents(documents)       

        split = text_splitter.split_documents(documents)
         
        return split
    
    def split_documents(self, documents: list[Document]) -> list[Document]:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, separators="\n\n")   

        split = text_splitter.split_documents(documents)
         
        return split
    
    def persist_vectorstore(self, documents: list[Document], persist_directory: str) -> Chroma:
        db = self.vectorstore.from_documents(documents=documents, embedding=self.embeddings_model, persist_directory=persist_directory)
        db.persist()
        return db
        
    def load_from_persisted_vectorstore(self) -> Chroma:
        db = Chroma(persist_directory=self.persist_directory, embedding_function=self.embeddings_model)
        return db
    
    def run(self, query:str) -> ChatMessage:
        # if the vector store path does not exist, create the vectorstore and persist it
        if os.path.exists(self.persist_directory):
            # load vectore store
            db = self.load_from_persisted_vectorstore()       
        else:
            split = self.load_file_and_split(self.file_path)   
            db = self.persist_vectorstore(split, self.persist_directory)  
        
        # Query the vectorstore
        results = db.similarity_search_with_relevance_scores(query, k=self.k)
         
        print(len(results))
        
        placeholder = ""
        for r in results:
            doc, score = r
            print(doc.page_content)
            print(score)
            if score > 0.5:
                placeholder += doc.page_content + "\n\n"
            
        #print(placeholder)
        
        chatmessage_result = ChatMessage(name="Retriever", content=placeholder, role="assistant", cost=0)
        
        # print ("Answer")
        # print (chatmessage_result.content)
        
        return chatmessage_result
    
    
