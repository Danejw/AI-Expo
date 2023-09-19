import os
import PyPDF2
from dotenv import load_dotenv
import streamlit as st
import openai

# Set up OpenAI API credentials
# Load .env file
env = load_dotenv('.env')

# Retrieve API key
API_KEY = os.getenv("OPENAI_API_KEY")

# Check if the API key is loaded correctly
if not API_KEY:
    raise ValueError("API Key not found!")

openai.api_key = API_KEY


def main():
    st.title("PDF Information Extractor")
    file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if file is not None:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)

        extracted_text = ""
        for page in range(num_pages):
            page_obj = pdf_reader.pages[page]
            extracted_text += page_obj.extract_text()

        # Split the extracted text into sections
        sections = split_text_into_sections(extracted_text)

        # Display the extracted information
        st.subheader("Extracted Information")
        st.text(extracted_text)

        # Display the split sections
        st.subheader("Split Sections")
        for i, section in enumerate(sections):
            st.text(f"Section {i+1}:")
            st.text(section)
            st.text("")

def split_text_into_sections(text, section_length=1000):
    sections = []
    words = text.split()
    current_section = ""
    for word in words:
        if len(current_section) + len(word) <= section_length:
            current_section += word + " "
        else:
            sections.append(current_section.strip())
            current_section = word + " "
    if current_section:
        sections.append(current_section.strip())
    return sections

if __name__ == "__main__":
    main()