import json
import os 
import numpy as np
import spacy
import en_core_web_sm
#Directory containing all the JSON files
source_directory = './JSONFiles_withID/';

#Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_sm")

all_files = os.listdir(source_directory)

#List that stores IDs of all the items
input_ids = ["2132","3193"]
#List that stores the item dictionaries
items = {}
#List that stores all the attribute names of the items
item_attributes = {} 

similarity_matrix = np.array([])

matrix_header = []
matrix_id = []
num_of_attributes = 0

def get_items():
    temp_ids = input_ids.copy()
    for file in all_files:
        with open(f"{source_directory}/{file}",'r') as f: 
            data = json.load(f)
            for id in input_ids:
                if id in data.keys():
                    items[id] = data[id]
                    temp_ids.remove(id)
    #If item is not found
    if len(temp_ids) != 0:
        print("Items not found: ",*temp_ids)
    for i in items.keys():
        item_attributes[i] = (list(items[i].keys()))

def get_common_attributes():
    item_attributes_set = []
    for i in item_attributes.keys():
        item_attributes_set.append(set(item_attributes[i]))
    common_attributes = set.intersection(*item_attributes_set)
    return common_attributes

def print_common_attributes(common_attributes):
    global items
    for item in items:
        print("*********************************")
        print("Common data = ");
        for j in common_attributes:
            print(items[item][j])
        print("*********************************")

def create_matrix():
    global matrix_header
    global matrix_id
    global similarity_matrix
    global num_of_attributes
    size = 0
    matrix_header = []
    matrix_id = []
    for i in item_attributes.keys():
        size += len(item_attributes[i])
        for attr in item_attributes[i]:
            matrix_header.append(attr.replace("-"," "))
            matrix_id.append(i)
    similarity_matrix = np.zeros((size,size))
    num_of_attributes = size

def fill_matrix():
    global num_of_attributes
    global similarity_matrix
    for i in range(num_of_attributes):
        for j in range(i,num_of_attributes):
            if i != j and matrix_id[i] != matrix_id[j]:
                if(matrix_header[i] == matrix_header[j]):
                    similar_score = 1.0
                else:
                    similar_score = float(nlp(matrix_header[i]).similarity(nlp(matrix_header[j])))
                    print(matrix_header[i],matrix_header[j],", Score: ",similar_score)
                similarity_matrix[i][j] = similar_score
                similarity_matrix[j][i] = similar_score


get_items()
#Get common attributes between the given items
common_attributes = get_common_attributes()
print(common_attributes)
print_common_attributes(common_attributes)
create_matrix()
print(matrix_id)
print(matrix_header)
fill_matrix()
print(similarity_matrix)

similarity_matrix.tofile('similarity_matrix.csv',sep=',',format='%10.5f')

