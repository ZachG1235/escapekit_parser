import os, json
from .immutable_constants import *

def get_room_names() -> list:
    # initialize constants
    config_path = os.path.join(CONFIG_FILE_NAME)
    with open(config_path, 'r') as config_info:
        data = json.load(config_info)
    input_folder_path_str = data["INPUT_FOLDER_PATH"]
    input_filename_str = data["INPUT_FILENAME"]

    formatted_line = []
    room_list = []
    input_file_path = f"{input_folder_path_str}/{input_filename_str}.csv"
    if os.path.isfile(input_file_path):
        with open(f"{input_folder_path_str}/{input_filename_str}.csv", 'r') as raw_file:
            line = raw_file.readline()
            formatted_line = parse_line(line)
        for each_header in formatted_line:
            if each_header.find(": Date") != -1 and not each_header.split(':')[0] in room_list:
                room_list.append(each_header.split(':')[0])
    else:
        room_list.append(UTILS_UNIDENTIFYABLE_ROOM_NAME_STR)
    return room_list

def parse_line(cur_line_str : str) -> list:
    # if ", read until next "
    # otherwise, read until next comma
    line_content = []
    current_parse = ""
    reading_quote = False
    for i in range(0, len(cur_line_str)):
        if cur_line_str[i] == '\"':
            reading_quote = not reading_quote
        elif cur_line_str[i] == ',' and not reading_quote:
            line_content.append(current_parse.strip())
            current_parse = ""
        else:
            current_parse += cur_line_str[i]
    line_content.append(current_parse.strip())
    return line_content

def get_value_from_cache(index_to_grab : str) -> str:
    grabbed_str = ""
    with open(CACHE_FILE_NAME, 'r') as fileObj:
        cache_contents = json.load(fileObj)
    return cache_contents[index_to_grab]

def create_cache():
    cache_dict = {}
    json_dict = json.dumps(cache_dict, indent=4)
    with open(CACHE_FILE_NAME, 'w') as out_file:
        for each_key in json_dict:
            out_file.write(each_key)

def write_to_cache(key_to_write : str, value_to_write : str):
    cache_read = {}
    if not os.path.exists(CACHE_FILE_NAME):
        create_cache()

    with open(CACHE_FILE_NAME, 'r') as fileObj:
        cache_read = json.load(fileObj)
    cache_read[key_to_write] = value_to_write

    json_dict = json.dumps(cache_read, indent=4)
    with open(CACHE_FILE_NAME, 'w') as out_cache:
        for each_key in json_dict:
            out_cache.write(each_key)

def get_mod_index(list_to_return : list, index : int):
    return list_to_return[index % len(list_to_return)]

def get_frac_of_num(base_number : int, numerator : int, denominator : int, use_floor_division=True):
    if use_floor_division:
        out_num = (base_number * numerator) // denominator
    else:
        out_num = (base_number * numerator) / denominator
    return out_num

def format_output_str(output_str : str, strings_to_change : tuple) -> str:
    # casts it as a tuple
    if isinstance(strings_to_change, str):
        strings_to_change = (strings_to_change,)

    current_output = output_str
    for each_value in strings_to_change:
        current_output = current_output.replace(";;;", str(each_value), 1)
    return current_output