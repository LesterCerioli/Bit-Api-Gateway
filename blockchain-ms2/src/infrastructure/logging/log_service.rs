use sqlx::PgPool;
use chrono::{Utc, DateTime};
use std::sync::Arc;

pub struct LogService {
    pool: Arc<PgPool>,
}

impl LogService {
    pub fn new(pool: PgPool) -> Self {
        Self {
            pool: Arc::new(pool),
        }
    }

    pub async fn log_event(
        &self,
        service_name: &str,
        event: &str,
        status: &str,
        start_run_time: DateTime<Utc>,
    ) -> Result<(), String> {
        let end_run_time = Utc::now();
        let duration = end_run_time.signed_duration_since(start_run_time);
        
        let max_attempts = 5;
        let mut attempts = 0;

        while attempts < max_attempts {
            match sqlx::query!(
                "INSERT INTO logs (service_name, event, date, start_run_time, end_run_time, status, duration)
                 VALUES ($1, $2, $3, $4, $5, $6, $7)",
                service_name,
                event,
                Utc::now(),
                start_run_time,
                end_run_time,
                status,
                duration.num_seconds()
            )
            .execute(&*self.pool)
            .await
            {
                Ok(_) => {
                    println!("[LOG SUCCESS] {} - {}", service_name, event);
                    return Ok(());
                }
                Err(e) => {
                    eprintln!("[LOG ERROR] Attempt {}/{} - Failed to insert log: {}", attempts + 1, max_attempts, e);
                    attempts += 1;
                    sleep(Duration::from_secs(2)).await; 
                }
            }
        }

        Err(format!(
            "[LOG FAILURE] Could not insert log after {} attempts: Service: {}, Event: {}",
            max_attempts, service_name, event
        ))
    }
}
