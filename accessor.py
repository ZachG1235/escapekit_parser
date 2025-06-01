import json

def main():
    user_input = "dummy"
    with open("players.json", 'r') as fileObj:
        json_data = json.load(fileObj)
    while user_input[0] != "q":
        user_input = input("What will you do?\n > ")
        if user_input.lower() == "master":
            user_input = input("Who?\n > ")
            found_data = {}
            with open("output/output.txt", 'w') as out_file:
                for each_group in json_data:
                    if json_data[each_group]["game_master"].lower() == user_input.lower().strip():
                        found_data[each_group] = json_data[each_group]
                out_file.write(json.dumps(found_data, indent=4))

main()