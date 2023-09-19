# main.py
import os
from scraper import WebScraper

def main():
    # Get multiple URLs from the user as a comma-separated string
    urls = input("Enter the URLs of the websites to scrape (comma-separated): ").split(',')
    
    
    # Initialize the WebScraper
    scraper = WebScraper()
    
    # Extract links from each URL
    #for url in urls:
    #    scraper.extract_links(url.strip())

    # Scrape each URL and save the content
    # for url in urls:
    #     scraper.extract_content(url.strip())
    
    #scraper.create_dataframe_from_csv("links/Hawaii_links.csv")
    scraper.extract_linktext_body_from_csv("extracted_content.csv")

if __name__ == "__main__":
    main()


# python webscraping/webscraper_app.py