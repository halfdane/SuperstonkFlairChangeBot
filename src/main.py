import sys, getopt, os
import logging

from reddit_front import RedditFront
from web_scraper import WebScraper

old_flairs_to_flair_searchterm=[
    ("DD+%F0%9F%91%A8%E2%80%8D%F0%9F%94%AC", "Due Diligence"),
    ("Serious%20DD%20👨%E2%80%8D🔬🔬", "Due Diligence"),
    ("Possible%20DD%20%F0%9F%91%A8%E2%80%8D%F0%9F%94%AC", "Possible DD"),
    ("Discussion", "Discussion / Question"),
    ("Discussion+🦍", "Discussion / Question"),
    ("Question%20❓", "Discussion / Question"),
    ("Question", "Discussion / Question"),
    ("Opinion%20👽", "Speculation / Opinion"),
    ("Education%20👨%E2%80%8D🏫%20%7C%20Data%20🔢", "Education"),
    ("🖥%EF%B8%8F🚽%20Computershare%20🍦💩🪑", "Computershare"),
    ("News%20📰%20%7C%20Media%20📱", "News"),
    ("News%20📰", "News"),
    ("Meme%20🤣", "Meme"),
    ("Meme", "Meme"),
    ("Shitpost 👾", "Shitpost"),
    ("Shitpost", "Shitpost"),
    ("Social Media 📲🦜", "Social Media"),
    ("Fluff ☁", "Hype/ Fluff"),
    ("Fluff", "Hype/ Fluff"),
]

def main(argv):
    test = False
    try:
        opts, args = getopt.getopt(argv, "t")
    except getopt.GetoptError:
        logging.error('main.py [-t testrun]')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-t':
            test = True

    redditFront = RedditFront(test=test)
    web_scraper = WebScraper(test=test)

    for old_flair, flair_searchterm in old_flairs_to_flair_searchterm:
        new_flair = redditFront.find_new_flair(flair_searchterm)
        logging.info(f"New flair {new_flair['text']}")
        logging.info(f"Old flair {old_flair}")

        web_scraper.get_search_results(old_flair, lambda url: redditFront.reflair(url, new_flair))

        if test: break


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main(sys.argv[1:])
