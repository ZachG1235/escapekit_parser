import json, os
import tkinter as tk
from file_updater import parse_line, update_escape_groups

INPUT_FOLDER_PATH = "input"
INPUT_FILENAME = "players"
OUTPUT_FOLDER_PATH = "output"

def search_and_sort(key_tuples : list, sort_tuple : tuple) -> int:
    with open(f"{INPUT_FOLDER_PATH}/{INPUT_FILENAME}.json", 'r') as fileObj:
        json_data = json.load(fileObj)
    found_data = {}

    for each_group in json_data:
        matching_search = 0
        for each_tuple in key_tuples:
            tup_key, tup_value = each_tuple
            if tup_key == "group_size":
                if int(json_data[each_group][tup_key]) == int(tup_value):
                    matching_search += 1
            elif tup_key == "escaped":
                if json_data[each_group][tup_key]:
                    matching_search += 1
            else:
                tup_value = tup_value.lower()
                compare_value = json_data[each_group][tup_key].lower()
                if compare_value.find(tup_value) != -1:
                    matching_search += 1
        if matching_search == len(key_tuples):
            found_data[each_group] = json_data[each_group]

    if len(sort_tuple) > 0:
        sort_key, sort_bool = sort_tuple
        sort_bool = not sort_bool # originally asked for least to greatest, inverting it is actually least to greatest
        found_data = dict(sorted(found_data.items(), key=lambda item: item[1][sort_key], reverse=sort_bool))

    
    out_file_str = ""
    for each_tuple in key_tuples:
        first_tuple, second_tuple = each_tuple
        first_tuple = str(first_tuple).lower()
        second_tuple = str(second_tuple).replace(' ', '_')
        try:
            second_tuple = second_tuple.upper()
        except:
            second_tuple = second_tuple

        each_tuple = f"{first_tuple}{second_tuple}"
        tuple_str = str(each_tuple)
        for each_letter in tuple_str:
            if each_letter.isalnum() or each_letter == '_':
                out_file_str += each_letter
    if len(sort_tuple) > 0:
        first_tuple, second_tuple = sort_tuple
        out_file_str += f"sort{first_tuple.upper()}ltg{str(second_tuple).upper()}"
    with open(f"{OUTPUT_FOLDER_PATH}/{out_file_str}.json", 'w') as out_file:
        out_file.write(json.dumps(found_data, indent=4))

    return len(found_data)
        
def get_room_names() -> list:
    formatted_line = []
    room_list = []
    input_file_path = f"{INPUT_FOLDER_PATH}/{INPUT_FILENAME}.csv"
    if os.path.isfile(input_file_path):
        with open(f"{INPUT_FOLDER_PATH}/{INPUT_FILENAME}.csv", 'r') as raw_file:
            line = raw_file.readline()
            formatted_line = parse_line(line)
        for each_header in formatted_line:
            if each_header.find(": Date") != -1 and not each_header.split(':')[0] in room_list:
                room_list.append(each_header.split(':')[0])
    else:
        room_list.append("N/A")
    return room_list
            
