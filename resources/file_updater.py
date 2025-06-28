import json, random, time, os
from .constants import * # imports constants
from .utils import parse_line


def add_to_dict(dictionary : dict, cur_line : list, list_of_headers : list):
    line_group_size = 0
    try:
        line_group_size = int(cur_line[16])
    except ValueError:
        line_group_size = 0
    
    if cur_line[12] in dictionary.keys():
        # add the player
        minor_list = parse_line(cur_line[7])
        dictionary[cur_line[12]]["players"].update({
            len(dictionary[cur_line[12]]["players"].keys()) : {
                "first_name" : cur_line[0],
                "last_name" : cur_line[1],
                "email" : cur_line[2],
                "guardian_only" : cur_line[4] == "True",
                "phone_num" : cur_line[5],
                "date_of_birth" : cur_line[6],
                "minors" : minor_list,
                "date_added" : cur_line[8],
                "date_completed" : cur_line[9],
                "waiver_url" : cur_line[11],
                "group_id" : cur_line[12]
            }
        })
        # TODO calculate group size if event afterwards
        if dictionary[cur_line[12]]["game_master"] == "N/A":
            if not cur_line[4] == "True":
                dictionary[cur_line[12]]["group_size"] += 1  # if person participates, add 1
            dictionary[cur_line[12]]["group_size"] += len(minor_list) # 1 per minor
    else:
        # get room specific information
        line_room_name, line_room_date, line_room_time = get_game_data(cur_line, list_of_headers)
        # get list of minors
        minor_list = parse_line(cur_line[7])

        # if recieved "N/A" in time, game is an event
        if line_room_time == "N/A":
            line_group_name = line_room_name # set the group's name to the 31st column
            line_room_name = "Event"     # room name cannot be determined
            line_game_master = "N/A"   # game master cannot be determined 
            line_escaped = False         # escape status cannot be  determined 
            line_group_size = 0          # group size initialized to 0
            line_time_remaining = "N/A"  # time remaining cannot be determined
        else:
            line_group_name = cur_line[14]
            line_game_master = cur_line[15]
            line_escaped = cur_line[17] == "True"
            line_time_remaining = cur_line[18]

        # add the group and add the player
        dictionary[cur_line[12]] = {
            "group_name" : line_group_name,
            "status" : cur_line[13],
            "game_master" : line_game_master,
            "group_size" : line_group_size,
            "escaped" : line_escaped,
            "time_remaining" : line_time_remaining,
            "room" : line_room_name,
            "room_date" : line_room_date,
            "room_time" : line_room_time,
            "players" : {
                0 : {
                    "first_name" : cur_line[0],
                    "last_name" : cur_line[1],
                    "email" : cur_line[2],
                    "guardian_only" : cur_line[4] == "True",
                    "phone_num" : cur_line[5],
                    "date_of_birth" : cur_line[6],
                    "minors" : parse_line(cur_line[7]),
                    "date_added" : cur_line[8],
                    "date_completed" : cur_line[9],
                    "waiver_url" : cur_line[11],
                    "group_id" : cur_line[12]

                }
            }
        }

        # if event, add/subtract from group_size
        if line_game_master == "N/A":
            if not cur_line[4] == "True":
                dictionary[cur_line[12]]["group_size"] += 1  # if person participates, add 1
            dictionary[cur_line[12]]["group_size"] += len(minor_list) # 1 per minor
 
def get_game_data(line_data : list, list_of_headers : list) -> tuple:
    # returns a list [game name, game date, game time]
    if len(line_data[21]) > 0:
        return (list_of_headers[21].split(':')[0], line_data[21], line_data[22])
    elif len(line_data[23]) > 0:
        return (list_of_headers[23].split(':')[0], line_data[23], line_data[24])
    elif len(line_data[25]) > 0:
        return (list_of_headers[25].split(':')[0], line_data[25], line_data[26])
    elif len(line_data[27]) > 0:
        return (list_of_headers[27].split(':')[0], line_data[27], line_data[28])
    elif len(line_data[29]) > 0:
        return (list_of_headers[29].split(':')[0], line_data[29], line_data[30])
    else:
        # returns event name, date, and dummy data
        return (line_data[31], line_data[32], "N/A")

