

class TransactionReoisutiryPostgres(TransactionRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def save_transaction(self, transaction: Transaction):
        self.db_session.add(transaction)
        self.db_session.commit()
        return transaction
    
    def get_transaction(self, tx_hash: str) -> Optional[Transaction]:
        return self.db_session.query(Transaction).filter_by(tx_hash=tx_hash).first()