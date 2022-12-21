import json
import os
import re
from bs4 import BeautifulSoup
import string
import nltk
from datetime import datetime
from collections import Counter
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from logger import Logger
stopWords = set(stopwords.words('english'))


fetched_content = {}
fetched_items = {}
weights = {}
data_file = 'intermediates/data.json'
items_file = 'intermediates/items.json'


def fetch_data():
    global fetched_content
    global fetched_items
    with open(data_file, "r") as data_f:
        fetched_content = json.load(data_f)
    with open(items_file, "r") as items_f:
        fetched_items = json.load(items_f)


selected_words = []


def process_link_content():
    for link in fetched_content:
        temp_data = fetched_content[link]
        words = word_tokenize(*temp_data)
        selected_words = []
        for w in words:
            if w not in stopWords:
                selected_words.append(w)
        fetched_content[link] = (" ").join(selected_words)
    Logger.write_info("Text from links processed.")


def remove_punctuation(text):
    translator = str.maketrans("", "", string.punctuation)
    return text.translate(translator)


def get_co_occurrence_count(t1, t2, to_match):
    co_regex = r"(\b" + t1 + r")\s?(\s*&\s*)?(\s*-\s*)?(\s*/\s*)?(\b or \b)?(\b and \b)?(" + t2 + \
        r"\b)" + r"|" + r"(\b" + t2 + r")\s?(\s*&\s*)?(\s*-\s*)?(\s*/\s*)?(\b or \b)?(\b and \b)?(" + t1 + \
        r"\b)"
    return len(re.findall(co_regex, to_match, re.IGNORECASE))


def get_occurrence_count(t1, to_match):
    if re.match(r" ?yes ?| ?no ?", t1, re.IGNORECASE):
        return 0
    match_regex = r".?" + t1 + r".?"
    return len(re.findall(match_regex, to_match, re.IGNORECASE))


if __name__ == "__main__":
    fetch_data()
    process_link_content()
    print(get_co_occurrence_count("A", "B", "A or B A or B B & A"))
    print(get_occurrence_count("yes", "A or  yes B A "))
