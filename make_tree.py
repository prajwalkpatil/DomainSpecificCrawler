import json
import os 

#Directory containing all the JSON files
source_directory = './JSONFiles_withID/';
all_files = os.listdir(source_directory)

tree = {}
tree_p = {}

def create_tree():
    global tree
    for file in all_files:
        with open(f"{source_directory}/{file}",'r') as f: 
            data = json.load(f)
            for i in data.keys():
                for attribute in data[i].keys():
                    if attribute in tree.keys():
                        tree[attribute].append(i)
                        tree_p[attribute.replace("-"," ").lower()].append(i)
                    else:
                        tree[attribute] = [i]
                        tree_p[attribute.replace("-"," ").lower()] = [i]


create_tree()
with open("./NewJSONfiles/tree.json", "w") as outfile:
    json.dump(tree, outfile)

with open("./NewJSONfiles/tree_p.json", "w") as outfile:
    json.dump(tree_p, outfile)