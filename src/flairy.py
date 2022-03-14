import logging
import re
import praw
import os

flairy_detection = "!flairy!"

flairy_detect_user_flair_change = \
    re.compile(r".*!\s*FLAIRY\s*!(.*?)(?:(red|blue|pink|yellow|green|black))?\s*$",
               re.IGNORECASE | re.MULTILINE | re.DOTALL)

templates = {"red": "0446bc04-91c0-11ec-8118-ce042afdde96",
             "blue": "6e40ab4c-f3cd-11eb-889e-ae4cdf00ff3b",
             "pink": "6de5f58e-f3ce-11eb-af43-eae78a59944d",
             "yellow": "5f91a294-f3ce-11eb-948b-d26e0741292d",
             "green": "7dfd44fe-f3ce-11eb-a228-aaac7809dc68",
             "black": "8abdf72e-f3ce-11eb-b3e3-22147bc43b70"}

default_color = "black"


def check_templates():
    subreddit_templates = map(lambda x: x['id'], subreddit.flair.templates)
    for color in templates:
        assert templates[color] in subreddit_templates, f"no subreddit_template for {color} found"


def watch_me(flairy_user):
    assert flairy_user in subreddit.moderator(), f"{flairy_user} isn't a subreddit moderator"

    for comment in subreddit.stream.comments(skip_existing=True):
        if flairy_detection.lower() in comment.body.lower() and comment.author == flairy_user:
            user_to_be_flaired = comment.parent().author
            if user_to_be_flaired != flairy_user:
                flairy = flairy_detect_user_flair_change.match(comment.body)
                if flairy:
                    flair_user(comment, user_to_be_flaired, flairy.group(1), flairy.group(2))


def flair_user(comment, user_to_be_flaired, flair_match, color_match):
    flair_text = flair_match.strip()
    color = (color_match or default_color).lower().strip()
    if color not in templates.keys():
        message = f"Cowardly refusing to use [{color}] as a color!"
        log_message = f"Wrong color [{color}]: not changing {user_to_be_flaired}'s flair"
    elif len(flair_text) > 63:
        message = f"(ノಠ益ಠ)ノ彡┻━┻ THE FLAIR TEXT IS TOO LONG!"
        log_message = f"Too long: Not changing {user_to_be_flaired}'s flair to [{flair_text}]"
    else:
        template = templates[color]
        previous_flair = next(subreddit.flair(user_to_be_flaired))
        log_message = f"[{previous_flair['flair_text']}] => [{flair_text}]"
        subreddit.flair.set(redditor=user_to_be_flaired, text=flair_text, flair_template_id=template)
        message = rf"(✿\^‿\^)━☆ﾟ.*･｡ﾟ `{flair_text}` >!Used to be `{previous_flair['flair_text']}`!<"
        comment.parent().upvote()
    logging.info(log_message)
    comment.edit(message)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    reddit = praw.Reddit(username=os.environ["reddit_username"],
                         password=os.environ["reddit_password"],
                         client_id=os.environ["reddit_client_id"],
                         client_secret=os.environ["reddit_client_secret"],
                         user_agent="desktop:com.halfdane.superstonk_flairy:v0.0.5r (by u/half_dane)")

    reddit.validate_on_submit = True
    subreddit = reddit.subreddit(os.environ["target_subreddit"])
    logging.info(f'working in {subreddit.display_name} as {reddit.user.me()}')

    check_templates()

    while True:
        try:
            watch_me(reddit.user.me())
        except Exception as e:
            logging.error(e)

