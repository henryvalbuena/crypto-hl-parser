import time
import concurrent.futures
from datetime import datetime
import json

from modules.parser import run_parser


def load_file_data(file):
    """
    Load exchange and pairs from file
    :param file: file path where source data is located
    :return dict: dictionatry containing the exchange info and pairs
    """
    with open(file) as f:
        data = json.load(f)
    return data["exchange"]


def polling(data):
    """
    Single thread polling method to get the data from cryptocompare
    :param data: dictionary containing the details to be fetched
    :return list: containing the high low metrics for each pair
    """
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
    print(
        f"Processed {count} symbols for {exchange} | Total count: <{count} of {total}>"
    )

    return hl_pairs


def threaded_polling(data, max_workers):
    """
    Multithreaded polling method to get the data from cryptocompare
    :param data: dictionary containing the details to be fetched
    :param max_workers: maximum number of threads to spawn
    :return list: containing the high low metrics for each pair
    """
    hl_parsed_data = list()
    exchange = data["name"]
    pairs = data["pair_whitelist"]
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Start the load operations and mark each future with its URL
        future_to_pairs = [
            executor.submit(run_parser, _.split("/")[0], _.split("/")[1], exchange)
            for _ in pairs
        ]
        total = len(future_to_pairs)
        count = 0
        for future in concurrent.futures.as_completed(future_to_pairs):
            try:
                data = future.result()
                hl_parsed_data.append(data)
            except Exception as exc:
                print(exc)
            else:
                count += 1
                msg = f"Parsing {data['symbol']:10} | {count:2}/{total:2}"
                print(msg, end="\r")
        print(f"Pairs processed from {exchange} | {count:2}/{total:2}")
        return hl_parsed_data


def runner(input_file, output_file):
    """
    Main single threaded handler to process pairs, fetch cryptocompare and get high low metrics
    :param input_file: config file where the exchange and pairs are located
    :param output_file: where the parsed data will be stored
    """
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
    except Exception as err:
        print(f"Error {err}")
    else:
        end = time.perf_counter()
        print(f"Task executed in: {end - start:.2f} seconds")


def threaded_runner(input_file, output_file, max_workers):
    """
    Main multi threaded handler to process pairs, fetch cryptocompare and get high low metrics
    :param input_file: config file where the exchange and pairs are located
    :param output_file: where the parsed data will be stored
    :param max_workers: maximun amount of threads to be spawned
    """
    data = load_file_data(input_file)
    start = time.perf_counter()
    hl_parsed_data = threaded_polling(data, max_workers)
    try:
        timestamp = int(datetime.now().timestamp())
        if ".json" in output_file:
            filename = f"{output_file.split('.json')[0]}_{timestamp}.json"
        else:
            filename = f"{output_file}_{timestamp}.json"
        with open(filename, "w") as f:
            json.dump(hl_parsed_data, f)
    except Exception as err:
        print(f"Error {err}")
    else:
        end = time.perf_counter()
        print(
            f"Task executed in: {end - start:.2f} "
            f"seconds using {max_workers} threads."
        )
