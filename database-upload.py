# TODO: Fix Tkinter
# TODO: Run duplicate checker

import psycopg2
import json
from tkinter import Tk, filedialog
from configparser import ConfigParser

def config(filename="database.ini", section="postgresql"):
    parser = ConfigParser() # creating parser
    parser.read(filename) # reading the .ini file
    db = {} # empty dictionary for database

    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
        
    else:
        raise Exception("Section {0} not found in the {1} file".format(section, filename))
    
    try:
        conn = psycopg2.connect(**db)
        print("Database connected successfully.")
    except:
        print("Database not connected successfully.")
        raise

    return conn


def psyco_path(): # the full insertion program, much of this is pretty self explanatory
    user_file = input("Enter the full (or relative) path to the NDJSON file to merge: ")

    if not user_file:
        print("No file selected, exiting.")
        return

    conn = config() # connecting to db
    cur = conn.cursor() # creating the cursor

    insert_query = """
INSERT INTO card (id, name, supertype, subtypes, set_name, series, card_number, printed_total, artist, rarity)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (id) DO NOTHING
""" # insertion into the tables

    with open(user_file, "r", encoding="utf-8") as f: # reading out the merge files
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)

            for card in row.get("data", []): # literating through all the 'card' objects
                card_id = card["id"]
                name = card["name"]
                supertype = card["supertype"]
                subtypes = card.get("subtypes") or []
                set_object = card.get("set", {})
                set_series = set_object.get("series", None)
                card_number = card.get("number", None)
                set_pt = set_object.get("printedTotal", None)
                artist = card.get("artist", None)
                rarity = card.get("rarity", None)

                cur.execute(insert_query, ( # writing said 'card' objects
                    card_id,
                    name,
                    supertype,
                    subtypes,
                    set_object.get("name", None),
                    set_series,
                    card_number,
                    set_pt,
                    artist,
                    rarity
                ))
    
    conn.commit() # wrapping up
    cur.close()
    conn.close()
    print("Finished inserting records into database, closing connection.")

if __name__ == "__main__": # calling
    psyco_path()