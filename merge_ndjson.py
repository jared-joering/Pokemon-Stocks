import os, json
from datetime import date, timedelta


def week_date():
    today = date.today() # getting what today is
    w = today.weekday() # returning the 'integer' of the week
    daysBack = (w - 2) % 7 # distance back to Wednesday, modulo is the hero here
    weekStart = today - timedelta(days = daysBack) # subtracting the days back from today
    weekEnd = weekStart + timedelta(days=6) # and performing the opposite here

    startIso = weekStart.isoformat() # changing formats
    endIso = weekEnd.isoformat()
    weekLabel = f"{startIso} - {endIso}" # creating labels
    finalLabel = f"{weekLabel} log.ndjson"
    return finalLabel


def NDJSON_merge():
    source = "data/logs"
    dest = "data/merged"
    filename = week_date()
    combined = f"{dest}/{filename}"

    os.makedirs(dest, exist_ok = True)

    with open(combined, "w") as out: # open the (future) combined log
        for log in os.listdir(source): # search through the given directory
            if log.endswith('.json'): # find files that end in .json, while ignoring newly created folders
                path = os.path.join(source, log)
                with open(path, "r", encoding="utf-8") as f: # reading files
                    data = json.load(f)

                    if isinstance(data, list):
                        for record in data:
                            out.write(json.dumps(record, ensure_ascii=False) + "\n")
                    else:
                        out.write(json.dumps(data) + "\n")

if __name__ == "__main__":
    NDJSON_merge()