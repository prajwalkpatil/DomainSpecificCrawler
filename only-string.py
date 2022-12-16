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
input_ids = {"4082", "4430", "4000"}
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

        # remove Yes, No, yes and no
        try:
            item_values[id].remove('Yes')
        except:
            pass
        try:
            item_values[id].remove('yes')
        except:
            pass
        try:
            item_values[id].remove('No')
        except:
            pass
        try:
            item_values[id].remove('no')
        except:
            pass           
        # remove if the value is only numeric
        if value.isnumeric():
            item_values[id].remove(value)

    i = 0
    while i < len(item_values[id]):
        item_values[id][i] = item_values[id][i].replace("-", " ")
        i = i+1

# Selecting n random words from each id list and appending to search_items list
n = 4        # n random words are selected from each list
search_items = []
for id in item_values:
    # temp_list = random.sample(item_values[id], n)  # to get less combinations for testing
    
    print(len(item_values[id]))
    print(">>>>>>>>>>>>>>>>>>>>>>>>")
    # temp_list = random.sample(item_values[id], len(item_values[id]))
    # search_items.append(temp_list)
    search_items.append(item_values[id])

# print(search_items)
# print('\n')

search_terms = []
sets = []

for i in range(len(search_items)):
    sets.append(i)

sets = findsubsets(sets, 2)
print(sets)

for i in range(len(sets)):
    print(">>>>>>>>>>>>>>>>>>")
    print(len(search_items[sets[i][0]]))
    print(len(search_items[sets[i][1]]))
    for j in range(len(search_items[sets[i][0]])):   # replace with n to get less terms
        for k in range(len(search_items[sets[i][1]])):  # replace with n to get less terms
            search_terms.append(
                search_items[sets[i][0]][j] + " AND " + search_items[sets[i][1]][k])

print("The search terms are : ")
# for i in range(len(search_terms)):
#     print(search_terms[i])
print(len(search_terms))


# import re
# import requests
# from bs4 import BeautifulSoup

# duckDuckUrl = 'https://html.duckduckgo.com/html/'
# payload = {'q': ''}
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:84.0) Gecko/20100101 Firefox/84.0'}


# for l in search_terms:
#     payload['q'] = l
#     res = requests.post(duckDuckUrl, data=payload, headers=headers)
#     soup = BeautifulSoup(res.text, 'html.parser')
#     link_elements = soup.findAll('a')

#     link_set = set()

#     for i in link_elements:
#         link = i.get("href")
#         if(re.match(r"http\S*", str(link))):
#             link_set.add(link)
#             append_to_dictionary(link)

#     for i in link_set:
#         print(">> ", i)


# # print(">>>>>>>>>>>>>>")
# # print(link_dictionary)
# # print(">>>>>>>>>>>>>>")
# sorted_links = sorted(link_dictionary.items(),
#                       key=lambda x: x[1], reverse=True)
# # print(">>>>>>>>>>>>>>")
# # print(sorted_links)
# # print(">>>>>>>>>>>>>>")

# print("The seed URL will be - ")
# print(sorted_links[0][0])
# print("Number of occurences- ")
# print(sorted_links[0][1])
