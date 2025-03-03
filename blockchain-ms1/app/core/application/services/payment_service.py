from app.core.domain.entities.transaction import Transaction
from app.core.application.repositories.transaction_repository import TransactionRepository
from datetime import datetime
import uuid

class PaymentService:
    def __init__(self, repository: TransactionRepository):
        self.repository = repository

    def process_payment(self, user_id: str, amount: float, currency: str, blockchain: str) -> str:
        """
        Processes a payment by storing it in the database and indexing in Elasticsearch.
        """
        transaction = Transaction(
            id=str(uuid.uuid4()),
            user_id=user_id,
            amount=amount,
            currency=currency,
            blockchain=blockchain,
            status="pending",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        self.repository.save_transaction(transaction)
        return transaction.id