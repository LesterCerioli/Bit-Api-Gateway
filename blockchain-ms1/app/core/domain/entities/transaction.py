from dataclasses import dataclass
from datetime import datetime
import uuid

class Transaction:
    def __init__(self, sender: str, recipient: str, amount: float, tx_hash: str = "", status: str = "pending"):
        self.id = str(uuid.uuid4())
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.tx_hash = tx_hash
        self.status = status
        self.created_at = datetime.utcnow()