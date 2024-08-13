import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urlunparse
from collections import deque

root_url = '' # Enter the root URL to start crawling
allowed_urls = [] # Enter the allowed URLs to crawl (aka whitelist)
blocked_urls = [] # Enter the blocked URLs to avoid crawling (aka blacklist)
folder_path = 'scraped_pages' # Do not modify

def normalize_url(url):
    """Normalize a URL by removing parameters and fragment identifiers."""
    parsed_url = urlparse(url)
    # Reconstruct the URL without parameters (query) and fragment
    normalized_url = urlunparse(parsed_url._replace(query="", fragment=""))
    return normalized_url

def is_valid_url(url, allowed_urls, blocked_urls):
    """Check if the URL is valid and allowed, and not blocked."""
    for blocked_url in blocked_urls:
        if blocked_url in url:
            return False
    return any(url.startswith(allowed_url) for allowed_url in allowed_urls)

def get_abs_url(url, base_url):
    """Convert relative URL to absolute URL based on the base URL."""
    if url.startswith("http"):
        return url
    return urljoin(base_url, url)

def save_page_content(url, folder_path):
    """Scrape the page content and save it into a file."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text()

        # Define the filename based on the URL to avoid overwriting
        filename = normalize_url(url).replace("https://", "").replace("http://", "").replace("/", "_").rstrip("_") + ".txt"
        filepath = os.path.join(folder_path, filename)
        
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(text)
        print(f"Saved: {url}")
    except Exception as e:
        print(f"Error scraping {url}: {e}")

def scrape_urls(start_url, allowed_urls, blocked_urls, folder_path):
    """Recursively crawl the website starting from the start_url."""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    queue = deque([start_url])
    seen = set([normalize_url(start_url)])
    base_url = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(start_url))

    while queue:
        current_url = queue.popleft()
        print(f"Crawling: {current_url}")
        try:
            response = requests.get(current_url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")
            save_page_content(current_url, folder_path)  # Scrape and save the content of the current page

            for link in soup.find_all("a", href=True):
                abs_url = normalize_url(get_abs_url(link['href'], base_url))
                if abs_url not in seen and is_valid_url(abs_url, allowed_urls, blocked_urls):
                    queue.append(abs_url)
                    seen.add(abs_url)
                    print(f"Added to queue: {abs_url}")
                else:
                    print(f"Skipped invalid/disallowed/duplicate URL: {abs_url}")

        except Exception as e:
            print(f"Failed to process {current_url}: {e}")

# Start the scraping process
scrape_urls(root_url, allowed_urls, blocked_urls, folder_path)