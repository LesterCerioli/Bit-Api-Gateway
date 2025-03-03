use async_trait::async_trait;
use elasticsearch::{Elasticsearch, IndexParts};
use serde_json::Value;
use tokio::sync::mpsc;
use std::sync::Arc;
use chrono::Utc;
use crate::application::services::contracts::transaction_sync_service::TransactionSyncService;
use crate::infrastructure::logging::log_service::LogService;

pub struct TransactionSyncServiceImpl {
    es_client: Arc<Elasticsearch>,
    log_service: Arc<LogService>,
}

impl TransactionSyncServiceImpl {
    pub fn new(es_client: Elasticsearch, log_service: LogService) -> Self {
        Self {
            es_client: Arc::new(es_client),
            log_service: Arc::new(log_service),
        }
    }
}

#[async_trait]
impl TransactionSyncService for TransactionSyncServiceImpl {
    async fn process_events(&self, mut receiver: mpsc::Receiver<String>) {
        let service_name = "Transaction Sync Service";

        while let Some(event) = receiver.recv().await {
            let start_run_time = Utc::now();

            match serde_json::from_str::<Value>(&event) {
                Ok(transaction) => {
                    let tx_id = transaction["tx_id"].as_str().unwrap_or("");
                    let doc = transaction.clone();

                    let response = self.es_client
                        .index(IndexParts::IndexId("transactions", tx_id))
                        .body(doc)
                        .send()
                        .await;

                    let end_run_time = Utc::now();
                    let duration = end_run_time.signed_duration_since(start_run_time);

                    match response {
                        Ok(_) => {
                            let _ = self.log_service.log_event(
                                service_name,
                                &format!("Transaction {} synchronized with Elasticsearch", tx_id),
                                "success",
                                start_run_time,
                            ).await;
                        }
                        Err(e) => {
                            let _ = self.log_service.log_event(
                                service_name,
                                &format!("Error indexing transaction {}: {}", tx_id, e),
                                "failure",
                                start_run_time,
                            ).await;
                        }
                    }
                }
                Err(e) => {
                    let _ = self.log_service.log_event(
                        service_name,
                        &format!("Error processing JSON: {}", e),
                        "failure",
                        start_run_time,
                    ).await;
                }
            }
        }
    }
}
