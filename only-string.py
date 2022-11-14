import json
import os

import numpy as np

source_directory = './JSONFiles_withID/'
all_files = os.listdir(source_directory)
print("JSON Files are : ")

arrDict = {}

flag = 0
for file in all_files:
    print(file)
    with open(f"{source_directory}/{file}", 'r') as f:
        data = json.load(f)  # this data is of type dictionary
        for i in data:
            item = data[i]
            for i in item:
                arrDict.push(item[i])

print(arrDict)
# # str1 = "Geeks 123 for 127geeks"

# # printing initial .ini_string
# print("initial string : ", str1)

# # using loop and in
# # to remove numeric digits from string
# str2 = ""
# for i in str1:
#     if (not ord(i) in range(48, 58)):
#         str2 += i
# # printing result
# print("final string : ", str2)
