from abc import ABC, abstractmethod
from app.core.domain.entities.transaction import Transaction

class transactionRepository(ABC):
    """
    Defines the contract for transaction repository implementations.
    Enforces the Dependency Inversion Principle (DIP) from SOLID.
    """

     @abstractmethod
    def save_transaction(self, transaction: Transaction) -> None:
        """Saves a transaction to the database."""
        pass

    @abstractmethod
    def get_transaction(self, transaction_id: str) -> Transaction:
        """Retrieves a transaction by its ID."""
        pass

    @abstractmethod
    def update_transaction_status(self, transaction_id: str, status: str) -> None:
        """Updates the status of an existing transaction."""
        pass