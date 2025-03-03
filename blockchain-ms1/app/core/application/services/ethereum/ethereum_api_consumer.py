import logging
import os
import requests
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class EthereumAPIConsumer:
    def __init__(self):
        """Initializes the client to securely consume Ethereum APIs."""
        self.etherscan_api_url = os.getenv("ETHERSCAN_API_URL", "https://api.etherscan.io/api")
        self.etherscan_api_key = os.getenv("ETHERSCAN_API_KEY")

        self.blockcypher_api_url = os.getenv("BLOCKCYPHER_API_URL")
        self.blockcypher_api_token = os.getenv("BLOCKCYPHER_API_TOKEN")

        self.infura_url = os.getenv("INFURA_URL")  

        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def get_transaction_status(self, tx_hash):
        """Queries the status of a transaction on the Ethereum network using the Etherscan API."""
        try:
            params = {
                "module": "transaction",
                "action": "gettxreceiptstatus",
                "txhash": tx_hash,
                "apikey": self.etherscan_api_key
            }
            response = self.session.get(self.etherscan_api_url, params=params, timeout=10)
            response.raise_for_status()  # Raises an exception for HTTP 4xx or 5xx status codes
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error querying transaction {tx_hash}: {e}")
            return None

    def get_account_balance(self, address):
        """Queries the balance of an Ethereum account via Etherscan."""
        try:
            params = {
                "module": "account",
                "action": "balance",
                "address": address,
                "tag": "latest",
                "apikey": self.etherscan_api_key
            }
            response = self.session.get(self.etherscan_api_url, params=params, timeout=10)
            response.raise_for_status()
            return response.json().get("result")
        except requests.RequestException as e:
            logger.error(f"Error querying balance for {address}: {e}")
            return None
