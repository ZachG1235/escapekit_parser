import tkinter as tk
import json, os, webbrowser

def show_results(file_grab_name : str):
    root = tk.Toplevel()
    root.title("EscapeKit Parser: Results")

    config_path = os.path.join("config.json")
    with open(config_path, 'r') as config_info:
            data = json.load(config_info)
    output_folder = data["OUTPUT_FOLDER_PATH"]

    output_filestr = os.path.join(output_folder, file_grab_name)

    with open(f"{output_filestr}.json", 'r') as fileObj:
        json_data = json.load(fileObj)
    if len(json_data) < 1:
        return # failed
    
    # header handling
    for i in range(0, 9):
        root.grid_columnconfigure(i, minsize=20)
    
    test_label = tk.Label(root, text="", font=("Sitka Small", 9))
    test_label.grid(row=0, column=0, padx=5, pady=1)
    root.update()
    bbox = root.grid_bbox()
    trash1, trash2, trash3, cell_height = bbox # type: ignore

    index = 0
    first_entry = list(json_data)[0]
    for each_data in json_data[first_entry]:
        if not each_data == "status":
            displayable_data = each_data.replace('_', ' ').title()
            if each_data == "players": 
                displayable_data = "URL"
            current_label = tk.Label(root, text=displayable_data, font=("Sitka Small", 11))
            current_label.grid(row=0, column=index, padx=5, pady=3)
        index += 1
    index = 0

    screen_height = root.winfo_screenheight()
    max_window_height = screen_height - screen_height // 4
    
    def url_redirect(group_id : str, is_event : bool):
        if is_event:
            group_id += "/event"
        url = "https://www.escapekit.co/groups/" + group_id
        webbrowser.open_new(url)


    row_index = 1
    col_index = 0
    cell_height_total = cell_height
    for each_group in json_data:
        if cell_height_total + cell_height > max_window_height: 
            break
        else:
            cell_height_total += cell_height
        root.grid_rowconfigure(row_index, minsize=25)
        for each_data in json_data[each_group]:
            if not each_data == "status":
                displayable_data = json_data[each_group][each_data]
                if each_data == "escaped":
                    displayable_data = str(json_data[each_group][each_data] == 1)
                if each_data == "players":
                    # button
                    is_group = json_data[each_group]["game_master"] == "Event GM"
                    data_button = tk.Button(root, text="Link", font=("Sitka Small", 9), command=lambda v=each_group, b=is_group: url_redirect(v, b)) 
                    data_button.grid(row=row_index, column=col_index, padx=5, pady=0)
                else:
                    data_label = tk.Label(root, text=displayable_data, font=("Sitka Small", 9))
                    data_label.grid(row=row_index, column=col_index, padx=5, pady=1)
            col_index += 1
        row_index += 1
        col_index = 0
        
    
    root.mainloop()


if __name__ == "__main__":
    show_results("output/output.json")