# TODO: Fix Tkinter
# TODO: Run duplicate checker

import psycopg2
import json
from configparser import ConfigParser

'''
Running a function to take all key-value pairs in a config file 
and save them for later.
'''

def config(filename="database.ini", section="postgresql"):
    parser = ConfigParser() # creating parser
    parser.read(filename) # reading the .ini file
    db = {} # empty dictionary for database

    if parser.has_section(section): # checking if a config section exists
        params = parser.items(section) # "
        for param in params: # reading every setting
            db[param[0]] = param[1] # applying these for later use
        
    else:
        raise Exception("Section {0} not found in the {1} file".format(section, filename))
    
    try:
        conn = psycopg2.connect(**db) # connecting to the db by bypassing the dictionary
        print("Database connected successfully.")
    except:
        print("Database not connected successfully.")
        raise

    return conn

'''
The full insertion bit: we prompt the user for a file to insert
into the database.  If they don't select it, we kill the operation.
From there, we utilize the conn(ect) we created earlier and create 
a cursor that allows us to insert all of the files that we literate
through before cutting and closing down.
'''

def psyco_path():
    user_file = input("Enter the full (or relative) path to the NDJSON file to merge: ")

    if not user_file:
        print("No file selected, exiting.")
        return

    conn = config() # connecting to db
    cur = conn.cursor() # creating the cursor

    insert_query = """INSERT INTO card (id, name, supertype, subtypes, set_name, series, card_number, printed_total, artist, rarity)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING
    """ # insertion into the tables

    with open(user_file, "r", encoding="utf-8") as f: # reading out the merge files
        for line in f:
            line = line.strip() # stripping white space
            if not line:
                continue
            row = json.loads(line)

            for card in row.get("data", []): # literating through all the 'card' objects
                card_id = card["id"]
                name = card["name"]
                supertype = card["supertype"]
                subtypes = card.get("subtypes") or [] # subtypes can be multiple or there can be none -- this also allows for us to more easily search with SQL
                set_object = card.get("set", {})
                set_series = set_object.get("series", None) # as with subtypes and the others below - just in case - there could be empty results from this, so we account for it
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