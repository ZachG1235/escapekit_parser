# EscapeKit Parser 
Welcome to a Python EscapeKit Parser made by @ZachG1235 on Github. This was a fun personal project of mine and I'm happy to have finished it.

## Setup Instructions 

### Download this Program
1. On Github, download the **latest release** of this Program.

2. Once downloaded, extract it in a **suitable location**.

### Achieving Player Data
1. Navigate to the **"Players"** tab on [escapekit.co](https://www.escapekit.co/players).

2. Click on **"Export"** and choose **"Export Players to CSV"**.
    * You can also [click here to download your data on EscapeKit](https://www.escapekit.co/players/export/?).

3. Once downloaded, put the "`players.csv`" file into the "`input`" folder in this directory.

**PLEASE NOTE** you will have to **re-download** this file if you want an **up-to-date** version of the player data.

### Running the Program
1. Make sure you have the latest release of **Python3 installed**, otherwise this program does not work.

2. Run the `main.py` file by double-clicking on it.

3. The GUI will open. From there, click on **"Parse CSV"** in order to initialize program.

4. From there, you're good to go. Add search and sort filters, then press **"Search"**.

## Functionality Documentation

### Filter Explanation: 
The filters are the program's main functionality. They allow further filtering than EscapeKit currently allows. The allows a prioritization of "records" in categories and genuine group lookups.

* Game Master
    * Enabling this checkbox shows a textbox to input the game master's name. This is an **includes**-type search. Ex: Searching "ort" will return names "Orthy", "Mort", and "Gortus".
* Room Name
    * Enabling this checkbox shows a dropdown to input a room's name. The names are gathered using the header line in the .csv file. 
* Group Size
    * Enabling this checkbox shows a textbox to input the size of a group. Only valid integers are accepted. 
* Sort by
    * Enabling this checkbox shows a dropdown and another checkbox. The dropdown shows what field you can sort the output by, the choices are below. If the **"Sort Least to Greatest?"** checkbox is clicked, the order will be reversed.
        * **Game Master** (alphabetically)
        * **Room Name** (alphabetically)
        * **Group Size** (greatest to least)
        * **Time Remaining** (greatest to least) 
* Only show escaped rooms
    * Enabling this checkbox will only show rooms who **"escaped"** the game. **NOTE** if this is enabled and the `Open Rates` is clicked, the resulting escape rate table will all read as **100% escaped** since all data in the output file is an escaped room. 


### Button Explanation:
This is a brief explanation of each button and their functionality. 

* Parse CSV 
    * Reads a `[Input Filename].csv` file located in the `Input Folder Path` and outputs it into the `Input Folder Path` as `[Input Filename].json`. This conversion allows groups to be the focal point. 
* Search
    * Given the selected filters (or none at all), searches the file `[Input Filename].json` for groups that meet the valid filters, and exports them into the `Output Folder Path`. The name of the file depends on the checkbox `Generate Unique Outfile Name` (off by default). If off, writes search to `output.json` in `Output Folder Path`. If on, the file's name is based on what filters are supplied. 
* Delete Output
    * Deletes all files ending with **.json** that are in `Output Folder Path`. 
* Open Settings
    * Opens a settings window where some constants can be modified.
* Open Rates
    * Based off of the previously generated output json file in `Output Folder Path`, a table is created with escape rates for each room and each game master. 
* Open File 
    * Based off of the previously generated output json file in `Output Folder Path`, a scrollable list of each group is given with a hyperlink to it's corresponding EscapeKit group. 

#### **Setting Buttons**
* Save Current Settings
    * Saves all inputs in the textboxes to their corresponding value in `config.json`. **NOTE**: For some visual settings (the colors of the buttons outside of the settings menu), you must close and reopen the program for the settings to take effect. 
* Restore Defaults
    * Deletes all settings and overwrites them to their default state using the data in `constants.py` located in `Resources Folder Path`. 

### Settings Menu Explanation
The settings menu allows for the user to make modifications to the program's constants. It's import to keep in mind that changing the filepath's hierarchy is unstable and is not intended to be supported.

* `Input Folder Path`  
    * Alter the path where `[Input Filename].csv` and `[Input Filename].json` are held. 
* `Input Filename`
    * Alters the what file to read for the input. EscapeKit downloads the player data file as `players.csv`, so by default the string is **"players"**. Upon pressing **Parse CSV**, a **.json** using the `Input Filename` is created. 
* `Output Folder Path`
    * Alter the path where output data is stored.  
    **NOTE:** Upon pressing button **"Delete Output"**, all files ending in **.json** are **DELETED** from the `Output Folder Path`.
*  `Resources Folder Path`
    * Alter the path where the main python fails are stored.  
    **NOTE:** It is **not** supported to modify the file **hierarchy** and should really only be used to **change the name** of this folder.
* `Generate Unique Outfile Name`
    * Upon pressing the Search button, the program will output a result into a file within the `Output Folder Path`.  
    If the checkbox is disabled, all outputs will be written as **output.json** and will be overwritten each time the Search button is pressed.  
    If the checkbox is enabled, all outputs will have a semi-unique filename that depends on what filter is selected. For example: if the "Game Master" filter has the value "Bob" in it, the output will be **game_masterBOB.json** as the filename. HOWEVER,   
* `Max Displayed Entries`  
    * When pressing the **"Open File"** button, it will generate a scrollable window with all entries matching the search. The amount of entries displayed won't go over the number specified in this field. This is to increase performance and is set at a default value of 100. This value can be increased or decreased to the user's preference.    
* `X Button Color`
    * Using Tkinter's supported colors, you can **modify** any of the button's rendered colors. In order for these settings to take effect, their corresponding window must be **reopened** (you might need to **close and reopen** the program). If a color is not supported, a **status message** will be shown upon opening the **button's window**, and the incorrect color will override to **white**. 

### Supporting Files Explanation
* Input/Output Folder  
  * The input and output folder are where the program reads and writes from, respectively. Input will house the .csv file and converted .json that holds the player data. The .csv is downloaded from EscapeKit. Output will hold all output files. Both of these hold a `.gitkeep` file that keeps the file hierarchy in GitHub, it can removed manually if considered clutter.  
* Resources Folder 
   * This folder holds all of the python files that operate the program. These files are meant to be used in tandem and not standalone. `app_main.py` operates the main functionality of the main program's UI. `constants.py` hold all the default values of the program that **Restore Defaults** reads from. `file_parser.py` handles the initial converstion from the .csv file to the .json. `immutable_constants.py` holds the constants that are not modified by the program. `rate_display.py` handles the UI for the escape rates. `result_display.py` shows the ranking of groups from the most recent output search. `utils.py` holds basic functions that some of the prior files use.
* `.gitignore`  
   * GitHub support file to holds what files to ignore when uploading to the repository. It can be removed manually if considered clutter.
* `config.json`
   * This file is created after running the program. This file holds all customizable settings in the **Advanced Settings** window that the user has modified.
* `cache.json`
   * This file holds a cache, currently limited to hold the last output file that was created. This is accessed by other resource files during runtime. 
* `main.py` 
   * Runs the program.
* `README.md`
   * The file you're reading now. Thanks for reading!


### Additional Functionality
Some additional functionality is available, mainly for clean restarts of the program. 
* Resetting Program
    * If you'd like to restore the program to it's original state, you can run this command in your console within the project's directory:  
        ```bash
        python main.py -d
        ``` 
        This will remove a couple files, specifically **"input/players.json"**, **output/\*.json**, **cache.txt**, and **config.json**. Afterwards, it will run the program.  
        **NOTE**: This use the default files and currently does not support any altered directories after the user modifies the Advanced Settings.  
        *(Because of this, you may need to change the folders back to their original names manually in order for this command to work)*
    * Alternatively, if you'd just like to do all the work in the previous bullet point but **NOT** run the program, use this command in your console within the project's directory:
        ```bash
        python main.py -donly
        ``` 
    

## FAQ
### What OS/software does this program require to run?
* **Software:** Python3 (at least 3.11.4)
* **OS:** Windows 10/11 

### My program no longer works after I modified the settings/moved a folder. What next?
You may be able to fix the problem by restoring to default settings. Make sure your input, output, and resource folder are located inside the main directory. Then run the command located in the [additional functionality section](#additional-functionality).  
If these tactics are not working, you will most likely need to [reinstall the program](#download-this-program). 

### Will macOS/Linux systems be supported?
Currently, only Windows 10 and 11 have been tested, both work flawlessly with  default settings. Support for macOS/linux have not been verified and may need testing to verify support.

### The data for "Events" aren't populating correctly. Why is that?
With my limited knowledge on the ins and outs of EscapeKit, upon downloading the CSV for player data, some data is omitted. Specifically, Event data will only supply the player's information (for the waiver system) and omit basically all details about the game. There is no game master, there is no time remaining, there isn't even the game they played. The only column supplied is the Event Name and the day it occured.   
With that being said, it's impossible to determine these pieces without HTML scraping or an API. Since I wanted this app to be offline (and definitely not because I don't know how to do HTML scraping nor pay money for an API), event data is filled in as best we can. Group size is actually calculated as the CSV data is being read, so inaccuracies can occur due to duplicated entries. Please consider the Group Size of an Event group to be an estimation.  
With that being said, clicking on the hyperlink button will give you all the hidden information that was omitted in the CSV!   


## Blog/Inspiration
### Why did I create this project? 
I made this project for a couple of reasons. One day, I was asked by a customer, "Are we the fastest group of two that had finished that room?" and I really wanted to give them an answer. I wanted to also say to them "Yeah! You're the fastest group I've ever had!" but I didn't even know if that was true. Since EscapeKit doesn't have an option to filter by individual Game Masters, I really wanted to create a program that did it for me. Another answer to this question is that I really wanted to create a bigger project that I could be proud of. From my understanding, EscapeKit doesn't offer this information and I wanted to be of use! Finally, another answer to this question is simple: I was bored!

### What is the end goal? 
I wanted a easy-to-use while also easily customizable system for employees, especially employees at my work, to sort and view customer records.  

### Did I meet those goals?
I believe I met this goal. I'm not sure about other businesses that have a different quantity of Game Masters, rooms, and other such information, but it's a solid start!

### How long did this take?
I started this project back towards the beginning of June of 2025. I am concluding my work towards the end of July 2025. So 2 months! I'm kind of working on it on and off, but I think I'm tapering down my activity.


Final Remarks
-- 

If you have any questions, feel free to drop an issue on Github! Otherwise, thank you for taking the time to investigate my personal passion project!

\- Zach :)


