import logging
import re
import praw
import os

flairy_detection = "!flairy"
flairy_explain_command = "!flairy:explain"

flairy_detect_user_flair_change = \
    re.compile(r".*!FLAIRY!([^(]*)(?:\(([^)]*)\).*)?",
               re.IGNORECASE | re.MULTILINE | re.DOTALL)

templates = {"red": "509c1d8c-f3ce-11eb-9fd1-d69d0cd1d5b9",
             "blue": "6e40ab4c-f3cd-11eb-889e-ae4cdf00ff3b",
             "pink": "6de5f58e-f3ce-11eb-af43-eae78a59944d",
             "yellow": "5f91a294-f3ce-11eb-948b-d26e0741292d",
             "green": "7dfd44fe-f3ce-11eb-a228-aaac7809dc68",
             "black": "8abdf72e-f3ce-11eb-b3e3-22147bc43b70"}

default_color = "black"


def check_templates():
    subreddit_templates = map(lambda x: x['id'], subreddit.flair.templates)
    for color in templates:
        logging.info(f'{color} is valid {templates[color] in subreddit_templates}')


def explanation_message():
    colors = ", ".join(map(lambda x: f"`({x})`", templates))
    message = f"Respond to this comment with the magic incantation\n\n" \
              "    !FLAIRY!🚀 My Flair Text 🚀\n\n" \
              f"Default color is {default_color}.  \n" \
              f"Control color by appending **one** of {colors}"
    return message


def watch_me(flairy_user):
    for comment in subreddit.stream.comments(skip_existing=True):
        user_to_be_flaired = comment.parent().author
        if flairy_detection.lower() in comment.body.lower() and comment.author in subreddit.moderator():

            if flairy_explain_command.lower() in comment.body.lower():
                comment.edit(explanation_message())
            elif user_to_be_flaired != flairy_user:
                flairy = flairy_detect_user_flair_change.match(comment.body)
                if flairy:
                    flair_user(comment, user_to_be_flaired, flairy.group(1), flairy.group(2))


def flair_user(comment, user_to_be_flaired, flair_match, color_match):
    flair_text = flair_match.strip()
    color = (color_match or default_color).lower().strip()
    if color not in templates.keys():
        message = f"(ノಠ益ಠ)ノ彡┻━┻ [{color}] ISN'T A VALID COLOR!"
    elif len(flair_text) > 63:
        message = f"(ノಠ益ಠ)ノ彡┻━┻ THE FLAIR TEXT IS TOO LONG!"
    else:
        template = templates[color]
        previous_flair = next(subreddit.flair(user_to_be_flaired))
        log_message = f"changing {user_to_be_flaired}'s flair from [{previous_flair['flair_text']}] " \
                      f"in [{comment.author_flair_background_color}] to [{flair_text}] in [{color}] "
        logging.info(log_message)
        comment.author.message(f"Flair change for {user_to_be_flaired}", log_message, )
        subreddit.flair.set(redditor=user_to_be_flaired, text=flair_text, flair_template_id=template)
        message = rf"(✿\^‿\^)━☆ﾟ.*･｡ﾟ {flair_text}"
        comment.parent().upvote()
    comment.parent().reply(message)
    comment.delete()


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

    check_templates()

    watch_me(reddit.user.me())

