import requests
import json
import os
import math
from datetime import date

from config import api # calling the config file I created to hide my API

from pokemontcgsdk import Card

headers = {
    "X-API-Key": api
}

response = requests.get("https://api.pokemontcg.io/v2/cards", headers=headers)
present = date.today().strftime("%Y-%m-%d")
folder_path = "data\logs"

# define the directory, the destination, and create if it's not there, otherwise: "Directory already present."
# def mkdirectory():
os.makedirs(folder_path, exist_ok=True)

# def mkentries():
starting_page = 1 # setting the page number
pageSize = response.json()["pageSize"]
totalCount = response.json()["totalCount"]
allPages = math.ceil(totalCount/pageSize)
if response.status_code == 200: # only proceed if the HTTP request succeeds
    for pages in range(starting_page, starting_page + 3):
        step_response = requests.get(f"https://api.pokemontcg.io/v2/cards?page={pages}&pageSize=250") # a new response URL to include both page number and size
        try:
            log_path = os.path.join(folder_path, f"pmb_log_{present}-{pages}.json") # log with pg number added
            with open(log_path, "x") as f:
                json.dump(step_response.json(), f, indent = 2)
            print(f"Created log: {log_path}")
        except FileExistsError:
            print("Log already exists")
        except ValueError:
            print("Response did not contain valid JSON")
        except Exception as error:
            print("Unexpected error while writing log: ", error)

# def JSON_merger(totalFiles, final_log):
totalFiles = os.listdir(folder_path)
merged_data = []
for flog_path in totalFiles:
    with open(flog_path, "r") as flog:
        data = json.load(flog)
        merged_data.append(data)
    with open(f"final_log_{present}.json", "x") as final_log:
        json.dump(merged_data, final_log)
    