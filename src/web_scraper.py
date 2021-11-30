import logging, sys
import time
import requests
from pyquery import PyQuery as pq

class WebScraper:
    LOG = logging.getLogger(__name__)

    def __init__(self, test=False):
        self.test = test

    def get_search_results(self, flair, handler):
        next_url = f"https://old.reddit.com/r/Superstonk/search?q=flair_name%3A%22{flair}%22&restrict_sr=on&include_over_18=on&sort=new&t=all"

        while next_url is not None:
            print(f"Scraping {next_url}")
            d = pq(next_url, headers={'user-agent': 'testscraper by halfdane'})
            for url in d('.search-result-header a'):
                handler(url.attrib['href'])

            next_page_element = d('a[rel="nofollow next"]')

            if (len(next_page_element) > 0):
                next_url = next_page_element[0].attrib['href']
            else:
                next_url = None

            time.sleep(2)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    webscraper = WebScraper()
    webscraper.get_search_results("Possible%20DD%20%F0%9F%91%A8%E2%80%8D%F0%9F%94%AC",
        lambda x: print(x))

