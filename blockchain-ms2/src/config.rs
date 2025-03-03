use dotenvy::dotenv;
use std::env;

pub struct Config {
    pub postgres_url: String,
    pub elasticsearch_url: String,
    pub elasticsearch_index: String,
}

impl Config {
    pub fn new() -> Self {
        dotenv().ok(); // Load .env file

        Self {
            // Construct PostgreSQL connection URL
            postgres_url: format!(
                "host={} port={} dbname={} user={} password={}",
                env::var("POSTGRES_HOST").expect("POSTGRES_HOST not set"),
                env::var("POSTGRES_PORT").expect("POSTGRES_PORT not set"),
                env::var("POSTGRES_DB").expect("POSTGRES_DB not set"),
                env::var("POSTGRES_USER").expect("POSTGRES_USER not set"),
                env::var("POSTGRES_PASSWORD").expect("POSTGRES_PASSWORD not set"),
            ),

            // Construct Elasticsearch URL
            elasticsearch_url: format!(
                "{}:{}",
                env::var("ELASTICSEARCH_HOST").expect("ELASTICSEARCH_HOST not set"),
                env::var("ELASTICSEARCH_PORT").expect("ELASTICSEARCH_PORT not set"),
            ),

            // Load Elasticsearch index name
            elasticsearch_index: env::var("ELASTICSEARCH_INDEX").expect("ELASTICSEARCH_INDEX not set"),
        }
    }
}
