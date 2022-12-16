import json
import os
import itertools

source_directory = './JSONFiles_withID/'
# all_files is a directory containing all json files
all_files = os.listdir(source_directory)


# input ids from the user
input_ids = {"4079", "4430"}
temp_ids = input_ids
item_values = {}

# function gives (key, value) dict:item_values which contains id as key and list of preprocessed values as value
def preprocess_items():
    global input_ids
    global item_values

    temp_list = []
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
                        if attr.find("Warranty") != -1 or attr.find("warranty") != -1:
                            continue
                        elif data[id][attr].isnumeric():
                            continue
                        elif data[id][attr] == "no" or data[id][attr] == "No":
                            continue
                        elif(data[id][attr] == "Yes" or data[id][attr] == "yes"):
                            temp_list.append(attr)
                        else :
                            temp_list.append(data[id][attr])

                    # adding (id, list) to item_values
                    item_values[id] = temp_list
                    temp_list = []

    for id in item_values:
        for value in item_values[id]:
            # if value is a list get each list values and append to list and remove that value
            if ',' in value:
                temp = value.split(',')
                item_values[id].remove(value)
                item_values[id].extend(temp)

        i = 0
        while i < len(item_values[id]):
            item_values[id][i] = item_values[id][i].replace("-", " ")
            i = i+1


search_terms = []

# this function gives search_terms in the search_terms list
def create_searchterms():
    global search_terms
    search_items = []
    sets = []
    for id in item_values:
        search_items.append(item_values[id])
    
    for i in range(len(search_items)):
        sets.append(i)
    sets = list(itertools.combinations(sets, 2))
    print(sets)
    
    for i in range(len(sets)):
        print(">>>>>>>>>>>>>>>>>>")
        print(len(search_items[sets[i][0]]))
        print(len(search_items[sets[i][1]]))
        for j in range(len(search_items[sets[i][0]])):   # replace with n to get less terms
            for k in range(len(search_items[sets[i][1]])):  # replace with n to get less terms
                search_terms.append(
                    search_items[sets[i][0]][j] + " AND " + search_items[sets[i][1]][k])




preprocess_items()
for i in item_values:
    print("\n>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(i)
    print(item_values[i])

create_searchterms()
print("The search terms are : ")
# for i in range(len(search_terms)):
#     print(search_terms[i])
print(len(search_terms))