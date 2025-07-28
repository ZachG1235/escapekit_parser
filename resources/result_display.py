import tkinter as tk
import json, os, webbrowser
from .immutable_constants import *
from .utils import format_output_str

def show_results(file_grab_name: str, show_rank : bool):
    root = tk.Toplevel()
    root.title("EscapeKit Parser: Results")
    horizontal_pixels = 990
    if show_rank:
        horizontal_pixels += 35
    root.geometry(f"{horizontal_pixels}x600")  
    config_path = os.path.join(CONFIG_FILE_NAME)
    with open(config_path, 'r') as config_info:
        data = json.load(config_info)
    max_displayed_entries = int(data["MAX_DISPLAYABLE_ENTRIES"])

    # scroll region
    canvas = tk.Canvas(root)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    config_path = os.path.join(CONFIG_FILE_NAME)
    with open(config_path, 'r') as config_info:
        data = json.load(config_info)
    output_folder = data["OUTPUT_FOLDER_PATH"]

    output_filestr = os.path.join(output_folder, file_grab_name)
    with open(f"{output_filestr}.json", 'r') as fileObj:
        json_data = json.load(fileObj)
    if len(json_data) < 1:
        return

    # header
    for i in range(0, 9):
        scrollable_frame.grid_columnconfigure(i, minsize=20)

    test_label = tk.Label(scrollable_frame, text="", font=SMALL_FONT_TYPE)
    test_label.grid(row=0, column=0, padx=5, pady=1)
    first_entry = list(json_data)[0]
    index = 0
    if show_rank:
        number_header_label = tk.Label(scrollable_frame, text="#", font=LARGE_FONT_TYPE)
        number_header_label.grid(row=0, column=index, padx=5, pady=3)
        index += 1
    for each_data in json_data[first_entry]:
        if each_data != "status":
            displayable_data = each_data.replace('_', ' ').title()
            if each_data == "players":
                displayable_data = "URL"
            current_label = tk.Label(scrollable_frame, text=displayable_data, font=LARGE_FONT_TYPE)
            current_label.grid(row=0, column=index, padx=5, pady=3)
            index += 1

    def url_redirect(group_id: str, is_event: bool):
        if is_event:
            group_id += "/event"
        url = "https://www.escapekit.co/groups/" + group_id
        webbrowser.open_new(url)

    row_index = 1
    group_display_total = 0
    for each_group in json_data:
        col_index = 0
        scrollable_frame.grid_rowconfigure(row_index, minsize=25)
        if group_display_total > max_displayed_entries:
            out_msg = format_output_str(DISPLAY_HANDLER_CUTOFF_STR, (max_displayed_entries, len(json_data)))
            data_label = tk.Label(scrollable_frame, text=out_msg, font=VERY_LARGE_FONT_TYPE)
            span_amount = 9
            if show_rank:
                span_amount += 1
            data_label.grid(row=row_index, column=col_index, padx=5, pady=0, columnspan=span_amount)
            break
        # if bool to show rank, use first column to show rank
        if show_rank:
            number_label = tk.Label(scrollable_frame, text=row_index, font=SMALL_FONT_TYPE)
            number_label.grid(row=row_index, column=col_index, padx=0, pady=0)
            col_index += 1
        for each_data in json_data[each_group]:
            if each_data != "status":
                displayable_data = json_data[each_group][each_data]
                if each_data == SEARCH_ENUM_ESCAPED:
                    displayable_data = str(displayable_data == 1)
                if each_data == "players":
                    is_group = json_data[each_group].get(SEARCH_ENUM_GAME_MASTER) == EVENT_GM_CONVERSION_LITERAL
                    data_button = tk.Button(scrollable_frame, text="Link", font=SMALL_FONT_TYPE,
                                            command=lambda v=each_group, b=is_group: url_redirect(v, b))
                    data_button.grid(row=row_index, column=col_index, padx=0, pady=0)
                else:
                    data_label = tk.Label(scrollable_frame, text=displayable_data, font=SMALL_FONT_TYPE, wraplength=200)
                    data_label.grid(row=row_index, column=col_index, padx=0, pady=0)
                col_index += 1
        row_index += 1
        group_display_total += 1

    root.mainloop()

