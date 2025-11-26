# TODO: Create a loop back around to start reloading missed files again
# TODO: Don't create empty files when the script fails on ValueError

import requests
import json
import os
import math
import time
from urllib3.util.retry import Retry
from datetime import date

from config import api # calling the config file I created to hide my API

headers = { # setting the headers for the API request
    "X-API-Key": api
}

present = date.today().strftime("%Y-%m-%d")
folder_path = f"data/logs/{present} log"

'''
Define the directory, the destination, and create if it's not there,
otherwise: "Directory already present."
'''

def mkdirectory():
    os.makedirs(folder_path, exist_ok = True)

'''
We're pinging the API after opening a 'session' which allows us to 
maintain a state of contact with the API.

From there, we draw on each page of 250 up to a total of 79 -
allPages - [for the moment (10/21)] and create logs of each of
them.  After that, we move on to the next until the end.  Admidst
all of that, we're checking for errors.
'''

def mkentries():
    sesh = requests.Session() # creating a session to persist certain things across requests
    retries = Retry( # creating the retry vehicle
        total = 5, # Total retries 
        backoff_factor = 1, # We back off exponentially, five times (1, 2, 4, 8, 16 seconds)
        status_forcelist = [ 429, 500, 502, 503, 504 ], 
        allowed_methods = {"GET"},
        respect_retry_after_header = True)
    
    sesh.mount('https://', requests.adapters.HTTPAdapter(max_retries=retries))
    sesh.mount('http://', requests.adapters.HTTPAdapter(max_retries=retries))   

    response = sesh.get("https://api.pokemontcg.io/v2/cards", headers = headers)

    starting_page = 1  # setting the starting page number (can change if you need to)
 
    if response.status_code == 200: # only proceed if the HTTP request succeeds
        data = response.json()
        pageSize = data["pageSize"] # taking the page size...
        totalCount = data["totalCount"] # ... and the total amount of 'cards'...

        allPages = math.ceil(totalCount/pageSize) # ... and then calculating total pages for the loop
    
        for pages in range(starting_page, allPages + 1):
            step_response = sesh.get(f"https://api.pokemontcg.io/v2/cards?page={pages}&pageSize=250", headers = headers, timeout = (10.0, 90.0)) # a new response URL to include both page number and size
            try:
                log_path = os.path.join(folder_path, f"pmb_log_{present}-{pages}.json") # log file with pg number added
                with open(log_path, "x") as f:
                    json.dump(step_response.json(), f, indent = 2) # creating the log
                print(f"Created log: {log_path}")
            
                time.sleep(10.0) # giving the grace of a 10 second wait so the server doesn't bog down on our accord
            
            except FileExistsError: # running a few important error checkers and a general error
                print("Log already exists")
            except ValueError:
                print("Response did not contain valid JSON")
            except Exception as error:
                print("Unexpected error while writing log: ", error)

if __name__ == "__main__":
    mkdirectory()  # ensure the logs folder exists
    mkentries()    # run the API crawling/logging
    # JSON_merge(totalFiles, final_log)