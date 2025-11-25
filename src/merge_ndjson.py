# TODO: Put a success/fail prompt

import os, json
from datetime import date, timedelta

'''
Find and validate a user-chosen source folder to merge the files, and
deposit them in the 'merged' folder.
'''

def find_folder():
    user_input = input("Please enter the path where your desired files are located (default path is 'data/logs'): ") # asking for user input
    source = user_input or "data/logs" # ... or defaulting to our default directory
    
    if not os.path.exists(source): # error for no path existing
        print("Path does not exist.")
        return None
    
    if not os.path.isdir(source):
        print("That is a file, not a folder.") # accidentally, or otherwise, choosing a file instead of a directory
        return None

    json_files = [f for f in os.listdir(source) if f.endswith(".json")] # using a similar for-loop used in an earlier file to...

    if not json_files: # find if the folder even contains .json files
        print("There are no mergeable files in this folder.")
        return None

    return source
    
''' 
Retrieve the 'work week' when TCGPlayer used to roll over their price 
tracking.  It was usually on a Wednesday, which means it stopped on
Tuesday.  This is for the label alone and for a weekly pull.
'''

def week_date():
    today = date.today() # getting what today is
    w = today.weekday() # returning the 'integer' of the week (0-6)
    days_back = (w - 2) % 7 # distance back to Wednesday
    week_start = today - timedelta(days = days_back) # 
    week_end = week_start + timedelta(days=6) # and performing the opposite here

    start_iso = week_start.isoformat() # changing formats
    end_iso = week_end.isoformat()
    week_label = f"{start_iso} - {end_iso}" # creating labels
    final_label = f"{week_label} log.ndjson"
    return final_label

'''
To merge all of the files we've accrued from our API crawler.  This 
also has a corrupted files check, as well as writing to a temp file
before committing to the final draft.
'''

def NDJSON_merge():
    source = find_folder()
    if source is None:
        print("Cancelling merge.")
        return

    dest = "data/merged"
    filename = week_date()
    combined = f"{dest}/{filename}" # the final, merged file
    combined_temp = combined + ".tmp" # our temp file
    corrupted_dir = os.path.join(source, "corrupted") # creating a directory for corrupted files

    os.makedirs(dest, exist_ok = True) # making directories
    os.makedirs(corrupted_dir, exist_ok=True)

    with open(combined_temp, "w", encoding="utf-8") as out: # open the (future) combined log
        for log in os.listdir(source): # search through the given directory
            if log.endswith('.json'): # find files that end in .json, while ignoring newly created folders
                path = os.path.join(source, log) # joining our source folder and logs for a relative path
                try:
                    with open(path, "r", encoding="utf-8") as f: # reading the files
                        data = json.load(f) 
                except json.JSONDecodeError as e: # running a try-except to catch our corrupted files
                    corrupted_path = os.path.join(corrupted_dir, log)
                    os.replace(path, corrupted_path)
                    print(f"Skipped corrupted JSON {log}: {e} -> moved to {corrupted_path}") # returning the warning that we have a corrupted file...
                    continue # ... then moving on

                if isinstance(data, list):
                    for record in data:
                        out.write(json.dumps(record, ensure_ascii=False) + "\n") # writing the log into the merger and then jumping to a new line
                else:
                    out.write(json.dumps(data) + "\n")

    os.replace(combined_temp, combined)

if __name__ == "__main__":
    NDJSON_merge()