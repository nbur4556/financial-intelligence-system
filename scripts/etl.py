from dotenv import load_dotenv
import pandas as pd
import sqlite3
import re
import os

# Configuration
DB_PATH = ""
SCHEMA_PATH = ""
RAW_DATA_DIR = ""

def load_environment():
    global DB_PATH
    global SCHEMA_PATH
    global RAW_DATA_DIR

    load_dotenv()

    DB_PATH = os.getenv("DB_PATH", "")
    SCHEMA_PATH = os.getenv("SCHEMA_PATH", "")
    RAW_DATA_DIR = os.getenv("RAW_DATA_DIR", "")
    print("Environment loaded")

def init_db():
    with open(SCHEMA_PATH, 'r') as f:
        sql = f.read()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executescript(sql)
    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")

#TODO: This helps a bit, but it's not great...
#TODO: White space should be removed
def clean_merchant_name(description):
    """
    Strips noise from bank descriptions.
    """
    if not description:
        return "Unknown"
    
    # Remove common prefixes
    text = re.sub(r'^(Withdrawal (Debit|POS #|Trans To)|Deposit (Debit Ca|ACH))', '', description, flags=re.IGNORECASE)
    
    # Remove common suffixes (Card numbers, Dates, City/State)
    # This is a heuristic: often the merchant name is between '*' or before the first city/state pattern
    # Try to find a pattern like ' *MERCHANT NAME '
    if '*' in text:
        parts = text.split('*')
        if len(parts) > 1:
            text = parts[1]
    
    # Remove trailing noise: dates (MM/DD/YY), Card XXXX, and common city patterns
    text = re.sub(r'\s\d{2}/\d{2}/\d{2}.*$', '', text)
    text = re.sub(r'\sCard\s\d{4}.*$', '', text)
    
    # Remove location-like strings at the end (e.g., 'Franklin TN', 'Brentwood TN')
    # Look for [City] [State] patterns
    text = re.sub(r'\s[A-Z][a-z]+(?:\s[A-Z][a-z]+)*\s[A-Z]{2}\s*$', '', text)
    
    # Final cleanup of whitespace and common trailing characters
    text = text.strip().strip('*').strip('#').strip()
    
    # If the string is too long, it might still have noise. 
    # In a real scenario, we'd refine this regex.
    return text

#TODO: Why do we have a date AND a transaction date?
def process_csvs():
    """Load CSVs from raw_exports and insert into SQLite."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    files = [f for f in os.listdir(RAW_DATA_DIR) if f.endswith('.csv')]
    
    for file in files:
        file_path = os.path.join(RAW_DATA_DIR, file)
        print(f"Processing {file}...")
        
        df = pd.read_csv(file_path)
        
        # Mapping based on the provided sample:
        # "Posting Date" -> date
        # "Description" -> merchant_name (cleaned)
        # "Amount" -> amount
        
        for _, row in df.iterrows():
            raw_desc = str(row['Description'])
            clean_name = clean_merchant_name(raw_desc)
            
            # We insert into transactions. 
            # The relational link to merchants_mapping is handled by the merchant_name.
            cursor.execute(
                "INSERT INTO transactions (date, merchant_name, amount, description, source_file) VALUES (?, ?, ?, ?, ?)",
                (row['Posting Date'], clean_name, row['Amount'], raw_desc, file)
            )
            
    conn.commit()
    conn.close()
    print("Data load complete.")

def report_gaps():
    """Identify merchants that are not yet in the mapping table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = """
        SELECT DISTINCT t.merchant_name 
        FROM transactions t 
        LEFT JOIN merchants_mapping m ON t.merchant_name = m.merchant_name 
        WHERE m.merchant_name IS NULL
    """
    
    cursor.execute(query)
    gaps = cursor.fetchall()
    conn.close()
    
    print("\n--- UNKNOWN MERCHANTS ---")
    for gap in gaps:
        print(gap[0])
    print(f"Total unknown: {len(gaps)}")

if __name__ == "__main__":
    load_environment()
    init_db()
    process_csvs()
    report_gaps()
