import json, os, datetime
import tkinter as tk
from .file_parser import update_escape_groups
from .result_display import show_results
from .constants import *            # imports constants
from .immutable_constants import *
from .rate_display import escaperate_display
from .utils import get_room_names, get_value_from_cache, write_to_cache, format_output_str, ParsedFileExistenceError, InputFileExistenceError


def search_and_sort(key_tuples : list, sort_tuple : tuple) -> tuple:
    # initialize constants
    config_path = os.path.join(CONFIG_FILE_NAME)
    with open(config_path, 'r') as config_info:
        data = json.load(config_info)
    input_folder_path_str = data["INPUT_FOLDER_PATH"]
    input_filename_str = data["INPUT_FILENAME"]
    output_folder_path = data["OUTPUT_FOLDER_PATH"]
    
    input_file_path = os.path.join(input_folder_path_str, input_filename_str)
    
    try: 
        with open(f"{input_file_path}.json", 'r') as fileObj:
            json_data = json.load(fileObj)
    except FileNotFoundError:
        raise ParsedFileExistenceError(ERROR_PARSE_CSV_BUTTON_STR)

    
    found_data = {}
    
    # find groups
    for each_group in json_data:
        matching_search = 0
        for each_tuple in key_tuples:
            tup_key, tup_value = each_tuple
            if tup_key == SEARCH_ENUM_GROUP_SIZE:
                if int(json_data[each_group][tup_key]) == int(tup_value):
                    matching_search += 1
            elif tup_key == SEARCH_ENUM_ESCAPED:
                if json_data[each_group][tup_key]:
                    matching_search += 1
            else:
                tup_value = tup_value.lower()
                compare_value = json_data[each_group][tup_key].lower()
                if compare_value.find(tup_value) != -1:
                    matching_search += 1
        if matching_search == len(key_tuples):
            found_data[each_group] = json_data[each_group]
    
    def parse_time_remaining(time_str) -> datetime.timedelta:
        if time_str == EVENT_TIME_RM_CONVERSION_LITERAL:
            return datetime.timedelta(seconds=-1)
        # if the time_str is blank
        if not len(time_str) > 0:
            return datetime.timedelta(seconds=0)
        hours, mins, secs = map(int, time_str.split(":"))
        return datetime.timedelta(hours=hours, minutes=mins, seconds=secs)

    def parse_game_master_sort(gm_str, ltg_bool):
        if gm_str == "":
            if ltg_bool:
                # returns greatest alphabetical value 
                return "AAAAAA"
            # returns least alphabetical value
            return "zzzzzzz"
        return gm_str


    if len(sort_tuple) > 0:
        sort_key, sort_bool = sort_tuple

        if sort_key == "time_remaining":
            # originally asked for least to greatest, inverting it is actually least to greatest
            found_data = dict(sorted(found_data.items(), key=lambda item: parse_time_remaining(item[1][sort_key]), reverse=(not sort_bool)))
        elif sort_key == "game_master":
            # alphabetically is backwards. keep the boolean
            found_data = dict(sorted(found_data.items(), key=lambda item: parse_game_master_sort(item[1][sort_key], sort_bool), reverse=sort_bool))
        elif sort_key == "room":
            # alphabetically is backwards. keep the boolean
            found_data = dict(sorted(found_data.items(), key=lambda item: item[1][sort_key], reverse=sort_bool))
        elif sort_key == "group_size":
            # originally asked for least to greatest, inverting it is actually least to greatest
            found_data = dict(sorted(found_data.items(), key=lambda item: item[1][sort_key], reverse=(not sort_bool)))

        show_rank_bool_str = "true"
    else:
        show_rank_bool_str = "false"

    out_file_str = generate_outfile_str(key_tuples, sort_tuple)
    out_file_path = os.path.join(output_folder_path, out_file_str)
    
    with open(f"{out_file_path}.json", 'w') as out_file:
        out_file.write(json.dumps(found_data, indent=4))
    
    write_to_cache(CACHE_CURRENT_OUTPUT_KEY, out_file_str)
    write_to_cache(CACHE_SHOW_RANK_KEY, show_rank_bool_str)

    return (len(found_data), out_file_str)
        

