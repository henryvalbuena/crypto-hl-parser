#!/usr/bin/env python3

import argparse
import time

from modules.runner import runner
from modules.parser import run_parser

parser = argparse.ArgumentParser()

parser.add_argument("-i", help="File path containing the whitelisted pairs")
parser.add_argument("-o", help="File path where the parsed output will be stored")
parser.add_argument("-pair", help="Single pair to be parsed. i.e. BTC/EUR")
parser.add_argument("-exchange", help="Specify the exchange for a single pair. i.e. kraken")
parser.add_argument("-a", help="Fun")

args = parser.parse_args()

if args.i and args.o:
    try:
        runner(args.i, args.o)
    except Exception as err:
        print(f"Error: {err}")
elif args.pair and args.exchange:
    try:
        coin = args.pair.split("/")[0]
        currency = args.pair.split("/")[1]
        run_parser(coin, currency, args.exchange, True)
    except Exception as err:
        print(f"Error: {err}")
else:
    print("Error: -i <input file path> and -o <output file path> must be provided")
    print("use -h or --help for more")
