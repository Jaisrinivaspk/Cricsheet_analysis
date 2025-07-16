import pandas as pd
import sqlite3
import os

# File paths
DB_PATH = "database/cricsheet.db"
MATCHES_CSV = "processing/matches.csv"
DELIVERIES_CSV = "processing/deliveries.csv"

# Ensure the database folder exists
os.makedirs("database", exist_ok=True)

# Load CSVs
print("📥 Loading CSV files...")
matches_df = pd.read_csv(MATCHES_CSV)
deliveries_df = pd.read_csv(DELIVERIES_CSV)

# Connect to SQLite
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create tables
print("🛠️ Creating tables...")

cursor.execute("DROP TABLE IF EXISTS matches")
cursor.execute("""
CREATE TABLE matches (
    match_id TEXT PRIMARY KEY,
    date TEXT,
    venue TEXT,
    match_type TEXT,
    gender TEXT,
    season TEXT,
    event TEXT,
    team1 TEXT,
    team2 TEXT,
    toss_winner TEXT,
    toss_decision TEXT,
    winner TEXT,
    by_runs INTEGER,
    by_wickets INTEGER
)
""")

cursor.execute("DROP TABLE IF EXISTS deliveries")
cursor.execute("""
CREATE TABLE deliveries (
    match_id TEXT,
    batting_team TEXT,
    over INTEGER,
    batter TEXT,
    bowler TEXT,
    non_striker TEXT,
    runs_batter INTEGER,
    runs_extras INTEGER,
    runs_total INTEGER,
    wicket_kind TEXT,
    wicket_player_out TEXT
)
""")

# Load data into SQLite
print("📤 Inserting into database...")
matches_df.to_sql("matches", conn, if_exists="append", index=False)
deliveries_df.to_sql("deliveries", conn, if_exists="append", index=False)

conn.commit()
conn.close()


print(f"🗂️ SQLite DB saved at: {DB_PATH}")