def tk_main():
    root = tk.Tk()
    root.title("EscapeKit Parser: Made by ZachG1235")
    for i in range(0, 10):
        root.grid_rowconfigure(i, minsize=55)
    for j in range(0, 2):
        root.grid_columnconfigure(j, minsize=220)

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
    gm_check_box = tk.Checkbutton(root, text="Game Master", variable=gm_check_bool, command=toggle_gm_box, font=("Sitka Small", 11))
    gm_check_box.grid(row=0, column=0, padx=10, pady=10, rowspan=2)
    gm_label = tk.Label(root, text="Enter game master name:", font=("Sitka Small", 10))
    gm_box = tk.Entry(root, font=("Sitka Small", 10))

    # room name checkbox and dropdown
    room_check_box = tk.Checkbutton(root, text="Room Name", variable=room_check_bool, command=toggle_room_box, font=("Sitka Small", 11))
    room_check_box.grid(row=2, column=0, padx=10, pady=10, rowspan=2)
    room_dropdown = tk.OptionMenu(root, room_dropdown_selection, *room_dropdown_labels)
    room_dropdown.config(font=("Sitka Small", 10))
    room_dropdown["menu"].config(font=("Sitka Small", 10))
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
    gz_check_box = tk.Checkbutton(root, text="Group Size", variable=gz_check_bool, command=toggle_gz_box, font=("Sitka Small", 11))
    gz_check_box.grid(row=4, column=0, padx=10, pady=10, rowspan=2)
    gz_label = tk.Label(root, text="Enter group size:", font=("Sitka Small", 10))
    gz_box = tk.Entry(root, font=("Sitka Small", 10))

    # sort by checkbox and dropdown
    sort_check_box = tk.Checkbutton(root, text="Sort by", variable=sort_check_bool, command=sort_box, font=("Sitka Small", 11))
    sort_check_box.grid(row=6, column=0, padx=10, pady=10, rowspan=2)
    sort_dropdown = tk.OptionMenu(root, sort_dropdown_selection, *sort_dropdown_labels)
    sort_dropdown.config(font=("Sitka Small", 10))
    sort_dropdown["menu"].config(font=("Sitka Small", 10))
    ltg_check_box = tk.Checkbutton(root, text="Sort Least to Greatest?", variable=ltg_check_bool, font=("Sitka Small", 9))

    # checkbox for escaped groups
    escaped_check_box = tk.Checkbutton(root, text="Only show escaped rooms", variable=escaped_check_bool, font=("Sitka Small", 8))
    escaped_check_box.grid(row=8, column=0, padx=10, pady=10)

    # result displaying label
    result_label = tk.Label(root, text="", font=("Sitka Small", 8), wraplength=200)
    result_label.grid(row=9, column=0, pady=10)

    # function to start the search process (activates on Update Button)
    def search():
        search_queries = []
        sort_query = ()
        something_selected = False

        if gm_check_bool.get():
            game_master_to_search = gm_box.get()
            if len(game_master_to_search) > 0:
                search_queries.append(("game_master", game_master_to_search))
                something_selected = True
        if room_check_bool.get():
            room_name_to_search = room_dropdown_selection.get()
            search_queries.append(("room", room_name_to_search))
            something_selected = True
        if gz_check_bool.get():
            group_size_to_search = gz_box.get()
            if len(group_size_to_search) > 0:
                search_queries.append(("group_size", group_size_to_search))
                something_selected = True
        if sort_check_bool.get():
            sort_selection = sort_dropdown_selection.get()
            least_to_greatest_bool = ltg_check_bool.get()
            sort_selection = sort_selection.lower().replace("name", '').strip().replace(' ', '_')
            sort_query = (sort_selection, least_to_greatest_bool)
            something_selected = True
        if escaped_check_bool.get():
            search_queries.append(("escaped", True))
            something_selected = True

        if something_selected:
            amount_found = search_and_sort(search_queries, sort_query)
            result_label.config(text=f"Searched and found {amount_found} results")
        else:
            result_label.config(text="Nothing selected")

    def file_parse():
        in_file_name = f"{INPUT_FOLDER_PATH}/{INPUT_FILENAME}.csv"
        out_file_name = f"{INPUT_FOLDER_PATH}/{INPUT_FILENAME}.json"
        success = update_escape_groups(in_file_name, out_file_name)
        if not success:
            result_label.config(text=f"Could not find \"{INPUT_FOLDER_PATH}/{INPUT_FILENAME}.csv\"")
        else:
            update_dropdowns()
            result_label.config(text=f"Successfully parsed \"{INPUT_FOLDER_PATH}/{INPUT_FILENAME}.csv\"")
        

    # file updater button
    search_button = tk.Button(root, text="Parse CSV", command=file_parse, bg="darkolivegreen1", font=("Sitka Small", 11))
    search_button.grid(row=8, column=1, pady=10)

    # search button
    search_button = tk.Button(root, text="Search", command=search, bg="royalblue1", font=("Sitka Small", 16))
    search_button.grid(row=9, column=1, pady=10)
    

    root.mainloop()               

if __name__ == "__main__":
    tk_main()