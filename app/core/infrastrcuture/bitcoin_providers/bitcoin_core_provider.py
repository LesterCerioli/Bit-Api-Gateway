import requests
from app.core.domain.interfaces.payment_gateway import PaymentGateway
from app.core.domain.entities.transaction import Transaction
from config import BITCOIN_RPC_URL

class BitcoinCoreProvider(PaymentGateway):
    def create_transaction(self, transaction: Transaction):
        payload = {"to": "some_bitcoin_address", "amount": transaction.amount}
        response = requests.post(f"{BITCOIN_RPC_URL}/send_transaction", json=payload)
        return response.json()["txid"]

    def get_transaction_status(self, transaction_id: str) -> str:
        response = requests.get(f"{BITCOIN_RPC_URL}/tx/{transaction_id}")
        return response.json()["status"]