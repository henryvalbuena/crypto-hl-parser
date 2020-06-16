#!/usr/bin/env python3

import argparse

from modules.runner import runner, threaded_runner
from modules.parser import run_parser

parser = argparse.ArgumentParser()

parser.add_argument("-i", help="File path containing the whitelisted pairs")
parser.add_argument("-o", help="File path where the parsed output will be stored")
parser.add_argument("-t", help="Use multiple threads i.e [-t 5]. Default to 3", nargs="?", const=3, type=int)
parser.add_argument("-pair", help="Single pair to be parsed. i.e. BTC/EUR")
parser.add_argument("-exchange", help="Specify the exchange for a single pair. i.e. kraken")
parser.add_argument("-d", help=":) ;) :D :B B) 0.0", nargs="?", const="smile")

args = parser.parse_args()

if args.i and args.o and args.t:
    try:
        threaded_runner(args.i, args.o, args.t)
    except Exception as err:
        print(f"Error: {err}")
elif args.i and args.o:
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
elif args.d:
    print(":) ;) :D :B B) 0.0")
else:
    print("Error: missing arguments, use -h or --help for more")
