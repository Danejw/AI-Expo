import os
from dotenv import load_dotenv
import streamlit as st
import requests
from bs4 import BeautifulSoup

from urllib.parse import urlparse, urljoin
from collections import deque

import numpy as np
import faiss
from langchain.embeddings import OpenAIEmbeddings
import openai
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS


from prompted_models.BasePromptModel import BaseModelClass
from prompted_models.Summarizer import Summarization
from models.ChatHistory import ChatHistory
from models.ChatMessage import ChatMessage

# Load .env file
env = load_dotenv('.env')

# Retrieve API key
API_KEY = os.getenv("OPENAI_API_KEY")

# Check if the API key is loaded correctly
if not API_KEY:
    raise ValueError("API Key not found!")

openai.api_key = API_KEY



class Scraper(BaseModelClass):
    def __init__(self):
        super().__init__(
            name="Scrape",
            systemMessage="""
                Given a webpages content, summarize it. If there any code examples summarize what it is doing.
                Be concise, informative, and factual with your summary.
                Give a code examples to help explain. If the code example is long, make sure to write the full length of the code.
                Highlight the main points in a list with a descirption of that point.
            """
        )


def crawl_website(url):
    # Initialize a queue to store the URLs to be crawled
    queue = deque()
    queue.append(url)

    # Initialize a set to store the visited URLs
    visited = set()
    visited.add(url)

    # Extract the root domain from the given URL
    root_domain = urlparse(url).netloc

    # Initialize a list to store the crawled content
    crawled_content = []

    # Start crawling
    while queue:
        # Dequeue the next URL to crawl
        current_url = queue.popleft()

        # Send an HTTP GET request to fetch the webpage content
        response = requests.get(current_url)

        # Create a BeautifulSoup object by passing the HTML content and a parser
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the content from the webpage
        content = soup.get_text()

        # Store the content in the list
        crawled_content.append(content)

        # Extract all hyperlinks from the webpage
        hyperlinks = get_hyperlinks(response.text)

        # Filter out hyperlinks that are not part of the root domain
        filtered_hyperlinks = [link for link in hyperlinks if urlparse(link).netloc == root_domain]

        # Enqueue the filtered hyperlinks for further crawling
        for link in filtered_hyperlinks:
            absolute_link = urljoin(current_url, link)
            if absolute_link not in visited:
                queue.append(absolute_link)
                visited.add(absolute_link)

    # Return the crawled content
    return crawled_content

def get_hyperlinks(html):
    soup = BeautifulSoup(html, 'html.parser')
    hyperlinks = [link.get('href') for link in soup.find_all('a')]
    return hyperlinks


def initialize_session_state():
    #if "history" not in st.session_state:
        #st.session_state.history = ChatHistory(history=[])
        
    if "summary" not in st.session_state:
        st.session_state.summary = ""
    
    if "scraper" not in st.session_state:
        st.session_state.scraper = Scraper()
        
    if "db" not in st.session_state:
        st.session_state.db = FAISS


def scrape_website(history, url):
    st.info("Scraping in progress...")

    user_message = ChatMessage(name="User", role="user", content=url)
    history.history.append(user_message)

    crawled_content = crawl_website(url)                
    crawled_content = '\n'.join(crawled_content)

    crawl_message = ChatMessage(name="Crawl", role="assistant", content=crawled_content)
    history.history.append(crawl_message)

    codeScrape = st.session_state.scraper.run(history.history)
    st.session_state.summary = codeScrape.content

    history.history.append(codeScrape)



def clear_history(history):
    history.history.clear()
    if (len(history.history) == 0):
        st.success("History was successfully cleared")




# Streamlit app UI
def main():    
    
    initialize_session_state()
    
    history = ChatHistory(history=[])
    
    
    st.title("Web Scraper App")
    st.write("Enter the URL of the webpage to scrape:")
    url = st.text_input("URL")

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Scrape") and url:
            scrape_website(history, url)

    with col2:
        if st.button("Clear History"):
            clear_history(history)
             
             
    for message in history.history:
        if message.name == 'User' or message.name == 'Scrape':
            st.markdown(message.content)
             
    if st.session_state.summary:
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = text_splitter.split_text(st.session_state.summary)

        st.markdown(docs)

        embeddings = OpenAIEmbeddings()

        st.session_state.db = FAISS.from_texts(docs, embeddings)

        query = st.text_input("Query")

        if st.button("Ask"):
            docs = st.session_state.db.similarity_search(query)
            
            st.markdown(docs[0].page_content)
       

if __name__ == "__main__":
    main()