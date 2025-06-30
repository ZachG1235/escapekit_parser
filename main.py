from resources.accessor import tk_main
import sys, os


if __name__ == "__main__":
    run_program = True
    if len(sys.argv) > 1:
        arg_list = []
        for arg in sys.argv[1:]:
            arg_list.append(arg)
        if "-donly" in arg_list or "-d" in arg_list:
            if "-donly" in arg_list:
                run_program = False
            # reset program to original
            # delete input/players.json in input
            parsed_file = os.path.join("input", "players.json")
            if os.path.isfile(parsed_file):
                os.remove(parsed_file)
                print(f"File \"{parsed_file}\" has been removed.")

            # delete output/*.json
            output_folder_path_str = os.path.join("output")
            files_in_directory = os.listdir(f"{output_folder_path_str}")
            for each_file in files_in_directory:
                if each_file.endswith(".json"):
                    file_path = os.path.join(output_folder_path_str, each_file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        print(f"File \"{file_path}\" has been removed.")

            # delete cache.txt
            cache_file = os.path.join("cache.txt")
            if os.path.isfile(cache_file):
                os.remove(cache_file)
                print(f"File \"{cache_file}\" has been removed.")

            # delete config.json
            config_file = os.path.join("config.json")
            if os.path.isfile(config_file):
                os.remove(config_file)
                print(f"File \"{config_file}\" has been removed.")
    
    if run_program:
        tk_main()