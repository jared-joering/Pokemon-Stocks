import psycopg2
import json
import config

conn = psycopg2.connect(
    config
)

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

