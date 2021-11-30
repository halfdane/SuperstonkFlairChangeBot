import praw
import os
import logging

class RedditFront:
    LOG = logging.getLogger(__name__)

    def __init__(self, test=False):
        user_agent = "desktop:com.halfdane.superstonk_flair_change_bot:v0.0.1 (by u/half_dane)"
        self.LOG.debug("Logging in..")
        self.username=os.environ["reddit_username"]

        self.reddit = praw.Reddit(username=self.username,
                        password=os.environ["reddit_password"],
                        client_id=os.environ["reddit_client_id"],
                        client_secret=os.environ["reddit_client_secret"],
                        user_agent=user_agent)
        self.LOG.info(f"Logged in as {self.reddit.user.me()}")

        self.reddit.validate_on_submit = True
        self.subreddit = self.reddit.subreddit(os.environ["target_subreddit"])
        self.LOG.info(f'working in {self.subreddit.display_name}')

        self.test = test

    def find_new_flair(self, flair_content):
        for flair in self.subreddit.flair.link_templates:
            if (flair_content in flair['text']):
                return flair

    def reflair(self, url, new_flair):
        post = self.reddit.submission(url=url)
        if not self.test:
            post.mod.flair(flair_template_id=new_flair['id'])
        else:
            self.LOG.info(f"reflairing {post.title} to {new_flair['text']}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    reddit_front = RedditFront(test=True)
    reddit_front.find_flair('Education')
