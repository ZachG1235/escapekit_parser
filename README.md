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

## FAQ

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
* Parse CSV 
    * Reads a `[Input Filename].csv` file located in the `Input Folder Path` and outputs it into the `Input Folder Path` as `[Input Filename].json` 
* Search
    * Given the selected filters (or none at all), searches the file `[Input Filename].json` for groups that meet the valid filters, and exports them into the `Output Folder Path`. The name of the file depends on the checkbox `Generate Unique Outfile Name` (off by default). If off, writes search to `output.json` in `Output Folder Path`. If on, the file's name is based on what filters are supplied. 
* Delete Output
    * Deletes all files ending with **.json** that are in `Output Folder Path`. 
* Open Settings
    * Opens a settings window where some constants can be modified.
* Open Rates
    * Based off of the previously generated output json file in `Output Folder Path`, a table is created with escape rates for each room and each game master. 
* Open File 
    * Based off of the previously generated output json file in `Output Folder Path`, a list of each group is given with a hyperlink to it's corresponding EscapeKit group. 

Buttons pertaining to the settings menu
* Save Current Settings
    * Saves all inputs in the textboxes to their corresponding value in `config.json`. **NOTE**: For some visual settings (the colors of the buttons outside of the settings menu), you must close and reopen the program for the settings to take effect. 
* Restore Defaults
    * Deletes all settings and overwrites them to their default state using the data in `constants.py` located in `Resources Folder Path`. 

### Settings Menu Explanation
The settings menu allows for the user to make modifications to the program. It's very import to keep in mind that changing the filepath's heirarchy is unstable and not intended to be supported.
* 


## Insert Other things here

**NOTE**, add exception for no filters on Generate Unique file name  
**NOTE**, verify if group size filter is a positive integer
