use async_trait::async_trait;
use tokio_postgres::{NoTls, Error};
use tokio::sync::mpsc;
use std::sync::Arc;
use sqlx::PgPool;
use chrono::Utc;
use crate::application::services::contracts::transaction_listener_service::TransactionListenerService;
use crate::config::Config;
use crate::infrastructure::logging::log_service::LogService;

pub struct TransactionListenerServiceImpl {
    db_url: Arc<String>,
    pool: Arc<PgPool>,
    log_service: Arc<LogService>,
}

impl TransactionListenerServiceImpl {
    pub fn new(pool: PgPool) -> Self {
        let config = Config::new();
        let log_service = Arc::new(LogService::new(pool.clone()));

        Self {
            db_url: Arc::new(config.postgres_url),
            pool: Arc::new(pool),
            log_service,
        }
    }
}

#[async_trait]
impl TransactionListenerService for TransactionListenerServiceImpl {
    async fn listen_for_transactions(&self, sender: mpsc::Sender<String>) -> Result<(), Error> {
        let service_name = "Transaction Listener";
        let start_time = Utc::now();

        let (client, connection) = match tokio_postgres::connect(&self.db_url, NoTls).await {
            Ok((client, connection)) => {
                tokio::spawn(async move {
                    if let Err(e) = connection.await {
                        eprintln!("Error connecting to PostgreSQL: {}", e);
                    }
                });
                client
            }
            Err(e) => {
                let _ = self.log_service.log_event(service_name, "Failed to connect to PostgreSQL", "failure", start_time).await;
                return Err(e);
            }
        };

        if let Err(e) = client.execute("LISTEN new_transaction;", &[]).await {
            let _ = self.log_service.log_event(service_name, "Failed to execute LISTEN command", "failure", start_time).await;
            return Err(e);
        }

        let _ = self.log_service.log_event(service_name, "Started listening for transactions", "success", start_time).await;

        loop {
            client.notifications().await?;
            if let Some(notification) = client.notifications().try_recv() {
                let start_time = Utc::now();
                let payload = notification.payload();

                match sender.send(payload.to_string()).await {
                    Ok(_) => {
                        let _ = self.log_service.log_event(service_name, "Transaction received and processed", "success", start_time).await;
                    }
                    Err(e) => {
                        let _ = self.log_service.log_event(service_name, &format!("Failed to process transaction: {}", e), "failure", start_time).await;
                    }
                }
            }
        }
    }
}
