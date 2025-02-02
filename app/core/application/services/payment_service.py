

class PaymentService:
    def __init__(self, gateway: PaymentGateway, repository: TransactionRepository):
        self.gateway = gateway
        self.repository = repository
    def process_payment(self, user_id? str, amount: float, currency: str, blockchain: str) -> str:
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
        txid = self.gateway.create_transaction(transaction)
        transaction.status = "confirmed"
        self.repository.save_transaction(transaction)
        return txid