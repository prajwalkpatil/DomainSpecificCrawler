import json
import os
import random
import itertools
import requests
import json
import lxml
from bs4 import BeautifulSoup
import time

ids = ["3193", "3269", "1011"]
input_ids = ids.copy()
dict_ids = {}
temp_list = []
item_values = {}

source_directory = './JSONFiles_withID/'
# all_files is a directory containing all json files
all_files = os.listdir(source_directory)


def get_links_dummy(a):
    links = []
    for i in range(0, 10):
        links.append(f"Link{i}_{a[0]}_{a[1]}")
    return links

    # file is each .json files
for file in all_files:
    with open(f"{source_directory}/{file}", 'r') as f:
        # data is complete json file in form of dictionary
        data = json.load(f)
        for id in input_ids:
            if id in data.keys():
                for attr in data[id].keys():
                    temp_list.append(data[id][attr])
                item_values[id] = temp_list
                temp_list = []

if(len(item_values) != len(input_ids)):
    print("Missing items or invalid input ids")

attrs = {
    '1': ['a', 'b', 'c', 'd', 'e'],
    '2': ['p', 'q', 'r', 's', 't'],
    '3': ['v', 'w', 'x', 'y', 'z'],
    '4': ['A', 'B', 'C', 'D', 'E'],
    '5': ['V', 'W', 'X', 'Y', 'Z'],
}

all_ids = itertools.combinations(attrs.keys(), 2)

all_attr_combinations = []
for i in all_ids:
    print(i[0], i[1])
    P = itertools.product(attrs[i[0]], attrs[i[1]])
    combined_attrs = [p for p in P]
    all_attr_combinations.append(combined_attrs.copy())

all_combinations_links = []
for i in all_attr_combinations:
    all_combinations_links.append([])
    for j in i:
        all_combinations_links[-1].extend(get_links_dummy(j))

# print(all_combinations_links)
link_length_list = [*range(0, len(all_combinations_links))]
# print(link_length_list)
all_link_groups = list(itertools.combinations(link_length_list, 2))
# print(all_link_groups)
all_link_intersections = []
for i in all_link_groups:
    all_link_intersections.append(
        list(set(all_combinations_links[i[0]]) & set(all_combinations_links[i[1]])))
print(all_link_intersections)
