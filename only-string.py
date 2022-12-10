import json
import os
import random
import itertools
import requests
import json
import lxml
from bs4 import BeautifulSoup

headers = {
    'User-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
}

params = {
    'q': 'Google doodle',  # query
    'gl': 'us',    # country to search from
    'hl': 'en',     # language
}


def findsubsets(s, n):
    return list(itertools.combinations(s, n))


source_directory = './JSONFiles_withID/'
# all_files is a directory containing all json files
all_files = os.listdir(source_directory)

# input ids from the user
input_ids = {"5761", "5308"}
temp_ids = input_ids
item_values = {}
temp_list = []

link_dictionary = {}


def append_to_dictionary(l):
    global link_dictionary
    if l not in link_dictionary:
        link_dictionary[l] = 1
    else:
        link_dictionary[l] += 1


# file is each .json files
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
                # data[id] is each attr-value pair
                for attr in data[id].keys():
                    # data[id][attr] will give the value of each attribute

                    # appending all values into list
                    temp_list.append(data[id][attr])
                # adding (id, list) to item_values
                item_values[id] = temp_list
                temp_list = []


# purifying list
for id in item_values:
    for value in item_values[id]:
        # if value is a list get each list values and append to list and remove that value
        if ',' in value:
            temp = value.split(',')
            item_values[id].remove(value)
            item_values[id].extend(temp)
        # remove yes and nos
        if value == 'Yes' or value == 'yes' or value == 'No' or value == 'no':
            item_values[id].remove(value)
        # remove if the value is only numeric
        if value.isnumeric():
            item_values[id].remove(value)

    i = 0
    while i < len(item_values[id]):
        item_values[id][i] = item_values[id][i].replace("-", " ")
        i = i+1

# Selecting n random words from each id list and appending to search_items list
n = 3        # n random words are selected from each list
search_items = []
for id in item_values:
    temp_list = random.sample(item_values[id], n)
    search_items.append(temp_list)
print(search_items)
print('\n')

search_terms = []
sets = []

for i in range(len(search_items)):
    sets.append(i)

sets = findsubsets(sets, 2)  # change number to get more terms

for i in range(len(sets)):
    for j in range(n):
        for k in range(n):
            search_terms.append(
                search_items[sets[i][0]][j] + " AND " + search_items[sets[i][1]][k])

print("The search terms are : ")
for i in range(len(search_terms)):
    print(search_terms[i])


page_range = []
no_of_pages = 1
for i in range(0, no_of_pages):
    page_range.append(i * 5)

all_links = []
for term in search_terms:
    for i in page_range:
        params['start'] = i
        params['q'] = term
        html = requests.get("https://www.google.com/search",
                            headers=headers, params=params, timeout=20)
        soup = BeautifulSoup(html.text, 'lxml')
        for result in soup.select('.tF2Cxc'):
            link = result.select_one('.yuRUbf a')['href']
            # print(link)
            all_links.append(link)
            append_to_dictionary(link)

print(">>>>>>>>>>>>>>")
print(link_dictionary)
print(">>>>>>>>>>>>>>")
sorted_links = sorted(link_dictionary.items(),
                      key=lambda x: x[1], reverse=True)
print(">>>>>>>>>>>>>>")
print(sorted_links)
print(">>>>>>>>>>>>>>")


print("The seed URL will be - ")
print(sorted_links[0][0])
print("Number of occurences- ")
print(sorted_links[0][1])
