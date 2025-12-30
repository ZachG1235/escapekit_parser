import json
from pathlib import Path
from datetime import datetime, time
from resources.immutable_constants import *
from resources.app_main import check_for_config_init, search_and_sort
from resources.file_parser import update_escape_groups
import tkinter as tk
from tkcalendar import DateEntry

# only accepts positive integers (0 inclusive)
def ask_int_question(query_str : str) -> int:
    user_str = input(query_str).strip()
    while not user_str.isdigit():
        user_str = input(f"Input invalid. {query_str}").strip()
    return int(user_str)

def parse_dates(input_path : Path, before_date : datetime, after_date : datetime):
    trends_dict = {}

    # get data from output\trends.json
    data_dict = {}
    with open(input_path, 'r') as data_file:
        data_dict = json.load(data_file)
    # init metadata in dict
    trends_dict["metadata"] = {
        "id" : 0,
        "total_games" : 0, 
        "before_date" : before_date.strftime("%m/%d/%Y"), 
        "after_date" : after_date.strftime("%m/%d/%Y")
    }
    # iterate through all games
    for game_id in data_dict:
        room_date = data_dict[game_id]["room_date"]
        room_time = data_dict[game_id]["room_time"]
        # if room is an event
        if room_time == EVENT_ROOM_TIME_CONVERSION_LITERAL:
            # defaults to noon
            room_time = "12:00:00"
        # convert to datetime
        room_datetime = datetime.strptime(f"{room_date} {room_time}", "%Y-%m-%d %H:%M:%S")
        # if between input dates 
        if before_date <= room_datetime <= after_date:
            # add 1 total game to metadata
            trends_dict["metadata"]["total_games"] += 1
            # try incrementing the total_games key in the day of the week
            try:
                trends_dict[room_datetime.strftime("%A").lower()]["total_games"] += 1
            # if failed, there most likely isn't a day of week index in dict. initialize it
            except KeyError:
                trends_dict[room_datetime.strftime("%A").lower()] = {
                    "id" : room_datetime.isoweekday(),
                    "total_games" : 1,
                    "games" : {}
                }
            # try incrementing the room from the week's game's index. 
            try:
                trends_dict[room_datetime.strftime("%A").lower()]["games"][data_dict[game_id]["room"]] += 1
            # if failed, there most likely isn't a game's name in the game's dict. init it
            except KeyError:
                trends_dict[room_datetime.strftime("%A").lower()]["games"][data_dict[game_id]["room"]] = 1
            # check to see if it's after 4pm
            if room_datetime.time() >= time(16, 0):
                # try incrementing rooms that are after 4pm
                try:
                    trends_dict[room_datetime.strftime("%A").lower()]["games_after_4pm"] += 1
                except KeyError:
                    trends_dict[room_datetime.strftime("%A").lower()]["games_after_4pm"] = 1
            else:
                # try incrementing rooms that are before 4pm
                try:
                    trends_dict[room_datetime.strftime("%A").lower()]["games_before_4pm"] += 1
                except KeyError:
                    trends_dict[room_datetime.strftime("%A").lower()]["games_before_4pm"] = 1
    # sort by id key in each key's value
    sorted_data = dict(
        sorted(trends_dict.items(), key=lambda item: item[1]["id"], reverse=False)
    )
    # save to file
    with open(input_path, 'w', encoding="utf-8") as output_trends:
        json.dump(sorted_data, output_trends, indent=4)

