import os
import json
import sys
from logger import Logger

people_directory = "./data/people"
files_directory = "./data/files"
output_directory = "./data/files_with_id"
START_ID = 1000


def make_key(source_dic, data_with_keys):
    global START_ID
    for i in source_dic:
        try:
            del i["id"]
            data_with_keys[START_ID] = i
        except:
            data_with_keys[START_ID] = i
        START_ID += 1
    return data_with_keys


def create_person():
    global people_directory
    global files_directory
    try:
        all_person_files = os.listdir(people_directory)
        person_array = []

        for file in all_person_files:
            with open(f"{people_directory}/{file}", 'r') as f:
                data = json.load(f)
                person_array.append(data)

        with open(f"{files_directory}/Person.json", "w") as outfile:
            json.dump(person_array, outfile)
        Logger.write_info("People grouped.")
    except Exception as e:
        Logger.write_error(e)
        sys.exit(e)


def create_files_with_ids():
    global START_ID
    global files_directory
    global output_directory
    all_files = os.listdir(files_directory)
    try:
        for file in all_files:
            with open(f"{files_directory}/{file}", 'r') as f:
                data = json.load(f)
            Logger.write_info(f"{file} > JSON read")
            data_with_keys = {}
            data_with_keys = make_key(data, data_with_keys)
            Logger.write_info(f"{file} > Keys made")
            with open(f"{output_directory}/{file[:-5]}.json", "w+") as f:
                json.dump(data_with_keys, f)
            Logger.write_info(f"{file} > JSON written")
    except Exception as e:
        Logger.write_error(e)
        sys.exit(e)


def create_files(start_id=1000):
    global START_ID
    START_ID = start_id
    create_person()
    create_files_with_ids()
    Logger.write_info("Creating files completed!")
