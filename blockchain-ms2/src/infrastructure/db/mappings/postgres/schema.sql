
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    balance NUMERIC(18, 8) NOT NULL DEFAULT 0,
    currency VARCHAR(3) NOT NULL CHECK (currency IN ('USD', 'EUR', 'BTC', 'ETH')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tx_id VARCHAR(255) UNIQUE NOT NULL,
    sender UUID NOT NULL,
    receiver UUID NOT NULL,
    amount NUMERIC(18, 8) NOT NULL,
    currency VARCHAR(3) NOT NULL CHECK (currency IN ('USD', 'EUR', 'BTC', 'ETH')),
    status VARCHAR(50) NOT NULL CHECK (status IN ('pending', 'completed', 'failed')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE sync_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    start_run_time TIMESTAMP NOT NULL,
    end_run_time TIMESTAMP NOT NULL,
    status VARCHAR(50) NOT NULL CHECK (status IN ('success', 'failure', 'retrying')),
    duration INTERVAL NOT NULL
);
CREATE TABLE IF NOT EXISTS logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    service_name VARCHAR(100) NOT NULL,
    event VARCHAR(255) NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    start_run_time TIMESTAMP NOT NULL,
    end_run_time TIMESTAMP NOT NULL,
    status VARCHAR(50) NOT NULL CHECK (status IN ('success', 'failure', 'retrying')),
    duration INTERVAL NOT NULL
);
