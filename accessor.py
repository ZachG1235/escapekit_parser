import json
import tkinter as tk
from file_updater import parse_line

WINDOW_X = 1000
WINDOW_Y = 800


def search_and_write(section_to_search : str, key_user_searched : str):
    found_data = {}
    user_key_fixed = str(key_user_searched.lower().strip())
    searching_number = section_to_search == "group_size" # or (insert more here)
    with open("players.json", 'r') as fileObj:
        json_data = json.load(fileObj)
    with open("output/output.json", 'w') as out_file:
        for each_group in json_data:
            if searching_number and str(json_data[each_group][section_to_search]).lower() == user_key_fixed:
                found_data[each_group] = json_data[each_group]
            elif not searching_number and (str(json_data[each_group][section_to_search]).lower() == user_key_fixed or \
                    str(json_data[each_group][section_to_search]).lower().startswith(user_key_fixed) or \
                    str(json_data[each_group][section_to_search]).lower().endswith(user_key_fixed) or \
                    str(json_data[each_group][section_to_search]).lower().find(user_key_fixed) != -1):
                found_data[each_group] = json_data[each_group]
        out_file.write(json.dumps(found_data, indent=4))

def sort_and_write(section_to_sort : str, least_to_greatest : bool):
    with open("players.json", 'r') as fileObj:
        json_data = json.load(fileObj)
    sorted_data = dict(sorted(json_data.items(), key=lambda item: item[1][section_to_sort], reverse=least_to_greatest))
    with open("output/output.json", 'w') as out_file:
        out_file.write(json.dumps(sorted_data, indent=4))

def sort_and_write_multiple(sort_array : list):
    with open("players.json", 'r') as file_raw:
        file_lines = json.load(file_raw)
    sort_key_order = []
    for each_index in sort_array:
        if each_index != "N/A":
            sort_key_order.append(each_index)

    sorted_data = dict()
    if len(sort_key_order) == 1:
        sorted_data = dict(
            sorted(
                file_lines.items(), key=lambda item: (item[1][sort_key_order[0]])
            )
        )
    elif len(sort_key_order) == 2:
        sorted_data = dict(
            sorted(
                file_lines.items(), key=lambda item: (item[1][sort_key_order[1]], 
                                                      item[1][sort_key_order[0]])
            )
        )
    elif len(sort_key_order) == 3:
        sorted_data = dict(
            sorted(
                file_lines.items(), key=lambda item: (item[1][sort_key_order[0]],
                                                      item[1][sort_key_order[1]], 
                                                      item[1][sort_key_order[2]])
            )
        )
    elif len(sort_key_order) == 4:
        sorted_data = dict(
            sorted(
                file_lines.items(), key=lambda item: (item[1][sort_key_order[0]], 
                                                      item[1][sort_key_order[1]],
                                                      item[1][sort_key_order[2]],
                                                      item[1][sort_key_order[3]])
            )
        )
    elif len(sort_key_order) == 5:
        sorted_data = dict(
            sorted(
                file_lines.items(), key=lambda item: (item[1][sort_key_order[0]], 
                                                      item[1][sort_key_order[1]],
                                                      item[1][sort_key_order[2]],
                                                      item[1][sort_key_order[3]],
                                                      item[1][sort_key_order[4]])
            )
        )
    else:
        print("There was an error sorting the data.")
    
    with open("output/output.json", 'w') as out_file:
        out_file.write(json.dumps(sorted_data, indent=4))

def get_room_names() -> list:
    formatted_line = []
    with open("players.csv", 'r') as raw_file:
        line = raw_file.readline()
        formatted_line = parse_line(line)
    room_list = []
    for each_header in formatted_line:
        if each_header.find(": Date") != -1 and not each_header.split(':')[0] in room_list:
            room_list.append(each_header.split(':')[0])
    return room_list


