import json

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
            
                

main()