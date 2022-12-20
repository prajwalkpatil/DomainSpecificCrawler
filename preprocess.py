import os
import re
import json
import sys
import string
from logger import Logger

item_values = {}
processed_values = {}

source_directory = "./data/files_with_id"
output_intermediate = "./intermediates/items.json"
output_intermediate_processed = "./intermediates/items_processed.json"


def get_items(items):
    global source_directory
    global item_values
    try:
        all_files = os.listdir(source_directory)
        input_ids = items.copy()
        temp_list = []
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
                        # adding (id, list) to item_values
                        item_values[id] = data[id]
        Logger.write_info("Items read successfully")
        with open(output_intermediate, "w") as output_file:
            json.dump(item_values, output_file)
        Logger.write_info("Items written to file successfully")
    except Exception as e:
        Logger.write_error(e)
        sys.exit(-1)


def process_string(given_string):
    given_string = given_string.replace("-", " ")
    given_string = given_string.lower()
    return given_string


def process_dict(prop_dict):
    prop_list = []
    attribute_list = []
    yes_props = []
    split_props = []

    for item_attribute in prop_dict:
        item_property = prop_dict[item_attribute]
        attribute_list.append(
            (process_string(item_attribute), process_string(item_property)))

    attribute_list_copy = attribute_list.copy()

    for prop_pair in attribute_list_copy:
        # - Remove the attribute-property pair that consists of warranty information - #
        if re.match(r".*warranty.*", prop_pair[0]) or re.match(r".*warranty.*", prop_pair[1]):
            Logger.write_debug("Removed: " + str(prop_pair))
            attribute_list.remove(prop_pair)

        # - Remove the attribute-property pair that has a property of 'no' - #
        elif prop_pair[1] == 'no' or re.match(r"not ", prop_pair[1]):
            Logger.write_debug("Removed: " + str(prop_pair))
            attribute_list.remove(prop_pair)

        # - Remove the attribute that has property of 'yes' - #
        elif prop_pair[1] == 'yes':
            Logger.write_debug("Added to Yes:" + str(prop_pair))
            yes_props.append(prop_pair[0])
            attribute_list.remove(prop_pair)

        # - Split the property if its length is more than 150 - #
        elif len(prop_pair[1]) > 150:
            split_temp = prop_pair[1].split(", ")
            if len(split_temp[0]) < 150:
                split_props.extend(split_temp)
            attribute_list.remove(prop_pair)

    for prop_pair in attribute_list:
        prop_list.append(prop_pair[1])
    prop_list.extend(split_props)
    prop_list.extend(yes_props)
    return prop_list


def preprocess_items():
    global item_values
    global processed_values
    if not item_values:
        Logger.write_warning("Items not fetched")
        return
    for item_id in item_values:
        processed_values[item_id] = process_dict(item_values[item_id])
        Logger.write_debug("Dictionary processed for - " + item_id)
    try:
        with open(output_intermediate_processed, "w") as output_p_file:
            json.dump(processed_values, output_p_file)
        Logger.write_debug("Processed dictionary dumped to file")
    except Exception as e:
        Logger.write_error(e)
        sys.exit(-1)


def preprocess(items):
    get_items(items)
    preprocess_items()
