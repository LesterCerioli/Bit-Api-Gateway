from abc import ABC, abstractmethod
from typing import Optional
from domain.entities.transaction import Transaction

class TransactionRepository(ABC):

    @abstractmethod
    def save_transaction(self, transaction: Transaction):
        pass

    def get_transaction(self, tx_hash: str) -> Optional[Transaction]:
        pass