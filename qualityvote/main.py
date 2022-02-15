import logging
import os
import threading
import time
import datetime
import configparser
import praw
from collections import namedtuple
import ast


class QualityVoteBot():
    logger = logging.getLogger(__name__)
    logger_add_comment = logging.getLogger(__name__ + "_add_comments")
    logger_check_votes = logging.getLogger(__name__ + "_check_votes")

    qv_text = f"""**IMPORTANT POST LINKS**

[What is GME and why should you consider investing?](https://www.reddit.com/r/Superstonk/comments/qig65g/welcome_rall_looking_to_catch_up_on_the_gme_saga/) || 
[What is DRS and why should you care?](https://www.reddit.com/r/Superstonk/comments/ptvaka/when_you_wish_upon_a_star_a_complete_guide_to/) || 
[do you have low karma but still want to feed the DRS bot? Post on r/gmeorphans here](https://www.reddit.com/r/GMEOrphans/comments/qlvour/welcome_to_gmeorphans_read_this_post/)

[This is a temporary replacement until the regular QualityVoteBot's ban is revoked.](https://www.reddit.com/r/QualityVote/comments/sqd6kj/uqualityvote_is_currently_suspended_from_reddit/)
(It's a reddit wide ban because in **another** sub the mods used harassing language.)

------------------------------------------------------------------------

Please help us determine if this post deserves a place on /r/Superstonk. 
[Learn more about this bot and why we are using it here](https://www.reddit.com/r/Superstonk/comments/poa6zy/introducing_uqualityvote_bot_a_democratic_tool_to/)

If this post deserves a place on /r/Superstonk, **UPVOTE** this comment!!

If this post should not be here or or is a repost, **DOWNVOTE** This comment!"""

    ignore_flairs = ['7b24752e-85f9-11eb-b3c8-0e861167b641', '37ec242e-984f-11eb-94c6-0e8d0acce789',
                     '443477c2-9859-11eb-93e5-0e7222816149', '70f23bf8-95d6-11eb-a299-0e9b20cb9c43',
                     '02d4a642-a071-11eb-bf5d-0e4876509fbb', '33b1d54c-3445-11ec-953a-ceaf24437904']

    def __init__(self, reddit):
        self.logger.setLevel(logging.DEBUG)
        self.logger_add_comment.setLevel(logging.DEBUG)
        self.logger_check_votes.setLevel(logging.DEBUG)
        self.reddit = reddit
        self.subreddit = reddit.subreddit(os.environ["target_subreddit"])
        self.flair_ids_to_ignore = self.ignore_flairs
        self.logger.debug(f"ignoring flair ids: {self.flair_ids_to_ignore}")

    def run(self):
        commenter = threading.Thread(target=self.add_comment_to_every_post)
        commenter.start()

        checker = threading.Thread(target=self.check_existing_comments)
        checker.start()

    def has_stickied_comment(self, submission):
        return len(submission.comments) > 0 and submission.comments[0].stickied

    def add_comment_to_every_post(self, ):
        while True:
            try:
                for submission in self.subreddit.stream.submissions():
                    if not self.has_stickied_comment(
                            submission) and submission.link_flair_template_id not in self.flair_ids_to_ignore:
                        self.logger_add_comment.debug(f"https://www.reddit.com{submission.permalink}")
                        sticky = submission.reply(self.qv_text)
                        sticky.mod.distinguish(how="yes", sticky=True)
                    else:
                        self.logger_add_comment.debug(f"Ignoring https://www.reddit.com{submission.permalink}")
            except Exception as e:
                self.logger_check_votes.error(e)

            self.logger_check_votes.info(f"starting to sleep for ten minutes at {datetime.datetime.now()}")
            time.sleep(360)

    def is_removed(self, s):
        try:
            author = str(s.author.name)
        except:
            author = '[Deleted]'
        if s.banned_by is not None and author != '[Deleted]':
            return True
        else:
            return False

    def check_existing_comments(self, ):
        while True:
            try:
                for comment in reddit.user.me().comments.new(limit=None):
                    if "**IMPORTANT POST LINKS**" in comment.body \
                            and not self.is_removed(comment.parent()) \
                            and comment.score <= -7:
                        self.logger_check_votes.info(
                            f"{comment.score} for https://www.reddit.com{comment.parent().permalink}")
                        comment.parent().report(f"Score of stickied comment has dropped below threshold of {-7}")
            except Exception as e:
                self.logger_check_votes.error(e)

            self.logger_check_votes.info(f"starting to sleep for ten minutes at {datetime.datetime.now()}")
            time.sleep(360)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    reddit = praw.Reddit(username=os.environ["reddit_username"],
                         password=os.environ["reddit_password"],
                         client_id=os.environ["reddit_client_id"],
                         client_secret=os.environ["reddit_client_secret"],
                         user_agent="desktop:com.halfdane.superstonk_qvbot:v0.0.2 (by u/half_dane)")

    reddit.validate_on_submit = True
    logging.info(f'working as {reddit.user.me()}')

    QualityVoteBot(reddit).run()
