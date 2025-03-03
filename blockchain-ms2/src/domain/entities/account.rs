use serde::{Serialize, Deserialize};

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Account {
    pub address: String,  // Endereço público da conta
    pub balance: u64,     // Saldo em lamports
}

impl Account {
    pub fn new(address: String, balance: u64) -> Self {
        Self { address, balance }
    }
}
