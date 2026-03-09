import re


def normalize(text):

    text = text.lower()

    text = re.sub(r"[.!?,]", "", text)

    text = text.replace("ß", "ss")

    return text.strip()