from app.core.application.repositories.transaction_repository import TransactionRepository
from app.core.domain.entities.transaction import Transaction
from app.core.infrastructure.database.database import database
from app.core.infrastructure.search.elasticsearch_service import elasticsearch_service

class TransactionRepositoryImpl(TransactionRepository):
    """
    Implements TransactionRepository using PostgreSQL as the primary database
    and synchronizes with Elasticsearch as a cache layer.
    """

    def save_transaction(self, transaction: Transaction) -> None:
        """
        Saves a transaction into PostgreSQL and indexes it in Elasticsearch (cache).
        """
        cursor = database.get_cursor()
        cursor.execute(
            "INSERT INTO transactions (id, user_id, amount, currency, blockchain, status, created_at, updated_at) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (transaction.id, transaction.user_id, transaction.amount, transaction.currency,
             transaction.blockchain, transaction.status, transaction.created_at, transaction.updated_at)
        )

        # Index transaction in Elasticsearch as a cache layer
        transaction_doc = {
            "user_id": transaction.user_id,
            "transaction_id": transaction.id,
            "amount": transaction.amount,
            "currency": transaction.currency,
            "blockchain": transaction.blockchain,
            "status": transaction.status,
            "created_at": transaction.created_at.isoformat(),
            "updated_at": transaction.updated_at.isoformat()
        }
        elasticsearch_service.index_document("transactions", transaction.id, transaction_doc)

    def get_transaction(self, transaction_id: str) -> Transaction:
        """
        Retrieves a transaction from Elasticsearch cache first.
        If not found, fetch from PostgreSQL and update cache.
        """
        
        transaction_data = elasticsearch_service.get_document("transactions", transaction_id)
        if transaction_data:
            return Transaction(**transaction_data)

        # 2️⃣ If not in cache, fetch from PostgreSQL
        cursor = database.get_cursor()
        cursor.execute("SELECT * FROM transactions WHERE id = %s", (transaction_id,))
        row = cursor.fetchone()

        if row:
            transaction = Transaction(*row)

            
            transaction_doc = {
                "user_id": transaction.user_id,
                "transaction_id": transaction.id,
                "amount": transaction.amount,
                "currency": transaction.currency,
                "blockchain": transaction.blockchain,
                "status": transaction.status,
                "created_at": transaction.created_at.isoformat(),
                "updated_at": transaction.updated_at.isoformat()
            }
            elasticsearch_service.index_document("transactions", transaction.id, transaction_doc)
            
            return transaction
        
        return None

    def search_transactions_by_user(self, user_id: str):
        """
        Searches transactions by user ID using Elasticsearch.
        """
        query = {"match": {"user_id": user_id}}
        results = elasticsearch_service.search_documents("transactions", query)
        return results

    def update_transaction_status(self, transaction_id: str, status: str) -> None:
        """
        Updates the transaction status in PostgreSQL and Elasticsearch.
        """
        cursor = database.get_cursor()
        cursor.execute("UPDATE transactions SET status = %s, updated_at = NOW() WHERE id = %s", (status, transaction_id))

        elasticsearch_service.update_document("transactions", transaction_id, {"status": status})

    def delete_transaction(self, transaction_id: str) -> None:
        """
        Deletes a transaction from PostgreSQL and Elasticsearch cache.
        """
        cursor = database.get_cursor()
        cursor.execute("DELETE FROM transactions WHERE id = %s", (transaction_id,))

        elasticsearch_service.delete_document("transactions", transaction_id)
