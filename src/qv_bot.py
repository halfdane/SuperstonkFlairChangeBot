import logging
import os
import threading
import time
import datetime

import praw

qv_text = f"""**IMPORTANT POST LINKS**

[What is GME and why should you consider investing?](https://www.reddit.com/r/Superstonk/comments/qig65g/welcome_rall_looking_to_catch_up_on_the_gme_saga/) || 
[What is DRS and why should you care?](https://www.reddit.com/r/Superstonk/comments/ptvaka/when_you_wish_upon_a_star_a_complete_guide_to/) || 
[do you have low karma but still want to feed the DRS bot? Post on r/gmeorphans here](https://www.reddit.com/r/GMEOrphans/comments/qlvour/welcome_to_gmeorphans_read_this_post/)

[This is a temporary replacement until the regular QualityVoteBot's ban is revoked.](https://www.reddit.com/r/QualityVote/comments/sqd6kj/uqualityvote_is_currently_suspended_from_reddit/)

------------------------------------------------------------------------

Please help us determine if this post deserves a place on /r/Superstonk. 
[Learn more about this bot and why we are using it here]
(https://www.reddit.com/r/Superstonk/comments/poa6zy/introducing_uqualityvote_bot_a_democratic_tool_to/)

If this post deserves a place on /r/Superstonk, **UPVOTE** this comment!!

If this post should not be here or or is a repost, **DOWNVOTE** This comment!"""

flair_text_to_ignore = \
    ("Community",
     "Daily",
     "Debunked",
     "Partial Debunk",
     "Inconclusive",
     "Misleading Title",
     "Pending Review",
     "AMA",
     "Due Diligence",
     "Possible DD"
     )


def find_new_flair(flair_content):
    for flair in subreddit.flair.link_templates:
        if flair_content in flair['text']:
            return flair['id']


def has_stickied_comment(submission):
    return len(submission.comments) > 0 and submission.comments[0].stickied


def add_comment_to_every_post():
    for submission in subreddit.stream.submissions():
        if not has_stickied_comment(submission) and submission.link_flair_template_id not in flair_ids_to_ignore:
            logging.debug(f"https://www.reddit.com{submission.permalink}")
            sticky = submission.reply(qv_text)
            sticky.mod.distinguish(how="yes", sticky=True)
        else:
            logging.debug(f"Ignoring https://www.reddit.com{submission.permalink}")


def check_existing_comments():
    while True:
        for comment in reddit.user.me().comments.new(limit=None):
            if "**IMPORTANT POST LINKS**" in comment.body and comment.score < 0:
                print(f"{comment.score} for https://www.reddit.com{comment.parent().permalink}")
        print(f"starting to sleep for ten minutes at {datetime.datetime.now()}")
        time.sleep(360)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    reddit = praw.Reddit(username=os.environ["reddit_username"],
                         password=os.environ["reddit_password"],
                         client_id=os.environ["reddit_client_id"],
                         client_secret=os.environ["reddit_client_secret"],
                         user_agent="desktop:com.halfdane.superstonk_qvbot:v0.0.1 (by u/half_dane)")

    reddit.validate_on_submit = True
    subreddit = reddit.subreddit(os.environ["target_subreddit"])
    logging.info(f'working in {subreddit.display_name} as {reddit.user.me()}')

    flair_ids_to_ignore = [find_new_flair(f) for f in flair_text_to_ignore]

    commenter = threading.Thread(target=add_comment_to_every_post)
    commenter.start()

    checker = threading.Thread(target=check_existing_comments())
    checker.start()

