import os
import json
import datetime as dt
import configparser
import psycopg2

'''
Do a similar deal as we did with the database-upload
'''

def config(filename="database.ini", section="postgresql"):
    parser = configparser.ConfigParser() # creating parser
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
Again, much like the database-upload.py, we will be prompting the 
user for a file to insert into the database.  If they don't select
it, we kill the operation.  From there, we utilize the conn(ect) we
created earlier and create a cursor that allows us to insert all of
the files that we literate through before cutting and closing down.
'''

def psyco_price_path():
    user_file = input("Enter the full (or relative) path to the NDJSON file to merge: ")
    skipped = 0

    if not user_file:
        print("No file selected, exiting.")
        return

    conn = config() # connecting to db
    cur = conn.cursor() # creating the cursor

    insert_query = """INSERT INTO prices (card_id, source, variant, condition_txt, updated_at, market_price, low_price, mid_price, high_price, raw_json)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (card_id, source, variant, updated_at) DO NOTHING
    """

    with open (user_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)

            for card in row.get("data", []): # literating through all the 'card' objects
                card_id = card["id"] # foreign key
                source = "tcgplayer"
                condition_txt = "Near Mint" # all cards in the database are 'near mint' priced, this also gives me a ceiling
                tcgp = card.get("tcgplayer") # getting the tcgplayer portion of the API for the subheaders
                if tcgp == None:
                    print(f"Warning: 'tcgplayer' subheading for {card_id}")
                    skipped += 1
                    continue
                updated_at_raw = tcgp.get("updatedAt")
                updated_at = dt.datetime.strptime(updated_at_raw, "%Y/%m/%d").date()
                prices_blob = tcgp.get("prices", {}) # this is the collection of variant name, prices all held together by a dictionary
                for variant_name, variant_obj in prices_blob.items():
                    variant = variant_name
                    market_price = variant_obj.get("market")
                    low_price = variant_obj.get("low")
                    mid_price = variant_obj.get("mid")
                    high_price = variant_obj.get("high")
                    raw_json = json.dumps(variant_obj)

                    cur.execute(insert_query, ( # writing 'prices' objects in the 'for' loop for each variant
                        card_id,
                        source,
                        variant,
                        condition_txt,
                        updated_at,
                        market_price,
                        low_price,
                        mid_price,
                        high_price,
                        raw_json
                    ))
    
    conn.commit() # wrapping up
    cur.close()
    conn.close()
    print("Finished inserting records into database, closing connection.")

if __name__ == "__main__": # calling
    psyco_price_path()
