from abc import ABC, abstractmethod
from app.core.domain.entities.transaction import Transaction

class PaymentGateway(ABC):

    @abstractmethod
    def create_trasaction(self, transaction? Transaction) -> str:
        pass
    
    @abstractmethod
    def get_transaction_status(self, transaction_id: str) -> str:
        pass