# # # players.csv example format   
# 0 First Name
# 1 Last Name
# 2 Email
# 3 Email Opt In
# 4 Guardian Only
# 5 Phone
# 6 DOB
# 7 Minors
# 8 Date Added
# 9 Date Completed
# 10 Tags
# 11 Waiver URL
# 12 Group ID
# 13 Group Status
# 14 Group Name
# 15 Game Master
# 16 Group Size
# 17 Did Escape?
# 18 Time Remaining
# 29 Clues
# 20 Points
# 21 Room1: Date
# 22 Room1: Time
# 23 Room2: Date
# 24 Room2: Time
# 25 Room3: Date
# 26 Room3: Time
# 27 Room4: Date
# 28 Room4: Time
# 29 Room5: Date
# 30 Room5: Time
# 31 Event: Name

def update_escape_groups(file_name="players.csv", out_file_name="players.json") -> bool:
    file_contents = []
    header_list = []
    player_dictionary = {}

    # verify file existing
    if not os.path.isfile(file_name):
        return False
    
    with open(file_name, 'r', encoding="utf8") as file_raw:
        file_contents = file_raw.readlines()
    header_list = parse_line(file_contents[0])
    for each_line in file_contents[1:]:
        formatted_line = parse_line(each_line)
        add_to_dict(player_dictionary, formatted_line, header_list)
    json_dict = json.dumps(player_dictionary, indent=4)
    with open(out_file_name, 'w', encoding="utf8") as out_file:
        for each_key in json_dict:
            out_file.write(each_key)
    
    return True

def get_sample_groups(file_name="players.csv", out_file_name="players.json", quantity=3):
    random.seed(time.time())
    file_contents = []
    header_list = []
    player_dictionary = {}
    max_iterable = 0
    random_index = 0
    with open(file_name, 'r', encoding="utf8") as file_raw:
        file_contents = file_raw.readlines()
    header_list = parse_line(file_contents[0])

    if quantity < len(file_contents) - 1:
        max_iterable = quantity
    else:
        max_iterable = len(file_contents) - 1

    for i in range(0, max_iterable):
        random_index = random.randint(1, len(file_contents)-1)
        formatted_line = parse_line(file_contents[random_index])
        add_to_dict(player_dictionary, formatted_line, header_list)
    json_dict = json.dumps(player_dictionary, indent=4)
    with open(out_file_name, 'w', encoding="utf8") as out_file:
        for each_key in json_dict:
            out_file.write(each_key)

if __name__ == "__main__":
    file_csv = INPUT_FILENAME + ".csv"
    file_json = INPUT_FILENAME + ".json"
    in_path_string = ""
    out_path_string = ""
    if os.path.exists(INPUT_FOLDER_PATH):
        in_path_string = os.path.join(INPUT_FOLDER_PATH, file_csv)
        out_path_string = os.path.join(INPUT_FOLDER_PATH, file_json)
    else: 
        in_path_string = file_csv
        out_path_string = file_json

    successful = update_escape_groups(file_name=in_path_string, out_file_name=out_path_string)
    if not successful:
        print(f"Could not find input file with path \"{in_path_string}\"")
    


# example output
# {
#     "123123": {
#        "group_name": "Star Wars Fans",
#        "status": "complete",
#        "game_master": "Gameus Mastus",
#        "group_size": 8,
#        "escaped": true,
#        "time_remaining": "0:00:34",
#        "room": "Space Adventure",
#        "room_date": "2020-01-12",
#        "room_time": "15:00:00",
#        "players": {
#            "0": {
#                "first_name": "George",
#                "last_name": "Lucas",
#                "email": "georgelucas@starwars.com",
#                "guardian_only": true,
#                "phone_num": "1111111111",
#                "date_of_birth": "1944-05-14",
#                "minors": [
#                    "Amanda Lucas",
#                    "Katie Lucas",
#                    "Jett Lucas"
#                ],
#                "date_added": "2020-01-12 14:00:25.612455-01:00",
#                "date_completed": "2020-01-12 16:00:20.845679-01:00",
#                "waiver_url": "escapekit url to go back there",
#                "group_id": "123123"
#            }, ect...