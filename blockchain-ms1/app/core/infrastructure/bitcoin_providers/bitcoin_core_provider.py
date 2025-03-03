import requests
from app.core.domain.interfaces.payment_gateway import PaymentGateway
from app.core.domain.entities.transaction import Transaction
from config import BITCOIN_RPC_URL

class BitcoinCoreProvider(PaymentGateway):
    """
    BitcoinCoreProvider handles Bitcoin transactions for multiple accounts.
    Uses PostgreSQL for storage and Elasticsearch for fast search.
    """

     def __init__(self):
        self.repository = TransactionRepositoryImpl()
    
    def create_transaction(self, transaction: Transaction):
        """
        Creates a new Bitcoin transaction using Bitcoin Core.
        Allows transactions from multiple accounts.
        """

        transaction = Transaction(
            id=str(uuid.uuid4()),  # Unique Transaction ID
            user_id=user_id,
            amount=amount,
            currency=currency,
            blockchain="bitcoin",
            status="pending",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        
         payload = {
            "from": sender_address,
            "to": receiver_address,
            "amount": amount
        }
        response = requests.post(f"{BITCOIN_RPC_URL}/send_transaction", json=payload)

        if response.status_code == 200:
            txid = response.json().get("txid")
            transaction.id = txid  # Assign transaction ID from Bitcoin Core
            transaction.status = "confirmed"

            # Save transaction to PostgreSQL and Elasticsearch
            self.repository.save_transaction(transaction)

            return {"transaction_id": txid, "status": "confirmed"}
        else:
            return {"error": "Failed to process Bitcoin transaction"}

    def get_transaction_status(self, transaction_id: str) -> str:
        """
        Retrieves transaction status from Bitcoin Core API.
        Updates PostgreSQL & Elasticsearch if status has changed.
        """
        
        
        response = requests.get(f"{BITCOIN_RPC_URL}/tx/{transaction_id}")
        if response.status_code == 200:
            status = response.json().get("status")
            
            self.repository.update_transaction_status(transaction_id, status)

            return status

        return "unknown"