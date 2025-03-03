use elasticsearch::{Elasticsearch, IndexParts};
use sqlx::PgPool;
use serde_json::json;
use tokio::time::{sleep, Duration};
use chrono::Utc;
use std::sync::Arc;
use crate::infrastructure::logging::log_service::LogService;

pub struct SyncService {
    pool: Arc<PgPool>,
    es_client: Arc<Elasticsearch>,
    log_service: Arc<LogService>,
}

impl SyncService {
    pub fn new(pool: PgPool, es_client: Elasticsearch, log_service: LogService) -> Self {
        Self {
            pool: Arc::new(pool),
            es_client: Arc::new(es_client),
            log_service: Arc::new(log_service),
        }
    }

    pub async fn sync_postgres_to_elasticsearch(&self) -> Result<(), String> {
        let service_name = "SyncService";
        let start_run_time = Utc::now();

        let transactions = match sqlx::query!(
            "SELECT tx_id, sender, receiver, amount, currency, status, created_at FROM transactions"
        )
        .fetch_all(&*self.pool)
        .await
        {
            Ok(data) => data,
            Err(e) => {
                let _ = self.log_service.log_event(
                    service_name,
                    "PostgreSQL query failed",
                    "failure",
                    start_run_time,
                ).await;
                return Err(format!("PostgreSQL error: {}", e));
            }
        };

        for tx in transactions {
            let doc = json!({
                "tx_id": tx.tx_id,
                "sender": tx.sender,
                "receiver": tx.receiver,
                "amount": tx.amount,
                "currency": tx.currency,
                "status": tx.status,
                "created_at": tx.created_at
            });

            let mut attempts = 0;
            let max_attempts = 5;
            let mut success = false;

            while attempts < max_attempts {
                match self.es_client
                    .index(IndexParts::IndexId("transactions", &tx.tx_id))
                    .body(doc.clone())
                    .send()
                    .await
                {
                    Ok(_) => {
                        success = true;
                        break;
                    }
                    Err(e) => {
                        eprintln!("Error indexing transaction {}: {}. Retrying...", tx.tx_id, e);
                        attempts += 1;
                        sleep(Duration::from_secs(2)).await;
                    }
                }
            }

            let end_run_time = Utc::now();
            let duration = end_run_time.signed_duration_since(start_run_time);
            let status = if success { "success" } else { "failure" };

            let _ = self.log_service.log_event(
                service_name,
                &format!("Transaction {} synced to Elasticsearch", tx.tx_id),
                status,
                start_run_time,
            ).await;
        }

        Ok(())
    }
}
