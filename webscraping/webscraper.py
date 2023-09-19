import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import csv

def sanitize_filename(filename):
    # Remove invalid characters from the filename
    return "".join(c if c.isalnum() or c in ['-', '_'] else '_' for c in filename)

def scrape_website(url):
    # Fetch webpage content
    response = requests.get(url)
    if response.status_code == 200:
        webpage_content = response.text
    else:
        print("Failed to fetch webpage.")
        return

    # Extract header and paragraph content
    soup = BeautifulSoup(webpage_content, 'html.parser')
    header = soup.find('title').get_text()  # Assuming the title tag contains the header
    paragraphs = [p.get_text() for p in soup.find_all('p')]
    body = soup.body.get_text()

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

if __name__ == "__main__":
    # Get the URL from the user
    website_url = input("Enter the URL of the website to scrape: ")
    
    # Call the scraping function
    scrape_website(website_url)
