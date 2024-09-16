from pybit.unified_trading import HTTP

key = ''
secret = ''

session = HTTP(
    testnet=False,
    api_key=key,
    api_secret=secret
)
