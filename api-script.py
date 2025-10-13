import requests
import json
import psycopg2
import os
from datetime import date

from config import api # calling the config file I created to hide my API

from pokemontcgsdk import Card

headers = {
    "X-API-Key": api
}

response = requests.get("https://api.pokemontcg.io/v2/cards", headers=headers)
present = date.today().strftime("%Y-%m-%d")
folder_path = "data/logs/"

# define the directory, the destination, and create if it's not there, otherwise: "Directory already present."
# def mkdirectory():
os.makedirs(folder_path, exist_ok=True)

# def mkentry():
log_path = os.path.join(folder_path, f"pmb_log_{present}.json")
if response.status_code == 200: # only proceed if the HTTP request succeeds
    try:
        with open(log_path, "x") as f:
            json.dump(response.json(), f, indent = 2)
        print(f"Created log: {log_path}")
    except FileExistsError:
        print("Log already exists")
    except ValueError:
        print("Response did not contain valid JSON")
    except Exception as error:
        print("Unexpected error while writing log: ", error)