def main():
    user_input = "dummy"
    search_key = "dummy"
    
    while user_input[0] != "q":
        user_input = input("What will you do?\n"
                           "1. Select by Game Master\n"
                           "2. Select by Room\n"
                           "3. Select by Player Count\n"
                           "4. Select by Escaped Rooms\n"
                           "5. Sort by Escape Time Remaining\n"
                           "Enter (Q)uit to exit program\n"
                           " > ")
        if user_input.lower() == "master" or user_input[0] == "1":
            search_key = "game_master"
            user_input = input("Who?\n > ")
            search_and_write(search_key, user_input)
        elif user_input.lower() == "room" or user_input[0] == "2":
            search_key = "room"
            user_input = input("Which room?\n > ")
            search_and_write(search_key, user_input)
        elif user_input.lower() == "count" or user_input[0] == "3":
            search_key = "group_size"
            user_input = input("How many players?\n > ")
            search_and_write(search_key, user_input)
        elif user_input.lower() == "escaped" or user_input[0] == "4":
            search_key = "escaped"
            user_input = "true"
            search_and_write(search_key, user_input)
        elif user_input.lower() == "remaining" or user_input[0] == "5":
            search_key = "time_remaining"
            least_to_greatest = True
            sort_and_write(search_key, least_to_greatest)
            
def tk_main():
    root = tk.Tk()

    root.title("My Tkinter Window")
    root.geometry(f"{WINDOW_X}x{WINDOW_Y}")

    room_dropdown_labels = get_room_names() # get rooms
    room_dropdown_selection = tk.StringVar()
    room_dropdown_selection.set(room_dropdown_labels[0])

    section_dropdown_labels = ["N/A", "game_master", "room", "group_size", "time_remaining"]
    section_dropdown_selection = tk.StringVar()
    section_dropdown_selection.set(section_dropdown_labels[0])
    section_dropdown_selection_list = []

    gm_check_bool = tk.BooleanVar()
    room_check_bool = tk.BooleanVar()
    tm_check_bool = tk.BooleanVar()
    gz_check_bool = tk.BooleanVar()
    
    def toggle_gm_box():
        if gm_check_bool.get():
            gm_label.grid(row=1, column=1, padx=10, pady=5)
            gm_box.grid(row=2, column=1, padx=10, pady=5)
        else:
            gm_label.grid_remove()
            gm_box.grid_remove()

    def toggle_room_box():
        if room_check_bool.get():
            room_dropdown.grid(row=1, column=2, padx=10, pady=5)
        else:
            room_dropdown.grid_remove()

    def toggle_gz_box():
        if gz_check_bool.get():
            gz_label.grid(row=1, column=3, padx=10, pady=5)
            gz_box.grid(row=2, column=3, padx=10, pady=5)
        else:
            gz_label.grid_remove()
            gz_box.grid_remove()

    gm_check_box = tk.Checkbutton(root, text="Game Master", variable=gm_check_bool, command=toggle_gm_box)
    gm_check_box.grid(row=0, column=1, padx=10, pady=10)
    gm_label = tk.Label(root, text="Enter Game Master name:")
    gm_box = tk.Entry(root)

    room_check_box = tk.Checkbutton(root, text="Room Name", variable=room_check_bool, command=toggle_room_box)
    room_check_box.grid(row=0, column=2, padx=10, pady=10)
    room_dropdown = tk.OptionMenu(root, room_dropdown_selection, *room_dropdown_labels)

    gz_check_box = tk.Checkbutton(root, text="Group Size", variable=gz_check_bool, command=toggle_gz_box)
    gz_check_box.grid(row=0, column=3, padx=10, pady=10)
    gz_label = tk.Label(root, text="Enter Group Size:")
    gz_box = tk.Entry(root)

    for i in range(0, len(section_dropdown_labels)-1):
        new_dropdown_value_holder = tk.StringVar()
        new_dropdown = tk.OptionMenu(root, new_dropdown_value_holder, *section_dropdown_labels)
        new_dropdown.grid(row=i, column=0, padx=10, pady=10)
        new_dropdown_value_holder.set(section_dropdown_labels[0])
        section_dropdown_selection_list.append(new_dropdown_value_holder)

    def search():
        if room_check_bool.get():
            search_key = "room"
            room_name_to_search = room_dropdown_selection.get()
            search_and_write(search_key, room_name_to_search)
            result_label.config(text=f"{search_key.title()} '{room_name_to_search}' searched and written to 'output.txt'.")
        elif gm_check_bool.get():
            select_list = []
            for each_var in section_dropdown_selection_list:
                select_list.append(each_var.get())
            sort_and_write_multiple(select_list)


    update_button = tk.Button(root, text="Update", command=search)
    update_button.grid(row=5, column=3, pady=10)
    
    result_label = tk.Label(root, text="")
    result_label.grid(row=5, column=4, pady=10)


    root.mainloop()               

if __name__ == "__main__":
    tk_main()