use async_trait::async_trait;
use tokio::sync::mpsc;
use tokio_postgres::Error;

#[async_trait]
pub trait TransactionListenerService: Send + Sync {
    async fn listen_for_transactions(&self, sender: mpsc::Sender<String>) -> Result<(), Error>;
}