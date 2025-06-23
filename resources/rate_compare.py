import tkinter as tk
import os, json

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

def main():
    root = tk.Tk()
    root.title("Escape Rate Compare")

    # get top header columns
    x_column_sort_label = tk.Label(root, font=("Sitka Small", 10), text="Test")
    x_column_sort_box = tk.Entry(root, font=("Sitka Small", 10))
    x_column_sort_label.grid(row=0, column=0)
    x_column_sort_box.grid(row=0, column=1)

    game_masters = get_game_masters()
    sorted_game_masters = []
    game_masters = dict(sorted(game_masters.items(), key=lambda item: item[1], reverse=True))
    print(game_masters)
    index = 2
    for each_gm in game_masters:
        gm_label = tk.Label(root, font=("Sitka Small", 10), text=each_gm)
        gm_label.grid(row=index, column=0)
        index += 1

    #tk.mainloop()

if __name__ == "__main__":
    main()