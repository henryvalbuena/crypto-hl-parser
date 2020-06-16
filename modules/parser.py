import sys
import datetime as dt
from pprint import pprint
import requests

from modules.constants import SEVEN_DAYS, MONTH, SIX_MONTH, YEAR, DAY, URI

today = dt.date.today()
seven_days_date = today - dt.timedelta(seconds=SEVEN_DAYS)
one_month_date = today - dt.timedelta(seconds=MONTH)
six_month_date = today - dt.timedelta(seconds=SIX_MONTH)
one_year_date = today - dt.timedelta(seconds=YEAR)
one_day_date = today - dt.timedelta(seconds=DAY)
MIN_F = sys.float_info.min
MAX_F = sys.float_info.max


def midnight_timestamp(date):
    """
    Get midnight timestime from date datetime object
    :param date: datetime date object
    :return int: midnight hour timestamp from the argument date
    """
    year = date.year
    month = date.month
    day = date.day

    d = dt.datetime(year, month, day, 20)
    return int(d.timestamp())


def get_data(coin, currency, exchange):
    """
    Fetch all time data from cryptocompare API
    :param coin: crypto coin (BTC, XRP...)
    :param currency: fiat (CAD, USD, EUR...)
    :param exchange: name of the exchange
    :return list[dict]: returns the all time data from the coin/currency provided
    """
    URL = f"https://{URI}/data/v2/histoday?fsym={coin}&tsym={currency}&e={exchange}&allData=true"
    res = requests.get(URL)
    data = res.json()

    return data["Data"]["Data"]


def parsed_data(data):
    """
    Parses the all time data from get_data to get the high low metrics
    :param data: list containing the all time data from the exchange
    :return dict: parsed data containing metrics and float values
    """
    parsed_data = {
        "one_day_high": MIN_F,
        "one_day_low": MAX_F,
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
    on_the_day = midnight_timestamp(one_day_date)

    for d in data:
        # check the date for one year
        if d["time"] >= one_year_ago:
            parsed_data["one_year_high"] = max(d["high"], parsed_data["one_year_high"])
            parsed_data["one_year_low"] = min(d["low"], parsed_data["one_year_low"])
        # check the date for six months
        if d["time"] >= six_month_ago:
            parsed_data["six_month_high"] = max(
                d["high"], parsed_data["six_month_high"]
            )
            parsed_data["six_month_low"] = min(d["low"], parsed_data["six_month_low"])
        # check the date for one month
        if d["time"] >= one_month_ago:
            parsed_data["one_month_high"] = max(
                d["high"], parsed_data["one_month_high"]
            )
            parsed_data["one_month_low"] = min(d["low"], parsed_data["one_month_low"])
        # check the date for seven days
        if d["time"] >= seven_days_ago:
            parsed_data["seven_day_high"] = max(
                d["high"], parsed_data["seven_day_high"]
            )
            parsed_data["seven_day_low"] = min(d["low"], parsed_data["seven_day_low"])
        # check the date for the day
        if d["time"] == on_the_day:
            parsed_data["one_day_high"] = max(d["high"], parsed_data["one_day_high"])
            parsed_data["one_day_low"] = min(d["low"], parsed_data["one_day_low"])
        # check all time
        parsed_data["all_time_high"] = max(parsed_data["all_time_high"], d["high"])
        parsed_data["all_time_low"] = min(parsed_data["all_time_low"], d["low"])

    return parsed_data


def run_parser(coin, currency, exchange, verbose=False):
    """
    Manages the data parsing of the crypto currency
    :param coin: crypto coin (BTC, XRP...)
    :param currency: fiat (CAD, USD, EUR...)
    :param exchange: name of the exchange
    :param verbose: if set to True it will print the data parsed and return the data
    otherwise, it will just return the data
    :return dict: parsed data containing metrics and float values
    """
    all_data = get_data(coin, currency, exchange)
    parsed = parsed_data(all_data)
    parsed["symbol"] = f"{coin}/{currency}"
    parsed["exchange"] = exchange

    if verbose:
        pprint(parsed)
        return parsed
    else:
        return parsed
