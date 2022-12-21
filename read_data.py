import os
import re
import json
import sys
import itertools
from tqdm.auto import tqdm
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
processed_items = {}
weights = {}
matched_words = {}
data_file = 'intermediates/data.json'
items_file = 'intermediates/items.json'
processed_file = 'intermediates/items_processed.json'


def remove_punctuation(text):
    translator = str.maketrans("", "", string.punctuation)
    return text.translate(translator)


def process_wiki_data(arr):
    reg_ex = r"\(.*\)"
    for i in arr:
        i = remove_punctuation(i)
        i = re.sub(reg_ex, "", i)
        i = i.lower()
    return arr


def fetch_data():
    global fetched_content
    global fetched_items
    global processed_items
    with open(data_file, "r") as data_f:
        fetched_content = json.load(data_f)
    with open(items_file, "r") as items_f:
        fetched_items = json.load(items_f)
    with open(processed_file, "r") as processed_f:
        processed_items = json.load(processed_f)
    items_all = list(processed_items.keys())
    for id in items_all:
        try:
            with open(f"base/{id}.json", "r") as item_FF:
                processed_items[id].extend(
                    process_wiki_data(json.load(item_FF)))
        except:
            continue
    Logger.write_info("Data read from file.")


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


def get_co_occurrence_count(t1, t2, to_match):
    co_regex = r"(\b" + t1 + r")\s?(\s*&\s*)?(\s*-\s*)?(\s*/\s*)?(\b or \b)?(\b and \b)?(" + t2 + \
        r"\b)" + r"|" + r"(\b" + t2 + r")\s?(\s*&\s*)?(\s*-\s*)?(\s*/\s*)?(\b or \b)?(\b and \b)?(" + t1 + \
        r"\b)"
    return len(re.findall(co_regex, to_match, re.IGNORECASE))


def get_occurrence_count(t1, to_match):
    try:
        if re.match(r" ?yes ?| ?no ?", t1, re.IGNORECASE):
            return 0
        match_regex = r"\s" + t1 + r"\s"
        this_string = str(to_match)
        return len(re.findall(match_regex, this_string, re.IGNORECASE))
    except:
        return 0


def assign_weights():
    global weights
    global fetched_content
    global matched_words
    item_ids = fetched_items.keys()
    item_weights = {}
    pbar = tqdm(desc="Comparing data: ", total=len(fetched_content))
    for idx, url in enumerate(fetched_content):
        item_weights[url] = {}
        for i in item_ids:
            item_weights[url][i] = 0
        matched_words[url] = {}
        for i in item_ids:
            matched_words[url][i] = []
        for i in item_ids:
            for search_term in processed_items[i]:
                if len(search_term) > 2:
                    count = get_occurrence_count(
                        search_term, fetched_content[url][0])
                    item_weights[url][i] += count
                    if count > 0:
                        matched_words[url][i].append(search_term)
        pbar.update(1)
    pbar.close()
    print("Comparison done.")
    for url in item_weights:
        w = []
        for i in item_weights[url]:
            w.append(item_weights[url][i])
        w.sort()
        weights[url] = w[0]
    weights = sorted(weights.items(), key=lambda item: item[1], reverse=True)
    Logger.write_info("Weights assigned.")


def print_seed_urls():
    global weights
    Logger.write_debug("URLs with weights:")
    for i in range(0, 10):
        Logger.write_info(f">> {weights[i][0]} - {weights[i][1]}")
    Logger.write_info("Seed URL match:" + str(matched_words[weights[0][0]]))


def read_data():
    fetch_data()
    assign_weights()
    process_link_content()
    print_seed_urls()


if __name__ == "__main__":
    read_data()
