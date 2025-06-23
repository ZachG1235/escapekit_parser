import tkinter as tk
import os, json
from resources.accessor import get_room_names

def get_game_masters():
    config_path = os.path.join("config.json")
    with open(config_path, 'r') as config_info:
        data = json.load(config_info)

    input_folder_path_str = data["INPUT_FOLDER_PATH"]
    input_filename_str = data["INPUT_FILENAME"]
    
    input_file_path = os.path.join(input_folder_path_str, input_filename_str)
    with open(f"{input_file_path}.json", 'r') as fileObj:
        json_data = json.load(fileObj)
    
    game_masters = {}
    for each_group in json_data:
        cur_name = json_data[each_group]["game_master"]
        if len(cur_name) > 0:
            if not cur_name in game_masters:
                game_masters[cur_name] = 1
            else:
                game_masters[cur_name] += 1   
    return game_masters

def init_escape_rates():
    config_path = os.path.join("config.json")
    with open(config_path, 'r') as config_info:
        data = json.load(config_info)

    input_folder_path_str = data["INPUT_FOLDER_PATH"]
    input_filename_str = data["INPUT_FILENAME"]
    
    input_file_path = os.path.join(input_folder_path_str, input_filename_str)
    with open(f"{input_file_path}.json", 'r') as fileObj:
        json_data = json.load(fileObj)
    
    gm_escape_rate_dict = {}
    # name: {room_name: {total: 5, escaped: 2}}

    for each_group in json_data:
        cur_group = json_data[each_group]
        gm = cur_group["game_master"]
        room = cur_group["room"]

        if not gm in gm_escape_rate_dict:
            gm_escape_rate_dict[gm] = {room : {"total": 0, "escaped": 0}}
        elif not room in gm_escape_rate_dict[cur_group["game_master"]]:
            gm_escape_rate_dict[gm][room] = {"total": 0, "escaped": 0}
        gm_escape_rate_dict[gm][room]["total"] += 1
        if cur_group["escaped"] == True:
            gm_escape_rate_dict[gm][room]["escaped"] += 1
    
    return gm_escape_rate_dict

def main():
    root = tk.Tk()
    root.title("Escape Rate Compare")

    # get top header columns
    x_column_sort_label = tk.Label(root, font=("Sitka Small", 10), text="Test")
    x_column_sort_box = tk.Entry(root, font=("Sitka Small", 10))
    x_column_sort_label.grid(row=0, column=0)
    x_column_sort_box.grid(row=0, column=1)

    game_masters = get_game_masters()
    game_masters = dict(sorted(game_masters.items(), key=lambda item: item[1], reverse=True))
    index = 2
    for each_gm in game_masters:
        gm_label = tk.Label(root, font=("Sitka Small", 10), text=each_gm)
        gm_label.grid(row=index, column=0)
        index += 1
    
    room_names = get_room_names()
    
    escape_rate_data = init_escape_rates()


    tk.mainloop()

if __name__ == "__main__":
    main()