def generate_outfile_str(key_tuples : list, sort_tuple : tuple) -> str:
    # initialize constants
    config_path = os.path.join(CONFIG_FILE_NAME)
    with open(config_path, 'r') as config_info:
        data = json.load(config_info)
    generate_unique_outfile_name_bool = "True" == data["GENERATE_UNIQUE_OUTFILE_NAME"] 
    outfile_abbreviations_dict = data["OUTFILE_ABBREVIATIONS"]

    
    if not generate_unique_outfile_name_bool:
        return "output"
    elif len(key_tuples) == 0 and len(sort_tuple) == 0:
        time_now = datetime.datetime.now()
        time_now = time_now.strftime("%H-%M-%S_%y-%m-%d")
        return time_now
    
    out_file_str = ""
    for each_tuple in key_tuples:
        # replace _ with spaces, lower first_tuple and upper second_tuple
        first_tuple, second_tuple = each_tuple
        first_tuple = str(first_tuple).lower()
        second_tuple = str(second_tuple).replace(' ', '_')
        try:
            second_tuple = second_tuple.upper()
        except:
            second_tuple = second_tuple

        # concatenate them together
        each_tuple = f"{first_tuple}{second_tuple}"

        for each_letter in each_tuple:
            # delete non alnumeric characters (keep underscores)
            if each_letter.isalnum() or each_letter == '_':
                out_file_str += each_letter

    if len(sort_tuple) > 0:
        first_tuple, second_tuple = sort_tuple
        out_file_str += f"sort{first_tuple.upper()}ltg{str(second_tuple).upper()}"
    
    # outfilestr replacer
    for each_key in outfile_abbreviations_dict:
        out_file_str = out_file_str.replace(each_key, outfile_abbreviations_dict[each_key])

    # parse out room names to make them shorter
    # words are replaced by their first letter
    room_list = get_room_names()
    new_room_list = {}
    for each_room in room_list:
        old_room_name = each_room.upper().replace(' ', '_').replace('\'', '')
        new_old_room_name = ""
        new_str = ""

        each_room = each_room.replace('\'', '').title()

        for each_letter in old_room_name:
            # delete non alnumeric characters (keep underscores)
            if each_letter.isalnum() or each_letter == '_':
                new_old_room_name += each_letter

        for each_letter in each_room:
            if each_letter.isupper():
                new_str += each_letter  
        new_room_list[old_room_name] = new_str

    # parse out room names
    for each_key in new_room_list:
        out_file_str = out_file_str.replace(each_key, new_room_list[each_key])

    return out_file_str

def set_result_status(input_str : str, label : tk.Label):
    label.config(text=input_str)

def restore_config_default():
    config_path = os.path.join(CONFIG_FILE_NAME)
    constants_path = os.path.join(RESOURCE_FOLDER_PATH, "constants.py")
    constants_raw = []
    with open(constants_path, 'r') as constants_file:
        constants_raw = constants_file.readlines()
    
    constants_cleaned = []
    for each_line in constants_raw:
        cleaned_line = each_line.strip().replace(' ', '')
        if cleaned_line.find('{') == -1: #if line does not have bracket
           cleaned_line = cleaned_line.replace('"', '')
        if not cleaned_line.find('#') == -1: # if comment exists in line
            cleaned_line = cleaned_line[:cleaned_line.find('#')] # truncates line before '#'
        if len(cleaned_line) > 0:
            constants_cleaned.append(cleaned_line)
    
    out_dict = {}
    for each_line in constants_cleaned:
        name, value = each_line.split('=', 1) # split by equals once
        if not value.find('{') == -1: # if bracket is found
            temp_dict = json.loads(value)
            out_dict[name] = temp_dict
        else:
            out_dict[name] = value
    
    json_dict = json.dumps(out_dict, indent=4)
    with open(config_path, 'w') as out_config:
        for each_key in json_dict:
            out_config.write(each_key)

def check_for_config_init():
    # verify file existing
    if not os.path.isfile(CONFIG_FILE_NAME):
        # create new config.json
        restore_config_default()

def is_valid_color(window, color_str):
    try:
        window.winfo_rgb(color_str)
        return (True, color_str)
    except tk.TclError:
        return (False, "white")

def output_bad_colors(wrong_colors, label):
    if len(wrong_colors) > 0:
        prefix_wc_str = "Color"
        suffix_wc_str = "is"
        if len(wrong_colors) > 1:
            prefix_wc_str += "s"
            suffix_wc_str = "are"
        wrong_color_str = ""
        for each_color in wrong_colors:
            wrong_color_str += f"\'{each_color}\', "     
        wrong_color_str = wrong_color_str[:-2][::-1].replace(',', "dna ,", 1)[::-1]

        set_result_status(f"{prefix_wc_str} {wrong_color_str} {suffix_wc_str} invalid, please change in settings.", label)

