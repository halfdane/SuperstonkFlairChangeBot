import logging
import time
import os

import praw
from pyquery import PyQuery as pq\

old_flairs_to_flair_searchterm=[
    ("DD 👨‍🔬", "Due Diligence"),
    ("Serious DD 👨‍🔬🔬", "Due Diligence"),
    ("Possible DD 👨‍🔬", "Possible DD"),
    ("Discussion", "Discussion / Question"),
    ("Discussion 🦍", "Discussion / Question"),
    ("Question ❓", "Discussion / Question"),
    ("Question", "Discussion / Question"),
    ("Opinion 👽", "Speculation / Opinion"),
    ("Education 👨‍🏫 | Data 🔢", "Education"),
    ("🖥️🚽 Computershare 🍦💩🪑", "Computershare"),
    ("News 📰 | Media 📱", "News"),
    ("News 📰", "News"),
    ("Meme 🤣", "Meme"),
    ("Meme", "Meme"),
    ("Shitpost 👾", "Shitpost"),
    ("Shitpost", "Shitpost"),
    ("Social Media 📲🦜", "Social Media"),
    ("Fluff ☁", "Hype/ Fluff"),
    ("Fluff", "Hype/ Fluff"),
    ("🚀 Moderator 🚀", "Community"),
    ("🙌💎 Red Seal of Stonkiness 💎🙌", "Community"),
    ("⚠ Inconclusive ⚠", "Inconclusive"),
    ("🚨 Debunked 🚨", "Debunked"),

]


def find_new_flair(flair_content):
    for flair in subreddit.flair.link_templates:
        if flair_content in flair['text']:
            return flair


def search_reflair_loop(test, old_flair, new_flair):
    for submission in subreddit.search('flair_name:"{0}"'.format(old_flair), sort='new'):
        reflair_submission(submission, new_flair)
        if test:
            break


def reflair_submission(submission, new_flair):
    if submission.link_flair_text != new_flair['text']:
        logging.info(f"https://www.reddit.com{submission.permalink} {submission.link_flair_text} -> {new_flair['text']}")
        submission.flair.select(new_flair['id'])
    else:
        logging.info(f"SKIPPING https://www.reddit.com{submission.permalink}")


def search_by_webscraping():
    while True:
        logging.info("starting a new cycle")
        for old_flair, flair_searchterm in old_flairs_to_flair_searchterm:
            new_flair = find_new_flair(flair_searchterm)
            d = pq(url=f'https://www.reddit.com/r/Superstonk/?f=flair_name%3A"{old_flair}"')
            for post in d("a[data-click-id='body']").items():
                submission = reddit.submission(url=f"https://www.reddit.com{post.attr['href']}")
                reflair_submission(submission, new_flair)
        logging.info("cycle done")

        time.sleep(600)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    reddit = praw.Reddit(username=os.environ["reddit_username"],
                         password=os.environ["reddit_password"],
                         client_id=os.environ["reddit_client_id"],
                         client_secret=os.environ["reddit_client_secret"],
                         user_agent="desktop:com.halfdane.superstonk_flairy:v0.0.1 (by u/half_dane)")

    reddit.validate_on_submit = True
    subreddit = reddit.subreddit(os.environ["target_subreddit"])
    logging.info(f'working in {subreddit.display_name} as {reddit.user.me()}')

    search_by_webscraping()
