-- Financial Intelligence Schema
-- Version: 1.0

-- Table for Merchant Mappings
-- This allows us to change a category once and update all historical transactions
CREATE TABLE IF NOT EXISTS merchants_mapping (
    merchant_id INTEGER PRIMARY KEY AUTOINCREMENT,
    merchant_name TEXT UNIQUE NOT NULL,
    category TEXT NOT NULL, -- Fixed, Variable, Capital, Debt
    subcategory TEXT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for Raw Transactions
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id TEXT UNIQUE NOT NULL,
    date TEXT NOT NULL,
    merchant_name TEXT NOT NULL,
    amount REAL NOT NULL,
    description TEXT,
    source_file TEXT,
    transaction_date DATE,
    FOREIGN KEY (merchant_name) REFERENCES merchants_mapping(merchant_name)
);

-- Indices for performance on analytical queries
CREATE INDEX IF NOT EXISTS idx_trans_date ON transactions(date);
CREATE INDEX IF NOT EXISTS idx_trans_merchant ON transactions(merchant_name);
