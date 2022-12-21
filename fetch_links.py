import os
import re
import json
import random
import itertools
import requests
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen
from logger import Logger
from tqdm.auto import tqdm

useragent_list = []
search_terms = []


def read_useragents():
    global useragent_list
    try:
        with open("data/headers.json", "r") as header_file:
            useragent_list = json.load(header_file)
        Logger.write_info("Headers fetched.")
    except Exception as e:
        Logger.write_error(e)


def get_useragent():
    global useragent_list
    if not useragent_list:
        read_useragents()
    return random.choice(useragent_list)


def findsubsets(s, n):
    return list(itertools.combinations(s, n))


def create_search_terms(n=0):
    global search_terms
    global search_pairs
    item_values = {}
    with open("./intermediates/items_processed.json", "r") as processed_file:
        item_values = json.load(processed_file)
    attributes_pair = list(itertools.combinations(item_values.keys(), 2))
    all_attr_combinations = []
    # -------------- Take a cross product of attributes of each item ------------- #
    for i in attributes_pair:
        P = itertools.product(item_values[i[0]], item_values[i[1]])
        combined_attrs = [p for p in P]
        all_attr_combinations.extend(combined_attrs.copy())
    # --------------------- Removing duplicates from the list -------------------- #
    combinations_set = set(all_attr_combinations)
    all_attr_combinations = list(combinations_set)
    # Select random samples if there's a limit set to the number of search terms
    if n == 0:
        search_pairs = all_attr_combinations
    else:
        # ------------------------- Generate n random samples -------------------- #
        if(n < len(all_attr_combinations)):
            search_pairs = random.sample(all_attr_combinations, n)
        else:
            search_pairs = all_attr_combinations

    # ------------ Generate search terms based on the pairs generated ------------ #
    for search_p in search_pairs:
        if len(search_p[0]) > 2 and len(search_p[1]) > 2:
            term = f"{search_p[0]} AND {search_p[1]}"
            search_terms.append(term)

    # Logger.write_debug("Search terms: " + str(search_terms))


def get_links():
    global search_terms
    duckDuckUrl = 'https://html.duckduckgo.com/html/'
    payload = {'q': ''}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:84.0) Gecko/20100101 Firefox/84.0'}

    link_results = set()
    pbar = tqdm(desc="Fetching URLs: ", total=len(search_terms))
    for item in search_terms:
        payload['q'] = item
        link_elements = []
        while link_elements == []:
            try:
                res = requests.post(duckDuckUrl, data=payload, headers=headers)
            except Exception as e:
                Logger.write_warning(f"For: {item} - {e}")
                Logger.write_critical(f"Too many requests! need to cool down")
                time.sleep(random.randrange(5, 10))
                break
            soup = BeautifulSoup(res.text, 'html.parser')
            link_elements = soup.findAll('a')
            time.sleep(random.randrange(2, 4))
        time.sleep(random.randrange(2, 4))
        for i in link_elements:
            link = i.get("href")
            if(re.match(r"http\S*", str(link)) and not re.match(r"\S*wikipedia\S*", str(link))):
                link_results.add(link)
        pbar.update(1)
    pbar.close()
    link_list = list(link_results)
    Logger.write_info("Links fetched")
    with open("./intermediates/links.json", "w") as links_file:
        json.dump(link_list, links_file)
    Logger.write_info("Links dumped to file")


def fetch_links(limit=0):
    create_search_terms(limit)
    get_links()
