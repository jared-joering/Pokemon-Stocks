import psycopg2
import json
from configparser import configparser

def config(filename="database.ini", section="postgresql"):
    parser = configparser # creating parser
    parser.read(filename) # reading the .ini file

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
        
    else:
        raise Exception("Section {0} not found in the {1} file".format(section, filename))
    
    return db

def psyco_path()
    user_file=input("Please choose the file you wish to enter into the database: ")

    with open(user_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)

            for card in row.get("data", []):
                card_id = card["id"]
                name = card["name"]
                supertype = card["supertype"]
                subtypes = card.get("subtypes", None)
                set_object = card.get("set", {})
                set_series = set_object.get("series", None)
                card_number = card.get("number", None)
                set_pt = set_object.get("printedTotal", None)
                artist = card.get("artist", None)
                rarity = card.get("rarity", None)

