import os, json
from datetime import date, timedelta


def week_date():
    today = date.today() # getting what today is
    w = today.weekday() # returning the 'integer' of the week
    days_back = (w - 2) % 7 # distance back to Wednesday, modulo is the hero here
    week_start = today - timedelta(days = days_back) # subtracting the days back from today
    week_end = week_start + timedelta(days=6) # and performing the opposite here

    start_iso = week_start.isoformat() # changing formats
    end_iso = week_end.isoformat()
    week_label = f"{start_iso} - {end_iso}" # creating labels
    final_label = f"{week_label} log.ndjson"
    return final_label


def NDJSON_merge():
    source = "data/logs"
    dest = "data/merged"
    filename = week_date()
    combined = f"{dest}/{filename}"
    combined_temp = combined + ".tmp"
    corrupted_dir = os.path.join(source, "corrupted")

    os.makedirs(dest, exist_ok = True)
    os.makedirs(corrupted_dir, exist_ok=True)

    with open(combined_temp, "w", encoding="utf-8") as out: # open the (future) combined log
        for log in os.listdir(source): # search through the given directory
            if log.endswith('.json'): # find files that end in .json, while ignoring newly created folders
                path = os.path.join(source, log)
                try:
                    with open(path, "r", encoding="utf-8") as f: # reading files
                        data = json.load(f)
                except json.JSONDecodeError as e:
                    corrupted_path = os.path.join(corrupted_dir, log)
                    os.replace(path, corrupted_path)
                    print(f"Skipped corrupted JSON {log}: {e} -> moved to {corrupted_path}")
                    continue

                if isinstance(data, list):
                    for record in data:
                        out.write(json.dumps(record, ensure_ascii=False) + "\n")
                else:
                    out.write(json.dumps(data) + "\n")

    os.replace(combined_temp, combined)

if __name__ == "__main__":
    NDJSON_merge()