def tk_loop(config_data : dict) -> dict:
    root = tk.Tk()
    root.title("EscapeKit Parser - Trends: Made by ZachG1235")
    root.iconbitmap("icons/ekp_transparent.ico")
    result = {"date1" : datetime(1, 1, 1), "date2" : datetime(1, 1, 1)}

    title_label = tk.Label(root, text="Trend Viewer", font=HUGE_FONT_TYPE)
    title_label.grid(row=0, column=0, columnspan=2)

    subtitle_label = tk.Label(root, text="This is a version of EscapeKit Parser that shows trends in weekdays.", font=SMALL_FONT_TYPE)
    subtitle_label.grid(row=1, column=0, columnspan=2)

    subsubtitle_label = tk.Label(root, text="Please select a date range to observe.", font=SMALL_FONT_TYPE)
    subsubtitle_label.grid(row=2, column=0, columnspan=2)

    before_label = tk.Label(root, text="1st Date: ", font=LARGE_FONT_TYPE)
    before_label.grid(row=8, column=0)
    after_label = tk.Label(root, text="2nd Date: ", font=LARGE_FONT_TYPE)
    after_label.grid(row=9, column=0)
    
    date_one_entry = DateEntry(
        root,
        width=20,
        background=config_data["SAVE_STNGS_BTN_COLOR"],
        foreground="black",
        borderwidth=10,
        date_pattern="mm/dd/yyyy",
        showweeknumbers=False,
        firstweekday="monday",
        normalbackground="white", 
        normalforeground="black", 
        weekendbackground="white", 
        weekendforeground="black", 
        othermonthbackground="#ededed",
        othermonthwebackground="#ededed",
        othermonthforeground="#737373",
        othermonthweforeground="#737373", 
        font=MEDIUM_FONT_TYPE
    )
    date_one_entry.grid(row=8, column=1, padx=10, pady=10)

    date_two_entry = DateEntry(
        root,
        width=20,
        background=config_data["SAVE_STNGS_BTN_COLOR"],
        foreground="black",
        borderwidth=10,
        date_pattern="mm/dd/yyyy",
        showweeknumbers=False,
        firstweekday="monday",
        normalbackground="white", 
        normalforeground="black", 
        weekendbackground="white", 
        weekendforeground="black", 
        othermonthbackground="#ededed",
        othermonthwebackground="#ededed",
        othermonthforeground="#737373",
        othermonthweforeground="#737373", 
        font=MEDIUM_FONT_TYPE
    )
    date_two_entry.grid(row=9, column=1, padx=10, pady=10)

    def get_date():
        result["date1"] = date_one_entry.get_date()
        result["date2"] = date_two_entry.get_date()
        root.destroy()
        
        
    submit_btn = tk.Button(root, text="Submit", command=get_date, background=config_data["SEARCH_BTN_COLOR"], font=LARGE_FONT_TYPE)
    submit_btn.grid(row=10, column=0, columnspan=2, pady=10)

    root.mainloop()

    return result



def main():
    # check if configs exist to take constants
    config = {}
    check_for_config_init()    # creates config file if not existing
    with open(CONFIG_FILE_NAME, 'r') as config_file:
        config = json.load(config_file)
    # check if player data exists
    input_folder = config["INPUT_FOLDER_PATH"]
    input_filename = config["INPUT_FILENAME"]
    output_folder = config["OUTPUT_FOLDER_PATH"]
    filepath_prefix_str = f"{input_folder}/{input_filename}"
    # does source data exist?
    if not Path(f"{filepath_prefix_str}.csv").is_file():
        # return error that input file does not exist
        return "error, file does not exist"
    # does parsed data exist?
    if not Path(f"{filepath_prefix_str}.json").is_file():
        # if it doesn't exist, parse data
        print("Parsed data does not exist. Parsing...")
        update_escape_groups(f"{filepath_prefix_str}.csv", f"{filepath_prefix_str}.json")
        print("Data parsed!")
    # otherwise, parse all player data
    amount_found, out_file_name = search_and_sort([], (), trend_override=True)
    out_path_str = Path(f"{output_folder}/{out_file_name}.json")
    print(f"Data successfully parsed & searched into \"{out_path_str}\"!")
    print("Opening Tkinter window...")
    result = tk_loop(config)
    print("...closed Tkinter window.")

    before_date_str = str(result["date1"]) + " 00:00:00"
    after_date_str = str(result["date2"]) + " 23:59:59"
    try:
        before_date = datetime.strptime(before_date_str, "%Y-%m-%d %H:%M:%S")
        after_date = datetime.strptime(after_date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        print("[ERROR] Error while parsing Tkinter dates. Program either was manually closed or is corrupt.")
        print("Closing program...")
        return -1
    
    print("Parsing Dates...")
    parse_dates(out_path_str, before_date, after_date)
    print(f"Successfully Parsed Dates! Please view \"{out_path_str}\".")






if __name__ == "__main__":
    main()


# example output
# {
#     "metadata": {
#         "id": 0,
#         "total_games": 1045,
#         "before_date": "01/01/2025",
#         "after_date": "12/31/2025"
#     },
#     "monday" : {
#         "id": 1,
#         "total_games" : 200,
#         "games" {
#             "room_1" : 120, 
#             "room_2" : 40,  
#             "room_3" : 40, 
#         }
#         "games_after_4pm" : 140,
#         "games_before_4pm" : 60
#     }, 
#     "tuesday" : {
#         ect...
#     },
# }