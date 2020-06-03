import time
from datetime import datetime
import json

from modules.parser import run_parser


def load_file_data(file):
    with open(file) as f:
        data = json.load(f)
    return data["exchange"]


def polling(data):
    exchange = data["name"]
    pairs = data["pair_whitelist"]

    hl_pairs = list()
    total = len(pairs)
    count = 0

    for pair in pairs:
        msg = f"Parsing {pair:10} symbol | {count:2}/{total:2}"
        print(msg, end="\r")
        count += 1
        coin = pair.split("/")[0]
        currency = pair.split("/")[1]
        hl_pairs.append(run_parser(coin, currency, exchange))
    print(f"Processed {count} symbols for {exchange} | Total count: <{count} of {total}>")

    return hl_pairs


def runner(input_file, output_file):
    data = load_file_data(input_file)
    start = time.perf_counter()
    hl_parsed_data = polling(data)
    try:
        timestamp = int(datetime.now().timestamp())
        if ".json" in output_file:
            filename = f"{output_file.split('.json')[0]}_{timestamp}.json"
        else:
            filename = f"{output_file}_{timestamp}.json"
        with open(filename, "w") as f:
            json.dump(hl_parsed_data, f)
        print("Success. Data processed and file created.")
    except Exception:
        print("Error writing into file.")
    end = time.perf_counter()
    print(f"Sychronous task executed in: {end - start:.2f} seconds")
