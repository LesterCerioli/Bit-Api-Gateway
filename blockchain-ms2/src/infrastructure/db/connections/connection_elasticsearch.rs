use elasticsearch::Elasticsearch;
use crate::config::Config;

pub fn connect_to_elasticsearch() -> Elasticsearch {
    let config = Config::new();
    Elasticsearch::new(elasticsearch::http::transport::Transport::single_node(&config.elasticsearch_url).unwrap())
}
