import tkinter as tk
import os, json
from .utils import get_room_names, get_value_from_cache, get_mod_index, get_frac_of_num
from .immutable_constants import *


def init_escape_rates() -> dict:
    config_path = os.path.join(CONFIG_FILE_NAME)
    with open(config_path, 'r') as config_info:
        data = json.load(config_info)

    output_folder_path_str = data["OUTPUT_FOLDER_PATH"]
    cur_output_filestr = ""

    cur_output_filestr = get_value_from_cache(CACHE_CURRENT_OUTPUT_KEY)
    
    output_file_path = os.path.join(output_folder_path_str, cur_output_filestr)
    with open(f"{output_file_path}.json", 'r') as fileObj:
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
        gm = cur_group[SEARCH_ENUM_GAME_MASTER]
        room = cur_group[SEARCH_ENUM_ROOM]

        if not gm in gm_escape_rate_dict:
            gm_escape_rate_dict[gm] = {"total_rooms": 0, room : {"total": 0, "escaped": 0, "id_cache": []}}
        elif not room in gm_escape_rate_dict[cur_group[SEARCH_ENUM_GAME_MASTER]]:
            gm_escape_rate_dict[gm][room] = {"total": 0, "escaped": 0, "id_cache": []}
        gm_escape_rate_dict[gm][room]["total"] += 1
        if ESCAPE_RATE_CACHE_STORAGE:
            gm_escape_rate_dict[gm][room]["id_cache"].append(each_group)
        gm_escape_rate_dict[gm]["total_rooms"] += 1
        if cur_group[SEARCH_ENUM_ESCAPED] == True:
            gm_escape_rate_dict[gm][room][SEARCH_ENUM_ESCAPED] += 1
    
    return gm_escape_rate_dict

def escaperate_display():
    root = tk.Toplevel()
    root.title("Compare Escape Rates")

    gm_header_start_row = 3
    room_header_start_col = 2

    main_canvas = tk.Canvas(root, borderwidth=0)
    main_canvas.grid(row=1, column=0, columnspan=5, sticky="nsew")


    v_scrollbar = tk.Scrollbar(root, orient="vertical", command=main_canvas.yview)
    v_scrollbar.grid(row=1, column=7, sticky="ns")
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(1, weight=1)
    main_canvas.configure(yscrollcommand=v_scrollbar.set)

    inner_frame = tk.Frame(main_canvas)
    main_canvas.create_window((0, 0), window=inner_frame, anchor="nw")



    escape_rate_data = init_escape_rates()
    game_masters = dict(sorted(escape_rate_data.items(), key=lambda item: int(item[1]["total_rooms"]), reverse=True))
    room_names = get_room_names()
    # remove Event column since there's not enough data in CSV
    room_names.remove(EVENT_ROOM_NAME_CONVERSION_LITERAL) 

    row_index = gm_header_start_row
    col_index = room_header_start_col
    data_row_index = row_index  
    data_col_index = col_index

    room_label_list = []
    for each_room in room_names:
        rm_label = tk.Label(inner_frame, font=("Sitka Small", 10), text=each_room.replace(' ', "\n", 1))
        rm_label.grid(row=0, column=col_index, sticky="news")
        inner_frame.grid_columnconfigure(col_index, minsize=70)
        room_label_list.append(each_room)
        col_index += 1

    total_rooms_str = "total_rooms"
    for each_gm in game_masters:
        game_master_name = each_gm
        try:
            room_quantity = escape_rate_data[game_master_name][total_rooms_str]
        except KeyError:
            room_quantity = 0

        if each_gm == "":
            game_master_name = EMPTY_GM_CONVERSION_LITERAL
        if not each_gm == EVENT_GM_CONVERSION_LITERAL:
            gm_label = tk.Label(inner_frame, font=("Sitka Small", 10), text=f"{game_master_name}\n({room_quantity})")
            gm_label.grid(row=row_index, column=0, columnspan=2, rowspan=2)
        row_index += 2
    

    color_index = 0
    for each_gm in game_masters:
        # get column
        if not each_gm == EVENT_GM_CONVERSION_LITERAL:
            for each_room in room_label_list:
                try: 
                    escaped_count = int(escape_rate_data[each_gm][each_room][SEARCH_ENUM_ESCAPED])
                    total_count = int(escape_rate_data[each_gm][each_room]["total"])
                    rate_calc = escaped_count / total_count
                    rate_calc = round(rate_calc * 100, 2)
                    text_input = f"{rate_calc}%"
                    subtitle_text = f"{escaped_count} of {total_count}"
                except KeyError: # room data does not exist
                    text_input = ESCAPE_RATE_NO_VALUE_DISPLAY_LITERAL
                    subtitle_text = ""
                rate_label = tk.Label(inner_frame, font=("Sitka Small", 10), text=text_input,
                                                bg=get_mod_index(ESCAPE_RATE_BACKGROUND_COLORS, color_index))
                # if there is no data for the room
                if text_input == ESCAPE_RATE_NO_VALUE_DISPLAY_LITERAL: 
                    rate_label.grid(row=data_row_index, column=data_col_index, rowspan=2, sticky="news") 
                # otherwise, display data for room
                else:
                    rate_label.grid(row=data_row_index, column=data_col_index, sticky="news")
                    subtitle_label = tk.Label(inner_frame, font=("Sitka Small", 8), text=subtitle_text, 
                                                    bg=get_mod_index(ESCAPE_RATE_BACKGROUND_COLORS, color_index))
                    data_row_index += 1
                    subtitle_label.grid(row=data_row_index, column=data_col_index, sticky="news")
                    data_row_index -= 1
                data_col_index += 1
            color_index += 1
        data_row_index += 2
        data_col_index = room_header_start_col


    def on_frame_configure(event):
        main_canvas.configure(scrollregion=main_canvas.bbox("all"))

    inner_frame.bind("<Configure>", on_frame_configure)
    screen_height = root.winfo_screenheight()
    # get 3/4 of the screen height
    resized_screen_height = get_frac_of_num(screen_height, 3, 4)
    root.update_idletasks()
    # manual extension so rooms are displayed
    root.geometry(f"{root.winfo_reqwidth()+100}x{resized_screen_height}")

    root.mainloop()

if __name__ == "__main__":
    escaperate_display()