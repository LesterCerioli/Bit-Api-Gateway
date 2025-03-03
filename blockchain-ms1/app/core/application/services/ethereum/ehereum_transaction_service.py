import os
import psycopg2
from dotenv import load_dotenv
from web3 import Web3
from elasticsearch import Elasticsearch
import logging

# Configure logging securely
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class EthereumTransactionService:
    def __init__(self):
        """Initializes secure connections to Ethereum, PostgreSQL, and Elasticsearch."""
        self.web3 = Web3(Web3.HTTPProvider(os.getenv("ETHEREUM_NODE_URL")))
        if not self.web3.isConnected():
            raise ConnectionError("Failed to connect to Ethereum node")

        self.gas_limit = int(os.getenv("ETH_GAS_LIMIT", 21000))

        # Secure configuration for PostgreSQL
        try:
            self.pg_conn = psycopg2.connect(os.getenv("POSTGRES_URL"))
            self.pg_conn.autocommit = True  
            self.pg_cursor = self.pg_conn.cursor()
            logger.info("Connected to PostgreSQL")
        except Exception as e:
            logger.error(f"Error connecting to PostgreSQL: {e}")
            raise
        
        try:
            self.es = Elasticsearch(
                os.getenv("ELASTICSEARCH_HOST"),
                basic_auth=(os.getenv("ELASTICSEARCH_USER"), os.getenv("ELASTICSEARCH_PASSWORD")),
                verify_certs=True,  
                request_timeout=30  
            )
            logger.info("Connected to Elasticsearch")
        except Exception as e:
            logger.error(f"Error connecting to Elasticsearch: {e}")
            raise

    def send_transaction(self, from_address, to_address, private_key, value_in_ether):
        """Sends an ETH transaction, saves it in PostgreSQL, and indexes it in Elasticsearch."""
        try:
            nonce = self.web3.eth.get_transaction_count(from_address)
            value = self.web3.to_wei(value_in_ether, 'ether')
            gas_price = self.web3.eth.gas_price

            transaction = {
                'to': to_address,
                'value': value,
                'gas': self.gas_limit,
                'gasPrice': gas_price,
                'nonce': nonce,
                'chainId': self.web3.eth.chain_id
            }

            signed_txn = self.web3.eth.account.sign_transaction(transaction, private_key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            tx_hash_hex = self.web3.to_hex(tx_hash)

            logger.info(f"Transaction sent! Hash: {tx_hash_hex}")
            
            self.save_transaction_postgres(tx_hash_hex, from_address, to_address, value_in_ether)
            self.index_transaction_elasticsearch(tx_hash_hex, from_address, to_address, value_in_ether)

            return tx_hash_hex

        except Exception as e:
            logger.error(f"Error sending transaction: {e}")
            raise

    def save_transaction_postgres(self, tx_hash, from_address, to_address, value_in_ether):
        """Saves the transaction securely in PostgreSQL."""
        query = """
        INSERT INTO ethereum_transactions (tx_hash, from_address, to_address, value, timestamp)
        VALUES (%s, %s, %s, %s, NOW())
        """
        try:
            self.pg_cursor.execute(query, (tx_hash, from_address, to_address, value_in_ether))
            logger.info(f"Transaction {tx_hash} saved in PostgreSQL.")
        except Exception as e:
            logger.error(f"Error saving transaction in PostgreSQL: {e}")

    def index_transaction_elasticsearch(self, tx_hash, from_address, to_address, value_in_ether):
        """Indexes the transaction in Elasticsearch."""
        doc = {
            "tx_hash": tx_hash,
            "from_address": from_address,
            "to_address": to_address,
            "value": value_in_ether,
            "timestamp": self.web3.eth.get_block("latest").timestamp
        }
        try:
            self.es.index(index="ethereum_transactions", document=doc)
            logger.info(f"Transaction {tx_hash} indexed in Elasticsearch.")
        except Exception as e:
            logger.error(f"Error indexing transaction in Elasticsearch: {e}")

    def get_transaction_by_hash(self, tx_hash):
        """Queries a transaction by hash in PostgreSQL."""
        query = "SELECT * FROM ethereum_transactions WHERE tx_hash = %s"
        try:
            self.pg_cursor.execute(query, (tx_hash,))
            return self.pg_cursor.fetchone()
        except Exception as e:
            logger.error(f"Error querying transaction in PostgreSQL: {e}")

    def search_transactions_in_elasticsearch(self, search_query):
        """Searches for transactions in Elasticsearch."""
        query = {
            "query": {
                "multi_match": {
                    "query": search_query,
                    "fields": ["tx_hash", "from_address", "to_address"]
                }
            }
        }
        try:
            response = self.es.search(index="ethereum_transactions", body=query)
            return response['hits']['hits']
        except Exception as e:
            logger.error(f"Error searching transactions in Elasticsearch: {e}")
