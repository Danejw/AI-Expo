# scraper.py
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import csv
from utils import sanitize_filename

class WebScraper:
    def __init__(self):
        pass

    def fetch_webpage_content(self, url):
        # Fetch webpage content
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to fetch webpage from {url}.")
            return None

    def extract_content(self, webpage_content):
        # Extract header, paragraphs, and body content
        soup = BeautifulSoup(webpage_content, 'html.parser')

        # Check if a title tag exists on the page
        title_tag = soup.find('title')
        header = title_tag.get_text() if title_tag else "No Title Found"  # Provide a default header if no title tag is found

        # Check if there are any <p> tags on the page
        paragraphs = [p.get_text() for p in soup.find_all('p')] if soup.find_all('p') else []

        # Check if a body tag exists on the page
        body_tag = soup.body
        body = body_tag.get_text() if body_tag else "No Body Content Found"  # Provide a default body if no body tag is found

        return header, paragraphs, body

    def scrape_website(self, url):
        webpage_content = self.fetch_webpage_content(url)
        if webpage_content is not None:
            header, paragraphs, body = self.extract_content(webpage_content)
            
            # Generate a filename based on the website's domain and path
            parsed_url = urlparse(url)
            domain_path = parsed_url.netloc + parsed_url.path
            filename = f"text/{sanitize_filename(domain_path)}.csv"

            # Ensure the 'text' folder exists
            if not os.path.exists('text'):
                os.makedirs('text')

            # Write header and paragraphs to the CSV file
            with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(['Header', 'Paragraph'])

                # Write header and paragraphs as rows
                csv_writer.writerow([header, ''])
                for paragraph in paragraphs:
                    csv_writer.writerow(['', paragraph])
                    
                csv_writer.writerow(['', body])

            print(f"Scraped content from {url} and saved as {filename}")

    def extract_links(self, url):
        # Ensure that the provided URL is a valid string
        if not url.startswith('http://') and not url.startswith('https://'):
             print("Invalid URL format. Please provide a valid URL with 'http://' or 'https://'.")
             return

        webpage_content = self.fetch_webpage_content(url)
        if webpage_content is not None:
            soup = BeautifulSoup(webpage_content, 'html.parser')
            
            # Find all anchor (a) tags with an 'href' attribute
            links = soup.find_all('a', href=True)
            
            # Generate a filename based on the website's domain and path
            parsed_url = urlparse(url)
            domain_path = parsed_url.netloc + parsed_url.path
            filename = f"links/{sanitize_filename(domain_path)}_links.csv"

            # Ensure the 'links' folder exists
            if not os.path.exists('links'):
                os.makedirs('links')

            # Write links to the CSV file
            with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(['Link Text', 'Link URL'])

                for link in links:
                    link_text = link.get_text()
                    link_url = urljoin(url, link['href'])
                    csv_writer.writerow([link_text, link_url])

            print(f"Extracted all links from {url} and saved as {filename}")
            
    def create_dataframe_from_csv(self, filename):

        df_extracted_content = pd.DataFrame(columns=['Link Text', 'Header', 'Paragraphs', 'Body'])
        
        link_texts = []
        headers = []
        paragraphs = []
        bodies = []

        df_links = pd.read_csv(filename)

        for index, row in df_links.iterrows():

            link_text = row['Link Text']
            link_url = row['Link URL']

            print(link_text, link_url)

            webpage_content = self.fetch_webpage_content(link_url)

            if webpage_content:
                header, paragraph_list, body = self.extract_content(webpage_content)

            link_texts.append(link_text)
            headers.append(header)
            paragraphs.append(paragraph_list)
            bodies.append(body)

        df = pd.DataFrame({
            'Link Text': link_texts,
            'Header': headers,
            'Paragraphs': paragraphs,
            'Body': bodies
        })
        
        df_extracted_content = pd.concat([df_extracted_content, df], ignore_index=True)

        df_extracted_content.to_csv('extracted_content.csv', index=False)

        return df_extracted_content

    def extract_linktext_body_from_csv(self, filename):
        df_extracted_content = pd.DataFrame(columns=['Link Text', 'Body'])

        # read the original CSV file
        df_links = pd.read_csv(filename)

        # extract the link text and body from each row
        for index, row in df_links.iterrows():
            link_text = row['Link Text']
            body = row['Body']

            # add the link text and body to the new DataFrame
        df_extracted_content = pd.concat([df_extracted_content, pd.DataFrame({'Link Text': [link_text], 'Body': [body]})], ignore_index=True)

        # write the new DataFrame to a CSV file
        df_extracted_content.to_csv("links/text_body.csv", index=False)



