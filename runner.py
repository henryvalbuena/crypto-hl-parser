import time
import json

from app import run

pairs = [
    "ADA/EUR",
    "ATOM/EUR",
    "BAT/EUR",
    "BCH/EUR",
    "BTC/EUR",
    "DAI/EUR",
    "DASH/EUR",
    "EOS/EUR",
    "ETC/EUR",
    "ETH/EUR",
    "LINK/EUR",
    "LTC/EUR",
    "QTUM/EUR",
    "REP/EUR",
    "WAVES/EUR",
    "XLM/EUR",
    "XMR/EUR",
    "XRP/EUR",
    "XTZ/EUR",
    "ZEC/EUR",
]


def polling():
    exchange = "kraken"
    hl_pairs = list()

    for pair in pairs:
        coin = pair.split("/")[0]
        currency = pair.split("/")[1]
        hl_pairs.append(run(coin, currency, exchange))

    return hl_pairs


start = time.perf_counter()
hl_parsed_data = polling()
try:
    with open("kraken_hl_info.json", "w") as f:
        json.dump(hl_parsed_data, f)
    print("Success. Data processed and file created.")
except Exception:
    print("Error writing into file.")
end = time.perf_counter()
print(f"Synchronous IO: {end - start:.2f}")
