import requests
import json
import sys
import os
import nltk
from logger import Logger

items_all = []
item_values = {}
knowledge_base = {}
source_directory = "./data/files_with_id"


def init():
    global knowledge_base
    for i in items_all:
        knowledge_base[i] = []


def get_items():
    global items_all
    global source_directory
    global item_values
    try:
        all_files = os.listdir(source_directory)
        input_ids = items_all.copy()
        temp_list = []
        for file in all_files:
            with open(f"{source_directory}/{file}", 'r') as f:
                # data is complete json file in form of dictionary
                data = json.load(f)
                # each id is an item in json file
                for id in data.keys():
                    # only take ids from input_ids
                    if id in input_ids:
                        # remove read id from list to decrease computations
                        input_ids.remove(id)
                        # adding (id, list) to item_values
                        item_values[id] = data[id]
        Logger.write_info("Items read successfully")
    except Exception as e:
        Logger.write_error(e)
        sys.exit(-1)


def generate(word, id, limit=500):
    # The maximum limit for wikipedia api is 500
    global knowledge_base
    S = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php"
    # Parameters for GET request using Wikipedia's API
    PARAMS = {
        "action": "query",
        "format": "json",
        "titles": word,
        "prop": "links",
        "pllimit": limit
    }
    # Find all the words that link to other wikipedia pages
    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    PAGES = DATA["query"]["pages"]
    for k, v in PAGES.items():
        try:
            for l in v["links"]:
                if(':' not in l["title"]):
                    knowledge_base[id].append(l["title"])
        except:
            continue
    knowledge_base[id] = set(knowledge_base[id])
    knowledge_base[id] = list(knowledge_base[id])


# Function to dump the object containing primary and secondary attributes to a JSON file


def dump_base():
    global knowledge_base
    global item_values
    for i in item_values:
        try:
            with open(f"base/{i}.json", "w") as write_file:
                json.dump(knowledge_base[i], write_file)
        except:
            Logger.write_error("Error in dumping JSON!")


def dump_specific(id):
    global knowledge_base
    global item_values
    try:
        with open(f"base/{id}.json", "w") as write_file:
            json.dump(knowledge_base[id], write_file)
        Logger.write_info(f"Item {id} WiKi data written to JSON!")
    except:
        Logger.write_error("Error in dumping JSON!")


def process_string(given_string):
    given_string = given_string.replace("-", " ")
    given_string = given_string.lower()
    return given_string


def process_dict(d):
    temp_index = ''
    temp_dict = ''
    values_array = []
    nouns = []  # empty to array to hold all nouns
    for i in d:
        temp_index = i.replace("-", " ")
        temp_dict = d[i].replace("-", " ")

        sentences = nltk.sent_tokenize(temp_index)  # tokenize sentences
        for sentence in sentences:
            for word, pos in nltk.pos_tag(nltk.word_tokenize(str(sentence))):
                if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS'):
                    nouns.append(word)

        sentences = nltk.sent_tokenize(temp_dict)  # tokenize sentences
        for sentence in sentences:
            for word, pos in nltk.pos_tag(nltk.word_tokenize(str(sentence))):
                if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS'):
                    nouns.append(word)
    return nouns


def get_data():
    global items_all
    for i in items_all:
        item_values[i] = process_dict(item_values[i])


def get_wiki():
    global item_values
    for i in item_values:
        item_values[i] = set(item_values[i])
        item_values[i] = list(item_values[i])
        for j in item_values[i]:
            generate(j, i)
        dump_specific(i)


def fetch_wiki_items():
    init()
    get_items()
    get_data()
    get_wiki()


def fetch_wiki(item_list):
    Logger.write_info("Fetching data from WiKi")
    fetched_ids = os.listdir("./base")
    for idx, i in enumerate(fetched_ids):
        fetched_ids[idx] = i.split(".")[0]
    global items_all
    items_all = item_list.copy()
    for i in fetched_ids:
        if i in items_all:
            items_all.remove(i)
    print(items_all)
    fetch_wiki_items()
    Logger.write_info("Data fetched from WiKi")
