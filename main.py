# Project: WebCrawler
# Name: Carter Gamary

# Import statements
import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

# Create configuration for logging
logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO
)

# Crawler
class Crawler:

    # Create the lists of urls needed to visit, and those visited
    def __init__(self, urls=[]):
        self.visited=[]
        self.to_visit=urls

    # returns the text of the url
    def download_url(self, url):
        return requests.get(url).text

    # Finds the URLs in the HTML code through their HREF links
    def get_linked_urls(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            path=link.get('href')
            if path and path.startswith('/'):
                path=urljoin(url, path)
            yield path

    # Adds a URL to the list of those needing to visit
    def add_url_to_visit(self, url):
        if url not in self.visited and url not in self.to_visit:
            self.to_visit.append(url)

    # Performs the crawl
    def crawl(self, url):
        html=self.download_url(url)
        for url in self.get_linked_urls(url, html):
            self.add_url_to_visit(url)

    # main run function of the class
    def run(self):
        while self.to_visit:
            url=self.to_visit.pop(0)
            logging.info(f'Crawling: {url}')
            try:
                self.crawl(url)
            except Exception:
                logging.exception(f'Failed to crawl: {url}')
            finally:
                self.visited.append(url)

# Starts the crawl
if __name__ == '__main__':
    Crawler(urls=['https://www.imdb.com/']).run()