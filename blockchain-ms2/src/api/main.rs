mod config;
mod application;
mod infrastructure;

use config::Config;
use application::services::implementations::transaction_sync_service_impl::TransactionSyncServiceImpl;
use application::services::contracts::transaction_sync_service::TransactionSyncService;
use infrastructure::db::connections::{connection_postgres, connection_elasticsearch};
use infrastructure::logging::log_service::LogService;

use elasticsearch::Elasticsearch;
use tokio::sync::mpsc;

#[tokio::main]
async fn main() {
    // Load environment variables
    let config = Config::new();

    // Initialize PostgreSQL Connection
    let pool = connection_postgres::connect_to_postgres()
        .await
        .expect("Failed to connect to PostgreSQL");

    let es_client = elasticsearch::Elasticsearch::default();
    let log_service = LogService::new(pool.clone());

    let sync_service = SyncService::new(pool.clone(), es_client, log_service);

    match sync_service.sync_postgres_to_elasticsearch().await {
        Ok(_) => println!("Synchronization completed successfully"),
        Err(e) => eprintln!("Synchronization failed: {}", e),
    };
}
