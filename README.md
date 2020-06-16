# Crypto High Low Historic Parser

Python tool to parse historic high low data from `min-api.cryptocompare.com`.

### Requirements
- Python 3.6+

### Getting started
- Create virtual environment `python3.6 -m venv .env`
- Activate virtual environment `source .env/bin/activate`
- Install dependencies `pip install -r requirements.txt`

### Commands
Build from config.json example

```bash
./parsecrypto.py -i config.json -o output/kraken_crypto_info
```

Parse single pair

```bash
./parsecrypto.py -pair "BTC/EUR" -exchange "kraken"
```

### Examples

```bash
$ ./parsecrypto.py -i config.json -o derp -t 6
Pairs processed from kraken | 20/20
Task executed in: 2.90 seconds using 6 threads.
```

```bash
$ ./parsecrypto.py -i config.json -o derp -t  
Pairs processed from kraken | 20/20
Task executed in: 5.33 seconds using 3 threads.
```

```bash
$ ./parsecrypto.py -i config.json -o derp   
Processed 20 symbols for kraken | Total count: <20 of 20>
Success. Data processed and file created.
Task executed in: 15.80 seconds
```

```bash
$ ./parsecrypto.py -pair btc/eur -exchange kraken 
{'all_time_high': 16323,
 'all_time_low': 81,
 'exchange': 'kraken',
 'one_day_high': 8495.5,
 'one_day_low': 8279.9,
 'one_month_high': 9220,
 'one_month_low': 7925,
 'one_year_high': 12060,
 'one_year_low': 3550,
 'seven_day_high': 8764.4,
 'seven_day_low': 7925,
 'six_month_high': 9278,
 'six_month_low': 7100,
 'symbol': 'btc/eur'}
```

## Author
Henry Valbuena