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
from logger import Logger


fetched_content = {}
weights = {}
data_file = 'intermediates/data.json'


def remove_punctuation(text):
    translator = str.maketrans("", "", string.punctuation)
    return text.translate(translator)


def fetch_data():
    global fetched_content
    with open(data_file, "r") as data_f:
        fetched_content = json.load(data_f)


selected_words = []


def match_co_occurrence(t1, t2, to_match):
    co_regex = r"(\b" + t1 + r")\s?&?-?/?(\b or \b)?(\b and \b)?(" + t2 + \
        r"\b)" + r"|" + r"(\b" + t2 + r")\s?&?-?/?(\b or \b)?(\b and \b)?(" + t1 + \
        r"\b)"
    return re.match(co_regex, to_match, re.IGNORECASE)
