# Crypto High Low Historic Parser

Python tool to parse historic high low data from `min-api.cryptocompare.com`.

### Requirements
- Python 3.6+

### Getting started
- Create virtual environment `pip -m venv .env`
- Activate virtual environment `source .env/bin/activate`
- Install dependencies `pip install -r requirements.txt`

### Commands
Build from config.json

```bash
./parsecrypto.py -i config.json -o output/kraken_crypto_info
```

Parse single pair

```bash
./parsecrypto.py -pair "BTC/EUR" -exchange "kraken"
```

## Author
Henry Valbuena