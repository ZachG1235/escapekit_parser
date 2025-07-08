from resources.app_main import tk_main
import sys, os, json
from resources.immutable_constants import *


if __name__ == "__main__":
    run_program = True
    if len(sys.argv) > 1:
        arg_list = []
        for arg in sys.argv[1:]:
            arg_list.append(arg.lower())
        if "-donly" in arg_list or "-d" in arg_list:
            if "-donly" in arg_list:
                run_program = False
            # reset program to original
            # get config's folders
            input_folder_path_str = "input"
            input_filename_str = "players"
            output_folder_path_str = "output"
            config_path = os.path.join(CONFIG_FILE_NAME)
            if os.path.isfile(config_path):
                with open(config_path, 'r') as config_info:
                    data = json.load(config_info)
                input_folder_path_str = data["INPUT_FOLDER_PATH"]
                input_filename_str = data["INPUT_FILENAME"]
                output_folder_path_str = data["OUTPUT_FOLDER_PATH"]
            
            # delete input/players.json in input
            parsed_file = os.path.join(input_folder_path_str, f"{input_filename_str}.json")
            if os.path.isfile(parsed_file):
                os.remove(parsed_file)
                print(f"File \"{parsed_file}\" has been removed.")

            # delete output/*.json
            output_folder_path_str = os.path.join(output_folder_path_str)
            files_in_directory = os.listdir(f"{output_folder_path_str}")
            for each_file in files_in_directory:
                if each_file.endswith(".json"):
                    file_path = os.path.join(output_folder_path_str, each_file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        print(f"File \"{file_path}\" has been removed.")

            # delete cache.txt
            cache_file = os.path.join(CACHE_FILE_NAME)
            if os.path.isfile(cache_file):
                os.remove(cache_file)
                print(f"File \"{cache_file}\" has been removed.")

            # delete config.json
            config_file = os.path.join(CONFIG_FILE_NAME)
            if os.path.isfile(config_file):
                os.remove(config_file)
                print(f"File \"{config_file}\" has been removed.")
    
    if run_program:
        tk_main()