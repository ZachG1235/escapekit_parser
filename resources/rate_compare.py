import tkinter as tk
import os, json
from resources.accessor import get_room_names

def init_escape_rates() -> dict:
    config_path = os.path.join("config.json")
    with open(config_path, 'r') as config_info:
        data = json.load(config_info)

    input_folder_path_str = data["INPUT_FOLDER_PATH"]
    input_filename_str = data["INPUT_FILENAME"]
    
    input_file_path = os.path.join(input_folder_path_str, input_filename_str)
    with open(f"{input_file_path}.json", 'r') as fileObj:
        json_data = json.load(fileObj)
    
    gm_escape_rate_dict = {}
    # NOTE example structure:
    # gm_escape_rate_dict = {
    #       gm_name: 
    #       {
    #           total_rooms: 8
    #           room_name: 
    #           {
    #               total: 5, 
    #               escaped: 2,
    #               id_cache: [1234, 2345, 3456, 4567, 5678]
    #           }, 
    #           room_name2: 
    #           {
    #               total: 3, 
    #               escaped: 1,
    #               id_cache: [135, 246, 357]
    #           }
    #       },
    #       gm_name2: { ect..}
    # }
    for each_group in json_data:
        cur_group = json_data[each_group]
        gm = cur_group["game_master"]
        room = cur_group["room"]

        if not gm in gm_escape_rate_dict:
            gm_escape_rate_dict[gm] = {"total_rooms": 0, room : {"total": 0, "escaped": 0, "id_cache": []}}
        elif not room in gm_escape_rate_dict[cur_group["game_master"]]:
            gm_escape_rate_dict[gm][room] = {"total": 0, "escaped": 0, "id_cache": []}
        gm_escape_rate_dict[gm][room]["total"] += 1
        # gm_escape_rate_dict[gm][room]["id_cache"].append(each_group)
        gm_escape_rate_dict[gm]["total_rooms"] += 1
        if cur_group["escaped"] == True:
            gm_escape_rate_dict[gm][room]["escaped"] += 1
    
    return gm_escape_rate_dict

def main():
    root = tk.Tk()
    root.title("Escape Rate Compare")

    gm_header_start_row = 4
    room_header_start_col = 2


    # get top header columns
    x_column_sort_label = tk.Label(root, font=("Sitka Small", 10), text="Test")
    x_column_sort_box = tk.Entry(root, font=("Sitka Small", 10))
    x_column_sort_label.grid(row=0, column=0)
    x_column_sort_box.grid(row=0, column=1)

    escape_rate_data = init_escape_rates()
    game_masters = dict(sorted(escape_rate_data.items(), key=lambda item: int(item[1]["total_rooms"]), reverse=True))
    room_names = get_room_names()

    row_index = gm_header_start_row
    col_index = room_header_start_col
    data_row_index = row_index
    data_col_index = col_index
    for each_gm in game_masters:
        gm_label = tk.Label(root, font=("Sitka Small", 10), text=each_gm)
        gm_label.grid(row=row_index, column=0, columnspan=2, rowspan=2)
        row_index += 2
    
    
    room_label_list = []
    for each_room in room_names:
        rm_label = tk.Label(root, font=("Sitka Small", 10), text=each_room)
        rm_label.grid(row=3, column=col_index)
        root.grid_columnconfigure(col_index, minsize=80)
        room_label_list.append(each_room)
        col_index += 1
        
    
    print(escape_rate_data["Zach Garza"])
    
    for each_gm in game_masters:
        # get column
        for each_room in room_label_list:
            try: 
                escaped_count = int(escape_rate_data[each_gm][each_room]["escaped"])
                total_count = int(escape_rate_data[each_gm][each_room]["total"])
                rate_calc = escaped_count / total_count
                rate_calc = round(rate_calc * 100, 2)
                text_input = f"{rate_calc}%"
                subtitle_text = f"{escaped_count} of {total_count}"
            except KeyError:
                text_input = "n/a"
                subtitle_text = ""
            rate_label = tk.Label(root, font=("Sitka Small", 10), text=text_input)
            if text_input == "n/a":
                rate_label.grid(row=data_row_index, column=data_col_index, rowspan=2) 
            else:
                rate_label.grid(row=data_row_index, column=data_col_index)
                subtitle_label = tk.Label(root, font=("Sitka Small", 8), text=subtitle_text)
                data_row_index += 1
                subtitle_label.grid(row=data_row_index, column=data_col_index)
                data_row_index -= 1
            data_col_index += 1
        data_row_index += 2
        data_col_index = room_header_start_col

    tk.mainloop()

if __name__ == "__main__":
    main()