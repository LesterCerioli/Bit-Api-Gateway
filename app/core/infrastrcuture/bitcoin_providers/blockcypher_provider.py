import requests
import os
from datetime import datetime
import uuid
from app.core.domain.interfaces.payment_gateway import PaymentGateway
from app.core.domain.entities.transaction import Transaction
from app.core.infrastructure.database.transaction_repository_impl import TransactionRepositoryImpl

# Load API credentials from environment variables
BLOCKCYPHER_API_URL = os.getenv("BLOCKCYPHER_API_URL", "https://api.blockcypher.com/v1/btc/main")
BLOCKCYPHER_API_TOKEN = os.getenv("BLOCKCYPHER_API_TOKEN")  # Token for authentication

class BlockCypherProvider(PaymentGateway):
    """
    BlockCypher provider for Bitcoin transactions.
    Uses PostgreSQL as primary storage and Elasticsearch as a cache.
    """

    def __init__(self):
        self.repository = TransactionRepositoryImpl()

    def create_transaction(self, user_id: str, amount: float, currency: str):
        """
        Creates a new Bitcoin transaction via BlockCypher API.
        Saves it in PostgreSQL and indexes it in Elasticsearch.
        """
        
        transaction = Transaction(
            id=str(uuid.uuid4()),
            user_id=user_id,
            amount=amount,
            currency=currency,
            blockchain="bitcoin",
            status="pending",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        
        payload = {
            "inputs": [{"addresses": ["some_sender_bitcoin_address"]}],
            "outputs": [{"addresses": ["some_receiver_bitcoin_address"], "value": int(amount * 10**8)}]  # Convert BTC to Satoshis
        }
        headers = {"Authorization": f"Bearer {BLOCKCYPHER_API_TOKEN}"} if BLOCKCYPHER_API_TOKEN else {}

        response = requests.post(f"{BLOCKCYPHER_API_URL}/txs/new", json=payload, headers=headers)

        if response.status_code == 201:
            tx_data = response.json()
            transaction.id = tx_data.get("tx", {}).get("hash")
            transaction.status = "confirmed"

            
            self.repository.save_transaction(transaction)

            return {"transaction_id": transaction.id, "status": "confirmed"}
        else:
            return {"error": "Failed to process Bitcoin transaction"}

    def get_transaction_status(self, transaction_id: str) -> str:
        """
        Retrieves transaction status from BlockCypher API.
        Updates PostgreSQL and Elasticsearch if the status has changed.
        """
        headers = {"Authorization": f"Bearer {BLOCKCYPHER_API_TOKEN}"} if BLOCKCYPHER_API_TOKEN else {}
        response = requests.get(f"{BLOCKCYPHER_API_URL}/txs/{transaction_id}", headers=headers)

        if response.status_code == 200:
            tx_data = response.json()
            confirmations = tx_data.get("confirmations", 0)
            status = "confirmed" if confirmations > 0 else "pending"

            # 1️⃣ Update transaction status in PostgreSQL and Elasticsearch
            self.repository.update_transaction_status(transaction_id, status)

            return status

        return "unknown"
