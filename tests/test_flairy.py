import src.flairy as flairy


def match(string, expected1, expected2):
    m = flairy.flairy_detect_user_flair_change.match(string)

    if expected1:
        assert m.group(1).strip() == expected1

        if expected2:
            assert m.group(2).strip() == expected2
        else:
            assert m.group(2) is None
    else:
        assert m is None


def test_multiline():
    match(">\n      >\n >"
               "!Flairy! king gizzard and the lizard wizard 🚀 "
               "(red)\n    ￼\n    ", "king gizzard and the lizard wizard 🚀", "red")

def test_whitespace_variations():
    match("!Flairy! something ", "something", None)
    match("!Flairy! something", "something", None)
    match("!Flairy!something ", "something", None)
    match("!Flairy!something", "something", None)

    match("!Flairy!  something  (red)  ", "something", "red")
    match("!Flairy!something  (red)  ", "something", "red")
    match("!Flairy!  something(red)  ", "something", "red")
    match("!Flairy!  something  (red)", "something", "red")

    match("!Flairy!something(red)  ", "something", "red")
    match("!Flairy!something  (red)", "something", "red")
    match("!Flairy!something(red)", "something", "red")

    match("!Flairy!  something  ( red )  ", "something", "red")
    match("!Flairy!something  ( red )  ", "something", "red")
    match("!Flairy!  something( red )  ", "something", "red")
    match("!Flairy!  something  ( red )", "something", "red")

    match("!Flairy!something( red )  ", "something", "red")
    match("!Flairy!something  ( red )", "something", "red")
    match("!Flairy!something( red )", "something", "red")


def test_explanation_message():
    assert flairy.explanation_message() == \
        "Respond to this comment with the magic incantation\n\n"\
        "    !FLAIRY!🚀 My Flair Text 🚀\n\n" \
        "Default color is black.  \nControl color by appending **one** of " \
        "`(red)`, `(blue)`, `(pink)`, `(yellow)`, `(green)`, `(black)`"


