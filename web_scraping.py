import requests
from bs4 import BeautifulSoup
import pdfkit
import time
import os

def scrape_webpage(url):
    # Send an HTTP GET request to the URL
    # response = requests.get(url)
    response = requests.get(url, timeout=10)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Get all the links from the webpage
        links = soup.find_all("a")
        return links
    
    else:
        print("Failed to fetch the webpage. Status Code:", response.status_code)
        return None

def save_links_to_pdf(url, links, output_file):
    try:
        # Create a string to hold the links
        link_string = ""
        for link in links:
            link_string += f"{link.get('href')}<br>"

        # Use pdfkit to convert the link string to PDF
        pdfkit.from_string(link_string, output_file)
        print("PDF file saved successfully:", output_file)
    except Exception as e:
        print("Error saving PDF:", str(e))

if __name__ == "__main__":
    # Replace this with the URL of the webpage you want to scrape
    urls = """api.fishbowlapp.com/v4/user/providers/auth"""
    http = 'https://'
    data = urls.split("\n")

    # Scrape the webpage content to get the links
    for i, url in enumerate(data):
        page_links = scrape_webpage(http + url)

        if page_links:
            # Get the absolute path to the current directory
            current_dir = os.path.dirname(os.path.abspath(__file__))

            # Specify the relative path to the wkhtmltopdf executable within the current directory
            wkhtmltopdf_path = os.path.join(current_dir, "wkhtmltox-0.12.6-1.msvc2015-win64.exe")

            # Save the links to a PDF file
            output_file = f"links_output{i}.pdf"

            # Convert the links to PDF using pdfkit with the correct configuration
            config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
            save_links_to_pdf(http + url, page_links, output_file)
            time.sleep(2)
