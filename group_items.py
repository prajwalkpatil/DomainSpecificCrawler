import json
import os
source_directory = './JSONPerson/';
all_files = os.listdir(source_directory)

json_array = []

for file in all_files:
    with open(f"{source_directory}/{file}",'r') as f:
        data = json.load(f)
        json_array.append(data)

with open("persons.json", "w") as outfile:
    json.dump(json_array, outfile)