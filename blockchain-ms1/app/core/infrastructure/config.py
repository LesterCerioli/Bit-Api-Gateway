import os
from dotenv import load_dotenv

# Correct function call
load_dotenv()

# Retrieve environment variables
BITCOIN_RPC_URL = os.getenv("BITCOIN_RPC_URL")
ETHEREUM_NODE_URL = os.getenv("ETHEREUM_NODE_URL")
POSTGRES_URL = os.getenv("POSTGRES_URL")
RABBITMQ_URL = os.getenv("RABBITMQ_URL")
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")

# Validate that required environment variables are set
required_env_vars = {
    "BITCOIN_RPC_URL": BITCOIN_RPC_URL,
    "ETHEREUM_NODE_URL": ETHEREUM_NODE_URL,
    "POSTGRES_URL": POSTGRES_URL,
    "RABBITMQ_URL": RABBITMQ_URL,
    "COINGECKO_API_KEY": COINGECKO_API_KEY,
    "BINANCE_API_KEY": BINANCE_API_KEY,
    "BINANCE_SECRET_KEY": BINANCE_SECRET_KEY
}

missing_vars = [key for key, value in required_env_vars.items() if not value]
if missing_vars:
    raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

print("All environment variables loaded successfully.")