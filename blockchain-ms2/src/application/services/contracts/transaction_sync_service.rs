use async_trait::async_trait;
use tokio::sync::mpsc;
use elasticsearch::Elasticsearch;

#[async_trait]
pub trait TransactionSyncService: Send + Sync {
    async fn process_events(&self, receiver: mpsc::Receiver<String>);
}