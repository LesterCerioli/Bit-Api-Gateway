use serde::{Serialize, Deserialize};

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Transaction {
    pub tx_id: String,       // ID da transação na Solana
    pub from: String,        // Endereço do remetente
    pub to: String,          // Endereço do destinatário
    pub amount: u64,         // Valor em lamports (1 SOL = 1_000_000_000 lamports)
    pub status: String,      // Status da transação (ex: "Pending", "Confirmed")
}

impl Transaction {
    pub fn new(tx_id: String, from: String, to: String, amount: u64, status: String) -> Self {
        Self { tx_id, from, to, amount, status }
    }
}
