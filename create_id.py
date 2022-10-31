import json
import os
import uuid
all_files = os.listdir('./JSONFiles/')
id = 1000

for file in all_files:      
    with open(f"JSONFiles/{file}",'r') as f:
        data = json.load(f)
    print(f"{file} > JSON read")

    data_with_keys = {}

    def make_key(source_dic):
        global id
        for i in source_dic:
            try:
                del i["id"]
                data_with_keys[id] = i
            except:
                data_with_keys[id] = i
            id += 1
        return data_with_keys

    make_key(data)
    print(f"{file} > Keys made")

    with open(f"JSONFiles_withID/{file[:-5]}.json","w+") as f:
        json.dump(data_with_keys, f)
    print(f"{file} > JSON written")