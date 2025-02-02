import os
from dotenv import load_dotenv

load-dotenv()

BITCOIN_RPC_URL = os.getenv("BITCOIN_RPC_URL")
ETHEREUM_NODE_URL = os.getenv("ETHEREUM_NODE_URL")

POSTGRES_URL = os.getenv("POSTGRES_URL")

RABBITMQ_URL = os.getenv("RABBITMQ_URL")

COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")