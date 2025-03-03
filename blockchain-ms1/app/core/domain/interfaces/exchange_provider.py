from abc import ABC, abstractmethod
class ExchangeProvider(ABC):

    @abstractmethod
    def get_exchange_rate(self, currency: str) -> float:
        pass