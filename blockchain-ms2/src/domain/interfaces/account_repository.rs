use async_trait::async_trait;
use crate::domain::account::Account;


#[async_trait]
pub trait TransactionRepository {
    async fn get_balance(&self, address: &str) -> Result<Account, String>;
}