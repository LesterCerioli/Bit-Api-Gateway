use tokio_postgres::{NoTls, Client, Error};
use crate::config::Config;

pub async fn connect_to_postgres() -> Result<Client, Error> {
    let config = Config::new();
    let (client, connection) = tokio_postgres::connect(&config.postgres_url, NoTls).await?;
    
    tokio::spawn(async move {
        if let Err(e) = connection.await {
            eprintln!("PostgreSQL connection error: {}", e);
        }
    });

    Ok(client)
}
