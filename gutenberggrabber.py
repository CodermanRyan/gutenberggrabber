#Made in collaboration with ChatGPT and Ryan Christie

import os
import requests
from bs4 import BeautifulSoup
import re

# Function to download a book in .epub format
def download_epub(book_id, book_title):
    epub_url = f"https://www.gutenberg.org/ebooks/{book_id}.epub3.images"

    # Create the 'C:\ebooks' folder if it doesn't exist
    ebooks_folder = 'C:\\ebooks'
    os.makedirs(ebooks_folder, exist_ok=True)

    # Define the full path for saving the ebook
    epub_file_path = os.path.join(ebooks_folder, f"{book_title}.epub")

    # Download the .epub file
    epub_response = requests.get(epub_url)

    if epub_response.status_code == 200:
        with open(epub_file_path, 'wb') as file:
            file.write(epub_response.content)

        print(f"'{book_title}' has been downloaded successfully as '{epub_file_path}'.")
    else:
        print(f"'{book_title}' is not available in .epub format for download on Project Gutenberg.")

# Prompt the user for input
user_input = input("Enter the book title you'd like to search for: ")

# Convert user input to lowercase
user_input = user_input.lower()

# URL of the search results page
search_url = f"https://www.gutenberg.org/ebooks/search/?query={user_input}&submit_search=Go%21"

response = requests.get(search_url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all links in the search results
    result_links = soup.find_all('a', href=re.compile(r'/ebooks/\d+'))

    for link in result_links:
        href = link.get('href', '')

        # Extract the book ID from the link
        book_id_match = re.search(r'/(\d+)', href)
        if book_id_match:
            book_id = book_id_match.group(1)

            # Visit the book's specific page to extract the title and download the book
            book_page_url = f"https://www.gutenberg.org/ebooks/{book_id}"
            book_page_response = requests.get(book_page_url)

            if book_page_response.status_code == 200:
                book_page_soup = BeautifulSoup(book_page_response.text, 'html.parser')

                # Debugging: Print book_id
                print(f"Debug: Book ID: {book_id}")

                # Find the direct download link for .epub3.images
                epub_link = book_page_soup.find('a', href=lambda href: href and href.endswith('.epub3.images'))

                if epub_link:
                    epub_url = f"https://www.gutenberg.org{epub_link['href']}"

                    # Extract the book title from the page title
                    title_element = book_page_soup.find('h1', itemprop='name')
                    if title_element:
                        book_title = title_element.text.strip()
                    else:
                        # If title is not found, use a default title
                        book_title = f"Book-{book_id}"

                    # Debugging: Print book_title
                    print(f"Debug: Book Title: {book_title}")

                    # Download the book
                    download_epub(book_id, book_title)

else:
    print(f"Error: Unable to access the search results page: {search_url}")