def tk_main():
    root = tk.Tk()
    root.title("EscapeKit Parser: Made by ZachG1235")
    root.iconbitmap("icons/ekp_transparent.ico")
    for i in range(0, 10):
        root.grid_rowconfigure(i, minsize=55)
    for j in range(0, 2):
        root.grid_columnconfigure(j, minsize=220)

    # create config.json if not existing already
    check_for_config_init()

    # variables for room name initalization
    room_dropdown_labels = get_room_names() # get rooms
    room_dropdown_selection = tk.StringVar()
    room_dropdown_selection.set(room_dropdown_labels[0])

    # variables for sort initialization
    sort_dropdown_labels = ["Game master", "Room name", "Group size", "Time remaining"]
    sort_dropdown_selection = tk.StringVar()
    sort_dropdown_selection.set(sort_dropdown_labels[0])

    # checkbox bool holders
    gm_check_bool = tk.BooleanVar()
    room_check_bool = tk.BooleanVar()
    gz_check_bool = tk.BooleanVar()
    sort_check_bool = tk.BooleanVar()
    ltg_check_bool = tk.BooleanVar()
    escaped_check_bool = tk.BooleanVar()
    enable_setting_viz = tk.BooleanVar()
    enable_setting_viz.set(True)
    settings_guon_bool = tk.BooleanVar()
    
    # functions to toggle fields/dropdowns when associated checkbox is clicked
    def toggle_gm_box():
        if gm_check_bool.get():
            gm_label.grid(row=0, column=1, padx=10, pady=5)
            gm_box.grid(row=1, column=1, padx=10, pady=5)
        else:
            gm_label.grid_remove()
            gm_box.grid_remove()

    def toggle_room_box():
        if room_check_bool.get():
            room_dropdown.grid(row=2, column=1, padx=10, pady=5, rowspan=2)
        else:
            room_dropdown.grid_remove()

    def toggle_gz_box():
        if gz_check_bool.get():
            gz_label.grid(row=4, column=1, padx=10, pady=5)
            gz_box.grid(row=5, column=1, padx=10, pady=5)
        else:
            gz_label.grid_remove()
            gz_box.grid_remove()

    def sort_box():
        if sort_check_bool.get():
            sort_dropdown.grid(row=6, column=1, padx=10, pady=10)
            ltg_check_box.grid(row=7, column=1, padx=10, pady=10)
        else:
            sort_dropdown.grid_remove()
            ltg_check_box.grid_remove()

    # game master checkbox and field
    gm_check_box = tk.Checkbutton(root, text="Game Master", variable=gm_check_bool, command=toggle_gm_box, font=LARGE_FONT_TYPE)
    gm_check_box.grid(row=0, column=0, padx=10, pady=10, rowspan=2)
    gm_label = tk.Label(root, text="Enter game master name:", font=MEDIUM_FONT_TYPE)
    gm_box = tk.Entry(root, font=MEDIUM_FONT_TYPE)

    # room name checkbox and dropdown
    room_check_box = tk.Checkbutton(root, text="Room Name", variable=room_check_bool, command=toggle_room_box, font=LARGE_FONT_TYPE)
    room_check_box.grid(row=2, column=0, padx=10, pady=10, rowspan=2)
    room_dropdown = tk.OptionMenu(root, room_dropdown_selection, *room_dropdown_labels)
    room_dropdown.config(font=MEDIUM_FONT_TYPE)
    room_dropdown["menu"].config(font=MEDIUM_FONT_TYPE)
    def update_dropdowns(): # updates the dropdowns after parsing data
        menu = room_dropdown["menu"]
        menu.delete(0, "end")  # Clear existing options
        room_list = get_room_names()
        for option in room_list:
            menu.add_command(
                label=option,
                command=lambda value=option: room_dropdown_selection.set(value)
            )
        room_dropdown_selection.set(room_list[0])

    # group size checkbox and field
    gz_check_box = tk.Checkbutton(root, text="Group Size", variable=gz_check_bool, command=toggle_gz_box, font=LARGE_FONT_TYPE)
    gz_check_box.grid(row=4, column=0, padx=10, pady=10, rowspan=2)
    gz_label = tk.Label(root, text="Enter group size:", font=MEDIUM_FONT_TYPE)
    gz_box = tk.Entry(root, font=MEDIUM_FONT_TYPE)

    # sort by checkbox and dropdown
    sort_check_box = tk.Checkbutton(root, text="Sort by", variable=sort_check_bool, command=sort_box, font=LARGE_FONT_TYPE)
    sort_check_box.grid(row=6, column=0, padx=10, pady=10, rowspan=2)
    sort_dropdown = tk.OptionMenu(root, sort_dropdown_selection, *sort_dropdown_labels)
    sort_dropdown.config(font=MEDIUM_FONT_TYPE)
    sort_dropdown["menu"].config(font=MEDIUM_FONT_TYPE)
    ltg_check_box = tk.Checkbutton(root, text="Sort Least to Greatest?", variable=ltg_check_bool, font=SMALL_FONT_TYPE)

    # checkbox for escaped groups
    escaped_check_box = tk.Checkbutton(root, text="Only show escaped rooms", variable=escaped_check_bool, font=VERY_SMALL_FONT_TYPE)
    escaped_check_box.grid(row=8, column=0, padx=10, pady=10)

    # result displaying label
    result_label = tk.Label(root, text="", font=VERY_SMALL_FONT_TYPE, wraplength=200)
    result_label.grid(row=9, column=0, pady=10)

    # function to start the search process (activates on Search Button)
    def search():
        search_queries = []
        sort_query = ()
        something_selected = False

        if gm_check_bool.get():
            game_master_to_search = gm_box.get()
            if len(game_master_to_search) > 0:
                search_queries.append((SEARCH_ENUM_GAME_MASTER, game_master_to_search))
                something_selected = True
        if room_check_bool.get():
            room_name_to_search = room_dropdown_selection.get()
            search_queries.append((SEARCH_ENUM_ROOM, room_name_to_search))
            something_selected = True
        if gz_check_bool.get():
            group_size_to_search = gz_box.get()
            group_size_is_valid = True
            # error handle for non-ints
            try:
                # if negative number
                if int(group_size_to_search) < 0:
                    group_size_is_valid = False
            except ValueError:
                group_size_is_valid = False
            
            if not group_size_is_valid:
                set_result_status(ERROR_INVALID_GROUP_SIZE_STR, result_label)
                set_open_button(False)
                return
            if len(group_size_to_search) > 0:
                search_queries.append((SEARCH_ENUM_GROUP_SIZE, group_size_to_search))
                something_selected = True
        if sort_check_bool.get():
            sort_selection = sort_dropdown_selection.get()
            least_to_greatest_bool = ltg_check_bool.get()
            # removes "name" off of "Room name" and turns spaces into underscores
            sort_selection = sort_selection.lower().replace("name", '').strip().replace(' ', '_')
            sort_query = (sort_selection, least_to_greatest_bool)
            something_selected = True
        if escaped_check_bool.get():
            search_queries.append((SEARCH_ENUM_ESCAPED, True))
            something_selected = True
        
        try:
            amount_found, out_file_name = search_and_sort(search_queries, sort_query)
            out_msg = ""
            if len(search_queries) == 0 and len(sort_query) == 0:
                out_msg = format_output_str(RESULT_NO_FILTER_SEARCH_STR, (amount_found, out_file_name))
            else:
                out_msg = format_output_str(RESULT_WITH_FILTER_SEARCH_STR, (amount_found, out_file_name))
            set_result_status(out_msg, result_label)
            set_open_button(True)        
        except ParsedFileExistenceError as search_error:
            set_result_status(search_error.message, result_label)
        except InputFileExistenceError as in_error:
            set_result_status(in_error.message, result_label)

            
    def file_parse():
        # initialize constants
        config_path = os.path.join(CONFIG_FILE_NAME)
        with open(config_path, 'r') as config_info:
            data = json.load(config_info)
        input_folder_path_str = data["INPUT_FOLDER_PATH"]
        input_filename_str = data["INPUT_FILENAME"]
        
        in_file_name = os.path.join(input_folder_path_str, input_filename_str)
        in_file_name += ".csv"
        out_file_name = os.path.join(input_folder_path_str, input_filename_str)
        out_file_name += ".json"
        set_result_status(format_output_str(STATUS_PARSING_IN_PROG_STR, (in_file_name)), result_label)
        root.update() 

        success = update_escape_groups(in_file_name, out_file_name)
        if not success:
            set_result_status(format_output_str(ERROR_PARSE_INVALID_FILEPATH_STR, in_file_name), result_label)
            set_open_button(False)
        else:
            update_dropdowns()
            set_result_status(format_output_str(RESULT_PARSE_SUCCESS_STR, in_file_name), result_label)
            set_open_button(False)
        

    def open_file():
        file_name = get_value_from_cache(CACHE_CURRENT_OUTPUT_KEY)
        show_rank = get_value_from_cache(CACHE_SHOW_RANK_KEY) == "true"

        config_path = os.path.join(CONFIG_FILE_NAME)
        with open(config_path, 'r') as config_info:
            data = json.load(config_info)
        max_displayed_entries = data["MAX_DISPLAYABLE_ENTRIES"]
        try:
            if isinstance(int(max_displayed_entries), int):
                show_results(file_name, show_rank)
        except ValueError:
            set_result_status(format_output_str(INVALID_DISPLAY_INTEGER_STR, max_displayed_entries), result_label)
        

    def open_escaperate():
        escaperate_display()


    def set_open_button(show_bool : bool):
        if show_bool:
            open_file_button.grid(row=9, column=1, sticky="w")
            open_escaperate_button.grid(row=8, column=1, sticky="w")
        else:
            open_file_button.grid_remove()
            open_escaperate_button.grid_remove()


    def open_advanced_settings_window():
        # initialize constants
        config_path = os.path.join(CONFIG_FILE_NAME)
        with open(config_path, 'r') as config_info:
            data = json.load(config_info)

        if enable_setting_viz.get(): # create the settings menu and display
            enable_setting_viz.set(False)
            
            setting_root = tk.Toplevel()
            setting_root.title("EscapeKit Parser: Settings")
            
            def on_destroy(event):
                if event.widget == setting_root:
                    enable_setting_viz.set(True)
            
            def restore_defaults():
                restore_config_default()
                out_msg = format_output_str(ADV_SET_RESTORE_DEFAULTS_STR, (CONFIG_FILE_NAME,)) # typecast as tuple
                set_result_status(out_msg, result_label)
                setting_root.destroy()

            def save_current_settings():
                data_dict = {}
                data_dict["INPUT_FOLDER_PATH"] = in_fold_box.get()
                data_dict["INPUT_FILENAME"] = in_file_box.get()
                data_dict["OUTPUT_FOLDER_PATH"] = out_fold_box.get()
                data_dict["RESOURCE_FOLDER_PATH"] = resource_fold_box.get()
                data_dict["MAX_DISPLAYABLE_ENTRIES"] = max_displayed_box.get()
                data_dict["GENERATE_UNIQUE_OUTFILE_NAME"] = str(settings_guon_bool.get())
                

                abb_dict = {}
                abb_dict[SEARCH_ENUM_GAME_MASTER] = out_file_abb_box_gm.get()
                abb_dict[SEARCH_ENUM_ROOM] = out_file_abb_box_rm.get()
                abb_dict[SEARCH_ENUM_GROUP_SIZE] = out_file_abb_box_gz.get()
                abb_dict[SEARCH_ENUM_ESCAPED] = out_file_abb_box_es.get()
                abb_dict["TIME_REMAINING"] = out_file_abb_box_tm.get()
                abb_dict["TRUE"] = out_file_abb_box_true.get()
                abb_dict["FALSE"] = out_file_abb_box_false.get()
                
                data_dict["OUTFILE_ABBREVIATIONS"] = abb_dict
                data_dict["SEARCH_BTN_COLOR"] = search_btn_box.get()
                data_dict["DELETE_BTN_COLOR"] = delete_btn_box.get()
                data_dict["PARSE_BTN_COLOR"] = parse_btn_box.get()
                data_dict["OPEN_BTN_COLOR"] = open_btn_box.get()
                data_dict["SETTING_BTN_COLOR"] = setting_btn_box.get()
                data_dict["RESTR_CNFG_BTN_COLOR"] = restore_def_btn_box.get()
                data_dict["SAVE_STNGS_BTN_COLOR"] = save_set_btn_box.get()
                data_dict["OPEN_ESCAPERATE_BTN_COLOR"] = open_er_btn_box.get()


                json_dict = json.dumps(data_dict, indent=4)
                with open(config_path, 'w') as out_config:
                    for each_key in json_dict:
                        out_config.write(each_key)

                # destroy settings
                out_msg = format_output_str(ADV_SET_RESTORE_DEFAULTS_STR, (CONFIG_FILE_NAME,)) # typecast as tuple
                set_result_status(out_msg, result_label)
                setting_root.destroy()




            def toggle_outfile_abb_visibility():
                if settings_guon_bool.get():
                    # grid the abbreviations
                    out_file_abb_label_header.grid(row=6, column=0, pady=ADV_SET_VERT_PAD_INT, padx=5, columnspan=2)
                    out_file_abb_label_gm.grid(row=7, column=0, pady=ADV_SET_VERT_PAD_INT, padx=5)
                    out_file_abb_box_gm.grid(row=7, column=1, pady=ADV_SET_VERT_PAD_INT, padx=5)
                    out_file_abb_label_rm.grid(row=8, column=0, pady=ADV_SET_VERT_PAD_INT, padx=5)
                    out_file_abb_box_rm.grid(row=8, column=1, pady=ADV_SET_VERT_PAD_INT, padx=5)
                    out_file_abb_label_gz.grid(row=9, column=0, pady=ADV_SET_VERT_PAD_INT, padx=5)
                    out_file_abb_box_gz.grid(row=9, column=1, pady=ADV_SET_VERT_PAD_INT, padx=5)
                    out_file_abb_label_es.grid(row=10, column=0, pady=ADV_SET_VERT_PAD_INT, padx=5)
                    out_file_abb_box_es.grid(row=10, column=1, pady=ADV_SET_VERT_PAD_INT, padx=5)
                    out_file_abb_label_tm.grid(row=11, column=0, pady=ADV_SET_VERT_PAD_INT, padx=5)
                    out_file_abb_box_tm.grid(row=11, column=1, pady=ADV_SET_VERT_PAD_INT, padx=5)
                    out_file_abb_label_true.grid(row=12, column=0, pady=ADV_SET_VERT_PAD_INT, padx=5)
                    out_file_abb_box_true.grid(row=12, column=1, pady=ADV_SET_VERT_PAD_INT, padx=5)
                    out_file_abb_label_false.grid(row=13, column=0, pady=ADV_SET_VERT_PAD_INT, padx=5)
                    out_file_abb_box_false.grid(row=13, column=1, pady=ADV_SET_VERT_PAD_INT, padx=5)
                else:
                    # ungrid the abbreviations
                    out_file_abb_label_header.grid_remove()
                    out_file_abb_label_gm.grid_remove()
                    out_file_abb_box_gm.grid_remove()
                    out_file_abb_label_rm.grid_remove()
                    out_file_abb_box_rm.grid_remove()
                    out_file_abb_label_gz.grid_remove()
                    out_file_abb_box_gz.grid_remove()
                    out_file_abb_label_es.grid_remove()
                    out_file_abb_box_es.grid_remove()
                    out_file_abb_label_tm.grid_remove()
                    out_file_abb_box_tm.grid_remove()
                    out_file_abb_label_true.grid_remove()
                    out_file_abb_box_true.grid_remove()
                    out_file_abb_label_false.grid_remove()
                    out_file_abb_box_false.grid_remove()

            # get config file settings for the .insert() commands

            in_fold_label = tk.Label(setting_root, text="Input Folder Path", font=MEDIUM_FONT_TYPE)
            in_fold_box = tk.Entry(setting_root, font=MEDIUM_FONT_TYPE)
            in_fold_label.grid(row=0, column=0, pady=ADV_SET_VERT_PAD_INT, padx=5)
            in_fold_box.grid(row=0, column=1, pady=ADV_SET_VERT_PAD_INT, padx=5)
            in_fold_box.insert(0, data["INPUT_FOLDER_PATH"])

            in_file_label = tk.Label(setting_root, text="Input Filename", font=MEDIUM_FONT_TYPE)
            in_file_box = tk.Entry(setting_root, font=MEDIUM_FONT_TYPE)
            in_file_label.grid(row=1, column=0, pady=ADV_SET_VERT_PAD_INT, padx=5)
            in_file_box.grid(row=1, column=1, pady=ADV_SET_VERT_PAD_INT, padx=5)
            in_file_box.insert(0, data["INPUT_FILENAME"])

            out_fold_label = tk.Label(setting_root, text="Output Folder Path", font=MEDIUM_FONT_TYPE)
            out_fold_box = tk.Entry(setting_root, font=MEDIUM_FONT_TYPE)
            out_fold_label.grid(row=2, column=0, pady=ADV_SET_VERT_PAD_INT, padx=5)
            out_fold_box.grid(row=2, column=1, pady=ADV_SET_VERT_PAD_INT, padx=5)
            out_fold_box.insert(0, data["OUTPUT_FOLDER_PATH"])

            resource_fold_label = tk.Label(setting_root, text="Resources Folder Path", font=MEDIUM_FONT_TYPE)
            resource_fold_box = tk.Entry(setting_root, font=MEDIUM_FONT_TYPE)
            resource_fold_label.grid(row=3, column=0, pady=ADV_SET_VERT_PAD_INT, padx=5)
            resource_fold_box.grid(row=3, column=1, pady=ADV_SET_VERT_PAD_INT, padx=5)
            resource_fold_box.insert(0, data["RESOURCE_FOLDER_PATH"])

            max_displayed_label = tk.Label(setting_root, text="Max Displayed Entries", font=MEDIUM_FONT_TYPE)
            max_displayed_box = tk.Entry(setting_root, font=MEDIUM_FONT_TYPE)
            max_displayed_label.grid(row=4, column=0, pady=ADV_SET_VERT_PAD_INT, padx=5)
            max_displayed_box.grid(row=4, column=1, pady=ADV_SET_VERT_PAD_INT, padx=5)
            max_displayed_box.insert(0, data["MAX_DISPLAYABLE_ENTRIES"])
            
            # set settings_guon_bool to it's associated value
            settings_guon_bool.set("True" == data["GENERATE_UNIQUE_OUTFILE_NAME"])
            gen_unique_out_name_label = tk.Label(setting_root, text="Generate Unique Outfile Name", font=MEDIUM_FONT_TYPE)
            gen_unique_out_name_checkbox = tk.Checkbutton(setting_root, variable=settings_guon_bool, command=toggle_outfile_abb_visibility) # type: ignore
            gen_unique_out_name_label.grid(row=5, column=0, pady=ADV_SET_VERT_PAD_INT, padx=5)
            gen_unique_out_name_checkbox.grid(row=5, column=1, pady=ADV_SET_VERT_PAD_INT, padx=5, sticky="w")
            
            # outfile abbreviations
            out_file_abb_label_header = tk.Label(setting_root, text="Outfile Conversion Key", font=SMALL_FONT_TYPE)
            # game_master
            out_file_abb_label_gm = tk.Label(setting_root, text=SEARCH_ENUM_GAME_MASTER, font=VERY_SMALL_FONT_TYPE)
            out_file_abb_box_gm = tk.Entry(setting_root, font=VERY_SMALL_FONT_TYPE)
            out_file_abb_box_gm.insert(0, data["OUTFILE_ABBREVIATIONS"][SEARCH_ENUM_GAME_MASTER])
            # room
            out_file_abb_label_rm = tk.Label(setting_root, text=SEARCH_ENUM_ROOM, font=VERY_SMALL_FONT_TYPE)
            out_file_abb_box_rm = tk.Entry(setting_root, font=VERY_SMALL_FONT_TYPE)
            out_file_abb_box_rm.insert(0, data["OUTFILE_ABBREVIATIONS"][SEARCH_ENUM_ROOM])
            # group_size
            out_file_abb_label_gz = tk.Label(setting_root, text=SEARCH_ENUM_GROUP_SIZE, font=VERY_SMALL_FONT_TYPE)
            out_file_abb_box_gz = tk.Entry(setting_root, font=VERY_SMALL_FONT_TYPE)
            out_file_abb_box_gz.insert(0, data["OUTFILE_ABBREVIATIONS"][SEARCH_ENUM_GROUP_SIZE])
            # escaped
            out_file_abb_label_es = tk.Label(setting_root, text=SEARCH_ENUM_ESCAPED, font=VERY_SMALL_FONT_TYPE)
            out_file_abb_box_es = tk.Entry(setting_root, font=VERY_SMALL_FONT_TYPE)
            out_file_abb_box_es.insert(0, data["OUTFILE_ABBREVIATIONS"][SEARCH_ENUM_ESCAPED])
            # TIME_REMAINING
            out_file_abb_label_tm = tk.Label(setting_root, text="TIME_REMAINING", font=VERY_SMALL_FONT_TYPE)
            out_file_abb_box_tm = tk.Entry(setting_root, font=VERY_SMALL_FONT_TYPE)
            out_file_abb_box_tm.insert(0, data["OUTFILE_ABBREVIATIONS"]["TIME_REMAINING"])
            # TRUE
            out_file_abb_label_true = tk.Label(setting_root, text="TRUE", font=VERY_SMALL_FONT_TYPE)
            out_file_abb_box_true = tk.Entry(setting_root, font=VERY_SMALL_FONT_TYPE)
            out_file_abb_box_true.insert(0, data["OUTFILE_ABBREVIATIONS"]["TRUE"])
            # FALSE
            out_file_abb_label_false = tk.Label(setting_root, text="FALSE", font=VERY_SMALL_FONT_TYPE)
            out_file_abb_box_false = tk.Entry(setting_root, font=VERY_SMALL_FONT_TYPE)
            out_file_abb_box_false.insert(0, data["OUTFILE_ABBREVIATIONS"]["FALSE"])

            toggle_outfile_abb_visibility()  # will grid them if necessary 

            search_btn_label = tk.Label(setting_root, text="Search Button Color", font=MEDIUM_FONT_TYPE)
            search_btn_box = tk.Entry(setting_root, font=MEDIUM_FONT_TYPE)
            search_btn_label.grid(row=15, column=0, pady=ADV_SET_VERT_PAD_INT, padx=5)
            search_btn_box.grid(row=15, column=1, pady=ADV_SET_VERT_PAD_INT, padx=5)
            search_btn_box.insert(0, data["SEARCH_BTN_COLOR"])

            delete_btn_label = tk.Label(setting_root, text="Delete Button Color", font=MEDIUM_FONT_TYPE)
            delete_btn_box = tk.Entry(setting_root, font=MEDIUM_FONT_TYPE)
            delete_btn_label.grid(row=16, column=0, pady=ADV_SET_VERT_PAD_INT, padx=5)
            delete_btn_box.grid(row=16, column=1, pady=ADV_SET_VERT_PAD_INT, padx=5)
            delete_btn_box.insert(0, data["DELETE_BTN_COLOR"])

            parse_btn_label = tk.Label(setting_root, text="Parse Button Color", font=MEDIUM_FONT_TYPE)
            parse_btn_box = tk.Entry(setting_root, font=MEDIUM_FONT_TYPE)
            parse_btn_label.grid(row=17, column=0, pady=ADV_SET_VERT_PAD_INT, padx=5)
            parse_btn_box.grid(row=17, column=1, pady=ADV_SET_VERT_PAD_INT, padx=5)
            parse_btn_box.insert(0, data["PARSE_BTN_COLOR"])

            open_btn_label = tk.Label(setting_root, text="Open Button Color", font=MEDIUM_FONT_TYPE)
            open_btn_box = tk.Entry(setting_root, font=MEDIUM_FONT_TYPE)
            open_btn_label.grid(row=18, column=0, pady=ADV_SET_VERT_PAD_INT, padx=5)
            open_btn_box.grid(row=18, column=1, pady=ADV_SET_VERT_PAD_INT, padx=5)
            open_btn_box.insert(0, data["OPEN_BTN_COLOR"])

            setting_btn_label = tk.Label(setting_root, text="Setting Button Color", font=MEDIUM_FONT_TYPE)
            setting_btn_box = tk.Entry(setting_root, font=MEDIUM_FONT_TYPE)
            setting_btn_label.grid(row=19, column=0, pady=ADV_SET_VERT_PAD_INT, padx=5)
            setting_btn_box.grid(row=19, column=1, pady=ADV_SET_VERT_PAD_INT, padx=5)
            setting_btn_box.insert(0, data["SETTING_BTN_COLOR"])

            restore_def_btn_label = tk.Label(setting_root, text="Restore Defaults Button Color", font=MEDIUM_FONT_TYPE)
            restore_def_btn_box = tk.Entry(setting_root, font=MEDIUM_FONT_TYPE)
            restore_def_btn_label.grid(row=20, column=0, pady=ADV_SET_VERT_PAD_INT, padx=5)
            restore_def_btn_box.grid(row=20, column=1, pady=ADV_SET_VERT_PAD_INT, padx=5)
            restore_def_btn_box.insert(0, data["RESTR_CNFG_BTN_COLOR"])

            save_set_btn_label = tk.Label(setting_root, text="Save Settings Button Color", font=MEDIUM_FONT_TYPE)
            save_set_btn_box = tk.Entry(setting_root, font=MEDIUM_FONT_TYPE)
            save_set_btn_label.grid(row=21, column=0, pady=ADV_SET_VERT_PAD_INT, padx=5)
            save_set_btn_box.grid(row=21, column=1, pady=ADV_SET_VERT_PAD_INT, padx=5)
            save_set_btn_box.insert(0, data["SAVE_STNGS_BTN_COLOR"])
            
            open_er_btn_label = tk.Label(setting_root, text="Open Escape Rates Button Color", font=MEDIUM_FONT_TYPE)
            open_er_btn_box = tk.Entry(setting_root, font=MEDIUM_FONT_TYPE)
            open_er_btn_label.grid(row=22, column=0, pady=ADV_SET_VERT_PAD_INT, padx=5)
            open_er_btn_box.grid(row=22, column=1, pady=ADV_SET_VERT_PAD_INT, padx=5)
            open_er_btn_box.insert(0, data["OPEN_ESCAPERATE_BTN_COLOR"])

            bad_colors = []
            valid_color, accessed_color = is_valid_color(root, data["RESTR_CNFG_BTN_COLOR"])
            if not valid_color:
                bad_colors.append(data["RESTR_CNFG_BTN_COLOR"])
            restore_default_btn = tk.Button(setting_root, text="Restore Defaults", 
                                        command=restore_defaults, 
                                            bg=accessed_color,
                                                font=LARGE_FONT_TYPE)
            restore_default_btn.grid(row=23, column=0, pady=ADV_SET_VERT_PAD_INT, padx=5)

            valid_color, accessed_color = is_valid_color(root, data["SAVE_STNGS_BTN_COLOR"])
            if not valid_color:
                bad_colors.append(data["SAVE_STNGS_BTN_COLOR"])
            save_settings_btn = tk.Button(setting_root, text="Save Current\nSettings", 
                                        command=save_current_settings, 
                                            bg=accessed_color,
                                                font=LARGE_FONT_TYPE)
            save_settings_btn.grid(row=23, column=1, pady=ADV_SET_VERT_PAD_INT, padx=5)
            output_bad_colors(bad_colors, result_label)
            
            setting_root.bind("<Destroy>", on_destroy)
            setting_root.mainloop()


    def clear_files():
        # initialize constants
        config_path = os.path.join(CONFIG_FILE_NAME)
        with open(config_path, 'r') as config_info:
            data = json.load(config_info)
        output_folder_path_str = data["OUTPUT_FOLDER_PATH"]

        files_in_directory = os.listdir(f"{output_folder_path_str}")
        files_deleted = 0
        for each_file in files_in_directory:
            if each_file.endswith(".json"):
                file_path = os.path.join(output_folder_path_str, each_file)
                os.remove(file_path)
                files_deleted += 1
        repl_tup = (files_deleted, output_folder_path_str)
        if files_deleted == 0:
            out_msg = format_output_str(DEL_FILES_NO_FILES_STR, repl_tup)
        elif files_deleted == 1:
            out_msg = format_output_str(DEL_FILES_ONE_FILE_STR, repl_tup)
        else:
            out_msg = format_output_str(DEL_FILES_MULT_FILES_STR, repl_tup)
        set_result_status(out_msg, result_label)
        set_open_button(False)

    def test_function():
        print("test")

    # initialize constants
    config_path = os.path.join(CONFIG_FILE_NAME)
    with open(config_path, 'r') as config_info:
        data = json.load(config_info)
    parse_btn_color_str = data["PARSE_BTN_COLOR"]
    setting_btn_color_str = data["SETTING_BTN_COLOR"]
    search_btn_color_str = data["SEARCH_BTN_COLOR"]
    open_btn_color_str = data["OPEN_BTN_COLOR"]
    delete_btn_color_str = data["DELETE_BTN_COLOR"]
    escaperate_btn_color_str = data["OPEN_ESCAPERATE_BTN_COLOR"]
    output_folder_head = data["OUTPUT_FOLDER_PATH"]


    # file updater button
    valid_color = False
    wrong_colors = []
    valid_color, accessed_color = is_valid_color(root, parse_btn_color_str)
    if not valid_color:
        wrong_colors.append(parse_btn_color_str)
    
    parse_button = tk.Button(root, text="Parse CSV", 
                                 command=file_parse, 
                                     bg=accessed_color, 
                                        font=LARGE_FONT_TYPE)
    parse_button.grid(row=8, column=1, pady=10)

    valid_color, accessed_color = is_valid_color(root, setting_btn_color_str)
    if not valid_color:
        wrong_colors.append(setting_btn_color_str)
    # settings button
    advanced_settings_button = tk.Button(root, text="Open\nSettings", 
                                            command=open_advanced_settings_window, 
                                                bg=accessed_color, 
                                                font=VERY_SMALL_FONT_TYPE)
    advanced_settings_button.grid(row=8, column=1, sticky="e")

    valid_color, accessed_color = is_valid_color(root, search_btn_color_str)
    if not valid_color:
        wrong_colors.append(search_btn_color_str)
    # search button
    search_button = tk.Button(root, text="Search", 
                                  command=search, 
                                      bg=accessed_color, 
                                        font=HUGE_FONT_TYPE)
    search_button.grid(row=9, column=1, pady=10)
    
    valid_color, accessed_color = is_valid_color(root, open_btn_color_str)
    if not valid_color:
        wrong_colors.append(open_btn_color_str)
    # open file button
    open_file_button = tk.Button(root, text="Open\nFile", 
                                     command=open_file, 
                                         bg=accessed_color,
                                             font=VERY_SMALL_FONT_TYPE)
    
    # open_file_button will grid when valid output is received

    valid_color, accessed_color = is_valid_color(root, escaperate_btn_color_str)
    if not valid_color:
        wrong_colors.append(escaperate_btn_color_str)
    open_escaperate_button = tk.Button(root, text="Open\nRates", 
                                     command=open_escaperate, 
                                         bg=accessed_color,
                                             font=VERY_SMALL_FONT_TYPE)
    # open_escaperate_button will grid when valid output is received

    #if output file exists, grid buttons
    out_file = output_folder_head
    if os.path.isfile(CACHE_FILE_NAME):
        the_outfile_name = get_value_from_cache("cur_output_filename")
        out_str = os.path.join(out_file, the_outfile_name)
        if os.path.isfile(f"{out_str}.json"):
            # grid the button
            set_open_button(True)
    
    valid_color, accessed_color = is_valid_color(root, delete_btn_color_str)
    if not valid_color:
        wrong_colors.append(delete_btn_color_str)
    # delete file button
    file_clear_button = tk.Button(root, text="Delete\nOutput", 
                                      command=clear_files, 
                                          bg=accessed_color,
                                             font=VERY_SMALL_FONT_TYPE)
    file_clear_button.grid(row=9, column=1, sticky="e")

    # check if wrong colors
    output_bad_colors(wrong_colors, result_label)

    test_button = tk.Button(root, text="test", command=test_function)
    #test_button.grid(row=0, column=1, sticky="ne")

    root.mainloop()               

if __name__ == "__main__":
    tk_main()