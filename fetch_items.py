import json
import os
import spacy
import en_core_web_sm
#Directory containing all the JSON files
source_directory = './JSONFiles_withID/';

#Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_sm")

all_files = os.listdir(source_directory)

#List that stores IDs of all the items
input_ids = ["1024","2122","2122"]
#List that stores the item dictionaries
items = []
#List that stores all the attribute names of the items
item_attributes = [] 


def get_items():
    for file in all_files:
        with open(f"{source_directory}/{file}",'r') as f: 
            data = json.load(f)
            print(data.keys())
            for id in input_ids:
                if id in data.keys():
                    items.append(data[id])
    if len(input_ids) != len(items):
        print("Items not found")
    for i in items:
        item_attributes.append(list(i.keys()))

def get_common_attributes():
    item_attributes_set = []
    for i in item_attributes:
        item_attributes_set.append(set(i))
    common_attributes = set.intersection(*item_attributes_set)
    return common_attributes

def print_common_attributes(common_attributes):
    global items
    for i,item in enumerate(items):
        print("*********************************")
        print("Common data = ");
        for j in common_attributes:
            print(item[j])
        print("*********************************")


get_items()
#Get common attributes between the given items
common_attributes = get_common_attributes()
with open("sample.json", "w") as outfile:
    json.dump(items, outfile)
print(common_attributes)
print_common_attributes(common_attributes)
print(nlp("Company").similarity(nlp("Brand")))


