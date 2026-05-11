# Implementation Plan: Financial Intelligence System

## Tech Stack
- **Data Storage:** SQLite (Local-first, portable)
- **Processing:** Python (Pandas)
- **Analysis:** Jupyter Notebooks
- **Version Control:** Git (Code & Strategy only; Data excluded)

## Database Architecture
Two-table relational structure to ensure auditability and easy re-categorization:
1. `transactions` table: Raw transaction data (Date, Amount, Merchant, etc.)
2. `merchants_mapping` table: Relation between Merchant names and Category/Subcategory.

## Phase 1: Infrastructure & Schema
- [ ] Define the `.gitignore` to protect sensitive data (`.db`, `raw_exports/`).
- [ ] Create `schema.sql` to initialize the database structure.
- [ ] Setup the directory structure:
    - `/raw_exports`: Landing zone for bank CSVs.
    - `/scripts`: ETL and processing logic.
    - `/notebooks`: Reporting and "Board Meeting" analysis.

## Phase 2: ETL Pipeline
- [ ] Build Python script to parse various bank CSV formats.
- [ ] Implement the mapping logic (Join `transactions` $\rightarrow$ `merchants_mapping`).
- [ ] Create a mechanism to identify "Uncategorized" transactions for AI review.

## Phase 3: Analysis & Reporting
- [ ] Build Jupyter Notebooks to calculate KPIs:
    - Burn Rate
    - Savings Rate
    - Efficiency Ratio
    - Variance Analysis
- [ ] Create visualizations for monthly and quarterly trends.

## Phase 4: Agentic Automation
- [ ] Develop a "Gap Analysis" script to find new/unknown merchants.
- [ ] Integrate LLM to suggest categories for unknown merchants.
- [ ] Implement an approval workflow to commit AI suggestions to the mapping table.

## Security & Portability Protocol
- **No binary data in Git:** Only scripts, schema, and strategy are committed.
- **Local First:** Database file stays on local disks or secure vaults.
- **Migration Path:** Maintain SQL compatibility to allow future migration to Postgres if needed.
