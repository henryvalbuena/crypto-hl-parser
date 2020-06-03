import sys
import datetime as dt
from pprint import pprint

import requests

YEAR = 31536000
SIX_MONTH = 4320000
MONTH = 2630000
SEVEN_DAYS = 604800
today = dt.date.today()
seven_days_date = today - dt.timedelta(seconds=SEVEN_DAYS)
one_month_date = today - dt.timedelta(seconds=MONTH)
six_month_date = today - dt.timedelta(seconds=SIX_MONTH)
one_year_date = today - dt.timedelta(seconds=YEAR)
MIN_F = sys.float_info.min
MAX_F = sys.float_info.max
URI = "min-api.cryptocompare.com"


def midnight_timestamp(date):
    year = date.year
    month = date.month
    day = date.day

    d = dt.datetime(year, month, day, 20)
    return int(d.timestamp())


def get_data(coin, currency, exchange):
    URL = f"https://{URI}/data/v2/histoday?fsym={coin}&tsym={currency}&e={exchange}&allData=true"
    res = requests.get(URL)
    data = res.json()
    return data["Data"]["Data"]


def parsed_data(data):
    parsed_data = {
        "seven_day_high": MIN_F,
        "seven_day_low": MAX_F,
        "one_month_high": MIN_F,
        "one_month_low": MAX_F,
        "six_month_high": MIN_F,
        "six_month_low": MAX_F,
        "one_year_high": MIN_F,
        "one_year_low": MAX_F,
        "all_time_high": MIN_F,
        "all_time_low": MAX_F,
    }
    one_year_ago = midnight_timestamp(one_year_date)
    six_month_ago = midnight_timestamp(six_month_date)
    one_month_ago = midnight_timestamp(one_month_date)
    seven_days_ago = midnight_timestamp(seven_days_date)

    for d in data:
        # check the date for one year
        if d["time"] >= one_year_ago:
            parsed_data["one_year_high"] = max(d["high"], parsed_data["one_year_high"])
            parsed_data["one_year_low"] = min(d["low"], parsed_data["one_year_low"])
        # check the date for six months
        if d["time"] >= six_month_ago:
            parsed_data["six_month_high"] = max(d["high"], parsed_data["six_month_high"])
            parsed_data["six_month_low"] = min(d["low"], parsed_data["six_month_low"])
        # check the date for one month
        if d["time"] >= one_month_ago:
            parsed_data["one_month_high"] = max(d["high"], parsed_data["one_month_high"])
            parsed_data["one_month_low"] = min(d["low"], parsed_data["one_month_low"])
        # check the date for seven days
        if d["time"] >= seven_days_ago:
            parsed_data["seven_day_high"] = max(d["high"], parsed_data["seven_day_high"])
            parsed_data["seven_day_low"] = min(d["low"], parsed_data["seven_day_low"])
        # check all time
        parsed_data["all_time_high"] = max(parsed_data["all_time_high"], d["high"])
        parsed_data["all_time_low"] = min(parsed_data["all_time_low"], d["low"])

    return parsed_data


def run_parser(coin, currency, exchange, verbose=False):
    all_data = get_data(coin, currency, exchange)
    parsed = parsed_data(all_data)
    parsed["symbol"] = f"{coin}/{currency}"
    parsed["exchange"] = exchange

    if verbose:
        pprint(parsed)
        return parsed
    else:
        return parsed
