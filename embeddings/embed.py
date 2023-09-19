

import csv
import os
from dotenv import load_dotenv
import openai
import pandas as pd
from langchain.embeddings import OpenAIEmbeddings

from langchain.document_loaders.csv_loader import CSVLoader
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter


# Load .env file
env = load_dotenv('.env')

# Retrieve API key
API_KEY = os.getenv("OPENAI_API_KEY")

# Check if the API key is loaded correctly
if not API_KEY:
    raise ValueError("API Key not found!")

openai.api_key = API_KEY


class Emdedder():
    def __init__(self):
        self.embeddings_model = OpenAIEmbeddings()

    # TODO: Add a function to load the PDF, TXT, Markdown file

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
           
    def split_documents(self, documents: list[str]) -> list[Document]:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, separators="\n\n")
        
        documents = text_splitter.create_documents(documents)       

        split = text_splitter.split_documents(documents)
         
        return split
    
    def embed_documents(self, documents: list[str]):        
        
        doc_strings = []
        for doc in documents:
            doc_strings.append(doc.page_content)
        
        embeddings = self.embeddings_model.embed_documents(doc_strings)
                
        return embeddings
    
    def save_embeddings(self, embeddings, csv_path: str):
        df = pd.DataFrame(embeddings)
        df.to_csv(f"{csv_path}_embeddings.csv")

    def load_embeddings(self, csv_path: str) -> pd.DataFrame:
        df = pd.read_csv(csv_path)    
        return df
 
    def run(self, csv_path) -> pd.DataFrame:
        # Load the CSV file
        data = self.load_csv(csv_path, column_name="Body")
                
        # Split the documents into chunks
        documents = self.split_documents(data)
                
        print(len(documents))
        
        # Embed the documents
        embeddings = self.embed_documents(documents)    
        
        # Save the embeddings dataframe to a CSV file
        self.save_embeddings(embeddings, csv_path)
        
        # Load the embeddings dataframe from a CSV file
        return self.load_embeddings(csv_path)
    
# python embeddings/embedder_app.py
